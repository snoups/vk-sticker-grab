import os
import time
from concurrent.futures import ThreadPoolExecutor
from threading import local

import requests
from requests.sessions import Session

LAST_STICKER_ID = 5 # 72740
STICKER_RESOLUTION = 512 # 64 / 128 / 256 / 512
URL = 'https://vk.com/sticker/{}/{}.png'

sticker_ids = [str(id) for id in range(1, LAST_STICKER_ID + 1)]
thread_local = local()

def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session

def save_sticker(sticker_id: str, content: bytes) -> None:
    filename = f'stickers/{sticker_id}.png'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(content)

def download_sticker(sticker_id: str) -> None:
    session = get_session()
    with session.get(URL.format(sticker_id, STICKER_RESOLUTION)) as r:
        msg = 'Download sticker {}: {}!'
        if r.status_code == 200:
            print(msg.format(sticker_id, 'SUCCESS'))
            save_sticker(sticker_id, r.content)
        else: # TODO: make redownload sticker
            print(msg.format(sticker_id, 'FAIL'))

def download() -> None:
    with ThreadPoolExecutor() as executor:
        executor.map(download_sticker, sticker_ids)

def main() -> None: 
    start = time.time()
    download()
    end = time.time()
    print(f'Download {len(sticker_ids)} stickers in {end - start} seconds.')

if __name__ == '__main__':
    main()
