# Cryptex Token Metrics API
A simple API for supplying CoinMarketCap with total supply information for the CTX and TCAP tokens.

[Cryptex.Finance](https://cryptex.finance)

## Usage
First, bring up the service: `docker-compose up -d`.

### CoinMarketCap
* Total Token Supply: *GET* `/cmc/tokens/<token>` with `token` being either TCAP or CTX.

### Metrics
* APY: *GET* `/metrics/tokens/<token>/apy` with `token` being CTX.

## Changelog
* 2.0.0 - Implement new endpoint paths, support getting APY metrics for CTX
* 1.0.1 - Fix paths
* 1.0.0 - Initial API