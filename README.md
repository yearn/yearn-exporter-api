# yearn-exporter-api
Light-weight API in front of [yearn.vision](https://yearn.vision) that makes some data available for external sites.

## Usage
Start the api with `docker-compose up` or `docker-compose up -d` for detached mode. This will expose it at `http://localhost:5000`.

## Configuration
You can export the following environment variables if you want to override the defaults:
- `FLASK_RUN_PORT`: the listening port for the api, default: 5000
- `BASE_URL`: the URL pointing to the grafana instance, default: "https://yearn.vision"

## Routes

### `/tvl`
returns the summed up TVLs grouped by network and a summed total:
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
returns b2b fee-sharing partners info

#### `/partners/total`
returns the total fees to be paid out to-date, measured in USD value from all chains:
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
returns for a specific partner the paramater you specify:
  - paramaters are: allowed_params: `balance`, `balance_usd`, `payout_daily`, `payout_weekly`, `payout_monthly`, `payout_total`, `payout_usd_daily`, `payout_usd_weekly`, `payout_usd_monthly`, `payout_usd_total`
  - partners are the names of the b2b partners
 
 ```
 $ curl localhost:5000/partners/gb/payout_usd_monthly
{
  "partners_indiv_gb_payout_usd_monthly": {
    "0xdCD90C7f6324cfa40d7169ef80b12031770B4325": 0
  },
  "ts": 1665023175,
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
