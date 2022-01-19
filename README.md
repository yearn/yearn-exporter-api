# yearn-exporter-api
Light-weight API in front of [yearn.vision](https://yearn.vision) that makes some data available for external sites.

## Routes

### `/tvl`
returns the summed up TVLs grouped by network and a summed total:
```
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
{
  "ts":1642600475,
  "tvl_total":534919919.17,
  "unit":"USD"
}
```


## Optional Query Params
- `ts`

set a ts (millis) for retrieving the data at that specific timestamp
