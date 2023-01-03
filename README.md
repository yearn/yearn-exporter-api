# yearn-exporter-api
Light-weight API in front of [yearn.vision](https://yearn.vision) that makes some data available for external sites.

## Usage
Start the API with `make build && make up`. This will expose it at `http://localhost:5000`.


## Make commands
All these are prefaced with `make`.
- `build`, `up`, `down`, `destroy`, `stop`, `restart`, `ps`

## Configuration
You can export the following environment variables if you want to override the defaults:
- `FLASK_RUN_PORT`: the listening port for the api, default: 5000
- `BASE_URL`: the URL pointing to the grafana instance, default: "https://yearn.vision"

## Routes

### `/tvl`
returns the summed TVLs grouped by network and a summed total:
```
$ curl localhost:5000/tvl
{
  "ts":1642600346,
  "tvl_eth":5101043121.68,
  "tvl_ftm":533590588.63,
  "tvl_total":533590588.63,
  "unit":"USD"
}
```

### `/tvl/<network>`
returns the tvl for the given network, e.g. for `ETH`:
```
$ curl localhost:5000/tvl/eth
{
  "ts":1642600393,
  "tvl_eth":5101041358.88,
  "unit":"USD"
}
```
supported networks are:
- `ETH`
- `FTM`
- `OPI`
- `ARB`

### `/tvl/total`
returns the sum of the TVLs of all networks:
```
$ curl localhost:5000/tvl/total
{
  "ts":1642600475,
  "tvl_total":534919919.17,
  "unit":"USD"
}
```
### `/partners/{query}`
returns b2b fee-sharing partners' info

#### `/partners/total`
returns the total fees to be paid out to date, measured in USD value from all chains:
```
$ curl localhost:5000/partners/total
{
  "partners_total": 2601705.85,
  "ts": 1665017101,
  "unit": "USD"
}
```
#### `/partners/count`
returns the number of partners to-date from all chains:
```
$ curl localhost:5000/partners/count
{
  "partners_count": 22,
  "ts": 1665017986,
  "unit": ""
}
```
#### `/partners/<partner>/<param>`
returns for a specific partner the parameter you specify:
  - parameters are: allowed_params: `balance`, `payout_daily`, `payout_weekly`, `payout_monthly`, `payout_total`
  - partners are the names of the b2b partners
 
 ```
 $ curl localhost:5000/partners/sturdy/payout_total
  "partners_indiv_sturdy_payout_total": {
    "FTM": {
      "0x0DEC85e74A92c52b7F708c4B10207D9560CEFaf0": {
        "balance": 2238.09,
        "bucket": "Other short term assets",
        "token": "yvWFTM",
        "tvl": 1732.48
      },
      "0x0fBbf9848D969776a5Eb842EdAfAf29ef4467698": {
        "balance": 15.17,
        "bucket": "Other short term assets",
        "token": "yvBOO",
        "tvl": 123.41
      },
      "0x1e2fe8074a5ce1Bb7394856B0C618E75D823B93b": {
        "balance": 1714.68,
        "bucket": "Other short term assets",
        "token": "yvfBEETS",
        "tvl": 389.16
      },
      "0xf2d323621785A066E64282d2B407eAc79cC04966": {
        "balance": 5.92,
        "bucket": "Other short term assets",
        "token": "yvLINK",
        "tvl": 66.84
      }
    }
  },
  "ts": 1671244960,
  "unit": "USD"
}
```
 

## Optional Query Params
- `ts`
```
curl localhost:5000/tvl?ts=1642664109
{
  "ts":1642664109,
  "tvl_eth":5081490281.98,
  "tvl_ftm":574308185.62,
  "tvl_total":5655798467.6,
  "unit":"USD"
}
```
set a ts (millis) for retrieving the data at that specific timestamp
