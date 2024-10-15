from copy import deepcopy
import gc
import torch
from torch.utils.data import Dataset

__all__ = [
    'DataManager',
    'TensorDataset'
    ]

class DataManager(object):
    def __init__(self, X, Y):
        self.X     = X
        self.Y     = Y

    def __len__(self):
        return len(self.Y)
    
    def __getitem__(self, index):
        return self.X[index], self.Y[index]

class TensorDataset(Dataset):
    def __init__(self, dataset):
        self.X = torch.FloatTensor(dataset.X)
        self.Y = torch.LongTensor(dataset.Y)

    def __len__(self):
        return len(self.Y)

    def __getitem__(self, index):
        data   = self.X[index]
        target = self.Y[index]
        return data, target