import pandas as pd
import numpy as np
import re
from pf_optimal import pf_optimal
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
from initial import initial
from gbest_fitness import gbest_fitness
from update_v import update_v

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

# 1. 网架数据
Z2 = pd.read_excel('新网架数据.xlsx', sheet_name='Sheet2', header=None)
Z2 = Z2.applymap(parse_complex)
Z3 = pd.read_excel('新网架数据.xlsx', sheet_name='Sheet1', header=None).astype(float)
Z = np.concatenate([Z3.values, Z2.values], axis=1)
Z2 = np.array(Z2)
Z3 = np.array(Z3)

# 2. 负荷数据
# 处理字符串值为np.nan
S_load = pd.read_excel('新负荷数据.xlsx', header=None)
S_load = S_load.applymap(parse_complex)
S_load = S_load.apply(pd.to_numeric, errors='coerce')
S_load = np.array(S_load)
S_load1 = S_load

# 3. 已有光伏容量
S_plan_before = np.array(pd.read_excel('新已有容量.xlsx', header=None).astype(float))

# 4. 光伏接入方案
S_plan = np.array(pd.read_excel('新报装容量.xlsx', header=None).astype(float))

# 5. 网架结构图
# 暂不涉及图像导入及导出功能

# 6. 光伏数据
A = pd.read_excel('光伏数据.xlsx', header=None).values
P_pv = np.mean(pd.to_numeric(A.flatten(), errors='coerce').reshape(A.shape[1], -1), axis=0)[0]

# 7. 各节点光伏最大容量
Xmax = np.array(pd.read_excel('新各节点最大光伏容量.xlsx', header=None).values.astype(float))

Y = Z.shape[0]
T = S_load1.shape[1]
S_load = np.mean(S_load, axis=1)
S_load = S_load.reshape(-1, 1)

# print(Z.shape)
# print(S_load.shape)
# print(P_pv.shape)
# print(Xmax.shape)
# print(S_plan.shape)
# print(S_plan_before.shape)

[U1, Data1, obj] = pf_optimal(S_plan+S_plan_before,P_pv,Z,S_load,Y)
print(U1, Data1, obj)

# 创建实数数组 Data1
Data1 = np.zeros((Y, 3))
t = np.arange(1, Y+1)
Data1[:, 0] = t
Data1[:, 1] = S_plan_before
Data1[:, 2] = S_plan

# 输出结果
print("Data1数组:")
print(Data1)

# 获取当前日期时间
todayDate = datetime.now().strftime("%y-%m-%d-%H-%M")

# 将数组写入Excel文件
# df = pd.DataFrame(Data1, columns=["Column 1", "Column 2", "Column 3"])
# df.to_excel(todayDate + "光伏报装方案.xlsx", index=False)

U2 = np.zeros((Y, T))
Count = np.zeros(Y)

for t in range(T):
    temp =  S_load1[:, t]
    aa, _, _ = pf_optimal(S_plan + S_plan_before, P_pv, Z, temp.reshape((len(temp), 1)), Y)
    U2[:, t] = aa.reshape((len(aa),))
    for i in range(Y):
        if U2[i, t] < 0.95 or U2[i, t] > 1.05:
            Count[i] += 1

Data = np.where(Count > 0)[0]

if len(Data) == 0:
    print("无节点电压越限！")
    # im = Image.open("通过.png")  # 读取图像
    # plt.imshow(im)  # 显示图像
    # plt.show()
else:
    Str2 = []
    for i in range(len(Data)):
        numStr = f"第{Data[i]+1}个节点电压越限"
        Str2.append(numStr)
    print("\n".join(Str2))
    # im = Image.open("警告.png")  # 读取图像
    # plt.imshow(im)  # 显示图像
    # plt.show()

# todayDate = np.datetime_as_string(np.datetime64('now'), unit='s')
# csv_file = todayDate + '评估方案下各节点电压.csv'
# np.savetxt(csv_file, U2, delimiter=',')

condition = 1  # 以台区改建为目标为例，修改为其他数字即为台区扩建
if condition == 1:
    Xmin = np.zeros(Y)
else:
    Xmin = S_plan_before.reshape((len(S_plan_before),))

Data = 1

pop = 500  # 种群粒子数目
gen = 30  # 最大迭代次数
M = 4  # 目标函数个数（M-1）
V = Z.shape[0]  # 控制变量个数，节点个数
g_best = np.zeros((gen, V))  # 全局最优存放位置
pop_num = 50  # 保存的最优前沿
lamda = 0.5  # 退火常数

# 输入光伏以及负荷典型日数据
N = T  # 以一个典型日为例，15分钟一个节点，共96个节点

# 初始化种群个体
pop_x, pop_v = initial(pop, V, M, P_pv, Z, S_load, Xmin, Xmax.reshape((Xmax.shape[1],)), N)
print('pop_x', pop_x.shape, pop_v.shape)

[pbest,pbest_value,k]=gbest_fitness(pop_x,V,M,pop)
print('KK', pbest,pbest_value,k)

t = 0
g_best[t,:]=pbest
change_v=update_v(t,gen,pop_v,pop_x[:,0:V],g_best,V,pop,pbest)
print('change_v',change_v)