from flask import Flask, jsonify, request
from grafana import get_for

app = Flask(__name__)

@app.route("/tvl", methods=['GET'])
def tvl():
    ts = _get_ts()
    res = get_for('tvl_total', ts) | get_for('tvl_eth', ts) | get_for('tvl_ftm', ts)
    return jsonify(res)


@app.route("/tvl_total", methods=['GET'])
def tvl_total():
    return jsonify(get_for('tvl_total', _get_ts()))


@app.route("/tvl_eth", methods=['GET'])
def tvl_eth():
    return jsonify(get_for('tvl_eth', _get_ts()))


@app.route("/tvl_ftm", methods=['GET'])
def tvl_ftm():
    return jsonify(get_for('tvl_ftm', _get_ts()))


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
