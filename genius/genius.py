from __future__ import division
import requests
from collections import defaultdict
from math import ceil

BASE_URL = "http://api.genius.com"


def search_songs(search, n=25):
    pages = int(ceil(n / 25))
    songs = []
    for page in xrange(1, pages + 1):
        r = requests.get(BASE_URL + "/search", params={"q": search, "page": page})
        new_songs = [Song(x) for x in r.json()['response']['hits']]
        if len(new_songs) == 0:
            break
        songs += new_songs
    return songs


def search_artists(search):
    songs = search_songs(search)
    count = defaultdict(int)
    artist_by_name = {}
    for song in songs:
        if song.artist.name.lower() == search.lower():
            return song.artist
        else:
            artist_by_name[song.artist.name] = song.artist
            count[song.artist.name] += 1
    ranked = sorted(count, key=count.get, reverse=True)
    if count[ranked[0]] > 1:
        return artist_by_name[ranked[0]]
    else:
        return songs[0].artist


class Song:
    def __init__(self, data):
        try:
            data = data['result']
        except KeyError:
            pass
        self.artist = Artist(data['primary_artist'])
        self.title = data['title']
        self.id = data['id']
        self._lyrics = None
        self._description = None

    @property
    def lyrics(self):
        if self._lyrics is None:
            self.hydrate()
        return self._lyrics

    @property
    def description(self):
        if self._description is None:
            self.hydrate()
        return self._description

    def hydrate(self):
        r = requests.get(BASE_URL + "/songs/" + str(self.id))
        self._lyrics = self._process_child(r.json()['response']['song']['lyrics']['dom'])
        self._lyrics = [x for x in self._lyrics.split("\n") if x != ""]
        self._description = self._process_child(r.json()['response']['song']['description']['dom'])
        self._description = " ".join([x for x in self._description.split("\n") if x != ""])

    def _process_child(self, child):
        if type(child) is str or type(child) is unicode:
            if len(child) > 0 and (child[0] == "[" or child[-1] == "]"):
                return ""
            else:
                return child
        else:
            try:
                return "".join([self._process_child(c) for c in child['children']])
            except KeyError:
                return "\n"


class Artist:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.url = data['url']
        self.image_url = data['image_url']
        self._songs = None

    def _get_songs(self):
        self._songs = []
        songs_remaining = True
        page = 1
        while songs_remaining:
            r = requests.get(BASE_URL + "/artists/" + str(self.id) + "/songs", params={"page": page})
            new_songs = [Song(x) for x in r.json()['response']['songs']]
            if len(new_songs) == 0:
                songs_remaining = False
            else:
                page += 1
            self._songs += new_songs

    @property
    def songs(self):
        if self._songs is None:
            self._get_songs()
        return self._songs





