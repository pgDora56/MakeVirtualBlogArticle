# coding:utf-8
import re, time, requests
import os
from bs4 import BeautifulSoup

DIR = os.getcwd() + "/output/417/"
AMEBLO = "https://ameblo.jp"

os.makedirs(DIR)

def getArticlesPage(html):
    urls = [html]
    while True:
        data = requests.get(html).content
        soup = BeautifulSoup(data, "lxml")
        nexts = soup.find("a", {"class", "skin-paginationNext skin-btnIndex js-paginationNext"})
        if isinstance(nexts, type(None)):
            print("Complete to get article page")
            return urls
        else:
            urltmp = AMEBLO + nexts["href"]
            urls.append(urltmp)
            print(f"Append {urltmp}")
            html = urltmp
            time.sleep(1)


def getArticle(articlePages):
    pages = []
    for html in articlePages:
        data = requests.get(html).content
        soup = BeautifulSoup(data, "lxml")
        text = soup.find_all("li", class_ = "skin-borderQuiet")
        for t in text:
            pages.append(t.find("a"))
        print(f"OK: {html}")
        time.sleep(1)
    print("Complete to get articles")
    return pages


def getPlainText(data):
    pattern = re.compile("<.*?>")
    plain = re.sub(pattern, "", data)
    return plain


def scrape(articles):
    no = 1
    maxi = len(str(len(articles)))
    for article in articles:
        html = requests.get(AMEBLO + article["href"]).content
        soup = BeautifulSoup(html, "lxml")
        title = soup.find("a", class_ = "skinArticleTitle").text
        div_text = soup.find("div", {"class", "skin-entryBody _2nkwn0s9"})
        text = getPlainText(str(div_text)).strip()
        # with open(f"{DIR}{str(no).zfill(maxi)}. {title}.txt", "w", encoding="utf-8") as file:
        with open(f"{DIR}{str(no).zfill(maxi)}.txt", "w", encoding="utf-8") as file:
            print(f"Written file: {str(no).zfill(maxi)}.txt")
            file.write(text)
        no += 1
        time.sleep(1)
    print("Complete to scrape")

if __name__ == "__main__":
    print("Start")
    start_time = time.time()
    url = "https://ameblo.jp/natsukawashiinablog/entrylist.html"
    allArticlePage = getArticlesPage(url)
    pages = getArticle(allArticlePage)
    scrape(pages)
    print(f"Finish. Elapsed time: {time.time() - start_time}")

