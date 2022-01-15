import os
import time
import requests
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("grafana")

def get_latest_tvl_total():
    # TODO read query definition from grafana panel id
    query = "(sum(yearn{network=\"ETH\", param=\"tvl\"}) or vector(0)) + (avg(yearn{network=\"ETH\", param=\"vecrv balance\"}) * avg(yearn{network=\"ETH\", param=\"crv price\"}) or vector(0)) + (sum(yearn_vault{network=\"ETH\", param=\"tvl\"}) or vector(0)) + (sum(iearn{network=\"ETH\", param=\"tvl\"}) or vector(0)) + (sum(ironbank{network=\"ETH\", param=\"tvl\"}) or vector(0)) - (sum((yearn_strategy{network=\"ETH\", param=\"delegatedAssets\", experimental=\"false\"} / 1000000000000000000 > 0) * on(vault, version) group_left yearn_vault{network=\"ETH\", param=\"token price\", experimental=\"false\"}) or vector(0)) + (sum(ironbank{network=\"FTM\", param=\"tvl\"}) or vector(0)) + (sum(yearn_vault{network=\"FTM\", param=\"tvl\"}) or vector(0))"
    return _ds_query("tvl_total", query)


def get_latest_tvl_eth():
    # TODO read query definition from grafana panel id
    query = "(sum(yearn{network=\"ETH\", param=\"tvl\"}) or vector(0)) + (avg(yearn{network=\"ETH\", param=\"vecrv balance\"}) * avg(yearn{network=\"ETH\", param=\"crv price\"}) or vector(0)) + (sum(yearn_vault{network=\"ETH\", param=\"tvl\"}) or vector(0)) + (sum(iearn{network=\"ETH\", param=\"tvl\"}) or vector(0)) + (sum(ironbank{network=\"ETH\", param=\"tvl\"}) or vector(0)) - (sum((yearn_strategy{network=\"ETH\", param=\"delegatedAssets\", experimental=\"false\"} / 1000000000000000000 > 0) * on(vault, version) group_left yearn_vault{network=\"ETH\", param=\"token price\", experimental=\"false\"}) or vector(0))"
    return _ds_query("tvl_eth", query)


def get_latest_tvl_ftm():
    # TODO read query definition from grafana panel id
    query = "(sum(ironbank{network=\"FTM\", param=\"tvl\"}) or vector(0)) + (sum(yearn_vault{network=\"FTM\", param=\"tvl\"}) or vector(0))"
    return _ds_query("tvl_ftm", query)


def _ds_query(key, query):
    base_url = os.environ["DS_QUERY_BASE_URL"]
    to_millis = int(time.time() * 1000)
    from_millis = int(to_millis - 300 * 1000)

    url = f'{base_url}/api/ds/query'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    # TODO make this more stable accross new deployments
    # this could be done by an authed call to api/datasources to get the uid
    data = {
        "queries": [
            {
                "datasource": { "uid": "PBFE396EC0B189D67", "type": "prometheus" },
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
        values = res['results']['A']['frames'][0]['data']['values'][1]
        logger.debug(values)
        for i in range(len(values)-1, -1, -1):
            value = values[i]
            logger.debug(value)
            if value > 0:
                return { key: value }

        raise ValueError(f"Failed to get the latest value for the key '{key}'!")
