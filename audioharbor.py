from pytube import YouTube, Playlist, Channel, Search
import os, sys
import time
import requests
import json

#Things to improve:
# Some playlists include troubled characters such as '/', '\', '|' and others. Create a function that avoids all these troubled chars

#SERVICES FUNCTIONS

#Receives a YT url via input and downloads the audio
def download_song(store_location):
    url = input("Type the URL to harvest the song: ")
    yt = YouTube(url, use_oauth = False, allow_oauth_cache = True)
    start = time.time()
    stream = yt.streams.get_by_itag(140)
    print(f'Downloading song "{stream.title}" ...')
    stream.download(output_path = f'{store_location}\\Songs')
    end = time.time()
    #Displays time info
    print(f'\nYour song "{yt.title}" is ready!\n'
        f'Time elapsed to download: {str(round(end-start, 2))} seconds\n')
    
#Receives a yt_item, gets the audio and downloads it
def download_spotify_song(yt_item, store_location):
    yt = yt_item
    stream = yt.streams.get_audio_only()
    print(f'Downloading song "{stream.title}" ...')
    stream.download(output_path = f'{store_location}')

#Receives a Spotify username, calls the API, returns the playlists available for that user, creates a YT search extracting artist + song
#and downloads each track from the chosen playlist
def download_spotify_playlist(store_location, token):
    print("You can download Spotify custom playlists (e.g. your 'Liked Songs'). To make them appear you can follow this tutorial:\n" 
          "https://www.wikihow.com/Share-Liked-Songs-on-Spotify#:~:text=To%20copy%20the%20link%20to,choose%20Copy%20link%20to%20playlist.\n")
    user = input('Enter your spotify username: ')
    url = f'https://api.spotify.com/v1/users/{user}/playlists'
    header = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers = header)
    json_response = json.loads(r.text)
    r.close()
    counter = 1
    playlist_names = []
    playlist_ids = []
    playlist_tracks = []
    #Extracts the playlists available and saves names, ids and number of tracks
    print("Pick a playlist:")   
    for items in json_response['items']:
        print(f"{counter} - {items['name']}: {items['tracks']['total']}")
        playlist_names.append(items['name'])
        playlist_ids.append({counter : items['id']})
        playlist_tracks.append(items['tracks']['total'])
        counter = counter+1
    playlist_number = int(input('\n'))
    #To access the value of the dictionary picked we get the index of the dictionaries list and then the key assigned to the chosen value     
    start = time.time()
    playlist_id = playlist_ids[playlist_number-1][playlist_number]
    print(f'Selected playlist is: {playlist_id}')
    #Each call to the playlist API retrieves a max of 50 songs. We have to set the number of calls and the proper offset to download all the tracks
    #We use MAX_SONGS and LOOPS to calculate the number of calls needed
    MAX_SONGS = 100
    LOOPS = float(playlist_tracks[playlist_number-1]/MAX_SONGS)
    i = 0
    while (i < LOOPS):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={MAX_SONGS*i}"
        r = requests.get(url, headers = header)
        json_response = json.loads(r.text)
        #Now we need to extract artist + song name and call the download_spotify_song function
        for track in json_response['items']:
            song = track['track']['name']
            artist = track['track']['artists'][0]['name']
            print (f"Song is: {song}")
            print (f"Artist is: {artist}")
            try:
                s = Search(f'{artist} {song}')
                links = s.results
                download_spotify_song(links[0], f'{store_location}\\Spotify\\{playlist_names[playlist_number-1]}')
            #Sometimes there is age verification. In case we detect that we will try the same search but with lyrics in the search to avoid the main official video
            except:
                print("Official video is age-restricted. Trying again...")
                s = Search(f'{artist} {song} lyrics')
                links = s.results
                download_spotify_song(links[0], f'{store_location}\\Spotify\\{playlist_names[playlist_number-1]}')
        i = i+1
    end = time.time()
    print(f'\nYour playlist "{playlist_names[playlist_number-1]}" is ready!\n'
          f'Time elapsed: {str(round(end-start, 2))} seconds\n')

#Asks for a playlist URL and downloads all the audios of the playlist
def download_playlist(store_location):
    url = input("Type the playlist URL to start harvesting: ")
    p = Playlist(url)
    start = time.time()
    #For each video in the playlist we take the audio and store it in the desired path. A message will apear for each song
    for link in p.video_urls:
        yt = YouTube(link, use_oauth = False, allow_oauth_cache = True)
        stream = yt.streams.get_audio_only()
        print(f'Downloading song "{stream.title}" ...')
        playlist_name = str(p.title).replace("|//", "-")
        stream.download(output_path = f'{store_location}\\Playlists\\{playlist_name}')
    end = time.time()
    #Display time elapsed and path location to the playlist
    print(f'\nYour playlist "{p.title}" is ready!\n'
        f'Time elapsed to convert {p.length} songs: {str(round(end-start, 2))} seconds\n')
    
#Logs into the Spotify API using access tokens 
def get_spotify_token():
    try:
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type" : "application/x-www-form-urlencoded"}
        app_path = os.path.dirname(os.path.abspath(sys.argv[0]))        
        config_path = os.path.join(app_path, "config.json")
        with open(config_path, 'r', encoding="utf-8") as config:
            config_file = json.load(config)
            client_id = config_file['clientId']
            client_secret = config_file['clientSecret']
        data = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
        r = requests.post(url, headers = headers, data = data)
        json_token = json.loads(r.text)
        return json_token['access_token']
    except:
        print("Spotify token access is not ready, please check the creds.txt and try again")

#MENU FUNCTIONS

#Displays the configuration menu where you can set store location and spotify token 
def config_menu(store_location):
    config_option = 0
    while (config_option!=3):
        try:
            config_option = int(input('Configuration options:\n'
            '# 1 - Change AudioHarbor path to store content\n'
            '# 2 - Request another Spotify token (do this if Spotify functions are not working)\n'
            '# 3 - Return to main menu\n'))
        
            if config_option == 1:
                new_path = input('Type the new path location to store AudioHarbor: ')
                store_location = new_path
                print(f'Your new AudioHarbor path is {store_location}\n')
            elif config_option == 2:
                get_spotify_token()
            elif config_option == 3:
                print("Configuration saved.")
            else:
                print("Option not available. Please try again.\n")
        except: 
            print("Please type a number to choose an option and press enter.\n")
        return store_location

#Displays the main menu of the app
def main_menu(store_location):
    option = 0
    spotify_token = get_spotify_token()
    while(option != 6):
        option = int(input('# 1 - Download a YT playlist\n'
                    '# 2 - Download a YT song\n'
                    '# 3 - Show YT channel information\n'
                    '# 4 - Download a Spotify playlist\n'
                    '# 5 - Configuration options\n'
                    '# 6 - Exit\n'
                    ))
        if option == 1:
            try:
                download_playlist(store_location)
            except:
                print("An exception happened during the process. Please check the URL and try again.\n")
        elif option == 2:
            download_song(store_location)
        elif option == 3:
            channel_name = input("Type the channel's URL: ")
            channel = Channel(channel_name)
            print(f'{channel.channel_id}')
        elif option == 4:
            download_spotify_playlist(store_location, spotify_token)
        elif option == 5:
            store_location = config_menu(store_location)
        elif option == 6:
            print('Thank you for using AudioHarbor!\n'
                  'If you enjoy my work please consider donating me at: https://www.paypal.com/donate/?hosted_button_id=7QSS3APP4TSGE \n'
                  'Meet my other works and feedback me at: https://github.com/JVinuelas19\n'
                  'Goodbye!')
        else:
            print('Option not available. Try again please.\n')

#Main function. Shows some how to information and default settings
def main():
    dirname=os.path.dirname(__file__)
    store_location = f'{dirname}\\AudioHarbor'
    input('Welcome to AudioHarbor, your fresh audio harvest service.\n'
          'Before starting the harvest, please remember to choose the location to store the information from AudioHarbor.\n'
          f'By default the store path is "{store_location}"\n'
          'You can change it when you wish to do so. Enjoy the harvest!\n'
          'Press enter to start\n')
    main_menu(store_location)

if __name__ == "__main__":
    main()