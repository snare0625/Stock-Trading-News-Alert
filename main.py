import random

import domain

from datetime import datetime



STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "RCW9NZCNDK4UAALL"
NEWS_API_KEY = "ab11debedb824edb807bd5a3551186c0"


stock_data = domain.stock_data(STOCK_NAME, STOCK_API_KEY)
#print(f"Stock data: {stock_data}")
current_week_close = domain.curr_week_close(stock_data)
print(f"current week close: {current_week_close}")
prev_week_close = domain.prev_week_close(stock_data)
print(f"previous week close: {prev_week_close}")
weekly_perc_diff = domain.stock_weekly_perc_diff(current_week_close, prev_week_close)
#print(f"Stock weekly difference: {weekly_perc_diff}")
news_sources = domain.get_news_sources(COMPANY_NAME)
#print(f"News sources: {news_sources}")
company_articles = domain.company_article_list(news_sources, COMPANY_NAME, STOCK_NAME)
#print(f"Company articles: {company_articles}")
article_no = random.randint(0, 2)

send_stock_details = domain.send_message(STOCK_NAME, article_no, company_articles)
#print(send_stock_details)



