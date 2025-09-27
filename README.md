# Telegram Crypto Alert Bot

## Description
This Telegram bot allows users to monitor cryptocurrency prices and set alerts for specific price thresholds. Users can:
- Check the current price of supported cryptocurrencies.
- View the market prices of all supported cryptocurrencies.
- Set custom alerts that notify them when a cryptocurrency reaches a specified price.

Supported cryptocurrencies:
- BTC (Bitcoin)
- ETH (Ethereum)
- USDT (Tether)
- SOL (Solana)
- DOGE (Dogecoin)

Alerts are stored in a JSON file, and the bot periodically checks prices to notify users.

## Features
- Get cryptocurrency prices in real time using the CoinGecko API.
- Set alerts for when a currency goes above or below a specific price.
- Alerts are persistent and stored in `users_alerts.json`.
- Automated checking of alerts with job scheduling (via `python-telegram-bot` job queue).

## Installation
1. Clone this repository.
2. Install dependencies:
```bash
pip install python-telegram-bot requests
```
3. Replace `"TELEGRAM TOKEN"` in the code with your Telegram bot token.

## Usage
Run the bot:
```bash
python main.py
```
Bot commands:
- `/start` — display welcome message and instructions.
- `/price <CRYPTO>` — get the current price of a cryptocurrency.
- `/market` — get current prices of all supported cryptocurrencies.
- `/alert <CRYPTO> <>= or <= > <PRICE>` — set an alert for a cryptocurrency.

## Notes
- Alerts are checked every 30 seconds.
- The bot uses the CoinGecko API, which may have request limits.

## Example
Set an alert for Bitcoin when it reaches $100,000:
```
/alert BTC >= 100000
```
You will receive a message from the bot when the price threshold is reached.
