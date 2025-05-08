# AI Chess Game with Minimax and Alpha-Beta Pruning

## Project Overview

This project implements a chess game with an AI opponent using the minimax algorithm with alpha-beta pruning. The implementation focuses on efficient move evaluation and decision-making.

## Implementation Logic

### 1. Chess Board Representation

The chess board is represented as an 8x8 grid where each cell contains a piece object or an empty space. The board state is managed by the `grid_state.py` module, which:

- Initializes the board with pieces in their standard starting positions
- Tracks the current state of the game (whose turn, if in check, etc.)
- Validates moves according to chess rules
- Handles special moves like castling and en passant
- Detects check and checkmate conditions

### 2. Piece Movement Logic

Each chess piece is implemented as an object with properties that define:
- Its type (pawn, knight, bishop, rook, queen, king)
- Its color (white or black)
- Its current position on the board
- Its movement patterns

The `element.py` module defines these piece objects and their movement capabilities. The movement validation ensures that:
- Pieces only move according to their specific rules
- Pieces cannot move through other pieces (except knights)
- Pieces cannot move in ways that leave their king in check
- Special moves follow the standard chess rules

### 3. AI Decision Making

The AI uses the minimax algorithm with alpha-beta pruning to select its moves. This is implemented in `game_runner.py`:

#### Minimax Algorithm
- The AI evaluates the board position by assigning a numerical score
- It looks ahead a specified number of moves (depth)
- For each possible move, it simulates the move and evaluates the resulting position
- It alternates between maximizing (AI's moves) and minimizing (opponent's moves) the score
- The algorithm returns the move that leads to the best evaluated position

#### Alpha-Beta Pruning
- Alpha-beta pruning optimizes the minimax algorithm by eliminating branches that won't affect the final decision
- It maintains two values: alpha (best already explored option for maximizer) and beta (best already explored option for minimizer)
- When beta becomes less than or equal to alpha, the algorithm can stop exploring that branch
- This significantly reduces the number of positions that need to be evaluated

### 4. Position Evaluation

The AI evaluates board positions using a combination of:
- Material value (piece values: pawn=1, knight/bishop=3, rook=5, queen=9)
- Position value (using piece-square tables from `utils.py`)
- Piece mobility (number of legal moves available)
- King safety (distance from the center, protection)

The evaluation function in `utils.py` calculates a numerical score for the current board state, with positive values favoring white and negative values favoring black.

### 5. Move Generation and Selection

The AI generates all legal moves for the current position and evaluates each one:
1. For each piece, it calculates all possible destination squares
2. It filters out illegal moves (those that would leave the king in check)
3. It applies the minimax algorithm to evaluate each move
4. It selects the move with the highest evaluation score

### 6. User Interface

The game interface allows players to:
- View the current board state
- Input moves using standard chess notation (e.g., 'e2e4')
- See the AI's responses and evaluations
- Track the game state (whose turn, if in check, etc.)

## Key Functions and Their Implementation

### AI Functions (`game_runner.py`)

#### `max_value(self, _board, depth, team, alpha, beta)`
- **Purpose**: Implements the maximizing player's move evaluation in the minimax algorithm
- **Parameters**:
  - `_board`: Current board state
  - `depth`: How many moves ahead to look
  - `team`: Current player's team (white/black)
  - `alpha`: Best value that maximizer can guarantee
  - `beta`: Best value that minimizer can guarantee
- **Process**:
  1. If depth is 0, evaluate the current position and return
  2. Initialize value to negative infinity and best_move to None
  3. Get all legal moves for the current position
  4. For each move:
     - Make a copy of the board
     - Apply the move
     - Recursively call min_value with reduced depth
     - Update value and best_move if a better move is found
     - Update alpha
     - Prune if beta <= alpha
  5. Return the best value and move found

#### `min_value(self, _board, depth, team, alpha, beta)`
- **Purpose**: Implements the minimizing player's move evaluation in the minimax algorithm
- **Parameters**: Same as max_value
- **Process**: Similar to max_value but:
  - Initializes value to positive infinity
  - Updates value when a lower value is found
  - Updates beta instead of alpha
  - Prunes when beta <= alpha

#### `minimax(self, _board)`
- **Purpose**: Entry point for the minimax algorithm
- **Parameters**: `_board`: Current board state
- **Process**:
  1. Initialize alpha to negative infinity and beta to positive infinity
  2. Call max_value or min_value depending on the AI's team
  3. Return the best move found

#### `move(self, _board)`
- **Purpose**: Executes the AI's move on the board
- **Parameters**: `_board`: Current board state
- **Process**:
  1. Get the best move using minimax
  2. Convert the move to the proper format
  3. Apply the move to the board
  4. Return True if successful, False otherwise

### Utility Functions (`utils.py`)

#### `get_board_evaluation(_board)`
- **Purpose**: Evaluates the current board position
- **Parameters**: `_board`: Current board state
- **Process**:
  1. Initialize value to 0
  2. For each piece on the board:
     - Add the piece's material value
     - Add the piece's position value based on piece-square tables
  3. Return the total evaluation (positive favors white, negative favors black)

#### `get_piece_evaluation(_piece)`
- **Purpose**: Evaluates a piece's position on the board
- **Parameters**: `_piece`: The piece to evaluate
- **Process**:
  1. Get the piece's position (row, col)
  2. Look up the position value in the appropriate piece-square table
  3. For black pieces, mirror and invert the table
  4. Return the position value

#### `parse_input(move)`
- **Purpose**: Converts chess notation to board coordinates
- **Parameters**: `move`: Move in chess notation (e.g., 'e2e4')
- **Process**:
  1. Validate the move format
  2. Extract source and target squares
  3. Convert file (a-h) to column index (0-7)
  4. Convert rank (1-8) to row index (7-0)
  5. Return the coordinates as (curr_row, curr_col, new_row, new_col)

#### `un_parse_input(curr_row, curr_col, new_row, new_col)`
- **Purpose**: Converts board coordinates to chess notation
- **Parameters**: Coordinates of the move
- **Process**:
  1. Convert row and column indices to chess notation
  2. Return the move as a string (e.g., 'e2e4')

### Board Management Functions (`grid_state.py`)

#### `move_piece(self, move, team, is_human)`
- **Purpose**: Moves a piece on the board
- **Parameters**:
  - `move`: Move in chess notation
  - `team`: Team making the move
  - `is_human`: Whether the move is made by a human
- **Process**:
  1. Parse the move to get coordinates
  2. Validate that the move is legal
  3. Update the board state
  4. Handle special moves (castling, en passant, pawn promotion)
  5. Check for check and checkmate
  6. Return True if successful, False otherwise

#### `get_all_allowed_moves(self, team)`
- **Purpose**: Gets all legal moves for a team
- **Parameters**: `team`: Team to get moves for
- **Process**:
  1. Initialize an empty list of moves
  2. For each piece of the specified team:
     - Get all possible destination squares
     - Filter out illegal moves
     - Add legal moves to the list
  3. Return the list of legal moves

## Technical Implementation Details

### Key Components

1. **Board Representation**: 2D array with piece objects
2. **Move Validation**: Rule-based validation for each piece type
3. **AI Algorithm**: Minimax with alpha-beta pruning
4. **Position Evaluation**: Material + position + mobility + king safety
5. **Move Generation**: Legal move generation for all pieces

### Performance Considerations

- The search depth parameter balances between AI strength and response time
- Alpha-beta pruning significantly improves performance by reducing the search space
- Position evaluation tables are pre-calculated for efficiency
- Move generation is optimized to avoid unnecessary calculations

## Results and Limitations

The implemented AI:
- Can play a complete game of chess following standard rules
- Makes decisions based on material advantage and positional factors
- Can look ahead several moves to anticipate opponent's strategies
- Has limitations in long-term planning and complex positional play
- Performance varies based on the search depth parameter

## Future Improvements

Potential enhancements include:
- Opening book integration for better early game play
- More sophisticated evaluation functions
- Iterative deepening for time management
- Transposition table for caching evaluated positions
- Multi-threading for parallel position evaluation 