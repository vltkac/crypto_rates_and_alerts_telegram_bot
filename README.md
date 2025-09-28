# Crypto Alert Bot

A simple Telegram bot that allows you to check cryptocurrency prices and set alerts for specific price levels.  
The bot uses the [CoinGecko API](https://www.coingecko.com/en/api) for live market data and stores user alerts in a local JSON file.

---

## Features

- `/start` — show welcome message and instructions.
- `/price <crypto>` — check the current price of a specific cryptocurrency (BTC, ETH, USDT, SOL, DOGE).
- `/market` — display prices of all available cryptocurrencies at once.
- `/alert <crypto> <sign> <price>` — set a price alert.  
  Example: `/alert BTC >= 50000` or `/alert ETH <= 2000`.

When an alert condition is met, the bot sends you a notification in Telegram.

---

## Requirements

- Python 3.9+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v20+
- `requests`

Install dependencies:

```bash
pip install python-telegram-bot requests
```

---

## Setup

1. Clone the repository or copy the project files.

2. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram and get your API token.

3. Add your token to `main.py`:

```python
app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
```

4. Run the bot:

```bash
python main.py
```

---

## Data Storage

- Alerts are stored in a local JSON file: `users_alerts.json`. Bot will create this file in the directory of the main.py automatically.


---

## Notes

- Alerts are checked automatically every 30 seconds.
- Triggered alerts are removed from `users_alerts.json` so they won't repeat.
- The bot supports multiple users, each alert is tied to the user’s chat ID.

---

## Example Usage

```
/start
/price BTC
/market
/alert BTC >= 50000
/alert ETH <= 2000
```

---

## License

MIT License
