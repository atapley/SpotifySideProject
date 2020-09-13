import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt

# Client ID
cid ="4a7c6a8ab962478687646d76531811d0"

# Secret ID
secret = "a8eebb34f19e4494a93cbd05b772e7cc"

# Authorization Manager
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

# Access the API with these credentials
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

result = sp.search(q='country')
print(result)
genre_list = ["rock", "pop", "hip-hop", "country"]
years_list = range(2010,2020)

for genre in genre_list:
    # create empty lists where the results are going to be stored
    artist_name = []
    track_name = []
    track_id = []

    for year in years_list:
        for i in range(0,2000,50):
            track_results = sp.search(q='year:'+str(year) + ' genre:'+genre, type='track', market='US',limit=50,offset=i)
            for i, t in enumerate(track_results['tracks']['items']):
                artist_name.append(t['artists'][0]['name'])
                track_name.append(t['name'])
                track_id.append(t['id'])

    df_tracks = pd.DataFrame({'artist_name': artist_name, 'track_name': track_name, 'track_id': track_id})

    grouped = df_tracks.groupby(['artist_name', 'track_name'], as_index=True).size()
    print('Number of Duplicates: ' + str(grouped[grouped > 1].count()))

    df_tracks.drop_duplicates(subset=['artist_name', 'track_name'], inplace=True)
    print('Removing Duplicates...')

    grouped_after_dropping = df_tracks.groupby(['artist_name', 'track_name'], as_index=True).size()
    print('Number of Duplicates: ' + str(grouped_after_dropping[grouped_after_dropping > 1].count()))

    batchsize = 100
    no_features = 0
    features = []
    for id in range(0, len(df_tracks['track_id']), batchsize):
        batch = df_tracks['track_id'][id:id + batchsize]
        feature_results = sp.audio_features(batch)
        for i, t in enumerate(feature_results):
            if t == None:
                None_counter = None_counter + 1
            else:
                features.append(t)

    print('Number of Tracks Without Features: ' + str(no_features))

    df_audio_features = pd.DataFrame.from_dict(features, orient='columns')

    columns_to_drop = ['analysis_url', 'track_href', 'type', 'uri']
    df_audio_features.drop(columns_to_drop, axis=1, inplace=True)

    df_audio_features.rename(columns={'id': 'track_id'}, inplace=True)

    df = pd.merge(df_tracks, df_audio_features, on='track_id', how='inner')

    print('Number of Rows: ' + str(len(df)))

    df.to_csv('./data/' + genre + '.csv')

    print(genre + ' completed!')


