from tkinter import *
from tkinter import filedialog as fd
from pygame import mixer


class MusicPlayer:
    def __init__(self):
        self.is_pause = True
        self.window = Tk()
        self.window.title("Music Player")
        # self.window.iconbitmap("icon.ico")
        self.window.geometry("500x300")

        # initialze Pygame Mixer
        mixer.init()

        # create playlist box
        self.playlist = Listbox(self.window, bg="black", fg="green", width=60)

        self.playlist.pack(pady=20)

        # Create player control button images
        prev_img = PhotoImage(file="icons/prev.png")
        next_img = PhotoImage(file="icons/next.png")
        play_img = PhotoImage(file="icons/play.png")
        pause_img = PhotoImage(file="icons/pause.png")
        stop_img = PhotoImage(file="icons/stop.png")

        # Create Player Control Frame
        controls_frame = Frame(self.window)
        controls_frame.pack()

        # Create Player Control buttons
        prev_btn = Button(controls_frame, image=prev_img, borderwidth=0)
        next_btn = Button(controls_frame, image=next_img, borderwidth=0)
        play_btn = Button(controls_frame, image=play_img,
                          borderwidth=0, command=self.play)
        pause_btn = Button(controls_frame, image=pause_img, borderwidth=0)
        stop_btn = Button(controls_frame, image=stop_img,
                          borderwidth=0, command=self.stop)

        prev_btn.grid(row=0, column=0, padx=10)
        next_btn.grid(row=0, column=1, padx=10)
        play_btn.grid(row=0, column=2, padx=10)
        pause_btn.grid(row=0, column=3, padx=10)
        stop_btn.grid(row=0, column=4, padx=10)

        # Create Menu

        menu = Menu(self.window)
        self.window.config(menu=menu)

        # Add Song Menu
        add_song_menu = Menu(menu)
        menu.add_cascade(label="Add Songs", menu=add_song_menu)
        add_song_menu.add_command(
            label="Add one song to playlist", command=self.add_song)

        self.window.mainloop()

    def add_song(self):
        song = fd.askopenfilename(
            initialdir='', title="Choose a song", filetypes=(("Mp3 Files", "*.mp3"),))
        self.playlist.insert(END, song)

    def play(self):
        song = self.playlist.get(ACTIVE)
        mixer.music.load(song)
        mixer.music.play(loops=0)
        self.is_pause = False

    def stop(self):
        mixer.music.stop()
        self.playlist.selection_clear()

    def pause(self):
        if self.is_pause:
            mixer.music.unpause()
            self.is_pause = False
        else:
            mixer.music.pause()
            self.is_pause = True
