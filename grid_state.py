import random
from copy import deepcopy
import utils


class Piece:
    moves = []

    def __init__(self, name, symbol, team, row, col, points):
        self.name = name
        self.symbol = symbol
        self.team = team
        self.row = row
        self.col = col
        self.points = points
        self.has_moved = False

    def update_indexes(self, r, c):
        self.row = r
        self.col = c

    def get_allowed_moves(self, _board):
        allowed_moves = []

        # go through every move available for this piece
        for move in self.moves:
            row = self.row
            col = self.col

            # potential location to move to
            new_row = row + move[0]
            new_col = col + move[1]

            # check that destination is not out of range
            if _board.in_range(new_row, new_col):
                # check that initial location is not empty
                if not _board.is_cell_empty(row, col):
                    # check that the move is possible for that piece
                    if _board.is_move_possible(self, new_row, new_col):
                        # check that there are no team-mates at destination
                        if not _board.team_at_destination(self, new_row, new_col):
                            # check that there are no team-mates blocking the path
                            if not _board.team_in_path(self, new_row, new_col):
                                # form string representation of the move
                                move = utils.un_parse_input(row, col, new_row, new_col)

                                # add to our list
                                if move not in allowed_moves:
                                    allowed_moves.append(move)

        return allowed_moves

    def get_copy(self):
        copy_ = deepcopy(self)
        copy_.name = deepcopy(self.name)
        copy_.symbol = deepcopy(self.symbol)
        copy_.team = deepcopy(self.team)
        copy_.row = deepcopy(self.row)
        copy_.col = deepcopy(self.col)
        copy_.points = deepcopy(self.points)
        copy_.has_moved = deepcopy(self.has_moved)
        copy_.moves = deepcopy(self.moves)

        return deepcopy(copy_)


class King(Piece):
    def __init__(self, symbol, team, row, col):
        super().__init__('king', symbol, team, row, col, 99999)
        self.moves = [
            [0, 1], [1, 0], [0, -1], [-1, 0],  # right, down, left, up
            [-1, -1], [1, 1], [-1, 1], [-1, -1]  # up-left, down-right, up-right, down-left diagonals
        ]


class Queen(Piece):
    def __init__(self, symbol, team, row, col):
        super().__init__('queen', symbol, team, row, col, 9)
        self.moves = [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],  # going right
            [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0],  # going down
            [0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7],  # going left
            [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0],  # going up
            [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7],  # down-right diagonal
            [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7],  # down-left diagonal
            [-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7],  # up-right diagonal
            [-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]]  # up-left diagonal


class Rook(Piece):
    def __init__(self, symbol, team, row, col):
        super().__init__('rook', symbol, team, row, col, 5)
        self.moves = [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
            [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0],
            [0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7],
            [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]]


class Bishop(Piece):
    def __init__(self, symbol, team, row, col):
        super().__init__('bishop', symbol, team, row, col, 3)
        self.moves = [
            [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7],
            [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7],
            [-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7],
            [-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]]


class Knight(Piece):
    def __init__(self, symbol, team, row, col):
        super().__init__('knight', symbol, team, row, col, 3)
        self.moves = [
            [-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2]]


class Pawn(Piece):
    def __init__(self, symbol, team, row, col):
        super().__init__('pawn', symbol, team, row, col, 1)
        self.moves = [
            [-1, 0], [-2, 0], [-1, 1], [-1, -1]]  # Up one cell, Up two cell, Up-right diagonal, Up-left diagonal

    def remove_two_step_move(self):
        if [2, 0] in self.moves:
            self.moves.remove([2, 0])
        if [-2, 0] in self.moves:
            self.moves.remove([-2, 0])


def in_check(_board, team: str) -> bool:

    # getting the moves of the other team

    moves = _board.get_all_allowed_moves(utils.get_opposite_team(team))

    # getting the king of own team
    team_king = None

    for row in _board.board:
        for _piece in row:
            if _piece != ' ':
                if _piece.name == 'king' and _piece.team == team:
                    team_king = _piece

    if team_king is None:
        for row in _board.board:
            print(row)

        raise Exception("King was None while attempting to check if team " + team + " is in check.")

    # iterating through all moves of the opposite team
    for move in moves:
        _, __, new_row, new_col = utils.parse_input(move)

        # if destination of any move matches king's coordinates
        if new_row == team_king.row and new_col == team_king.col:
            return True

    return False


def in_checkmate(_board, team: str):

    # cannot be in checkmate if not in check :)
    if not in_check(_board, team):
        return False


    # obtaining all moves of team
    moves = _board.get_all_allowed_moves(team)

    # for every move that a piece in the team can make
    for move in moves:
        temp = deepcopy(_board.board)
        temp_board = deepcopy(_board)
        temp_board.board = deepcopy(temp)

        # temporarily making that move
        res, _ = temp_board.move_piece(move, team, False)

        if res:
            # if move does not lead to check, it means checkmate is not possible as there is at least one way out
            if not in_check(temp_board, team):
                return False

    return True


def in_stalemate(_board, team: str):
    # cannot be in checkmate for a stalemate to occur

    if in_checkmate(_board, team):
        return False

    moves = _board.get_all_allowed_moves(team)

    for move in moves:
        temp = deepcopy(_board.board)
        temp_board = deepcopy(_board)
        temp_board.board = deepcopy(temp)

        # temporarily making that move
        temp_board.move_piece(move, team, False)

        # if there is such a move that leads out of check
        if not in_check(temp_board, team):
            return False

    return True





class ChessBoard:
    board = []
    size_ = 8

    attempting_castling_left = False


    attempting_castling_right = False



    def __init__(self, skip):
        if not skip:
            for i in range(self.size_):
                col = []
                for j in range(self.size_):
                    col.append(' ')

                self.board.append(col)

    # put initial pieces on the actual board





    def place_pieces(self):
        # placing black pieces on top of board (row 0 = 8)
        self.board[0][0] = Rook('♜', 'black', 0, 0)
        self.board[0][1] = Knight('♞', 'black', 0, 1)
        self.board[0][2] = Bishop('♝', 'black', 0, 2)
        self.board[0][3] = Queen('♛', 'black', 0, 3)
        self.board[0][4] = King('♚', 'black', 0, 4)
        self.board[0][5] = Bishop('♝', 'black', 0, 5)
        self.board[0][6] = Knight('♞', 'black', 0, 6)
        self.board[0][7] = Rook('♜', 'black', 0, 7)



        # placing black pawns
        for i in range(self.size_):
            p = Pawn('♟', 'black', 1, i)
            self.board[1][i] = deepcopy(p)



        # placing white pieces at bottom (row 7 = 1)
        self.board[7][0] = Rook('♖', 'white', 7, 0)

        self.board[7][1] = Knight('♘', 'white', 7, 1)

        self.board[7][2] = Bishop('♗', 'white', 7, 2)
        self.board[7][3] = Queen('♕', 'white', 7, 3)
        self.board[7][4] = King('♔', 'white', 7, 4)
        self.board[7][5] = Bishop('♗', 'white', 7, 5)
        self.board[7][6] = Knight('♘', 'white', 7, 6)
        self.board[7][7] = Rook('♖', 'white', 7, 7)

        # placing white pawns
        for i in range(self.size_):
            p = Pawn('♙', 'white', 6, i)
            self.board[6][i] = deepcopy(p)

    # get a copy of the board (all pieces and their attributes copied as well)
    def get_copy(self):
        b = []

        for i in range(self.size_):
            col = []
            for j in range(self.size_):
                col.append(' ')

            b.append(col)

        for row in range(self.size_):
            for col in range(self.size_):
                if self.board[row][col] != ' ':
                    b[row][col] = deepcopy(self.board[row][col].get_copy())


        return deepcopy(b)



    # change the points of a piece depending on its colour
    def update_points(self):


        for row in self.board:
            for _piece in row:
                if _piece != ' ':
                    _piece.points = -1 * _piece.points if _piece.team == 'black' else _piece.points

    # depending on colour, the moves have to be negated as the teams face opposite directions
    def update_moves(self):

        for row in self.board:
            for _piece in row:
                if _piece != ' ':
                    for move in _piece.moves:
                        for i in range(len(move)):
                            if _piece.team == 'black':
                                move[i] = 0 - move[i]

    ################################################### BOARD DISPLAY #################################################

    def get_display_lines(self):
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rows = ['8', '7', '6', '5', '4', '3', '2', '1']
        lines = []

        for i in range(self.size_):
            line = f'{rows[i]} '
            for j in range(self.size_):
                if self.board[i][j] == ' ':
                    square = '▢' if (i + j) % 2 == 0 else '▨'
                    line += square + ' '
                else:
                    line += self.board[i][j].symbol + ' '
            lines.append(line)

        # Add the column letters at the bottom
        bottom_line = '  '
        for letter in columns:
            bottom_line += f'{letter} '
        lines.append(bottom_line)

        return lines

    def display(self):
        for line in self.get_display_lines():
            print(line)

    ############################################## BOARD UTILITY METHODS ##############################################

    # check if coordinates are on the board
    def in_range(self, row: int, col: int):
        if 0 <= row < self.size_ and 0 <= col < self.size_:
            return True
        return False

    # check if a particular cell is empty
    def is_cell_empty(self, row: int, col: int):
        if self.board[row][col] == ' ':
            return True
        return False

    def team_at_destination(self, _piece: Piece, row: int, col: int) -> bool:
        if self.is_cell_empty(row, col):
            return False

        if self.get_piece(row, col).team == _piece.team:
            return True

        return False



    # check if there is a member of opposite team at destination
    def enemy_at_destination(self, _piece: Piece, row: int, col: int):
        if self.is_cell_empty(row, col):
            return False

        if self.get_piece(row, col).team != _piece.team:
            return True

        return False


    ###################################### GETTERS FOR BOARD/PIECES INFORMATION #######################################



    # list of all allowed moves for this board
    def get_all_allowed_moves(self, team: str):
        allowed_moves = []
        for row in self.board:
            for _piece in row:
                if _piece != ' ':
                    if _piece.team == team:
                        allowed_moves += _piece.get_allowed_moves(self)

        return allowed_moves

    # list of (row, column) positions of every piece of the specified team



    def get_team_positions(self, team: str):
        positions = []

        for row in self.board:
            for _piece in row:
                if _piece != ' ':
                    if _piece.team == team:
                        pos = (_piece.row, _piece.col)
                        positions.append(pos)

        return positions

    # get a piece at a cell
    def get_piece(self, row: int, col: int):
        return self.board[row][col]

    # get the team of the piece at specified coordinates
    def get_team(self, row: int, col: int):
        if self.is_cell_empty(row, col):
            return None

        return self.board[row][col].team

    # get the name of a piece at specified string coordinates
    def get_piece_name(self, pos):
        row, col = utils.parse_position(pos)
        return self.board[row][col].name

    ######################################## ALTERING BOARD METHODS ################################################

    def empty_cell(self, row: int, col: int):
        self.board[row][col] = ' '

    # put a piece at those indexes
    def put_piece(self, _piece, row: int, col: int):
        self.board[row][col] = _piece

    # perform the castle move
    def castle(self, king):
        if self.attempting_castling_right:
            self.attempting_castling_right = False

            rook = self.get_piece(king.row, king.col + 3)

            self.empty_cell(king.row, king.col)  # remove king
            self.empty_cell(rook.row, rook.col)  # remove right rook

            self.put_piece(king, king.row, king.col + 2)  # king two steps right
            self.put_piece(rook, rook.row, rook.col - 2)  # rook two steps left

            # update their index
            king.col = king.col + 2
            rook.col = rook.col - 2

        elif self.attempting_castling_left:
            self.attempting_castling_left = False

            rook = self.get_piece(king.row, king.col - 4)

            self.empty_cell(king.row, king.col)  # remove king
            self.empty_cell(rook.row, rook.col)  # remove right rook

            self.put_piece(king, king.row, king.col - 2)  # king two steps left
            self.put_piece(rook, rook.row, rook.col + 3)  # rook three steps right

            # update their index
            king.col = king.col - 2
            rook.col = rook.col + 3

    # transform a pawn to some other piece
    def transform_pawn(self, pawn, is_human_player):

        upgradable_pieces = ['knight', 'bishop', 'rook', 'queen']
        name = ""

        if is_human_player:
            print("\nYour pawn can now be upgraded!", end=' ')

            while name not in upgradable_pieces:
                name = input("Choose from knight, bishop, rook, queen: ")

        else:
            # AI pawn will be upgraded to a random piece
            idx = random.randint(0, len(upgradable_pieces) - 1)
            name = upgradable_pieces[idx]

        row = pawn.row
        col = pawn.col
        team = pawn.team

        if team == 'white':
            symbol = '♕'
        else:
            symbol = '♛'

        if name == 'knight':
            self.board[row][col] = Knight(symbol, team, row, col)

        elif name == 'bishop':
            self.board[row][col] = Bishop(symbol, team, row, col)

        elif name == 'rook':
            self.board[row][col] = Rook(symbol, team, row, col)

        elif name == 'queen':
            self.board[row][col] = Queen(symbol, team, row, col)

        else:
            pass

# CONSIDERING MOVES #

    def should_pawn_transform(self, _piece) -> bool:
        if _piece.name == 'pawn':

            if _piece.team == 'white':
                if _piece.row == 0:
                    return True

            elif _piece.team == 'black':
                if _piece.row == self.size_ - 1:
                    return False

    # check if a move is even possible for a specified piece
    def is_move_possible(self, _piece: Piece, new_row: int, new_col: int):
        difference_row = new_row - _piece.row
        difference_col = new_col - _piece.col

        if _piece.name == 'pawn':
            # pawn can only move diagonally if there is an enemy there
            if [difference_row, difference_col] in [[-1, 1], [-1, -1], [1, -1], [1, 1]]:
                if not self.enemy_at_destination(_piece, new_row, new_col):
                    return False

            # pawn cannot move forward if there is a piece at the destination
            if [difference_row, difference_col] in [[1, 0], [-1, 0], [2, 0], [-2, 0]]:
                if [difference_row, difference_col] in [[2, 0], [-2, 0]] and _piece.has_moved:
                    return False
                if not self.is_cell_empty(new_row, new_col):
                    return False

        if _piece.name == 'king':
            king_row = _piece.row
            king_col = _piece.col

            # king attempting castling
            if [difference_row, difference_col] in [[0, 2], [0, -2]]:

                # castling not possible if king has already moved
                if _piece.has_moved:
                    return False

                # right castle
                if difference_col == 2:
                    # cells between king and rook should be empty
                    if not self.is_cell_empty(king_row, king_col + 1) or not self.is_cell_empty(king_row, king_col + 2):
                        return False

                    # where the rook should be
                    rook_place = self.get_piece(king_row, self.size_ - 1)

                    # no rook at the supposed position
                    if rook_place == ' ' or rook_place.name != 'rook':
                        return False

                    # cannot castle if rook has moved
                    if rook_place.has_moved:
                        return False

                    self.attempting_castling_right = True
                    return True

                # left castle
                elif difference_col == -2:
                    # cells between king and rook should be empty
                    if not self.is_cell_empty(king_row, king_col - 1) or not self.is_cell_empty(king_row,
                                                                                                king_col - 2) or not self.is_cell_empty(
                            king_row, king_col - 3):
                        return False

                    # where the rook should be
                    rook_place = self.get_piece(king_row, king_col - 4)

                    # no rook at the supposed position
                    if rook_place == ' ' or rook_place.name != 'rook':
                        return False

                    # cannot castle if rook has moved
                    if rook_place.has_moved:
                        return False

                    self.attempting_castling_left = True
                    return True

        if [difference_row, difference_col] in _piece.moves:
            return True
        else:
            return False

    # check if there is a piece (of any team) blocking the path to destination
    def team_in_path(self, _piece: Piece, new_row: int, new_col: int):

        # knight can jump over any pieces in path
        if _piece.name == 'knight':
            return False

        difference_row = new_row - _piece.row
        difference_col = new_col - _piece.col

        # getting the ratio
        row_step = difference_row / abs(difference_row) if difference_row != 0 else 0
        row_step = int(row_step)
        col_step = difference_col / abs(difference_col) if difference_col != 0 else 0
        col_step = int(col_step)

        curr_row = deepcopy(_piece.row)
        curr_col = deepcopy(_piece.col)

        curr_row += row_step
        curr_col += col_step

        # if destination is at immediate next step and there is a piece there of the same team
        if curr_row == new_row and curr_col == new_col:
            if _piece.team == self.get_team(curr_row, curr_col):
                return True

        # incrementing so we can go through the whole path to destination, step by step
        while curr_row != new_row or curr_col != new_col:

            if not self.is_cell_empty(curr_row, curr_col):
                return True

            curr_row += row_step
            curr_col += col_step

        return False

# ACTUAL MOVEMENT METHOD #

    # move a piece from one cell to another
    def move_piece(self, move: str, team: str, is_human_player: bool):
        row, col, new_row, new_col = utils.parse_input(move)

        # creating a temporary board
        temp = self.get_copy()
        temp_board = ChessBoard(True)
        temp_board.board = deepcopy(temp)

        _piece = temp_board.board[row][col]

        if (row, col) in self.get_team_positions(utils.get_opposite_team(team)):
            if is_human_player:
                print("\nCannot move a piece of the opposite team.")
            return False, None

        if row is None or col is None or new_row is None or new_col is None:
            if is_human_player:
                print("\nError parsing input.")
            return False, None

        if not self.in_range(new_row, new_col):
            if is_human_player:
                print("\nDestination out of range.")
            return False, None

        if self.is_cell_empty(row, col):
            if is_human_player:
                print("\nThere is no piece to move at the selected cell.")
            return False, None

        if not self.is_move_possible(_piece, new_row, new_col):
            if is_human_player:
                print("\nPiece at selected cell cannot move to the specified location.")
            return False, None

        if self.team_at_destination(_piece, new_row, new_col):
            if is_human_player:
                print("\nIllegal move. There is a friendly piece at the destination.")
            return False, None

        if self.team_in_path(_piece, new_row, new_col):
            if is_human_player:
                print("\nIllegal Move. There is a friendly piece in the path.")
            return False, None

        # trying left castling on temp board
        if self.attempting_castling_left:
            temp_board.attempting_castling_left = True
            temp_board.castle(_piece)

        # trying right castling on temp board
        if self.attempting_castling_right:
            temp_board.attempting_castling_right = True
            temp_board.castle(_piece)

        # trying any other move on temp board
        else:
            temp_board.empty_cell(row, col)
            temp_board.put_piece(_piece, new_row, new_col)
            temp_board.board[new_row][new_col].update_indexes(new_row, new_col)

        # if the movement leads to check
        if in_check(temp_board, team):
            # if this player was already in check
            if in_check(self, team):
                if is_human_player:
                    print("\nYou cannot make a move that keeps your King in check.")
            else:
                if is_human_player:
                    print("\nYou cannot make a move that puts your King into check.")
            return False, None

        # mark piece as moves
        if not _piece.has_moved:
            _piece.has_moved = True

            # once pawn has moved, it should no longer be allowed to do two step move
            if _piece.name == 'pawn':
                _piece.remove_two_step_move()

        # update actual board
        _piece = self.board[row][col]

        # castle left
        if self.attempting_castling_left:
            self.castle(_piece)

        # castle right
        elif self.attempting_castling_right:
            self.castle(_piece)

        # perform any other move
        else:
            self.empty_cell(row, col)
            self.put_piece(_piece, new_row, new_col)

            # update the piece attributes
            _piece.update_indexes(new_row, new_col)
            _piece.has_moved = True

        # check if pawn should be transformed to another piece (if it reaches end of board)
        if self.should_pawn_transform(_piece):
            self.transform_pawn(_piece, is_human_player)

        return True, _piece.name
