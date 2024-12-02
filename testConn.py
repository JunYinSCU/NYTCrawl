import requests

url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
params = {
    'q': 'Xinjiang',
    'api-key': 'MGTgxwAh6G7RiwjHVEBR10rEppjBUZxI',
    'begin_date': '20220101',
    'end_date': '20221231'
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()  # 检查请求是否成功
    print(response.json())  # 打印返回的 JSON 数据
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
