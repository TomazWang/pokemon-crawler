import requests
from bs4 import BeautifulSoup
import re
import json

BASE_URL = 'https://wiki.52poke.com/'


def remove_white_space(origin_str):
    new_str = origin_str.strip()
    new_str.replace(' ', '')
    return new_str


def get_all_pokemon():
    pokemons = []

    # use requests to get page
    page = requests.get('https://wiki.52poke.com/zh-hant/宝可梦列表（按全国图鉴编号）/简单版')
    page_text = page.text

    # parse html by BeautifulSoup
    page_html = BeautifulSoup(page_text, 'html.parser')

    # find the table contents the list of all pokemon
    table = page_html.find('table', class_='a-c roundy eplist bgl-X b-Y bw-2')
    rows = table.find_all('tr')

    # remove title row
    rows.pop(0)
    rows.pop(0)

    for row in rows:

        # remove generation title
        if 'colspan' not in row.td.attrs:
            infos = row.find_all('td')
            number = remove_white_space(infos[0].text)
            number = re.sub(r'\W', '', number)
            number = int(number)

            # all pokemon in gen 1 & gen 2
            if number > 251:
                break

            name_zh = remove_white_space(infos[1].text)
            name_en = remove_white_space(infos[3].text)
            link = infos[1].a['href']
            #  link : /wiki/%E5%A6%99%E8%9B%99%E7%A7%8D%E5%AD%90
            link = re.sub(r'/wiki', BASE_URL + 'zh-hant', link)

            pokemon = {
                'id': number,
                'name_zh': name_zh,
                'name_en': name_en,
                'link': link,
            }

            pokemons.append(pokemon)

    return pokemons


def get_pic_link(link):
    page = requests.get(link)
    page_text = page.text
    page_html = BeautifulSoup(page_text, 'html.parser')

    # page_html.find('a', class_='image').img['data-url'] : //media.52poke.com/wiki/thumb/7/73/002Ivysaur.png/300px-002Ivysaur.png
    img_link = 'http:' + page_html.find('a', class_='image').img['data-url']

    return img_link


def into_json(pokemon_list):
    # Add encodeing='utf-8' for Chinese names
    with open('pokedex.json', 'w', encoding='utf8') as json_file:
        # Add ensure_ascii=False to avoid Chinese character got convert to unicode.
        json.dump(pokemon_list, json_file, ensure_ascii=False)


if __name__ == '__main__':

    pokemon_list = get_all_pokemon()
    for pokemon in pokemon_list:
        pic_link = get_pic_link(pokemon['link'])
        pokemon['pic_link'] = pic_link

    into_json(pokemon_list)
    # print(pokemon_list)
