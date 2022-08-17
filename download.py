import requests
import re
import json
import html
from hurry.filesize import size, si
'''------------------------------- Input username and password below. ----------------------------'''



username = ""
password = ""



'''-----------------------------------------------------------------------------------------------'''
url = "https://bemaniso.ws/"
loginpage = str(url + "login.php")

data = {"username": username,
        "password": password}

# Get auth token from request headers
r = requests.post(loginpage, data=data)
accountinfo = str(r.request.headers)
x = re.search(".*\s(session=.*)'}", accountinfo)
token = x.group(1)

# Get authkey and torrent_pass from torrent download link
torrentpage = str(url + "torrents.php")
headers = {'cookie': token}
r = requests.get(torrentpage, headers=headers)
x = re.search(".*authkey=(.*)&amp.*torrent_pass=(.*).\sc", r.text)
authkey = x.group(1)
torrent_pass = x.group(2)

count = 1
while int(count) < 35000:
    count = int(count) + 1
    count = str(count)
    info_url = 'https://bemaniso.ws/ajax.php?action=torrent&id=' + count 
    download_url = "https://bemaniso.ws/torrents.php?action=download&id=" + count + "&authkey=" + authkey + "&torrent_pass=" + torrent_pass
    torrent_status = requests.get(info_url, headers=headers) # Get torrent name, size and checks if the torrent is valid
    torrent_info = json.loads(torrent_status.content)
    status = torrent_info['status']
    
    # Strip chars that break stuff
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
        
        # Save the '.torent' file
        open(f"{torrent_name}.torrent", 'wb').write(torrent_download.content)
        print(f"\033[1;32;40m \n{torrent_name} ({fsize}) downloaded. \n")
        
    else:
        print(f"\033[1;31;40m \nstatus: {status}, torrent {count} does not exist \n")
        
