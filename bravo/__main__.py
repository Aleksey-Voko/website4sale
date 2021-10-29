from bravo.data import BASE_URL
from bravo.parsing.catalog import get_catalog_links, get_page_links
from bravo.utils import get_html


catalog_html_code = get_html(BASE_URL)
catalog_links = get_catalog_links(catalog_html_code)
page_links = get_page_links(catalog_links)
