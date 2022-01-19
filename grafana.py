import os
import time
import requests
import logging
logger = logging.getLogger('grafana')
logging.basicConfig(level=logging.DEBUG)

# TODO check the queries are correct
QUERY_DELEGATED = """(sum((yearn_strategy{network=\"ETH\", param=\"delegatedAssets\", experimental=\"false\"} / 1000000000000000000 > 0) * on(vault, version)
group_left yearn_vault{network=\"ETH\", param=\"token price\", experimental=\"false\"}) or vector(0))"""

QUERY_FTM_TVL = """(sum(ironbank{network=\"FTM\", param=\"tvl\"}) or vector(0))
+ (sum(yearn_vault{network=\"FTM\", param=\"tvl\"}) or vector(0))
- (sum((yearn_strategy{network=\"FTM\", param=\"delegatedAssets\", experimental=\"false\"} / 1000000000000000000 > 0) * on(vault, version)
group_left yearn_vault{network=\"FTM\", param=\"token price\", experimental=\"false\"}) or vector(0))"""

QUERY_ETH_TVL = """(sum(yearn{network=\"ETH\", param=\"tvl\"}) or vector(0))
+ (avg(yearn{network=\"ETH\", param=\"vecrv balance\"}) * avg(yearn{network=\"ETH\", param=\"crv price\"}) or vector(0))
+ (sum(yearn_vault{network=\"ETH\", param=\"tvl\"}) or vector(0)) + (sum(iearn{network=\"ETH\", param=\"tvl\"}) or vector(0))
+ (sum(ironbank{network=\"ETH\", param=\"tvl\"}) or vector(0))
- (sum((yearn_strategy{network=\"ETH\", param=\"delegatedAssets\", experimental=\"false\"} / 1000000000000000000 > 0) * on(vault, version)
group_left yearn_vault{network=\"ETH\", param=\"token price\", experimental=\"false\"}) or vector(0))"""

QUERY_TOTAL_TVL = QUERY_ETH_TVL + " + " + QUERY_FTM_TVL

queries = {
    'tvl_total': QUERY_TOTAL_TVL,
    'tvl_eth': QUERY_ETH_TVL,
    'tvl_ftm': QUERY_FTM_TVL
}

def get_for(key, ts):
    if key not in queries:
        raise ValueError(f"No query found for key {key}!")

    return _ds_query(key, queries[key], ts)


def _ds_query(key, query, ts):
    base_url = os.environ["DS_QUERY_BASE_URL"]
    if not ts:
        ts = int(time.time())

    to_millis = int(ts * 1e3)
    from_millis = int(to_millis - 600 * 1e3)

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
                "datasourceId": 1
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
        res = response.json()
        data = res['results']['A']['frames'][0]['data']
        timestamps = data['values'][0]
        values = data['values'][1]
        value = 0
        for i in range(len(values)-1, -1, -1):
            if values[i] > 0:
                value = values[i]
                break

        return { key: value, 'timestamp': ts }
