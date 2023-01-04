'''
机械设计参数计算器
'''
import config
import math
from sympy import *


class point(object):
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y


'''
计算器 基类
'''


class calculation(object):
    def __init__(self) -> None:
        self.config: dict = config.config

    '''
    获取参数
    '''

    def get_config(self, par: str) -> None:
        return self.config[par]

    '''
    设置参数
    '''

    def set_config(self, key: str, val: any) -> None:
        self.config[key] = val

    '''
    计算周长
    '''

    def __Circumference_cal(self) -> None:
        self.config["Circumference"] = math.pi * self.config["D"]
        self.output(["确定周长", str(math.pi), " * ", str(self.config["D"]),
                    str(self.config["Circumference"]), "m"])

    '''
    计算转速
    '''

    def __Rotational_speed_cal(self) -> None:
        self.config["n"] = self.config["v"] / self.config["Circumference"] * 60
        self.output(["确定转速", str(self.config["v"]), " \ ", str(
            self.config["Circumference"]), " * 60", str(self.config["n"]), "r/min"])

    '''
    计算传动装置的总效率
    '''

    def __etaTotal_cal(self, arg: list) -> None:
        string: str = ""
        self.config["etaTotal"] = 1
        for eta in arg:
            self.config["etaTotal"] = self.config["etaTotal"] * eta
            string = string + str(eta) + " * "
        string = string[:-2]
        # self.config["etaTotal"] *= 100
        self.output(["计算转动装置的总效率", string, str(self.config["etaTotal"]), ""])

    '''
    获取周长
    '''

    def get_Circumference(self) -> float:
        return self.config["Circumference"]

    '''
    获取转速
    '''

    def get_Rotational_speed(self) -> float:
        return self.config["n"]

    '''
    输出结果
    '''

    def output(self, arg: list) -> None:
        res: str = arg[len(arg) - 2] + " " + arg[len(arg) - 1]
        step: str = ""
        for i in range(1, len(arg) - 2):
            step += arg[i]

        f = open(r'./计算结果.txt', 'a')

        print("步骤: %s -> %s -> res = %s" % (arg[0], step, res), file=f)

        f.close()


'''
电动机参数确定 子类
'''


class electroMotor(calculation):
    def __init__(self) -> None:
        self.output(
            ["*************************** 电动机参数确定 **************************", "", "\n"])
        super().__init__()

    '''
    确定容量
    '''

    def __Capacity_determination(self) -> None:
        Pw: float = (self.get_config("T") *
                     self.get_Rotational_speed()) / (9550 * self.get_config("etaw"))
        self.set_config("Pw", Pw)
        self.output(["确定工作机所需功率", "(", str(self.get_config("T")), " * ", str(self.get_Rotational_speed()),
                    ") / ( 9550 * ", str(self.get_config("etaw")), " )", str(Pw), "kW"])

        self.__Pd: float = Pw / self.get_config("etaTotal")
        self.set_config("Pd", self.__Pd)
        self.output(["计算电动机的输出功率", str(Pw), " / ",
                    str(self.get_config("etaTotal")), str(self.__Pd), "kW"])

    '''
    确定电动机的转速
    '''

    def __motor_speed_determination(self) -> None:
        max: float = self.config["n"]
        min: float = self.config["n"]

        rec_string1: str = str(self.config["n"]) + "* ( "
        rec_string2: str = str(self.config["n"]) + "* ( "

        for cur in self.config["Range_transmission_ratio"]:
            max = max * cur[1]
            min = min * cur[0]
            rec_string1 += str(cur[1]) + " * "
            rec_string2 += str(cur[0]) + " * "
        rec_string1 = rec_string1[:-2] + ")"
        rec_string2 = rec_string2[:-2] + ")"

        self.output(["确定电动机的最大转速", rec_string1, str(max), "r/min"])
        self.output(["确定电动机的最小转速", rec_string2, str(min), "r/min"])

        self.set_config("max_n", max)
        self.set_config("min_n", min)

    '''
    实现 run 函数
    '''

    def run(self) -> None:
        self._calculation__Circumference_cal()
        self._calculation__Rotational_speed_cal()
        self._calculation__etaTotal_cal(self.config["each_eta"])
        self.__Capacity_determination()
        self.__motor_speed_determination()


'''
传动装置参数计算
'''


class gearing(calculation):
    def __init__(self) -> None:
        self.output(
            ["\n\n*************************** 传动装置参数计算 **************************", "", "\n"])
        super().__init__()

    '''
    确定总传动比
    '''

    def __total_transmission_ratio_cal(self) -> None:
        ia: float = self.get_config("max_n") / self.get_Rotational_speed()
        self.set_config("ia", ia)
        self.output(["确定总传动比", str(self.get_config("max_n")), " / ",
                    str(self.get_Rotational_speed()), str(ia), ""])

    '''
    各级传动比的分配
    '''

    def __distribution_transmission_ratios(self) -> None:
        i减: float = self.get_config("ia") / self.get_config("i1")
        i2: float = pow(1.4 * i减, 0.5)
        i3: float = i减 / i2

        self.set_config("i减", i减)
        self.set_config("i2", i2)
        self.set_config("i3", i3)

        self.output(["设V带传动分配的传动比", str(self.get_config("i1")),
                    str(self.get_config("i1")), ""])
        self.output(
            ["确定圆柱齿轮减速器内总传动比", "pow ( 1.4 * ", str(i减), ", 0.5 )", str(i2), ""])
        self.output(["确定低速级齿轮传动比", str(i减), " / ", str(i2), str(i3), ""])

    '''
    计算各轴输入转速
    '''

    def __input_speed_shaft(self) -> None:
        n1: float = self.get_config("max_n")
        n2: float = self.get_config("max_n") / self.get_config("i1")
        n3: float = self.get_config(
            "max_n") / (self.get_config("i1") * self.get_config("i2"))
        n4: float = n3

        self.set_config("n1", n1)
        self.set_config("n2", n2)
        self.set_config("n3", n3)
        self.set_config("n4", n4)

        self.output(["确定高速轴一的转速", "n1 = ", str(n1), str(n1), ""])
        self.output(["中间轴2的转速", str(self.get_config("max_n")),
                    " / ", str(self.get_config("i1")), str(n2), ""])
        self.output(["低速轴3的转速", str(self.get_config("max_n")), " / ",
                    str(self.get_config("i1")), " * ", str(self.get_config("i2")), str(n3), ""])
        self.output(["滚筒轴4的转速", "n4 = ", str(n3), str(n3), ""])

    '''
    计算各轴的输入功率
    '''

    def __input_power_shaft(self) -> None:
        pre = self.get_config("Pd")
        index: int = 1
        cur: str = ""
        for eta in self.get_config("each_eta"):
            Pi = pre * eta
            pre = Pi
            cur = "P" + str(index)
            self.set_config(cur, Pi)
            self.output(["轴" + str(index) + "输入功率", str(pre),
                        " * ", str(eta), str(Pi), "kW"])
            index += 1

    '''
    计算各轴的输入转矩
    '''

    def __input_torque_shaft(self) -> None:
        pre = self.get_config("Pd")
        index: int = 1
        cur: str = ""
        for eta in range(len(self.get_config("each_eta"))):
            Ti = 9550 * (pre / self.get_config("n" + str(index)))
            pre = self.get_config("P" + str(index))
            cur = "T" + str(index)
            self.set_config(cur, Ti)
            self.output(["轴" + str(index) + "输入转矩", str(pre),
                        " * ", str(self.get_config("n" + str(index))), str(Ti), "N * m"])
            index += 1

    '''
    实现 run 函数
    '''

    def run(self) -> None:
        self.__total_transmission_ratio_cal()
        self.__distribution_transmission_ratios()
        self.__input_speed_shaft()
        self.__input_power_shaft()
        self.__input_torque_shaft()


'''
带轮设计计算
'''


class pulley(calculation):
    def __init__(self) -> None:
        self.output(
            ["\n\n*************************** 带轮设计计算 **************************", "", "\n"])
        super().__init__()

    '''
    计算输入功率
    '''

    def __inputPower(self) -> None:
        self.Pca: float = self.get_config("Pw") * self.get_config("Ka")
        self.set_config("Pca", self.Pca)
        self.output(["输入功率", "Pca = ", "Pca = " + str(self.get_config("Pw")) +
                    "*" + str(self.get_config("Ka")) + "=", str(self.get_config("Pw")), "KW"])

    '''
    V带轮选型
    '''

    def __selection_pulley(self) -> None:
        self.n: float = self.get_config("n")
        self.type: str = self.get_config("V-Type")
        self.set_config("type", self.type)
        self.output(["带轮型号：", "根据Pca", " n", self.type, "型V带轮"])

    '''
    确定小轮直径
    '''

    def __diameter_small_pulley(self) -> None:
        range: list = self.get_config("type_linear_coefficient")[
                                      self.type]["range"]
        self.dd1: int = int((range[0] + range[1]) / 2)
        self.output(["确定小轮直径", "由", self.type, "型V带轮得出：", str(self.dd1), "mm"])

    '''
    验算带速
    '''

    def __belt_speed(self) -> None:
        self.v: float = math.pi * self.dd1 * self.get_config("n1") / 60000
        if 5 < self.v < 30:
            self.output(["验算带速v 合适", "pi*dd1*n/60000", str(self.v), "m/s"])
        else:
            self.output(["验算带速v 不合适", "pi*dd1*n/60000", str(self.v), "m/s"])

    '''
    确定大轮直径
    '''

    def __diameter_large_pulley(self) -> None:
        self.dd2: int = int(self.dd1 * self.get_config("i1"))
        self.output(["确定大轮直径", "由小轮直径和传动比得出：", str(self.dd2), "mm"])

    '''
    计算中心距
    '''

    def __center_distance(self) -> None:
        max: float = 2 * (self.dd1 + self.dd2)
        min: float = 0.7 * (self.dd1 + self.dd2)
        self.a0: int = int((max + min) / 2)
        self.output(["计算中心距", "由小轮直径和大轮直径得出：", str(self.a0), "mm"])

    '''
    计算基准长度
    '''

    def __datum_length(self) -> None:
        self.l: float = (2 * self.a0) + (math.pi / 2) * \
            (self.dd1 + self.dd2) + pow((self.dd2 - self.dd1), 2) / (4 * self.a0)
        self.output(["计算基准长度", "由中心距和小轮直径和大轮直径得出：", str(self.l), "mm"])

    '''
    计算实际间距
    '''

    def __actual_spacing(self) -> None:
        self.a: float = (self.get_config("ld") - self.l) / 2 + self.a0
        self.output(["计算实际间距", "由实际间距得出：", str(self.a), "mm"])

    '''
    计算小带轮包角
    '''

    def __small_pulley_wrap_angle(self) -> None:
        self.a1 = 180 - ((self.dd2 - self.dd1) / self.a) * 57.3
        self.output(["计算小带轮包角", "由小轮直径和大轮直径和实际间距得出：", str(self.a1), "°"])

    '''
    单根V带的额定功率
    '''

    def __rated_power_single_belt(self) -> None:
        self.P0: float = self.get_config("P0")
        self.dP0: float = self.get_config("dP0")
        self.ka: float = self.get_config("ka")
        self.kl: float = self.get_config("kl")

    '''
    计算带的根数
    '''

    def __belt_root_number(self) -> None:
        Pd: float = self.get_config("Pd")
        self.z: int = Pd / ((self.P0 + self.dP0) * self.ka * self.kl)
        self.set_config("belt_num", self.z)
        self.output(["计算带的根数", "由额定功率和单根V带的额定功率得出：", str(self.z), "根"])

    '''
    计算单根V带的最小拉力
    '''

    def __min_value_initial_tension_belt(self) -> None:
        self.F0 = 500 * (2.5 / self.ka - 1)
        self.get_config("Pd") / (self.z *
                                 self.v) + self.get_config("q") * pow(self.v, 2)
        self.output(["计算单根V带的最小拉力", "由额定功率和带的根数和带速得出：", str(self.F0), "N"])

    '''
    计算压轴力
    '''

    def __axial_force(self) -> None:
        self.Fr = 2 * self.F0 * math.sin(self.a0) / 2 * self.z
        self.output(["计算压轴力", "由单根V带的最小拉力和实际间距得出：", str(self.Fr), "N"])

    def run(self) -> None:
        self.__inputPower()
        self.__selection_pulley()
        self.__diameter_small_pulley()
        self.__belt_speed()
        self.__diameter_large_pulley()
        self.__center_distance()
        self.__datum_length()
        self.__actual_spacing()
        self.__small_pulley_wrap_angle()
        self.__rated_power_single_belt()
        self.__belt_root_number()
        self.__min_value_initial_tension_belt()
        self.__axial_force()


'''
齿轮设计计算
'''


class gear(calculation):
    def __init__(self) -> None:
        self.output(
            ["\n\n*************************** 齿轮设计计算 **************************", "", "\n"])
        super().__init__()

    '''
    计算εα
    '''

    def __calculation_epsilon_alpha(self) -> None:
        self.εα = self.get_config("εα1") + self.get_config("εα2")
        self.set_config("εα", self.εα)
        self.output(["计算εα", "由εα1和εα2得出：", str(self.εα), ""])

    '''
    计算应力循环次数
    '''

    def __Calculate_number_stress_cycles(self) -> None:
        self.N1: float = 60 * \
            self.get_config("n2") * self.get_config("j") * \
            self.get_config("Lh")
        self.output(["计算应力循环次数N1", "由n1和j和Lh得出：", str(self.N1), ""])
        self.N2: float = self.N1 / 5
        self.output(["计算应力循环次数N2", "由N1得出：", str(self.N2), ""])

    '''
    计算接触疲劳需用应力
    '''

    def __Calculation_stress_required_contact_fatigue(self) -> None:
        self._σH_1 = self.get_config("KHN1") * self.get_config("σHlim1")
        self.output(["计算接触疲劳需用应力σH1", "由KHN1和σHlim1得出：", str(self._σH_1), ""])
        self._σH_2 = self.get_config("KHN2") * self.get_config("σHlim2")
        self.output(["计算接触疲劳需用应力σH2", "由KHN2和σHlim2得出：", str(self._σH_2), ""])
        self._σH_ = (self._σH_1 + self._σH_2) / 2
        self.output(["计算接触疲劳需用应力σH", "由_σH_1和_σH_2得出：", str(self._σH_), ""])

    '''
    试算小齿轮分度圆直径
    '''

    def __TryCalculate_diameter_pinion_indexing_circle(self) -> None:
        temp1: float = (2 * self.get_config("Kt") * self.get_config("T2") * pow(10, 3)) / \
                        (self.get_config("varphi_d") * self.get_config("εα"))
        temp2: float = (self.get_config("u") + 1) / self.get_config("u")
        temp3: float = pow(
            (self.get_config("ZH") * self.get_config("ZE")) / self._σH_, 2)
        self.d1t = pow(temp1 * temp2 * temp3, float(1) / float(3))
        self.output(
            ["试算小齿轮分度圆直径d1t", "由Kt和T1和varphi_d和εα和u和ZH和ZE和_σH_1得出：", str(self.d1t), "mm"])
        self.set_config("d1t", self.d1t)

    '''
    试算大齿轮分度圆直径
    '''

    def __TryCalculate_diameter_large_pinion_indexing_circle(self) -> None:
        temp1: float = (2 * self.get_config("Kt") * self.get_config("T3") * pow(10, 3)) / \
                        (self.get_config("varphi_d") * self.get_config("εα"))
        temp2: float = (self.get_config("u") + 1) / self.get_config("u")
        temp3: float = pow(
            (self.get_config("ZH") * self.get_config("ZE")) / self._σH_, 2)
        self.d2t = pow(temp1 * temp2 * temp3, float(1) / float(3))
        self.output(
           ["试算大齿轮分度圆直径d2t", "由Kt和T2和varphi_d和εα和u和ZH和ZE和_σH_2得出：", str(self.d2t), "mm"])
        self.set_config("d1t", self.d1t)

    '''
    计算小齿轮圆柱速度
    '''

    def __Calculate_cylindrical_speed_pinion(self) -> None:
        self.v_gear1 = (math.pi *
                        self.d1t * self.get_config("n2")) / (60 * 1000)
        self.output(["计算小齿轮圆柱速度", "由d1和n2得出：", str(self.v_gear1), "m/s"])

    '''
    计算小齿轮齿宽b
    '''

    def __Calculate_pinion_tooth_width(self) -> None:
        self.b1 = self.get_config("varphi_d") * self.get_config("d1t")
        self.output(["计算小齿轮齿宽b", "由varphi_d和d1t得出：", str(self.b1), "mm"])

    '''
    计算大齿轮齿宽b
    '''

    def __Calculate_large_pinion_tooth_width(self) -> None:
        self.b2 = self.get_config("varphi_d") * self.d2t
        self.output(["计算大齿轮齿宽b", "由varphi_d和d1t得出：", str(self.b2), "mm"])

    '''
    计算小齿轮模数
    '''

    def __Calculate_pinion_modulus(self) -> None:
        self.m1 = (self.d1t *
                   math.cos(math.radians(self.get_config("beta")))) / self.get_config("z2")
        self.output(["计算小齿轮模数m1", "由d1t和beta和Z2得出：", str(self.m1), ""])
        self.h1 = 2.25 * self.m1
        self.output(["计算小齿轮h1", "由m1得出：", str(self.h1), ""])
        self.temp = self.b1 / self.h1
        self.output(["b / h", "由b1和h1得出：", str(self.temp), ""])

    '''
    计算大齿轮模数
    '''

    def __Calculate_large_pinion_modulus(self) -> None:
        self.m2 = self.d2t * \
            math.cos(math.radians(self.get_config("beta"))) / \
            self.get_config("z1")
        #self.output(["计算大齿轮模数", "由d1t和beta和Z1得出：", str(self.m2), ""])
        self.h2 = 2.25 * self.m2
        #self.output(["计算大齿轮h1", "由m1得出：", str(self.h2), ""])
        self.temp = self.b2 / self.h2
        #self.output(["b / h", "由b1和h1得出：", str(self.temp), ""])

    '''
    计算小齿轮的纵向重合度
    '''

    def __Calculate_longitudinal_coincidence_degree_pinion(self) -> None:
        self.εβ = 0.318 * 1 * \
            self.get_config("z2") * \
            math.tan(math.radians(self.get_config("beta")))
        self.output(["计算小齿轮的纵向重合度", "由z1和beta得出：", str(self.εβ), ""])

    '''
    计算载荷系数 K
    '''

    def __Calculate_load_coefficient(self) -> None:
        self.K = self.get_config(
            "KA") * self.get_config("KV") * self.get_config("KHβ") * self.get_config("KHα")
        self.output(["计算载荷系数 K", "由KA和KV和KHβ和KHα得出：", str(self.K), ""])

    '''
    矫正分度圆直径
    '''

    def __Corrected_graduation_circle_diameter(self) -> None:
        self.d1 = self.d1t * pow(self.K /
                                 self.get_config("Kt"), float(1) / float(3))
        self.output(["矫正小齿轮分度圆直径", "由d1t和K和Kt得出：", str(self.d1), "mm"])

        self.d2 = self.d2t * pow(self.K /
                                 self.get_config("Kt"), float(1) / float(3))
        self.output(["矫正大齿轮分度圆直径", "由d2t和K和Kt得出：", str(self.d2), "mm"])

    '''
    矫正模数
    '''

    def __Correction_modulus(self) -> None:
        self.n = self.d1 * \
            math.cos(math.radians(self.get_config("beta"))) / \
            self.get_config("z2")
        self.output(["矫正模数", "由d1和beta和Z1得出：", str(self.n), ""])

    '''
    计算载荷系数按齿根弯曲强度设计
    '''

    def __Calculation_load_coefficient_with_bending_strength_tooth_root(self) -> None:
        self.K = self.get_config(
            "KA") * self.get_config("KV") * self.get_config("KFβ") * self.get_config("KFα")
        self.output(["计算载荷系数 K", "由KA和KV和KFβ和KFα得出：", str(self.K), ""])

        temp1: float = (2 * self.K *
                        self.get_config("T2") * self.get_config("Yβ") * pow(10, 3) *
                        pow(math.cos(math.radians(self.get_config("beta"))), 2)) / (self.get_config("varphi_d") * pow(self.get_config("z2"), 2) * self.εα)
        temp2: float = (self.get_config("Yfa2") *
                        self.get_config("Ysa2")) / self.get_config("σF2")

        self.mn = pow(temp1 * temp2, float(1) / float(3))

        self.output(
            ["计算模数", "由K和T2和Yβ和beta和varphi_d和z2和εα和Yfa2和Ysa2和σF2得出：", str(self.mn), ""])

    '''
    计算当量齿数
    '''

    def __Calculate_equivalent_tooth_number(self) -> None:
        temp: float = math.cos(math.radians(self.get_config("beta")))
        self.z1 = self.get_config(
            "z1") / pow(temp, 3)
        self.output(["计算当量齿数", "由Z1和beta得出：", str(self.z1), ""])
        self.z2 = self.get_config(
            "z2") / pow(temp, 3)
        self.output(["计算当量齿数", "由Z2和beta得出：", str(self.z2), ""])

    '''
    计算中心距
    '''

    def __Calculate_center_distance(self) -> None:
        temp: float = self.z2
        self.z2 = (
            self.d1t * math.cos(math.radians(self.get_config("beta")))) / self.mn
        self.z1 = self.z1 * (self.z2 / temp)

        self.a = ((self.z1 + self.z2) * self.mn) / \
            (2 * math.cos(math.radians(self.get_config("beta"))))
        self.output(["计算中心距", "由z1和z2和m1和beta得出：", str(self.a), "mm"])

    '''
    修正螺旋角
    '''

    def __Modified_helix_angle(self) -> None:
        temp = ((self.z1 + self.z2) * self.mn) / (2 * self.a)
        self.beta = math.degrees(math.acos(temp))
        self.set_config("beta", self.beta)
        self.output(["修正螺旋角", "由z1和z2和mn和a得出：", str(self.beta), "度"])

    '''
    计算分度圆直径
    '''

    def __Calculate_diameter_graduation_circle(self) -> None:
        self.d1 = self.get_config(
            "z1") * self.mn / math.cos(math.radians(self.get_config("beta")))
        self.output(["计算分度圆直径", "由Z1和mn和beta得出：", str(self.d1), "mm"])
        self.d2 = self.get_config(
            "z2") * self.mn / math.cos(math.radians(self.get_config("beta")))
        self.output(["计算分度圆直径", "由Z2和mn和beta得出：", str(self.d2), "mm"])

    '''
    计算齿轮宽度
    '''

    def __Calculate_gear_width(self) -> None:
        self.B1 = self.get_config("varphi_d") * self.d1
        self.output(["计算齿轮宽度", "由varphi_d和d1得出：", str(self.B1), "mm"])
        self.set_config("B1", self.B1)  # 保存齿轮宽度
        self.B2 = self.get_config("varphi_d") * self.d2
        self.output(["计算齿轮宽度", "由varphi_d和d2得出：", str(self.B2), "mm"])
        self.set_config("B2", self.B2)  # 保存齿轮宽度

    def run(self) -> None:
        self.__calculation_epsilon_alpha()
        self.__Calculate_number_stress_cycles()
        self.__Calculation_stress_required_contact_fatigue()
        self.__TryCalculate_diameter_pinion_indexing_circle()
        self.__TryCalculate_diameter_large_pinion_indexing_circle()
        self.__Calculate_cylindrical_speed_pinion()
        self.__Calculate_pinion_tooth_width()
        self.__Calculate_large_pinion_tooth_width()
        self.__Calculate_pinion_modulus()
        self.__Calculate_large_pinion_modulus()
        self.__Calculate_longitudinal_coincidence_degree_pinion()
        self.__Calculate_load_coefficient()
        self.__Corrected_graduation_circle_diameter()
        self.__Correction_modulus()
        self.__Calculation_load_coefficient_with_bending_strength_tooth_root()
        self.__Calculate_equivalent_tooth_number()
        self.__Calculate_center_distance()
        self.__Modified_helix_angle()
        self.__Calculate_diameter_graduation_circle()
        self.__Calculate_gear_width()


'''
轴设计计算
'''


class shift(calculation):

    def __init__(self, string: str) -> None:
        self.typeName: str = string

        self.temp1str = self.temp2str = self.temp3str = ""

        if self.typeName == "High-speed-shift":
            self.output(
                ["\n\n*************************** 高速轴 轴设计计算 **************************", "", "\n"])
            self.temp1str = "P1"
            self.temp2str = "n1"
            self.temp3str = "T1"
        elif self.typeName == "Low-speed-shift":
            self.output(
                ["\n\n*************************** 低速轴 轴设计计算 **************************", "", "\n"])
            self.temp1str = "P3"
            self.temp2str = "n3"
            self.temp3str = "T3"
        elif self.typeName == "Medium-speed-shift":
            self.output(
                ["\n\n*************************** 中间轴 轴设计计算 **************************", "", "\n"])
            self.temp1str = "P2"
            self.temp2str = "n2"
            self.temp3str = "T2"

        super().__init__()

    def get_config(self, par: str) -> None:
        self.config[self.typeName][self.temp1str] = self.config[self.temp1str]
        self.config[self.typeName][self.temp2str] = self.config[self.temp2str]
        self.config[self.typeName][self.temp3str] = self.config[self.temp3str]
        self.config[self.typeName]["B2"] = self.config["B2"]
        self.config[self.typeName]["beta"] = self.config["beta"]
        return self.config[self.typeName][par]

    '''
    确定轴的最小直径
    '''

    def __Calculate_minimum_diameter(self) -> None:
        self.dmin = self.get_config(
            "A0") * math.sqrt((self.get_config(self.temp1str) / self.get_config(self.temp2str)))

        self.dmin = self.dmin + self.dmin * 0.06

        self.output(["确定轴的最小直径", "由A0和P1和n1得出：", str(self.dmin), "mm"])

    '''
    联轴器的计算转矩
    '''

    def __Calculated_torque_coupling(self) -> None:
        self.Tca = self.get_config("KA") * self.get_config(self.temp3str)
        self.output(["联轴器的计算转矩", "由Ka和T1得出：", str(self.Tca), "N·m"])

    '''
    确定联轴器的参数
    '''

    def __Determine_parameters_coupling(self) -> None:
        self.d = int(self.dmin)  # 联轴器孔径
        if self.typeName == "High-speed-shift":
            self.output(["确定联轴器孔径", "由dmin得出：", str(self.d), "mm"])
            self.output(["确定联轴器长度", "查表得出", str(self.get_config("L")), "mm"])
            self.output(["确定半联轴器长度", "查表得出", str(
                self.get_config("L1")), "mm"])

        self.output(["L 1 - 2", "选用", str(self.get_config("L1-2")), "mm"])
        self.output(["L 2 - 3", "选用", str(self.get_config("L2-3")), "mm"])
        self.output(["L 3 - 4", "选用", str(self.get_config("L3-4")), "mm"])
        self.output(["L 4 - 5", "选用", str(self.get_config("L4-5")), "mm"])
        self.output(["L 5 - 6", "选用", str(self.get_config("L5-6")), "mm"])
        self.output(["L 6 - 7", "选用", str(self.get_config("L6-7")), "mm"])
        self.output(["L 7 - 8", "选用", str(self.get_config("L7-8")), "mm"])

        self.output(["D 1 - 2", "选用", str(self.get_config("D1-2")), "mm"])
        self.output(["D 2 - 3", "选用", str(self.get_config("D2-3")), "mm"])
        self.output(["D 3 - 4", "选用", str(self.get_config("D3-4")), "mm"])
        self.output(["D 4 - 5", "选用", str(self.get_config("D4-5")), "mm"])
        self.output(["D 5 - 6", "选用", str(self.get_config("D5-6")), "mm"])
        self.output(["D 6 - 7", "选用", str(self.get_config("D6-7")), "mm"])
        self.output(["D 7 - 8", "选用", str(self.get_config("D7-8")), "mm"])

    def __Force_calculation(self) -> None:
        self.Ft = (2 * self.get_config(self.temp3str) * pow(10, 2)) / self.d
        self.output(["计算Ft1", "由T1和d得出：", str(self.Ft), "N"])

        self.Fr = self.Ft * \
            (math.tan(math.radians(self.get_config("alpha")) /
             math.cos(math.radians(self.get_config("beta")))))
        self.output(["计算Fr", "由T1t和alpha得出：", str(self.Fr), "N"])
        self.Fa = self.Ft * math.tan(math.radians(self.get_config("beta")))
        self.output(["计算Fa", "由Fr1和beta得出：", str(self.Fa), "N"])

        if self.typeName == "High-speed-shift":
            self.set_config("Fa1", self.Fa)
        elif self.typeName == "Medium-speed-shift":
            self.set_config("Fa2", self.Fa)
        elif self.typeName == "Low-speed-shift":
            self.set_config("Fa3", self.Fa)

    '''
    计算支反力
    '''

    def __Calculate_supporting_force(self) -> None:
        self.Fah = Symbol("Fah")
        self.Fav = Symbol("Fav")
        self.Fbh = Symbol("Fbh")
        self.Fbv = Symbol("Fbv")

        # 水平
        res = solve([self.Ft * self.get_config("L3") - self.Fah *
                     (self.get_config("L2") + self.get_config("L3")), self.Ft - self.Fah - self.Fbh], [self.Fah, self.Fbh])

        self.Fah = res[self.Fah]
        self.Fbh = res[self.Fbh]

        self.output(["计算Fah", "由Ft1和L3得出：", str(self.Fah), "N"])
        self.output(["计算Fbh", "由Ft1和L3得出：", str(self.Fbh), "N"])

        # 垂直
        res = solve([self.Fr - self.Fav - self.Fbv, self.Fa *
                     (self.get_config("d1") / 2) - self.Fr * self.get_config("L3") + self.Fav * (self.get_config("L2") + self.get_config("L3"))], [self.Fav, self.Fbv])

        self.Fav = res[self.Fav]
        self.Fbv = res[self.Fbv]

        self.output(["计算Fav", "由Fr1和L3得出：", str(self.Fav), "N"])
        self.output(["计算Fbv", "由Fr1和L3得出：", str(self.Fbv), "N"])

        if self.typeName == "High-speed-shift":
            self.set_config("Fah1", self.Fah)
            self.set_config("Fav1", self.Fav)
            self.set_config("Fbh1", self.Fbh)
            self.set_config("Fbv1", self.Fbv)
        elif self.typeName == "Medium-speed-shift":
            self.set_config("Fah2", self.Fah)
            self.set_config("Fav2", self.Fav)
            self.set_config("Fbh2", self.Fbh)
            self.set_config("Fbv2", self.Fbv)
        elif self.typeName == "Low-speed-shift":
            self.set_config("Fah3", self.Fah)
            self.set_config("Fav3", self.Fav)
            self.set_config("Fbh3", self.Fbh)
            self.set_config("Fbv3", self.Fbv)

    def run(self) -> None:
        self.__Calculate_minimum_diameter()
        self.__Calculated_torque_coupling()
        self.__Determine_parameters_coupling()
        self.__Force_calculation()
        self.__Calculate_supporting_force()


'''
    轴承设计计算
'''


class bearing(calculation):
    def __init__(self, name: str) -> None:
        super().__init__()

        self.TypeName: str = name
        self.Fahtemp: float = 0
        self.Favtemp: float = 0
        self.Fbhtemp: float = 0
        self.Fbvtemp: float = 0
        self.Fa: float = 0

        if self.TypeName == "High-speed-bear":
            self.output(
                ["\n\n*************************** 高速轴 轴承设计计算 **************************", "", "\n"])
            self.Fahtemp: float = self.config["Fah1"]
            self.Favtemp: float = self.config["Fav1"]
            self.Fbhtemp: float = self.config["Fbh1"]
            self.Fbvtemp: float = self.config["Fbv1"]
            self.Fa: float = self.config["Fa1"]
            self.ntemp = self.config["n1"]
        elif self.TypeName == "Low-speed-bear":
            self.output(
                ["\n\n*************************** 低速轴 轴承设计计算 **************************", "", "\n"])
            self.Fahtemp: float = self.config["Fah3"]
            self.Favtemp: float = self.config["Fav3"]
            self.Fbhtemp: float = self.config["Fbh3"]
            self.Fbvtemp: float = self.config["Fbv3"]
            self.Fa: float = self.config["Fa2"]
            self.ntemp = self.config["n3"]
        elif self.TypeName == "Medium-speed-bear":
            self.output(
                ["\n\n*************************** 中间轴 轴承设计计算 **************************", "", "\n"])
            self.Fahtemp: float = self.config["Fah2"]
            self.Favtemp: float = self.config["Fav2"]
            self.Fbhtemp: float = self.config["Fbh2"]
            self.Fbvtemp: float = self.config["Fbv2"]
            self.Fa: float = self.config["Fa3"]
            self.ntemp = self.config["n2"]

    def get_config(self, par: str) -> None:
        return self.config[self.TypeName][par]

    '''
    计算径向载荷
    '''

    def __Calculate_radial_load(self) -> None:
        self.FrA = pow(pow(self.Fahtemp, 2) + pow(self.Favtemp, 2), 0.5)
        self.FrB = pow(pow(self.Fbhtemp, 2) + pow(self.Fbvtemp, 2), 0.5)
        self.output(["计算FtA", "由Fr1和Ft1得出：", str(self.FrA), "N"])
        self.output(["计算FrB", "由Fa1和Ft1得出：", str(self.FrB), "N"])

    '''
    计算轴向载荷
    '''

    def __Calculate_axial_load(self) -> None:
        self.Sa = self.FrA / (2 * self.get_config("Y"))
        self.output(["计算Sa", "由Fta和Y得出：", str(self.Sa), "N"])
        self.Sb = self.FrB / (2 * self.get_config("Y"))
        self.output(["计算Sb", "由Fra和Y得出：", str(self.Sb), "N"])
        if self.Fa + self.Sb > self.Sa:
            self.output(["轴承A被压紧，轴承B放松", "", ""])
        else:
            self.output(["轴承A放松，轴承B被压紧", "", ""])
    '''
    计算当量动载荷
    '''

    def __Calculate_equivalent_dynamic_load(self) -> None:
        temp: float = self.Fa / self.Sa
        self.Y = self.get_config("Y")
        if temp > self.get_config("e"):
            self.X = 0.4
        else:
            self.X = 1
            self.Y = 0
        self.set_config("Y", self.Y)

        self.Pa: float = self.get_config(
            "fp") * (self.X * self.Fa + self.get_config("Y") * self.Sa)
        self.output(["计算 A 轴承 P", "由fp、X、Fa1和Y得出：", str(self.Pa), "N"])

        temp: float = self.Fa / self.Sb
        self.Y = self.get_config("Y")
        if temp > self.get_config("e"):
            self.X = 0.4
        else:
            self.X = 1
            self.Y = 0
        self.set_config("Y", self.Y)

        self.Pb: float = self.get_config(
            "fp") * (self.X * self.Fa + self.get_config("Y") * self.Sb)
        self.output(["计算 B 轴承 P", "由fp、X、Fa1和Y得出：", str(self.Pb), "N"])

    '''
    计算轴承寿命
    '''

    def __Calculate_bearing_life(self) -> None:
        self.La: float = (pow(10, 5) / (60 * self.ntemp)) * \
            pow((self.get_config("C") / self.Pa), 10 / 3)
        self.output(["轴承 A 计算 L", "由C和P得出：", str(self.La), "h"])
        self.Lb: float = (pow(10, 5) / (60 * self.ntemp)) * \
            pow((self.get_config("C") / self.Pb), 10 / 3)
        self.output(["轴承 B 计算 L", "由C和P得出：", str(self.Lb), "h"])

    '''
    计算深沟球轴承寿命
    '''

    def __Calculate_life_deep_groove_ball_bearings(self) -> None:
        self.__Calculate_bearing_life()
        if self.La < 38400:
            self.output(["不满足寿命要求，需要重新设计", "", ""])
            self.Pa = self.FrB
            self.__Calculate_life_deep_groove_ball_bearings()
        else:
            self.output(["满足寿命要求，需要重新设计", "", ""])

    def run(self) -> None:
        self.__Calculate_radial_load()
        self.__Calculate_axial_load()
        self.__Calculate_equivalent_dynamic_load()
        if self.TypeName != "Low-speed-bear":
            self.__Calculate_bearing_life()
        else:
            self.__Calculate_life_deep_groove_ball_bearings()


if __name__ == "__main__":
    '''
    确定电动机参数
    '''
    e = electroMotor()
    e.run()

    '''
    确定传动装置参数
    '''
    g = gearing()
    g.run()

    '''
    带轮设计计算
    '''
    p = pulley()
    p.run()

    '''
    齿轮设计计算
    '''
    ge = gear()
    ge.run()

    '''
    轴设计计算
    '''
    hss = shift("High-speed-shift")
    hss.run()

    mss = shift("Medium-speed-shift")
    mss.run()

    lss = shift("Low-speed-shift")
    lss.run()

    '''
    轴承设计计算
    '''
    b1 = bearing("High-speed-bear")
    b1.run()

    b2 = bearing("Medium-speed-bear")
    b2.run()

    b3 = bearing("Low-speed-bear")
    b3.run()
