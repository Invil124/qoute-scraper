import json
from typing import List

import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com/"
LIST_ALL_QUOTES = []
LIST_All_AUTHORS_URL = []


def parse_all_info_from_page(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.select("li[class=next] a ")
    get_quotes(soup)
    get_author_urls(soup)

    if len(pages) == 0:
        return None

    page = pages[0].get("href")

    return parse_all_info_from_page(URL+page)


def get_quotes(soup):

    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')

    for i in range(0, len(quotes)):
        quote = {}
        tags_list = []
        tagsforquote = tags[i].find_all('a', class_='tag')

        for tagforquote in tagsforquote:
            tag = tagforquote.text
            tags_list.append(tag)

        quote["tags"] = tags_list
        quote["author"] = authors[i].text
        quote["quote"] = quotes[i].text
        LIST_ALL_QUOTES.append(quote)


def save_to_json(data, file_name):

    with open(file_name, "w", encoding="utf-8") as fd:
        json.dump(data, fd, ensure_ascii=False)


def get_author_urls(soup):
    authors = soup.select("div[class=quote] span a")

    for author in authors:
        author_url = author.get("href")
        full_author_url = URL + author_url
        if full_author_url not in LIST_All_AUTHORS_URL:
            LIST_All_AUTHORS_URL.append(full_author_url)


def get_author_info(url):
    author = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    author_name = soup.find_all("h3", class_="author-title")
    author_born_date = soup.find_all("span", class_="author-born-date")
    author_born_location = soup.find_all("span", class_="author-born-location")
    author_description = soup.find_all("div", class_="author-description")

    author["fullname"] = author_name[0].text.strip()
    author["born_date"] = author_born_date[0].text.strip()
    author["born_location"] = author_born_location[0].text.strip()
    author["description"] = author_description[0].text.strip()
    return author


def get_all_authors_info(list_all_author_url: List[str]): # робить список авторів
    all_authors = []

    for author_url in list_all_author_url:
        all_authors.append(get_author_info(author_url))

    return all_authors


if __name__ == "__main__":
    parse_all_info_from_page(URL)
    save_to_json(LIST_ALL_QUOTES, "quotes.json")
    save_to_json(get_all_authors_info(LIST_All_AUTHORS_URL), "author.json")



