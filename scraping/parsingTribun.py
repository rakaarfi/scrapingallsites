import requests
from concurrent.futures import ThreadPoolExecutor

from scraping.requesting import get_requests

def get_links(soup):
  article = soup.find('div', class_='content')
  links_tag = article.find_all('a')

  # List of link's pattern to exclude
  exclude_patterns = [
        ".com/tag/",
        ".com/topic/",
        ".com/internasional/bbc-indonesia?utm_campaign",
        ".com/internasional/dw?utm_campaign",
        ".com/australia-plus?utm_campaign"
    ]

  links = []
  for i in links_tag:
    href = i.get('href')
    exclude = False

    # Loop through each pattern and check if it's in the href
    for i in exclude_patterns:
      if i in href:
        exclude = True
        break

    if len(href) > 70 and not exclude:
      # Split the href by 'utm_campaign' and take only the first part before it
      clean_href = href.split('utm_campaign')[0]

      # Ensure the trailing '?' or '&' after removing 'utm_campaign' is cleaned up
      clean_href = clean_href.rstrip('?,&')

      # Add ?page=all to extract all pages from the news
      complete_link = clean_href + "?page=all"

      links.append(complete_link)

  unique_links = list(set(links))
  return unique_links

# Extract Title, Date, Author, Image URL, Content/Paragraphs
def get_info_links(link):
  session = requests.Session()
  soup, status = get_requests(link, session=session)

  info = {}
  title = None
  date = None
  author = None
  img_url = None
  content_tag = None

  if status == 200:
    article = soup.find('div', attrs={'id':'article'})
        
    if article:
      # Extract Title
      title_tag = article.find('h1', class_='f50 black2 f400 crimson')
      title = title_tag.get_text(strip=True) if title_tag else "Title not Found"

      # Extract Date
      date_div = article.find('div', class_='grey bdr3 pb10 pt10')
      date_tag = date_div.find('span') if date_div else "Date div not found"
      date = date_tag.get_text() if date_tag else "Date not found"

      # Extract Author
      author_div = article.find('div', attrs={'id':'penulis'})
      if author_div:
        author_tag = author_div.find('a')
        author = author_tag.get_text() if author_tag else "Author tag not found"

      else: #If id:penulis not found, find id:editor
        author_div = article.find('div', attrs={'id':'editor'})
        if author_div:
          author_tag = author_div.find('a') if author_div else "Editor div not found"
          author = author_tag.get_text() if author_tag else "Editor not found"

        else: #If id:editor also not found, find another source
          author_div = article.find('div', attrs={'class':'wfull'})
          author_tag = author_div.find('a') if author_div else "Author from another web, div not found"
          author = author_tag.get('title') if author_tag else "Author from another web not found"

      # Extract Image URL
      img_url_tag = article.find('img', class_='imgfull')
      img_url = img_url_tag.get('src') if img_url_tag else "Image URL not found"

      # Extract Content
      content_tag = article.find('div', class_='side-article txt-article multi-fontsize').get_text(strip=True)

    else:
      print(f"Article div not found for link: {link}")

    info['Link'] = link
    info["Title"] = title
    info["Date"] = date
    info["Author"] = author
    info["Image URL"] = img_url
    info["Content"] = content_tag

  else:
      print(f"Failed to extract info. Status code: {status}")
      info["Error"] = f"Failed to extract info. Status code: {status}"

  return info

def get_info_all_links(links):
  # Error Handling
  def process_link(link):
    try:
      info = get_info_links(link)
      return info
    except Exception as e:
      print(f"Error extracting info from {link}: {e}")
      return None # Return None if an exception occurs
    
  # Create a thread pool to process multiple links concurrently
  executor = ThreadPoolExecutor()
  all_info = list(executor.map(process_link, links))

  return all_info