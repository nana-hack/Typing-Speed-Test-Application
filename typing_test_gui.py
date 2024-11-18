import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
import random

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f0f0")

        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
        style.configure("TButton", font=("Arial", 11))

        # Variables
        self.current_text = ""
        self.start_time = None
        self.timer_running = False
        self.typed_chars = []
        self.difficulty = tk.StringVar(value="easy")

        self.setup_ui()
        self.load_new_text()

    def setup_ui(self):
        # Difficulty selection
        difficulty_frame = ttk.Frame(self.root, padding="10")
        difficulty_frame.pack(fill="x")
        
        ttk.Label(difficulty_frame, text="Difficulty:").pack(side="left", padx=5)
        for diff in ["easy", "medium", "hard"]:
            ttk.Radiobutton(difficulty_frame, text=diff.capitalize(), 
                          variable=self.difficulty, value=diff,
                          command=self.load_new_text).pack(side="left", padx=5)

        # Text display area
        self.text_display = tk.Text(self.root, height=4, width=60, wrap="word",
                                  font=("Arial", 12), pady=10, padx=10)
        self.text_display.pack(pady=20, padx=20)
        self.text_display.config(state="disabled")

        # Input area
        self.input_label = ttk.Label(self.root, text="Type here:")
        self.input_label.pack()
        
        self.input_text = tk.Text(self.root, height=4, width=60, wrap="word",
                                font=("Arial", 12), pady=10, padx=10)
        self.input_text.pack(pady=10, padx=20)
        self.input_text.bind("<KeyPress>", self.on_key_press)

        # Stats frame
        stats_frame = ttk.Frame(self.root, padding="10")
        stats_frame.pack(fill="x", pady=10)

        # WPM display
        self.wpm_label = ttk.Label(stats_frame, text="WPM: 0")
        self.wpm_label.pack(side="left", padx=20)

        # Accuracy display
        self.accuracy_label = ttk.Label(stats_frame, text="Accuracy: 100%")
        self.accuracy_label.pack(side="left", padx=20)

        # Time display
        self.time_label = ttk.Label(stats_frame, text="Time: 0s")
        self.time_label.pack(side="left", padx=20)

        # Buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill="x")

        self.reset_button = ttk.Button(button_frame, text="Reset", 
                                     command=self.reset_test)
        self.reset_button.pack(side="left", padx=5)

        self.new_text_button = ttk.Button(button_frame, text="New Text", 
                                        command=self.load_new_text)
        self.new_text_button.pack(side="left", padx=5)

    def load_new_text(self):
        try:
            with open("texts.json", "r") as f:
                texts = json.load(f)
                selected_difficulty = self.difficulty.get()
                self.current_text = random.choice(texts[selected_difficulty])
                
                self.text_display.config(state="normal")
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(1.0, self.current_text)
                self.text_display.config(state="disabled")
                
                self.reset_test()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading text: {str(e)}")

    def calculate_wpm(self):
        if not self.start_time:
            return 0
        elapsed_time = max(time.time() - self.start_time, 1)
        words = len(self.input_text.get(1.0, tk.END).split())
        return round((words / elapsed_time) * 60)

    def calculate_accuracy(self):
        typed_text = self.input_text.get(1.0, "end-1c")
        if not typed_text:
            return 100
        
        correct_chars = sum(1 for t, c in zip(self.current_text, typed_text) 
                          if t == c)
        total_chars = len(typed_text)
        return round((correct_chars / total_chars) * 100) if total_chars > 0 else 100

    def update_stats(self):
        if self.timer_running:
            wpm = self.calculate_wpm()
            accuracy = self.calculate_accuracy()
            elapsed_time = round(time.time() - self.start_time)

            self.wpm_label.config(text=f"WPM: {wpm}")
            self.accuracy_label.config(text=f"Accuracy: {accuracy}%")
            self.time_label.config(text=f"Time: {elapsed_time}s")

            # Check if test is complete
            if self.input_text.get(1.0, "end-1c") == self.current_text:
                self.timer_running = False
                messagebox.showinfo("Complete", 
                                  f"Test completed!\nWPM: {wpm}\n"
                                  f"Accuracy: {accuracy}%\n"
                                  f"Time: {elapsed_time} seconds")
            else:
                self.root.after(1000, self.update_stats)

    def on_key_press(self, event):
        if not self.timer_running and event.char:
            self.start_time = time.time()
            self.timer_running = True
            self.update_stats()

    def reset_test(self):
        self.input_text.delete(1.0, tk.END)
        self.start_time = None
        self.timer_running = False
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 100%")
        self.time_label.config(text="Time: 0s")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
