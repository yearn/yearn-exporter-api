import logging
import os
from collections import defaultdict

import requests

logger = logging.getLogger('grafana')
logging.basicConfig(level=logging.WARN)

# Explanation of query
# sum v2 vaults does not subtract delegated deposits
QUERY_FTM_TVL = """sum(sum by (vault, version, address) (yearn_vault{param=\"tvl\", experimental=\"false\", network=\"FTM\"})) or vector(0)"""

QUERY_ETH_TVL = """sum(sum by (vault, version, address) (yearn_vault{param=\"tvl\", experimental=\"false\", network=\"ETH\"})) or vector(0)"""

QUERY_styETH_TVL = """yeth{product=\"st-yETH\",param=\"tvl\"}"""

QUERY_OPTI_TVL = """sum(sum by (vault, version, address) (yearn_vault{param=\"tvl\", experimental=\"false\", network=\"OPTI\"})) or vector(0)"""

QUERY_BASE_TVL = """sum(sum by (vault, version, address) (yearn_vault{param=\"tvl\", experimental=\"false\", network=\"BASE\"})) or vector(0)"""

QUERY_ARBI_TVL = """sum(sum by (vault, version, address) (yearn_vault{param=\"tvl\", experimental=\"false\", network=\"ARB\"})) or vector(0)"""

QUERY_TOTAL_TVL = QUERY_ETH_TVL + " + " + QUERY_FTM_TVL + " + " + QUERY_OPTI_TVL + " + " + QUERY_ARBI_TVL + " + " + QUERY_BASE_TVL + " + " + QUERY_styETH_TVL

# Partner queries
# Count of unique entries in the partner field
QUERY_PAR_CNT = """(count(count(partners) by (partner)))"""
# Sum of the payouts measured in USD up-to-date
QUERY_PAR_TOTAL = """(sum(partners{param=\"payout_usd_total\"}))"""
# Get individual payouts data
QUERY_PAR_INDIV = """(partners{{partner=\"{0}\", param=\"{1}\"}})"""



queries = {
    'tvl_total': QUERY_TOTAL_TVL,
    'tvl_eth': QUERY_ETH_TVL,
    'tvl_ftm': QUERY_FTM_TVL,
    'tvl_opt': QUERY_OPTI_TVL,
    'tvl_arb': QUERY_ARBI_TVL,
    'tvl_base': QUERY_BASE_TVL,
    'tvl_styETH': QUERY_styETH_TVL,  
    'partners_count': QUERY_PAR_CNT,
    'partners_total': QUERY_PAR_TOTAL,
}


def get_for(key, ts, unit):
    if key not in queries:
        raise ValueError(f"No query found for key {key}!")

    if ts < 1581467400: # yearn inception 2020-02-12
        return { key: 0, 'ts': ts, 'unit': unit }

    res = _ds_query(queries[key], ts)
    return { key: _ds_parse_value(res), 'ts': ts, 'unit': unit}


def _ds_parse_value(response):
    frames = response['results']['A']['frames']
    if len(frames) == 0:
      return 0

    data = frames[0]['data']
    values = data['values'][1]
    value = 0
    for i in range(len(values)-1, -1, -1):
        if values[i] > 0:
            value = round(values[i], 2)
            break
    return value


def _ds_query(query, ts):
    base_url = os.environ["BASE_URL"]

    to_millis = int(ts * 1e3)
    from_millis = int(to_millis - 3600 * 1e3)

    url = f'{base_url}/api/ds/query'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    data = {
        "queries": [
            {
                "expr": query,
                "utcOffsetSec": 0,
                "datasourceId": 1,
                "maxDataPoints": 50
            }
        ],
        "from": str(from_millis), "to": str(to_millis)
    }

    with requests.Session() as session:
        response = session.post(
            url = url,
            headers = headers,
            json = data
        )
    return response.json()


def _ds_parse_partners(token_bals, usd_bals):
    data = token_bals['results']['A']['frames']
    usd_data = usd_bals['results']['A']['frames']
    output = defaultdict(dict)
    for series, usd_series in zip(data, usd_data):
        values = series['data']['values'][1]
        usd_values = usd_series['data']['values'][1]
        value = 0
        usd_value = 0
        for i in range(len(values)-1, -1, -1):
            if values[i] > 0:
                value = round(values[i], 2)
                usd_value = round(usd_values[i], 2)
                break
        labels = series['schema']['fields'][1]['labels']
        network = labels['network']
        output[network][labels['token_address']] = {
            'balance': value,
            'tvl': usd_value,
            'token': labels['token'],
            'bucket': labels['bucket'],
        }
    return output


def get_partners_for(partner, param, ts, unit):
    if ts < 1581467400: # yearn inception 2020-02-12
        return { key: 0, 'ts': ts, 'unit': unit }

    usd_queries = {
        'balance':          'balance_usd',
        'payout_daily':     'payout_usd_daily',
        'payout_weekly':    'payout_usd_weekly',
        'payout_monthly':   'payout_usd_monthly',
        'payout_total':     'payout_usd_total',
    }

    if param not in usd_queries:
        raise ValueError(f"No query available for param {param}!")

    key = f'partners_indiv_{partner.lower()}_{param.lower()}'
    query = QUERY_PAR_INDIV.format(partner, param)
    token_bals = _ds_query(query, ts)
    query = QUERY_PAR_INDIV.format(partner, usd_queries[param])
    usd_bals = _ds_query(query, ts)
    #return res['results']['A']['frames'][0]['schema']['fields'][1]['labels']['network']
    return { key: _ds_parse_partners(token_bals, usd_bals), 'ts': ts, 'unit': unit }
