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
        
    def __len__(self):
        """
        Calculates the number of batches per epoch
        """
        return self.size // batchSize