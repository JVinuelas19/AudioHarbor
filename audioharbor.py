from pytube import YouTube
from pytube import Playlist
import os
import time

def main():
    url = input("Welcome to AudioHarbor, your fresh audio harvest service.\nType the playlist URL to start harvesting: ")
    p = Playlist(url)
    dirname=os.path.dirname(__file__)
    DEFAULT_LOCATION = f'{dirname}\\Playlists'
    playlist_folder = input("Type the path to store the playlist folder or press enter to use the default location: ") 
    start = time.time()
    #If no path is specified it will store the playlist in the code's current location
    if playlist_folder == "":
        playlist_folder = DEFAULT_LOCATION
    #For each video in the playlist we take the audio and store it in the desired path. A message will apear for each song
    for link in p.video_urls:
        yt = YouTube(link, use_oauth = True, allow_oauth_cache = True)
        stream = yt.streams.get_audio_only()
        print(f'Downloading song "{stream.title}" ...')
        playlist_name = str(p.title).replace("|//", "-")
        stream.download(output_path = f'{playlist_folder}\\{playlist_name}')
    end = time.time()
    #Display time elapsed and path location to the playlist
    print(f'Your playlist "{p.title}" is ready!\n'
        f'Time elapsed to convert {p.length} songs: {str(round(end-start, 2))} seconds')

if __name__ == "__main__":
    main()