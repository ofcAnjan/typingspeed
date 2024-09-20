import tkinter as tk
from tkinter import messagebox
import time
import random

# Variables that would have been instance variables
root = tk.Tk()
root.title("Typing Speed Test")
root.geometry("600x400")

bg_color = "#2e2e2e"  # Dark gray
fg_color = "#ffffff"  # White
highlight_color = "#4a4a4a"  # Slightly lighter gray for highlighting
common_words = []
sample_text = ""
start_time = 0
end_time = 0
test_started = False
penalty = 2  # Penalty in seconds for each incorrect word
errors = 0  # Track the number of errors

def load_words_from_file(filename):
    global common_words
    try:
        with open(filename, 'r') as file:
            common_words = [line.strip() for line in file.readlines()]
        print(f"Loaded {len(common_words)} words from {filename}.")  # Debug print
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filename}' not found.")
        print(f"Error: File '{filename}' not found.")  # Debug print
        root.quit()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Error: {str(e)}")  # Debug print
        root.quit()

def generate_sample_text():
    # Generate a random sample text from the common words
    return " ".join(random.sample(common_words, 10))  # Select 10 random words

def start_timing(event):
    # Start the timer on the first key press
    global start_time, test_started
    if not test_started:
        start_time = time.time()  # Record the start time
        test_started = True

def on_enter_pressed(event):
    # Handle the logic when the user presses 'Enter' to end the test
    global end_time, errors

    user_input = entry_text.get(1.0, tk.END).strip()

    # Prevent new line insertion when pressing Enter
    entry_text.mark_set(tk.INSERT, "end-1c")  # Move cursor to the end of the text to prevent newline insertion

    if user_input:
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate elapsed time in seconds

        # Calculate WPM without penalty
        word_count = len(user_input.split())
        wpm = word_count / (elapsed_time / 60)

        # Check for errors and apply penalty
        errors = calculate_errors(user_input)
        total_penalty = errors * penalty
        total_time_with_penalty = elapsed_time + total_penalty
        wpm_with_penalty = word_count / (total_time_with_penalty / 60)

        # Display result
        label_result.config(text=f"You made {errors} error(s).\nYour typing speed: {wpm:.2f} WPM")

        # Disable further typing after completion
        entry_text.config(state=tk.DISABLED)

    return "break"  # Stop default behavior of adding new line

def calculate_errors(user_input):
    # Calculate the number of incorrect words in the user's input
    user_words = user_input.split()
    sample_words = sample_text.split()

    # Count errors by comparing words at each position
    return sum(1 for u_word, s_word in zip(user_words, sample_words) if u_word != s_word)

def reset_test():
    # Reset the test so that a new test can be started
    global sample_text, start_time, end_time, test_started, errors
    entry_text.config(state=tk.NORMAL)
    entry_text.delete(1.0, tk.END)
    label_result.config(text="")
    sample_text = generate_sample_text()  # Generate new sample text
    label_sample_text.config(text=sample_text)  # Update the displayed text
    start_time = 0
    end_time = 0
    test_started = False
    errors = 0  # Reset errors

# Configure root window colors
root.configure(bg=bg_color)

# Load words from the file
load_words_from_file('D:\Programming\VSCode files\Python\Programming\common_words.txt')

# Generate the sample text
sample_text = generate_sample_text()

# Label for instruction
label_instruction = tk.Label(root, text="Start typing the sentence below", font=('Arial', 14), bg=bg_color, fg=fg_color)
label_instruction.pack(pady=20)

# Label for displaying the sentence
label_sample_text = tk.Label(root, text=sample_text, font=('Arial', 12), bg=bg_color, fg=fg_color, wraplength=500)
label_sample_text.pack(pady=10)

# Text box for user input
entry_text = tk.Text(root, height=5, width=60, font=('Arial', 12), bg=highlight_color, fg=fg_color, insertbackground='white')
entry_text.pack(pady=10)
entry_text.bind("<KeyPress>", start_timing)  # Bind the keypress event to start the test
entry_text.bind("<Return>", on_enter_pressed)  # Bind "Enter" key to end the test

# Result label
label_result = tk.Label(root, text="", font=('Arial', 14), bg=bg_color, fg=fg_color)
label_result.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
