import csv
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

dict = []
response = requests.get('https://so.gushiwen.cn/shiwen/')
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")
poems = soup.select("div.sright a")
for poem in poems:
    text = poem.text
    link = (poem.get('href'))[:-6]
    dict.append([text, link])
with open("all-dynasties.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["key", "Dynasty", "Count"])

with open("all-authors.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["key", "Author", "Count"])
for index, item in enumerate(dict):
    type, url_head = item
    statistics = {
        "dynasties": defaultdict(int),
        "authors": defaultdict(int),
        "themes": defaultdict(int)
    }
    # 遍历多个页面并进行统计
    for page in range(1, 21):
        print(f'{index + 1}/{len(dict)} {page}/20')
        url = f"{url_head}{page}.aspx"
        response = requests.get(url)
        # print(response.status_code)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        # print(soup)

        poems = soup.find_all("div", class_="cont")
        # print(url, poems)
        for poem in poems:
            dynasty_element = poem.find("p", class_="source")
            if dynasty_element is not None:
                dynasty_link = dynasty_element.find_all("a")[1]
                if dynasty_link is not None:
                    dynasty = dynasty_link.text.strip()
                    statistics["dynasties"][dynasty] += 1

            author_element = poem.find("p", class_="source")
            if author_element is not None:
                author_link = author_element.find("a")
                if author_link is not None:
                    author = author_link.text.strip()
                    statistics["authors"][author] += 1
            # print(dynasty_element, author_element)

            theme_element = poem.find("p", class_="tag")
            if theme_element is not None:
                theme_link = theme_element.find("a")
                if theme_link is not None:
                    theme = theme_link.text.strip()
                    statistics["themes"][theme] += 1

    # 保存"Dynasty"统计结果到CSV文件
    with open("all-dynasties.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for dynasty, count in statistics["dynasties"].items():
            writer.writerow([type, dynasty, count])

    # 保存"Author"统计结果到CSV文件
    with open("all-authors.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for author, count in statistics["authors"].items():
            writer.writerow([type, author, count])
