import requests
from concurrent.futures import ThreadPoolExecutor

from scraping.requesting import get_requests

# Extract all links
def get_links(soup):
  article = soup.find('div', class_='articleList -list')

  links = article.find_all('a', class_='article-link')
  link_list = []
  for i in links:
    link = i.get('href')
    link_list.append(link)

  return link_list

# Extract Title, Date, Author, Image URL, Content/Paragraphs
def get_info(link):
  session = requests.Session()
  soup, status = get_requests(url=link, session=session)

  # Validating info
  def validate_info(tag, classes, soup):
    try:
      info = soup.find(tag, class_=classes)
      if info is None:
        raise AttributeError(f"Tag '{tag}' with class '{classes}' not found in link: {link}")
    except AttributeError as e:
      info = None
      print(f"An exception occurred: {e}")
    return info

  info = {}

  if status == 200:
    # Get Title
    title_tag = validate_info(tag='h1', classes='read__title', soup=soup)
    title = title_tag.text.strip() if title_tag else "Title Not Found"

    # Get Date Tag
    date_tag = validate_info(tag='div', classes='read__time', soup=soup)
    ## Extract and get the text if date_tag is found
    if date_tag:
      date_text = date_tag.text.strip()
      date_time = date_text.split(" - ")[1] if ' - ' in date_text else "Date format incorrect"
    else:
      date_time = "Date Not Found"

    # Get Author
    author_tag = validate_info(tag='div', classes='credit-title-name', soup=soup) or validate_info(tag='div', classes='opinion__author', soup=soup)
    author = author_tag.get_text(strip=True) if author_tag else "No author found"

    # Get Image Tag
    img_tag = validate_info(tag='div', classes='photo__wrap', soup=soup)
    img_url = img_tag.find('img').get('src') if img_tag else "No Image URL found"

    # Get Content
    content_tag = validate_info(tag='div', classes='read__content', soup=soup)
    content = content_tag.get_text() if content_tag else "No content found"

    # Add info to the empty dictionary
    info['Link'] = link
    info['Title'] = title
    info['Date'] = date_time
    info['Author'] = author
    info['Image URL'] = img_url
    info["Content"] = content

  else:
    print(f"Failed to extract info. Status code: {status}")
  return info

# Get info from all links
def get_info_all_links(links):

  # Create a thread pool to process multiple links concurrently
  executor = ThreadPoolExecutor()
  all_info = list(executor.map(get_info, links))
  
  return all_info