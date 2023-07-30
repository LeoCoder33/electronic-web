import numpy as np
import random
from datetime import datetime
from initial import initial
from mokuaihanshu import mokuaihanshu
from gbest_fitness import gbest_fitness
from update_v import update_v
from non_domination_sort_mod import non_domination_sort_mod
from replace_chromosome import replace_chromosome
from pf_optimal import pf_optimal

def optimize_function(Z, S_load, Xmin, Xmax, P_pv, T):
    # parameter setting
    pop = 5
    gen = 30
    M = 4
    V = Z.shape[0]
    g_best = np.zeros((gen, V))
    pop_num = 50
    lamda = 0.5
    N = T
    # main function body
    Data = np.array([1])
    while Data.size > 0:
        pop_x = np.zeros((pop, V+M))
        pop_v = np.zeros((pop, V))
        pbest = np.zeros((pop, V))
        pbest_value = np.zeros(pop)
        gbest = np.zeros((pop, V))
        gbest_value = np.zeros(pop)
        change_x = np.zeros((pop, V+M))
        change_v = np.zeros((pop, V))
        migle_x = np.zeros((pop, V+M))
        
        tic = datetime.now()
        format_short = np.short
        

        
        # pop_x, pop_v = initial(pop, V, M, P_pv, Z, S_load, Xmin, Xmax, N)
        pop_x, pop_v = initial(pop, V, M, P_pv, Z, S_load, Xmin, Xmax.reshape((Xmax.shape[1],)), N)
        todayDate = datetime.now().strftime("%y-%m-%d-%H-%M")
        Xmax.reshape((Xmax.shape[1],))
        for t in range(1, gen+1):
            Gbest_value = np.zeros(pop)
            R = np.zeros(pop)
            g_best_value = np.zeros((gen, M))
            g_best = np.zeros((gen, V))
            # 寻找全局最优
            pbest, pbest_value, k = gbest_fitness(pop_x, V, M, pop)
            g_best[t-1,:] = pbest
            g_best_value[t-1,:] = pbest_value
            g_best_value1 = np.zeros(t)
            for i in range(t):
                g_best_value1[i] = g_best_value[i,0]/(1e5) + g_best_value[i,1]/700 + g_best_value[i,2]/7 + 10000*g_best_value[i,3]
            R = np.argsort(g_best_value1)
            Fit, index = np.sort(R), np.argsort(R)
            gbest = g_best[index,:]
            
            change_v = update_v(t, gen, pop_v, pop_x[:,:V], g_best, V, pop, pbest)
            pop_v = change_v
            
            change_x = pop_x[:, :V] + change_v
            change_x = np.concatenate((change_x, np.zeros((pop, M))), axis=1)
            for i in range(pop):
                for j in range(V):
                    if change_x[i, j] > Xmax[0, j]:
                        change_x[i, j] = random.randint(Xmin[j], Xmax[0, j])
                    elif change_x[i, j] < Xmin[j]:
                        change_x[i, j] = random.randint(Xmin[j], Xmax[0, j])
            
            for i in range(pop):
                change_x[i, V:V+M] = mokuaihanshu(pop_x[i, :].reshape(1,-1), pop, M, V, P_pv, Z, S_load, N)
            
            y1, x1 = pop_x.shape
            y2, x2 = change_x.shape

            migle_x[:y1,:] = pop_x
            migle_x = np.concatenate((migle_x, np.zeros((y2, x1))), axis=0)
            migle_x[y1:y1+y2, :x2] = change_x

            migle_x = non_domination_sort_mod(migle_x, M, V)

            pop_x = replace_chromosome(migle_x, M, V, pop)

            Ploss = pop_x[:, V] / 1e9
            Cost = pop_x[:, V+1] / 1e6
            print('优化迭代第{}轮'.format(t))

            A = np.argmax(g_best_value[:,3] == np.min(g_best_value[:,3]))
            U3 = np.zeros((V, T))
            for t in range(T):
                U3[:, t], _, _ = pf_optimal(g_best[A,:], P_pv, Z, S_load1[:,t], V)

            Count = np.zeros(V)
            for i in range(V):
                for j in range(T):
                    if U3[i, j] < 0.95 or U3[i, j] > 1.05:
                        Count[i] += 1
            Data = np.where(Count > 0)[0]
    # 返回最终结果
    return pop_x