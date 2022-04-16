import requests
import json
import html
from hurry.filesize import size, si

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
        filesize = torrent_info['response']['torrent']['size']
        fsize = str(size(filesize))

        open(f"{torrent_name}.torrent", 'wb').write(torrent_download.content)
        print(f"\033[1;32;40m \n{torrent_name} ({fsize}) downloaded. \n")

    else:
        print(f"\033[1;31;40m \nstatus: {status}, torrent {count} does not exist \n")

