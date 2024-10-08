import requests
import concurrent.futures

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

def detik_multi_page(base_url):
  session = requests.Session()

  all_results = []
  for i in range(1):
    url = f"{base_url + str(i+1)}"
    print(url) # Print URL for debugging

    # Put the scraping per page function inside the loop
    result_detik = detik_per_page(url, session=session)
    # Add the result in the empty list
    all_results.extend(result_detik)

  # Extract detailed information and its index from all link.
  all_info, index = data_detik(all_results)

  # with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
  #   executor.map(data_detik, all_results)

  # Store all info to a dictionary.
  data = create_dict(resource=base_url, count=index+1, data=all_info)

  return data

def kompas_per_page(url, session):
  # Sends requests with a session.
  soup, status = get_requests(url, session)
  # Extract all links from the parsed HTML content using the 'get_link' function.
  result_link_kompas = link_kompas(soup)

  return result_link_kompas

def kompas_multi_page(base_url):
  session = requests.Session()

  all_results = []
  for i in range(1):
    url = f"{base_url + "&page=" + str(i+1)}"
    print(url) # Print URL for debugging

    # Put the scraping per page function inside the loop
    result_kompas = kompas_per_page(url, session=session)
    # Add the result in the empty list
    all_results.extend(result_kompas)

  # Extract detailed information and its index from all link.
  all_info, index = data_kompas(all_results)

  # with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
  #   executor.map(data_kompas, all_results)

  # Store all info to a dictionary.
  data = create_dict(resource=base_url, count=index+1, data=all_info)

  return data

if __name__ == '__main__':
  url = 'https://indeks.kompas.com/?site=news'
  result = kompas_multi_page(base_url=url)
  print(result)