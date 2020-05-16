#!/usr/bin/env python
# coding: utf-8

import numpy as np
import chess 
import chess.pgn
import random


def choosePositions(positions, moves, nExcludeStarting = 5, nPositions = 10):
    """
    Returns positions that will be used in our model
    
    Inputs:
        positions: List of all chessboard positions of a game in FEN format
        moves: List of all moves that led to the given positions
        nExcludeStarting: Number of positions not to choose at the start of the game
        nPositions: Number of random positions to choose from a single game
    Outputs:
        chosenPositions: list of randomly chosen positions out of all positions 
    """
    # Remove nExcludeStarting number of moves from start of the match
    chosenPositions = positions[nExcludeStarting:]
    chosenMoves = moves[nExcludeStarting:]
    
    # Choose all positions which were not led by any capture
    chosenPositions = [chosenPositions[i] for i in range(len(chosenMoves)) if 'x' not in chosenMoves[i]]
    
    # Select nPositions random positions from chosenPositions
    chosenPositions = random.sample(chosenPositions, k = nPositions)
    
    return chosenPositions







