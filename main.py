import threading as thr
from musicplayer import MusicPlayer
import tkinter as tk


mp = MusicPlayer()


class Main(object):
    def __init__(self):
        self._stop = False
        self.mainloop()

    def input_thread(self):
        while not self._stop:
            inp = input("PyMP: ")
            if inp in ["next", "n"]:
                mp.next_song()
            elif inp in ["pause", "p"]:
                if mp.toggle_pause():
                    print("paused")
                else:
                    print("un-paused")
            elif inp.startswith("speed ") and len(inp) > len("speed "):
                mp.set_speed(float(inp[6:]))
                print("speed is set to", inp[6:])
            elif inp in ["exit", "x"]:
                self._stop = True
                mp.stop()
                mp.next_song()
            elif inp in ["pause at end", "pae"]:
                mp.pause_at_end_of_song()
            elif inp.startswith("search ") and len(inp) > len("search "):
                mp.search_music(inp[7:])
            elif inp in ["help", "h"]:
                show_help()
            elif inp in ["reverse", "r"]:
                if mp.toggle_reverse():
                    print("reversed")
                else:
                    print("un-reversed")
            elif inp in ["reorder"]:
                if yes_or_no(input("This will permanently change the metadata and "
                                   "name of files. Do you want to proceed? y/n: ")):
                    mp.reorder()
            else:
                print("No valid input...")
        print("input stopped")

    def music_thread(self):
        while not self._stop:
            mp.play_next_song()
        print("music stopped")

    def loader_thread(self):
        while not self._stop:
            mp.load_next()
        print("loader stopped")

    def gui_thread(self):
        gui = Gui()
        gui.mainloop()
        print("gui stopped")

    def mainloop(self):
        thr_gui = thr.Thread(target=self.gui_thread)
        thr_loader = thr.Thread(target=self.loader_thread)
        thr_music = thr.Thread(target=self.music_thread)
        thr_input = thr.Thread(target=self.input_thread)

        thr_gui.start()
        thr_loader.start()
        thr_music.start()
        thr_input.start()

        thr_gui.join()
        thr_loader.join()
        thr_music.join()
        thr_input.join()


class Gui(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        tk.Frame.__init__(self, self.root)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.button_pause = tk.Button(self)
        self.button_pause["text"] = "Pause"
        self.button_pause["command"] = mp.toggle_pause
        self.button_pause.pack(side="top")

        self.button_next = tk.Button(self)
        self.button_next["text"] = "Next"
        self.button_next["command"] = mp.next_song
        self.button_next.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=self.root.destroy)
        self.QUIT.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")


def yes_or_no(inp):
    if inp in ["y", "yes", "Y", "Yes", "YES", "j", "J", "JA", "ja", "Ja"]:
        return True
    return False


def show_help():
    print()
    print("help (or 'h')\t\t\t-Show this help page")
    print("next (or 'n')\t\t\t-Play next song")
    print("pause (or 'p')\t\t\t-Pause or play song")
    print("speed X\t\t\t\t\t-Set the speed for the next song to X. X=1 is normal speed")
    print("pause at end (or 'pae')\t-Pause at end of song")
    print("search X\t\t\t\t-search the music library for term X")
    print("exit (or 'x')\t\t\t-Close the program")
    print()


Main()
