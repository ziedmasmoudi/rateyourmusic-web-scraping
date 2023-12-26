import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page_content_scraperapi(url):
    payload = {'api_key': '14909c782c424358e32379909b1424f7', 'url': url}
    r = requests.get('https://api.scraperapi.com/', params=payload)
    return r.content


def scrape_page(content_f):
    soup = BeautifulSoup(content_f, "html.parser")

    tracklist = soup.find("ul", id="tracks_mobile")

    if tracklist is None:
        number_of_tracks_f = 9999
        return number_of_tracks_f

    tracks = tracklist.findAll("li", class_="track")

    number_of_tracks_f = len(tracks) - 1

    return number_of_tracks_f


genre = "rock"

df = pd.read_csv(genre + '_albums/' + genre + '_albums.csv')

number_of_tracks_row = []

print(df['link'])
i = 0
for link in df['link']:
    i += 1
    if i >= 500:
        break
    page_content = get_page_content_scraperapi(link)
    number_of_tracks = scrape_page(page_content)
    number_of_tracks_row.append(number_of_tracks)
    print(i, end=" ")
    print(number_of_tracks, end=" ")
    print(link, end='\n')

df_n_tracks = pd.DataFrame(number_of_tracks_row)

df_concat = pd.concat([df, df_n_tracks], axis=1)

df_concat.to_csv(genre + '_albums/' + genre + '_albums_final.csv')
