import os
import sys

import requests
from dotenv import load_dotenv
from twilio.rest import Client

# --- Configuration ---
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
ARTICLES_LIMIT = 3

load_dotenv()  # loads the .env file
sys.stdout.reconfigure(encoding='utf-8')  # fixes output encoding chinese characters

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": os.environ.get("STOCK_API_KEY"),
}

news_params = {
    "apiKey": os.environ.get("NEWS_API_KEY"),
    "q": COMPANY_NAME,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = "🔺" if difference > 0 else "🔻"

difference_percent = round((difference / float(yesterday_closing_price)) * 100, 2)

if abs(difference) > 5:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    three_articles = articles[:ARTICLES_LIMIT]
    
    formatted_articles = [f"{STOCK_NAME}: {up_down}{difference_percent}% \nHeadline: {article['title']} \nBrief: {article['description']}" for article in three_articles]

    client = Client(os.environ.get("TWILIO_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=os.environ.get("TWILIO_PHONE_NUMBER"),
            to=os.environ.get("MY_PHONE_NUMBER")
        )
        print(message.sid)
        print(message.status)
