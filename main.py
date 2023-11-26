import requests
from bs4 import BeautifulSoup
import pandas as pd

from_file = True

URL = "https://rateyourmusic.com/genre/rock/"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 '
                  'Safari/537.36'
}
if not from_file:
    page = requests.get(URL, headers=headers)
    page_content = page.content
    with open("response.txt", "wb") as f:
        f.write(page.content)
    print("From HTTP request")
else:
    page_content = open("response.txt", "rb")
    print("From saved file")

soup = BeautifulSoup(page_content, "html.parser")

discography_elements = soup.find_all("li", class_="component_discography_item")

# df = pd.DataFrame({}, columns=["Genre", "Title", "Year", "Type", "Number of Tracks", "Link"])

rows_list = []

for discography_element in discography_elements:
    dict1 = {}

    element_title = discography_element.find(class_="ui_name_locale_original").get_text(strip=True)
    dict1.update({"title": element_title})

    element_type = (discography_element.find(class_="component_discography_item_details").select('div > span')[2]
                    .get_text(strip=True))
    dict1.update({"type": element_type})

    element_link = discography_element.find(class_="component_discography_item_link release")["href"]
    dict1.update({"link": "https://rateyourmusic.com" + element_link})

    rows_list.append(dict1)

df = pd.DataFrame(rows_list)

df.to_csv('file.csv')
