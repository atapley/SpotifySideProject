import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid ="4a7c6a8ab962478687646d76531811d0" 
secret = "a8eebb34f19e4494a93cbd05b772e7cc"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


artist = sp.artist('spotify:artist:4tZwfgrHOc3mvqYlEYSvVi')
print(artist)