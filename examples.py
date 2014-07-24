import genius

# Searches for songs containing the words or by Iron Maiden. We'll ask for up to 50 results (default is 25)
songs = genius.search_songs("Iron Maiden", 50)
for song in songs:
    print song.title, song.artist.name

# The first result is "Iron Maiden" by Ghostface Killah. You can access lyrics (as a list of lines) and description
# as attributes of the song object
print songs[0].lyrics
print songs[0].description

# The second result is by the band Iron Maiden. By accessing the songs attribute of the artist object attached to that
# song, we can get the rest of their songs with lyrics on the site.
print songs[1].artist.name
for song in songs[1].artist.songs:
    print song.title

# There isn't a artist search endpoint, but we can take a decent guess from song results. We'll try Judas Priest.
jp = genius.search_artists("Judas Priest")
print jp.name
for song in jp.songs:
    print song.title
