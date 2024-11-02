
class Board:                                                # Define the Board class to build the game board
    def __init__(self):                                     # Constructor to initialize the board with empty cells
        self.x = [[" " for _ in range(3)] for _ in range(3)]  # 3x3 board

    def printBoard(self):                                   # Method to print the current state of the board

        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"  # BOARD_HEADER constant to display the header row
        print(BOARD_HEADER)
        for i in range(3):                                   # Loop through rows to display the board contents
            row_display = f"| {i}  | " + " | ".join(self.x[i]) + " |"
            print(row_display)
            print("-----------------")


class Game:                                                   # Define the Game class to implement the game logic

    def __init__(self):                                       # Game state initialization constructor
        self.board = Board()
        self.turn = 'X'                                       # X always starts the game

    def switchPlayer(self):                                   # Method to switch between players
        self.turn = 'O' if self.turn == 'X' else 'X'

    def validateEntry(self, row, col):                        # Method to validate user input
        if 0 <= row < 3 and 0 <= col < 3 and self.board.x[row][col] == " ":
            return True
        return False

    def checkFull(self):                                       # Method to check if the board is full
        return all(self.board.x[row][col] != " " for row in range(3) for col in range(3))

    def checkWin(self):                                        # Method to check for a winning condition
        x = self.board.x
        for i in range(3):                                     # Check rows, columns, and diagonals for a win
            if x[i][0] == x[i][1] == x[i][2] != " " or x[0][i] == x[1][i] == x[2][i] != " ":
                return True
        if x[0][0] == x[1][1] == x[2][2] != " " or x[0][2] == x[1][1] == x[2][0] != " ":
            return True
        return False

    def checkEnd(self):                                         # Method to check if the game has ended
        if self.checkWin():
            print(f"{self.turn} IS THE WINNER!!!")
            return True
        if self.checkFull():
            print("DRAW! NOBODY WINS!")
            return True
        return False

    def playGame(self):                                         # Method to play the Tic-Tac-Toe game
        while True:
            self.board.printBoard()
            move = input(f"{self.turn}'s turn. Enter row and column separated by a comma: ").strip()
            try:
                row, col = map(int, move.split(","))
                if self.validateEntry(row, col):
                    self.board.x[row][col] = self.turn
                    if self.checkEnd():
                        self.board.printBoard()
                        break
                    self.switchPlayer()
                else:
                    print("Invalid entry or spot already taken. Try again.")
            except (ValueError, IndexError):
                print("Invalid input format. Please enter row and column as numbers between 0 and 2.")


def main():
    play_again = 'Y'
    while play_again.lower() == 'y':
        game = Game()
        game.playGame()
        play_again = input("Another game? Enter Y or y for yes: ")

    print("Thank you for playing!")


if __name__ == "__main__":
    main()
