import random

from tkinter import ttk
from pathlib import Path
import tkinter as tk
import random
import string
import sys

WORD_LEN = 5
MAX_TRIES = 6
COLOR_BORDER_HIGHLIGHT = "#565758"
COLOR_BLANK = "#121213"
COLOR_INCORRECT = "#3a3a3c"
COLOR_HALF_CORRECT = "#b59f3b"
COLOR_CORRECT = "#538d4e"
BOX_SIZE = 55
PADDING = 3


try:
    BASE_PATH = Path(sys._MEIPASS)
except AttributeError:
    BASE_PATH = Path(".")

WORDLIST = BASE_PATH / "wordle_ord.txt"

with open(WORDLIST, "r") as f:
    WORD = set(word.strip().lower() for word in f)


class MainScreen(tk.Frame):
    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller

        self.bind("<Return>", self.check_word)
        self.bind("<BackSpace>", self.remove_letter)
        self.bind("<Key>", self.enter_letter)

        self.init_ui()
        self.new_game()

    def new_game(self):
        self.answer = random.choice(list(WORD)).lower()
        self.words = [""] * 6
        self.correct_letters = set()
        self.half_correct_letters = set()
        self.incorrect_letters = set()
        self.current_word = 0

        # reset the grid and keyboard
        for i in range(MAX_TRIES):
            self.use_word = i
            self.update_labels()
        self.use_word = self.current_word
        self.update_keyboard()

        # hide the game over dialog
        self.game_over_dialog.place_forget()

    def congratulate(self):
        self.game_over_dialog_title.set("Congrats!")
        self.game_over_dialog_message.set(f"You guessed the word {self.answer.upper()}. Play again?")
        self.game_over_dialog.place(relx=0.5, rely=0.5, anchor="center")

    def humiliate(self):
        self.game_over_dialog_title.set("Max attemts reached")
        self.game_over_dialog_message.set(f"The word was {self.answer.upper()}. Play again?")
        self.game_over_dialog.place(relx=0.5, rely=0.5, anchor="center")

    def init_ui(self):

        # top bar
        container = tk.Frame(self, bg=COLOR_BLANK, height=40)
        container.grid(sticky="we")
        container.grid_columnconfigure(1, weight=1)

        # title
        tk.Label(
            container,
            text="WORDLE",
            fg="#d7dadc",
            bg=COLOR_BLANK,
            font=("Helvetica Neue", 28, "bold"),
        ).grid(row=0, column=1)

        # rules
        tk.Label(
            container,
            text="Six attempts to guess a 5-letter word. Guidance is by using color-coded feedback.\n Green means correct letter in the correct position, yellow means correct letter in the wrong position, and gray means incorrect letter. Good luck!",
            fg="#d7dadc",
            bg=COLOR_BLANK,
            font=("Helvetica Neue", 10),
        ).grid(row=1, column=1)

        # top
        ttk.Separator(self).grid(sticky="ew")
        self.top_separator = tk.Frame(self, bg=COLOR_BLANK, height=45)
        self.top_separator.grid_rowconfigure(0, weight=1)
        self.top_separator.grid_columnconfigure(0, weight=1)
        self.top_separator.grid_propagate(False)
        self.top_separator.grid(sticky="news")

        # main game grid
        self.rowconfigure(3, weight=1)

        container = tk.Frame(self, bg=COLOR_BLANK)
        container.grid()

        self.labels = []
        for i in range(MAX_TRIES):
            row = []
            for j in range(WORD_LEN):
                cell = tk.Frame(
                    container,
                    width=BOX_SIZE,
                    height=BOX_SIZE,
                    highlightthickness=1,
                    highlightbackground=COLOR_INCORRECT,
                )
                cell.grid_propagate(0)
                cell.grid_rowconfigure(0, weight=1)
                cell.grid_columnconfigure(0, weight=1)
                cell.grid(row=i, column=j, padx=PADDING, pady=PADDING)
                t = tk.Label(
                    cell,
                    text="",
                    justify="center",
                    font=("Helvetica Neue", 24, "bold"),
                    bg=COLOR_BLANK,
                    fg="#d7dadc",
                    highlightthickness=1,
                    highlightbackground=COLOR_BLANK,
                )
                t.grid(sticky="news")
                row.append(t)
            self.labels.append(row)

        # bottom
        tk.Frame(self, bg=COLOR_BLANK, height=45).grid()

        #  keyboard
        container = tk.Frame(self, bg=COLOR_BLANK)
        container.grid()

        # add all the alphabets
        self.keyboard_buttons = {}
        for i, keys in enumerate(["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]):
            row = tk.Frame(container, bg=COLOR_BLANK)
            row.grid(row=i, column=0)

            for j, c in enumerate(keys):
                if i == 2:
                    j += 1

                cell = tk.Frame(
                    row,
                    width=40,
                    height=55,
                    highlightthickness=1,
                    highlightbackground=COLOR_INCORRECT,
                )
                cell.grid_propagate(0)
                cell.grid_rowconfigure(0, weight=1)
                cell.grid_columnconfigure(0, weight=1)
                cell.grid(row=0, column=j, padx=PADDING, pady=PADDING)
                btn = tk.Button(
                    cell,
                    text=c,
                    justify="center",
                    font=("Helvetica Neue", 13),
                    bg=COLOR_BLANK,
                    fg="#d7dadc",
                    cursor="hand2",
                    border=0,
                    command=lambda c=c: self.enter_letter(key=c),
                )
                btn.grid(sticky="news")
                self.keyboard_buttons[c] = btn

        for col in (0, 8):
            text = "ENTER" if col == 0 else "⌫"
            func = self.check_word if col == 0 else self.remove_letter
            cell = tk.Frame(
                row,
                width=75,
                height=55,
                highlightthickness=1,
                highlightbackground=COLOR_INCORRECT,
            )
            cell.grid_propagate(0)
            cell.grid_rowconfigure(0, weight=1)
            cell.grid_columnconfigure(0, weight=1)
            cell.grid(row=0, column=col, padx=PADDING, pady=PADDING)
            btn = tk.Button(
                cell,
                text=text,
                justify="center",
                font=("Helvetica Neue", 13),
                bg=COLOR_BLANK,
                fg="#d7dadc",
                cursor="hand2",
                border=0,
                command=func,
            )
            btn.grid(row=0, column=0, sticky="news")

        # game over dialog

        self.game_over_dialog = tk.Frame(self, bg=COLOR_INCORRECT, highlightthickness=2)

        # title text
        self.game_over_dialog_title = tk.StringVar()
        tk.Label(
            self.game_over_dialog,
            textvariable=self.game_over_dialog_title,
            font=("Helvetica Neue", 22),
            bg=COLOR_INCORRECT,
            fg="white",
        ).grid(sticky="news", padx=10, pady=10)
        ttk.Separator(self.game_over_dialog).grid(sticky="ew")

        # message body
        self.game_over_dialog_message = tk.StringVar()
        tk.Label(
            self.game_over_dialog,
            textvariable=self.game_over_dialog_message,
            font=("Arial", 16),
            bg=COLOR_INCORRECT,
            fg="white",
        ).grid(sticky="news", padx=10, pady=10)
        ttk.Separator(self.game_over_dialog).grid(sticky="ew")

        # yes/no buttons
        self.game_over_dialog.grid_rowconfigure(4, weight=1)
        f = tk.Frame(self.game_over_dialog, bg=COLOR_INCORRECT)
        f.grid(sticky="news")
        f.grid_columnconfigure(0, weight=1)
        f.grid_columnconfigure(2, weight=1)
        for col in (0, 2):
            btn_text = "Yes" if col == 0 else "No"
            func = self.new_game if col == 0 else self.controller.destroy
            bg = "#4caf50" if col == 0 else "tomato"
            btn = tk.Button(
                f,
                text=btn_text,
                bg=COLOR_INCORRECT,
                fg="white",
                font=("Helvetica Neue", 13),
                border=0,
                cursor="hand2",
                command=func,
            )
            btn.bind("<Enter>", lambda e, btn=btn, bg=bg: btn.config(bg=bg))
            btn.bind("<Leave>", lambda e, btn=btn: btn.config(bg=COLOR_INCORRECT))
            btn.grid(row=0, column=col, sticky="ew")

        ttk.Separator(f, orient="vertical").grid(row=0, column=1, sticky="ns")

    #  game over dialog
    def toast(self, message, duration=2):

        t = tk.Label(self.top_separator, text=message, font=("Helvetica Neue", 16))
        t.grid(row=0, column=0, sticky="news", padx=5, pady=5)
        self.master.after(duration * 1000, lambda: t.grid_remove())

    def update_keyboard(self):
        for key, btn in self.keyboard_buttons.items():
            if key in self.correct_letters:
                btn["bg"] = COLOR_CORRECT
            elif key in self.half_correct_letters:
                btn["bg"] = COLOR_HALF_CORRECT
            elif key in self.incorrect_letters:
                btn["bg"] = COLOR_INCORRECT
            else:
                btn["bg"] = COLOR_BLANK

    def update_labels(self, colors=None):
        word = self.words[self.current_word]
        for i, label in enumerate(self.labels[self.use_word]):
            try:
                letter = word[i].upper()
            except IndexError:
                letter = ""

            label["text"] = letter
            if colors:
                label["bg"] = colors[i]
                label["highlightbackground"] = colors[i]
            else:
                label["bg"] = COLOR_BLANK
                label["highlightbackground"] = (
                    COLOR_BORDER_HIGHLIGHT if letter else COLOR_BLANK
                )

    def check_word(self, event=None):

        word = self.words[self.current_word].lower()
        if len(word) < WORD_LEN or word not in WORD or not word.isalpha():
            self.toast("Please enter a 5 letter valid word")
            return

        colors = [COLOR_BLANK] * WORD_LEN
        answer_letters = list(self.answer)

        # First pass: mark correct positions (green)
        for i, letter in enumerate(word):
            if letter == self.answer[i]:
                colors[i] = COLOR_CORRECT
                self.correct_letters.add(letter.upper())
                answer_letters[i] = None

        # Second pass: mark present letters (yellow)
        for i, letter in enumerate(word):
            if colors[i] == COLOR_CORRECT:
                continue

            if letter in answer_letters:
                colors[i] = COLOR_HALF_CORRECT
                self.half_correct_letters.add(letter.upper())
                answer_letters[answer_letters.index(letter)] = None
            else:
                colors[i] = COLOR_INCORRECT
                self.incorrect_letters.add(letter.upper())

        # update display
        self.use_word = self.current_word
        self.update_labels(colors)
        self.update_keyboard()

        # check win/lose conditions
        self.current_word += 1
        if word == self.answer:
            self.congratulate()
        elif self.current_word >= MAX_TRIES:
            self.humiliate()
        else:
            toast_message = f"Try again. Attempts left: {MAX_TRIES - self.current_word}"
            self.toast(toast_message)

    def remove_letter(self, event=None):

        if self.words[self.current_word]:
            self.words[self.current_word] = self.words[self.current_word][:-1]
            self.use_word = self.current_word
            self.update_labels()

    def enter_letter(self, event=None, key=None):

        key = key or event.keysym.upper()
        if key in string.ascii_uppercase:
            self.words[self.current_word] += key
            self.use_word = self.current_word
            self.update_labels()


class WordleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Wordle-Shmordle")
        self.geometry("600x800")

        # container
        container = tk.Frame(self, bg=COLOR_BLANK)
        container.grid(sticky="news")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create main screen
        self.frames = {}
        self.frames["MainScreen"] = MainScreen(
            master=container, controller=self, bg=COLOR_BLANK
        )
        self.frames["MainScreen"].grid(row=0, column=0, sticky="ns")

        # show the main screen
        self.show_frame("MainScreen")

        # fullscreen toggle
        self.fullscreen = False
        self.bind("<F11>", self.fullscreen_toggle)

    def show_frame(self, page_name):

        frame = self.frames[page_name]
        frame.focus_set()
        frame.tkraise()

    def fullscreen_toggle(self, event=None):

        self.fullscreen = not self.fullscreen
        self.wm_attributes("-fullscreen", self.fullscreen)


if __name__ == "__main__":
    app = WordleApp()
    app.mainloop()
