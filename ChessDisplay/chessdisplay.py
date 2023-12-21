# @author Seth Stemen
# A visualizer for a game of chess between two human players, on a Novation Launchpad Mk2.

import sys
from pygame import time
import chess

# Import launchpad_py library
try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("error loading launchpad.py")


def main():
    # Initialize launchpad
    # Project currently only supports Launchpad Mk2 (as that is the only launchpad I own and can test on)
    if launchpad.LaunchpadMk2().Check(0):
        lp = launchpad.LaunchpadMk2()
        if lp.Open(0, "mk2"):
            print("Launchpad Mk2")
            mode = "Mk2"
    else:
        sys.exit("Failed to find a compatible Launchpad")

    lp.ButtonFlush()

    # Initialize Chess Logic
    board = chess.Board()
    print(board)

    # Provide list of legal moves on each turn
    legal_moves = [
        board.san(move)
        for move in board.legal_moves
    ]
    print(legal_moves)



if __name__ == "__main__":
    main()
