import aiohttp
import asyncio
import pandas as pd
from io import StringIO
from datetime import datetime
from fastapi.responses import StreamingResponse

from scraping.requesting import get_requests
from scraping.parsingDetik import get_link as link_detik, get_info_all_links as data_detik, scrape_urls as tasks_detik
from scraping.parsingKompas import get_links as link_kompas, get_info_all_links as data_kompas, scrape_urls as tasks_kompas
from scraping.parsingTribun import get_links as link_tribun, get_info_all_links as data_tribun, scrape_urls as tasks_tribun
from scraping.exporting import create_dict

# DETIK
async def detik_per_page(url):

  # Create a session and get the response text with async.
  async with aiohttp.ClientSession() as session:
    response_text = await get_requests(url, session)

    # Extract links from the response text using 'get_link'.
    result_link_detik = link_detik(response_text)

    return result_link_detik

async def detik_multi_page(base_url, format:str="json"):

  async def get_all_info(link):
    # Open an async session and fetch response text
    async with aiohttp.ClientSession() as session:
      response_text = await get_requests(url=link, session=session)
      if response_text:
        # Get links from the page
        result_link_detik = await detik_per_page(url=link)

        # Scrape content from the links
        results = await tasks_detik(urls=result_link_detik)

        # Extract info from the scraped data
        all_info = data_detik(response_texts=results, links=result_link_detik)
        return all_info
  
  # Create tasks to gather info from all links in base_url
  tasks = [get_all_info(link) for link in base_url]
  
  # Run all tasks concurrently
  results = await asyncio.gather(*tasks)

  # Store info in a dictionary.
  data = create_dict(resource=base_url, data=results)
    
  # Return data in JSON or CSV format.    
  if format == "json":
    print(type(data))
    return data
  elif format == "csv":
    source = 'detik'
    return csv_format(results, source)


# KOMPAS
async def kompas_per_page(url):

  # Async with a session.
  async with aiohttp.ClientSession() as session:
    response_text = await get_requests(url, session)

    # Extract all links from the parsed HTML content using the 'get_link' function.
    result_link_detik = link_kompas(response_text)

    return result_link_detik

async def kompas_multi_page(base_url, format:str="json"):

  async def get_all_info(link):
    # Open an async session and fetch response text
    async with aiohttp.ClientSession() as session:
      response_text = await get_requests(url=link, session=session)
      if response_text:
        # Get links from the page
        result_link_detik = await kompas_per_page(url=link)

        # Scrape content from the links
        results = await tasks_kompas(urls=result_link_detik)

        # Extract info from the scraped data
        all_info = data_kompas(response_texts=results, links=result_link_detik)
        return all_info

  # Create tasks to gather info from all links in base_url
  tasks = [get_all_info(link) for link in base_url]

  # Run all tasks concurrently
  results = await asyncio.gather(*tasks)

  # Store info in a dictionary.
  data = create_dict(resource=base_url, data=results)
    
  # Return data in JSON or CSV format.    
  if format == "json":
    print(data)
    return data
  elif format == "csv":
    source = 'detik'
    return csv_format(results, source)


# TRIBUN
async def tribun_per_page(url):

  # Async with a session.
  async with aiohttp.ClientSession() as session:
    response_text = await get_requests(url, session)

    # Extract all links from the parsed HTML content using the 'get_link' function.
    result_link_detik = link_tribun(response_text)

    return result_link_detik

async def tribun_multi_page(base_url, format:str="json"):

  async def get_all_info(link):
    # Open an async session and fetch response text
    async with aiohttp.ClientSession() as session:
      response_text = await get_requests(url=link, session=session)
      if response_text:
        # Get links from the page
        result_link_detik = await tribun_per_page(url=link)

        # Scrape content from the links
        results = await tasks_tribun(urls=result_link_detik)

        # Extract info from the scraped data
        all_info = data_tribun(response_texts=results, links=result_link_detik)
        return all_info

  # Create tasks to gather info from all links in base_url
  tasks = [get_all_info(link) for link in base_url]

  # Run all tasks concurrently
  results = await asyncio.gather(*tasks)

  # Store info in a dictionary.
  data = create_dict(resource=base_url, data=results)
    
  # Return data in JSON or CSV format.    
  if format == "json":
    print(data)
    return data
  elif format == "csv":
    source = 'detik'
    return csv_format(results, source)

# Export to CSV
def csv_format(all_info, source):
  df = pd.DataFrame(all_info)

  # Make CSV in string with StringIO
  csv_buffer = StringIO()
  df.to_csv(csv_buffer, index=False)
  csv_buffer.seek(0)

  # Configurate the name file with timestamp and 
  generated_time = datetime.now().strftime('%Y-%m-%d_%H%M%S')
  csv_data = f"{source}_{generated_time}.csv"

  # Configurate the name file with timestamp
  return  StreamingResponse(
      csv_buffer,
      media_type="text/csv",
      headers={"Content-Disposition": f"attachment; filename={csv_data}"}
  )