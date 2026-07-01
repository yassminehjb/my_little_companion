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
   while seconds_left > 0 and timer_on == True:
        m, s = divmod(seconds_left, 60)
        timer_text.configure(text=f"{m:02d}:{s:02d}")
        time.sleep(1)
        seconds_left -= 1
    
    if seconds_left == 0:
        timer_text.configure(text="Time to rest! ☕")
        timer_on = False
        xp += 50  # free xp !!
        fix_plant_screen()

# =====================================================================
# here is the to do listtt 
# =====================================================================
def press_add_todo():
    thing = todo_input.get()
    if thing != "":
        todo_output.insert(ctk.END, f"🌸 {thing}\n")
        todo_input.delete(0, ctk.END)

# =====================================================================
# and hereeee the diaryyy 
# =====================================================================
def press_save_diary():
    t_val = diary_title_input.get().strip()
    c_val = diary_text_input.get("1.0", ctk.END).strip()
    if t_val == "" or c_val == "":
        return
    
    # just writing it directly to a file
    file = open("diary_pages.txt", "a", encoding="utf-8")
    file.write(f"===PAGE_START===\nTITLE:{t_val}\n{c_val}\n===PAGE_END===\n")
    file.close()
    
    diary_title_input.delete(0, ctk.END)
    diary_text_input.delete("1.0", ctk.END)
    reload_diary_list()

def reload_diary_list():
    if not os.path.exists("diary_pages.txt"):
        return
    all_titles = []
    file = open("diary_pages.txt", "r", encoding="utf-8")
    for line in file:
        if line.startswith("TITLE:"):
            clean_title = line.replace("TITLE:", "").strip()
            all_titles.append(clean_title)
    file.close()
    if all_titles:
        diary_dropdown.configure(values=all_titles)

def load_old_page(chosen_title):
    if not os.path.exists("diary_pages.txt"):
        return
    file = open("diary_pages.txt", "r", encoding="utf-8")
    everything = file.read()
    file.close()
    
    chunks = everything.split("===PAGE_START===\n")
    for chunk in chunks:
        if f"TITLE:{chosen_title}" in chunk:
            story = chunk.split(f"TITLE:{chosen_title}\n")[1].replace("\n===PAGE_END===\n", "").strip()
            diary_title_input.delete(0, ctk.END)
            diary_title_input.insert(0, chosen_title)
            diary_text_input.delete("1.0", ctk.END)
            diary_text_input.insert("1.0", story)
            break

# =====================================================================
# anddd heree is the calculator ( so easyyyy this one)
# =====================================================================
def calc_click(btn_value):
    now = calc_screen.get()
    if btn_value == "C":
        calc_screen.delete(0, ctk.END)
    elif btn_value == "=":
        try:
            answer = str(eval(now)) # eval does all the math math
            calc_screen.delete(0, ctk.END)
            calc_screen.insert(0, answer)
        except:
            calc_screen.delete(0, ctk.END)
            calc_screen.insert(0, "Error")
    else:
        calc_screen.insert(ctk.END, btn_value)

# =====================================================================
# and here theeee music player (i dont know how to play music yet so idk if it s well done)
# =====================================================================
def click_music_play():
    global music_playing
    if music_playing == False:
        music_playing = True
        music_play_btn.configure(text="⏸️ Pause")
        threading.Thread(target=music_bar_mover, daemon=True).start()
    else:
        music_playing = False
        music_play_btn.configure(text="▶️ Play Ambient Beats")

def music_bar_mover():
    g = 0.0
    while music_playing == True and g < 1.0:
        time.sleep(0.5)
        g += 0.01
        music_bar.set(g)

# ==========