from pathlib import Path, PurePosixPath

from slugify import slugify

from bravo.data import PRODUCT_CARDS_FILE, IMG_DIR, IMG_LINK_DICT
from bravo.utils import get_from_yaml, add_in_yaml, download_file


def save_img_link_dict():
    product_cards = list(get_from_yaml(PRODUCT_CARDS_FILE))

    for card in product_cards:
        model = card['Характеристики']['Модель']
        for img in card['images']:
            color_name = img['name']
            link = img['image']
            ext = Path(link).suffix
            slugify_name = slugify(f'{model}_{color_name}')
            file_name = f'{slugify_name}{ext}'
            path_name = IMG_DIR / file_name

            img_dict = {
                'model': model,
                'color_name': color_name,
                'link': link,
                'path_name': str(PurePosixPath(path_name)),
            }

            add_in_yaml(img_dict, IMG_LINK_DICT, flow_style=False)


def download_images():
    img_links_dict = list(get_from_yaml(IMG_LINK_DICT))
    for img_dct in img_links_dict:
        link = img_dct['link']
        path_name = img_dct['path_name']
        if not Path(path_name).exists():
            print(path_name)
            download_file(link, path_name)
