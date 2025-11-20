import tkinter as tk                    # Import Tkinter for GUI components
from tkinter import messagebox          # Import messagebox for pop-up messages
from PIL import Image, ImageTk          # Import PIL for handling images
import random                           # Import random for selecting random jokes

# Load jokes from file
def load_jokes():
    """
    Read jokes from 'randomJokes.txt', split each into (setup, punchline)
    Only considers lines that contain a question mark '?'.
    """
    with open("alexa tell me a joke/randomJokes.txt", "r", encoding="utf-8") as f:  # Open file in read mode
        jokes = f.read().splitlines()                          # Read all lines and remove newline chars

    processed = []                                            # Initialize empty list for jokes
    for j in jokes:                                           # Loop through each line in file
        if "?" in j:                                         # Only consider lines with '?'
            setup, punch = j.split("?", 1)                  # Split at the first '?' into setup and punchline
            processed.append((setup + "?", punch))          # Add tuple (setup, punchline) to processed list
    return processed                                         # Return the list of jokes

# Global variables
jokes_list = load_jokes()            # Store all jokes loaded from the file
current_joke = None                   # Variable to store the current joke
punchline_shown = False               # Flag to track whether punchline has been revealed

# Tkinter window setup
window = tk.Tk()                      # Create main application window
window.title("Alexa Joke App")        # Set window title
window.geometry("800x600")            # Set fixed size for window
window.resizable(False, False)        # Disable window resizing

# Create canvas to place background images
canvas = tk.Canvas(window, width=800, height=600, highlightthickness=0)
canvas.pack()                         # Pack canvas to fill the window

# Load background images
main_bg = ImageTk.PhotoImage(Image.open("images/joke1.png").resize((800, 600)))  # Main screen background
joke_bg = ImageTk.PhotoImage(Image.open("images/joke2.jpg").resize((800, 600)))  # Joke screen background

# Show main screen
def show_main():
    """
    Display the main screen with Start Joke button.
    """
    canvas.delete("all")                                          # Clear the canvas
    canvas.create_image(0, 0, image=main_bg, anchor="nw")        # Display main background

    # Start Joke button
    start_button = tk.Button(
        window,                                                   # Parent window
        text="Start Joke",                                        # Button label
        font=("Arial", 16, "underline"),                          # Font size and underline
        fg="black",                                               # Text color
        bg=canvas['bg'],                                          # Match canvas background
        activebackground=canvas['bg'],                            # Background color when clicked
        activeforeground="black",                                 # Text color when clicked
        bd=0,                                                     # Remove border
        highlightthickness=0,                                     # Remove focus highlight
        highlightbackground=canvas['bg'],                         # Highlight background color
        highlightcolor=canvas['bg'],                              # Highlight color
        relief="flat",                                            # Flat button style
        cursor="hand2",                                           # Hand cursor on hover
        command=show_joke_screen                                   # Function to call on click
    )
    canvas.create_window(400, 370, window=start_button)           # Place button on canvas

# Show joke screen
def show_joke_screen():
    """
    Display joke screen with setup text, punchline text, and control buttons.
    """
    global setup_text_id, punchline_text_id, punchline_shown       # Declare global variables
    punchline_shown = False                                        # Reset punchline flag

    canvas.delete("all")                                           # Clear the canvas
    canvas.create_image(0, 0, image=joke_bg, anchor="nw")         # Display joke screen background

    # Setup text (initial message)
    setup_text_id = canvas.create_text(
        400, 250,                                                  # x, y coordinates
        text="Click on Alexa tell me a Joke! to begin",           # Initial text
        fill="black",                                              # Text color
        font=("Comic Sans MS", 20),                                # Font size
        width=500                                                  # Max width for wrapping text
    )

    # Punchline text (hidden initially)
    punchline_text_id = canvas.create_text(
        400, 330,                                                  # x, y coordinates
        text="",                                                    # Empty initially
        fill="black",                                              # Text color
        font=("Comic Sans MS", 20),                                # Font size
        width=500                                                  # Max width for wrapping
    )

    # Alexa button (works only once)
    def alexa_first_joke():
        """
        Displays first joke and disables button after click.
        """
        next_joke()                                                  # Call next_joke to show first joke
        alexa_button.config(state="disabled")                        # Disable Alexa button

    # Create Alexa button
    alexa_button = tk.Button(
        window,
        text="Alexa tell me a Joke",                                 # Button label
        font=("Arial", 16),                                          # Font size
        fg="black",                                                   # Text color
        bg=canvas['bg'],                                              # Background color
        activebackground=canvas['bg'],                                # Background color on click
        activeforeground="black",                                      # Text color on click
        bd=0,                                                         # Remove border
        highlightthickness=0,                                         # Remove focus highlight
        relief="flat",                                                # Flat style
        cursor="hand2",                                               # Hand cursor on hover
        command=alexa_first_joke                                       # Function to call on click
    )
    canvas.create_window(380, 430, window=alexa_button)               # Place Alexa button

    # Show Punchline button
    def show_punchline_button():
        """
        Displays punchline and sets flag to allow next joke.
        """
        global punchline_shown
        if current_joke is None:                                      # Check if a joke has been shown
            messagebox.showinfo("Oops!", "Click Alexa tell me a Joke first!")  # Show alert
        else:
            canvas.itemconfigure(punchline_text_id, text=current_joke[1])     # Show punchline
            punchline_shown = True                                        # Set flag that punchline is shown

    # Create Show Punchline button
    show_button = tk.Button(
        window,
        text="Show Punchline",                                           # Button label
        font=("Arial", 16),                                              # Font size
        command=show_punchline_button                                     # Function on click
    )

    # Next Joke button
    def next_joke_button():
        """
        Only allows next joke if punchline was revealed.
        """
        global punchline_shown
        if not punchline_shown:                                         # If punchline not shown
            messagebox.showinfo(                                         # Show alert
                "Hold on!", 
                "See punchline before moving to next joke! Click 'Show Punchline'."
            )
        else:
            next_joke()                                                  # Show next joke
            punchline_shown = False                                       # Reset flag for next joke

    # Create Next Joke button
    next_button = tk.Button(
        window,
        text="Next Joke",                                                 # Button label
        font=("Arial", 16),                                              # Font size
        command=next_joke_button                                          # Function on click
    )

    # Quit button
    quit_button = tk.Button(
        window,
        text="Quit",                                                      # Button label
        font=("Arial", 16),                                               # Font size
        command=window.destroy                                             # Close app on click
    )

    # Place buttons on canvas
    canvas.create_window(250, 500, window=show_button)                      # Show Punchline
    canvas.create_window(400, 500, window=next_button)                      # Next Joke
    canvas.create_window(500, 500, window=quit_button)                      # Quit button

# Joke functions
def next_joke():
    """
    Select a random joke, display setup, and clear punchline.
    """
    global current_joke
    current_joke = random.choice(jokes_list)                 # Pick a random joke
    canvas.itemconfigure(setup_text_id, text=current_joke[0])  # Display setup
    canvas.itemconfigure(punchline_text_id, text="")           # Clear punchline

# Start program
show_main()         # Display the main screen
window.mainloop()   # Run the Tkinter event loop
