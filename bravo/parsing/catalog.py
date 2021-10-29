from bs4 import BeautifulSoup

from bravo.data import BASE_URL


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
