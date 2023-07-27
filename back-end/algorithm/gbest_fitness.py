import numpy as np

def gbest_fitness(X, V, M, pop):
    # 基于小生境技术的多目标全局寻优
    k = np.random.rand(1) + 1
    Data = X[:, V:V+M]
    
    Data1 = Data[:, 0] / (1e5) + Data[:, 1] / (700) + Data[:, 2] / (7) + 10000 * Data[:, 3]
    
    R = np.argsort(Data1)
    index = np.argsort(R)
    
    gbest = X[index[0], 0:V]
    gbest_value = X[index[0], V:V+M]
    
    return gbest, gbest_value, k