import curses
from curses import wrapper 

import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.addstr("\n\nPress ESC at any time to quit")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0, accuracy=100):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm} | Accuracy: {accuracy}%")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)

def load_text():
    try:
        with open("text.txt", "r", encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                return "The quick brown fox jumps over the lazy dog."
            return random.choice(lines).strip()
    except FileNotFoundError:
        return "The quick brown fox jumps over the lazy dog."

def calculate_accuracy(target, current):
    if not current:
        return 100
    correct = sum(1 for t, c in zip(target, current) if t == c)
    return round((correct / len(current)) * 100)

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        accuracy = calculate_accuracy(target_text, current_text)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm, accuracy)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # ESC key
            return False

        if key in ("KEY_BACKSPACE", '\b', "\x7f", "KEY_DC"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text) and len(key) == 1:  # Only accept single characters
            current_text.append(key)
    
    return True

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        if not wpm_test(stdscr):
            break
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue or ESC to quit...")
        key = stdscr.getkey()
        
        if ord(key) == 27:
            break
		

wrapper(main)
