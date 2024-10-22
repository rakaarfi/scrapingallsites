import requests
import pandas as pd
from fastapi.responses import StreamingResponse
from datetime import datetime
from io import StringIO

from scraping.requesting import get_requests
from scraping.parsingDetik import get_link as link_detik, get_info_all_links as data_detik
from scraping.parsingKompas import get_links as link_kompas, get_info_all_links as data_kompas
from scraping.parsingTribun import get_links as link_tribun, get_info_all_links as data_tribun
from scraping.exporting import create_dict

# DETIK
def detik_per_page(url, session):

  # Sends requests with a session.
  response_text, status = get_requests(url, session)

  # Extract all links from the parsed HTML content using the 'get_link' function.
  result_link_detik = link_detik(response_text)

  return result_link_detik

def detik_multi_page(base_url, format:str="json"):
  session = requests.Session()

  all_links = []
  for url_category in base_url:
    # Put the scraping per page function inside the loop
    result_detik = detik_per_page(url=url_category, session=session)
    all_links.extend(result_detik)

  all_response_text =[]
  # Request each link to get detailed info
  for link in all_links:
    response_text, status = get_requests(url=link, session=session)
    all_response_text.append(response_text)

  # Extract detailed information and its index from all link.
  all_info, index = data_detik(response_texts=all_response_text, links=all_links)

  # Store all info to a dictionary.
  data = create_dict(resource=base_url, count=index+1, data=all_info)

  # Return data in JSON or CSV format.   
  if format == "json":
    return data
  
  elif format == "csv":
    source = 'detik'
    return csv_format(all_info, source)


# KOMPAS
def kompas_per_page(url, session):

  # Sends requests with a session.
  response_text, status = get_requests(url, session)

  # Extract all links from the parsed HTML content using the 'get_link' function.
  result_link_kompas = link_kompas(response_text)

  return result_link_kompas

def kompas_multi_page(base_url, format:str="json"):
  session = requests.Session()

  all_links = []
  for url_category in base_url:
    # Put the scraping per page function inside the loop
    result_kompas = kompas_per_page(url=url_category, session=session)
    all_links.extend(result_kompas)

  all_response_text =[]
  # Request each link to get detailed info
  for link in all_links:
    response_text, status = get_requests(url=link, session=session)
    all_response_text.append(response_text)

  # Extract detailed information and its index from all link.
  all_info, index = data_kompas(response_texts=all_response_text, links=all_links)

  # Store all info to a dictionary.
  data = create_dict(resource=base_url, count=index+1, data=all_info)

  # Return data in JSON or CSV format.   
  if format == "json":
    return data
  
  elif format == "csv":
    source = 'kompas'
    return csv_format(all_info, source)
  

# TRIBUN  
def tribun_per_page(url, session):

  # Sends requests with a session.
  response_text, status = get_requests(url, session)

  # Extract all links from the parsed HTML content using the 'get_link' function.
  result_link_tribun = link_tribun(response_text)

  return result_link_tribun

def tribun_multi_page(base_url, format:str="json"):
  session = requests.Session()

  all_links = []
  for url_category in base_url:
    # Put the scraping per page function inside the loop
    result_tribun = tribun_per_page(url=url_category, session=session)
    all_links.extend(result_tribun)

  all_response_text =[]
  # Request each link to get detailed info
  for link in all_links:
    response_text, status = get_requests(url=link, session=session)
    all_response_text.append(response_text)

  # Extract detailed information and its index from all link.
  all_info, index = data_tribun(response_texts=all_response_text, links=all_links)

  # Store all info to a dictionary.
  data = create_dict(resource=base_url, count=index+1, data=all_info)

  # Return data in JSON or CSV format.   
  if format == "json":
    return data

  elif format == "csv":
    source = 'tribun'
    return csv_format(all_info, source)
  
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