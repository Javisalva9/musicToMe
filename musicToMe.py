import time
import urllib.request
from urllib.request import Request
import urllib.parse
import webbrowser
#from urllib import urlopen as urlOpen
from bs4 import BeautifulSoup as bs
# import mutagen
# from mutagen.easyid3 import EasyID3

import sys, deezer


import os

#Down
# url = "http://www.deezer.com/playlist/1176643681"
playId = 1176643681
#awwesome
#url = "http://www.deezer.com/playlist/2114429244"

# soup = bs(urllib.request.urlopen(url), "html.parser")
client = deezer.Client()
song_list = client.get_playlist(playId).tracks


successSongs = []
failedSongs = []
failedSongsUrls = []

for index, song in enumerate(song_list):

    #print("ITEMPROP",soup.find_all(itemprop="track"))
    # title = soup.find_all("span" , itemprop="name")[index].get_text()
    title = song.title
    # title = title.encode("utf-8")
    # artist = soup.find_all(itemprop="byArtist")[index].get_text()

    artist = song.get_artist().name
    # artist = artist.encode("utf-8")
    print (index, "title", title , "artist", artist)

    #Search in Youtube the lyric video for the song and
    #gets the first result.
    textToSearch = title + artist + " lyric video"
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soupYoutube = bs(html,"html.parser")
    vid = soupYoutube.find(attrs={'class':'yt-uix-tile-link'})
    idVideo = 'https://www.youtube.com' + vid['href']

    #Adds that video to the api for youtubeinmp3. direct dowload that song with title change as our wish
    #we set a sleep to avoid overloading web
    urlDownload = 'https://www.convertmp3.io/fetch/?video=' + idVideo + '&title=' + urllib.parse.quote(artist) + urllib.parse.quote(" - ") + urllib.parse.quote(title)
    req = Request(urlDownload, headers={'User-Agent': 'Mozilla/5.0'})

    print(urlDownload)
    responseAPI = urllib.request.urlopen(req).geturl()
    #print (urlDownload)
    #print (responseAPI)
    # save fails for retry
    if "get/?" in responseAPI:
        successSongs.append(title)
        webbrowser.open_new_tab(responseAPI)
        print ("SUCCESS : " , title)
    else:
        failedSongs.append(title)
        failedSongsUrls.append(urlDownload)
        print ("FAIL : " , title)

    time.sleep(2)

print ("SUCCESSSONGS",  len(successSongs))
print ("\n" .join(successSongs))
print ("\n")
print ("FAILEDSONGS", len(failedSongs))
print ("\n" .join(failedSongs))

porcent = (100*len(successSongs))/(len(successSongs)+len(failedSongs))
print ("PORCENT " + str(porcent))


retries = 0
while ((len(failedSongsUrls) != 0) and (retries < 3)):
    print ("RETRY waiting 60seconds...")
    time.sleep(60)
    retries += 1
    for index, retrySongUrl in enumerate(failedSongsUrls):
        req = Request(retrySongUrl, headers={'User-Agent': 'Mozilla/5.0'})
        responseAPI = urllib.request.urlopen(req).geturl()
        #print (retrySongUrl)
        #print (responseAPI)
        # save fails for retry
        if "get/?" in responseAPI:
            failedSongsUrls.pop(index)
            successSongs.append(failedSongs[index])
            failedSongs.pop(index)
            webbrowser.open_new_tab(responseAPI)
            print ("SUCCESS : " , retrySongUrl)
        else:
            print ("FAIL : ", retrySongUrl)

        time.sleep(2)

print ("SUCCESSSONGS POST RETRY",  len(successSongs))
print ("\n" .join(successSongs))
print ("\n")
print ("FAILEDSONGS", len(failedSongs))
print ("\n" .join(failedSongs))

porcent = (100*len(successSongs))/(len(successSongs)+len(failedSongs))
print ("PORCENT " + str(porcent))


print ("LAST CHANCE + MANUAL :(")
if (len(failedSongsUrls) != 0):
    for index, retrySongUrl in  enumerate(failedSongsUrls):
        req = Request(retrySongUrl, headers={'User-Agent': 'Mozilla/5.0'})
        responseAPI = urllib.request.urlopen(req).geturl()
        if "get/?" in responseAPI:
            successSongs.append(failedSongs[index])
            failedSongs.pop(index)
            webbrowser.open_new_tab(responseAPI)
            print ("SUCCESS : " , retrySongUrl)
        else:
            webbrowser.open_new_tab(responseAPI)
            print ("FAIL : ", retrySongUrl)


print ("SUCCESSSONGS FINAL",  len(successSongs))
print ("\n" .join(successSongs))
print ("\n")
print ("FAILEDSONGS", len(failedSongs))
print ("\n" .join(failedSongs))

porcent = (100*len(successSongs))/(len(successSongs)+len(failedSongs))
print ("PORCENT " + str(porcent))

# downloads = os.path.expanduser('~') + "\Downloads"
# song=  downloads + "\CHVRCHES - Leave A Trace.mp3"
# os.chdir(downloads)
#
# audio = mp3("CHVRCHES - Leave A Trace.mp3")
# title = 'test'
# # create ID3 tag if not present
# audio = EasyID3(song)
# audio['title'] = "Title"
# audio['artist'] = "Artist"
# audio['album'] = "Album"
# audio['composer'] = "" # empty
# audio.save(v2_version=3)
