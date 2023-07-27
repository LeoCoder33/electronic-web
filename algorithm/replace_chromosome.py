import numpy as np

def replace_chromosome(intermediate_chromosome, M, V, pop):
    print('intermediate_chromosome', intermediate_chromosome[:, M + V])
    N, m = intermediate_chromosome.shape
    
    # Get the index for the population sort based on the rank
    index = np.argsort(intermediate_chromosome[:, M + V])
    
    sorted_chromosome = np.zeros((N, m))
    for i in range(N):
        sorted_chromosome[i, :] = intermediate_chromosome[index[i], :]
    # Find the maximum rank in the current population
    max_rank = np.max(intermediate_chromosome[:, M + V]).astype(int)
    previous_index = 0
    for i in range(1, max_rank + 1):
        current_index = np.max(np.where(sorted_chromosome[:, M + V + 1] == i))
        if current_index > pop:
            remaining = pop - previous_index
            temp_pop = sorted_chromosome[previous_index:current_index, :]
            temp_sort_index = np.argsort(temp_pop[:, M + V + 1])[::-1]
            for j in range(remaining):
                f[previous_index + j, :] = temp_pop[temp_sort_index[j], :]
            return f
        elif current_index < pop:
            f[previous_index:current_index, :] = sorted_chromosome[previous_index:current_index, :]
        else:
            f[previous_index:current_index, :] = sorted_chromosome[previous_index:current_index, :]
            return f
        previous_index = current_index