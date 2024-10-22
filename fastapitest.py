from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

import allsites
import allsitesdict
from scraping.main import detik_multi_page, kompas_multi_page, tribun_multi_page
from scraping.exporting import generate_result


app = FastAPI()

@app.get("/categories")
async def show_categories():
  categories = allsitesdict.categories
  links_data = allsitesdict.links_data

  result = generate_result(links_data, categories)

  return result

class Item(BaseModel):
  source: str
  category: str | None = None
  format: str | None = "json"

@app.post("/scrape")
def scraping(item:Item):
  # DETIK
  if item.source == "detik":
    if item.category == "top_news":
      site = allsites.DETIK_TOPNEWS
    elif item.category == "sports":
      site = allsites.DETIK_ALL_SPORT
    elif item.category == "entertainment":
      site = allsites.DETIK_POP
    elif item.category == "health": 
      site = allsites.DETIK_HEALTH
    elif item.category == "science_tech":
      site = allsites.DETIK_INET
    elif item.category == "news":
      site = allsites.DETIK_NEWS
    elif item.category == "local_news":
      site = allsites.DETIK_ALL_LOCALNEWS
    elif item.category == "travel":
      site = allsites.DETIK_ALL_TRAVEL

    asyncio.run(detik_multi_page(base_url=site, format=item.format))
  
  # KOMPAS
  elif item.source == "kompas":
    if item.category == "top_news":
      site = allsites.KOMPAS_ALL_TOPNEWS
    elif item.category == "business":
      site = allsites.KOMPAS_ALL_BUSINESS
    elif item.category == "sports":
      site = allsites.KOMPAS_BOLA
    elif item.category == "health":
      site = allsites.KOMPAS_HEALTH
    elif item.category == "science_tech":
      site = allsites.KOMPAS_ALL_SCIENCETECH
    elif item.category == "news":
      site = allsites.KOMPAS_NEWS
    elif item.category == "world_news":
      site = allsites.KOMPAS_GLOBAL
    elif item.category == "local_news":
      site = allsites.KOMPAS_ALL_LOCALNEWS
    elif item.category == "travel":
      site = allsites.KOMPAS_ALL_TRAVEL
    
    return kompas_multi_page(base_url=site, format=item.format)
  
  # TRIBUN
  elif item.source == "tribun":
    if item.category == "politics":
      site = allsites.TRIBUN_ALL_POLITICS
    elif item.category == "business":
      site = allsites.TRIBUN_ALL_BUSINESS
    elif item.category == "sports":
      site = allsites.TRIBUN_ALL_SPORT
    elif item.category == "entertainment":
      site = allsites.TRIBUN_ALL_ENTERTAINMENT
    elif item.category == "health":
      site = allsites.TRIBUN_HEALTH
    elif item.category == "science_tech":
      site = allsites.TRIBUN_TECH
    elif item.category == "news":
      site = allsites.TRIBUN_NEWS
    elif item.category == "world_news":
      site = allsites.TRIBUN_INTERNASIONAL
    elif item.category == "local_news":
      site = allsites.TRIBUN_ALL_LOCALNEWS
    elif item.category == "travel":
      site = allsites.TRIBUN_TRAVEL
 
    return tribun_multi_page(base_url=site, format=item.format)