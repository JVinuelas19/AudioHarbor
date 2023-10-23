# -*- coding: utf-8 -*-
import tkinter as tk
import sys
from tkinter import Tk, ttk, messagebox, filedialog
from PIL import Image, ImageTk
from pygame import mixer as pymixer
from random import randint
import customtkinter as ctk
import audioharbor_module as ahm
import language as lang
import webbrowser
import threading
import json
import os

#######THINGS TO DO
#CREATE THE EXECUTABLE. ANTIVIRUS STUFF? 

################################################################   AUXILIARY FUNCTIONS   #########################################################################

#Creates a Window with a name and a geometry
class Window(tk.Toplevel):
    def __init__(self, name):
        super().__init__()
        self.title(name)
        self.geometry(AUXILIAR_WINDOW_GEOMETRY)

#Plays music based on isButton value
def play_music(isButton):
    if isButton:
        note = f"note_{randint(1,3)}.mp3"
        pymixer.music.load(os.path.join(sounds_file_path, note))
    else:
        pymixer.music.load(os.path.join(sounds_file_path, "back.mp3"))
    pymixer.music.play(loops=0)

#Widget sounds when destroyed
def on_destroy(e):
    if e.widget != root:
        play_music(isButton=False)

#Paints the buttons when hovered with bg_colour and fg_colour
def on_enter(e, bg_colour, fg_colour):
    e.widget['background'] = bg_colour
    e.widget['foreground'] = fg_colour

#Paints the buttons when unhovered with bg_colour and fg_colour
def on_leave(e, bg_colour, fg_colour):
    e.widget['background'] = bg_colour
    e.widget['foreground'] = fg_colour  

#Plays music when a social button is pressed
def on_click(e):
    pymixer.music.load(os.path.join(sounds_file_path, "about_me.mp3"))
    pymixer.music.play(loops=0)

#Changes the path if one is selected during the fileDialog
def select_path():
    directory = filedialog.askdirectory(initialdir="/", title="Select file")
    if directory != "":
        config['path']=directory
        save_config(config)
        path[0]=directory

#Updates the config.json
def save_config(config):
    with open(config_file_path, 'w', encoding="utf-8") as config_file:
            json.dump(config, config_file, indent=4)

#Sets the store path. If it's empty will ask the user to choose it. Otherwise will take it from config.json
def set_store_path(config):
    if config['path'] == "":
        print(lang_package[1][0]['messageBoxTitle'])
        print(lang_package[1][1]['messageBoxText'])
        messagebox.showinfo(title=lang_package[1][0]['messageBoxTitle'], message=lang_package[1][1]['messageBoxText'])
        store_path = filedialog.askdirectory(initialdir="/")
        config['path'] = store_path
        with open(os.path.join(config_file_path), 'w', encoding="utf-8") as config_file:
            json.dump(config, config_file, indent=4)
    else:
        store_path = config['path']
    return store_path

#Shows the language selection window. Will reset to apply changes if called from the config window.
def change_language(needs_reset):
    def select_language():
        if combobox.get() == "Español":
            config['chosenLanguage'] = "spanish"
        elif combobox.get() == "English":
            config['chosenLanguage'] = "english"
        elif combobox.get() == "Deutsch":
            config['chosenLanguage'] = "german"
        elif combobox.get() == "Italian":
            config['chosenLanguage'] = "italian"
        else:
            config['chosenLanguage'] = "english"

        save_config(config)
        language = config['chosenLanguage']
        global lang_package
        lang_package = lang.get_lang_package(language)
        frame.destroy()
        if not needs_reset:
            messagebox.showinfo(title=lang_package[0][0]['messageBoxTitle'], message=lang_package[0][1]['messageBoxText'])
        else:
            messagebox.showinfo(title=lang_package[9][3]['dialog4'], message=lang_package[9][4]['dialog5'])
            root.destroy()
    frame = Tk(className='Language')
    frame.geometry(AUXILIAR_WINDOW_GEOMETRY)
    frame.resizable(False, False)
    main_frame = tk.Frame(frame)
    main_frame.configure(background="#56CBF9")
    main_frame.columnconfigure(COLUMN_CONFIG, weight=1)
    main_frame.rowconfigure([0,1], weight=1)
    main_frame.pack(fill=tk.BOTH, expand = True)
    combobox = ttk.Combobox(main_frame, state="readonly", values=['English', 'Español', 'Deutsch', 'Italian'], width=30, height=10, takefocus=0)
    combobox.current(0)
    combobox.grid(column=1,row=0)
    button = tk.Button(main_frame, cursor='hand2', background="#80bc00", width=20, height=1, activebackground="#ff0000", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text='OK', command = select_language)
    button.grid(column = 1, row = 1, padx=25)
    frame.mainloop()     

#Sets the chosen language from the json config file. If it's empty will ask the user to choose one.
def choose_language(needsReset):
    if config['chosenLanguage'] == "":
        change_language(needsReset)
    else:
        language = config['chosenLanguage']
        global lang_package
        lang_package = lang.get_lang_package(language)

#Service function: Calls the functions to download a YT song (service=1) or a YT playlist (service=2) via url and a Spotify playlist (service=3) via user
def service_button(url, service, user, window, root):
    try:
        #Url/user check
        ahm.check(url, user, service)
        cbar = ctk.CTkProgressBar(window, width=370, height=20, corner_radius=0, border_width=4, bg_color='transparent', fg_color='#000000', 
                            border_color='#000000', progress_color='#ffffff', mode="indeterminate", indeterminate_speed=1)
        #Threading function
        def download(num):
            if num==1:
                cbar.place(x=70, y=370)
                cbar.start()
                ahm.download_song(f"{path[0]}", url)
            elif num==2:
                cbar.place(x=70, y=370)
                cbar.start()
                ahm.download_playlist(f"{path[0]}", url)
            else:
                token = ahm.get_spotify_token()
                playlists = ahm.show_spotify_playlist(token, user)
                pick_playlist(playlists, token, root)

        #Thread set up
        if service==1:
            download_thread = threading.Thread(target=download, args=(1,))
            txt=lang_package[9][0]['dialog1']
        elif service==2:
            download_thread = threading.Thread(target=download, args=(2,))
            txt=lang_package[9][1]['dialog2']
        else:
            download_thread = threading.Thread(target=download, args=(3,))
        #Running the thread
        download_thread.start()
        while download_thread.is_alive():
            window.update()
        #Outcome
        if service==1 or service==2:
            root.destroy()
            messagebox.showinfo(message=f"{txt}")

    #Error management
    except:
        if service == 1:
            label = tk.Label(window, text=lang_package[3][3]['errorLabel'], background="#fe2400", font=("ACETONE", 14))
            label.place(x=87, y=290)
        elif service == 2:
            label = tk.Label(window, text=lang_package[4][3]['errorLabel'], background="#fea500", font=("ACETONE", 14))
            label.place(x=87, y=290)
        elif service == 3:
            label = tk.Label(window, text=lang_package[5][3]['errorLabel'], background="#00a86b", font=("ACETONE", 14))
            label.place(x=87, y=290)
        else:
            print("External error.")

################################################################   WINDOW FUNCTIONS   #############################################################################

#Creates the "YT song" window
def yt_song_window():
    #Window layout
    root = Window(lang_package[3][0]['windowTitle'])
    root.bind("<Destroy>", on_destroy)
    root.resizable(False, False)
    play_music(True)
    window = tk.Frame(root, bg="white")
    window.columnconfigure(COLUMN_CONFIG, weight=1)
    window.rowconfigure([0,1,2], weight=1)
    window.pack(fill=tk.BOTH, expand = True)
    #Background
    image1 = Image.open(os.path.join(images_file_path, "yt_song_bg.jpg"))
    bg_image = ImageTk.PhotoImage(image1)
    label1 = tk.Label(window, image=bg_image)
    label1.image = bg_image
    label1.place(x=-2, y=0)
    #Url label
    url_label = tk.Label(window, text=lang_package[3][1]['mainLabel'], background="#fe2400", font=("ACETONE", 26))
    url_label.grid(column=1, row=0)
    #Text box
    textbox = tk.Text(window, font=("ACETONE", 18), width=30, height=2)
    textbox.grid(column=1, row=1)
    #Download button
    button1 = tk.Button(window, cursor='hand2', background="#ffffff", width=20, height=1, activebackground="#000000", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[3][2]['button'], 
                    command = lambda:(service_button(textbox.get("1.0", "end-1c"), service=1, user=None, window=window, root=root)))
    button1.grid(column=1, row=2)
    button1.bind("<Button-1>", on_click)

#Creates the "YT playlist" window
def yt_playlist_window():
    #Window layout
    root = Window(lang_package[4][0]['windowTitle'])
    root.bind("<Destroy>", on_destroy)
    root.resizable(False, False)
    play_music(True)
    window = tk.Frame(root, bg="white")
    window.columnconfigure(COLUMN_CONFIG, weight=1)
    window.rowconfigure([0,1,2], weight=1)
    window.pack(fill=tk.BOTH, expand = True)
    #Background
    image1 = Image.open(os.path.join(images_file_path,"yt_playlist_bg.jpg"))
    bg_image = ImageTk.PhotoImage(image1)
    label1 = tk.Label(window, image=bg_image)
    label1.image = bg_image
    label1.place(x=-2, y=0)
    #Label
    url_label = tk.Label(window, background="#fea500" , text=lang_package[4][1]['mainLabel'], font=("ACETONE", 26))
    url_label.grid(column=1, row=0)
    #Text box
    textbox = tk.Text(window, font=("ACETONE", 18), width=30, height=2)
    textbox.grid(column=1, row=1)
    #Download button
    button1 = tk.Button(window, cursor='hand2', background="#ffffff", width=20, height=1, activebackground="#000000", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[4][2]['button'], 
                    command = lambda:(service_button(textbox.get("1.0", "end-1c"), service=2, user=None, window=window, root=root)))
    button1.grid(column=1, row=2)
    button1.bind("<Button-1>", on_click)

#Creates the "Spotify playlist" window
def spotify_window():
    #Window layout
    root = Window(lang_package[5][0]['windowTitle'])
    root.bind("<Destroy>", on_destroy)
    root.resizable(False, False)
    play_music(True)
    window = tk.Frame(root, bg="white")
    window.columnconfigure(COLUMN_CONFIG, weight=1)
    window.rowconfigure([0,1,2], weight=1)
    window.pack(fill=tk.BOTH, expand = True)
    #Background
    image1 = Image.open(os.path.join(images_file_path,"spotify_bg.jpg"))
    bg_image = ImageTk.PhotoImage(image1)
    label1 = tk.Label(window, image=bg_image)
    label1.image = bg_image
    label1.place(x=-2, y=0)
    #Username label
    url_label = tk.Label(window, background="#00a86b", text=lang_package[5][1]['mainLabel'], font=("ACETONE", 26))
    url_label.grid(column=1, row=0)
    #Text box
    textbox = tk.Text(window, font=("ACETONE", 18), width=30, height=2)
    textbox.grid(column=1, row=1)
    #Button
    button1 = tk.Button(window, cursor='hand2', background="#ffffff", width=20, height=1, activebackground="#000000", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[5][2]['button'], 
                    command = lambda:(service_button(None, service=3, user=textbox.get("1.0", "end-1c"), window=window, root=root)))
    button1.grid(column=1, row=2)
    button1.bind("<Button-1>", on_click)

    #Creates the "Pick a playlist" window
def pick_playlist(playlists, token, root):

    #Thread function
    def dl_playlist(playlists, combobox, token, cbar):
        selected = 0
        cbar.start()
        for playlist in playlists:
            if playlist[0] == combobox.get():
                ahm.download_spotify_playlist(f"{path[0]}", token, playlist[0], playlist[1][selected+1],playlist[2])
            selected+=1

    #Threading setup and outcome (creates the progress bar and runs the thread)
    def start_thread():
        cbar = ctk.CTkProgressBar(window, width=370, height=20, corner_radius=0, border_width=4, bg_color='transparent', fg_color='#000000', 
                            border_color='#000000', progress_color='#ffffff', mode="indeterminate", indeterminate_speed=1)
        cbar.place(x=70, y=360)
        download_thread = threading.Thread(target=dl_playlist, args=(playlists, combobox, token, cbar))
        download_thread.start()
        while download_thread.is_alive():
            window.update()
        cbar.destroy()
        frame.destroy()
        root.destroy()
        messagebox.showinfo(message=lang_package[9][1]['dialog2'])

    #Window layout
    frame = Window(lang_package[6][0]['windowTitle'])
    frame.bind("<Destroy>", on_destroy)
    frame.resizable(False, False)
    window = tk.Frame(frame, bg="white")
    window.columnconfigure(COLUMN_CONFIG, weight=1)
    window.rowconfigure([0,1,2], weight=1)
    window.pack(fill=tk.BOTH, expand = True)
    #Background
    image1 = Image.open(os.path.join(images_file_path,"spotify_bg.jpg"))
    bg_image = ImageTk.PhotoImage(image1)
    label1 = tk.Label(window, image=bg_image)
    label1.image = bg_image
    label1.place(x=-2, y=0)
    #Url label
    url_label = tk.Label(window, text=lang_package[6][1]['mainLabel'], background="#00a86b" ,font=("ACETONE", 26))
    url_label.config(padx=-10)
    url_label.grid(column=1, row=0)
    #Combobox
    names=[]
    for playlist in playlists:
        names.append(playlist[0])
    combobox = ttk.Combobox(window, state="readonly", values=names, font=("ACETONE", 18), width=20, takefocus=0)
    combobox.current(0)
    combobox.place(x=131, y=150)
    #Download Button
    button1 = tk.Button(window, cursor='hand2', background="#ffffff", width=20, height=1, activebackground="#000000", 
                        activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[6][2]['button'], command = start_thread)
    button1.grid(column=1, row=2)    
    button1.bind("<Button-1>", on_click)

#Creates the "Configuration" window
def config_window():
    root = Window(lang_package[7][0]['windowTitle'])
    root.bind("<Destroy>", on_destroy)
    root.resizable(False, False)
    play_music(True)
    window = tk.Frame(root, bg="white")
    window.columnconfigure(COLUMN_CONFIG, weight=1)
    window.rowconfigure([0,1,2,3,4,5,6], weight=1)
    window.pack(fill=tk.BOTH, expand = True)

    image1 = Image.open(os.path.join(images_file_path,"config_bg.jpg"))
    bg_image = ImageTk.PhotoImage(image1)
    label1 = tk.Label(window, image=bg_image)
    label1.image = bg_image
    label1.place(x=-2, y=0)

    url_label = tk.Label(window, text=lang_package[7][1]['mainLabel'], background="#008b8a", font=("ACETONE", 26))
    url_label.grid(column=1, row=0)
    #Button
    button1 = tk.Button(window, cursor='hand2', background="#ffffff", width=35, height=1, activebackground="#000000", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[7][2]['button1'], command=select_path)
    button1.grid(column=1, row=1)
    button1.bind("<Button-1>", on_click)
    button2 = tk.Button(window, cursor='hand2', background="#ffffff", width=35, height=1, activebackground="#000000", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[7][3]['button2'], command=lambda:change_language(needs_reset=True))
    button2.grid(column=1, row=2)
    button2.bind("<Button-1>", on_click)

#Creates the "About me" window
def about_me_window():
    #Window set up
    root = Window(lang_package[8][0]['windowTitle'])
    root.resizable(False, False)
    root.bind("<Destroy>", on_destroy)
    play_music(True)
    window = tk.Frame(root, bg="white")
    window.columnconfigure(COLUMN_CONFIG, weight=1)
    window.rowconfigure([0,1,2,3,4,5,6], weight=1)
    window.pack(fill=tk.BOTH, expand = True)
    #BG image
    image1 = Image.open(os.path.join(images_file_path, "aboutme_bg.jpg"))
    bg_image = ImageTk.PhotoImage(image1)
    label1 = tk.Label(window, image=bg_image)
    label1.image = bg_image
    label1.place(x=-2, y=0)
    #Text header
    url_label = tk.Label(window, text=lang_package[8][0]['windowTitle'], background="#01ced1", font=("ACETONE", 26))
    url_label.grid(column=1, row=0)
    info_label = tk.Label(window, text=lang_package[8][1]['mainLabel'], background="#01ced1", font=("ACETONE", 16))
    info_label.grid(column=1, row=1)
    #Social Buttons configuration
    github_button = tk.Button(window, cursor='hand2', background="#ffffff", width=25, height=1, activebackground="#8c8787", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[8][2]['button1'],
                    command=lambda:webbrowser.open("https://github.com/JVinuelas19"))
    twitter_button1 = tk.Button(window, cursor='hand2', background="#ffffff", width=25, height=1, activebackground="#0fdefd", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[8][3]['button2'],
                    command=lambda:webbrowser.open("https://twitter.com/JVinuelas19"))
    twitter_button2 = tk.Button(window, cursor='hand2', background="#ffffff", width=25, height=1, activebackground="#7fc31e", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[8][4]['button3'],
                    command=lambda:webbrowser.open("https://twitter.com/Ornithob0t"))
    instagram_button = tk.Button(window, cursor='hand2', background="#ffffff", width=25, height=1, activebackground="#eea8ea", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[8][5]['button4'], 
                    command=lambda:webbrowser.open("https://www.instagram.com/jvinuelas19/"))
    paypal_button = tk.Button(window, cursor='hand2', background="#ffffff", width=25, height=1, activebackground="#1053fa", 
                    activeforeground="#ffffff", font=("ACETONE", 18),  text=lang_package[8][6]['button5'], 
                    command=lambda:webbrowser.open("https://www.paypal.com/donate/?hosted_button_id=7QSS3APP4TSGE"))
    
    buttons = [github_button, twitter_button1, twitter_button2, instagram_button, paypal_button]
    for button in buttons:
        button.bind("<Enter>", lambda event, bg_colour=button.cget('activebackground') :on_enter(event, bg_colour, None))
        button.bind("<Button-1>", on_click)
        button.bind("<Leave>", lambda event, bg_colour='#ffffff':on_leave(event, bg_colour, None))
        button.grid(column=1, row=buttons.index(button)+2)

#Creates the "AudioHarbor" window 
def main():
    main_frame = tk.Frame(root, bg="white")
    main_frame.columnconfigure(COLUMN_CONFIG, weight=1)
    main_frame.rowconfigure([0,1,2,3,4], weight=1)
    main_frame.pack(fill=tk.BOTH, expand = True)
    root.geometry(MAIN_WINDOW_GEOMETRY)
    # Create a photoimage object of the image in the path
    image1 = Image.open(os.path.join(images_file_path, "AudioHarbor.jpg"))
    test1 = ImageTk.PhotoImage(image1)
    label1 = tk.Label(main_frame, image=test1)

    image2 = Image.open(os.path.join(images_file_path, "notes.jpg"))
    test2 = ImageTk.PhotoImage(image2)
    label2 = tk.Label(main_frame, image=test2)

    # Position images
    label1.place(x=-2, y=-2)
    label2.place(x=512, y=0)

    #Buttons

    button1 = tk.Button(main_frame, cursor='hand2', background="#ff0000", width=20, height=1, activebackground="#ff0000", 
                        activeforeground="#ffffff", font=("ACETONE", 18), text=lang_package[2][0]['button1'], command = yt_song_window)
    button2 = tk.Button(main_frame, cursor='hand2', background="#ffa300", width=20, height=1, activebackground="#ffa300", 
                        activeforeground="#ffffff", font=("ACETONE", 18), text=lang_package[2][1]['button2'], command = yt_playlist_window)
    button3 = tk.Button(main_frame, cursor='hand2', background="#00bc66", width=20, height=1, activebackground="#00bc66", 
                        activeforeground="#ffffff", font=("ACETONE", 18), text=lang_package[2][2]['button3'], command = spotify_window)
    button4 = tk.Button(main_frame, cursor='hand2', background="#009b8d", width=20, height=1, activebackground="#009b8d", 
                        activeforeground="#ffffff", font=("ACETONE", 18), text=lang_package[2][3]['button4'], command = config_window)
    button5 = tk.Button(main_frame, cursor='hand2', background="#02b3c3", width=20, height=1, activebackground="#02b3c3", 
                        activeforeground="#ffffff", font=("ACETONE", 18), text=lang_package[2][4]['button5'], command = about_me_window)

    buttons = [button1, button2, button3, button4, button5]
    for button in buttons:
        button.bind("<Enter>", lambda event, bg_colour=button.cget("background"), fg_colour="#ffffff":on_enter(event, bg_colour, fg_colour))
        button.bind("<Leave>", lambda event, bg_colour=button.cget("background"), fg_colour="#000000":on_leave(event, bg_colour, fg_colour))
        button.grid(column = 2, row = buttons.index(button), padx=25)

    pymixer.music.load(os.path.join(sounds_file_path,"ahb_opening.mp3"))
    pymixer.music.play(loops=0)
    root.mainloop()

#Global variables setup and main() start
if __name__ == "__main__":
    #Frame environment, global variables, language, store path and music settings
    os.path
    MAIN_WINDOW_GEOMETRY = '1024x512+454+184'
    AUXILIAR_WINDOW_GEOMETRY = '512x512+966+184'
    COLUMN_CONFIG = [0,1,2]
    lang_package = None
    application_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Construct the full path to the config file
    config_file_path = os.path.join(application_path, 'config.json')
    images_file_path = os.path.join(application_path, 'images')
    sounds_file_path = os.path.join(application_path, 'sounds')
 
    with open(config_file_path, 'r', encoding="utf-8") as config_file:
        config = json.load(config_file)
    choose_language(False)
    #Check if we have a chosen path via config.json. If we have it the program will start normaly, otherwise we will show a dialog asking for one and write it
    #to the config file for future use.
    path = [set_store_path(config), images_file_path, sounds_file_path]
    pymixer.init()
    root = Tk(className='AudioHarbor')
    root.resizable(False, False)
    main()

