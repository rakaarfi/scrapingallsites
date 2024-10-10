import requests
import pandas as pd
from fastapi.responses import StreamingResponse
from datetime import datetime
from io import StringIO

# (Nama folder) + (.) + (nama file) import 
from scraping.requesting import get_requests
from scraping.parsingDetik import get_link as link_detik, get_info_all_links as data_detik
from scraping.parsingKompas import get_links as link_kompas, get_info_all_links as data_kompas
from scraping.exporting import create_dict

def detik_per_page(url, session):
  # Sends requests with a session.
  soup, status = get_requests(url, session)
  # Extract all links from the parsed HTML content using the 'get_link' function.
  result_link_detik = link_detik(soup)

  return result_link_detik

def detik_multi_page(base_url, format:str="json"):
  session = requests.Session()

  all_results = []
  for i in range(1):
    url = f"{base_url + str(i+1)}"
    # print(url) # Print URL for debugging

    # Put the scraping per page function inside the loop
    result_detik = detik_per_page(url, session=session)
    # Add the result in the empty list
    all_results.extend(result_detik)

  # Extract detailed information and its index from all link.
  all_info, index = data_detik(all_results)

  # Store all info to a dictionary.
  data = create_dict(resource=base_url, count=index+1, data=all_info)

  if format == "json":
    return data
  
  elif format == "csv":
    df = pd.DataFrame(data)

    # Make CSV in string with StringIO
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Configurate the name file with timestamp
    generated_time = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    csv_data = f"detik_{generated_time}.csv"

    # Return the response as CSV file
    return  StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={csv_data}"}
    )

def kompas_per_page(url, session):
  # Sends requests with a session.
  soup, status = get_requests(url, session)
  # Extract all links from the parsed HTML content using the 'get_link' function.
  result_link_kompas = link_kompas(soup)

  return result_link_kompas

def kompas_multi_page(base_url, format:str="json"):
  session = requests.Session()

  all_results = []
  for i in range(1):
    url = base_url+'&page='+str(i+1)
    print(url) # Print URL for debugging

    # Put the scraping per page function inside the loop
    result_kompas = kompas_per_page(url, session=session)
    # Add the result in the empty list
    all_results.extend(result_kompas)

  # Extract detailed information and its index from all link.
  all_info, index = data_kompas(all_results)

  # Store all info to a dictionary.
  data = create_dict(resource=base_url, count=index+1, data=all_info)

  if format == "json":
    return data

  elif format == "csv":
    df = pd.DataFrame(data)

    # Make CSV in string with StringIO
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Configurate the name file with timestamp
    generated_time = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    csv_data = f"kompas_{generated_time}.csv"

    # Configurate the name file with timestamp
    return  StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={csv_data}"}
    )