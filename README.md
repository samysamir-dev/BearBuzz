# Stock & News Alert Script

This Python script monitors a stock's daily price changes using the [Alpha Vantage API](https://www.alphavantage.co/).  
If the price moves significantly, it fetches related news from the [News API](https://newsapi.org/) and sends alerts via [Twilio SMS](https://www.twilio.com/).

---

### Features
- Fetch daily stock data from Alpha Vantage
- Compare yesterday’s closing price with the day before
- Calculate price change percentage and direction (🔺 / 🔻)
- Fetch latest company news if change exceeds threshold
- Send formatted alerts by SMS through Twilio

---

### Requirements
- Python 3.9+
- A `.env` file with API keys and Twilio credentials :
    Create a .env file in the project root with:
    
    STOCK_API_KEY=your_alphavantage_key  
    NEWS_API_KEY=your_newsapi_key  
    TWILIO_ACCOUNT_SID=your_twilio_account_sid  
    TWILIO_AUTH_TOKEN=your_twilio_auth_token  
    TWILIO_PHONE_NUMBER=your_twilio_phone_number  
    MY_PHONE_NUMBER=the_number_to_receive_alerts  

---

### Usage

Run the script:

python main.py


If the stock moves by more than 5% between the last two days, you’ll receive SMS alerts with news headlines.

---

### Notes

The script is written in pure Python and uses requests, python-dotenv, and Twilio.

Stock and news APIs may have rate limits on free tiers.

Only tested with U.S. stocks. Other symbols should also work.
