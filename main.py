'''
机械设计参数计算器
'''
import config
import math


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
        print("步骤: %s -> %s -> res = %s" % (arg[0], step, res))


'''
电动机参数确定 子类
'''


class electroMotor(calculation):
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

    def run(self):
        self.__total_transmission_ratio_cal()
        self.__distribution_transmission_ratios()
        self.__input_speed_shaft()
        self.__input_power_shaft()
        self.__input_torque_shaft()


'''
带轮设计计算
'''


class pulley(calculation):
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
        self.type: str = ""
        min: float = 999999.0
        for cur in self.get_config("type_linear_coefficient").values():
            distance: float = euclidean_distance(
                cur["k"], cur["b"], point(self.Pca, self.n))
            if distance < min:
                min = distance
                self.type = cur["type"]
        self.output(["带轮型号：", "根据Pca", " n", self.type, "型V带轮"])

    '''
    确定效率直径
    '''

    def __diameter_small_pulley(self) -> None:
        range: list = self.get_config("type_linear_coefficient")[
                                      self.type]["range"]
        self.dd1: float = (range[0] + range[1]) / 2
        self.set_config("dd1", self.dd1)
        self.output(["确定小轮直径", "由", self.type, "型V带轮得出：", str(self.dd1), "mm"])

    '''
    验算带速
    '''

    def __belt_speed(self) -> None:
        pass

    '''
    确定大轮直径
    '''

    def __diameter_large_pulley(self) -> None:
        pass

    '''
    计算中心距
    '''

    def __center_distance(self) -> None:
        pass

    '''
    计算基准长度
    '''

    def __datum_length(self) -> None:
        pass

    '''
    计算小带轮包角
    '''

    def __small_pulley_wrap_angle(self) -> None:
        pass

    '''
    单根V带的额定功率
    '''

    def __rated_power_single_belt(self) -> None:
        pass

    '''
    计算带的根数
    '''

    def __belt_root_number(self) -> None:
        pass

    '''
    计算单根V带的最小拉力
    '''

    def __min_value_initial_tension_belt(self) -> None:
        pass

    '''
    计算压轴力
    '''

    def __axial_force(self) -> None:
        pass

    def run(self) -> None:
        self.__inputPower()
        self.__selection_pulley()
        self.__diameter_small_pulley()


'''
点到直线的距离
'''


def euclidean_distance(k: float, h: float, val: point) -> float:
    x = val.x
    y = val.y
    theDistance = math.fabs(h + k * (x - 0) - y) / (math.sqrt(k * k + 1))
    return theDistance


'''
计算步骤
'''

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
