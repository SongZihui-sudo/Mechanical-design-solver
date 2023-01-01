config: dict = {}

'''
初始参数设置
'''
config["T"]: int = 1000    # 运输机工作轴转矩
config["v"]: float = 0.70    # 运输带工作速度
config["D"]: float = 0.4     # 滚筒直径
config["etaw"]: float = 0.98   # 工作机的效率
config["ld"]: float = 2000  # 运输机的传动长度
config["q"] = 0.1  # 单位长度质量
config["each_eta"]: list = [0.97, 0.91, 0.9, 0.9]  # 传动部分各级的效率
config["Range_transmission_ratio"]: list = [
    [3, 4],
    [3, 7]
]
config["i1"]: float = 3.3   # v带轮传动比范围
config["Ka"]: float = 1.0   # 工作情况系数
config["P0"]: float = 1.67  # 单根V带的额定功率
config["dP0"]: float = 0.169  # 单根V带的额定功率增量
config["ka"]: float = 0.92  # 小带轮的包角修正系数
config["kl"]: float = 1.01  # 带长修正系数
# V带选型
config["type_linear_coefficient"]: dict = {
    "A": {
        "type": "A",
        "range": [80, 100]
    },
    "B": {
        "type": "B",
        "range": [125, 140]
    },
    "C": {
        "type": "C",
        "range": [200, 315]
    },
    "D": {
        "type": "D",
        "range": [355, 400]
    },
    "E": {
        "type": "E",
        "range": [455, 500]
    },
    "Z": {
        "type": "Z",
        "range": [50, 71]
    }
}
config["z1"]: int = 100  # 大齿轮齿数缺省值
config["z2"]: int = 20   # 小齿轮齿数缺省值
config["beta"]: float = 15  # 螺旋角缺省值
config["Kt"]: float = 1.5  # 载荷系数缺省值
config["ZH"]: float = 2.433  # 区域系数缺省值
config["varphi_d"]: float = 1  # 齿宽系数缺省值
config["εα1"]: float = 0.7  # εα1缺省值
config["εα2"]: float = 0.9  # εα2缺省值
config["ZE"]: float = 180  # 弹性影响系数缺省值
config["σHlim1"]: float = 610  # 小齿轮的接触疲劳强度极限
config["σHlim2"]: float = 570  # 大齿轮的接触疲劳强度极限
config["j"]: int = 1  # 齿轮转一周时同侧齿面的啮合次数
config["Lh"]: int = 2 * 8 * 300 * 5  # 齿轮的寿命
config["KHN1"]: float = 0.95  # 大齿轮的接触疲劳寿命系数
config["KHN2"]: float = 0.97  # 小齿轮的接触疲劳寿命系数
config["u"]: int = 5
config["KA"]: float = 1
config["KV"]: float = 1.11
config["KHβ"]: float = 1.36
config["KHα"]: float = 1.40
config["KFα"]: float = 1.40
config["KFβ"]: float = 1.36
config["Yβ"]: float = 0.88  # 螺旋角影响系数
# 齿型系数
config["YFa1"]: float = 2.724
config["Yfa2"]: float = 2.172
# 应力校正系数
config["Ysa1"]: float = 1.569
config["Ysa2"]: float = 1.798
config["KFN1"]: float = 0.95
config["KFN2"]: float = 0.98
# 设 [σF]
config["σF1"]: float = 500
config["σF2"]: float = 380
