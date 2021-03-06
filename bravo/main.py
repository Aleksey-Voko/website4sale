from pathlib import Path

from bravo.data import (BASE_URL, PRODUCT_LINKS_FILE, PRODUCT_CARDS_FILE,
                        PRODUCT_CARDS_JSON_FILE, IMG_LINK_DICT)
from bravo.parsing.catalog import (get_catalog_links, get_page_links,
                                   get_product_links)
from bravo.parsing.images import save_img_link_dict, download_images
from bravo.parsing.product_card import get_product_cards
from bravo.utils import get_html, add_in_yaml, get_from_yaml, yaml_to_json


def main():
    if not Path(PRODUCT_LINKS_FILE).exists():
        print('### Ссылки на страницы категорий...')
        catalog_html_code = get_html(BASE_URL)

        print('### Ссылки на страницы пагинации...')
        catalog_links = get_catalog_links(catalog_html_code)
        page_links = get_page_links(catalog_links)

        print('### Ссылки на страницы товаров...')
        for link in get_product_links(page_links):
            add_in_yaml(link, PRODUCT_LINKS_FILE, flow_style=False)

    product_links = list(get_from_yaml(PRODUCT_LINKS_FILE))
    product_links = [x for x in product_links if not x.endswith('=')]

    if Path(PRODUCT_CARDS_FILE).exists():
        product_cards = get_from_yaml(PRODUCT_CARDS_FILE)
        completed_links = [x['link'] for x in product_cards]
    else:
        completed_links = []

    product_links = sorted(list(set(product_links) - set(completed_links)))

    print('### Карточки товаров...')
    print('=' * 30)
    print()
    for product_card in get_product_cards(product_links):
        add_in_yaml(product_card, PRODUCT_CARDS_FILE, flow_style=False)
        completed_links.append(product_card['link'])

    if not Path(PRODUCT_CARDS_JSON_FILE).exists():
        print('### Конвертация в JSON...')
        yaml_to_json(PRODUCT_CARDS_FILE, PRODUCT_CARDS_JSON_FILE)

    if not Path(IMG_LINK_DICT).exists():
        print('### Словарь для фото...')
        save_img_link_dict()

    print('### Загрузка фото...')
    download_images()
