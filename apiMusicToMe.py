import json, requests

url = 'http://api.deezer.com/playlist/908622995'

# params = dict(
#     origin='Chicago,IL',
#     destination='Los+Angeles,CA',
#     waypoints='Joplin,MO|Oklahoma+City,OK',
#     sensor='false'
# )
#
# resp = requests.get(url=url, params=params)
resp = requests.get(url)
data = json.loads(resp.text)

print (data['tracks']['title'])
