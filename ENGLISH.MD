# Mechanical design course has calculator.
> a calculator set in mechanical design course can calculate the geometric or force and kinematic parameters of motor, transmission device, V pulley, gear, shaft and bearing.

-[mechanical design course has a calculator] (# mechanical design course has a calculator)
-[Quick Start] (# Quick Start)
-[install] (# install)
-[Run] (# Run)
-[parameter setting] (# parameter setting)
-[Transporter Parameters] (# Transporter Parameters)
-[pulley parameters] (# pulley parameters)
-[gear factor] (# gear factor)
-[axis coefficient] (# axis coefficient)
-[axis coefficient] (# axis coefficient -1)
-[example] (# example)

# # Get started quickly

# # # Install
First clone the source code using git.
Command:
```
git clone https://github.com/SongZihui-sudo/Mechanical-design-solver.git
```

This calculator is a python script, so you need python to run it. If you don't have python installed, please install python in [python official website ](https://www.python.org/).
This project uses sympy for algebraic operations, so it is necessary to install the third-party library sympy.
Console input command:
```
pip install sympy
```
Complete installation

# # # Run
Command:
```
Enter folder
cd Mechanical-design-solver

Modify config.py for configuration. Detailed configuration instructions are below.

Run script
pyhon main.py
```

# # # Parameter setting

# # # # Transporter parameters
```python
Config["T"]: int = 1000 # working shaft torque of conveyor
Config["v"]: float = 0.70 # working speed of conveyor belt
Config["D"]: float = 0.4 # drum diameter
Config["etaw"]: float = 0.98 # efficiency of working machine
Config ["LD"]: float = transmission length of 2000 # conveyor
Config["q"] = 0.1 # mass per unit length
Config ["each _ eta"]: list = [0.97, 0.91, 0.9, 0.9] # Efficiency of all levels of transmission part
Config ["range _ transmission _ ratio"]: list = [# transmission ratio range
[3, 4],
[3, 7]
]
Config["i1"]: float = 3.3 # v pulley transmission ratio range
```

# # # # pulley parameters
Select various coefficients.
```python
Config["Ka"]: float = 1.0 # working condition coefficient
Config["P0"]: float = 1.67 # rated power of single V-belt
Config["dP0"]: float = 0.169 # rated power increment of single V-belt
Config["ka"]: float = 0.92 # wrap angle correction coefficient of small pulley
Config["kl"]: float = 1.01 # band length correction coefficient
Config["V-Type"]: str = "B" # V-band type * * You need to choose it yourself according to the actual situation * *
# V belt selection data
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
```
# # # # Gear coefficient
Select various coefficients.
```python
Config["z1"]: int = 100 # default value of gear tooth number
Config["z2"]: int = 20 # default value of pinion tooth number
Config["beta"]: float = 15 # default value of helix angle
Config["Kt"]: float = 1.5 # Default value of load factor
Config["ZH"]: float = 2.433 # Default value of regional coefficient
Config["varphi_d"]: float = 1 # default value of tooth width coefficient
Config["εα1"]: float = 0.7 # εα1 default value
Config["εα2"]: float = 0.9 # εα2 default value
Config["ZE"]: float = 180 # default value of elastic influence coefficient
Config ["σ hlim1"]: float = contact fatigue strength limit of 610 # pinion
Config ["σ hlim2"]: float = contact fatigue strength limit of 570 # gear
Config ["j"]: int = the meshing times of the same side tooth surface of 1 # gear during one revolution.
Config["Lh"]: int = 2 * 8 * 300 * 5 # gear life
Config["KHN1"]: float = 0.95 # contact fatigue life coefficient of gear wheel
Config["KHN2"]: float = 0.97 # contact fatigue life coefficient of pinion
config["u"]: int = 5
config["KA"]: float = 1
config["KV"]: float = 1.11
config["KHβ"]: float = 1.36
config["KHα"]: float = 1.40
config["KFα"]: float = 1.40
config["KFβ"]: float = 1.36
Config["Yβ"]: float = 0.88 # helix angle influence coefficient
# Tooth shape coefficient
config["YFa1"]: float = 2.724
config["Yfa2"]: float = 2.172
# Stress correction coefficient
config["Ysa1"]: float = 1.569
config["Ysa2"]: float = 1.798
config["KFN1"]: float = 0.95
config["KFN2"]: float = 0.98
# Let [σF]
config["σF1"]: float = 500
config["σF2"]: float = 380
```
# # # # Axis coefficient
It needs to be selected according to the actual situation, taking high-speed shaft as an example.
```python
# ZL1 coupling
config["High-speed-shift"]: dict = {}
Config ["high-speed-shift"] ["a"]: float = 14 # A size gear distance from the inner wall of the box body
config["High-speed-shift"]["c"]: float = 12.5   # c
Config ["high-speed-shift"] ["s"]: float = a distance from the inner wall of 12 # box body
Config ["high-speed-shift"] ["bear"]: list = [17,40,12] # 30203 tapered roller bearing
Config ["high-speed-shift"] ["A0"]: float = 112 # A0 size
Config ["high-speed-shift"] ["ka"]: float = 1.3 # usage factor
Config ["high-speed-shift"] ["L1-2"]: float = 28 # L1-2 size
Config ["high-speed-shift"] ["L2-3"]: float = 40 # L2-3 size
config["High-speed-shift"]["L3-4"]: float = 47
config["High-speed-shift"]["L4-5"]: float = config["High-speed-shift"]["a"] + \
config["High-speed-shift"]["s"] + \
Config ["high-speed-shift"] ["bear"] [0]+50 # L4-5 size
Config ["high-speed-shift"] ["L5-6"]: float = 12 # L5-6 size
Config ["high-speed-shift"] ["L6-7"]: float = 46 # L6-7 size
Config ["high-speed-shift"] ["L7-8"]: float = 60 # L7-8 size
Config ["high-speed-shift"] ["D1-2"]: float = 14 # D1-2 size
Config ["high-speed-shift"] ["D2-3"]: float = 16 # D2-3 size
Config ["high-speed-shift"] ["D3-4"]: float = 18 # D3-4 size
Config ["high-speed-shift"] ["D4-5"]: float = 22 # D4-5 size
Config ["high-speed-shift"] ["D5-6"]: float = 24 # D5-6 size
Config ["high-speed-shift"] ["D6-7"]: float = 26 # D6-7 size
Config ["high-speed-shift"] ["D7-8"]: float = 17 # D7-8 size
Config ["high-speed-shift"] ["dquan"]: float = 25 # retaining ring diameter
Config ["High-speed-shift"] ["Lduan"]: float = 30 # retaining ring length
Config ["high-speed-shift"] ["alpha"] = 20 # angle
Config ["high-speed-shift"] ["l"] = 32 # coupling length
Config ["high-speed-shift"] ["L1"] = 27 # half coupling length
Config ["high-speed-shift"] ["L2"] = 37 # Look-up table according to bearing
Config ["high-speed-shift"] ["L3"] = 22 # Look-up table according to bearing
Config ["high-speed-shift"] ["d1"] = 12 # coupling D1
Config ["high-speed-shift"] ["h"] = 2.5 # shoulder h
```
# # # # Axis coefficient
Select some coefficients.
```python
config["High-speed-bear"]: dict = {}
Config ["high-speed-bear"] ["y"]: float = 2.5 # axial dynamic load coefficient
Config ["high-speed-bear"] ["e"]: float = 0.3 # judgment coefficient
Config ["high-speed-bear"] ["c"]: float = 44800 # basic rated dynamic load
Config ["high-speed-bear"] ["C0"]: float = 30000 # basic rated static load coefficient
config["High-speed-bear"]["fp"]: float = 1.2
```

# # Example
The same directory calculation result. txt is an example of calculation result.

![1672821062210](image/README/1672821062210.png)

The results are very long, and they are not listed one by one.
