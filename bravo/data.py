from pathlib import Path
from urllib.parse import urljoin

BASE_URL = 'https://door.website4sale.online/'

PRODUCT_PREFIX_URL = urljoin(
    BASE_URL,
    'index.php?route=product/product&product_id='
)

USER_AGENT = ('Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) '
              'AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 '
              'Mobile/15E148 Safari/604.1')

HEADERS = {'User-Agent': USER_AGENT}

OUT_DIR = Path('out_data')
PRODUCT_LINKS_FILE = OUT_DIR / 'product_links.yaml'
PRODUCT_CARDS_FILE = OUT_DIR / 'product_cards.yaml'
PRODUCT_CARDS_JSON_FILE = OUT_DIR / 'product_cards.json'
IMG_DIR = OUT_DIR / 'img'
