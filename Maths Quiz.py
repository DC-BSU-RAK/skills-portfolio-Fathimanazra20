# MATHS QUIZ

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# -----------------------------
# SOUND SETUP
# -----------------------------
# pygame mixer is used to play small sound effects
from pygame import mixer
mixer.init()

# Load sound effects from the “sounds” folder
correct_sound = mixer.Sound("sounds/correct.wav")
wrong_sound = mixer.Sound("sounds/error.wav")
timeup_sound = mixer.Sound("sounds/timerup.wav")
click_sound = mixer.Sound("sounds/buttonclick.wav")

# -----------------------------
# WINDOW SETUP
# -----------------------------
window = tk.Tk()
window.title("Math Quiz")
window.geometry("800x600")        # Window size
window.resizable(False, False)     # Lock resizing (fixed window)

# -----------------------------
# BACKGROUND IMAGES
# -----------------------------
# Start Screen Background
bg_start_photo = ImageTk.PhotoImage(
    Image.open("images/1.jpg").resize((800, 600))
)

# How-to-Play Background
bg_how_photo = ImageTk.PhotoImage(
    Image.open("images/2.jpg").resize((800, 600))
)

# Difficulty Selection Background
bg_difficulty_photo = ImageTk.PhotoImage(
    Image.open("images/3.jpg").resize((800, 600))
)

# Quiz Screen Background
bg_quiz_photo = ImageTk.PhotoImage(
    Image.open("images/4.jpg").resize((800, 600))
)

# Game Over Background 
gameover_bg_photo = ImageTk.PhotoImage(
    Image.open("images/5.jpg").resize((800, 600))
)

# -----------------------------
# CANVAS (Main Display Area)
# -----------------------------
canvas = tk.Canvas(window, width=800, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Display start screen image
canvas.create_image(0, 0, image=bg_start_photo, anchor="nw")

# -----------------------------
# PRESS TO START (Blinking Text)
# -----------------------------
press_text_id = canvas.create_text(
    400, 410,
    text="PRESS TO START",
    font=("Pixel Emulator", 22, "bold"),
    fill="white"
)

# Blink state toggles color every 600ms
blink_state = True

def blink_text():
    """Make the PRESS TO START text blink."""
    global blink_state
    canvas.itemconfigure(
        press_text_id, 
        fill="white" if blink_state else "#797979"
    )
    blink_state = not blink_state
    window.after(600, blink_text)

blink_text()

# -----------------------------
# HOW TO PLAY SCREEN
# -----------------------------
def show_how_to_play():
    """Display instructions screen."""
    click_sound.play()
    canvas.delete("all")
    canvas.create_image(0, 0, image=bg_how_photo, anchor="nw")

    # Instructions text
    instructions = (
        "1.  Choose your difficulty level.\n"
        "2.  You’ll get 10 random math questions.\n"
        "3.  Type your answer and click NEXT.\n"
        "4.  Each correct answer gives you points.\n"
        "5.  Try to finish all before you run out of lives!"
    )

    canvas.create_text(
        400, 340,
        text=instructions,
        fill="black",
        font=("Pixel Emulator", 16),
        width=580,
        justify="left",
        anchor="center"
    )

    # Button - Go to Difficulty Selection
    start_btn = tk.Button(
        window,
        text="Start Game",
        font=("Pixel Emulator", 18, "bold"),
        bg="#FFD93D",
        activebackground="#FFEA7A",
        command=lambda: (click_sound.play(), show_difficulty_screen())
    )
    canvas.create_window(400, 520, window=start_btn)

# -----------------------------
# DIFFICULTY SELECTION SCREEN
# -----------------------------
def show_difficulty_screen():
    """Display difficulty choices (Easy, Moderate, Advanced)."""
    click_sound.play()
    canvas.delete("all")
    canvas.create_image(0, 0, image=bg_difficulty_photo, anchor="nw")

    # Difficulty labels
    canvas.create_text(210, 470, text="Easy",
                       fill="black", font=("Pixel Emulator", 18, "bold"),
                       tags="easy")

    canvas.create_text(380, 470, text="Moderate",
                       fill="black", font=("Pixel Emulator", 18, "bold"),
                       tags="moderate")

    canvas.create_text(560, 470, text="Advanced",
                       fill="black", font=("Pixel Emulator", 18, "bold"),
                       tags="advanced")

    # Bind clicks to each difficulty
    canvas.tag_bind("easy", "<Button-1>",
                    lambda e: (click_sound.play(), start_quiz("Easy")))
    canvas.tag_bind("moderate", "<Button-1>",
                    lambda e: (click_sound.play(), start_quiz("Moderate")))
    canvas.tag_bind("advanced", "<Button-1>",
                    lambda e: (click_sound.play(), start_quiz("Advanced")))

# -----------------------------
# QUIZ VARIABLES
# -----------------------------
score = 0
lives = 3
question_number = 0
timer_id = None
time_left = 15
correct_answer = None

# -----------------------------
# GENERATE A QUESTION BASED ON DIFFICULTY
# -----------------------------
def generate_question(level):
    """Return a math question and its correct answer."""
    if level == "Easy":
        a, b = random.randint(1, 10), random.randint(1, 10)
    elif level == "Moderate":
        a, b = random.randint(10, 50), random.randint(10, 50)
    else:
        a, b = random.randint(50, 100), random.randint(50, 100)

    operation = random.choice(["+", "-"])
    return f"{a} {operation} {b} = ?", eval(f"{a}{operation}{b}")

# -----------------------------
# START QUIZ
# -----------------------------
def start_quiz(level):
    """Reset stats and begin quiz."""
    global score, lives, question_number
    score = 0
    lives = 3
    question_number = 0
    show_question(level)

# -----------------------------
# SHOW QUESTION SCREEN
# -----------------------------
def show_question(level):
    """Display the current question and update game state."""
    global question_number, correct_answer, time_left, timer_id

    canvas.delete("all")
    canvas.create_image(0, 0, image=bg_quiz_photo, anchor="nw")

    # If finished or out of lives - go to results
    question_number += 1
    if question_number > 10 or lives <= 0:
        show_result()
        return

    # Generate new question
    q_text, correct_answer = generate_question(level)

    # ---- TOP UI (Score + Lives) ----
    canvas.create_text(
        650, 40,
        text=f"Score: {score}",
        fill="black",
        font=("Pixel Emulator", 18, "bold"),
        anchor="w"
    )

    # Lives display (❤️ hearts)
    hearts = "❤️" * lives + "🤍" * (3 - lives)
    canvas.create_text(
        60, 40,
        text=f"Lives: {hearts}",
        fill="red",
        font=("Pixel Emulator", 18, "bold"),
        anchor="w"
    )

    # ---- QUESTION ----
    canvas.create_text(
        400, 190,
        text=f"Question {question_number}/10",
        font=("Pixel Emulator", 20, "bold"),
        fill="black"
    )

    canvas.create_text(
        400, 260,
        text=q_text,
        font=("Pixel Emulator", 28, "bold"),
        fill="black"
    )

    # ---- TIMER ----
    timer_text = canvas.create_text(
        400, 320,
        text=f"Time Left: 15s",
        font=("Pixel Emulator", 16),
        fill="red"
    )

    # ---- ANSWER ENTRY ----
    answer_entry = tk.Entry(
        window,
        font=("Pixel Emulator", 20),
        width=10,
        justify="center",
        bg="white",
        highlightthickness=2,
        highlightbackground="black",
        highlightcolor="black"
    )
    canvas.create_window(400, 380, window=answer_entry)
    answer_entry.focus_set()

    # ---- NEXT BUTTON ----
    next_btn = tk.Button(
        window,
        text="Next ➜",
        font=("Pixel Emulator", 14, "bold"),
        bg="#FFD93D",
        command=lambda: (click_sound.play(),
                         check_answer(level, answer_entry.get()))
    )
    canvas.create_window(400, 450, window=next_btn)

    # ---- ENTER KEY SUPPORT ----
    # Remove previous bind to avoid stacking multiple handlers
    window.unbind("<Return>")
    window.bind("<Return>",
                lambda event: check_answer(level, answer_entry.get()))

    # ---- TIMER COUNTDOWN ----
    time_left = 15

    def countdown():
        """Decrease time and trigger time-up penalty."""
        global time_left, timer_id, lives, score
        time_left -= 1

        # Update countdown text
        canvas.itemconfigure(timer_text, text=f"Time Left: {time_left}s")

        if time_left <= 0:
            # Time up → penalty
            timeup_sound.play()
            lives -= 1
            score = max(0, score - 5)
            messagebox.showinfo("⏰ Time’s Up!", "You ran out of time! -5 pts.")
            show_question(level)
        else:
            # Continue countdown every second
            timer_id = window.after(1000, countdown)

    timer_id = window.after(1000, countdown)

# -----------------------------
# CHECK ANSWER
# -----------------------------
def check_answer(level, user_answer):
    """Check if answer is correct and apply score/life changes."""
    global score, lives, timer_id

    # Stop countdown timer
    try:
        window.after_cancel(timer_id)
    except:
        pass

    # Correct answer
    if str(user_answer).strip() == str(correct_answer):
        correct_sound.play()
        score += 10
        messagebox.showinfo("✅ Correct!", "Nice job! +10 pts.")

    # Wrong answer
    else:
        wrong_sound.play()
        lives -= 1
        score = max(0, score - 5)
        messagebox.showinfo("❌ Wrong!", "Oops! That’s not correct. -5 pts.")

    show_question(level)

# -----------------------------
# GAME OVER SCREEN
# -----------------------------
def show_result():
    """Display final score and play again/exit options."""
    window.unbind("<Return>")
    canvas.delete("all")

    canvas.create_image(0, 0, image=gameover_bg_photo, anchor="nw")

    # Final score
    canvas.create_text(
        400, 370,
        text=f"Your Score: {score}",
        fill="white",
        font=("Pixel Emulator", 20, "bold")
    )

    # Performance message
    if score >= 80:
        msg = "Outstanding! 🌟"
    elif score >= 50:
        msg = "Nice Job! 👍"
    else:
        msg = "Keep Practicing! 💪"

    canvas.create_text(
        400, 400,
        text=msg,
        fill="white",
        font=("Pixel Emulator", 20, "bold")
    )

    # Play Again Button
    canvas.create_window(320, 460, window=tk.Button(
        window, text="Play Again", font=("Pixel Emulator", 18, "bold"),
        bg="#FFD93D", activebackground="#FFEA7A",
        command=lambda: (click_sound.play(), show_difficulty_screen())
    ))

    # Exit Game Button
    canvas.create_window(480, 460, window=tk.Button(
        window, text="Exit Game", font=("Pixel Emulator", 18, "bold"),
        bg="#FF6B6B", activebackground="#FF8787",
        command=lambda: (click_sound.play(), window.destroy())
    ))

# -----------------------------
# START SCREEN CLICK - How To Play
# -----------------------------
canvas.tag_bind(
    press_text_id, "<Button-1>",
    lambda e: (click_sound.play(), show_how_to_play())
)

# -----------------------------
# START TK LOOP
# -----------------------------
window.mainloop()
