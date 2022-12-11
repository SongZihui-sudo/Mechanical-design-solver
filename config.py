config: dict = {}

'''
初始参数设置
'''
config["T"]: int = 1000    # 运输机工作轴转矩
config["v"]: float = 0.70    # 运输带工作速度
config["D"]: float = 0.4     # 滚筒直径
config["etaw"]: float = 0.96   # 工作机的效率
# 准确性存疑问
config["each_eta"]: list = [0.98, 0.9, 0.9, 0.9]  # 传动部分各级的效率
# 准确性存疑问
config["Range_transmission_ratio"]: list = [
    [3, 4],
    [3, 7]
]   # v带轮传动比范围
config["i1"]: float = 3.2
# 工作情况系数
config["Ka"]: float = 1.1
# V选型中各直线的方程系数
config["type_linear_coefficient"]: dict = {
    "A": {
        "type": "A",
        "k": 40,
        "b": 160,
        "range": [80, 100]
    },
    "B": {
        "type": "B",
        "k": 177,
        "b": -284,
        "range": [125, 140]
    },
    "C": {
        "type": "C",
        "k": 62.5,
        "b": -500,
        "range": [200, 315]
    },
    "D": {
        "type": "D",
        "k": 4.7,
        "b": 12,
        "range": [355, 400]
    },
    "E": {
        "type": "E",
        "k": 4.2,
        "b": -210,
        "range": [455, 500]
    },
    "Z": {
        "type": "Z",
        "k": 296,
        "b": 630,
        "range": [50, 71]
    }
}
