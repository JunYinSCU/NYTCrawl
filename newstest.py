
import requests
import pandas as pd

# 设置API密钥和基本URL
API_KEY = 'MGTgxwAh6G7RiwjHVEBR10rEppjBUZxI'
BASE_URL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'


def get_articles(query, begin_date, end_date):
    # 设置请求参数
    params = {
        'q': query,
        'begin_date': begin_date,
        'end_date': end_date,
        'api-key': API_KEY
    }

    # 发送请求
    response = requests.get(BASE_URL, params=params)

    # 检查请求状态
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def parse_articles(data):
    articles = data['response']['docs']
    article_list = []

    for article in articles:
        article_info = {
            'headline': article['headline']['main'],
            'pub_date': article['pub_date'],
            'web_url': article['web_url'],
            'snippet': article['snippet'],
            'lead_paragraph': article['lead_paragraph'],
            'source': article['source']
        }
        article_list.append(article_info)

    return pd.DataFrame(article_list)


# 设定查询参数
query = "climate change"
begin_date = "20230801"
end_date = "20230815"

# 获取文章数据
data = get_articles(query, begin_date, end_date)

# 解析并保存数据
if data:
    articles_df = parse_articles(data)
    articles_df.to_csv('nyt_articles.csv', index=False)
    print("Articles saved to nyt_articles.csv")
else:
    print("Failed to retrieve articles.")