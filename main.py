import threading as thr
from musicplayer import musicplayer
import time

stop = False


def mainthread():
    global stop

    while not stop:
        time.sleep(1)


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


def inputthread():
    global stop
    while not stop:
        inp = input("PyMP: ")
        if inp in ["next", "n"]:
            mp.next_song()
        elif inp in ["pause", "p"]:
            if mp.toggle_pause():
                print("paused")
            else:
                print("unpaused")
        elif inp.startswith("speed ") and len(inp) > len("speed "):
            mp.set_speed(float(inp[6:]))
            print("speed is set to", inp[6:])
        elif inp in ["exit", "x"]:
            stop = True
            mp.next_song()
        elif inp in ["pause at end", "pae"]:
            mp.pause_at_end_of_song()
        elif inp.startswith("search ") and len(inp) > len("search "):
            mp.search_music(inp[7:])
        elif inp in ["help", "h"]:
            show_help()
        else:
            print("No valid input...")


def musicthread():
    global stop
    mp.scan_files()
    mp.init_play_queue()
    mp.export_from_queue()
    while not stop:
        mp.play_song()


mp = musicplayer()

thr_main = thr.Thread(target=mainthread)
thr_music = thr.Thread(target=musicthread)
thr_input = thr.Thread(target=inputthread)

thr_main.start()
thr_music.start()
thr_input.start()

thr_main.join()
thr_music.join()
thr_input.join()
