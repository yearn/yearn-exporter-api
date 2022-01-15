from flask import Flask, jsonify
from grafana import get_latest_tvl_total, get_latest_tvl_eth, get_latest_tvl_ftm

app = Flask(__name__)

@app.route("/tvl", methods=['GET'])
def tvl():
    tvl_total = get_latest_tvl_total()
    tvl_eth = get_latest_tvl_eth()
    tvl_ftm = get_latest_tvl_ftm()
    return jsonify(tvl_total | tvl_eth | tvl_ftm)


@app.route("/tvl_total", methods=['GET'])
def tvl_total():
    return jsonify(get_latest_tvl_total())


@app.route("/tvl_eth", methods=['GET'])
def tvl_eth():
    return jsonify(get_latest_tvl_eth())


@app.route("/tvl_ftm", methods=['GET'])
def tvl_ftm():
    return jsonify(get_latest_tvl_ftm())
