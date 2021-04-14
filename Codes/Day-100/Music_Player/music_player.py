from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
from PIL import ImageTk, Image
from pygame import mixer
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import threading
import time
import random
import _thread
import os


mixer.init()


class MusicPlayer:
    def __init__(self):
        # create main window
        self.window = Tk()
        self.window.geometry('600x400')
        self.window.minsize(width=600, height=45)
        self.window.title('Music Player')
        self.window.iconbitmap('icon.ico')

        # Create Menu bar
        self.__create_menu()

        # Album Art Part
        self.__create_art()

        # create controls button
        self.__create_controllers()

        self.window.mainloop()

    def __create_menu(self):
        """
            create menu bar and menu
        """
        main_menu = Menu(self.window, tearoff=0)
        self.window.configure(menu=main_menu)

        file = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='Media', menu=file)

        file.add_command(label='Open',  command=self.open_file)
        file.add_command(label='Open Folder', )  # command=self.set_playlist)
        file.add_command(label='Open Muliple Files', )
        file.add_separator()
        file.add_command(label='Exit',  command=self.exit)

        about = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='About', menu=about)

        about.add_command(label='About Us', )  # command=self.about)

    def __create_art(self):
        # Config row 1
        # index means row
        Grid.rowconfigure(self.window, index=0, weight=1)
        Grid.columnconfigure(self.window, index=0, weight=1)
        # Album Art Part
        self.album_art_label = Label(self.window, bg='black')
        self.album_art_label.grid(row=0, column=0, sticky="nsew")

    def __create_playlist(self):
        # Playlist Frame
        playlist_frame = Label(self, text='', bg='White', height=19,
                               width=35, relief_='ridge')
        playlist_frame.grid(row=0, column=3)

        self.playlist = Listbox(playlist_frame, height=23, width=41)
        self.playlist.place(x=0, y=0)
        # self.playlist.bind('<Double-Button>', self.playSongInitial)

    def __create_controllers(self):
        control_frame = LabelFrame(
            self.window, width=400, height=50, padx=5, pady=5)
        control_frame.grid(row=1, column=0)

        self.play_img = PhotoImage(file='icons/play.png')
        self.play_btn = Button(control_frame, image=self.play_img, bd=0,
                               )  # command=self.play_music)
        self.play_btn.grid(row=0, column=0)

    def open_file(self):
        pass

    def exit(self):
        pass
