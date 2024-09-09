import math
import random

# Function to convert row, col into chess notation ('a', 1)
def get_chess_position(position):
    if 0 <= position[1] < 8 and 0 <= position[0] < 8:  # Ensure it's within bounds
        return (chr(position[1] + 97), position[0] + 1)
    return None  # Invalid position

# Convert chess notation like ('a', 1) to numeric indices (0, 0)
def chess_position_to_position(chess_position):
    if isinstance(chess_position[0], int):  # Already numeric
        return chess_position
    return (chess_position[1] - 1, ord(chess_position[0]) - 97)

# Ensure position is valid within 0-7 range
def is_valid_position(position):
    row, col = position
    return 0 <= row < 8 and 0 <= col < 8

# Piece class definition
class Piece:
    def __init__(self, colour, position, piece_type):
        self.colour = colour
        self.position = chess_position_to_position(position)
        self.piece_type = piece_type
        self.max_rows = 8
        self.max_cols = 8

    def get_traversals(self):
        if self.piece_type == "King":
            return [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        elif self.piece_type == "Queen":
            return [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        elif self.piece_type == "Knight":
            return [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        elif self.piece_type == "Bishop":
            return [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        elif self.piece_type == "Rook":
            return [(0, -1), (-1, 0), (1, 0), (0, 1)]
        elif self.piece_type == "Pawn":
            if self.colour == "White":
                return [(1, 0)]
            else:
                return [(-1, 0)]
        else:
            return []


class Rook(Piece):
    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():  # Traversals: straight lines
            row, col = self.position[0] + traversal[0], self.position[1] + traversal[1]
            while is_valid_position((row, col)):
                if get_chess_position((row, col)) not in gameboard:  # Empty square
                    res.append((get_chess_position(self.position), get_chess_position((row, col))))
                else:
                    if gameboard[get_chess_position((row, col))][1] == self.colour:
                        break  # Friendly piece blocking the way
                    else:
                        res.append((get_chess_position(self.position), get_chess_position((row, col))))  # Capture opponent
                        break  # Stop after capturing
                row += traversal[0]  # Continue in the same direction
                col += traversal[1]
        return res

    def get_piece_score(self):
        return 5


class Queen(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            while is_valid_position((row, col)):
                if get_chess_position((row, col)) not in gameboard:
                    res.append((get_chess_position(self.position), get_chess_position((row, col))))
                else:
                    if gameboard[get_chess_position((row, col))][1] == self.colour:
                        break
                    else:
                        res.append((get_chess_position(self.position), get_chess_position((row, col))))
                        break
                row += traversal[0]
                col += traversal[1]
        return res

    def get_piece_score(self):
        return 9

class King(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            if is_valid_position((row, col)):
                if get_chess_position((row, col)) not in gameboard:
                    res.append((get_chess_position(self.position), get_chess_position((row, col))))
                else:
                    if gameboard[get_chess_position((row, col))][1] != self.colour:
                        res.append((get_chess_position(self.position), get_chess_position((row, col))))
        return res

    def get_piece_score(self):
        return 100

class Knight(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            if is_valid_position((row, col)):
                if get_chess_position((row, col)) not in gameboard:
                    res.append((get_chess_position(self.position), get_chess_position((row, col))))
                else:
                    if gameboard[get_chess_position((row, col))][1] != self.colour:
                        res.append((get_chess_position(self.position), get_chess_position((row, col))))
        return res

    def get_piece_score(self):
        return 3

class Bishop(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            while is_valid_position((row, col)):
                if get_chess_position((row, col)) not in gameboard:
                    res.append((get_chess_position(self.position), get_chess_position((row, col))))
                else:
                    if gameboard[get_chess_position((row, col))][1] == self.colour:
                        break
                    else:
                        res.append((get_chess_position(self.position), get_chess_position((row, col))))
                        break
                row += traversal[0]
                col += traversal[1]
        return res

    def get_piece_score(self):
        return 3

class Pawn(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def getValidMoves(self, gameboard):
        res = []
        direction = 1 if self.colour == "White" else -1
        row, col = self.position

        if (row + direction, col) not in gameboard:
            res.append(((row, col), (row + direction, col)))

        if (self.colour == "White" and row == 1) or (self.colour == "Black" and row == 6):
            if (row + direction, col) not in gameboard and (row + 2 * direction, col) not in gameboard:
                res.append(((row, col), (row + 2 * direction, col)))

        for diag in [-1, 1]:
            new_row, new_col = row + direction, col + diag
            if 0 <= new_col < self.max_cols and (new_row, new_col) in gameboard:
                if gameboard[(new_row, new_col)][1] != self.colour:
                    res.append(((row, col), (new_row, new_col)))

        return res

    def get_piece_score(self):
        return 1

# Function to create a piece object based on its type
def makePiece(piece, colour, position):
    if piece == 'Rook':
        return Rook(colour, position, piece)
    elif piece == 'Knight':
        return Knight(colour, position, piece)
    elif piece == 'Bishop':
        return Bishop(colour, position, piece)
    elif piece == 'Queen':
        return Queen(colour, position, piece)
    elif piece == 'King':
        return King(colour, position, piece)
    elif piece == 'Pawn':
        return Pawn(colour, position, piece)
    else:
        print(f"Unknown piece type: {piece} at {position}. Ignoring.")
        return None  # Handle unknown pieces

class State:
    def __init__(self, gameboard, turn, depth):
        self.gameboard = {k: v for k, v in gameboard.items() if is_valid_position(chess_position_to_position(k))}  # Only valid positions
        self.turn = turn
        self.depth = depth
        self.is_terminal = self.check_terminal_state()
        print(f"State initialized for {turn} with depth {depth} and valid board: {self.gameboard}")

    def check_terminal_state(self):
        kings = 0
        for position, piece in self.gameboard.items():
            if piece[0] == 'King':
                kings += 1
        return kings < 2

    def get_all_moves(self):
        res = []
        for position, piece in self.gameboard.items():
            piece_obj = makePiece(piece[0], piece[1], get_chess_position(position))
            if piece_obj:  # Check if piece_obj is not None
                res.extend(piece_obj.getValidMoves(self.gameboard))
            else:
                print(f"Skipping unknown piece {piece[0]} at {position}.")
        return res

    def generate_successors(self):
        res = []
        for move in self.get_all_moves():
            start_pos = chess_position_to_position(move[0])
            end_pos = chess_position_to_position(move[1])
            if is_valid_position(end_pos):  # Ensure the move is within bounds
                new_gameboard = self.gameboard.copy()
                new_gameboard[end_pos] = new_gameboard[start_pos]
                del new_gameboard[start_pos]
                next_turn = 'Black' if self.turn == 'White' else 'White'
                res.append((State(new_gameboard, next_turn, self.depth - 1), move))
        return res

    def get_score(self):
        score = 0
        for position, piece in self.gameboard.items():
            temp = makePiece(piece[0], piece[1], get_chess_position(position))
            if piece[1] == 'White':
                score += temp.get_piece_score()
            else:
                score -= temp.get_piece_score()
        return score

def maximize(state, depth, alpha, beta):
    if depth == 0 or state.is_terminal:
        return state.get_score(), None

    score = -math.inf
    best_move = None
    for new_state, move in state.generate_successors():
        curr_score, _ = minimize(new_state, depth - 1, alpha, beta)
        if curr_score > score:
            score = curr_score
            best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return score, best_move

def minimize(state, depth, alpha, beta):
    if depth == 0 or state.is_terminal:
        return state.get_score(), None

    score = math.inf
    best_move = None
    for new_state, move in state.generate_successors():
        curr_score, _ = maximize(new_state, depth - 1, alpha, beta)
        if curr_score < score:
            score = curr_score
            best_move = move
        beta = min(beta, score)
        if alpha >= beta:
            break
    return score, best_move

def Agent3070(gameboard, is_black_turn):
    turn = "Black" if is_black_turn else "White"
    print(f"Evaluating gameboard for {turn}:")
    
    # Filtering only Black pieces when it is Black's turn
    gameboard = {pos: piece for pos, piece in gameboard.items() if piece[1] == turn}
    
    move = maximize(State(gameboard, turn, 3), 3, -math.inf, math.inf)[1]
    
    print(f"Generated move: {move}")
    return move

# Example main function
def main():
    gameboard = {
        ('a', 1): ('Rook', 'White'), ('b', 1): ('Knight', 'White'),
        ('c', 1): ('Bishop', 'White'), ('d', 1): ('Queen', 'White'), ('e', 1): ('King', 'White'),
        ('f', 1): ('Bishop', 'White'), ('g', 1): ('Knight', 'White'), ('h', 1): ('Rook', 'White'),
        ('a', 2): ('Pawn', 'White'), ('b', 2): ('Pawn', 'White'), ('c', 2): ('Pawn', 'White'),
        ('d', 2): ('Pawn', 'White'), ('e', 2): ('Pawn', 'White'), ('f', 2): ('Pawn', 'White'),
        ('g', 2): ('Pawn', 'White'), ('h', 2): ('Pawn', 'White'),
        ('a', 7): ('Pawn', 'Black'), ('b', 7): ('Pawn', 'Black'), ('c', 7): ('Pawn', 'Black'),
        ('d', 7): ('Pawn', 'Black'), ('e', 7): ('Pawn', 'Black'), ('f', 7): ('Pawn', 'Black'),
        ('g', 7): ('Pawn', 'Black'), ('h', 7): ('Pawn', 'Black'),
        ('a', 8): ('Rook', 'Black'), ('b', 8): ('Knight', 'Black'), ('c', 8): ('Bishop', 'Black'),
        ('d', 8): ('Queen', 'Black'), ('e', 8): ('King', 'Black'), ('f', 8): ('Bishop', 'Black'),
        ('g', 8): ('Knight', 'Black'), ('h', 8): ('Rook', 'Black'),
    }

    is_black_turn = False  # Set this based on the current turn
    move = Agent3070(gameboard, is_black_turn)
    print(f"Move generated by engine_3070: {move}")

if __name__ == "__main__":
    main()
