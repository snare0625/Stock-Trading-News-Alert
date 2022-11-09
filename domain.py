import requests
from twilio.rest import Client


#GET STOCK DATA
def stock_data(stock_name, stock_api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stock_name}&apikey={stock_api_key}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

def curr_week_close(stock_data):
    data = stock_data["Weekly Time Series"]
    data_list = [value for (key, value) in data.items()]
    current_week_data = data_list[1]
    current_week_closing_price = float(current_week_data["4. close"])
    #curr_week_close = float(stock_data["Weekly Time Series"]["2022-11-08"]["4. close"])

    return current_week_closing_price

def prev_week_close(stock_data):
    data = stock_data["Weekly Time Series"]
    data_list = [value for (key, value) in data.items()]
    previous_week_data = data_list[0]
    previous_week_closing_price = float(previous_week_data["4. close"])
    #prev_week_close = float(stock_data["Weekly Time Series"]["2022-11-04"]["4. close"])
    return previous_week_closing_price

def stock_weekly_perc_diff(curr_week_close, prev_week_close):
    positive_diff = abs(curr_week_close - prev_week_close)
    perc_stock_diff = round(int((positive_diff/curr_week_close) * 100), 2)

    return perc_stock_diff

def get_news_sources(company_name):
    url = f"https://newsapi.org/v2/everything?q={company_name}&from=2022-10-09&sortBy=publishedAt&apiKey=ab11debedb824edb807bd5a3551186c0"
    response = requests.get(url)
    response.raise_for_status()
    articles = response.json()["articles"]
    return articles

def company_article_list(articles, company_name, stock_name):
    news_list = []

    for article in articles:
        if (company_name in article["title"] or
            company_name in article["description"] or
            company_name in article["content"]):
            source = {}
            headline = article['description']
            brief = article['content']
            source['stock_name'] = stock_name
            source['headline'] = headline
            source['brief'] = brief
            news_list.append(source)
            if len(news_list) == 3:
                break
    return news_list

def send_message(stock_name, article_no, company_article_list):

    account_sid = "AC53c02b716c92cd490d905c2cb1367a7a"
    auth_token = "5fbec5d6c66796a9f41c65eb627264b8"
    client = Client(account_sid, auth_token)

    news_source = company_article_list[article_no]


    message = client.messages \
                    .create(
                         body=f"{stock_name}: percentage_increase\n"
                              f"Headline: {news_source['headline']}\n"
                              f"Brief: {news_source['brief']}",
                         from_='+14782428486',
                         to='+27825748542'
                     )

    return message.sid


"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

