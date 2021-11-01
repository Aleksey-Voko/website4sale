import json
import logging
from pathlib import Path

import requests
from ruamel.yaml import YAML

from bravo.data import HEADERS


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    print(url)
    print(f'status code = {response.status_code}')
    print('=' * 30)
    print()
    return response.text


def add_in_yaml(data, out_file: str, encoding='utf-8', flow_style=True):
    yaml = YAML(pure=True)
    yaml.default_flow_style = flow_style
    sep = ''
    if Path(out_file).exists():
        mode = 'a'
        if Path(out_file).stat().st_size:
            if isinstance(data, dict):
                sep = '---\n'
    else:
        mode = 'w'
    Path(out_file).parent.mkdir(parents=True, exist_ok=True)
    with open(Path(out_file), mode, encoding=encoding) as f_out:
        if sep:
            f_out.write(sep)
        yaml.dump(data, f_out)


def get_from_yaml(input_file: str, encoding='utf-8'):
    yaml = YAML(pure=True)
    with open(Path(input_file), encoding=encoding) as f_in:
        for item in yaml.load_all(f_in):
            yield item


def yaml_to_json(yaml_file, json_file, encoding='utf-8'):
    card_list = list(get_from_yaml(yaml_file))
    indent = ' ' * 4
    with open(json_file, 'w', encoding=encoding) as out_f:
        json.dump(card_list, out_f, ensure_ascii=False, indent=indent)


def download_file(url, f_name):
    logging.basicConfig(level=logging.INFO)

    Path(f_name).parent.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            logging.info(f'\nFile: {Path(f_name).name}\n')
            response = requests.get(url, headers=HEADERS)
            logging.info(f'\nDownload file:\n{url}\n{"=" * 30}\n')
            with open(Path(f_name), 'wb') as f_out:
                f_out.write(response.content)
            break
        except Exception as e:
            logging.warning(f'{"#" * 10} Exception {"#" * 10}')
            logging.warning(f'{e}')
            logging.warning(f'{"#" * 10} Exception {"#" * 10}\n')
