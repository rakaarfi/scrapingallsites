import requests
from concurrent.futures import ThreadPoolExecutor

from scraping.requesting import get_requests

# Extract all links
def get_link(soup):
# Find all links tag
  links = (soup.find_all('a', class_='media__link') or 
           soup.find_all('a', class_='flex gap-4 group items-center'))

  # Iterate each link to an empty list
  link_list = []
  for link in links:
    href = link.get('href')

    # Add ?single=1 to extract all pages from the news
    complete_link = href + "?single=1"

    # Excluding some from link
    if len(complete_link) > 50 and "https://20.detik.com/" not in complete_link and ".com/foto-" not in complete_link:
      link_list.append(complete_link)

  no_duplicate_link = [i for n, i in enumerate(link_list) if i not in link_list[:n]]
  
  return no_duplicate_link

# Extract img URL, Title, Content, author, date
def get_info(link):
  session = requests.Session()
  soup, status = get_requests(url=link, session=session)

  info = {}
  img = None
  if status == 200:
    # Find tag that have link inside
    article = soup.find('article', class_='detail')

    # Get Image URL
    # img = validate_info(tag='img', classes=None, article=article).get('src')
    img_tag = article.find('img') if article else "Image tag not found"
    img = img_tag.get('src') if img_tag else "Image not found"

    # Get Title
    title = (safe_get_text(tag='h1', classes='detail__title', article=article) or
              safe_get_text(tag='h1', classes='text-center text-[32px] leading-10 mb-2.5', article=article))
    
    # Get Author
    author = (safe_get_text(tag='div', classes='detail__author', article=article) or
              safe_get_text(tag='div', classes='text-[#8B8B8B]', article=article))

    # Get Date
    date = (safe_get_text(tag='div', classes='detail__date', article=article) or
            safe_get_text(tag='time', classes='text-[#8B8B8B] text-[13px] text-center', article=article))

    # Get Content
    content = (safe_get_text(tag='div', classes='detail__body-text itp_bodycontent', article=article) or 
               safe_get_text(tag='div', classes='detail__body flex-grow min-w-0 font-helvetica text-lg itp_bodycontent', article=article))

    # Add info to the empty dictionary
    info["Link"] = link
    info["Title"] = title
    info["Author"] = author
    info["Date"] = date
    info["Image URL"] = img
    info["Content"] = content

  else:
    print(f"Failed to extract info. Status code: {status}")
  return info

# Helper function to safely get text
def safe_get_text(tag, classes, article):
    result = validate_info(tag, classes, article)
    return result.get_text(strip=True) if result else ''

# Validating info
def validate_info(tag, classes, article):
  try:
    info = article.find(tag, class_=classes)
  except AttributeError as e:
    info = None
    print(f"An exception occurred: {e}")
  return info

# Extracting all info from all links
def get_info_all_links(links):

  # Create a thread pool to process multiple links concurrently
  executor = ThreadPoolExecutor()
  all_info = list(executor.map(get_info, links))

  return all_info