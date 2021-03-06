'''
name: E#15
author: Andrey Plugin
email: 9keepa@gmail.com
link: https://www.youtube.com/channel/UCNN3bpPlWWUkUMB7gjcUFlw
'''
import requests
from bs4 import BeautifulSoup
import sqlite3

base_url = "http://books.toscrape.com/catalogue"
url = "http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"

response = requests.get(url)

html = response.text

soup = BeautifulSoup(html, "html.parser")
container = soup.select_one("ol.row")
books = container.find_all("li")
urls = [base_url + "/" + x.select_one("h3 a")['href'].replace("../", "") for x in books]

args = []
for url in urls:
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    name = soup.select_one("h1").text
    price = soup.select_one("p.price_color").text[2:]
    description = soup.find("div", {"class":"sub-header"}).find_next("p").text
    info = str(soup.select_one("table.table.table-striped"))
    args.append((name, price, description, info))

conn = sqlite3.connect("mydata.db")
cursor = conn.cursor()
cursor.executemany("INSERT INTO books VALUES(?,?,?,?)", args)
conn.commit()
conn.close()



