from pytube import YouTube, Playlist, Search
import time, sys, os, requests, json

#Receives a YT url via input and downloads the audio
def download_song(store_location, url):
    try:
        yt = YouTube(url, use_oauth = False, allow_oauth_cache = True)
        start = time.time()
        stream = yt.streams.get_by_itag(140)
        output_path = os.path.join(store_location, "Youtube songs")
        stream.download(output_path = output_path)
        end = time.time()
        elapsed_time = str(round(end-start, 2))
        return elapsed_time
    except:
        raise Exception

#Receives a yt_item, gets the audio and downloads it
def download_spotify_song(yt_item, store_location):
    yt = yt_item
    stream = yt.streams.get_audio_only()
    stream.download(output_path = f'{store_location}')

#This function is an auxiliar tool to check the URLs/Spotify user input to avoid threading problems 
def check(url, user, service):
    try:
        if service==1:
            yt = YouTube(url, use_oauth = False, allow_oauth_cache = True)
        elif service==2:
            p = Playlist(url)
            print(p.title)
        else:
            token = get_spotify_token()
            show_spotify_playlist(token, user)
    except:
        raise Exception ('Input error')
    
#Show playlists
def show_spotify_playlist(token, user):
    try:
        url = f'https://api.spotify.com/v1/users/{user}/playlists'
        header = {'Authorization': f'Bearer {token}'}
        r = requests.get(url, headers = header)
        json_response = json.loads(r.text)
        r.close()
        counter = 1
        playlists = []
        for items in json_response['items']:
            playlist_name=remove_conflictive_chars(items['name'])
            playlist_id={counter : items['id']}
            playlist_tracks=items['tracks']['total']
            playlists.append([playlist_name, playlist_id, playlist_tracks])
            counter+=1
        return playlists
    except:
        print("Bad username")
        raise ValueError


def download_spotify_playlist(store_location, token, playlist_name, playlist_id, num_tracks):
    start = time.time()
    MAX_SONGS = 100
    LOOPS = float(num_tracks/MAX_SONGS)
    playlist_path = os.path.join(store_location, "Spotify", playlist_name)
    i = 0
    while (i < LOOPS):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={MAX_SONGS*i}"
        header = header = {'Authorization': f'Bearer {token}'}
        r = requests.get(url, headers = header)
        json_response = json.loads(r.text)
        for track in json_response['items']:
            song = track['track']['name']
            artist = track['track']['artists'][0]['name']
            try:
                s = Search(f'{artist} {song}')
                links = s.results
                download_spotify_song(links[0], playlist_path)
            except:
                s = Search(f'{artist} {song} lyrics')
                links = s.results
                download_spotify_song(links[0], playlist_path)
        i = i+1
    end = time.time()
    time_elapsed = str(round(end-start, 2))
    return time_elapsed

def remove_conflictive_chars(string):
    no_colons = string.replace(":", "")
    no_backslash = no_colons.replace("\\", "")
    no_forward_slash = no_backslash.replace("/","")
    no_asterisk = no_forward_slash.replace("*", "")
    no_question_marks = no_asterisk.replace("?", "")
    no_double_quotes = no_question_marks.replace('"', '')
    no_left_bracket = no_double_quotes.replace("<", "")
    no_right_bracket = no_left_bracket.replace(">", "")
    no_pipes = no_right_bracket.replace("|", "")
    cleared_string = no_pipes.replace("\0", "")
    return cleared_string

#Asks for a playlist URL and downloads all the audios of the playlist
def download_playlist(store_location, url):
    p = Playlist(url)
    start = time.time()
    for link in p.video_urls:
        yt = YouTube(link, use_oauth = False, allow_oauth_cache = True)
        stream = yt.streams.get_audio_only()
        playlist_name = remove_conflictive_chars(p.title)
        output_path = os.path.join(store_location, "Playlists", playlist_name)
        stream.download(output_path = output_path)
    end = time.time()
    time_elapsed = str(round(end-start, 2))
    return time_elapsed

#Logs into the Spotify API using access tokens 
def get_spotify_token():
    try:
        application_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        config_file_path = os.path.join(application_path, "config.json")
        with open(config_file_path, "r", encoding="utf-8") as config:
            config_file = json.load(config)
            client_id=config_file['clientId']
            client_secret=config_file['clientSecret']
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type" : "application/x-www-form-urlencoded"}
        data = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
        r = requests.post(url, headers = headers, data = data)
        json_token = json.loads(r.text)
        return json_token['access_token']
    except:
        raise Exception("Spotify token access denied.")