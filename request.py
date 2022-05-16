#!C:/Users/user/AppData/Local/Programs/Python/Python310/python.exe
print()
import cgi
import requests
import pandas as pd
form = cgi.FieldStorage()

uid = form.getvalue("uid")
playlist_name = form.getvalue("pass")
#Declaring variables and urls
#uid = "65hpfzf0uv3jd92vza1o6df64"
#playlist_name = "Marine Drive Vibe"

CLIENT_ID = '68c40583d4f24203b2cf36bdcef93815'
CLIENT_SECRET = '37daffe5294145028854936c593e6aa1'
AUTH_URL = 'https://accounts.spotify.com/api/token'

#Auth
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

#Declaring a base url
BASE_URL = 'https://api.spotify.com/v1/'

#requesting playlist names
r = requests.get(BASE_URL + 'users/' + uid + '/playlists' ,
                 headers=headers,
                 params={'limit': 50, 'offset': 0})

#Extracting playlist names from the json output
d = r.json()
names=[]
href=[]
data_playlist = pd.DataFrame(d)
p_items = data_playlist['items']
playlist_items = dict(p_items)
for i in range(len(p_items)):
    all_items = dict(playlist_items[i])
    names.append(all_items['name'])
    href.append(all_items['href'])
tracks_url = href[names.index(playlist_name)]
#print(tracks_url)


#requesting playlist items
s = requests.get(tracks_url + '/tracks' ,
                 headers=headers,
                 params={'market': 'IN'})

#Extracting song(track) names from the json output
e = s.json()
data_tracks = pd.DataFrame(e)
t_items = data_tracks['items']
track_items = dict(t_items)
song_list = []
for i in range(len(t_items)):
    track_tracks = track_items[i]
    track_track = track_tracks['track']
#    track_albums = track_track['album']
    track_name = track_track['name']
    song_list.append(track_name)
print("<html><body><form><center><select name='songs' id='slist'>")
for i in song_list:
    print("<option value='"+i+"'>"+i+"</option>")

print("</select><input type=button value=Delete></center></form></body></html>")

