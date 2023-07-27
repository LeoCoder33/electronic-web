import os.path
from algorithm.util import plan_evaluation
from flask import Flask, request

app = Flask(__name__)


@app.route('/evaluate', methods=["POST"])
def evaluate():
    files = request.files
    # 网架数据
    architecture = files.get('model')
    # 已有容量
    existPV = files.get('PV')
    # 报装容量
    PackingPV = files.get('PVmethod')
    # 新负荷数据
    loadData = files.get('load')
    # 光伏数据
    PVdata = files.get('PVdata')

    # save_path = 'D:/Project/electronic-web-vue3/back-end/' + file.filename
    # file.save(save_path)
    evaluate_data = plan_evaluation(architecture, existPV, PackingPV, loadData, PVdata)
    evaluate_result = evaluate_data[0]
    cross_result = evaluate_data[1]
    capacity = {
        'node': ['节点'] + list(evaluate_result[:, 0]),
        'loadPV': ['报装容量'] + list(evaluate_result[:, 2]),
        'existPV': ['已有容量'] + list(evaluate_result[:, 1])
    }

    capacity_table = []
    for i in range(1, len(capacity['node'])):
        capacity_table.append({
            'node': capacity['node'][i],
            'loadPV': capacity['loadPV'][i],
            'existPV': capacity['existPV'][i]
        })

    return {
        'capacity': capacity,
        'capacity_table': capacity_table,
        'cross_result': cross_result,
    }

@app.route('/calculate', methods=["POST"])
def calculate():
    file = request.files.get('PV')
    save_path = 'D:/Project/electronic-web-vue3/back-end/' + file.filename
    file.save(save_path)
    capacity = {
        'node': ['节点'] + [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        'optimizePV': ['优化容量'] + [1, 3, 4, 9.656661558, 5, 4.510076302, 7, 1, 6, 2, 5, 3, 2, 2, 2, 1, 3, 0]
    }
    capacity_table = []
    for i in range(1, len(capacity['node'])):
        capacity_table.append({
            'node': capacity['node'][i],
            'optimizePV': capacity['optimizePV'][i]
        })
    
    return {
        'capacity': capacity,
        'capacity_table': capacity_table,
        'down_cost': 43.8177,
        'down_loss': 65.6083,
        'down_fluctuation': 71.961
    }


if __name__ == '__main__':
    app.run()
