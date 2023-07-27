import numpy as np

def update_v(t, gen, pop_v, pop_x, g_best, V, pop, pbest):
    w_max = 0.9
    w_min = 0.4
    w = w_min + ((w_max - w_min) * (gen - t)) / gen
    C1 = 2.5 + (0.5 - 2.5) * t / gen
    C2 = 0.5 + (2.5 - 0.5) * t / gen
    
    for i in range(pop):
        for j in range(V):
            print('III', pop_v.shape, pbest.shape, g_best.shape,pop_x.shape, i, j)
            pop_v[i, j] = w * pop_v[i, j] + C1 * np.random.rand() * (pbest[j] - pop_x[i, j]) + C2 * np.random.rand() * (g_best[0,j] - pop_x[i, j])
    
    V = pop_v
    
    return V