import httplib2

URL = 'https://vk.com/sticker/1-{}-512'

def main():
    h = httplib2.Http('.cache')
    for sticker in range(1, 2):
        response, content = h.request(URL.format(sticker))
        out = open(f'stickers/{sticker}.png', 'wb')
        out.write(content)
        out.close()

if __name__ == '__main__':
    main() 


#Emoji.stickersById