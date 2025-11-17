# MATHS QUIZ

# Import necessary libraries
import tkinter as tk  # For GUI creation
from tkinter import messagebox  # For pop-up messages
from PIL import Image, ImageTk  # For handling images in Tkinter
import random  # For generating random numbers

# SOUND SETUP
# pygame mixer is used to play small sound effects
from pygame import mixer
mixer.init()  # Initialize the pygame mixer

# Load sound effects from the "sounds" folder
correct_sound = mixer.Sound("sounds/correct.wav")  # Sound when answer is correct
wrong_sound = mixer.Sound("sounds/error.wav")      # Sound when answer is wrong
timeup_sound = mixer.Sound("sounds/timerup.wav")   # Sound when timer runs out
click_sound = mixer.Sound("sounds/buttonclick.wav") # Sound for button clicks

# WINDOW SETUP
window = tk.Tk()  # Create the main window
window.title("Math Quiz")  # Set window title
window.geometry("800x600")  # Set window size
window.resizable(False, False)  # Disable resizing to keep fixed size

# BACKGROUND IMAGES
# Load and resize images for different screens
bg_start_photo = ImageTk.PhotoImage(
    Image.open("images/1.jpg").resize((800, 600))
)
bg_how_photo = ImageTk.PhotoImage(
    Image.open("images/2.jpg").resize((800, 600))
)
bg_difficulty_photo = ImageTk.PhotoImage(
    Image.open("images/3.jpg").resize((800, 600))
)
bg_quiz_photo = ImageTk.PhotoImage(
    Image.open("images/4.jpg").resize((800, 600))
)
gameover_bg_photo = ImageTk.PhotoImage(
    Image.open("images/5.jpg").resize((800, 600))
)

# CANVAS SETUP
canvas = tk.Canvas(window, width=800, height=600, highlightthickness=0)  # Create a canvas to place images and text
canvas.pack(fill="both", expand=True)  # Fill the whole window
canvas.create_image(0, 0, image=bg_start_photo, anchor="nw")  # Display start screen background

# PRESS TO START blinking text
press_text_id = canvas.create_text(
    400, 410,  # Position on canvas
    text="PRESS TO START",  # Text displayed
    font=("Pixel Emulator", 22, "bold"),  # Font style
    fill="white"  # Text color
)

blink_state = True  # Flag for blinking effect
def blink_text():
    """Function to make start text blink."""
    global blink_state
    canvas.itemconfigure(
        press_text_id,
        fill="white" if blink_state else "#797979"  # Alternate colors
    )
    blink_state = not blink_state  # Toggle state
    window.after(600, blink_text)  # Repeat every 600ms
blink_text()  # Start blinking

# HOW TO PLAY SCREEN
def show_how_to_play():
    click_sound.play()  # Play click sound
    canvas.delete("all")  # Clear previous canvas
    canvas.create_image(0, 0, image=bg_how_photo, anchor="nw")  # Display "how to play" background

    # Instructions text
    instructions = (
        "1.  Choose your difficulty level.\n"
        "2.  You’ll get 10 random math questions.\n"
        "3.  Type your answer and click NEXT.\n"
        "4.  Each correct answer gives you points.\n"
        "5.  Try to finish all before you run out of lives!"
    )

    # Display instructions
    canvas.create_text(
        400, 340,  # Position
        text=instructions,
        fill="black",
        font=("Pixel Emulator", 16),
        width=580,  # Wrap text width
        justify="left",
        anchor="center"
    )

    # Start game button
    start_btn = tk.Button(
        window,
        text="Start Game",
        font=("Pixel Emulator", 18, "bold"),
        bg="#FFD93D",
        activebackground="#FFEA7A",
        command=lambda: (click_sound.play(), show_difficulty_screen())  # Play sound & go to difficulty selection
    )
    canvas.create_window(400, 520, window=start_btn)  # Place button on canvas

# DIFFICULTY SELECTION SCREEN
def show_difficulty_screen():
    click_sound.play()  # Play click sound
    canvas.delete("all")  # Clear previous canvas
    canvas.create_image(0, 0, image=bg_difficulty_photo, anchor="nw")  # Display difficulty background

    # Display difficulty options
    canvas.create_text(210, 470, text="Easy", fill="black", font=("Pixel Emulator", 18, "bold"), tags="easy")
    canvas.create_text(380, 470, text="Moderate", fill="black", font=("Pixel Emulator", 18, "bold"), tags="moderate")
    canvas.create_text(560, 470, text="Advanced", fill="black", font=("Pixel Emulator", 18, "bold"), tags="advanced")

    # Bind mouse clicks to start quiz with chosen difficulty
    canvas.tag_bind("easy", "<Button-1>", lambda e: (click_sound.play(), start_quiz("Easy")))
    canvas.tag_bind("moderate", "<Button-1>", lambda e: (click_sound.play(), start_quiz("Moderate")))
    canvas.tag_bind("advanced", "<Button-1>", lambda e: (click_sound.play(), start_quiz("Advanced")))

# QUIZ VARIABLES
score = 0  # Player score
lives = 3  # Player lives
question_number = 0  # Current question number
timer_id = None  # Store timer reference
time_left = 15  # Countdown timer per question
correct_answer = None  # Store correct answer for current question
current_question_text = None  # Store current question to allow retry without regenerating

# FUNCTION TO GENERATE QUESTIONS BASED ON DIFFICULTY
def generate_question(level):
    if level == "Easy":
        a, b = random.randint(1, 10), random.randint(1, 10)  # Small numbers
    elif level == "Moderate":
        a, b = random.randint(10, 50), random.randint(10, 50)  # Medium numbers
    else:
        a, b = random.randint(50, 100), random.randint(50, 100)  # Large numbers
    operation = random.choice(["+", "-"])  # Random addition or subtraction
    return f"{a} {operation} {b} = ?", eval(f"{a}{operation}{b}")  # Return question string & answer

# FUNCTION TO START QUIZ
def start_quiz(level):
    global score, lives, question_number
    score = 0  # Reset score
    lives = 3  # Reset lives
    question_number = 0  # Reset question count
    show_question(level)  # Show first question

# FUNCTION TO DISPLAY QUESTION
def show_question(level):
    global question_number, correct_answer, time_left, timer_id, current_question_text

    canvas.delete("all")  # Clear canvas
    canvas.create_image(0, 0, image=bg_quiz_photo, anchor="nw")  # Quiz background

    # If retrying (skip or wrong), reuse previous question
    if (hasattr(check_answer, "retry_flag") and check_answer.retry_flag is True) or \
       (hasattr(check_answer, "wrong_retry") and check_answer.wrong_retry is True):
        q_text = current_question_text  # Use existing question
        # correct_answer remains the same
    else:
        question_number += 1
        if question_number > 10 or lives <= 0:  # End game if 10 questions done or lives over
            show_result()
            return
        q_text, correct_answer = generate_question(level)  # Generate new question
        current_question_text = q_text  # Store it

    # Display score
    canvas.create_text(650, 40, text=f"Score: {score}", fill="black",
                       font=("Pixel Emulator", 18, "bold"), anchor="w")

    # Display lives using hearts
    hearts = "❤️" * lives + "🤍" * (3 - lives)
    canvas.create_text(60, 40, text=f"Lives: {hearts}", fill="red",
                       font=("Pixel Emulator", 18, "bold"), anchor="w")

    # Question counter
    canvas.create_text(400, 190, text=f"Question {question_number}/10",
                       font=("Pixel Emulator", 20, "bold"), fill="black")

    # Display question text
    canvas.create_text(400, 260, text=q_text,
                       font=("Pixel Emulator", 28, "bold"), fill="black")

    # Timer text
    timer_text = canvas.create_text(400, 320, text=f"Time Left: 15s",
                                    font=("Pixel Emulator", 16), fill="red")

    # Answer entry box
    answer_entry = tk.Entry(window, font=("Pixel Emulator", 20), width=10, justify="center",
                            bg="white", highlightthickness=2, highlightbackground="black",
                            highlightcolor="black")
    canvas.create_window(400, 380, window=answer_entry)
    answer_entry.focus_set()  # Focus cursor here

    # Next button
    next_btn = tk.Button(window, text="Next ➜", font=("Pixel Emulator", 14, "bold"), bg="#FFD93D",
                         command=lambda: (click_sound.play(), check_answer(level, answer_entry.get())))
    canvas.create_window(400, 450, window=next_btn)

    # ENTER key support
    window.unbind("<Return>")
    window.bind("<Return>", lambda event: check_answer(level, answer_entry.get()))

    time_left = 15  # Reset timer

    # Countdown function
    def countdown():
        global time_left, timer_id, lives, score
        time_left -= 1
        canvas.itemconfigure(timer_text, text=f"Time Left: {time_left}s")  # Update timer text

        if time_left <= 0:  # If time runs out
            timeup_sound.play()
            lives -= 1
            score = max(0, score - 5)  # Penalty
            messagebox.showinfo("⏰ Time’s Up!", "You ran out of time! -5 pts.")
            show_question(level)  # Show same question again
        else:
            timer_id = window.after(1000, countdown)  # Repeat every 1 second

    timer_id = window.after(1000, countdown)  # Start countdown

# FUNCTION TO CHECK ANSWER 
def check_answer(level, user_answer):
    global score, lives, timer_id

    try:
        window.after_cancel(timer_id)  # Stop countdown
    except:
        pass

    # SKIP / EMPTY ANSWER LOGIC
    if user_answer.strip() == "":
        if not hasattr(check_answer, "retry_flag") or check_answer.retry_flag is False:
            # First skip - allow retry
            check_answer.retry_flag = True
            messagebox.showinfo("Try Again!", "You skipped the question.\nTry again! You have one more chance.")
            show_question(level)
            return
        else:
            # Second skip - penalty
            check_answer.retry_flag = False
            check_answer.wrong_retry = False if hasattr(check_answer, "wrong_retry") else False
            wrong_sound.play()
            lives -= 1
            score = max(0, score - 5)
            messagebox.showinfo("❌ Wrong!", "Oops! That’s not correct. -5 pts.")
            show_question(level)
            return

    # WRONG ANSWER RETRY LOGIC
    if str(user_answer).strip() != str(correct_answer):
        if not hasattr(check_answer, "wrong_retry") or check_answer.wrong_retry is False:
            # First wrong - retry
            check_answer.wrong_retry = True
            messagebox.showinfo("Try Again!", "Incorrect answer.\nTry again! You have one more chance.")
            show_question(level)
            return
        else:
            # Second wrong - penalty
            check_answer.wrong_retry = False
            check_answer.retry_flag = False
            wrong_sound.play()
            lives -= 1
            score = max(0, score - 5)
            messagebox.showinfo("❌ Wrong!", "Still incorrect! -5 pts.")
            show_question(level)
            return

    # CORRECT ANSWER
    check_answer.retry_flag = False  # Reset retry flags
    check_answer.wrong_retry = False
    correct_sound.play()
    score += 10
    messagebox.showinfo("✅ Correct!", "Nice job! +10 pts.")
    show_question(level)  # Show next question

# FUNCTION TO DISPLAY FINAL RESULT
def show_result():
    window.unbind("<Return>")  # Unbind Enter key
    canvas.delete("all")  # Clear canvas

    canvas.create_image(0, 0, image=gameover_bg_photo, anchor="nw")  # Background

    # Show score
    canvas.create_text(400, 370, text=f"Your Score: {score}", fill="white",
                       font=("Pixel Emulator", 20, "bold"))

    # Show message based on score
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
    # Exit Game button
    canvas.create_window(480, 460, window=tk.Button(window, text="Exit Game", font=("Pixel Emulator", 18, "bold"),
                                                   bg="#FF6B6B", activebackground="#FF8787",
                                                   command=lambda: (click_sound.play(), window.destroy())))

# BIND start screen click to go to HOW TO PLAY
canvas.tag_bind(press_text_id, "<Button-1>", lambda e: (click_sound.play(), show_how_to_play()))

# Start the main Tkinter loop
window.mainloop()
