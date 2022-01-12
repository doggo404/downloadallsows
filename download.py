import requests
import json
import re
import html


authkey = ''
cookie = 'session='
torrent_pass = ''

headers = {'cookie': cookie}
count = 1
while count < 35000:
    count = count + 1
    info_url = 'https://bemaniso.ws/ajax.php?action=torrent&id=' + str(count)
    download_url = "https://bemaniso.ws/torrents.php?action=download&id=" + str(count) + "&authkey=" + authkey + "&torrent_pass=" + torrent_pass
    torrent_status = requests.get(info_url, headers=headers)
    torrent_info = json.loads(torrent_status.content)
    status = torrent_info['status']

    if status == 'success':
        torrent_download = requests.get(download_url, headers=headers)
        torrent_name =  torrent_info['response']['group']['name']
        torrent_name = torrent_name.replace('/', '')
        torrent_name = torrent_name.replace('*', '')
        torrent_name = torrent_name.replace('+', '')
        torrent_name = torrent_name.replace(':', '')
        torrent_name = torrent_name.replace('>', '')
        torrent_name = torrent_name.replace('<', '')
        torrent_name = html.unescape(torrent_name)
        open(f"{torrent_name}.torrent", 'wb').write(torrent_download.content)
        print(f"\n{torrent_name} downloaded. \n")

    else:
        print(f"status: {status}, torrent {count} does not exist")
