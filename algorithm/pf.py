import numpy as np
from fitness import fitness

def pf(x, M, P_pv, Z, S_load, V, N):
    np.set_printoptions(precision=4)

    # 读取IEEE69节点算例的参数
    # 线路数据
    Z = np.hstack((Z, S_load))
    N_line = Z.shape[0]
    # 节点数据
    N_bus = V

    # 找到负荷节点
    load = np.abs(Z[:, 3])
    Nload = np.where(load != 0)[0]  # 找到对应负荷不为0的编号

    # 计算相关参数标幺值
    Sb = 100                       # 基准功率100MVA
    Vb = 12.66                     # 基准电压12.66Kv
    Zb = Vb**2 / Sb                # 基准阻抗Zb
    Z[:, 2] /= Zb                 # 计算节点阻抗的标幺值
    tmp = Z[:, 3]
    tmp = tmp.reshape((len(tmp), 1))
    tmp = (tmp - x.T.dot(P_pv) - 1j * 10 * x.T.dot(P_pv) * np.tan(np.arccos(0.9))) / (Sb * 1000)  # 计算加入分布式电源后系统容量的标幺值，在这里直接用功率因数来折算无功
    Z[:,3] = tmp[:,0]
    U =np.ones((V, 1)).astype(complex)   # 设置电压初始值

    # 使用前推回代法计算配电网潮流
    for t in range(1, 201):  # 设置迭代次数
        tmp = Z[:, 3]
        tmp = tmp.reshape((len(tmp), 1))
        I = (tmp.T) @ np.diag(1/U[:,0])  # 节点注入电流
        I = I.T  # 转为列向量
        I1 = I  # 节点注入电流列向量
        for k in range(N_bus, 0, -1):  # 后推电流
            A = np.where(Z[:, 0] == k)[0]
            if len(A) != 0:  # 找到末节点号
                I[k, 0] = np.sum(I[A, 0]) + I[k, 0]
        
        U[0, 0] = 1 - Z[0, 2] * I[0, 0]  # 前推电压
        for L in range(1, N_line):
            B = np.where(Z[:, 1] == L)[0]  # 找到支路号
            temp = Z[B, 0]
            tempInt = int(temp.real)
            U[L, 0] = U[tempInt, 0] - Z[B, 2] * I[B, 0]
            
        dS = Z[:, 3] - ((np.diag(U[:, 0])).conj() @ I1[:, 0])  # 节点功率不平衡量
        dP = dS.real  # 实部
        dQ = dS.imag  # 虚部
        dPQ = np.vstack((dP, dQ))
        
        if np.max(np.abs(dPQ)) < 0.000001:
            break
        else:
            t += 1  # 迭代次数

    s = np.zeros((N_line, 1)).astype(complex)  # 线路容量
    for k in range(N_bus, 0, -1):  # 后推线路容量
        A = np.where(Z[:, 0] == k)[0]
        if len(A) == 0:  # 找到末节点号
            temp = Z[k-1, 3] + (np.real(Z[k-1, 3]) ** 2 + np.imag(Z[k-1, 3]) ** 2) * Z[k-1, 2] / (U[k-1, 0] ** 2)
            s[k-1, 0] = temp
        else:
            a = Z[k-1, 3] + np.sum(s[A, 0])
            temp =  a + (np.real(a) ** 2 + np.imag(a) ** 2) * Z[k-1, 2] / (U[k-1, 0] ** 2) 
            s[k-1, 0] = temp
    
    I = np.abs(I) * Sb / Vb * 1000  # 节点注入电流
    U = np.abs(U)  # 节点电压幅值
    Pg = np.sum(x)  # 分布式电源安装总容量
    
    ploss, Cost, dU, dup = fitness(I, Z, Pg, U, Nload, V)  # 计算目标函数的值
    
    fit = []
    if M == 2:
        fit.append(ploss)
        fit.append(Cost)
    elif M == 3:
        fit.append(ploss)
        fit.append(Cost)
        fit.append(dU)
    elif M == 4:
        fit.append(ploss)
        fit.append(Cost)
        fit.append(dU)
        fit.append(dup)
    
    fit = np.array(fit)
    # fit = fit.reshape((1, len(fit)))
    return fit