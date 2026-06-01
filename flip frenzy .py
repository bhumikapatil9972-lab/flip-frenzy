import tkinter as tk
from tkinter import messagebox
import random
import time


class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 FLIP FRENZY 🎮")

        self.buttons = []
        self.cards = []
        self.flipped = []
        self.matched = []

        self.start_time = None
        self.time_limit = 60
        self.num_pairs = 4
        self.score = 0
        self.misses = 0

        # Window size and center
        window_width = 900
        window_height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # White background
        root.config(bg="white")

        # Splash Screen
        self.splash_frame = tk.Frame(root, bg="white")
        self.splash_frame.pack(expand=True, fill="both")

        title = tk.Label(
            self.splash_frame,
            text="⚡ FLIP FRENZY ⚡",
            font=("Arial", 36, "bold"),
            fg="#333333",
            bg="white"
        )
        title.pack(pady=50)

        start_btn = tk.Button(
            self.splash_frame,
            text="Start Game",
            font=("Arial", 20, "bold"),
            bg="#eeeeee",
            fg="#333333",
            command=self.start_game
        )
        start_btn.pack(pady=20)

    def start_game(self):
        self.splash_frame.destroy()

        self.score_label = tk.Label(
            self.root,
            text="Score: 0 | Misses: 0",
            font=("Consolas", 18, "bold"),
            fg="#333333",
            bg="white"
        )
        self.score_label.pack(pady=5)

        self.timer_label = tk.Label(
            self.root,
            text="Time Left: 0s",
            font=("Consolas", 18, "bold"),
            fg="#333333",
            bg="white"
        )
        self.timer_label.pack(pady=5)

        # Controls
        control_frame = tk.Frame(self.root, bg="white")
        control_frame.pack(pady=10)

        btn_style = {
            "font": ("Arial", 14, "bold"),
            "bg": "#eeeeee",
            "fg": "#333333",
            "width": 10
        }

        tk.Button(control_frame, text="Hint", command=self.show_hint, **btn_style).pack(side="left", padx=10)
        tk.Button(control_frame, text="Solve", command=self.solve_game, **btn_style).pack(side="left", padx=10)
        tk.Button(control_frame, text="New Game", command=self.new_game, **btn_style).pack(side="left", padx=10)

        self.grid_frame = tk.Frame(self.root, bg="white")
        self.grid_frame.pack(expand=True)

        tk.Button(
            self.root,
            text="Exit",
            font=("Arial", 12, "bold"),
            bg="#eeeeee",
            fg="#333333",
            width=10,
            command=self.safe_exit
        ).pack(side="bottom", pady=10)

        self.new_game()

    def safe_exit(self):
        """Exit instantly."""
        self.root.destroy()

    def new_game(self):
        emojis = [
            "🍎", "🍌", "🐱", "🐶",
            "⭐", "❤️", "🚗", "⚽",
            "🌸", "🎵", "🍕", "🎲",
            "🐼", "🐧", "🌈", "🔥",
            "🧠", "💎", "🚀", "🎮"
        ]

        self.cards = emojis[:self.num_pairs] * 2
        random.shuffle(self.cards)
        self.flipped = []
        self.matched = []
        self.start_time = time.time()
        self.time_limit = 30 + (self.num_pairs * 10)
        self.score = 0
        self.misses = 0
        self.update_score()

        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()

        total_cards = len(self.cards)
        cols = min(4, total_cards)

        for i in range(total_cards):
            btn = tk.Button(
                self.grid_frame,
                text="?",
                width=6,
                height=3,
                font=("Arial", 24, "bold"),
                fg="#333333",
                bg="white",
                relief="solid",          # pastel border
                bd=2,                    # border thickness
                highlightbackground="#cccccc",  # soft border color
                command=lambda i=i: self.flip_card(i)
            )
            btn.grid(row=i // cols, column=i % cols, padx=15, pady=15)
            self.buttons.append(btn)

        self.update_timer()

    def flip_card(self, index):
        if index in self.flipped or index in self.matched:
            return

        # Different colors for emojis
        colors = ["#FF0000", "#008000", "#0000FF", "#FF00FF", "#FFA500", "#800080", "#00AAAA", "#333333"]
        color = colors[index % len(colors)]

        self.buttons[index].config(text=self.cards[index], fg=color)
        self.flipped.append(index)

        if len(self.flipped) == 2:
            self.root.after(600, self.check_match)

    def check_match(self):
        i1, i2 = self.flipped
        if self.cards[i1] == self.cards[i2]:
            self.matched.extend([i1, i2])
            self.buttons[i1].config(bg="#aaffaa")
            self.buttons[i2].config(bg="#aaffaa")
            self.score += 10
        else:
            self.buttons[i1].config(text="?", fg="#333333", bg="white")
            self.buttons[i2].config(text="?", fg="#333333", bg="white")
            self.misses += 1
            self.score = max(0, self.score - 2)
        self.flipped.clear()
        self.update_score()

        if len(self.matched) == len(self.cards):
            elapsed = int(time.time() - self.start_time)
            bonus = max(0, (self.time_limit - elapsed) // 5)
            self.score += bonus
            self.update_score()
            messagebox.showinfo("Winner", f"🎉 You Won!\n\nTime: {elapsed}s\nScore: {self.score}")
            if elapsed < self.time_limit // 2 and self.num_pairs < 12:
                self.num_pairs += 2
            self.new_game()

    def update_timer(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            remaining = self.time_limit - elapsed
            self.timer_label.config(text=f"Time Left: {remaining}s")
            if remaining <= 0:
                self.score = max(0, self.score - 5)
                messagebox.showinfo("Game Over", "⏳ Time's Up!")
                self.new_game()
                return
        self.root.after(1000, self.update_timer)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score} | Misses: {self.misses}")

    def show_hint(self):
        unmatched = [i for i in range(len(self.cards)) if i not in self.matched]
        if len(unmatched) < 2:
            return
        random.shuffle(unmatched)
        hint_cards = unmatched[:2]
        for i in hint_cards:
            self.buttons[i].config(text=self.cards[i], bg="#ffff99")

        def hide_hint():
            for i in hint_cards:
                if i not in self.matched:
                    self.buttons[i].config(text="?", fg="#333333", bg="white")

        self.root.after(1500, hide_hint)

    def solve_game(self):
        for i in range(len(self.cards)):
            self.buttons[i].config(text=self.cards[i], bg="#aaffaa", fg="#000000")
        messagebox.showinfo("AI Solver", "🤖 AI Solved The Game!")
        self.new_game()


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
