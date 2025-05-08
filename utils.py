from copy import deepcopy



piece_square_tables = {
    "king": [
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
    ],

    "queen": [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
    ],

    "rook": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
    ],

    "bishop": [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
        [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
        [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
    ],

    "knight": [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
        [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
    ],

    "pawn": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ],

}


# Creates a mirrored and inverted version of the position table
def get_opposite_table(table):
    table = deepcopy(table)
    table.reverse()

    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = 0 - table[i][j]

    return table


# Returns the base value of a chess piece
def get_piece_value(_piece):
    if _piece == ' ':
        return 0

    return _piece.points


# Calculates position-based value for a piece using evaluation tables
def get_piece_evaluation(_piece):
    if _piece == ' ':
        return 0

    row = _piece.row
    col = _piece.col

    piece_table = piece_square_tables[_piece.name]

    if _piece.team == 'white':
        return piece_table[row][col]

    # Mirror table for black pieces
    else:
        piece_table = get_opposite_table(piece_table)
        return piece_table[row][col]


# Calculates total board evaluation based on piece values and positions
def get_board_evaluation(_board):
    val = 0

    for row in _board.board:
        for _piece in row:
            val += get_piece_value(_piece) + get_piece_evaluation(_piece)

    return val


# Converts chess notation (e.g., 'e2e4') to board coordinates
def parse_input(move: str) -> (int, int, int, int):
    if len(move) != 4:
        return None, None, None, None

    try:
        move_piece = move[0:2]  # Source square
        move_to = move[2:4]     # Target square

        # Validate chess notation format
        if not ('a' <= move_piece[0] <= 'h' and '1' <= move_piece[1] <= '8'):
            return None, None, None, None
        if not ('a' <= move_to[0] <= 'h' and '1' <= move_to[1] <= '8'):
            return None, None, None, None

        # Convert file to column index
        curr_col = ord(move_piece[0]) - ord('a')
        # Convert rank to row index
        curr_row = 8 - int(move_piece[1])

        # Convert target square coordinates
        new_col = ord(move_to[0]) - ord('a')
        new_row = 8 - int(move_to[1])

        # Validate coordinate ranges
        if not (0 <= curr_row <= 7 and 0 <= curr_col <= 7 and 0 <= new_row <= 7 and 0 <= new_col <= 7):
            return None, None, None, None

        return curr_row, curr_col, new_row, new_col
    except:
        return None, None, None, None


# Converts single square notation (e.g., 'e4') to board coordinates
def parse_position(pos: str) -> (int, int):
    try:
        # Validate square notation
        if len(pos) != 2 or not ('a' <= pos[0] <= 'h' and '1' <= pos[1] <= '8'):
            return None, None

        # Convert file to column index
        col = ord(pos[0]) - ord('a')
        # Convert rank to row index
        row = 8 - int(pos[1])

        # Validate coordinate ranges
        if not (0 <= row <= 7 and 0 <= col <= 7):
            return None, None

        return row, col
    except:
        return None, None


# Converts board coordinates to chess notation
def un_parse_input(curr_row: int, curr_col: int, new_row: int, new_col: int):
    try:
        # Convert coordinates to chess notation
        move_piece = chr(curr_col + ord('a')) + str(8 - curr_row)
        move_to = chr(new_col + ord('a')) + str(8 - new_row)
        return move_piece + move_to
    except:
        return None


# Returns the opposing team color
def get_opposite_team(team):
    if team == 'white':
        return 'black'

    if team == 'black':
        return 'white'
