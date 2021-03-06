import requests
from bs4 import BeautifulSoup

from bravo.data import HEADERS, PRODUCT_PREFIX_URL


def get_product_cards(links):
    with requests.Session() as sess:
        for link in links:
            print('#### Товар...')
            print(link)
            product_card = get_product_card(link, sess)
            if product_card.keys():
                yield product_card
            print('=' * 100)
            print()


def get_product_card(link, sess: requests.sessions.Session) -> dict:
    product_card = {}

    while True:
        try:

            response = sess.get(link, headers=HEADERS)
            if response.status_code == requests.codes.ok:
                print('status_code', str(response.status_code), sep=' -> ')
                print()

                html_code = response.text
                soup = BeautifulSoup(html_code, 'html.parser')

                product_card['link'] = link
                product_card['meta_title'] = get_meta_title(soup)
                product_card['meta_description'] = get_meta_description(soup)
                product_card['keywords'] = get_keywords(soup)
                product_card['h1'] = get_h1(soup)

                images, owl_images = get_images(soup)
                product_card['images'] = images
                product_card['owl_images'] = owl_images

                product_card['Описание'] = get_description(soup)
                product_card['Характеристики'] = get_specification(soup)

                product_card[
                    'Все характеристики'
                ] = get_all_specification(soup)

                product_card['Комплектующие'] = get_components(soup)
                product_card['Размеры'] = get_dimensions(soup)

                break
                ####################

            elif response.status_code == 404:
                product_card = {}
                print(response.url + '\n',
                      '!!! Get link request failed !!!'.upper(), sep=' -> ')
                print('status_code', str(response.status_code), sep=' -> ')
                break
            else:
                print(response.url + '\n',
                      '!!! Get link request failed !!!'.upper(), sep=' -> ')
                print('status_code', str(response.status_code), sep=' -> ')

            print('=' * 100)
            print()
            continue

        except Exception as e:
            print(('#' * 20) + '  Exception  ' + ('#' * 20))
            print(link)
            print(e)
            print(('#' * 20) + '  Exception  ' + ('#' * 20))
            print()

    return product_card


def get_meta_title(soup: BeautifulSoup):
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.text
    else:
        return ''


def get_meta_description(soup: BeautifulSoup):
    meta_description_tag = soup.find(
        'meta', {'name': 'description'})
    if meta_description_tag:
        return meta_description_tag.get('content')
    else:
        return ''


def get_keywords(soup: BeautifulSoup):
    keywords_tag = soup.find('meta', {'name': 'keywords'})
    if keywords_tag:
        return keywords_tag.get('content')
    else:
        return ''


def get_h1(soup: BeautifulSoup):
    h1_tag = soup.find('h1')
    return h1_tag.text.strip()


def get_images(soup: BeautifulSoup) -> tuple:
    images = []

    group_1_tag = soup.find('div', {'class': 'hpm-group hpm-group-1'})
    if group_1_tag:
        hpm_item_tags = group_1_tag.find_all('div', {'class': 'hpm-item'})
        print('##### Get images...')
        for hpm_item_tag in hpm_item_tags:
            img = {'data-id': hpm_item_tag.get('data-id')}

            img_tag = hpm_item_tag.find('img')
            if img_tag:
                img['name'] = img_tag.get('title')
                img['color'] = img_tag.get('src')
            else:
                img['name'] = ''
                img['color'] = ''

            data_id = img['data-id'].split(',')
            image = get_image(data_id[0])
            img['image'] = image
            images.append(img)
        print()

    owl_images = []

    owl_img_tag = soup.find('div', {'id': 'owl-images'})
    if owl_img_tag:
        item_tags = owl_img_tag.find_all('div', {'class': 'item'})
        for item_tag in item_tags:
            a_tag = item_tag.find('a')
            owl_images.append(a_tag.get('id'))

    return images, owl_images


def get_image(var_id):
    link = f'{PRODUCT_PREFIX_URL}{var_id}'
    print(link)
    with requests.Session() as sess:
        response = sess.get(link, headers=HEADERS)
        print('status_code', str(response.status_code), sep=' -> ')

        html_code = response.text
        soup = BeautifulSoup(html_code, 'html.parser')

        img_box_tag = soup.find('div', {'class': 'main_img_box'})
        image_tag = img_box_tag.find('div', {'class': 'image'})
        a_tag = image_tag.find('a', {'class': 'main-image'})
        href = a_tag.get('href')

        return href


def get_description(soup: BeautifulSoup):
    description_tag = soup.find('div', {'itemprop': 'description'})
    description = description_tag.text.strip()
    return description


def get_specification(soup: BeautifulSoup) -> dict:
    specification = {}

    info_tag = soup.find(
        'div', {'class': 'col-sm-12 col-md-7 product_informationss'}
    )
    li_tags = info_tag.find_all('li', {'class': 'dotted-line'})
    for li_tag in li_tags[1:]:
        left_tag = li_tag.find('div', {'class': 'dotted-line_left'})
        key = left_tag.text.strip().replace(':', '')

        right_tag = li_tag.find('div', {'class': 'dotted-line_right'})
        a_tag = right_tag.find('a')
        if a_tag:
            href = a_tag.get('href')
        else:
            href = None

        span_tag = right_tag.find('span')
        if span_tag:
            spec_value = span_tag.text.strip()
        else:
            spec_value = right_tag.text.strip()

        if href:
            value = (spec_value, href)
        else:
            value = spec_value

        specification[key] = value

    return specification


def get_all_specification(soup: BeautifulSoup) -> dict:
    specification = {}

    tab_tag = soup.find('div', {'id': 'tab-specification'})
    tbody_tag = tab_tag.find('tbody')
    tr_tags = tbody_tag.find_all('tr', {'itemprop': 'additionalProperty'})
    for tr_tag in tr_tags:
        td_name = tr_tag.find('td', {'itemprop': 'name'})
        name = td_name.text.strip()
        td_value = tr_tag.find('td', {'itemprop': 'value'})
        value = td_value.text.strip()
        specification[name] = value

    return specification


def get_components(soup: BeautifulSoup) -> list:
    components = []

    complection_tag = soup.find('div', {'id': 'tab-complection'})
    if complection_tag:
        form_group_tags = complection_tag.find_all(
            'div', {'class': 'form-group'})
        for form_group_tag in form_group_tags:
            table_tag = form_group_tag.find('table')

            component = {}
            head_keys = []
            thead_tag = table_tag.find('thead')
            td_tags = thead_tag.find_all('td')
            for td_tag in td_tags:
                td_text = td_tag.text.strip()
                if td_text:
                    if td_text != 'Количество:':
                        head_keys.append(td_text)
                else:
                    head_keys.append('image')

            tbody_tag = table_tag.find('tbody')
            tr_tags = tbody_tag.find_all('tr')
            for tr_tag in tr_tags:
                td_tags = tr_tag.find_all('td')
                for head_key, td_tag, in zip(head_keys, td_tags):
                    img_tag = td_tag.find('img')
                    if img_tag:
                        component[head_key] = img_tag.get('src')
                    else:
                        component[head_key] = td_tag.text.strip()
                components.append(component)

    return components


def get_dimensions(soup: BeautifulSoup) -> list:
    dimensions = []

    group_0_tag = soup.find('div', {'class': 'hpm-group hpm-group-0'})
    print('##### Get prices...')
    if group_0_tag:
        hpm_item_tags = group_0_tag.find_all('div', {'class': 'hpm-item'})
        if hpm_item_tags:
            for hpm_item_tag in hpm_item_tags:
                dim = {
                    'name': hpm_item_tag.get('data-key'),
                    'data-id': hpm_item_tag.get('data-id'),
                }
                data_id = dim['data-id'].split(',')
                dim['prices'] = get_prices(data_id[0])

                dimensions.append(dim)
        else:
            hpm_item_tag = group_0_tag.find('div', {'class': 'hpm-item'})
            dim = {
                'name': hpm_item_tag.get('data-key'),
                'data-id': hpm_item_tag.get('data-id'),
            }
            data_id = dim['data-id'].split(',')
            dim['prices'] = get_prices(data_id[0])
            dimensions.append(dim)
    print()

    return dimensions


def get_prices(var_id) -> dict:
    link = f'{PRODUCT_PREFIX_URL}{var_id}'
    print(link)
    with requests.Session() as sess:
        response = sess.get(link, headers=HEADERS)
        print('status_code', str(response.status_code), sep=' -> ')

        html_code = response.text
        soup = BeautifulSoup(html_code, 'html.parser')

        prices = {}

        prices_main_tag = soup.find('div', {'class': 'product-prices-main'})
        main_label_tag = prices_main_tag.find('span', {'class': 'price-label'})
        if main_label_tag:
            main_label = main_label_tag.text.strip()
        else:
            main_label = 'main_price'

        main_old_price_tag = prices_main_tag.find(
            'span', {'class': 'oldprice'}
        )
        if main_old_price_tag:
            main_old_price = main_old_price_tag.text.strip()
            main_old_price = main_old_price.replace(' р.', '')
            main_old_price = main_old_price.replace(' ', '')
            main_old_price = int(main_old_price)
        else:
            main_old_price = ''

        main_price_tag = prices_main_tag.find('meta', {'itemprop': 'price'})
        main_price = main_price_tag.get('content')
        main_price = int(float(main_price))

        prices[main_label] = {
            'old_price': main_old_price,
            'price': main_price,
        }

        prices_complection_tag = soup.find(
            'div', {'class': 'product-prices-complection'}
        )
        if prices_complection_tag:
            compl_label_tag = prices_complection_tag.find(
                'span', {'class': 'price-label'}
            )
            compl_label = compl_label_tag.text.strip()

            compl_old_price_tag = prices_complection_tag.find(
                'span', {'class': 'price-old'}
            )
            if compl_old_price_tag:
                compl_old_price = compl_old_price_tag.text.strip()
                compl_old_price = compl_old_price.replace(' р.', '')
                compl_old_price = compl_old_price.replace(' ', '')
                compl_old_price = int(compl_old_price)

                compl_price_tag = prices_complection_tag.find(
                    'span', {'class': 'price-new'}
                )
                compl_price = compl_price_tag.text.strip()
            else:
                compl_old_price = ''
                compl_price_tag = prices_complection_tag.find(
                    'div', {'class': 'product-price-complection'}
                )
                compl_price = compl_price_tag.text.strip()

            compl_price = compl_price.replace(' р.', '')
            compl_price = compl_price.replace(' ', '')
            compl_price = int(compl_price)

            prices[compl_label] = {
                'old_price': compl_old_price,
                'price': compl_price,
            }

        return prices
