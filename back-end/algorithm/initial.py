import numpy as np
from mokuaihanshu import mokuaihanshu

def initial(pop, V, M, P_pv, Z, S_load, Xmin, Xmax, N):
    pop_x = np.zeros((pop, V+M))  # 粒子的位置初始种群
    pop_v = np.zeros((pop, V))  # 粒子的速度初始种群
    
    print(Xmin.shape, Xmax.shape)
    for i in range(pop):  # 初始化种群的个体
        for j in range(V):
            pop_x[i, j] = np.random.randint(Xmin[j], Xmax[j]+1) # 随机初始化位置
            pop_v[i, j] = np.random.randn()  # 随机初始化速度

    for i in range(pop):
        temp = pop_x[i, :]
        result = mokuaihanshu(temp.reshape((1, len(temp))), pop, M, V, P_pv, Z, S_load, N)  # 求出各个体的目标函数值
        pop_x[i, V:V+M] = result
    
    return pop_x, pop_v