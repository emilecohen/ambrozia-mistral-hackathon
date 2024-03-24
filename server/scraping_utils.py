import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_base_url(url):
    # Extract scheme and netloc
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def check_url(url_initial, url):
    # Parse the initial URL and the URL to be checked
    parsed_initial = urlparse(url_initial)
    parsed_url = urlparse(url)

    # Extract the domain names, ignoring possible 'www.' prefixes
    domain_initial = parsed_initial.netloc.split('www.')[-1]
    domain_url = parsed_url.netloc.split('www.')[-1]

    # Check if the domain names match and if the URL to be checked starts with the base URL
    return domain_url == domain_initial and url.startswith(parsed_initial.scheme + "://")


def scrape_website(url_initial):
    urls_to_scrap, urls_scraped = [url_initial], []
    i = 0
    scraped_dict = {}

    while len(urls_to_scrap) != 0 and i<=30:
        url = urls_to_scrap[0]
        if not check_url(url_initial, url) or url in urls_scraped:
          print('not url: ', url)
          urls_to_scrap.pop(0)
          continue

        else:
            print('url: ', url)
            urls_scraped.append(url)
            urls_to_scrap.pop(0)
            data = []

            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                html = response.text


                # Parse the HTML content
                soup = BeautifulSoup(html, 'html.parser')

                # Extracting all hyperlinks
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if type(href) == str :
                        if href not in urls_scraped and href not in urls_to_scrap:
                            urls_to_scrap.append(href)

                page_title = soup.title.text if soup.title else 'No title found'

                # Extracting all text from paragraphs
                paragraphs = soup.find_all('p')
                for paragraph in paragraphs:
                    data.append(paragraph.text.strip())

                scraped_dict[page_title]= data
            else:
                print("Failed to retrieve the website")

            i += 1
    return scraped_dict
