import numpy as np

def non_domination_sort_mod(X, M, V):
    N, m = X.shape[0], X.shape[1] # 获取种群大小N和决策变量个数m
    x = np.zeros((N, m + 1)) # 初始化新的种群
    x[:, 0:m] = X # 将原始种群复制到新的种群中

    front = 1
    F = []
    F.insert(front-1, {'f': []})
    individual = [] 

    for i in range(N):
        individual.append({'n': 0, 'p': []})

        for j in range(N):
            dom_less = 0
            dom_equal = 0
            dom_more = 0

            for k in range(M):
                if x[i, V + k] < x[j, V + k]:
                    dom_less += 1
                elif x[i, V + k] == x[j, V + k]:
                    dom_equal += 1
                else:
                    dom_more += 1

            if dom_less == 0 and dom_equal != M:
                individual[i]['n'] += 1
            elif dom_more == 0 and dom_equal != M:
                individual[i]['p'].append(j)

        if individual[i]['n'] == 0:
            x[i, M + V] = 1
            print('front-1', front-1, F)
            F[front-1]['f'].append(i)

    while len(F[front-1]['f']) != 0:
        Q = []

        for i in range(len(F[front-1]['f'])):
            if len(individual[F[front-1]['f'][i]]['p']) != 0:
                for j in range(len(individual[F[front-1]['f'][i]]['p'])):
                    individual[individual[F[front-1]['f'][i]]['p'][j]]['n'] -= 1

                    if individual[individual[F[front-1]['f'][i]]['p'][j]]['n'] == 0:
                        x[individual[F[front-1]['f'][i]]['p'][j], M + V] = front + 1
                        Q.append(individual[F[front-1]['f'][i]]['p'][j])

        front += 1
        F.append({'f': Q})


    temp = np.argsort(x[:, M + V])
    sorted_based_on_front = x[temp, :]
    current_index = 0
    z = np.zeros((1000, 24))

    for front in range(len(F) - 1):
        distance = 0
        y = []
        previous_index = current_index + 1

        for i in range(len(F[front]['f'])):
            y.append(sorted_based_on_front[current_index + i, :])

        current_index += i
        sorted_based_on_objective = np.array([])

        y = np.array(y)
        [Y1, Y2] = y.shape
        Y = np.zeros((Y1, M + V + M))
        Y[:, 0:Y2] = y
        y = Y
        for i in range(M):
            sorted_based_on_objective, index_of_objectives = np.sort(y[:, V + i]), np.argsort(y[:, V + i])
            sorted_based_on_objective = []

            for j in range(len(index_of_objectives)):
                sorted_based_on_objective.append(y[index_of_objectives[j], :])
            sorted_based_on_objective = np.array(sorted_based_on_objective)

            f_max = sorted_based_on_objective[len(index_of_objectives)-1, V + i]
            f_min = sorted_based_on_objective[0, V + i]
            
            y[index_of_objectives[len(index_of_objectives)-1], M + V + i] = np.inf
            y[index_of_objectives[0], M + V + i] = np.inf

            for j in range(1, len(index_of_objectives) - 1):
                next_obj = sorted_based_on_objective[j+1, V + i]
                previous_obj = sorted_based_on_objective[j - 1, V + i]

                if f_max - f_min == 0:
                    y[index_of_objectives[j], M + V + i] = np.inf
                else:
                    y[index_of_objectives[j], M + V + i] = (next_obj - previous_obj) / (f_max - f_min)

        distance = np.zeros((len(F[front]['f']), 1))

        for i in range(M):
            distance[:, 0] += y[:, M + V + i]


        y[:, M + V + 2] = np.ravel(distance)
        y = y[:, :M + V + 2]
        z[previous_index-1:current_index+1, :] = y

    f = z
    return f