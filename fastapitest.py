from fastapi import FastAPI
from pydantic import BaseModel
import json

from scraping.main import detik_multi_page, kompas_multi_page
import allsites


app = FastAPI()
# run dengan fastapi dev (namafile)

# API = Application Programing Interface
"""
fungsinya untuk jembatan komunikasi antara berbagai macam aplikasi
aplikasi bisa bermacam2, be fe
"""

class Item(BaseModel):
  source: str
  category: str | None = None
  page: int | None = None
  format: str | None = None

@app.post("/scrape")
async def scraping(item:Item):
  if item.source == "detik":
    if item.category == "news":
      site = allsites.DETIK_NEWS
    elif item.category == "business":
      site = allsites.DETIK_BUSINESS
    elif item.category == "top-news":
      site = allsites.DETIK_TOPNEWS
    return detik_multi_page(base_url=site, format=item.format)
  
  if item.source == "kompas":
    if item.category == "news":
      site = allsites.KOMPAS_NEWS
      return kompas_multi_page(base_url=site)
    
    elif item.category == "business":
      sites = [allsites.KOMPAS_MONEY, allsites.KOMPAS_UMKM]
      results = []
      for site in sites:
        results.append(kompas_multi_page(base_url=site))
      return results 

    elif item.category == "top-news":
      sites = [allsites.KOMPAS_TREN, allsites.KOMPAS_HYPE]
      results = []
      for site in sites:
        results.append(kompas_multi_page(base_url=site))
      return results
