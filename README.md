# Cryptex CoinMarketCap API
A simple API for supplying CoinMarketCap with total supply information for the CTX and TCAP tokens.

[Cryptex.Finance](https://cryptex.finance)

## Usage
First, bring up the service: `docker-compose up -d`.

After the service is running, the following endpoints will become available: 
`/total-supply-tcap` and `/total-supply-ctx`. Make a GET request to either to get
their respective total supply values.

## Changelog
1.0.0 - Initial API