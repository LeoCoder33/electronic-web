import numpy as np

def fitness(I, Z, Pg, U, Nload, V):
    # 输入目标函数基本参数
    C1 = 0.12
    C2 = 0.18
    n = 20
    r = 0.1
    Ue = 1
    Up = 0.05
    Umin = 0.95
    Umax = 1.05
    F1 = 0
    F2 = 0
    
    # 总有功网损目标函数
    sloss = np.sum(np.abs(I[:V, 0])**2 * Z[:V, 2])
    ploss = np.real(sloss)
    
    # 总投资与运行成本目标函数
    Cost = ((r * (1 + r)**n) / ((1 + r)**n - 1) * C1 + C2) * Pg * 10
    
    # 电压安全稳定性目标函数
    dU = np.sum(((U[Nload] - Ue) / Up)**2)
    
    # 节点电压约束
    Uminm = Umin - U[:V, 0]
    Umaxm = U[:V, 0] - Umax
    F1 = np.sum(100000 * np.maximum(Uminm, 0)**2)
    F2 = np.sum(100000 * np.maximum(Umaxm, 0)**2)
    
    # 安装总容量约束
    xsum = Pg - 380
    F3 = 100000 * max(xsum, 0)**2
    
    # 罚函数
    dup = F1 + F2 + F3
    
    return ploss, Cost, dU, dup