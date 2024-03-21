from bs4 import BeautifulSoup
from numpy import dtype
import pandas as pd
import os
import requests

links = pd.read_csv("data/links.csv")
header = "https://www.boxofficemojo.com/title/"


def scrapeBoxOffice(url):  # scrape cast and crew from imdb
    response = requests.get(url)
    boxOffice = {
        "Domestic": None,
        "International": None,
        "WorldWide": None,
    }
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        spans = soup.find_all("span", class_="a-size-medium a-text-bold")
        revenueType = ["Domestic", "International", "WorldWide"]
        for i in range(len(spans)):
            s = spans[i].text.strip()
            if len(s) == 1:
                continue
            s = int(s.replace("$", "").replace(",", ""))
            boxOffice[revenueType[i]] = s
    return boxOffice


boxOffices = []
for imdb in links["imdbId"]:
    if imdb:
        temp = imdb
        imdb = str(int(imdb))
        imdb = imdb.zfill(7)
        print(imdb)
        url = os.path.join(header, "tt" + imdb)
        boxOffice = scrapeBoxOffice(url)
        boxOffice["imdbId"] = temp
        boxOffices.append(boxOffice)
    else:
        continue

boxOffice_df = pd.DataFrame(boxOffices)
boxOffice_df.to_csv("boxOffice.csv")
