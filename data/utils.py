
from copy import deepcopy
import sys, gc
import numpy as np

from memory_profiler import profile
from data.types import DataManager
import data.config as cfg


"""
For memory trace
"""
# @profile
def load_raw_trainset(dataset, n_shots, dataset_operation=None):# -> DataManager:
    X = np.load(f'./dataset/{dataset}/x_train.npy') # (75455, 1, 1800) float64
    Y = np.load(f'./dataset/{dataset}/y_train.npy') # (75455, ) int32

    if dataset_operation == "benchmark":
        X = X[:1]
        Y = Y[:1]
        return DataManager(X, Y)
    
    idxs_n_shots = []
    for i in range(cfg.N_CLASS[dataset]):
        idxs_n_shot = np.random.choice(np.where(Y==i)[0], n_shots, replace=False).tolist()
        idxs_n_shots.extend(idxs_n_shot)
    
    X = X[idxs_n_shots]
    Y = Y[idxs_n_shots]

    del idxs_n_shot
    del idxs_n_shots
    
    trainset = DataManager(X, Y)
    # del X
    # del Y
    return trainset

def load_raw_testset(dataset, dataset_operation=None):# -> DataManager:
    X = np.load(f'./dataset/{dataset}/x_test.npy') # (18864, 1, 1800)
    Y = np.load(f'./dataset/{dataset}/y_test.npy') # (18864,)
    if dataset_operation == "downsample":
        X = X[:, :, ::2]
    testset = DataManager(X, Y)
    return testset

# @profile
def load_raw_trainset_and_select_n_shots_per_class(dataset, n_shots, dataset_operation=None):# -> tuple[DataManager, DataManager]:
    trainset = load_raw_trainset(dataset, n_shots, dataset_operation)
    # trainset = select_n_shots_per_class(trainset, dataset, n_shots)
    return trainset

# @profile
def load_raw_and_select_n_shots_per_class(dataset, n_shots, dataset_operation=None):# -> tuple[DataManager, DataManager]:
    trainset = load_raw_trainset(dataset, n_shots, dataset_operation)
    # trainset = select_n_shots_per_class(trainset, dataset, n_shots)
    testset = load_raw_testset(dataset, dataset_operation)
    return trainset, testset

"""End"""

def load_raw_dataset(path="./dataset", dataset='mitbih_arr'):# -> tuple[DataManager, DataManager]:
    X = np.load(f'{path}/{dataset}/x_train.npy') # (75455, 1, 1800) float64
    Y = np.load(f'{path}/{dataset}/y_train.npy') # (75455, ) int32
    trainset = DataManager(X, Y)
    X = np.load(f'{path}/{dataset}/x_test.npy') # (18864, 1, 1800)
    Y = np.load(f'{path}/{dataset}/y_test.npy') # (18864,)
    testset = DataManager(X, Y)
    return trainset, testset

# @profile
def select_n_shots_per_class(trainset, dataset, n_shots, dataset_operation=None):# -> DataManager:
    """
    From the trainset, choose n_shots samples for each class.
    """
    
    idxs_n_shots = []
    for i in range(cfg.N_CLASS[dataset]):
        
        idxs_n_shot = np.random.choice(np.where(trainset.Y==i)[0], n_shots, replace=False).tolist()
        idxs_n_shots.extend(deepcopy(idxs_n_shot))
    
    trainset.X = trainset.X[idxs_n_shots]
    trainset.Y = trainset.Y[idxs_n_shots]
    del idxs_n_shot
    del idxs_n_shots
    
    if dataset_operation == "coreset":
        # Coreset sampling
        pass
    return trainset