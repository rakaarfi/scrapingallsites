import requests
from scraping.requesting import get_requests
# from requesting import get_requests

# Extract all links
def get_links(soup):
  article = soup.find('div', class_='articleList -list')

  links = article.find_all('a', class_='article-link')
  link_list = []
  for i in links:
    link = i.get('href')
    link_list.append(link)

  print(f"The total of extracted links is {len(link_list)}")
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
  title = None
  date_time = None
  author = None
  img_url = None
  content = None
  if status == 200:
    # Get Title
    title_tag = validate_info(tag='h1', classes='read__title', soup=soup)
    ## If title_tag is found, extract and get the text
    if title_tag:
      title = title_tag.get_text(strip=True)
    ## If title_tag isn't found:
    else:
      title = "Title Not Found"

    # Get Date Tag
    date_tag = validate_info(tag='div', classes='read__time', soup=soup)
    ## If date_tag is found, extract and get the text
    if date_tag:
      date_text = date_tag.text.strip()

      # Check if the text contains the " - "
      if ' - ' in date_text:
        date_time = date_text.split(" - ")[1]
      else:
        date_time = "Date format incorrect"
    ## If date_tag isn't found
    else:
      date_time = "Date Not Found"

    # Get Author
    ## Get Author from class:'credit-title-name'
    author_tag = validate_info(tag='div', classes='credit-title-name', soup=soup)
    if author_tag:
      author = author_tag.get_text(strip=True)
    ## If not found from above class:
    else:
      author_tag = validate_info(tag='div', classes='opinion__author', soup=soup)
      if author_tag:
        author = author_tag.get_text(strip=True)
    ## If both of them not found:
    if not author:
      author = "No Author Found"

    # Get Image Tag
    img_tag = validate_info(tag='div', classes='photo__wrap', soup=soup)
    # If img_tag found:
    if img_tag:
      img_url = img_tag.find('img').get('src')
    # If img_tag not found:
    else:
      img_url = 'No Image URL Found'

    info['Link'] = link
    info['Title'] = title
    info['Date'] = date_time
    info['Author'] = author
    info['Image URL'] = img_url

    # Get Content
    content = validate_info(tag='div', classes='read__content', soup=soup)
    p_tags = content.find_all('p')
    p = []
    for i in p_tags:      
      p.append(i.get_text())
    info["Content"] = p

  else:
    print(f"Failed to extract info. Status code: {status}")
    info['Link'] = link
    info['Title'] = "Title Not Found"
    info['Date'] = "Date Not Found"
    info['Author'] = "No Author Found"
    info['Image URL'] = "No Image URL Found"
    info['Content'] = "No Content Found"

  return info

# Get info from all links
def get_info_all_links(links):
  all_info = []
  for index, link in enumerate(links):
    info = get_info(link=link)
    print(f"Extracting {index+1} out of {len(links)}.")
    if info:
      info["Index"] = index + 1
      all_info.append(info)
    print("Info added.")
  return all_info, index

if __name__ == "__main__":
  session = requests.Session()
  # soup, status = get_requests(url='https://indeks.kompas.com/?site=news', session=session)
  # link = get_links(soup)
  # info, index = get_info_all_links(links=link)

  # link = 'https://megapolitan.kompas.com/read/2024/10/05/17581561/debat-pilkada-jakarta-memuluskan-transformasi-jadi-kota-global'
  link = 'https://www.kompas.com/hype/read/2024/10/09/120752466/lima-bulan-bercerai-dodhy-kangen-band-menikahi-ayu-rizki-lagi'
  content = get_info(link)
  print(content)