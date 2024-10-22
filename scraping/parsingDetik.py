import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs

from scraping.requesting import get_requests

# Extract all links
def get_link(response_text:str):
  soup = bs(response_text, 'html.parser')
  # Find all links tag
  links = (soup.find_all('a', class_='media__link') or 
           soup.find_all('a', class_='flex gap-4 group items-center'))

  # Iterate each link to an empty list
  link_list = []
  for link in links:
    href = link.get('href')

    # Add ?single=1 to extract all pages from the news
    if href:
      complete_link = href + "?single=1"

      # Excluding some from link
      if len(complete_link) > 50 and "https://20.detik.com/" not in complete_link and ".com/foto-" not in complete_link:
        link_list.append(complete_link)

  no_duplicate_link = [i for n, i in enumerate(link_list) if i not in link_list[:n]]
  
  return no_duplicate_link  

# Extract img URL, Title, Content, author, date
def get_info(response_text:str, link):
  soup = bs(response_text, 'html.parser')

  # Validating info
  def validate_info(tag, classes, article):
    try:
      info = article.find(tag, class_=classes)
    except AttributeError as e:
      info = None
      print(f"An exception occurred: {e}")
    return info

  # Helper function to safely get text
  def safe_get_text(tag, classes, article):
    result = validate_info(tag, classes, article)
    return result.get_text(strip=True) if result else ''

  info = {}
  img = None

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

  return info

# Extracting all info from all links
def get_info_all_links(response_texts:str, links):

  all_info = []
  # Loop through responses and links with indexing
  for index, (response_text, link)in enumerate(zip(response_texts, links)):
    info = get_info(response_text, link)

    print(f"Extracting {index+1} out of {len(links)}.") #Print Statement later deleted
    
    if info:
      info["Index"] = index + 1  # Add index to info dict
      all_info.append(info)

    print(link) #Print Statement later deleted

  return all_info, index

# Asynchronously scrape multiple URLs
async def scrape_urls(urls):
  async with aiohttp.ClientSession() as session:
    # Create async tasks for each URL request
    tasks = [get_requests(url, session) for url in urls]
    # Await all tasks and return results
    results = await asyncio.gather(*tasks)

    return results