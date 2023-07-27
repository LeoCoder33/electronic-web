from pf import pf

def mokuaihanshu(x, pop, M, V, P_pv, Z, S_load, N):
    fit = pf(x[:, 0:V], M, P_pv, Z, S_load, V, N)
    return fit