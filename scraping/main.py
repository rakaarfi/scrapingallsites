import requests
import pandas as pd
from io import StringIO
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from fastapi.responses import StreamingResponse

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
  with requests.Session() as session:    
    with ThreadPoolExecutor() as executor:
      # Use lambda to pass both URL and session to the function
      all_results_gen = executor.map(lambda url: detik_per_page(url, session), base_url)

  all_links = []
  # Collect all links from the generator
  for result in all_results_gen:
    all_links.extend(result)

  all_response_text = []
  # Request each link to get detailed info
  for link in all_links:
    response_text, status = get_requests(url=link, session=session)
    all_response_text.append(response_text)

  # Extract detailed information and its index from all link.
  all_info = data_detik(response_texts=all_response_text, links=all_links)

  # Store all info to a dictionary.
  data = create_dict(resource=base_url, data=all_info)

  # Return data in JSON or CSV format
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
  with requests.Session() as session:
    with ThreadPoolExecutor() as executor:
      # Use lambda to pass both URL and session to the function
      all_results_gen = executor.map(lambda url: kompas_per_page(url, session), base_url)

  all_links = []
  # Collect all links from the generator
  for link in all_results_gen:
    all_links.extend(link)

  all_response_text = []
  # Request each link to get detailed info
  for link in all_links:
    response_text, status = get_requests(url=link, session=session)
    all_response_text.append(response_text)

  # Extract detailed information and its index from all link.
  all_info = data_kompas(response_texts=all_response_text, links=all_links)

  # Store all info to a dictionary.
  data = create_dict(resource=base_url, data=all_info)

  # Return data in JSON or CSV format
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
  with requests.Session() as session:
    with ThreadPoolExecutor() as executor:
      # Use lambda to pass both URL and session to the function
      all_results_gen = executor.map(lambda url: tribun_per_page(url, session), base_url)

  all_links = []
  # Collect all links from the generator
  for result in all_results_gen:
    all_links.extend(result)

  all_response_text = []
  # Request each link to get detailed info
  for link in all_links:
    response_text, status = get_requests(url=link, session=session)
    all_response_text.append(response_text)  

  # Extract detailed information from all link.
  all_info = data_tribun(response_texts=all_response_text, links=all_links)

  # Store all info to a dictionary.
  data = create_dict(resource=base_url, data=all_info)

  # Return data in JSON or CSV format
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