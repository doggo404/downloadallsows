import requests
import re
import json
import html

"""
This was made as a joke, it works but you probably shouldnt use this as it is awfully innefficent.
Get authkey and torrent_pass by copying a download link.
Get cookie by going to https://bemaniso.ws/index.php , pressing 'ctrl + shift + i' and going to the network tab
reload page and click 'index.php' on the top, scroll down to request headers and copy the string after session=
"""
authkey = ''
cookie = 'session='
torrent_pass = ''

headers = {'cookie': cookie}
count = 1
while count < 28595:
    count = count + 1
    ajax_url = 'https://bemaniso.ws/ajax.php?action=torrent&id=' + str(count)
    url = "https://bemaniso.ws/torrents.php?action=download&id=" + str(count) + "&authkey=" + authkey + "&torrent_pass=" + torrent_pass
    r = requests.get(url, headers=headers)
    error = re.search('	<title>Error (.+?) :: #bemaniso tracker</title>', r.text)

    if not error:
        getname = requests.get(ajax_url, headers=headers)
        json_info = json.loads(getname.content)
        tname = json_info['response']['group']['name']
        tname = tname.replace('/', '')
        tname = html.unescape(tname)
        open(f"{tname}.torrent", 'wb').write(r.content)
        print(f'{tname} downloaded.')

    else:
        error_message = error.group(1)
        print(f'Page gave Error {error_message}, torrent does not exist.')
