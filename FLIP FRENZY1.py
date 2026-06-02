import tkinter as tk
import random
import time
from tkinter import messagebox

class FlipFrenzy:
    def __init__(self, root):
        self.root = root
        self.root.title("Flip Frenzy")
        self.root.configure(bg="#f0f8ff")
        self.reset_game()

    def reset_game(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.cards = []
        self.buttons = []
        self.flipped = []
        self.ai_memory = {}
        self.player_score = 0
        self.ai_score = 0
        self.turn = "Player"
        self.start_time = time.time()

        emojis = ["😀","🐱","🍎","⚽","🚗","🌸","🎵","⭐"]
        self.deck = emojis * 2
        random.shuffle(self.deck)

        # Splash screen
        self.splash = tk.Label(self.root, text="Welcome to Flip Frenzy!", 
                               font=("Arial", 24, "bold"), bg="#f0f8ff")
        self.splash.pack(pady=20)
        self.start_btn = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_btn.pack()

    def start_game(self):
        self.splash.destroy()
        self.start_btn.destroy()

        # Scoreboard
        self.score_label = tk.Label(self.root, text="Player: 0 | AI: 0", 
                                    font=("Arial", 16), bg="#f0f8ff")
        self.score_label.pack(pady=10)

        # Timer
        self.timer_label = tk.Label(self.root, text="Time: 0s", 
                                    font=("Arial", 14), bg="#f0f8ff")
        self.timer_label.pack()
        self.update_timer()

        # Exit button (fixed)
        self.exit_btn = tk.Button(self.root, text="Exit Game", command=self.root.destroy)
        self.exit_btn.pack(pady=5)

        # Card grid
        frame = tk.Frame(self.root, bg="#f0f8ff")
        frame.pack()
        for i in range(4):
            for j in range(4):
                idx = i*4+j
                btn = tk.Button(frame, text="?", width=6, height=3, 
                                font=("Arial", 20), bg="#ffe4e1", 
                                command=lambda idx=idx: self.flip_card(idx))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(btn)

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed}s")
        self.root.after(1000, self.update_timer)

    def flip_card(self, idx):
        if self.turn != "Player":
            return
        if self.buttons[idx]["text"] == "?":
            self.buttons[idx]["text"] = self.deck[idx]
            self.flipped.append(idx)
            if len(self.flipped) == 2:
                self.root.after(1000, self.check_match)

    def check_match(self):
        first, second = self.flipped
        if self.deck[first] == self.deck[second]:
            self.player_score += 1
            self.buttons[first]["state"] = "disabled"
            self.buttons[second]["state"] = "disabled"
        else:
            self.buttons[first]["text"] = "?"
            self.buttons[second]["text"] = "?"
            self.turn = "AI"
            self.root.after(1000, self.ai_turn)
        self.flipped = []
        self.update_score()
        self.check_game_over()

    def ai_turn(self):
        # Step 1: Pick first card
        first = self.ai_pick_card()
        self.buttons[first]["text"] = self.deck[first]
        self.root.update()
        time.sleep(0.5)

        # Step 2: Pick second card
        second = self.ai_pick_card(exclude=first)
        self.buttons[second]["text"] = self.deck[second]
        self.root.update()
        time.sleep(0.5)

        # Step 3: Check match
        if self.deck[first] == self.deck[second]:
            self.ai_score += 1
            self.buttons[first]["state"] = "disabled"
            self.buttons[second]["state"] = "disabled"
            self.update_score()
            self.check_game_over()
            # AI continues if matched
            self.root.after(1000, self.ai_turn)
            return
        else:
            self.buttons[first]["text"] = "?"
            self.buttons[second]["text"] = "?"
            self.turn = "Player"

        # Step 4: Update memory
        self.ai_memory[first] = self.deck[first]
        self.ai_memory[second] = self.deck[second]

        self.update_score()
        self.check_game_over()

    def ai_pick_card(self, exclude=None):
        # Competitive AI: prioritize known pairs
        for pos1, val1 in self.ai_memory.items():
            for pos2, val2 in self.ai_memory.items():
                if pos1 != pos2 and val1 == val2:
                    if self.buttons[pos1]["text"] == "?" and pos1 != exclude:
                        return pos1
                    if self.buttons[pos2]["text"] == "?" and pos2 != exclude:
                        return pos2
        # Otherwise pick random unrevealed card
        choices = [i for i, btn in enumerate(self.buttons) if btn["text"] == "?" and i != exclude]
        return random.choice(choices)

    def update_score(self):
        self.score_label.config(text=f"Player: {self.player_score} | AI: {self.ai_score}")

    def check_game_over(self):
        if all(btn["state"] == "disabled" for btn in self.buttons):
            winner = "Player" if self.player_score > self.ai_score else "AI"
            messagebox.showinfo("Game Over", f"Winner: {winner}\nPlayer: {self.player_score} | AI: {self.ai_score}")
            # Automatically start new game
            self.reset_game()

# -----------------------------
# Run Game
# -----------------------------
root = tk.Tk()
game = FlipFrenzy(root)
root.mainloop()

