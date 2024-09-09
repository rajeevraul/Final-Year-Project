import subprocess
import chess
from engine_3070 import Agent3070  # Importing the other engine

# Start Sunfish as a subprocess (Sunfish runs as a separate process)
def start_sunfish():
    return subprocess.Popen(
        ['python3', 'sunfish.py'],  # This runs Sunfish as an external process
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

# Send UCI commands to Sunfish and capture the response
def send_sunfish_command(engine, command):
    engine.stdin.write(command + '\n')
    engine.stdin.flush()
    response = ''
    while True:
        line = engine.stdout.readline().strip()
        if line.startswith('bestmove'):
            break
        response += line + '\n'
    return response, line

# Get the best move from Sunfish
def get_sunfish_move(board, engine):
    moves = ' '.join([move.uci() for move in board.move_stack])
    command = f'position startpos moves {moves}'
    send_sunfish_command(engine, command)  # Send the board position to Sunfish
    response, bestmove = send_sunfish_command(engine, 'go')  # Ask Sunfish for a move
    move_str = bestmove.split(' ')[1].strip()  # Get the best move from Sunfish
    return chess.Move.from_uci(move_str)

# 3070 Engine's move
def get_3070_move(board):
    gameboard = convert_board_to_3070_format(board)
    is_black_turn = not board.turn  # Black's turn if board.turn is False
    move = Agent3070(gameboard, is_black_turn)

    if move:
        from_square = chess.parse_square(move[0][0] + str(move[0][1]))
        to_square = chess.parse_square(move[1][0] + str(move[1][1]))
        if board.piece_at(from_square) and board.piece_at(from_square).color == chess.BLACK:
            return chess.Move(from_square, to_square)
        else:
            print(f"Invalid move by 3070: expected Black to move, but got {move}.")
            return None
    return None

# Play game between Sunfish (White) and 3070 (Black)
async def play_sunfish_vs_3070():
    board = chess.Board()
    move_count = 0
    
    # Start Sunfish engine
    sunfish_engine = start_sunfish()
    
    while not board.is_game_over() and move_count < 100:
        if board.turn == chess.WHITE:
            # Sunfish's turn (White)
            sunfish_move = get_sunfish_move(board, sunfish_engine)
            print(f"Sunfish (White) move: {sunfish_move}")
            if sunfish_move and sunfish_move in board.legal_moves:
                board.push(sunfish_move)
            else:
                print("Invalid move by Sunfish!")
                break
        else:
            # 3070's turn (Black)
            other_engine_move = get_3070_move(board)
            print(f"3070 (Black) move: {other_engine_move}")
            if other_engine_move and other_engine_move in board.legal_moves:
                board.push(other_engine_move)
            else:
                print("Invalid move by 3070!")
                break

        move_count += 1
        print(board)

    # Terminate Sunfish engine after game ends
    sunfish_engine.terminate()

    print(f"Game stopped after {move_count} moves.")

if __name__ == "__main__":
    asyncio.run(play_sunfish_vs_3070())
