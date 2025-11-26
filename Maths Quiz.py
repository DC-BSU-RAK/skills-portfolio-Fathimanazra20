# MATHS QUIZ

# Import required libraries
import tkinter as tk  # Tkinter for GUI components
from tkinter import messagebox  # Message boxes for feedback
from PIL import Image, ImageTk  # For displaying images in Tkinter
import random  # For generating random math questions
from pygame import mixer  # For playing sound effects

# SOUND SETUP
mixer.init()  # Initialize pygame mixer to enable sound playback

# Load sound effects from local folder
correct_sound = mixer.Sound("sounds/correct.wav")  # Sound for correct answers
wrong_sound = mixer.Sound("sounds/error.wav")  # Sound for wrong answers
timeup_sound = mixer.Sound("sounds/timerup.wav")  # Sound when time is up
click_sound = mixer.Sound("sounds/buttonclick.wav")  # Sound when buttons are clicked

# WINDOW SETUP
window = tk.Tk()  # Create main Tkinter window
window.title("Math Quiz")  # Set window title
window.geometry("800x600")  # Set fixed window size
window.resizable(False, False)  # Disable resizing to keep layout fixed

# LOAD BACKGROUND IMAGES
# Loading images for different screens and resize them to fit window
bg_start_photo = ImageTk.PhotoImage(Image.open("images/1.jpg").resize((800, 600)))
bg_how_photo = ImageTk.PhotoImage(Image.open("images/2.jpg").resize((800, 600)))
bg_difficulty_photo = ImageTk.PhotoImage(Image.open("images/3.jpg").resize((800, 600)))
bg_quiz_photo = ImageTk.PhotoImage(Image.open("images/4.jpg").resize((800, 600)))
gameover_bg_photo = ImageTk.PhotoImage(Image.open("images/5.jpg").resize((800, 600)))

# CANVAS SETUP
canvas = tk.Canvas(window, width=800, height=600, highlightthickness=0)  # Canvas for graphics
canvas.pack(fill="both", expand=True)  # Fill entire window
canvas.create_image(0, 0, image=bg_start_photo, anchor="nw")  # Display start screen background

# BLINKING START TEXT
press_text_id = canvas.create_text(
    400, 410,  # Position in canvas
    text="PRESS TO START",  # Display text
    font=("Pixel Emulator", 22, "bold"),  # Text font
    fill="white"  # Initial color
)

blink_state = True  # Variable to toggle blink state

def blink_text():  # Function to blink the start text
    global blink_state
    # Alternate text color between white and grey
    canvas.itemconfigure(press_text_id, fill="white" if blink_state else "#797979")
    blink_state = not blink_state  # Toggle state
    window.after(600, blink_text)  # Repeat every 600ms

blink_text()  # Start blinking effect

# HOW TO PLAY SCREEN
def show_how_to_play():  # Function to show instructions
    click_sound.play()  # Play button click sound
    canvas.delete("all")  # Clear current canvas
    canvas.create_image(0, 0, image=bg_how_photo, anchor="nw")  # Show background

    instructions = (  # Instruction text
        "1.  Choose your difficulty level.\n"
        "2.  You’ll get 10 random math questions.\n"
        "3.  Type your answer and click NEXT.\n"
        "4.  Each correct answer gives you points.\n"
        "5.  Try to finish all before you run out of lives!"
    )

    # Display instructions on canvas
    canvas.create_text(
        400, 340,
        text=instructions,
        fill="black",
        font=("Pixel Emulator", 16),
        width=580,  # Wrap text width
        justify="left",
        anchor="center"
    )

    # Button to start the game
    start_btn = tk.Button(
        window,
        text="Start Game",
        font=("Pixel Emulator", 18, "bold"),
        bg="#FFD93D",
        activebackground="#FFEA7A",
        command=lambda: (click_sound.play(), show_difficulty_screen())  # On click, play sound and show difficulty screen
    )
    canvas.create_window(400, 520, window=start_btn)  # Place button on canvas

# DIFFICULTY SELECTION SCREEN
def show_difficulty_screen():  # Function to show difficulty options
    click_sound.play()  # Play click sound
    canvas.delete("all")  # Clear canvas
    canvas.create_image(0, 0, image=bg_difficulty_photo, anchor="nw")  # Background

    # Display difficulty options as text
    canvas.create_text(210, 470, text="Easy", fill="black", font=("Pixel Emulator", 18, "bold"), tags="easy")
    canvas.create_text(380, 470, text="Moderate", fill="black", font=("Pixel Emulator", 18, "bold"), tags="moderate")
    canvas.create_text(560, 470, text="Advanced", fill="black", font=("Pixel Emulator", 18, "bold"), tags="advanced")

    # Bind mouse clicks to start quiz at chosen difficulty
    canvas.tag_bind("easy", "<Button-1>", lambda e: (click_sound.play(), start_quiz("Easy")))
    canvas.tag_bind("moderate", "<Button-1>", lambda e: (click_sound.play(), start_quiz("Moderate")))
    canvas.tag_bind("advanced", "<Button-1>", lambda e: (click_sound.play(), start_quiz("Advanced")))

# QUIZ VARIABLES
score = 0  # Player score
lives = 3  # Number of lives
question_number = 0  # Question counter
timer_id = None  # Timer callback ID
time_left = 15  # Seconds per question
correct_answer = None  # Stores correct answer
current_question_text = None  # Stores current question text for retry

# GENERATE QUESTIONS FUNCTION
def generate_question(level):  # Generate random math question
    if level == "Easy":
        a, b = random.randint(1, 10), random.randint(1, 10)
    elif level == "Moderate":
        a, b = random.randint(10, 50), random.randint(10, 50)
    else:  # Advanced
        a, b = random.randint(50, 100), random.randint(50, 100)

    operation = random.choice(["+", "-"])  # Randomly select + or -
    return f"{a} {operation} {b} = ?", eval(f"{a}{operation}{b}")  # Return question text and answer

# START QUIZ FUNCTION
def start_quiz(level):  # Reset quiz variables and show first question
    global score, lives, question_number
    score = 0
    lives = 3
    question_number = 0
    show_question(level)  # Display first question

# SHOW QUESTION FUNCTION
def show_question(level):
    global question_number, correct_answer, time_left, timer_id, current_question_text

    canvas.delete("all")  # Clear canvas
    canvas.create_image(0, 0, image=bg_quiz_photo, anchor="nw")  # Background

    # Retry logic: reuse question if retry flagged
    if (hasattr(check_answer, "retry_flag") and check_answer.retry_flag) or \
       (hasattr(check_answer, "wrong_retry") and check_answer.wrong_retry):
        q_text = current_question_text  # Reuse question
    else:
        question_number += 1  # Increment question counter
        if question_number > 10 or lives <= 0:  # End quiz if limit reached
            show_result()
            return
        q_text, correct_answer = generate_question(level)  # Generate new question
        current_question_text = q_text

    # Display score
    canvas.create_text(650, 40, text=f"Score: {score}", fill="black",
                       font=("Pixel Emulator", 18, "bold"), anchor="w")
    # Display lives as hearts
    hearts = "❤️" * lives + "🤍" * (3 - lives)
    canvas.create_text(60, 40, text=f"Lives: {hearts}", fill="red",
                       font=("Pixel Emulator", 18, "bold"), anchor="w")
    # Display question counter
    canvas.create_text(400, 190, text=f"Question {question_number}/10",
                       font=("Pixel Emulator", 20, "bold"), fill="black")
    # Display question text
    canvas.create_text(400, 260, text=q_text,
                       font=("Pixel Emulator", 28, "bold"), fill="black")
    # Display timer
    timer_text = canvas.create_text(400, 320, text=f"Time Left: 15s",
                                    font=("Pixel Emulator", 16), fill="red")

    # Answer input box
    answer_entry = tk.Entry(window, font=("Pixel Emulator", 20), width=10, justify="center",
                            bg="white", highlightthickness=2, highlightbackground="black",
                            highlightcolor="black")
    canvas.create_window(400, 380, window=answer_entry)
    answer_entry.focus_set()  # Focus cursor on input box

    # Next button
    next_btn = tk.Button(window, text="Next ➜", font=("Pixel Emulator", 14, "bold"), bg="#FFD93D",
                         command=lambda: (click_sound.play(), check_answer(level, answer_entry.get())))
    canvas.create_window(400, 450, window=next_btn)

    # Bind Enter key to check answer
    window.unbind("<Return>")
    window.bind("<Return>", lambda event: check_answer(level, answer_entry.get()))

    # Timer countdown
    time_left = 15  # Reset timer
    def countdown():
        global time_left, timer_id, lives, score
        time_left -= 1
        canvas.itemconfigure(timer_text, text=f"Time Left: {time_left}s")
        if time_left <= 0:  # Time up
            timeup_sound.play()
            lives -= 1
            score = max(0, score - 5)
            messagebox.showinfo("⏰ Time’s Up!", "You ran out of time! -5 pts.")
            show_question(level)
        else:
            timer_id = window.after(1000, countdown)  # Repeat every second
    timer_id = window.after(1000, countdown)  # Start timer

# CHECK ANSWER FUNCTION
def check_answer(level, user_answer):
    global score, lives, timer_id

    try:
        window.after_cancel(timer_id)  # Stop countdown
    except:
        pass

    # Empty answer / skip
    if user_answer.strip() == "":
        if not hasattr(check_answer, "retry_flag") or not check_answer.retry_flag:
            check_answer.retry_flag = True  # Allow one retry
            messagebox.showinfo("Try Again!", "You skipped the question.\nTry again! You have one more chance.")
            show_question(level)
            return
        else:
            check_answer.retry_flag = False
            wrong_sound.play()
            lives -= 1
            score = max(0, score - 5)
            messagebox.showinfo("❌", "You skipped again! -5 pts")
            show_question(level)
            return

    # Wrong answer
    if str(user_answer).strip() != str(correct_answer):
        if not hasattr(check_answer, "wrong_retry") or not check_answer.wrong_retry:
            check_answer.wrong_retry = True  # Allow one retry
            wrong_sound.play()
            lives -= 1
            score = max(0, score - 5)
            messagebox.showinfo("❌", "Wrong! -5 pts. Try again!")
            show_question(level)
            return
        else:
            check_answer.wrong_retry = False
            check_answer.retry_flag = False
            wrong_sound.play()
            lives -= 1
            score = max(0, score - 5)
            messagebox.showinfo("❌", "Still wrong! -5 pts")
            show_question(level)
            return

    # Correct answer
    check_answer.retry_flag = False
    check_answer.wrong_retry = False
    correct_sound.play()
    score += 10
    messagebox.showinfo("✅", "correct! +10 pts")
    show_question(level)

# SHOW RESULT SCREEN
def show_result():
    window.unbind("<Return>")  # Unbind Enter key
    canvas.delete("all")  # Clear canvas
    canvas.create_image(0, 0, image=gameover_bg_photo, anchor="nw")  # Background

    canvas.create_text(400, 370, text=f"Your Score: {score}", fill="white",
                       font=("Pixel Emulator", 20, "bold"))

    # Display message based on score
    if score >= 80:
        msg = "Outstanding! 🌟"
    elif score >= 50:
        msg = "Nice Job! 👍"
    else:
        msg = "Keep Practicing! 💪"

    canvas.create_text(400, 400, text=msg, fill="white", font=("Pixel Emulator", 20, "bold"))

    # Play Again button
    canvas.create_window(320, 460, window=tk.Button(window, text="Play Again", font=("Pixel Emulator", 18, "bold"),
                                                   bg="#FFD93D", activebackground="#FFEA7A",
                                                   command=lambda: (click_sound.play(), show_difficulty_screen())))
    # Exit button
    canvas.create_window(480, 460, window=tk.Button(window, text="Exit Game", font=("Pixel Emulator", 18, "bold"),
                                                   bg="#FF6B6B", activebackground="#FF8787",
                                                   command=lambda: (click_sound.play(), window.destroy())))

# BIND START CLICK
canvas.tag_bind(press_text_id, "<Button-1>", lambda e: (click_sound.play(), show_how_to_play()))

# START MAIN LOOP
window.mainloop()  # Start Tkinter event loop
