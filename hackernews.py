import requests
from bs4 import BeautifulSoup
from pprint import pprint

r = requests.get('https://news.ycombinator.com/')
soup = BeautifulSoup(r.text, 'lxml')
titles = soup.select('.storylink')

subtexts = soup.select('.subtext')

articles_info = []

for title in titles:
    url = title['href']
    name = title.text
    article_info = {'url': url, 'name': name}
    articles_info.append(article_info)

pprint(articles_info)

'''
# 用列表推导式更简单
pprint([{'url': title['href'], 'name': title.text} for title in titles])
'''
