import os
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from threading import local

import requests
from requests.sessions import Session

VALID_STICKER_RESOLUTIONS = [64, 128, 256, 512]
MAX_STICKERS = 72740
sticker_resolution = 512
sticker_ids = None
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
    base_url = 'https://vk.com/sticker/{}/{}.png'
    session = get_session()
    with session.get(base_url.format(sticker_id, sticker_resolution)) as r:
        msg = 'Download sticker {}: {}!'
        if r.status_code == 200:
            print(msg.format(sticker_id, 'SUCCESS'))
            save_sticker(sticker_id, r.content)
        else:  # TODO: make redownload sticker
            print(msg.format(sticker_id, 'FAIL'))


def download() -> None:
    with ThreadPoolExecutor() as executor:
        executor.map(download_sticker, sticker_ids)


def get_args() -> dict:
    parser = argparse.ArgumentParser(description='vk-sticker-grab')
    parser.add_argument('-r', '--resolution', type=int, default=512,
                        help='sticker resolution (only 64 / 128 / 256 / 512)')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-a', '--amount', type=int, required=True,
                          help=f'number of stickers to download (max {MAX_STICKERS})')
    args = parser.parse_args()

    if args.resolution not in VALID_STICKER_RESOLUTIONS:
        parser.error('sticker resolution (only 64 / 128 / 256 / 512)')

    if args.amount < 1:
        parser.error('Minimum amount is 1')
    elif args.amount > 72740:
        parser.error(f'Maximum amount is {MAX_STICKERS}')

    sticker_ids = [str(id) for id in range(1, args.amount + 1)]
    sticker_resolution = args.resolution
    args = {'sticker_ids': sticker_ids,
            'sticker_resolution': sticker_resolution}
    return args


def main() -> None:
    args = get_args()
    global sticker_resolution
    global sticker_ids
    sticker_resolution = args['sticker_resolution']
    sticker_ids = args['sticker_ids']

    start = time.time()
    download()
    end = time.time()
    print(f'Downloaded {len(sticker_ids)} stickers in {end - start} seconds.')


if __name__ == '__main__':
    main()