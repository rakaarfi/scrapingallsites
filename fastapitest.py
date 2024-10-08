from fastapi import FastAPI

from scraping.main import detik_multi_page, kompas_multi_page

import sys

sys.setrecursionlimit(9000000)

app = FastAPI()
# run dengan fastapi dev (namafile)

@app.get("/")
def read_root():
  return {"status code": 200,
          "message": "ok"}

@app.get("/detik/news")
def categorynews():
  news = "https://news.detik.com/indeks/"
  data = detik_multi_page(base_url=news)
  return data

@app.get("/detik/edu")
def categoryedu():
  edu = "https://www.detik.com/edu/indeks/"
  data = detik_multi_page(base_url=edu)
  return data

@app.get("/detik/newsCategory/{site}")
def allcategory(site:str = "News"):
  # Conditioning based on each category
  if site == "News":
    site = "https://news.detik.com/indeks/"
  elif site == "Business":
    site = "https://finance.detik.com/indeks/"
  elif site == "Top-News":
    site = "https://hot.detik.com/indeks/"

  # Extracting all data from certain pages
  data = detik_multi_page(base_url=site)
  return data

@app.get("/detik/allNews")
def allnews():
  # Input all news category
  news = "https://news.detik.com/indeks/"
  business = "https://finance.detik.com/indeks/"
  top_news = "https://hot.detik.com/indeks/"

  # Put all category in one single list
  sites = [news, business, top_news]

  # Extracting all data from all category
  all_data = []
  for site in sites:
    data = detik_multi_page(base_url=site)
    all_data.append(data)
  
  return all_data

@app.get("/kompas/newsCategory/{site}")
def kompascategory(site:str = "News"):

  # Conditioning based on each category
  # if site == "News":
  site = "https://indeks.kompas.com/?site=news"

  # elif site == "Business":
  #   money = 'https://indeks.kompas.com/?site=money'
  #   umkm = 'https://indeks.kompas.com/?site=umkm'
  #   all_site = [money, umkm]
  #   for i in all_site:
  #     site = i

  # elif site == "Top-News":
  #   tren = 'https://indeks.kompas.com/?site=tren'
  #   hype = 'https://indeks.kompas.com/?site=hype'
  #   all_site = [tren, hype]
  #   for i in all_site:
  #     site = i

  # Extracting all data from certain pages
  data = kompas_multi_page(base_url=site)
  return data
