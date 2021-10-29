from bs4 import BeautifulSoup

from bravo.data import BASE_URL
from bravo.utils import get_html


def get_catalog_links(html_code) -> list:
    catalog_links = []

    soup = BeautifulSoup(html_code, 'html.parser')
    navbar_tag = soup.find('ul', {'class': 'nav navbar-nav'})
    li_tags = navbar_tag.contents

    for li_tag in li_tags:
        if li_tag:
            a_tag = li_tag.find('a')
            if a_tag and a_tag != -1:
                href = a_tag.get('href')
                if href == '#':
                    href = f'{BASE_URL}mezhkomnatnye_dveri/'
                catalog_links.append(href)

    return catalog_links


def get_page_links(catalog_links: list) -> list:
    page_links = []

    for url in catalog_links:
        page_links.append(url)
        page_count = get_page_count(url)
        if page_count:
            page_links += generate_page_links(url, page_count)

    return page_links


def get_page_count(url):
    html_code = get_html(url)
    soup = BeautifulSoup(html_code, 'html.parser')

    pagination_tag = soup.find('ul', {'class': 'pagination'})

    if pagination_tag:
        li_tags = pagination_tag.find_all('li')
        last_a_tag = li_tags[-1].find('a')
        href = last_a_tag.get('href')
        count = href.split('=')[-1]
        return int(count)
    else:
        return None


def generate_page_links(url, count):
    page_links = []

    for page in range(2, count + 1):
        page_links.append(f'{url}?page={page}')

    return page_links
