import json
import os 
import sys
# Language selection function
def get_lang_package(selected):
    application_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    config_path= os.path.join(application_path, 'config.json')
    with open(config_path, 'r', encoding="utf-8") as config_file:
        config = json.load(config_file)
    language=selected
    language_window, path_store_window, main_menu_window, song_window, yt_playlist_window = [],[],[],[],[]
    spotify_playlist_window, pick_window, config_window, about_me_window, dialogs= [],[],[],[],[]
    lang_package = [language_window, path_store_window, main_menu_window, song_window, yt_playlist_window, spotify_playlist_window,
               pick_window, config_window, about_me_window, dialogs]
    
    #Extract dictionaries as lists and saves it to lang_package
    for i, item in enumerate(config['languages'][0][language]):
        key = list(item)
        keys = list(item[key[0]])
        inner_keys = []
        for items in keys:
            inner_keys.append(items)
        actual_inner_key = list(inner_keys)
        for j, items in enumerate(keys):
            actual_inner_keys = list(actual_inner_key[j])
            lang_package[i].append(actual_inner_key[j][actual_inner_keys[0]])
    return lang_package