import requests
import re
import csv
from datetime import datetime
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}
url = "https://www.amazon.co.uk/Best-Sellers-Electronics-Mobile-Phone-Cases-Covers/zgbs/electronics/340321031/ref=zg_bs_pg_1?_encoding=UTF8&pg="

headerlist = ['Ranking', 'Brand', 'Title', 'Price', 'Rating', 'Reviews', 'URL', 'Main Image URL']
filename = str(datetime.now().strftime("%Y-%m-%d-%Hh%M")) + "_UK_Top100.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
writer.writerow(headerlist)

try:
    for page in range(1, 3):
        res = requests.get(url + str(page), headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        items = soup.find("ol", attrs={"id":"zg-ordered-list"}).find_all("li", attrs={"class":"zg-item-immersion"})
        
        for item in items:

            ranking = item.find("span", attrs={"class":"zg-badge-text"}).get_text()
            
            title = item.find("div", attrs={"aria-hidden":"true"}).get_text().strip()

            brand = item.find("div", attrs={"aria-hidden":"true"}).get_text().strip().split()[0]
            
            # try:
            #     price = item.find("span", attrs={"class":"p13n-sc-price"}).get_text()
            # except AttributeError:
            #     continue

            try:
                price = item.find("span", attrs={"class":"p13n-sc-price"}).get_text()
            except AttributeError:
                try:
                    price = item.find("span", attrs={"a-size-base a-color-price"}).get_text()
                except AttributeError:
                    price = '0'

            rating = float(item.find("span", attrs={"class":"a-icon-alt"}).get_text().replace("out of 5 stars",""))
            
            rate_cnt = item.find("a", attrs={"class":"a-size-small a-link-normal"}).get_text()

            item_url = item.a["href"]
            if item_url.startswith("/"):
                item_url = "https://www.amazon.co.uk" + item_url
            
            image_url = item.img["src"]
            
            top100 = [ranking, brand, title, price, rating, rate_cnt, item_url, image_url]
            writer.writerow(top100)

except:
    print("Error...")