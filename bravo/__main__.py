from pathlib import Path

from bravo.data import BASE_URL, PRODUCT_LINKS_FILE
from bravo.parsing.catalog import (get_catalog_links, get_page_links,
                                   get_product_links)
from bravo.utils import get_html, add_in_yaml


if not Path(PRODUCT_LINKS_FILE).exists():
    catalog_html_code = get_html(BASE_URL)
    catalog_links = get_catalog_links(catalog_html_code)
    page_links = get_page_links(catalog_links)

    for link in get_product_links(page_links):
        print(link)
        add_in_yaml(link, PRODUCT_LINKS_FILE, flow_style=False)
