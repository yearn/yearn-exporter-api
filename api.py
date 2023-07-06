from flask import Flask, jsonify, request
from flask_cors import CORS
import time
from grafana import get_for, get_partners_for

app = Flask(__name__)
CORS(app)

NETWORKS = ['eth', 'ftm', 'opti', 'arbi']

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


@app.route("/partners/total", methods=['GET'])
def partners_total():
    return jsonify(get_for('partners_total', _get_ts(), UNIT_USD))


@app.route("/partners/count", methods=['GET'])
def partners_count():
    return jsonify(get_for('partners_count', _get_ts(), ''))


@app.route("/partners/<partner>/<param>", methods=['GET'])
def partners_indiv(partner, param):
    res = get_partners_for(partner, param, _get_ts(), UNIT_USD)
    return jsonify(res)


def _get_ts():
    ts = request.args.get('ts', None)
    if not ts:
        return int(time.time())
    try:
        ts_int = int(ts)
        if ts_int > 0:
            return ts_int
    except ValueError:
        raise ValueError("Wrong request param specified (ts must be an int).")

def create_app():
    return app

