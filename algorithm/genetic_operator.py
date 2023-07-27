import numpy as np

def genetic_operator(parent_chromosome, M, V, mu, mum, Xmax, Xmin):
    N, m = parent_chromosome.shape
    
    child = []
    p = 0
    was_crossover = False
    was_mutation = False
    
    for i in range(N):
        if np.random.rand() < 0.9:
            child_1 = np.empty(V)
            child_2 = np.empty(V)
            
            parent_1 = np.round(N * np.random.rand())
            if parent_1 < 1:
                parent_1 = 1
            parent_2 = np.round(N * np.random.rand())
            if parent_2 < 1:
                parent_2 = 1
            
            while np.array_equal(parent_chromosome[parent_1], parent_chromosome[parent_2]):
                parent_2 = np.round(N * np.random.rand())
                if parent_2 < 1:
                    parent_2 = 1
            
            parent_1 = parent_chromosome[parent_1]
            parent_2 = parent_chromosome[parent_2]
            
            for j in range(V):
                u = np.random.rand()
                if u <= 0.5:
                    bq = (2 * u) ** (1 / (mu + 1))
                else:
                    bq = (1 / (2 * (1 - u))) ** (1 / (mu + 1))
                
                child_1[j] = 0.5 * (((1 + bq) * parent_1[j]) + (1 - bq) * parent_2[j])
                child_2[j] = 0.5 * (((1 - bq) * parent_1[j]) + (1 + bq) * parent_2[j])
                
                # 控制变量约束
                if child_1[j] > Xmax:
                    child_1[j] = Xmax
                elif child_1[j] < Xmin:
                    child_1[j] = Xmin
                
                # 控制变量约束
                if child_2[j] > Xmax:
                    child_2[j] = Xmax
                elif child_2[j] < Xmin:
                    child_2[j] = Xmin
            
            child_1 = np.concatenate((child_1, mokuaihanshu(child_1, V, M)))
            child_2 = np.concatenate((child_2, mokuaihanshu(child_2, V, M)))
            
            was_crossover = True
            was_mutation = False
        
        else:
            parent_3 = np.round(N * np.random.rand())
            if parent_3 < 1:
                parent_3 = 1
            
            child_3 = parent_chromosome[parent_3].copy()
            
            for j in range(V):
                r = np.random.rand()
                if r < 0.5:
                    delta = (2 * r) ** (1 / (mum + 1)) - 1
                else:
                    delta = 1 - (2 * (1 - r)) ** (1 / (mum + 1))
                
                child_3[j] += delta
                
                # 控制变量约束
                if child_3[j] > Xmax:
                    child_3[j] = Xmax
                elif child_3[j] < Xmin:
                    child_3[j] = Xmin
            
            child_3 = np.concatenate((child_3[:M+V], mokuaihanshu(child_3, V, M)))
            
            was_mutation = True
            was_crossover = False
        
        if was_crossover:
            child.append(child_1)
            child.append(child_2)
            p += 2
        elif was_mutation:
            child.append(child_3)
            p += 1
    
    return np.array(child)