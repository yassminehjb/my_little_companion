import customtkinter as ctk
import time
import threading
import os
import random

# =====================================================================
# here i set all the stuff like Colors and fonts lol(I loveee cute things lol)
# =====================================================================
ctk.set_appearance_mode("light")

window = ctk.CTk()
window.title("Cozy Study Space ☁️✨")
window.geometry("780x540")
window.configure(fg_color="#F9F6F0") # cream color because its pretty

# basic text styles so i dont have to retype them
title_font = ("Segoe UI", 20, "bold")
normal_font = ("Segoe UI", 13)

# =====================================================================
# VARIABLES (Tons of globals because i dont know how to use classes yet hihi)
# =====================================================================
timer_on = False
seconds_left = 25 * 60  
xp = 0
lvl = 1

# game variables
score_counter = 0
basket_position = 150
cupcake_left = 150
cupcake_top = 0
game_is_running = False

# music status
music_playing = False

# =====================================================================
# CODE FOR SCREEN SWITCHING (the msot satisfying for me !!)
# =====================================================================
def reset_all_screens():
    # hides everything so we can show the one we want
    pomo_box.pack_forget()
    todo_box.pack_forget()
    diary_box.pack_forget()
    calc_box.pack_forget()
    music_box.pack_forget()
    plant_box.pack_forget()
    game_box.pack_forget()

def go_to_pomo():
    reset_all_screens()
    pomo_box.pack(fill="both", expand=True, padx=20, pady=20)

def go_to_todo():
    reset_all_screens()
    todo_box.pack(fill="both", expand=True, padx=20, pady=20)

def go_to_diary():
    reset_all_screens()
    diary_box.pack(fill="both", expand=True, padx=20, pady=20)

def go_to_calc():
    reset_all_screens()
    calc_box.pack(fill="both", expand=True, padx=20, pady=20)

def go_to_music():
    reset_all_screens()
    music_box.pack(fill="both", expand=True, padx=20, pady=20)

def go_to_plant():
    reset_all_screens()
    plant_box.pack(fill="both", expand=True, padx=20, pady=20)

def go_to_game():
    reset_all_screens()
    game_box.pack(fill="both", expand=True, padx=20, pady=20)

# =====================================================================
#here is the pomodor timer 
# =====================================================================
def click_start():
    global timer_on
    if timer_on == False:
        timer_on = True
        # threading stops the window from crashing lol
        t = threading.Thread(target=clock_loop, daemon=True)
        t.start()

def click_pause():
    global timer_on
    timer_on = False

def click_reset():
    global timer_on, seconds_left
    timer_on = False
    seconds_left = 25 * 60
    timer_text.configure(text="25:00")
