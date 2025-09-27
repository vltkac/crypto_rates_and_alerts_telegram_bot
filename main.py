from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests, asyncio, json


CRYPTO_INSERTIONS = {'btc', 'bitcoin', 'tether', 'usdt', 'ethereum', 'eth', 'solana', 'sol', 'doge'}
ALERT_SIGNS = {'>=', '<='}
ALERT_ID = 0
ALERTS_REACHED = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ALERT_ID

    await update.message.reply_text("Welcome to the crypto alert bot! 💵"
                                    "\n\n🏷️ To check the price of the crypto now use /price (e. g. /price BTC)."
                                    '\n📉 To check the price of all available cryptos use /market.'
                                    "\n🚨 To set an alert use /alert (e. g. /alert BTC >= 100000 or /alert BTC <= 100000)."
                                    "\n\n💎 Available currencies 💎\n"
                                    "BTC ETH USDT SOL DOGE")

    with open('users_alerts.json', 'r', encoding='utf-8') as f:
        try:
            alerts = json.load(f)

            ALERT_ID = max(alerts, key=lambda al: al['alert_id'])['alert_id'] + 1
        except json.decoder.JSONDecodeError:
            ALERT_ID = 0


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please specify a currency (BTC ETH USDT SOL DOGE).")
        return

    crypto = context.args[0].lower()

    if crypto == 'bitcoin' or crypto == 'btc':
        crypto = 'bitcoin'
    elif crypto == 'doge':
        crypto = 'doge'
    elif crypto == 'ethereum' or crypto == 'eth':
        crypto = 'ethereum'
    elif crypto == 'solana' or crypto == 'sol':
        crypto = 'solana'
    elif crypto == 'tether' or crypto == 'usdt':
        crypto = 'tether'

    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,solana,doge&vs_currencies=usd')

    try:
        data = response.json()

        if crypto in data:
            price_now = data[crypto]['usd']

            await update.message.reply_text(f'{crypto.upper()} {price_now} USD')
        else:
            await update.message.reply_text("No crypto found.")
            return

    except requests.exceptions.RequestException as err:
        await update.message.reply_text(f'Network connection error occurred: {err}')
        return


async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,solana,doge&vs_currencies=usd')

    try:
        data = response.json()
        market_now_message = ''

        for currency in data:
            price_now = data[currency]['usd']
            market_now_message += f'{currency.upper()} {price_now} USD\n'

        await update.message.reply_text(market_now_message)

    except requests.exceptions.RequestException as err:
        await update.message.reply_text(f'Network connection error occurred: {err}')
        return


async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ALERT_ID

    if len(context.args) != 3 or context.args[0].lower() not in CRYPTO_INSERTIONS or context.args[1] not in ALERT_SIGNS or not context.args[2].isdigit() or float(context.args[2]) < 0:
        await update.message.reply_text("Please specify the currency, the alert sign (more or equal or less or equal) and the alert price "
                                        "(e. g. /alert BTC >= 100000 or /alert BTC <= 100000).")
        return None

    crypto = context.args[0].lower()

    if crypto == 'bitcoin' or crypto == 'btc':
        crypto = 'bitcoin'
    elif crypto == 'doge':
        crypto = 'doge'
    elif crypto == 'ethereum' or crypto == 'eth':
        crypto = 'ethereum'
    elif crypto == 'solana' or crypto == 'sol':
        crypto = 'solana'
    elif crypto == 'tether' or crypto == 'usdt':
        crypto = 'tether'

    alert_sign = context.args[1]
    alert_price = context.args[2]

    with open('users_alerts.json', 'r', encoding='utf-8') as f:
        try:
            alerts = json.load(f)
            ALERT_ID = max(alerts, key=lambda al: al['alert_id'])['alert_id'] + 1
        except json.decoder.JSONDecodeError:
            ALERT_ID = 0

    user_alert = {
        'alert_id': ALERT_ID,
        'chat_id': update.effective_chat.id,
        'crypto': crypto,
        'alert_sign': alert_sign,
        'alert_price': alert_price
    }

    data = None

    with open('users_alerts.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = []

    with open('users_alerts.json', 'w', encoding='utf-8') as f:
        data.append(user_alert)
        json.dump(data, f, ensure_ascii=False, indent=4)

    ALERT_ID += 1

    await update.message.reply_text('Your alert was saved successfully. You will receive a message from the bot when the price reaches your alert price.')
    return None


async def check_alerts(context: ContextTypes.DEFAULT_TYPE):
    try:
        with open('users_alerts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,solana,doge&vs_currencies=usd')
        rates_now = response.json()

        for alert in data:
            alert_id = alert['alert_id']
            alert_user = alert['chat_id']
            alert_crypto = alert['crypto']
            alert_sign = alert['alert_sign']
            alert_price = alert['alert_price']

            for rate_currency in rates_now:
                price_now = rates_now[rate_currency]['usd']

                if rate_currency == alert_crypto:
                    if eval(str(price_now) + alert_sign + str(alert_price)):
                        ALERTS_REACHED.add(alert_id)
                        await context.bot.send_message(chat_id=alert_user, text=f'{alert_crypto.upper()} reached your alert price {alert_price} USD.')
    except requests.exceptions.RequestException as err:
        print(f'Network connection error occurred: {err}')
    except json.decoder.JSONDecodeError:
        return


async def remove_checked_alerts(context: ContextTypes.DEFAULT_TYPE):
    with open('users_alerts.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = []
            return

    data = list(filter(lambda al: al['alert_id'] not in ALERTS_REACHED, data))

    with open('users_alerts.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    app = ApplicationBuilder().token("TELEGRAM TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("market", market))
    app.add_handler(CommandHandler("alert", alert))

    job_queue = app.job_queue
    job_queue.run_repeating(check_alerts, interval=30, first=10)
    job_queue.run_repeating(remove_checked_alerts, interval=30, first=15)

    print("Bot is running...")
    app.run_polling()