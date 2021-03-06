#!/usr/bin/env python
# coding: utf-8

from tensorflow import keras
import numpy as np
import h5py


class DataGenerator(keras.utils.Sequence):
    
    def __init__(self, filePath, first, size, batchSize=64, shuffle=True):
        """
        Initialization for DataGenerator class
        """
        self.filePath = filePath
        self.first = first
        self.size = size
        self.batchSize = batchSize
        self.shuffle = shuffle
        self.onEpochEnd()
        
    def __len__(self):
        """
        Calculates the number of batches per epoch
        """
        return self.size // self.batchSize
        
    def __getitem__(self, index):
        """
        Generate one batch of data
        """
        with h5py.File(self.filePath, 'r') as file:
            batchBitboards = file['bitboards'][index * self.batchSize : (index + 1) * self.batchSize]
            batchLabels = file['labels'][index * self.batchSize : (index + 1) * self.batchSize]
            return batchBitboards, batchBitboards
    
    def onEpochEnd(self):
        self.indexes = np.arange(self.size)
        if self.shuffle:
            np.random.shuffle(self.indexes)




