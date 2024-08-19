import math
import random
import sys

def get_chess_position(position):
    return (chr(position[1] + 97), position[0])

class Piece:
    top_left = (-1, -1)
    top = (0, -1)
    top_right = (1, -1)
    left = (-1, 0)
    right = (1, 0)
    bottom_left = (-1, 1)
    bottom = (0, 1)
    bottom_right = (1, 1)

    def __init__(self, colour, position, piece_type):
        self.colour = colour
        self.position = self.chess_position_to_position(position)
        self.piece_type = piece_type
        self.max_rows = 8
        self.max_cols = 8

    def getColour(self):
        return self.colour

    def getPosition(self):
        return self.position

    def getPieceType(self):
        return self.piece_type

    def get_position(self):
        return self.position

    def get_chess_position(self):
        return (chr(self.position[1] + 97), self.position[0])

    @staticmethod
    def chess_position_to_position(chess_position):
        return (chess_position[1], ord(chess_position[0]) - 97)

    def get_traversals(self):
        if self.piece_type == "King":
            return [self.top_left, self.top, self.top_right, self.left, self.right, self.bottom_left, self.bottom, self.bottom_right]
        elif self.piece_type == "Queen":
            return [self.top_left, self.top, self.top_right, self.left, self.right, self.bottom_left, self.bottom, self.bottom_right]
        elif self.piece_type == "Knight":
            return [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        elif self.piece_type == "Bishop":
            return [self.top_left, self.top_right, self.bottom_left, self.bottom_right]
        elif self.piece_type == "Rook":
            return [self.top, self.left, self.right, self.bottom]
        elif self.piece_type == "Pawn":
            if self.colour == "White":
                return [(1, 0)]
            else:
                return [(-1, 0)]
        else:
            return []

    def getValidMoves(self, gameboard):
        pass

    def get_piece_score(self):
        if self.piece_type == "King":
            return 400
        elif self.piece_type == "Queen":
            return 8.375
        elif self.piece_type == "Knight":
            return 3
        elif self.piece_type == "Bishop":
            return 3.375
        elif self.piece_type == "Rook":
            return 5
        elif self.piece_type == "Pawn":
            return 1
        else:
            return 0


class Queen(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            while 0 <= row < self.max_rows and 0 <= col < self.max_cols:
                if get_chess_position((row, col)) not in gameboard:
                    res.append((get_chess_position(
                        (self.position[0], self.position[1])), get_chess_position((row, col))))
                else:
                    if gameboard[get_chess_position((row, col))][1] == self.colour:
                        break
                    else:
                        res.append((get_chess_position(
                            (self.position[0], self.position[1])), get_chess_position((row, col))))
                        break
                row += traversal[0]
                col += traversal[1]
        return res


class King(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            if 0 <= row < self.max_rows and 0 <= col < self.max_cols:
                if get_chess_position((row, col)) not in gameboard:
                    res.append((get_chess_position(
                        (self.position[0], self.position[1])), get_chess_position((row, col))))
                elif get_chess_position((row, col)) in gameboard:
                    if gameboard[get_chess_position((row, col))][1] != self.colour:
                        res.append((get_chess_position(
                            (self.position[0], self.position[1])), get_chess_position((row, col))))
        return res


class Knight(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            if 0 <= row < self.max_rows and 0 <= col < self.max_cols:
                if get_chess_position((row, col)) not in gameboard:
                    res.append((get_chess_position(
                        (self.position[0], self.position[1])), get_chess_position((row, col))))
                elif get_chess_position((row, col)) in gameboard:
                    if gameboard[get_chess_position((row, col))][1] != self.colour:
                        res.append((get_chess_position(
                            (self.position[0], self.position[1])), get_chess_position((row, col))))
        return res


class Bishop(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            while 0 <= row < self.max_rows and 0 <= col < self.max_cols:
                if get_chess_position((row, col)) not in gameboard:
                    res.append((get_chess_position(
                        (self.position[0], self.position[1])), get_chess_position((row, col))))
                else:
                    if gameboard[get_chess_position((row, col))][1] == self.colour:
                        break
                    else:
                        res.append((get_chess_position(
                            (self.position[0], self.position[1])), get_chess_position((row, col))))
                        break
                row += traversal[0]
                col += traversal[1]
        return res


class Rook(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            while 0 <= row < self.max_rows and 0 <= col < self.max_cols:
                if get_chess_position((row, col)) not in gameboard:
                    res.append((get_chess_position(
                        (self.position[0], self.position[1])), get_chess_position((row, col))))
                else:
                    if gameboard[get_chess_position((row, col))][1] == self.colour:
                        break
                    else:
                        res.append((get_chess_position(
                            (self.position[0], self.position[1])), get_chess_position((row, col))))
                        break
                row += traversal[0]
                col += traversal[1]
        return res


class Pawn(Piece):
    def __init__(self, colour, position, piece_type):
        super().__init__(colour, position, piece_type)

    def get_diagonals(self):
        if self.colour == "White":
            return [(1, 1), (1, -1)]
        else:
            return [(-1, 1), (-1, -1)]

    def getValidMoves(self, gameboard):
        res = []
        for traversal in self.get_traversals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            if 0 <= row < self.max_rows and 0 <= col < self.max_cols:
                if get_chess_position((row, col)) not in gameboard:
                    res.append((get_chess_position(
                        (self.position[0], self.position[1])), get_chess_position((row, col))))

        for traversal in self.get_diagonals():
            row = self.position[0] + traversal[0]
            col = self.position[1] + traversal[1]
            if 0 <= row < self.max_rows and 0 <= col < self.max_cols:
                if get_chess_position((row, col)) in gameboard:
                    if gameboard[get_chess_position((row, col))][1] != self.colour:
                        res.append((get_chess_position(
                            (self.position[0], self.position[1])), get_chess_position((row, col))))
        return res
    
def makePiece(piece, colour, position):
    if piece == 'King':
        return King(colour, position, piece)
    elif piece == 'Queen':
        return Queen(colour, position, piece)
    elif piece == 'Rook':
        return Rook(colour, position, piece)
    elif piece == 'Bishop':
        return Bishop(colour, position, piece)
    elif piece == 'Knight':
        return Knight(colour, position, piece)
    elif piece == 'Pawn':
        return Pawn(colour, position, piece)
    
class State():
    def __init__(self, gameboard, turn, depth):
        self.gameboard = gameboard
        self.turn = turn
        self.depth = depth
        self.is_terminal = self.check_terminal_state()

    def getGameboard(self):
        return self.gameboard

    def getTurn(self):
        return self.turn

    def get_all_moves(self):
        res = []
        for position, piece in self.gameboard.items():
            if piece[1] == self.turn:
                piece = makePiece(piece[0], piece[1], position)
                res.extend(piece.getValidMoves(self.gameboard))
        return res
    
    def get_self_threatening_moves(self):
        res = []
        for move in self.get_all_moves():
            if move[1] in self.gameboard:
                res.append(move)
        return len(res)
    
    def get_white_threatening_moves(self, colour):
        new_state = State(self.gameboard, colour, self.depth)
        return new_state.get_self_threatening_moves()
    
    def get_black_threatening_moves(self, colour):
        new_state = State(self.gameboard, colour, self.depth)
        return new_state.get_self_threatening_moves()

    def get_opponent_threatening_moves(self):
        new_state = State(self.gameboard, self.opposite_colour(), self.depth)
        return new_state.get_self_threatening_moves()

    def get_all_moves_for_piece(self, piece):
        return piece.getValidMoves(self.gameboard)

    def get_all_pieces(self):
        res = []
        for position, piece in self.gameboard.items():
            res.append(makePiece(piece[0], piece[1], position))
        return res
    
    def check_terminal_state(self):
        kings = 0
        for position, piece in self.gameboard.items():
            if piece[0] == 'King':
                kings += 1
        if kings == 2:
            return False
        else:
            return True
    
    def out_of_moves(self):
        for position, piece in self.gameboard.items():
            self_pieces = 0
            if piece[1] == self.turn:
                self_pieces += 1
        if self_pieces == 0:
            return True
        elif self_pieces == 1 and len(self.get_all_moves()) == 0:
            return True
        return False
    def generate_successors(self):
        res = []
        king_capture_moves = []
        queen_capture_moves = []
        rook_capture_moves = []
        bishop_capture_moves = []
        knight_capture_moves = []
        pawn_capture_moves = []

        for move in self.get_all_moves():
            new_gameboard = self.gameboard.copy()
            new_gameboard[move[1]] = new_gameboard[move[0]]
            del new_gameboard[move[0]]
            if self.turn == 'White':
                if move[1] in self.gameboard:
                    if self.gameboard[move[1]][0] == 'King':
                        king_capture_moves.append((State(new_gameboard, 'Black', self.depth - 1), move))
                    elif self.gameboard[move[1]][0] == 'Queen':
                        queen_capture_moves.append((State(new_gameboard, 'Black', self.depth - 1), move))
                    elif self.gameboard[move[1]][0] == 'Rook':
                        rook_capture_moves.append((State(new_gameboard, 'Black', self.depth - 1), move))
                    elif self.gameboard[move[1]][0] == 'Bishop':
                        bishop_capture_moves.append((State(new_gameboard, 'Black', self.depth - 1), move))
                    elif self.gameboard[move[1]][0] == 'Knight':
                        knight_capture_moves.append((State(new_gameboard, 'Black', self.depth - 1), move))
                    elif self.gameboard[move[1]][0] == 'Pawn':
                        pawn_capture_moves.append((State(new_gameboard, 'Black', self.depth - 1), move))
                    else:
                        res.insert(0, (State(new_gameboard, 'Black', self.depth - 1), move))
                else:
                    res.append((State(new_gameboard, 'Black', self.depth - 1), move))
            else:
                if move[1] in self.gameboard:
                    if self.gameboard[move[1]][0] == 'King':
                        king_capture_moves.append((State(new_gameboard, 'White', self.depth - 1), move))
                    elif self.gameboard[move[1]][0] == 'Queen':
                        queen_capture_moves.append((State(new_gameboard, 'White', self.depth - 1), move))
                    elif self.gameboard[move[1]][0] == 'Rook':
                        rook_capture_moves.append((State(new_gameboard, 'White', self.depth - 1), move))
                    elif self.gameboard[move[1]][0] == 'Bishop':
                        bishop_capture_moves.append((State(new_gameboard, 'White', self.depth - 1), move))
                    elif self.gameboard[move[1]][0] == 'Knight':
                        knight_capture_moves.append((State(new_gameboard, 'White', self.depth - 1), move))
                    elif self.gameboard[move[1]][0] == 'Pawn':
                        pawn_capture_moves.append((State(new_gameboard, 'White', self.depth - 1), move))
                    else:
                        res.insert(0, (State(new_gameboard, 'White', self.depth - 1), move))
                else:
                    res.append((State(new_gameboard, 'White', self.depth - 1), move))
        res = king_capture_moves + queen_capture_moves + rook_capture_moves + bishop_capture_moves + knight_capture_moves + pawn_capture_moves + res
        return res
    
    def opposite_colour(self):
        if self.turn == 'White':
            return 'Black'
        else:
            return 'White'
    
    def get_score(self):
        score = 0
        for position, piece in self.gameboard.items():
            if piece[1] == 'White':
                temp = makePiece(piece[0], piece[1], position)
                score += temp.get_piece_score()
            else:
                temp = makePiece(piece[0], piece[1], position)
                score -= temp.get_piece_score()
        return score
    
def maximize(state, depth, alpha, beta):
    best_move = None
    if depth == 0 or state.is_terminal:
        return state.get_score(), best_move
    score = -math.inf
    new_states = state.generate_successors()
    for new_state, move in new_states:
        curr_score, _ = minimize(new_state, depth - 1, alpha, beta)
        if curr_score > score:
            score = curr_score
            best_move = move
        alpha = max(alpha, score)
        if curr_score >= beta:
            break
    return score, best_move

def minimize(state, depth, alpha, beta):
    best_move = None
    if depth == 0 or state.is_terminal:
        return state.get_score(), best_move
    score = math.inf
    new_states = state.generate_successors()
    for new_state, move in new_states:
        curr_score, _ = maximize(new_state, depth - 1, alpha, beta)
        if curr_score < score:
            score = curr_score
            best_move = move
        beta = min(beta, score)
        if curr_score <= alpha:
            break
    return score, best_move
    

def studentAgent(gameboard):
    d = random.choice([2, 3])
    move = maximize(State(gameboard, 'White', d), d, -math.inf, math.inf)[1]

    return move

# board = {
#     ('a', 1) : ('Rook', 'White'), ('b', 1) : ('Knight', 'White'), ('c', 1) : ('Bishop', 'White'), ('d', 1) : ('Queen', 'White'), ('e', 1) : ('King', 'White'), ('f', 1) : ('Bishop', 'White'), ('g', 1) : ('Knight', 'White'), ('h', 1) : ('Rook', 'White'),
#     ('a', 2) : ('Pawn', 'White'), ('b', 2) : ('Pawn', 'White'), ('c', 2) : ('Pawn', 'White'), ('d', 2) : ('Pawn', 'White'), ('e', 2) : ('Pawn', 'White'), ('f', 2) : ('Pawn', 'White'), ('g', 2) : ('Pawn', 'White'), ('h', 2) : ('Pawn', 'White'),
#     ('a', 7) : ('Pawn', 'Black'), ('b', 7) : ('Pawn', 'Black'), ('c', 7) : ('Pawn', 'Black'), ('d', 7) : ('Pawn', 'Black'), ('e', 7) : ('Pawn', 'Black'), ('f', 7) : ('Pawn', 'Black'), ('g', 7) : ('Pawn', 'Black'), ('h', 7) : ('Pawn', 'Black'),
#     ('a', 8) : ('Rook', 'Black'), ('b', 8) : ('Knight', 'Black'), ('c', 8) : ('Bishop', 'Black'), ('d', 8) : ('Queen', 'Black'), ('e', 8) : ('King', 'Black'), ('f', 8) : ('Bishop', 'Black'), ('g', 8) : ('Knight', 'Black'), ('h', 8) : ('Rook', 'Black')
# }
