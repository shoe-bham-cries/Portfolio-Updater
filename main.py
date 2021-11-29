import requests
import smtplib
import html


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
my_email = "shu.py.thore@gmail.com"
password = "qetuadgj0"
recipient = "shubhamrathore3261@gmail.com"
STOCK_API_KEY = "WQOXN8L45ZDGJQI6"
NEWS_API_KEY = "a46e10cc58964adf98514494c6a88ded"

stock_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_param)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

diff_percent = (abs(float(day_before_yesterday_closing_price) - float(yesterday_closing_price))/float(yesterday_closing_price))*100


if diff_percent > 2:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]


    top_3 = articles[:3]
    print(news_response.json())
    messages = [f"Headline: {article['title']}, \nBrief: {article['description']}" for article in top_3]
    for message in messages:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=recipient,
                msg=f"Subject: Portfolio Update\n\n{html.unescape(message.encode('utf8'))}"
            )
            print("Done!")
