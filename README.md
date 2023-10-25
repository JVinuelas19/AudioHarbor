# AudioHarbor
An audio downloader made with PyTube and Spotify API! The main idea is to download the audio files from YT or Spotify. Next steps will be creating a cool GUI to simplify its use

![AudioHarbor_main](https://github.com/JVinuelas19/AudioHarbor/assets/111135343/4914e3f0-a91e-49d6-a50a-c0c0b78c9da5)

# Version 1.0
A quick version of the idea: you can pick a playlist, paste the URL to the program and it will download the playlist to a selected location.

# Version 1.1
A lot of features added and bug fixes:
- Main menu 
- Download YT songs
- Show YT channel information
- Import playlists from Spotify accounts via Spotify API (Spotify parser)
- Configuration menu: you can request Spotify tokens and select the store location of the songs downloaded by the app
- Commented code

You need Spotify API credentials if you want to use the Spotify function. You can request it here: https://developer.spotify.com/documentation/web-api
There are some bugs with the pytube version 15.0.0 that requires updating a couple of pytubes .py files. I will add to the repository the fixed .py files (these fixes are not mine, they are on the pytube issues page. I'm just providing them to make your life easier).
This code has educational purposes only.

# Version 2.0
AudioHarbor now has a cool graphics user interface! In this case i wanted to develop a real application that you can download, install and use without opening CMD/VSCode. You just install the app and enjoy it. I have been struggling with a lot of concepts i wasn't used to: threading functions, languages implementation, path normalization to open files via .exe with no execution errors (this one was just horrendous), modules creation to avoid a very long unique code... It's been an adventure, i've learned a lot of things.
Let's overview the main changes compared to v1.1:
- A brand new GUI with different menus, images, sounds and user-friendly.
- 4 new languages implemented: english, spanish, deutsch and italian.
- New options to select the store path for the music and to change the language of the app.
- A new "About Me" section where you can know more about me and find my socials.
- A new language.py file to manage the language selection.
- A new audioharbor_module.py file to manage the pytube work along with the GUI.
- A new config.json to store configuration data: store path, Spotify credentials, chosen language and all languages dialogs.
- YT channel info and request Spotify tokens options has been deleted.
- Bug fixing: proper pathing implemented, language selection errors resolved, playlists titles with conflictive characters are now parsed into a non-problematic version

Like i said earlier, you need credentials to use the Spotify function. You can get yours here: https://developer.spotify.com/documentation/web-api
Please read the README.txt included with the installer before booting up AudioHarbor. 
This code has educational purposes only.


