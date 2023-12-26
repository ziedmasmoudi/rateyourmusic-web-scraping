import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_page(content_f):
    soup = BeautifulSoup(content_f, "html.parser")

    discography_elements = soup.find_all("li", class_="component_discography_item")

    rows = []

    for discography_element in discography_elements:
        dict1 = {}

        element_title = discography_element.find(class_="ui_name_locale_original").get_text(strip=True)
        dict1.update({"title": element_title})

        element_type = (discography_element.find(class_="component_discography_item_details").select('div > span')[2]
                        .get_text(strip=True))
        dict1.update({"type": element_type})

        element_link = discography_element.find(class_="component_discography_item_link release")["href"]
        dict1.update({"link": "https://rateyourmusic.com" + element_link})

        rows.append(dict1)
    return rows


def get_page_content(genre_f, page_number_f, from_file_f):
    url = "https://rateyourmusic.com/genre/" + genre_f + "/" + str(page_number_f)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/119.0.0.0'
                      'Safari/537.36'
    }
    file_path = genre + "/" + genre_f + "_" + str(page_number_f) + ".txt"
    if not from_file_f:
        page = requests.get(url, headers=headers)
        page_content_f = page.content
        with open(file_path, "wb") as f:
            f.write(page.content)
        print("From HTTP request")
    else:
        page_content_f = open(file_path, "rb")
        print("From saved file")
    return page_content_f


def get_page_content_scraperapi(genre_f, page_number_f):
    payload = {'api_key': '14909c782c424358e32379909b1424f7', 'url': 'https://rateyourmusic.com/genre/' + genre_f + "/" + str(page_number_f)}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    file_path = genre_f + "/" + genre_f + "_" + str(page_number_f) + ".txt"
    with open(file_path, "wb") as f:
        f.write(r.content)
    return r.content


from_file = False
genre = "jazz"

rows_list = []

for i in range(1, 251):
    page_content = get_page_content_scraperapi(genre, i)
    content = scrape_page(page_content)
    print(content, end='\n')
    rows_list.extend(content)

print(rows_list)
df = pd.DataFrame(rows_list)

df.to_csv(genre + '/' + genre + '.csv')
