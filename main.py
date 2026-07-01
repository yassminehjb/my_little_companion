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
# and here is the plant that growsss as you useee this app
# =====================================================================
def fix_plant_screen():
    global lvl, xp
    if xp >= 100:
        lvl += 1
        xp -= 100
    
    pic = "🌱"
    if lvl == 2: pic = "🌿"
    if lvl == 3: pic = "🪴"
    if lvl == 4: pic = "🌳"
    if lvl >= 5: pic = "🌸🌳✨"
    
    plant_emoji.configure(text=pic)
    plant_status_text.configure(text=f"Level {lvl} Matcha Tree\nXP Progress to next evolution: {xp}/100")
    plant_bar.set(xp / 100)

def click_water_plant():
    global xp
    xp += 25
    fix_plant_screen()

# =====================================================================
# i alssoooo addeddd a miniii gameee where you catch cupcakes in a basket (i loveee this one)
# =====================================================================
def press_start_game():
    global game_is_running, score_counter, cupcake_top, cupcake_left
    if game_is_running == False:
        game_is_running = True
        score_counter = 0
        cupcake_top = 0
        cupcake_left = random.randint(20, 300)
        game_score_lbl.configure(text="Score: 0 🧁")
        threading.Thread(target=main_game_loop, daemon=True).start()

def go_left():
    global basket_position
    if basket_position > 10:
        basket_position -= 25
    game_basket.place(x=basket_position, y=200)

def go_right():
    global basket_position
    if basket_position < 290:
        basket_position += 25
    game_basket.place(x=basket_position, y=200)

def main_game_loop():
    global cupcake_top, cupcake_left, score_counter, game_is_running
    while game_is_running == True:
        cupcake_top += 8
        game_cupcake.place(x=cupcake_left, y=cupcake_top)
        
        if cupcake_top >= 190:
            if abs(cupcake_left - basket_position) <= 35:
                score_counter += 1
                game_score_lbl.configure(text=f"Score: {score_counter} 🧁")
            else:
                game_is_running = False
                game_score_lbl.configure(text=f"Game Over! Final: {score_counter} 🍰")
            cupcake_top = 0
            cupcake_left = random.randint(20, 300)
            
        time.sleep(0.04)

# =====================================================================
the main interfaceeeeee
# =====================================================================
sidebar = ctk.CTkFrame(window, width=180, fg_color="#E8E3D9", corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(sidebar, text="🧸\ncozy space", font=("Segoe UI", 14, "italic"), text_color="#6D5D51")
logo.pack(pady=20)

# making side buttons look un-AI and handmade
b1 = ctk.CTkButton(sidebar, text="⏱️ Timer", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_pomo)
b1.pack(fill="x", padx=10, pady=2)
b2 = ctk.CTkButton(sidebar, text="📝 To-Do", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_todo)
b2.pack(fill="x", padx=10, pady=2)
b3 = ctk.CTkButton(sidebar, text="📖 Diary", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_diary)
b3.pack(fill="x", padx=10, pady=2)
b4 = ctk.CTkButton(sidebar, text="🧮 Calc", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_calc)
b4.pack(fill="x", padx=10, pady=2)
b5 = ctk.CTkButton(sidebar, text="🎵 Lo-Fi", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_music)
b5.pack(fill="x", padx=10, pady=2)
b6 = ctk.CTkButton(sidebar, text="🌱 Status", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_plant)
b6.pack(fill="x", padx=10, pady=2)
b7 = ctk.CTkButton(sidebar, text="🎮 Play", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_game)
b7.pack(fill="x", padx=10, pady=2)
b3 = ctk.CTkButton(sidebar, text="📖 Diary", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_diary)
b3.pack(fill="x", padx=10, pady=2)
b4 = ctk.CTkButton(sidebar, text="🧮 Calc", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_calc)
b4.pack(fill="x", padx=10, pady=2)
b5 = ctk.CTkButton(sidebar, text="🎵 Lo-Fi", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_music)
b5.pack(fill="x", padx=10, pady=2)
b6 = ctk.CTkButton(sidebar, text="🌱 Status", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_plant)
b6.pack(fill="x", padx=10, pady=2)
b7 = ctk.CTkButton(sidebar, text="🎮 Play", font=normal_font, fg_color="transparent", text_color="#5D544B", hover_color="#DFD8CD", anchor="w", height=38, command=go_to_game)
b7.pack(fill="x", padx=10, pady=2)
el(pomo_box, text="25:00", font=("Segoe UI", 55, "bold"), text_color="#89A894")
timer_text.pack(pady=10)
pomo_btns = ctk.CTkFrame(pomo_box, fg_color="transparent")
pomo_btns.pack(pady=20)
ctk.CTkButton(pomo_btns, text="Start ✨", fg_color="#89A894", width=80, command=click_start).pack(side="left", padx=5)
ctk.CTkButton(pomo_btns, text="Pause ☁️", fg_color="#D1BFA7", width=80, command=click_pause).pack(side="left", padx=5)
ctk.CTkButton(pomo_btns, text="Reset 🔄", fg_color="#E0B0B0", width=80, command=click_reset).pack(side="left", padx=5)

# =====================================================================
# SCREEN 2: TO-DO LISTTTT
# =====================================================================
todo_box = ctk.CTkFrame(main_area, fg_color="#F2EDE4", corner_radius=15)
ctk.CTkLabel(todo_box, text="🎀 My Little Goals 🎀", font=title_font, text_color="#7A6F62").pack(pady=15)
todo_input = ctk.CTkEntry(todo_box, placeholder_text="Type a cute mission...", width=250, fg_color="#FFFFFF")
todo_input.pack(pady=5)
ctk.CTkButton(todo_box, text="Add Mission 🍰", fg_color="#A799B7", command=press_add_todo).pack(pady=5)
todo_output = ctk.CTkTextbox(todo_box, width=320, height=180, fg_color="#FFFFFF")
todo_output.pack(pady=10)

# =====================================================================
# SCREEN 3: DIARY SECRETS HIHI
# =====================================================================
diary_box = ctk.CTkFrame(main_area, fg_color="#F2EDE4", corner_radius=15)
ctk.CTkLabel(diary_box, text="🔒 Soft Thoughts Diary 🔒", font=title_font, text_color="#7A6F62").pack(pady=10)
history_bar = ctk.CTkFrame(diary_box, fg_color="transparent")
history_bar.pack(fill="x", padx=30, pady=2)
ctk.CTkLabel(history_bar, text="Read Past Pages:", font=normal_font).pack(side="left", padx=5)
diary_dropdown = ctk.CTkComboBox(history_bar, values=["No entries yet"], command=load_old_page, width=160)
diary_dropdown.pack(side="left", padx=5)
diary_title_input = ctk.CTkEntry(diary_box, placeholder_text="Entry Title (e.g., July 1st) ☕", width=340, fg_color="#FFFFFF")
diary_title_input.pack(pady=5)
diary_text_input = ctk.CTkTextbox(diary_box, width=340, height=150, fg_color="#FFFFFF")
diary_text_input.pack(pady=5)
ctk.CTkButton(diary_box, text="Save Page Permanently 🌸", fg_color="#E0B0B0", command=press_save_diary).pack(pady=5)
reload_diary_list()

# =====================================================================
# SCREEN 4: CALCULATORRRRRRR
# =====================================================================
calc_box = ctk.CTkFrame(main_area, fg_color="#F2EDE4", corner_radius=15)
ctk.CTkLabel(calc_box, text="🧮 Tiny Math Box 🧮", font=title_font, text_color="#7A6F62").pack(pady=10)
calc_screen = ctk.CTkEntry(calc_box, width=240, font=("Segoe UI", 18), justify="right", fg_color="#FFFFFF")
calc_screen.pack(pady=10)
calc_grid = ctk.CTkFrame(calc_box, fg_color="transparent")
calc_grid.pack()

# row 1
ctk.CTkButton(calc_grid, text="7", width=50, height=38, fg_color="#E8E3D9", text_color="#5D544B", command=lambda:calc_click("7")).grid(row=0, column=0, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="8", width=50, height=38, fg_color="#E8E3D9", text_color="#5D544B", command=lambda:calc_click("8")).grid(row=0, column=1, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="9", width=50, height=38, fg_color="#E8E3D9", text_color="#5D544B", command=lambda:calc_click("9")).grid(row=0, column=2, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="/", width=50, height=38, fg_color="#D1BFA7", text_color="#5D544B", command=lambda:calc_click("/")).grid(row=0, column=3, padx=4, pady=4)
# row 2
ctk.CTkButton(calc_grid, text="4", width=50, height=38, fg_color="#E8E3D9", text_color="#5D544B", command=lambda:calc_click("4")).grid(row=1, column=0, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="5", width=50, height=38, fg_color="#E8E3D9", text_color="#5D544B", command=lambda:calc_click("5")).grid(row=1, column=1, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="6", width=50, height=38, fg_color="#E8E3D9", text_color="#5D544B", command=lambda:calc_click("6")).grid(row=1, column=2, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="*", width=50, height=38, fg_color="#D1BFA7", text_color="#5D544B", command=lambda:calc_click("*")).grid(row=1, column=3, padx=4, pady=4)
# row 3
ctk.CTkButton(calc_grid, text="1", width=50, height=38, fg_color="#E8E3D9", text_color="#5D544B", command=lambda:calc_click("1")).grid(row=2, column=0, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="2", width=50, height=38, fg_color="#E8E3D9", text_color="#5D544B", command=lambda:calc_click("2")).grid(row=2, column=1, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="3", width=50, height=38, fg_color="#E8E3D9", text_color="#5D544B", command=lambda:calc_click("3")).grid(row=2, column=2, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="-", width=50, height=38, fg_color="#D1BFA7", text_color="#5D544B", command=lambda:calc_click("-")).grid(row=2, column=3, padx=4, pady=4)
# row 4
ctk.CTkButton(calc_grid, text="C", width=50, height=38, fg_color="#D1BFA7", text_color="#5D544B", command=lambda:calc_click("C")).grid(row=3, column=0, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="0", width=50, height=38, fg_color="#E8E3D9", text_color="#5D544B", command=lambda:calc_click("0")).grid(row=3, column=1, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="=", width=50, height=38, fg_color="#D1BFA7", text_color="#5D544B", command=lambda:calc_click("=")).grid(row=3, column=2, padx=4, pady=4)
ctk.CTkButton(calc_grid, text="+", width=50, height=38, fg_color="#D1BFA7", text_color="#5D544B", command=lambda:calc_click("+")).grid(row=3, column=3, padx=4, pady=4)

# =====================================================================
# SCREEN 5: MUSICOOOOOOO
# =====================================================================
music_box = ctk.CTkFrame(main_area, fg_color="#F2EDE4", corner_radius=15)
ctk.CTkLabel(music_box, text="🎵 Ambient Cozy Beats 🎵", font=title_font, text_color="#7A6F62").pack(pady=20)
music_play_btn = ctk.CTkButton(music_box, text="▶️ Play Ambient Beats", fg_color="#A799B7", command=click_music_play)
music_play_btn.pack(pady=10)
music_bar = ctk.CTkProgressBar(music_box, width=250, progress_color="#89A894", fg_color="#FFFFFF")
music_bar.pack(pady=10)
music_bar.set(0)
ctk.CTkLabel(music_box, text="🎚️ Volume Control:", font=normal_font).pack(pady=5)
music_slider = ctk.CTkSlider(music_box, from_=0, to=100, progress_color="#D1BFA7")
music_slider.pack()
music_slider.set(70)

# =====================================================================
# SCREEN 6: PLANT THAT GROWS AS YOOO STUDYYY
# =====================================================================
plant_box = ctk.CTkFrame(main_area, fg_color="#F2EDE4", corner_radius=15)
ctk.CTkLabel(plant_box, text="🌱 Study Sprout Status 🌱", font=title_font, text_color="#7A6F62").pack(pady=15)
plant_emoji = ctk.CTkLabel(plant_box, text="🌱", font=("Segoe UI", 70))
plant_emoji.pack(pady=10)
plant_status_text = ctk.CTkLabel(plant_box, text="Level 1 Matcha Tree\nXP Progress to next evolution: 0/100", font=normal_font)
plant_status_text.pack(pady=5)
plant_bar = ctk.CTkProgressBar(plant_box, width=220, progress_color="#89A894")
plant_bar.pack(pady=10)
plant_bar.set(0)
ctk.CTkButton(plant_box, text="Give Water 💧 (+25 XP)", fg_color="#89A894", command=click_water_plant).pack(pady=10)

# =====================================================================
# SCREEN 7: MINIII GAMEEEEEE
# =====================================================================
game_box = ctk.CTkFrame(main_area, fg_color="#F2EDE4", corner_radius=15)
ctk.CTkLabel(game_box, text="🧁 Cupcake Basket Break 🧁", font=title_font, text_color="#7A6F62").pack(pady=5)
game_score_lbl = ctk.CTkLabel(game_box, text="Press Start to Play!", font=normal_font)
game_score_lbl.pack()

game_board = ctk.CTkFrame(game_box, width=340, height=240, fg_color="#FFFFFF", border_width=2, border_color="#D1BFA7")
game_board.pack(pady=10)

game_cupcake = ctk.CTkLabel(game_board, text="🧁", font=("Arial", 22))
game_basket = ctk.CTkLabel(game_board, text="🧺", font=("Arial", 26))
game_basket.place(x=basket_position, y=200)

game_buttons = ctk.CTkFrame(game_box, fg_color="transparent")
game_buttons.pack()
ctk.CTkButton(game_buttons, text="◀️ Left", width=70, fg_color="#D1BFA7", command=go_left).pack(side="left", padx=5)
ctk.CTkButton(game_buttons, text="🎮 Start", width=80, fg_color="#89A894", command=press_start_game).pack(side="left", padx=5)
ctk.CTkButton(game_buttons, text="Right ▶️", width=70, fg_color="#D1BFA7", command=go_right).pack(side="left", padx=5)

# run the first screen at boot
go_to_pomo()

window.mainloop()