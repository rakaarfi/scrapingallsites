import requests
from bs4 import BeautifulSoup as bs

from scraping.requesting import get_requests

# Extract all links
def get_links(response_text):
  soup = bs(response_text, 'html.parser')

  article = soup.find('div', class_='articleList -list')

  # Find all links tag
  links = article.find_all('a', class_='article-link')

  # Iterate each link to an empty list
  link_list = []
  for i in links:
    link = i.get('href')
    link_list.append(link)

  return link_list

# Extract Title, Date, Author, Image URL, Content/Paragraphs
def get_info(response_text, link):
  soup = bs(response_text, 'html.parser')

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

  # Get Title
  title_tag = validate_info(tag='h1', classes='read__title', soup=soup)
  title = title_tag.text.strip() if title_tag else "Title Not Found"

  # Get Date Tag
  date_tag = validate_info(tag='div', classes='read__time', soup=soup)
  ## extract and get the text if date_tag is found, 
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
  content = validate_info(tag='div', classes='read__content', soup=soup)
  p_tags = content.find_all('p')
  p = [i.get_text() for i in p_tags]

  # Add info to the empty dictionary
  info['Link'] = link
  info['Title'] = title
  info['Date'] = date_time
  info['Author'] = author
  info['Image URL'] = img_url
  info["Content"] = p

  return info

# Get info from all links
def get_info_all_links(response_texts, links):

  all_info = []
  # Loop through responses and links with indexing
  for index, (response_text, link)in enumerate(zip(response_texts, links)):
    try:
      # Attempt to extract info from the response text and link
      info = get_info(response_text, link)

      if info:
        info["Index"] = index + 1 # Add index to info dict
        all_info.append(info)

    except Exception as e:
      # Handle any exceptions that occur during extraction
      print(f"Error extracting info from {link}: {e}")
      
      continue # Skip to the next link if an error occurs

  return all_info, index