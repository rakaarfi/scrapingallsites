import requests

from scraping.requesting import get_requests
# from requesting import get_requests

# Extract all links
def get_link(soup):
# Find all links tag
  links = soup.find_all('a', class_='media__link')
  if not links:
    links = soup.find_all('a', class_='flex gap-4 group items-center')

  # Iterate each link to an empty list
  link_list = []
  for link in links:
    href = link.get('href')

    # Excluding some from link
    if len(href) > 50 and "https://20.detik.com/" not in href and ".com/foto-" not in href:
      link_list.append(href)
  
  return link_list

# Extract img URL, Title, Content, author, date
def get_info(link):

  # Add ?single=1 to extract all pages from the news
  link = link + "?single=1"

  session = requests.Session()
  soup, status = get_requests(url=link, session=session)

  info = {}
  if status == 200:
    # Find tag that have link inside
    article = soup.find('article', class_='detail')

    # Find title, author, date, img url
    try:
      img = article.find('img').get('src')
    except AttributeError as e:
      img = None
      print(f"An exception occurred in Image: {e}")

    title = validate_info(tag='h1', classes='detail__title', article=article).get_text(strip=True)
    author = validate_info(tag='div', classes='detail__author', article=article).get_text(strip=True)
    date = validate_info(tag='div', classes='detail__date', article=article).get_text(strip=True)    

    # Find content
    content = validate_info(tag='div', classes='detail__body-text itp_bodycontent', article=article).get_text(strip=True)

    # Add info to the empty dictionary
    info["Link"] = link
    info["Title"] = title
    info["Author"] = author
    info["Date"] = date
    info["Image URL"] = img
    info["Content"] = content
  return info

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
  all_info = []
  for index, link in enumerate(links):
    info = get_info(link=link)
    if info:
      info["Index"] = index + 1  # Add index to info dict
      all_info.append(info)
    print(link)
  print(f"Total links extracted are {len(links)}")

  return all_info, index

if __name__ == "__main__":
  session = requests.Session()
  soup, status = get_requests(url='https://www.detik.com/pop/indeks/', session=session)
  link = get_link(soup)
  # info, index = get_info_all_links(links=link)

  # # link = 'https://megapolitan.kompas.com/read/2024/10/05/17581561/debat-pilkada-jakarta-memuluskan-transformasi-jadi-kota-global'
  # link = 'https://www.kompas.com/hype/read/2024/10/09/120752466/lima-bulan-bercerai-dodhy-kangen-band-menikahi-ayu-rizki-lagi'
  # content = get_info(link)
  print(link)