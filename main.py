import yfinance as yf
import requests
import os
from datetime import datetime

# --- SETTINGS ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TOP_12 = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "LT.NS", "KOTAKBANK.NS", "AXISBANK.NS", "BAJFINANCE.NS"]

def get_analysis():
    msg = f"📈 *NIFTY TOP 12 - {datetime.now().strftime('%d %b %Y')}*\n\n"
    for stock in TOP_12:
        try:
            data = yf.download(stock, period="5d", interval="1d", progress=False)
            if len(data) < 2:
                continue
            prev_close = data['Close'].iloc[-2].item()
            last_close = data['Close'].iloc[-1].item()
            change = ((last_close - prev_close) / prev_close) * 100
            
            emoji = "🟢" if change > 0 else "🔴"
            msg += f"{emoji} {stock.replace('.NS','')} : {change:.2f}%\n"
        except Exception as e:
            msg += f"⚪ {stock} : Error\n"
    
    msg += "\n✅ Bot by Sagarmali90"
    return msg

def send_telegram(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Token/Chat ID missing")
        print(text)
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    final_msg = get_analysis()
    send_telegram(final_msg)
    print(final_msg)
