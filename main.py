import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "H348B2BQCY4KEL0O"
NEWS_API_KEY = "b592bf6119004b32b22a7b97d0649c6c"
TWILIO_SID = "ACb05f6b217bd85fd5a2d5d500b17b888e"
TWILIO_AUTH_TOKEN = "91c226ba24005e637467b8a8974b16cd"
## STEP 1: Use https://www.alphavantage.co/documentation/#daily
#Get yesterday's closing stock price.
stock_params = {
     "function": "TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)
# Get the day before yesterday's closing stock price
day_bef_yesterday_data=data_list[1]
day_bef_yesterday_closing_price = day_bef_yesterday_data["4. close"]
print(day_bef_yesterday_closing_price)
#find the positive difference between 1 and 2.
diff = abs(float(yesterday_closing_price) - float(day_bef_yesterday_closing_price))
up_down= None
if diff > 0:
    up_down= "**"
else:
    up_down = "*"

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent=float(diff/float(yesterday_closing_price))*100
print(diff_percent)
# If the diff percentage is greater than some percentage then print the news.
if abs(diff_percent) > 0.2:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
     #Using Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]
    print(three_articles)

#Creating a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"{STOCK_NAME}:{up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief:{article['description']}" for article in three_articles]

#Sending each article as a separate message via Twilio.
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_="+14708285947",
        to="+91917702093493",
    )