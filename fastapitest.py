from fastapi import FastAPI
from pydantic import BaseModel

from scraping.main import detik_multi_page, kompas_multi_page, tribun_multi_page
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
  format: str | None = "json"

@app.post("/scrape")
async def scraping(item:Item):
  # DETIK
  if item.source == "detik":
    if item.category == "top-news":
      site = allsites.DETIK_TOPNEWS
    elif item.category == "business":
      site = allsites.DETIK_BUSINESS

    elif item.category == "sports":
      sites = allsites.DETIK_ALL_SPORT
      results = []
      for site in sites:
        results.append(detik_multi_page(base_url=site, format=item.format))
      return results
    
    elif item.category == "entertainment":
      site = allsites.DETIK_POP
    elif item.category == "health": 
      site = allsites.DETIK_HEALTH
    elif item.category == "science-tech":
      site = allsites.DETIK_INET
    elif item.category == "news":
      site = allsites.DETIK_NEWS

    elif item.category == "localnews":
      sites = allsites.DETIK_ALL_LOCALNEWS
      results = []
      for site in sites:
        results.append(detik_multi_page(base_url=site, format=item.format))
      return results
    
    elif item.category == "travel":
      sites = allsites.DETIK_ALL_TRAVEL
      results = []
      for site in sites:
        results.append(detik_multi_page(base_url=site, format=item.format))
      return results

    return detik_multi_page(base_url=site, format=item.format)
  
  # KOMPAS
  elif item.source == "kompas":
    if item.category == "top-news":
      sites = allsites.KOMPAS_ALL_TOPNEWS
      results = []
      for site in sites:
        results.append(kompas_multi_page(base_url=site, format=item.format))
      return results
    
    elif item.category == "business":
      sites = allsites.KOMPAS_ALL_BUSINESS
      results = []
      for site in sites:
        results.append(kompas_multi_page(base_url=site, format=item.format))
      return results
    
    elif item.category == "sports":
      site = allsites.KOMPAS_BOLA
    elif item.category == "health":
      site = allsites.KOMPAS_HEALTH

    elif item.category == "science-tech":
      sites = allsites.KOMPAS_ALL_SCIENCETECH
      results = []
      for site in sites:
        results.append(kompas_multi_page(base_url=site, format=item.format))
      return results

    elif item.category == "news":
      site = allsites.KOMPAS_NEWS
    elif item.category == "worldnews":
      site = allsites.KOMPAS_GLOBAL

    elif item.category == "localnews":
      sites = allsites.KOMPAS_ALL_LOCALNEWS
      results = []
      for site in sites:
        results.append(kompas_multi_page(base_url=site, format=item.format))
      return results
    
    elif item.category == "travel":
      sites = allsites.KOMPAS_ALL_TRAVEL
      results = []
      for site in sites:
        results.append(kompas_multi_page(base_url=site, format=item.format))
      return results
    
    return kompas_multi_page(base_url=site, format=item.format)
  
  # TRIBUN
  elif item.source == "tribun":
    if item.category == "politics":
      sites = allsites.TRIBUN_ALL_POLITICS
      results = []
      for site in sites:
        results.append(tribun_multi_page(base_url=site, format=item.format))
      return results
    
    elif item.category == "business":
      sites = allsites.TRIBUN_ALL_BUSINESS
      results = []
      for site in sites:
        results.append(tribun_multi_page(base_url=site, format=item.format))
      return results
    
    elif item.category == "sports":
      sites = allsites.TRIBUN_ALL_SPORT
      results = []
      for site in sites:
        results.append(tribun_multi_page(base_url=site, format=item.format))
      return results

    elif item.category == "entertainment":
      sites = allsites.TRIBUN_ALL_ENTERTAINMENT
      results = []
      for site in sites:
        results.append(tribun_multi_page(base_url=site, format=item.format))
      return results

    elif item.category == "health":
      site = allsites.TRIBUN_HEALTH

    elif item.category == "science-tech":
      site = allsites.TRIBUN_TECH

    elif item.category == "news":
      site = allsites.TRIBUN_NEWS

    elif item.category == "worldnews":
      site = allsites.TRIBUN_INTERNASIONAL

    elif item.category == "localnews":
      sites = allsites.TRIBUN_ALL_LOCALNEWS
      results = []
      for site in sites:
        results.append(tribun_multi_page(base_url=site, format=item.format))
      return results
    
    elif item.category == "travel":
      site = allsites.TRIBUN_TRAVEL
 
    return tribun_multi_page(base_url=site, format=item.format)