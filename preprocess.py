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


def winner(game):
    """
    Returns who is the winner, if draw return 'd'
    
    Inputs:
        game: A chess game[PGN]
    Outputs:
        winner: White('w') / Black('b') / Draw('d')
    """
    if game.headers['Result'] == '1-0':
        return 'w'
    elif game.headers['Result'] == '0-1':
        return 'b'
    return 'd'


def pgn2fen(game):
    """
    Returns all positions[FEN] and moves[SAN] from game[PGN]
    
    Inputs:
        game: A chess game[PGN]
    Outputs:
        positions: All positions of game[List of FEN]
        moves: All moves that led to the positions[List of SAN]
    """
    node = game
    positions = []
    moves = []
    
    # All positions and moves until the game ends
    while not node.is_end():
        nextNode = node.variation(0)
        move = node.board().san(nextNode.move)
        position = nextNode.board().fen()
        moves.append(move)
        positions.append(position)
        node = nextNode
    return positions, moves



