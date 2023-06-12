import logging

import user_agent
from bs4 import BeautifulSoup
import requests
from config import URL, DOMAIN
from data import DataBase

def get_user_agent():
    headers = {
        "Accept": "*/*",
        "User-Agent" : user_agent.generate_user_agent()
    }
    return headers

class Parcer:
    data = DataBase()
    def __init__(self):
        self.link = None
    def get_news_list(self):
        query = requests.get(URL, headers=get_user_agent())
        src = query.text

        with open("sources/news_list.html", "w") as file:
            file.write(src)

    def find_news(self):
        LAST_NEWS_NUMBER = 6
        with open("sources/news_list.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        views_list = soup.find_all('span', class_="post-card-inline__stats-item")[:LAST_NEWS_NUMBER]
        a_link_list = soup.find_all('a', class_="post-card-inline__title-link")[:LAST_NEWS_NUMBER]
        views_and_links = {}
        #анализ популярности последних LAST_NEWS_NUMBER статей.
        print(src)

        for i in range(LAST_NEWS_NUMBER):
            views_and_links[a_link_list[i]['href']] = int(views_list[i].text)
        sorted_links = sorted(views_and_links, key=views_and_links.get)
        sorted_views_and_links = {}
        for w in sorted_links:
            sorted_views_and_links[w] = views_and_links[w]
        #sorted_views_and_links - словарь из новостей, отсортированных по просмотрам.
        most_popular_news = sorted_views_and_links.keys()
        most_popular_news = reversed(most_popular_news)
        for news_link in most_popular_news:
            if news_link not in self.data.get_history():
                link = DOMAIN + news_link
                self.data.upload_history(news_link)
                return link
        logging.WARNING('return None')
        return None
    def prepare_last_news(self, link):
        query = requests.get(link, headers=get_user_agent())
        src = query.text

        with open("sources/last_news.html", "w") as file:
            file.write(src)

    def scrap(self, link):
        self.prepare_last_news(link)
        with open("sources/last_news.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        div_content_data = soup.find("div", class_="post-content")

        news = []

        news.append(soup.find("h1", class_="post__title").text)
        for x in div_content_data:
            x.find("p")
            news.append(x.text)
        news.append('<a href="' + link+'">Ознакомиться с оригинальной статьей.</a>')
        return news


    def get_last_link(self):
        return self.link

    def get_awesome_news(self):
        self.get_news_list()
        self.link = self.find_news()
        news = self.scrap(self.link)
        return news