# 📈 Crypto Price Tracker

This Python script fetches real-time cryptocurrency price data from the [CoinGecko API](https://www.coingecko.com/), stores it in a CSV file, and optionally plots historical price trends for selected coins. It supports tracking **Bitcoin**, **Ethereum**, and **Solana** prices in **USD**, along with market cap and 24-hour change.

## 🚀 Features

- Fetches live price data for Bitcoin, Ethereum, and Solana
- Saves data to a local CSV file for persistent tracking
- Handles API errors gracefully
- Generates time-series plots for price history (current month)
- Customizable via `.env` configuration

## 📦 Requirements

- Python 3.7+
- `requests`
- `pandas`
- `matplotlib`
- `python-dotenv`

Install the required dependencies with:
create .env with (API_KEY = your coingecko api key) in it
```bash
pip install -r requirements.txt
