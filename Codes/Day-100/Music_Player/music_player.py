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
import threading
import os
import icons


mixer.init()


class MusicPlayer:
    REPEAT_ONE_SONG = "repeat_one"
    REPEAT_ALL_SONG = "repeat_all"
    RANDOM_SONG = "random"

    def __init__(self):
        # Variables
        self.songs = []
        self.current_song_index = 0
        self.is_playing = False
        self.is_pause = False
        self.play_thread = None
        self.current_time = 0
        self.play_style = self.REPEAT_ALL_SONG

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

        # Create song frame
        process_frame = LabelFrame(
            self.window, bd=0, padx=5, pady=5)

        process_frame.grid(row=1, column=0, sticky=E+W+N+S)
        # Time Durations
        self.dur_start = Label(process_frame, text='--:--',
                               font=('Calibri', 10, 'bold'))
        self.dur_start.grid(row=0, column=0)

        # Progress Bar - The progress bar which indicates the running music
        Grid.rowconfigure(process_frame, index=0, weight=1)
        Grid.columnconfigure(process_frame, index=1, weight=1)

        self.progress_bar = ttk.Progressbar(
            process_frame, orient='horizontal')
        self.progress_bar.grid(row=0, column=1, padx=10, sticky=E+W+N+S)

        self.dur_end = Label(process_frame, text='--:--',
                             font=('Calibri', 10, 'bold'))
        self.dur_end.grid(row=0, column=2)

        # create icon image
        self.play_img = self.__get_image(icons.PLAY)
        self.pause_img = self.__get_image(icons.PAUSE)
        self.mute_img = self.__get_image(icons.MUTE)
        self.speaker_img = self.__get_image(icons.SPEAKER)
        prev_img = self.__get_image(icons.PREV)
        stop_img = self.__get_image(icons.STOP)
        next_img = self.__get_image(icons.NEXT)
        shuffle_img = self.__get_image(icons.SHUFFLE)
        repeat_img = self.__get_image(icons.REPEAT)
        rep_one_img = self.__get_image(icons.REPEAT_ONE)

        # Create control frame
        control_frame = LabelFrame(
            self.window, bd=0, padx=5, pady=5)

        control_frame.grid(row=2, column=0, sticky=E+W+N+S)

        # Create Buttons
        # Left side control button
        self.play_btn = self.__create_button(
            control_frame, image=self.play_img, padx=(10, 20))
        self.play_btn.bind('<Button-1>', self.play)

        prev_btn = self.__create_button(control_frame, image=prev_img)
        stop_btn = self.__create_button(control_frame, image=stop_img)
        next_btn = self.__create_button(control_frame, image=next_img)
        stop_btn.bind('<Button-1>', self.stop)
        # Right side control button
        self.scale = ttk.Scale(control_frame, from_=0, to=100,
                               orient=HORIZONTAL)
        self.scale.set(70)
        mixer.music.set_volume(0.7)
        self.scale.pack(side=RIGHT, fill=X, padx=10)

        self.speaker = self.__create_button(
            control_frame, image=self.speaker_img, side=RIGHT)

        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        self.window.mainloop()

    def __create_button(self, root, image, side=LEFT, fill=X, padx=0):
        btn = Button(root, image=image, bd=0)
        btn.pack(side=side, fill=fill, padx=padx)
        return btn

    def __create_menu(self):
        # create menu bar and menu
        main_menu = Menu(self.window, tearoff=0)
        self.window.configure(menu=main_menu)

        file_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='Media', menu=file_menu)

        file_menu.add_command(label='Open',  command=self.open_file)
        # command=self.set_playlist)
        file_menu.add_command(label='Open Folder', )
        file_menu.add_command(label='Open Muliple Files', )
        file_menu.add_separator()
        file_menu.add_command(label='Exit',  command=self.exit)

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

    def __get_image(self, img_name):
        return PhotoImage(file=os.path.join("icons", img_name))

    def open_file(self):
        selected_file = filedialog.askopenfilename(
            initialdir='', title='Select File')
        filename = os.path.basename(selected_file)
        self.songs.append(selected_file)
        # self.playlist.insert(END, filename)
        self.is_playing = False
        # Play the song
        self.play()

    def play(self, *args):
        if len(self.songs) <= 0:
            return

        try:
            if self.is_playing:
                self.puase()
            else:
                self.current_song_index = len(self.songs) - 1
                song = self.songs[self.current_song_index]
                mixer.music.load(song)
                mixer.music.play()
                self.play_btn['image'] = self.pause_img
                self.is_playing = True
                self.show_details(song)

        except Exception as e:
            mb.showerror('error', f'No file found to play.\n{e}')

    def puase(self):
        if self.is_pause:
            mixer.music.unpause()
            total_length = self.progress_bar['maximum']
            self.play_thread = threading.Thread(
                target=self.song_timer, args=(total_length,))
            self.play_thread.start()
            self.is_pause = False
            self.play_btn['image'] = self.pause_img
        else:
            mixer.music.pause()
            self.is_pause = True
            self.play_btn['image'] = self.play_img

    def show_details(self, play_song):
        file_data = os.path.splitext(play_song)

        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length

            with open('temp.jpg', 'wb') as img:
                a = ID3(play_song)
                img.write(a.getall('APIC')[0].data)
                image = self.makeAlbumArtImage('temp.jpg')
                self.album_art_label.configure(image=image)
                self.album_art_label.image = image

        else:
            a = mixer.Sound(play_song)
            total_length = a.get_length()

        self.progress_bar['maximum'] = total_length
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        self.dur_end['text'] = f'{mins:02d}:{secs:02d}'
        self.play_thread = threading.Thread(
            target=self.song_timer, args=(total_length,))
        self.play_thread.start()

    def song_timer(self, t):
        # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
        # Continue - Ignores all of the statements below it. We check if music is paused or not.
        while self.current_time <= t and mixer.music.get_busy():
            mins, secs = divmod(self.current_time, 60)
            mins = round(mins)
            secs = round(secs)
            self.dur_start['text'] = f'{mins:02d}:{secs:02d}'
            time.sleep(1)
            self.current_time += 1
            self.progress_bar['value'] = self.current_time
            self.progress_bar.update()

        self.is_playing = False
        if self.is_pause:
            return
        elif len(self.songs) == 1 and not self.play_style == self.REPEAT_ONE_SONG:
            self.stop()
        else:
            try:
                self.next_song(self.play_style)
            except:
                pass

    def next_song(self, play_style):
        self.current_time = 0
        try:
            if play_style == self.RANDOM_SONG:
                random_index = -1
                while self.current_song_index == random_index or random_index != -1:
                    random_index = random.randint(0, len(self.songs))
                self.current_song_index = random_index
            elif play_style == self.REPEAT_ALL_SONG:
                self.current_song_index += 1

            self.play_next(self.songs[self.current_song_index])
        except:
            self.play()

    def play_next(self, song):
        mixer.music.load(song)
        mixer.music.play()
        self.play_btn['image'] = self.pause_img
        self.is_playing = True
        self.show_details(song)

    def stop(self, *args):
        mixer.music.stop()
        self.current_time = 0
        self.is_pause = True
        self.is_playing = False
        self.current_song_index = -1
        self.dur_start['text'] = '--:--'
        self.dur_end['text'] = '--:--'
        self.progress_bar['value'] = 0.0
        self.progress_bar.update()
        self.album_art_label.configure(image=None)
        self.album_art_label.image = None
        self.play_btn['image'] = self.play_img

    def makeAlbumArtImage(self, image_path):
        image = Image.open(image_path)
        image = image.resize((350, 350), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)

    def exit(self):
        self.stop()
        self.window.destroy()
        os.sys.exit()
