import numpy as np
import pandas as pd
import re

from algorithm.pf_optimal import pf_optimal


def parse_complex(string):
    match = re.search(r'([-+]?\d+\.\d+)\s*([+-])\s*([-+]?\d+\.\d+)i', string)
    if match:
        real = float(match.group(1))
        sign = match.group(2)
        imag = float(match.group(3))
        if sign == '-':
            return complex(real, -imag)
        else:
            return complex(real, -imag)
    else:
        return np.nan


# 模块一中图的绘制，包括光伏容量、光伏接入方案的评估，判断有无电压越界的情况
def plan_evaluation(architecture, existPV, PackingPV, loadData, PVdata):
    Z1 = pd.read_excel(architecture, sheet_name='Sheet1', header=None).astype(float)
    Z2 = pd.read_excel(architecture, sheet_name='Sheet2', header=None)
    Z2 = Z2.applymap(parse_complex)
    Z = np.concatenate([Z1.values, Z2.values], axis=1)
    Z1 = np.array(Z1)
    Z2 = np.array(Z2)
    # 已有光伏容量
    S_plan_before = np.array(pd.read_excel(existPV, header=None).astype(float))
    # 光伏接入方案
    S_plan = np.array(pd.read_excel(PackingPV, header=None).astype(float))
    Y = Z.shape[0]
    evaluation_data = np.zeros((Y, 3))
    t = np.arange(1, Y + 1)
    evaluation_data[:, 0] = t
    evaluation_data[:, 1] = S_plan_before
    evaluation_data[:, 2] = S_plan
    # 判断是否有电压越界的情况
    # 负荷数据
    S_load = pd.read_excel(loadData, header=None)
    S_load = S_load.applymap(parse_complex)
    S_load = S_load.apply(pd.to_numeric, errors='coerce')
    S_load = np.array(S_load)
    S_load1 = S_load
    # 光伏数据
    A = pd.read_excel(PVdata, header=None).values
    P_pv = np.mean(pd.to_numeric(A.flatten(), errors='coerce').reshape(A.shape[1], -1), axis=0)[0]

    Y = Z.shape[0]
    T = S_load1.shape[1]
    S_load = np.mean(S_load, axis=1)
    S_load = S_load.reshape(-1, 1)
    U2 = np.zeros((Y, T))
    Count = np.zeros(Y)
    for t in range(T):
        temp = S_load1[:, t]
        aa, _, _ = pf_optimal(S_plan + S_plan_before, P_pv, Z, temp.reshape((len(temp), 1)), Y)
        U2[:, t] = aa.reshape((len(aa),))
        for i in range(Y):
            if U2[i, t] < 0.95 or U2[i, t] > 1.05:
                Count[i] += 1

    Data = np.where(Count > 0)[0]

    if len(Data) == 0:
        crossNode = -1
    else:
        for i in range(len(Data)):
            crossNode = Data[i] + 1
    return evaluation_data, crossNode
