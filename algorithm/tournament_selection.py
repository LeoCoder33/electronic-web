import numpy as np

def tournament_selection(chromosome, pool_size, tour_size):
    # Get the size of chromosome
    pop, variables = chromosome.shape[0], chromosome.shape[1]
    # The penultimate element contains the information about rank.
    rank = variables - 2
    # The last element contains information about crowding distance.
    distance = variables - 1
    
    f = np.zeros((pool_size, variables))  # Initialize the mating pool
    
    # Until the mating pool is filled, perform tournament selection
    for i in range(pool_size):
        # Select n individuals at random, where n = tour_size
        candidate = np.zeros(tour_size, dtype=int)  # Initialize the candidate array
        # Select an individual at random
        candidate[0] = np.random.randint(pop)
        if candidate[0] == 0:
            candidate[0] = 1
        for j in range(1, tour_size):
            # Make sure that same candidate is not chosen
            while True:
                candidate[j] = np.random.randint(pop)
                if candidate[j] == 0:
                    candidate[j] = 1
                if not np.any(candidate[0:j] == candidate[j]):
                    break
        
        c_obj_rank = chromosome[candidate, rank]  # Collect information about the selected candidates
        c_obj_distance = chromosome[candidate, distance]
        
        # Find the candidate with the least rank
        min_candidate = np.where(c_obj_rank == np.min(c_obj_rank))[0]
        
        # If more than one candidate have the least rank, find the candidate within that group having the maximum crowding distance
        if len(min_candidate) != 1:
            max_candidate = np.where(c_obj_distance[min_candidate] == np.max(c_obj_distance[min_candidate]))[0]
            
            # If a few individuals have the least rank and have maximum crowding distance, select only one individual (not at random)
            if len(max_candidate) != 1:
                max_candidate = max_candidate[0]
            
            # Add the selected individual to the mating pool
            f[i, :] = chromosome[candidate[min_candidate[max_candidate]], :]
        else:
            # Add the selected individual to the mating pool
            f[i, :] = chromosome[candidate[min_candidate[0]], :]
    
    return f