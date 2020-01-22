# coding: utf-8

import re, requests
from bs4 import BeautifulSoup

AMEBLO = "https://ameblo.jp"

def scrape(allArticles, BASEDIR):
    for articles in allArticles:
        for url in articles:
            title = url.string
            print(f"{BASEDIR}{title}")
            with open(f"{BASEDIR}{title}.txt", "w") as file:
                html = requests.get(url["href"]).content
                soup = BeautifulSoup(html, "html.parser")
                divs = soup.find("div", {"class", "articleText"})
                text = getPlainText(str(divs)).strip()
                print(f"Written file: {title}.txt")
                file.write(text)
    print("Complete to scrape")

def getArticleList(listhtml):
    urls = []
    html = requests.get(listhtml)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.content, "html.parser")
    nextPage = soup.find("li", class_="skin-borderQuiet").a
    while True:
        if isinstance(nextPage, type(None)):
            print("Complete to get article list")
            return urls
        else:
            urls.append(AMEBLO+nextPage["href"])
            #print(AMEBLO+nextPage["href"])
            html = requests.get(AMEBLO+nextPage["href"]).content
            #print(html)
            soup = BeautifulSoup(html, "html.parser")
            #nextPage = None
            # ここの、各ページの前の記事をほっていく部分で、前のページのaタグを見つけられていない
            nextPage = soup.find("ul", class_="skin-paging")
            print(nextPage)


def getUrl(articleList):
    pages = []
    for html in articleList:
        code = requests.get(html).content
        soup = BeautifulSoup(code, "html.parser")
        text = soup.find_all("a", {"class", "contentTitle"})
        pages.append(text)
    print("Complete to get url")
    return pages

def getPlainText(html):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", html)
    return cleantext

if __name__=='__main__':
    # request - test
    # art = requests.get("https://trysail.jp")
    # print(art.text)
    URL = "https://ameblo.jp/natsukawashiinablog/entrylist.html"
    DIR = "output/"
    allArticles = getArticleList(URL)
    print(allArticles)
    pages = getUrl(allArticles)
    print(pages)
    scrape(pages, DIR)
