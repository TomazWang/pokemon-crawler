import json
import os
from queue import Queue
from threading import Thread, current_thread

# custom module
import requests

import crawler


Q = Queue()  # global queue
_WORKER_THREAD_NUM = 50  # max worker number
_NUMBER_OF_POKEMON_TO_CRAWL = 151
_FORCE_DOWNLOAD_IMAGE = False


def into_json(pokemon_list):

    json_element_strs = []
    for p in pokemon_list:
        # print(p.__class__.__name__)
        # print(p.__dict__)
        # print(json.dumps(p.__dict__, ensure_ascii=False))
        json_element_strs.append(json.dumps(p, ensure_ascii=False, default=lambda o: o.__dict__))

    json_str = '[{}]'.format(',\n'.join(json_element_strs))

    # Add encodeing='utf-8' for Chinese names
    with open('pokedex.json', 'w', encoding='utf8') as json_file:
        # Add ensure_ascii=False to avoid Chinese character got convert to unicode.
        json_file.write(json_str)
    print('json done')


def download_img(poke):
    img_path = os.getcwd() + '/img'
    if not os.path.exists(img_path):
        os.mkdir(img_path)

    if not _FORCE_DOWNLOAD_IMAGE:
        # if force download doesn't turn on, check file
        if os.path.isfile(img_path+'/'+poke.pic_name):
            print('image already exist')
            return

    pic_content = requests.get(poke.pic_link).content
    cwd = os.getcwd()

    with open('{}/img/{}'.format(cwd, poke.pic_name), 'wb') as pic_file:
        pic_file.write(pic_content)

    print('download image {}'.format(poke.pic_name))


def fetch_pic():
    while not Q.empty():
        poke = Q.get()
        print('processing poke #{} in Thread #{}'.format(poke.id, current_thread()))

        link = poke.link
        pic_link = crawler.get_pic_link(link)
        poke.pic_link = pic_link
        poke.pic_name = '{}_{}.png'.format(poke.id,poke.name_en.lower())

        download_img(poke)
        Q.task_done()

def main():
    pokemon_list = crawler.get_all_pokemon(_NUMBER_OF_POKEMON_TO_CRAWL)

    worker_threads = []

    for pokemon in pokemon_list:
        Q.put(pokemon)

    for i in range(_WORKER_THREAD_NUM):
        t = Thread(target=fetch_pic)
        t.daemon = True
        t.start()
        worker_threads.append(t)

    for thread in worker_threads:
        thread.join()

    Q.join()
    into_json(pokemon_list)

if __name__ == '__main__':
    main()
