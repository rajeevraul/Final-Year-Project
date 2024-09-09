import asyncio
import chess
from engine_3070 import Agent3070  # Importing the other engine

# Function to convert chess.Board to the format required by engine_3070
def convert_board_to_3070_format(board):
    gameboard = {}
    piece_map = {
        'R': 'Rook', 'N': 'Knight', 'B': 'Bishop', 'Q': 'Queen', 'K': 'King', 'P': 'Pawn',
        'r': 'Rook', 'n': 'Knight', 'b': 'Bishop', 'q': 'Queen', 'k': 'King', 'p': 'Pawn'
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_type = piece_map.get(piece.symbol())
            color = 'White' if piece.color == chess.WHITE else 'Black'
            gameboard[(chess.square_file(square), chess.square_rank(square))] = (piece_type, color)
    
    return gameboard

async def get_sunfish_move(board):
    """
    Get a move from Sunfish (White).
    """
    print("Getting move for Sunfish (White).")
    send_sunfish_position(board)
    send_sunfish_go()
    sunfish_output = await get_sunfish_move_output()  # Simulating engine output capture
    return parse_sunfish_move(sunfish_output)

def get_3070_move(board):
    gameboard = convert_board_to_3070_format(board)
    is_black_turn = not board.turn  # Black's turn if board.turn is False

    # Ensure that Agent3070 only moves Black pieces during Black's turn
    move = Agent3070(gameboard, is_black_turn)

    if move:
        from_square = chess.parse_square(move[0][0] + str(move[0][1]))
        to_square = chess.parse_square(move[1][0] + str(move[1][1]))

        # Check if the piece at from_square is Black, because it should be Black's move
        if board.piece_at(from_square) and board.piece_at(from_square).color == chess.BLACK:
            return chess.Move(from_square, to_square)
        else:
            print(f"Invalid move by 3070: expected Black to move, but got {move}.")
            return None
    return None
def send_sunfish_position(board):
    moves = ' '.join([move.uci() for move in board.move_stack])
    print(f"position startpos moves {moves}")  # Example position command for Sunfish

def send_sunfish_go():
    print("go")  # Example go command to tell Sunfish to search for a move

async def get_sunfish_move_output():
    """
    Simulates reading the output from the Sunfish engine after sending 'go'.
    """
    await asyncio.sleep(1)  # Simulate waiting time for engine response
    return "bestmove e2e4"  # Replace with the actual move returned by Sunfish engine

def parse_sunfish_move(engine_output):
    """
    Parse the move from Sunfish engine's 'bestmove' output.
    """
    try:
        move_str = engine_output.split('bestmove ')[1].strip()
        return chess.Move.from_uci(move_str)
    except Exception as e:
        print(f"Error parsing Sunfish move: {e}")
        return None

async def play_sunfish_vs_3070():
    board = chess.Board()
    move_count = 0

    while not board.is_game_over() and move_count < 100:
        if board.turn == chess.WHITE:
            # Sunfish's turn (White)
            print("Sunfish's turn.")
            sunfish_move = await get_sunfish_move(board)
            print(f"Sunfish (White) move: {sunfish_move}")
            if sunfish_move and sunfish_move in board.legal_moves:
                board.push(sunfish_move)
            else:
                print("Invalid move by Sunfish!")
                break
        else:
            # 3070's turn (Black)
            print("3070's turn.")
            other_engine_move = get_3070_move(board)
            print(f"3070 (Black) move: {other_engine_move}")
            if other_engine_move and other_engine_move in board.legal_moves:
                board.push(other_engine_move)
            else:
                print("Invalid move by 3070!")
                break

        move_count += 1
        print(board)

    print(f"Game stopped after {move_count} moves.")

if __name__ == "__main__":
    asyncio.run(play_sunfish_vs_3070())
