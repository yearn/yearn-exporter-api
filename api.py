from flask import Flask, jsonify, request
from grafana import get_for

app = Flask(__name__)

NETWORKS = ['eth', 'ftm']

UNIT_USD = 'USD'

@app.route("/tvl", methods=['GET'])
def tvl():
    ts = _get_ts()
    res = get_for('tvl_total', ts, UNIT_USD)
    for network in NETWORKS:
        key = f"tvl_{network.lower()}"
        res = res | get_for(key, ts, UNIT_USD)
    return jsonify(res)


@app.route("/tvl/total", methods=['GET'])
def tvl_total():
    return jsonify(get_for('tvl_total', _get_ts(), UNIT_USD))


@app.route("/tvl/<network>", methods=['GET'])
def tvl_network(network):
    if network and network.lower() not in NETWORKS:
        return "Network not found!", 400

    key = f"tvl_{network.lower()}"
    res = get_for(key, _get_ts(), UNIT_USD)
    return jsonify(res)


def _get_ts():
    ts = request.args.get('ts', None)
    if not ts:
        return None
    try:
        ts_int = int(ts)
        if ts_int > 0:
            return ts_int
    except ValueError:
        raise ValueError("Wrong request param specified (ts must be an int).")
