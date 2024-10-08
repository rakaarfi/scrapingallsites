import requests
from bs4 import BeautifulSoup as bs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_requests(url, session:requests.Session):
  response = session.get(url, headers=headers)

  # Only parsing the url if status_code is 200
  if response.status_code == 200:
      soup = bs(response.content, 'html.parser')
  else:
      soup = None
      print(f"Failed to get response from {url}, status code: {response.status_code}")
  return soup, response.status_code