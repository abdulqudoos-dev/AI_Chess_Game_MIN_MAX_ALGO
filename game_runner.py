import grid_state
import utils
import os
from collections import deque
from copy import deepcopy


###########################################
# AI Implementation with Minimax Algorithm
###########################################

class AI:
    """
    AI chess player implementation using minimax algorithm with alpha-beta pruning.
    This class handles all AI-related functionality including:
    - Move calculation using minimax algorithm
    - Alpha-beta pruning for optimization
    - Move execution and validation
    """

    def __init__(self, team: str, depth: int):
        """
        Initialize AI player with team color and search depth
        Args:
            team: AI's team color ('black' or 'white')
            depth: How many moves ahead the AI should look
        """
        self.team = team
        self.depth = depth

    def max_value(self, _board: grid_state.ChessBoard, depth: int, team: str, alpha: int, beta: int) -> (float, str): # type: ignore
        """
        Maximizing player's move evaluation (typically white)
        Implements the maximizing part of minimax algorithm with alpha-beta pruning
        Args:
            _board: Current board state
            depth: Search depth
            team: Current player's team
            alpha: Alpha value for pruning
            beta: Beta value for pruning
        Returns:
            Tuple of (evaluation score, best move)
        """
        if depth == 0:
            return utils.get_board_evaluation(_board), None

        value = -9999
        best_move = None
        moves = _board.get_all_allowed_moves(team)

        for move in moves:
            temp = _board.get_copy()
            temp_board = grid_state.ChessBoard(True)
            temp_board.board = deepcopy(temp)

            if temp_board.move_piece(move, team, False):
                val, _ = self.min_value(temp_board, depth - 1, utils.get_opposite_team(team), alpha, beta)

                if val > value:
                    value = val
                    best_move = move

                alpha = max(alpha, value)
                if beta <= alpha:
                    return value, best_move

        return value, best_move

    def min_value(self, _board: grid_state.ChessBoard, depth: int, team: str, alpha: int, beta: int) -> (float, str): # type: ignore
        """
        Minimizing player's move evaluation (typically black)
        Implements the minimizing part of minimax algorithm with alpha-beta pruning
        Args:
            _board: Current board state
            depth: Search depth
            team: Current player's team
            alpha: Alpha value for pruning
            beta: Beta value for pruning
        Returns:
            Tuple of (evaluation score, best move)
        """
        if depth == 0:
            return utils.get_board_evaluation(_board), None

        value = 9999
        best_move = None
        moves = _board.get_all_allowed_moves(team)

        for move in moves:
            temp = _board.get_copy()
            temp_board = grid_state.ChessBoard(True)
            temp_board.board = deepcopy(temp)

            if temp_board.move_piece(move, team, False):
                val, _ = self.max_value(temp_board, depth - 1, utils.get_opposite_team(team), alpha, beta)

                if val < value:
                    value = val
                    best_move = move

                beta = min(beta, value)
                if beta <= alpha:
                    return value, best_move

        return value, best_move

    def minimax(self, _board: grid_state.ChessBoard) -> str:
        """
        Determines the optimal move using minimax algorithm with alpha-beta pruning
        This is the main entry point for AI move calculation
        Args:
            _board: Current board state
        Returns:
            Best move in chess notation
        """
        try:
            alpha = -10000  # Minimum possible score
            beta = 10000    # Maximum possible score

            if self.team == 'black':
                _, best_move = self.min_value(_board, self.depth, 'black', alpha, beta)
            elif self.team == 'white':
                _, best_move = self.max_value(_board, self.depth, 'black', alpha, beta)
            else:
                raise Exception("Invalid AI team configuration")

            return best_move
        except Exception as e:
            print(f"Error in minimax: {str(e)}")
            return None

    def convert_move_format(self, move: str) -> str:
        """
        Converts move format between different chess notation styles
        Args:
            move: Move in old format
        Returns:
            Move in new format
        """
        try:
            if move and len(move) == 4:
                src = move[:2]
                dst = move[2:]
                src_new = chr(ord('a') + int(src[1]) - ord('a')) + src[0]
                dst_new = chr(ord('a') + int(dst[1]) - ord('a')) + dst[0]
                return src_new + dst_new
            return move
        except:
            return move

    def move(self, _board: grid_state.ChessBoard) -> bool:
        """
        Executes the AI's move on the board
        This method:
        1. Calculates the best move using minimax
        2. Converts the move to proper notation
        3. Executes the move on the board
        Args:
            _board: Current board state
        Returns:
            True if move was successful, False otherwise
        """
        try:
            best_move = self.minimax(_board)

            if best_move is not None:
                old_row, old_col, new_row, new_col = utils.parse_input(best_move)
                if old_row is not None:
                    best_move_new = chr(old_col + ord('a')) + str(8 - old_row) + chr(new_col + ord('a')) + str(8 - new_row)
                    name = _board.get_piece_name(best_move_new[:2])
                    result = _board.move_piece(best_move_new, self.team, False)
                    if result:
                        print(f"\nAI: moving {name} from {best_move_new[:2]} to {best_move_new[2:]}")
                        return True
            return False
        except Exception as e:
            print(f"Error executing AI move: {str(e)}")
            return False


###########################################
# Game UI and Control Functions
###########################################

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_game_state(chess_board, move_history):
    clear_screen()
    print("\n🎮 Battle of Kings Arena 🎮")
    
    # Split the display into board and move history
    board_lines = chess_board.get_display_lines()
    
    # Display board with move history
    print("\n   Last 4 Moves:")
    print("   ------------")
    for i, move in enumerate(move_history):
        print(f"   {move}")
    print("   ------------\n")
    
    # Display the board
    for line in board_lines:
        print(line)


def is_valid_position(pos):
    """Validate if the position input is in correct chess notation format."""
    if not isinstance(pos, str) or len(pos) != 2:
        return False
    
    # First character should be a-h
    if pos[0] not in 'abcdefgh':
        return False
    
    # Second character should be 1-8
    if pos[1] not in '12345678':
        return False
    
    return True


def get_valid_move_input(prompt):
    """Get and validate move input from user."""
    while True:
        try:
            move = input(prompt).strip().lower()
            
            # Allow quitting
            if move in ['q', 'quit', 'exit']:
                return None
                
            # Check basic format
            if not is_valid_position(move):
                print("❌ Invalid format! Use letter (a-h) + number (1-8), e.g., 'e2'")
                continue
                
            return move
            
        except Exception as e:
            print(f"❌ Invalid input! Please use proper chess notation (e.g., 'e2')")
            continue


def game(depth):
    # user's predefined team colour
    player_team = 'white'

    # initialising the AI player
    ai_player = AI('black', depth)

    # initialising the board and its pieces
    chess_board = grid_state.ChessBoard(False)
    chess_board.place_pieces()
    chess_board.update_points()
    chess_board.update_moves()

    # Initialize move history
    move_history = deque(maxlen=4)

    display_game_state(chess_board, move_history)

    while True:
        # take user input with validation
        move_piece = get_valid_move_input("\n🔄 From: ")
        if move_piece is None:
            print("\n👋 Game ended by player.")
            return
            
        move_to = get_valid_move_input("🎯 To: ")
        if move_to is None:
            print("\n👋 Game ended by player.")
            return

        try:
            result, name = chess_board.move_piece(move_piece + move_to, player_team, True)

            if not result:
                print("\n❌ Invalid move! Try again.")
                input("Press Enter to continue...")

            else:
                # Add move to history
                move_history.append(f"You: {name} {move_piece} → {move_to}")
                display_game_state(chess_board, move_history)

                # check if user wins
                if grid_state.in_checkmate(chess_board, ai_player.team):
                    print("\n👑 Victory! You've conquered the AI!\n")
                    break

                if grid_state.in_stalemate(chess_board, ai_player.team):
                    print("🤝 Stalemate - A draw!")
                    break

                # move by AI
                print("\n🤖 AI calculating...")
                
                # Get the piece at current position before AI moves
                best_move = ai_player.minimax(chess_board)
                if best_move:
                    old_row, old_col, new_row, new_col = utils.parse_input(best_move)
                    if old_row is not None:
                        from_pos = chr(old_col + ord('a')) + str(8 - old_row)
                        to_pos = chr(new_col + ord('a')) + str(8 - new_row)
                        piece_name = chess_board.get_piece_name(from_pos)
                        
                        # Make the AI move
                        if ai_player.move(chess_board):
                            move_history.append(f"AI: {piece_name} {from_pos} → {to_pos}")
                
                display_game_state(chess_board, move_history)

                # check if AI wins
                if grid_state.in_checkmate(chess_board, player_team):
                    print("💫 Checkmate - AI wins!")
                    break

                if grid_state.in_stalemate(chess_board, player_team):
                    print("🌟 Stalemate - Game drawn!")
                    break
                    
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try your move again.")
            input("Press Enter to continue...")
            display_game_state(chess_board, move_history)


def main():
    clear_screen()
    print("\n🏰 Royal Chess Arena 🏰")
    print("⚔️ Player vs AI ⚔️")
    
    # initialise depth
    depth = -1

    while depth not in [1, 2, 3, 4, 5]:
        print("\n🎚️ Select AI Level:")
        print("1 - Novice")
        print("2 - Advanced")
        print("3 - Expert")
        print("4 - Master")
        print("5 - Grandmaster")
        try:
            choice = input("\n⭐ Choose level (1-5): ").strip()
            if choice.lower() in ['q', 'quit', 'exit']:
                print("\n👋 Game cancelled.")
                return
                
            depth = int(choice)
            if depth not in [1, 2, 3, 4, 5]:
                print("❌ Enter 1-5 only!")
        except ValueError:
            print("❌ Invalid input! Please enter a number between 1 and 5.")

    # run game
    game(depth)


if __name__ == "__main__":
    main()
