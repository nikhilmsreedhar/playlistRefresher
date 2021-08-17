import json
import requests
from behind import spotify_user_id, discover_weekly_id, current_playlist_id
from datetime import date
from refresh import Refresh


class save:

    def __init__(self):
        self.user_id=spotify_user_id
        self.spotify_token=""
        self.discover_weekly_id=discover_weekly_id
        self.current_playlist_id=current_playlist_id
        self.tracks = ""
        self.new_playlist_id = ""


    def searchSongs(self):
        #loop through tracks in playlists and compile them into a list
        print("finding songs in discover weekly...")
        query= "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_weekly_id)
        response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json=response.json()
        print(response)
        for i in response_json["items"]:
            self.tracks+=(i["track"]["uri"] + ",")
        self.tracks=self.tracks[:-1]
        self.addToPlaylist()
        #print(self.tracks)


    def createNewPlaylist(self):
        #creates a new playlist
        print("trying to create playlist")
        today = date.today()
        todayFormat=today.strftime("%d/%m/%Y")
        query="https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        request_body = json.dumps({
            "name": " Discover Weekly", "description": "An automated playlist updating and saving past and present discover weekly tracks. Last updated: "+todayFormat+ ".", "public": False})
        response = requests.post(query, data=request_body, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json=response.json()
        print(response_json)
        return response_json["id"]


    def addToPlaylist(self):
        #adds all songs from discover weekly to playlist
        print("adding songs...")
        if self.current_playlist_id:
            id = self.current_playlist_id
            query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(id, self.tracks)
        else:
            self.new_playlist_id = self.createNewPlaylist()
            query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)
        response = requests.post(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})


    def callRefresh(self):
        print("refreshing token")
        refreshCall = Refresh()
        self.spotify_token = refreshCall.refresh()
        self.searchSongs()


a=save()
a.callRefresh()
