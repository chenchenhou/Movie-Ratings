from bs4 import BeautifulSoup
from numpy import dtype
import pandas as pd
import os
import requests

links = pd.read_csv(
    "/Users/panfucheng/Desktop/CMU/ETIM/Data Science/Final Project/ml-latest-small/links.csv"
)
print(links.head())
header = "http://www.imdb.com/title/"


def scrapeCrew(url):  # scrape cast and crew from imdb
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")
        headers = soup.find_all("h4")
        for i in range(len(tables)):
            header = headers[i].text.strip().replace("\n", "")
            rows = tables[i].find_all("tr")
            names = []
            if header.strip().startswith("Cast"):
                for row in rows[1:]:
                    anchors = row.find_all("a")
                    if len(anchors) >= 2:
                        names.append(anchors[1].text.strip())
                    else:
                        continue
                break
    else:
        names = []
    return names[:10] if len(names) >= 10 else names


casts = []
for imdb in links["imdbId"][9000:]:
    if imdb:
        temp = imdb
        imdb = str(int(imdb))
        imdb = imdb.zfill(7)
        print(imdb)
        url = os.path.join(header, "tt" + imdb, "fullcredits?ref_=tt_cl_sm")
        cast = scrapeCrew(url)
        cast = [temp] + cast
        casts.append(cast)
    else:
        continue

name_df = pd.DataFrame(
    casts,
    columns=[
        "imdbId",
        "Actor1",
        "Actor2",
        "Actor3",
        "Actor4",
        "Actor5",
        "Actor6",
        "Actor7",
        "Actor8",
        "Actor9",
        "Actor10",
    ],
)
print(name_df.head())
name_df.to_csv("cast_9000_to_999.csv")
