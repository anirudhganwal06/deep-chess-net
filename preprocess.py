#!/usr/bin/env python
# coding: utf-8

import numpy as np
import chess 
import chess.pgn
import random
import h5py


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
    if len(chosenPositions) > nPositions:
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


def fen2bitboard(fen):
    """
    Returns bitboard [np array of shape(1, 773)] from fen
    
    Input:
        fen: A chessboard position[FEN]
    Output:
        bitboard: A chessboard position [bitboard - np array of shape(1, 773)]
    """
    mapping = {
        'p': 0,
        'n': 1,
        'b': 2,
        'r': 3,
        'q': 4,
        'k': 5,
        'P': 6,
        'N': 7,
        'B': 8,
        'R': 9,
        'Q': 10,
        'K': 11
    }
    bitboard = np.zeros((1, 773), dtype=int)
    currIndex = 0
    [position, turn, castling, _, _, _] = fen.split(' ')
    for ch in position:
        if ch == '/':
            continue
        elif ch >= '1' and ch <= '8':
            currIndex += (ord(ch) - ord('0')) * 12
        else:
            bitboard[0, currIndex + mapping[ch]] = 1
            currIndex += 12
    bitboard[0, 768] = 1 if turn == 'w' else 0
    bitboard[0, 769] = 1 if 'K' in castling else 0
    bitboard[0, 770] = 1 if 'Q' in castling else 0
    bitboard[0, 771] = 1 if 'k' in castling else 0
    bitboard[0, 772] = 1 if 'q' in castling else 0
    return bitboard


def saveData(filePath, bitboards, labels):
    """
    Save data to a .h5 file
    
    Inputs:
        filePath: the path with file name to which processed data will be saved
        bitboards: np array of processed bitboards
        labels: np array of processed labels
    """
    with h5py.File(filePath, 'w') as file:
        print(f'Bitboards shape: {bitboards.shape}')
        print(f'Labels shape: {labels.shape}')
        file.create_dataset('bitboards', data = bitboards, maxshape = (None, 773))
        file.create_dataset('labels', data = labels, maxshape = (None, 1))


def iterateOverAllGames(pgnFilePath):
    """
    Iterate over all games of pgnFile and returns some good positions from those games
    
    Inputs:
        pgnFilePath: path of the file where pgn games are stored
    Outputs:
        bitboards: chessboard positions [np array of shape(None, 773)]
        labels: labels of corresponding bitboards - winner [np array of shape(None, 1)]
    """
    pgnFile = open(pgnFilePath)
    game = chess.pgn.read_game(pgnFile)
    bitboards = np.ndarray((0, 773))
    labels = np.ndarray((0, 1))
    count = 0
    
    
    while game is not None:
        win = winner(game)
        if win in ['w', 'b']:
            positions, moves = pgn2fen(game)
            positions = choosePositions(positions, moves)
            for position in positions:
                bitboard = fen2bitboard(position)
                label = 1 if win == 'w' else 0
                label = np.array([[label]])
                bitboards = np.append(bitboards, bitboard, axis = 0)
                labels = np.append(labels, label, axis = 0)
                count += 1
                if count % 100 == 0:            
                    appendDataToH5File('./datasets/processed1.h5', bitboards, labels)
                    print(f'{count} positions saved')
                    bitboards = bitboards[100:]
                    labels = labels[100:]
                    
        game = chess.pgn.read_game(pgnFile)   
    appendDataToH5File('./datasets/processed1.h5', bitboards, labels)
    print(f'{count} positions saved')
    return bitboards, labels


def createH5File(filePath):
    with h5py.File(filePath, 'a') as file:
        file.create_dataset('bitboards', shape=(0, 773), maxshape=(None, 773))
        file.create_dataset('labels', shape=(0, 1), maxshape=(None, 1))