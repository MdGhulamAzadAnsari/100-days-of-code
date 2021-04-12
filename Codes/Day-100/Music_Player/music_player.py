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
        # Variables
        self.is_playing = False
        self.is_paused = False
        self.is_mute = False
        self.cur_playing = ''
        self.con_style = 'rep_one'
        self.to_break = False
        self.current_time = 0
        self.file = None

        self.window = Tk()
        self.window.geometry('800x520')
        self.window.resizable(0, 0)
        self.window.title('DeePlayer')
        # self.window.wm_attributes('-alpha', 0.95)
        self.window.iconbitmap('icon.ico')

        # Menu bar - all the menu_cascades and menu_commands.
        main_menu = Menu(self.window, tearoff=0)
        self.window.configure(menu=main_menu)

        file = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='Media', menu=file)

        file.add_command(label='Open', )  # command=self.open_file)
        file.add_command(label='Open Folder', )  # command=self.set_playlist)
        file.add_command(label='Open Muliple Files', )
        file.add_separator()
        file.add_command(label='Exit',  command=self.exit)

        about = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='About', menu=about)

        about.add_command(label='About Us', )  # command=self.about)

        # Album Art Part
        self.album_art_label = Label(self.window)
        self.album_art_label.place(x=85, y=20)

        # Playlist Frame
        playlist_frame = Label(self.window, text='', bg='White', height=19,
                               width=35, relief_='ridge')
        playlist_frame.place(x=543, y=0)

        self.playlist = Listbox(self.window, height=23, width=41)
        self.playlist.place(x=544, y=0)
        self.playlist.bind('<Double-Button>', self.playSongInitial)

        # Bottom Control Center
        Label(self.window, text='', height=5, relief_='groove',
              width=200).place(x=0, y=395)

        self.play_img = PhotoImage(file='icons/play.png')

        def on_enter_play(event):
            play_des.place(x=25, y=460)

        def on_leave_play(event):
            play_des.place(x=1000, y=1000)

        self.play_btn = Button(self.window, image=self.play_img, bd=0,
                               )  # command=self.play_music)
        self.play_btn.place(x=10, y=440)
        self.play_btn.bind('<Enter>', on_enter_play)
        self.play_btn.bind('<Leave>', on_leave_play)

        def on_enter_prev(event):
            prev_des.place(x=45, y=460)

        def on_leave_prev(event):
            prev_des.place(x=1000, y=1000)

        prev_img = PhotoImage(file='icons/prev.png')
        self.prev_btn = Button(self.window, image=prev_img, bd=0,
                               )  # command=lambda: self.next_prev(1))
        self.prev_btn.place(x=50, y=433)
        self.prev_btn.bind('<Enter>', on_enter_prev)
        self.prev_btn.bind('<Leave>', on_leave_prev)

        def on_enter_stop(event):
            stop_des.place(x=70, y=460)

        def on_leave_stop(event):
            stop_des.place(x=1000, y=1000)

        stop_img = PhotoImage(file='icons/stop.png')
        self.stop_btn = Button(self.window, image=stop_img,
                               bd=0, )  # command=self.stop)
        self.stop_btn.place(x=85, y=438)
        self.stop_btn.bind('<Enter>', on_enter_stop)
        self.stop_btn.bind('<Leave>', on_leave_stop)

        def on_enter_next(event):
            next_des.place(x=100, y=460)

        def on_leave_next(event):
            next_des.place(x=1000, y=1000)

        next_img = PhotoImage(file='icons/next.png')
        self.next_btn = Button(self.window, image=next_img, bd=0,
                               )  # command=lambda: self.next_prev(2))
        self.next_btn.place(x=113, y=433)
        self.next_btn.bind('<Enter>', on_enter_next)
        self.next_btn.bind('<Leave>', on_leave_next)

        self.pause_img = PhotoImage(file='icons/pause.png')

        self.speaker_img = PhotoImage(file='icons/vol.png')

        self.mute_img = PhotoImage(file='icons/mute.png')

        def on_enter_vol(event):
            vol_des.place(x=560, y=450)

        def on_leave_vol(event):
            vol_des.place(x=1000, y=1000)

        self.speaker = Button(self.window, image=self.speaker_img, bd=0,
                              )  # command=self.speaker_func)
        self.speaker.place(x=650, y=442)
        self.speaker.bind('<Enter>', on_enter_vol)
        self.speaker.bind('<Leave>', on_leave_vol)

        def on_enter_shuffle(event):
            shuffle_des.place(x=180, y=460)

        def on_leave_shuffle(event):
            shuffle_des.place(x=1000, y=1000)

        shuffle_img = PhotoImage(file='icons/shuffle.png')
        self.shuffle_btn = Button(self.window, image=shuffle_img,
                                  bd=0, )  # command=lambda: self.set_con(1))
        self.shuffle_btn.place(x=170, y=440)
        self.shuffle_btn.bind('<Enter>', on_enter_shuffle)
        self.shuffle_btn.bind('<Leave>', on_leave_shuffle)

        def on_enter_rep_all(event):
            rep_all_des.place(x=220, y=460)

        def on_leave_rep_all(event):
            rep_all_des.place(x=1000, y=1000)

        repeat_img = PhotoImage(file='icons/repeat.png')
        repeat_btn = Button(self.window, image=repeat_img,
                            bd=0, )  # command=lambda: self.set_con(2))
        repeat_btn.place(x=200, y=440)
        repeat_btn.bind('<Enter>', on_enter_rep_all)
        repeat_btn.bind('<Leave>', on_leave_rep_all)

        def on_enter_rep_one(event):
            rep_one_des.place(x=250, y=460)

        def on_leave_rep_one(event):
            rep_one_des.place(x=1000, y=1000)

        rep_one_img = PhotoImage(file='icons/rep_one.png')
        rep_one_btn = Button(self.window, image=rep_one_img,
                             bd=0, )  # command=lambda: self.set_con(3))
        rep_one_btn.place(x=230, y=437)
        rep_one_btn.bind('<Enter>', on_enter_rep_one)
        rep_one_btn.bind('<Leave>', on_leave_rep_one)

        play_des = Label(self.window, text='Play/Pause', relief='groove')
        prev_des = Label(self.window, text='Previous Track', relief='groove')
        stop_des = Label(self.window, text='Stop Music', relief='groove')
        next_des = Label(self.window, text='Next Track', relief='groove')
        shuffle_des = Label(self.window, text='Shuffle All', relief='groove')
        rep_all_des = Label(self.window, text='Repeat All', relief='groove')
        rep_one_des = Label(self.window, text='Repeat One', relief='groove')
        vol_des = Label(self.window, text='Adjust Volume', relief='groove')

        # Volume Scale - adjust volume
        self.scale = ttk.Scale(self.window, from_=0, to=100,
                               orient=HORIZONTAL, )  # command=self.set_vol)
        # implement the default value of scale when music player starts
        self.scale.set(70)
        mixer.music.set_volume(0.7)
        self.scale.place(x=680, y=440)

        # Time Durations
        self.dur_start = Label(self.window, text='--:--',
                               font=('Calibri', 10, 'bold'))
        self.dur_start.place(x=5, y=400)
        self.dur_end = Label(self.window, text='--:--',
                             font=('Calibri', 10, 'bold'))
        self.dur_end.place(x=750, y=400)

        # Progress Bar - The progress bar which indicates the running music
        self.progress_bar = ttk.Progressbar(
            self.window, orient='horizontal', length=705)
        self.progress_bar.place(x=42, y=400)

        # Status Bar - at the bottom of self.windowdow
        self.status_bar = Label(self.window, text='Welcome to Music Player',
                                relief_='sunken', anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

        self.window.protocol("WM_DELETE_self.windowDOW", self.exit)
        self.window.mainloop()

    def playSongInitial(self):
        self.stop()
        self.play_music()

    def play_music(self):
        try:
            if self.is_playing:
                if self.is_paused:
                    mixer.music.unpause()
                    self.is_paused = False
                    self.status_bar['text'] = 'Playing - ' + self.file
                    self.play_btn['image'] = self.pause_img
                else:
                    mixer.music.pause()
                    self.is_paused = True
                    self.play_btn['image'] = self.play_img
                    self.status_bar['text'] = 'Music Paused'
            else:
                self.file = self.playlist.get(ACTIVE)
                self.cur_playing = file
                mixer.music.load(file)
                mixer.music.play()
                self.status_bar['text'] = 'Playing - ' + self.file
                self.play_btn['image'] = self.pause_img
                self.is_playing = True
                self.show_details(file)
        except:
            mb.showerror('error', 'No file found to play.')

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
        # div - total_length/60, mod - total_length % 60
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.dur_end['text'] = timeformat

        self.play_thread = _thread.start_new_thread(
            self.start_count, (total_length,))

    def start_count(self, t):
        # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
        while self.urrent_time <= t and mixer.music.get_busy():
            if self.is_paused:
                continue
            elif self.to_break:
                break
            else:
                mins, secs = divmod(self.current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                self.dur_start['text'] = timeformat
                time.sleep(1)
                self.current_time += 1
                self.progress_bar['value'] = self.current_time
                self.progress_bar.update()
        if self.to_break:
            self.to_break = False
            self.current_time = 0
            return None
        else:
            try:
                self.con_func(self.con_style)
            except:
                pass

    def makeAlbumArtImage(self, image_path):
        image = Image.open(image_path)
        image = image.resize((350, 350), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)

    def con_func(self, con):
        self.current_time = 0
        if con == 'rand':
            try:
                in_ = random.randint(0, len(self.songs))
                next_play = self.songs[in_]
                self.play_next(next_play)
            except:
                self.play_music()
        elif con == 'rep_all':
            try:
                in_ = self.songs.index(cur_playing)
                next_play = self.songs[in_+1]
                self.play_next(next_play)
            except:
                self.play_music()
        else:
            self.play_next(cur_playing)

    def stop(self):
        mixer.music.stop()
        to_break = True
        self.current_time = 0
        self.cur_playing = ''
        self.is_playing = False
        self.is_paused = False
        self.dur_start['text'] = '--:--'
        self.dur_end['text'] = '--:--'
        self.progress_bar['value'] = 0.0
        self.progress_bar.update()

        self.album_art_label.configure(image=None)
        self.album_art_label.image = None

        self.play_btn['image'] = self.play_img
        self.status_bar['text'] = 'Music Stopped'
        self.to_break = False

        return None

    def exit(self):
        self.stop()
        self.window.destroy()
        os.sys.exit()
