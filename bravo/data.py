BASE_URL = 'https://door.website4sale.online/'
PRODUCT_PREFIX_URL = f'{BASE_URL}index.php?route=product/product&product_id='

USER_AGENT = ('Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) '
              'AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 '
              'Mobile/15E148 Safari/604.1')

HEADERS = {'User-Agent': USER_AGENT}

PRODUCT_LINKS_FILE = 'out_data/product_links.yaml'
PRODUCT_CARDS_FILE = 'out_data/product_cards.yaml'
PRODUCT_CARDS_JSON_FILE = 'out_data/product_cards.json'
