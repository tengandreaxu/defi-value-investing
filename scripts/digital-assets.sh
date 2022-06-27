#!/bin/bash

#  Total Value Locked From DefiLlama
python3 fetching/fetch_tvls.py;

# Market Prices from Binance
python3 fetching/fetch_historical_market_prices.py;

# Market Caps from Coingecko
python3 fetching/fetch_market_caps.py;

# Treasury values from CryptoStats
python3 fetching/fetch_cryptostats_treasury.py;