import requests
from bs4 import BeautifulSoup

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

print(soup.prettify())
