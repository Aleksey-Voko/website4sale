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
