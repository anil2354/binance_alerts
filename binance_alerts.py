import time
import asyncio
from binance.client import Client
from telegram import Bot

# Telegram Bot credentials
TELEGRAM_BOT_TOKEN = '7769253765:AAGU97xLLeTJ5iNz-0A7Oor4E9WVsBxjlM0'
TELEGRAM_CHAT_ID = '1950782042'

# Binance API credentials
BINANCE_API_KEY = 'cexFWtoVTEv7AN7SlUmM7onhrQPhO05MQUcsBuGQJg9K4PJFp3h14y8N4cMW5j64'
BINANCE_SECRET_KEY = 'vTV4PT3IZXnuKizwRyyiMDzjfMhGuyKZCawnadEMNHkLnFYpPSKRpPn2OKhV7tET'

# Initialize Binance Client
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Set up for tracking alerts sent (to ensure each coin gets alerted only once)
coin_alerts = {}

# Function to check price changes of futures coins
async def check_binance_futures():
    # Get all futures coin data
    futures_data = client.futures_ticker()

    # Loop through the data and find coins with a 20% pump in 24 hours
    for coin in futures_data:
        symbol = coin['symbol']
        price_change_percent = float(coin['priceChangePercent'])

        # Debugging: Print price change for each coin to check
        print(f"Checking {symbol}: {price_change_percent}% change in the last 24 hours")

        # Check if the price change is greater than or equal to 20%
        if price_change_percent >= 20:
            if symbol not in coin_alerts:
                coin_alerts[symbol] = 1
                await send_alert(symbol, price_change_percent)
            elif coin_alerts[symbol] < 2:
                coin_alerts[symbol] += 1
                await send_alert(symbol, price_change_percent)

# Function to send alert to Telegram bot
async def send_alert(symbol, price_change_percent):
    message = f"🚀 {symbol} has pumped by {price_change_percent}% in the last 24 hours!"
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Function to reset alerts after sending two alerts for a coin
def reset_alerts():
    for coin in list(coin_alerts.keys()):
        if coin_alerts[coin] >= 2:
            del coin_alerts[coin]

# Main async loop to check every 5 minutes
async def main():
    while True:
        print("Checking for 20% pumps...")
        await check_binance_futures()
        reset_alerts()  # Reset alert count after checking
        await asyncio.sleep(300)  # Wait for 5 minutes (300 seconds) before checking again

# Start the program
if __name__ == "__main__":
    asyncio.run(main())
