config: dict = {}

'''
初始参数设置
'''

'''
---------------------------------------------------- 运输机参数 ----------------------------------------------------
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

'''
---------------------------------------------------- 带轮参数 ----------------------------------------------------
'''

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

'''
-------------------------------------------------- 齿轮参数 --------------------------------------------------
'''
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

'''
----------------------------------------------------- 轴参数 ----------------------------------------------------
'''
config["Hight-speed-shift"]: dict = {}
config["Hight-speed-shift"]["A0"]: float = 112
config["Hight-speed-shift"]["K1"]: float = 1.3
config["Hight-speed-shift"]["Laxis"]: float = 32        # 联轴器的长度 查表
config["Hight-speed-shift"]["Laxis/2"]: float = 27      # 半联轴器的长度 查表
config["Hight-speed-shift"]["D23"]: float = 16          # 2 -3 轴的直径
config["Hight-speed-shift"]["D34"]: float = 17          # 3 -4 长度 根据轴承
config["Hight-speed-shift"]["D45"]: float = 47          # 4 -5 长度 根据轴承
config["Hight-speed-shift"]["L78"]: float = 14          # 5 -6 长度 根据轴承
config["Hight-speed-shift"]["h"]: float = 2.5           # 轴肩的高度
config["Hight-speed-shift"]["a"]: float = 14
config["Hight-speed-shift"]["c"]: float = 12.5
config["Hight-speed-shift"]["s"]: float = 12
config["Hight-speed-shift"]["d12"]: float = 7.5
config["Hight-speed-shift"]["Dquan"]: float = 20
config["Hight-speed-shift"]["L12"]: float = 25
config["Hight-speed-shift"]["L67"]: float = 46
config["Hight-speed-shift"]["l-duan"]: float = 22
config["Hight-speed-shift"]["L23"] = 50
config["Hight-speed-shift"]["L56"] = 12
config["Hight-speed-shift"]["alpha"] = 20

config["Medium-speed-shift"]: dict = {}
config["Medium-speed-shift"]["A0"]: float = 112
config["Medium-speed-shift"]["K1"]: float = 1.3             # 32904
config["Medium-speed-shift"]["Laxis"]: float = False        # 联轴器的长度 查表
config["Medium-speed-shift"]["Laxis/2"]: float = False      # 半联轴器的长度 查表
config["Medium-speed-shift"]["D23"]: float = 16             # 2 -3 轴的直径
config["Medium-speed-shift"]["D34"]: float = 20             # 3 -4 长度 根据轴承
config["Medium-speed-shift"]["D45"]: float = 37             # 4 -5 长度 根据轴承
config["Medium-speed-shift"]["L78"]: float = 12             # 5 -6 长度 根据轴承
config["Medium-speed-shift"]["h"]: float = 3                # 轴肩的高度
config["Medium-speed-shift"]["a"]: float = 17
config["Medium-speed-shift"]["c"]: float = False
config["Medium-speed-shift"]["s"]: float = False
config["Medium-speed-shift"]["d12"]: float = 10
config["Medium-speed-shift"]["Dquan"]: float = 30
config["Medium-speed-shift"]["L12"]: float = 25
config["Medium-speed-shift"]["L67"]: float = 46
config["Medium-speed-shift"]["l-duan"]: float = 32
config["Medium-speed-shift"]["L23"] = 20
config["Medium-speed-shift"]["L56"] = 40
config["Medium-speed-shift"]["alpha"] = 20

config["low-speed-shift"]: dict = {}
config["low-speed-shift"]["A0"]: float = 112
config["low-speed-shift"]["K1"]: float = 1.3        # 61806
config["low-speed-shift"]["Laxis"]: float = False      # 联轴器的长度 查表
config["low-speed-shift"]["Laxis/2"]: float = False    # 半联轴器的长度 查表
config["low-speed-shift"]["D23"]: float = 16        # 2 -3 轴的直径
config["low-speed-shift"]["D34"]: float = 30        # 3 -4 长度 根据轴承
config["low-speed-shift"]["D45"]: float = 47        # 4 -5 长度 根据轴承
config["low-speed-shift"]["L78"]: float = 14        # 5 -6 长度 根据轴承
config["low-speed-shift"]["h"]: float = 6         # 轴肩的高度
config["low-speed-shift"]["a"]: float = 16.5
config["low-speed-shift"]["c"]: float = False
config["low-speed-shift"]["s"]: float = False
config["low-speed-shift"]["d12"]: float = 7.5
config["low-speed-shift"]["Dquan"]: float = 30
config["low-speed-shift"]["L12"]: float = 30
config["low-speed-shift"]["L67"]: float = 30
config["low-speed-shift"]["l-duan"]: float = 20
config["low-speed-shift"]["L23"] = 40
config["low-speed-shift"]["L56"] = 16
config["low-speed-shift"]["alpha"] = 20

'''
------------------------------------------------------ 轴承参数 ------------------------------------------------
'''
config["Y"]: float = 2  # 轴向动载荷系数
config["e"]: float = 0.3 # 判断系数
config["C"]: float = 44800 # 基本额定动载荷
config["C0"]: float = 0.5 # 基本额定静载荷系数
config["fp"]: float = 1.2
