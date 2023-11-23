import requests

URL = "https://rateyourmusic.com/genre/rock/"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 '
                  'Safari/537.36'
}
page = requests.get(URL, headers=headers)

print(page.text)
