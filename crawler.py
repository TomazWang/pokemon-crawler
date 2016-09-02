import requests
from bs4 import BeautifulSoup
import re

from Pokemon import Pokemon

BASE_URL = 'https://wiki.52poke.com/'


def remove_white_space(origin_str):
    new_str = origin_str.strip()
    new_str.replace(' ', '')
    return new_str


def get_all_pokemon(total_num_of_pokemon = 151):
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

    generation = 0

    for row in rows:

        # remove generation title
        if 'colspan' not in row.td.attrs:
            infos = row.find_all('td')
            poke_id = int(re.sub(r'\W', '', remove_white_space(infos[0].text)))

            if poke_id > total_num_of_pokemon:
                break

            name_zh = remove_white_space(infos[1].text)
            name_en = remove_white_space(infos[3].text)
            link = infos[1].a['href']
            #  link : /wiki/%E5%A6%99%E8%9B%99%E7%A7%8D%E5%AD%90
            link = re.sub(r'/wiki', BASE_URL + 'zh-hant', link)

            pokemon = Pokemon(poke_id, name_zh=name_zh, name_en= name_en)
            pokemon.link = link
            pokemon.generation = generation

            pokemons.append(pokemon)

        else:
            generation += 1
    return pokemons


def get_pic_link(link):
    page = requests.get(link)
    page_text = page.text
    page_html = BeautifulSoup(page_text, 'html.parser')

    # page_html.find('a', class_='image').img['data-url'] : //media.52poke.com/wiki/thumb/7/73/002Ivysaur.png/300px-002Ivysaur.png
    img_link = 'http:' + page_html.find('a', class_='image').img['data-url']

    return img_link

# if __name__ == '__main__':
#
#     pokemon_list = get_all_pokemon()
#     for pokemon in pokemon_list:
#         pic_link = get_pic_link(pokemon['link'])
#         pokemon['pic_link'] = pic_link
#
#     into_json(pokemon_list)
    # print(pokemon_list)
