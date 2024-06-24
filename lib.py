import random
import requests
from ipytv import playlist
from typing import List

HEADERS = {
    'accept': 'audio/x-mpegurl',
}


def expand_playlist(url: str, search: str = '', only_return_pl=False) -> playlist.M3UPlaylist:
    print(f'Get {url}')
    response = requests.get(url=url, headers=HEADERS)
    assert response.status_code == 200, f'{url} get error! \n{str(response.text)[:1000]}'
    assert '#EXTM3U' in response.text, f'{url} get error! \n{str(response.text)[:1000]}'

    pl = playlist._populate(response.text.split("\n")[1:])
    if only_return_pl:
        return pl

    channels = pl.get_channels()
    if search:
        searches = search.split('|')
        channels = [ch for ch in channels for s in searches if s.lower() in ch.name.lower()]

    new_channels: List[playlist.IPTVChannel] = []
    for ch in channels:
        if 'type' in ch.attributes and ch.attributes['type'] == 'playlist':
            temp_pl = expand_playlist(ch.url, only_return_pl=True)
            for temp_ch in temp_pl.get_channels():
                temp_ch.name = f"{ch.name} / {temp_ch.name}"
            new_channels += temp_pl.get_channels()
        else:
            new_channels.append(ch)

    new_pl = playlist.M3UPlaylist()
    new_pl.append_channels(new_channels)
    return new_pl


def shaffle(pl: playlist.M3UPlaylist) -> playlist.M3UPlaylist:
    channels = pl.copy().get_channels()
    random.shuffle(channels)
    new_pl = playlist.M3UPlaylist()
    new_pl.append_channels(channels)
    return new_pl


def shaffle_by_priority(pl: playlist.M3UPlaylist) -> playlist.M3UPlaylist:
    def priority(s: str) -> int:
        s = s.lower()
        rnd = random.randint(0, 100)
        if 'spongebob' in s or 'спанч' in s or rnd > 90:
            return random.randint(90, 100)
        elif 'jerry' in s or rnd > 80:
            return random.randint(80, 100)
        elif 'южный парк' in s or 'south park' in s or rnd > 70:
            return random.randint(70, 100)
        return rnd

    channels = pl.copy().get_channels()
    new_channels = sorted(channels, key=lambda x: priority(x.name), reverse=True)

    new_pl = playlist.M3UPlaylist()
    new_pl.append_channels(new_channels)
    return new_pl


if __name__ == '__main__':
    url_main = 'http://192.168.0.160:8090/playlistall/all.m3u'

    result = expand_playlist(url_main, search='sponge|jerry')
    result_shaffle = shaffle(result)
    result_shaffle_by_priority = shaffle_by_priority(result)
