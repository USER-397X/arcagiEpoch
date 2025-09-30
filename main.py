def print_board(board):
    """Prints the current state of the Tic-Tac-Toe board."""
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("-----------")

def check_win(board, player):
    """Checks if the current player has won."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    return any(all(board[pos] == player for pos in condition) for condition in win_conditions)

def main():
    """Main game loop for Tic-Tac-Toe."""
    board = [" " for _ in range(9)]
    players = ["X", "O"]
    current_player = 0
    moves = 0

    print("Welcome to Tic-Tac-Toe!")
    print("Enter a number from 1-9 to place your mark.")
    print_board(board)

    while moves < 9:
        position = input(f"\nPlayer {players[current_player]}, choose a position (1-9): ")
        
        # Validate input
        if not position.isdigit() or not 1 <= int(position) <= 9:
            print("Invalid input! Please enter a number between 1 and 9.")
            continue
        
        index = int(position) - 1
        if board[index] != " ":
            print("That position is already taken! Try again.")
            continue
        
        # Make move
        board[index] = players[current_player]
        moves += 1
        print_board(board)
        
        # Check for win
        if check_win(board, players[current_player]):
            print(f"\nPlayer {players[current_player]} wins! Congratulations!")
            return
        
        # Switch player
        current_player = 1 - current_player
    
    print("\nIt's a draw! Good game!")

if __name__ == "__main__":
    main()
