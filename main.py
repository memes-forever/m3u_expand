import requests as r
import random

headers = {
    'accept': 'audio/x-mpegurl',
}


def content_to_list(content: str) -> list:
    return [c for c in content.replace('#EXTM3U', '').split('\n') if c.strip()]


def list_to_content(content_list: list) -> str:
    return "\n".join(['#EXTM3U'] + content_list + [''])


def expand_playlist(url: str) -> str:
    print(f'Get {url}')
    response = r.get(url=url, headers=headers)
    assert response.status_code == 200, f'{url} get error! \n{str(response.text)[:1000]}'
    assert '#EXTM3U' in response.text, f'{url} get error! \n{str(response.text)[:1000]}'

    content = content_to_list(response.text)

    all_playlist_index = [i for i, c in enumerate(content) if 'type="playlist"' in c]
    for i in all_playlist_index:
        url_playlist = content[i+1]
        content = content + content_to_list(expand_playlist(url_playlist))

    result_content = [
        c
        for i, c in enumerate(content)
        if c
           and i not in all_playlist_index
           and i-1 not in all_playlist_index
    ]
    return list_to_content(result_content)


def shaffle(text_m3u: str) -> str:
    content = [f"#EXTINF{c}" for c in text_m3u.replace('#EXTM3U\n', '').split('#EXTINF') if c.strip()]
    random.shuffle(content)
    return '#EXTM3U\n' + "".join(content)


if __name__ == "__main__":
    url_main = 'http://192.168.0.160:8090/playlistall/all.m3u'

    new_list = expand_playlist(url_main)
    with open('all.m3u', 'w', encoding='utf-8') as f:
        f.write(new_list)

    new_random_list = shaffle(new_list)
    with open('all_random.m3u', 'w', encoding='utf-8') as f:
        f.write(new_random_list)

    a = 2