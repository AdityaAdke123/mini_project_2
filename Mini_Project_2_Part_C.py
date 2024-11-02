import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# Function to read dataset from file and extract features and labels

def load_data(filepath):
    data = np.loadtxt(filepath)  # Load data from the specified file
    X = data[:, :-1]  # Extract board states as features
    y = data[:, -1]   # Extract the target variable (outcome or optimal move)
    return X, y


# Class representing the Tic-Tac-Toe game board and its functionality
class Board:
    def __init__(self): # Create an empty Tic-Tac-Toe board represented as a 1D array of size 9

        self.board = np.zeros(9)

    def display(self):   # Show the current state of the board using symbols for players and empty spaces

        symbol_map = {1: 'X', -1: 'O', 0: ' '}
        print(f"\n {symbol_map[self.board[0]]} | {symbol_map[self.board[1]]} | {symbol_map[self.board[2]]}")
        print("---+---+---")
        print(f" {symbol_map[self.board[3]]} | {symbol_map[self.board[4]]} | {symbol_map[self.board[5]]}")
        print("---+---+---")
        print(f" {symbol_map[self.board[6]]} | {symbol_map[self.board[7]]} | {symbol_map[self.board[8]]}\n")

    def make_move(self, position, player):
        # Adjust input position from 1-9 to 0-8 (index) and validate move
        position -= 1
        if self.board[position] == 0:
            self.board[position] = player
            return True
        return False


# Class that manages the game flow and handles AI and human moves
class TicTacToeGame:
    def __init__(self, endgame_model, optimal_move_model):
        self.board = Board()  # Initialize a new empty board
        self.current_player = 1  # Start with player X (represented by 1)
        self.endgame_model = endgame_model  # Model for predicting endgame results
        self.optimal_move_model = optimal_move_model  # Model for choosing best moves in early stages

    def display_position_guide(self):   # Display the numbered positions of the board to guide the user

        print("Board positions are as follows:")
        print("\n 1 | 2 | 3")
        print("---+---+---")
        print(" 4 | 5 | 6")
        print("---+---+---")
        print(" 7 | 8 | 9\n")

    def switch_turn(self):  # Change the turn from one player to the other

        self.current_player *= -1

    def is_valid_move(self, move):  # Ensure the selected move is valid (within bounds and on an empty square)

        return 1 <= move <= 9 and self.board.board[move - 1] == 0

    def is_board_full(self):    # Check if all spaces on the board are filled

        return np.all(self.board.board != 0)

    def check_winner(self):     # Check the current board for a winning combination (rows, columns, or diagonals)

        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]
        for combo in winning_combinations:
            if self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]] != 0:
                return self.board.board[combo[0]]  # Return the winner (1 for X, -1 for O)
        return None

    def check_game_over(self):
        # Determine if the game has finished either with a win or a draw
        winner = self.check_winner()
        if winner:
            return f"Player {'X' if winner == 1 else 'O'} wins!"
        elif self.is_board_full():
            return "It's a draw!"
        return None

    def play(self):
        # Main game loop where turns alternate between human and AI
        self.display_position_guide()  # Show the position guide before the game starts
        while True:
            self.board.display()  # Display the current board state
            game_status = self.check_game_over()  # Check if the game has ended
            if game_status:
                print(game_status)
                break

            if self.current_player == 1:  # Human's turn (Player X)
                try:
                    move = int(input("Your move (1-9): "))  # Get input from the human player
                    if not self.is_valid_move(move):
                        print("Invalid move, try again.")
                        continue
                    self.board.make_move(move, 1)  # Make the move for the human player
                except ValueError:
                    print("Please enter a valid number.")
                    continue
            else:  # AI's turn (Player O)
                if np.count_nonzero(self.board.board) == 8:  # Check if only one move remains (endgame)
                    # Use the endgame model to predict the optimal final move
                    move = int(self.endgame_model.predict([self.board.board])[0]) + 1  # Adjust back to 1-9
                    print(f"AI (Endgame) chose: {move}")
                else:
                    # Use the optimal move model to decide the best move for the current board state
                    move = int(self.optimal_move_model.predict([self.board.board])[0]) + 1  # Adjust back to 1-9
                    print(f"AI (Optimal Move) chose: {move}")
                self.board.make_move(move, -1)  # Make the move for the AI

            self.switch_turn()  # Switch turns between the human and AI


# Load datasets for both endgame predictions and intermediate move optimization

X_endgame, y_endgame = load_data('tictac_final.txt')
X_optimal, y_optimal = load_data('tictac_single.txt')


# Initialize RandomForest models for predicting endgame results and optimal moves
endgame_model = RandomForestClassifier(n_estimators=100)

optimal_move_model = RandomForestClassifier(n_estimators=100)


# Split the datasets into training and testing sets
X_train_endgame, X_test_endgame, y_train_endgame, y_test_endgame = train_test_split(X_endgame, y_endgame, test_size=0.2, random_state=42)

X_train_optimal, X_test_optimal, y_train_optimal, y_test_optimal = train_test_split(X_optimal, y_optimal, test_size=0.2, random_state=42)



# Train the RandomForest models using their respective datasets
endgame_model.fit(X_train_endgame, y_train_endgame)

optimal_move_model.fit(X_train_optimal, y_train_optimal)


# Start the game where a human plays against the AI
game = TicTacToeGame(endgame_model, optimal_move_model)
game.play()
