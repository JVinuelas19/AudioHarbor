import json
import os 
import sys
# Language selection function
def get_lang_package(selected):
    application_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    config_path= os.path.join(application_path, 'config.json')
    print(config_path)
    with open(config_path, 'r', encoding="utf-8") as config_file:
        config = json.load(config_file)
    language_window=[]
    path_store_window=[]
    main_menu_window=[]
    song_window=[] 
    yt_playlist_window=[]
    spotify_playlist_window=[]
    pick_window=[]
    config_window=[]
    about_me_window=[]
    dialogs=[]
    lang_package = []
    language=selected
    #Extract dictionaries as lists and saves it to lang_package
    for items in config['languages'][0][language][0]['languageWindow']:
        language_window.append(items)
    lang_package.append(language_window)
    for items in config['languages'][0][language][1]['pathStoreWindow']:
        path_store_window.append(items)
    lang_package.append(path_store_window)
    for items in config['languages'][0][language][2]['mainMenu']:
        main_menu_window.append(items)
    lang_package.append(main_menu_window)
    for items in config['languages'][0][language][3]['songWindow']:
        song_window.append(items)
    lang_package.append(song_window)
    for items in config['languages'][0][language][4]['ytPlaylistWindow']:
        yt_playlist_window.append(items)
    lang_package.append(yt_playlist_window)
    for items in config['languages'][0][language][5]['spotifyPlaylistWindow']:
        spotify_playlist_window.append(items)
    lang_package.append(spotify_playlist_window)
    for items in config['languages'][0][language][6]['pickPlaylistWindow']:
        pick_window.append(items)
    lang_package.append(pick_window)
    for items in config['languages'][0][language][7]['configWindow']:
        config_window.append(items)
    lang_package.append(config_window) 
    for items in config['languages'][0][language][8]['aboutMeWindow']:
        about_me_window.append(items)
    lang_package.append(about_me_window)
    for items in config['languages'][0][language][9]['dialogs']:
        dialogs.append(items)
    lang_package.append(dialogs)
    
    return lang_package

    #print(widgets["english"][0]['mainMenu'])
    #print(widgets["english"][1]['songWindow'])
   

# Save the updated configuration
#with open('config.json', 'w') as config_file:
#   json.dump(config, config_file, indent=4)