import requests
import csv

# API Key
api_key = "MGTgxwAh6G7RiwjHVEBR10rEppjBUZxI"

# 搜索关键词列表
search_keywords = ["Xinjiang", "Xinjiang Human Rights", "Uyghur"]

# 将多个关键词合并成一个字符串，关键词之间用逗号分隔
search_query = " OR ".join(search_keywords)

# 构造请求 URL
url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

params = {
    "q": search_query,  # 使用多个关键词进行搜索，关键词间用 OR 连接
    "api-key": api_key,  # API 密钥
    "begin_date": "20150101",  # 开始日期 (格式: YYYYMMDD)
    "end_date": "20240101",  # 结束日期 (格式: YYYYMMDD)
    "sort": "newest"  # 按最新排序
}
proxies = {
    "http": None,
    "https": None
}



# 打开 CSV 文件以便写入
with open('nyt_articles_XinJiang.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "URL", "Date", "Abstract", "Author", "Keywords"])  # 表头

    page = 0  # 从第 1 页开始
    while True:
        params["page"] = page  # 设置分页参数

        # 发送请求
        response = requests.get(url, params=params)

        # 检查响应状态
        if response.status_code == 200:
            data = response.json()
            articles = data.get("response", {}).get("docs", [])

            if not articles:  # 如果没有文章，停止分页
                print("No more articles found.")
                break

            # 写入数据
            for article in articles:
                title = article.get("headline", {}).get("main")
                url = article.get("web_url")
                pub_date = article.get("pub_date")
                abstract = article.get("abstract", "N/A")
                byline = article.get("byline", {}).get("original", "N/A")
                keywords = [keyword["value"] for keyword in article.get("keywords", [])]
                keywords = ", ".join(keywords) if keywords else "N/A"

                writer.writerow([title, url, pub_date, abstract, byline, keywords])

            print(f"Page {page + 1} processed successfully.")
            page += 1  # 获取下一页的数据
        else:
            print(f"Failed to fetch articles. HTTP Status Code: {response.status_code}")
            break  # 如果请求失败，停止执行