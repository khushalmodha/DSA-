import tkinter as tk
from queue import Queue

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.turn = "X"  # Player X always starts
        self.root.state('zoomed')
        self.board = [[None for _ in range(3)] for _ in range(3)]  # 3x3 grid for the game
        self.queues = {
            'rows': [Queue(maxsize=3) for _ in range(3)],
            'cols': [Queue(maxsize=3) for _ in range(3)],
            'diag1': Queue(maxsize=3),
            'diag2': Queue(maxsize=3),
        }
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.winner_declared = False
        self.winner = None  # To store the winner's name
        self.moves_count = 0  # Track the number of moves to determine a draw
        self.home_page()  # Start with the home page

    def home_page(self):
        """Display the home page with a title and a Play button."""
        self.clear_frame()

        # Title
        title_label = tk.Label(self.root, text="Welcome to Tic Tac Toe", font=("Helvetica", 24, "bold"), bg="lightblue", fg="darkblue")
        title_label.pack(pady=30)

        title_label2 = tk.Label(self.root, text="Created by Jeel & Khushal ", font=("Helvetica", 18, "bold"), bg="lightblue", fg="darkblue")
        title_label2.pack(pady=35)

        # If there's a winner or a draw, show the corresponding message
        if self.winner:
            winner_label = tk.Label(self.root, text=f"{self.winner} Wins!", font=("Helvetica", 18, "bold"), bg="yellow", fg="black")
            winner_label.pack(pady=20)
        elif self.winner_declared and self.moves_count == 9:
            draw_label = tk.Label(self.root, text="It's a Draw!", font=("Helvetica", 18, "bold"), bg="orange", fg="black")
            draw_label.pack(pady=20)

        # Play button
        play_button = tk.Button(self.root, text="Play Game", font=("Helvetica", 16), bg="green", fg="white", padx=20, pady=10, command=self.start_game)
        play_button.pack(pady=20)

    def start_game(self):
        """Start the game by creating the game board."""
        self.clear_frame()
        self.create_board()

    def clear_frame(self):
        """Clears the current frame so new content can be loaded."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_board(self):
        """Create a 3x3 grid of buttons for the game board."""
        self.winner_declared = False
        self.turn = "X"  # Reset the turn to Player X
        self.board = [[None for _ in range(3)] for _ in range(3)]  # Clear the board
        self.moves_count = 0  # Reset moves count for the new game
        self.queues = {  # Reset the queues
            'rows': [Queue(maxsize=3) for _ in range(3)],
            'cols': [Queue(maxsize=3) for _ in range(3)],
            'diag1': Queue(maxsize=3),
            'diag2': Queue(maxsize=3),
        }

        # Set up grid row/column configurations to expand when resizing
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)  # Make rows expandable
            self.root.grid_columnconfigure(i, weight=1)  # Make columns expandable

        # Create the game board grid
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text="", font=("Helvetica", 20), bg="lightgray",
                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                # Use sticky NSEW to make the button expand to fill the grid cell
                button.grid(row=row, column=col, sticky="NSEW", padx=5, pady=5)  # No need for specific height/width
                self.buttons[row][col] = button

        # Start the game in maximized mode instead of fullscreen
        self.root.state('zoomed')

        # Allow exiting fullscreen with 'Esc'
        self.root.bind('<Escape>', self.exit_fullscreen)

    def on_button_click(self, row, col):
        """Handle the player's move when they click a button."""
        if self.buttons[row][col]['text'] == "" and not self.winner_declared:
            # Place player's move
            self.buttons[row][col]['text'] = self.turn
            self.buttons[row][col]['bg'] = "lightgreen" if self.turn == "X" else "lightcoral"
            self.board[row][col] = self.turn
            self.update_queues(row, col)
            self.moves_count += 1  # Increment move count

            # Check if there's a winner after this move
            if self.check_winner():
                self.declare_winner(self.turn)
            elif self.moves_count == 9:  # Check if all moves are made and it's a draw
                self.declare_draw()
            else:
                # Change turn
                self.turn = "O" if self.turn == "X" else "X"

    def update_queues(self, row, col):
        """Update the queues for rows, columns, and diagonals."""
        # Update row queue
        self.queues['rows'][row].put(self.turn)
        # Update column queue
        self.queues['cols'][col].put(self.turn)
        # Update diagonals if necessary
        if row == col:
            self.queues['diag1'].put(self.turn)
        if row + col == 2:
            self.queues['diag2'].put(self.turn)

    def check_winner(self):
        """Check if the current player has won the game."""
        # Check rows and columns
        for i in range(3):
            if self.is_winning_queue(self.queues['rows'][i]) or self.is_winning_queue(self.queues['cols'][i]):
                return True
        # Check diagonals
        if self.is_winning_queue(self.queues['diag1']) or self.is_winning_queue(self.queues['diag2']):
            return True
        return False

    def is_winning_queue(self, q):
        """Check if a queue contains three of the same item."""
        if q.full():
            items = list(q.queue)
            if items[0] == items[1] == items[2]:
                return True
        return False

    def declare_winner(self, player):
        """Declare the winner and display a message."""
        self.winner_declared = True
        self.winner = f"Player {player}"

        # Show Play Again button
        self.clear_frame()  # Clear board to show winner
        self.home_page()  # Go back to home page and show winner

    def declare_draw(self):
        """Declare the match as a draw if no winner is found and the board is full."""
        self.winner_declared = True
        self.winner = None

        # Show Play Again button with draw message
        self.clear_frame()  # Clear the board
        draw_label = tk.Label(self.root, text="It's a Draw!", font=("Helvetica", 18, "bold"), bg="orange", fg="black")
        draw_label.pack(pady=20)
        self.home_page()  # Go back to home page and show the draw message

# Main part of the program
root = tk.Tk()

# Allow window resizing, and grid will adjust
game = TicTacToe(root)

root.mainloop()
