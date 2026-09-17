# -*- coding: utf-8 -*-
"""
01 · 基础语法
    变量、数据类型、运算符、类型转换

跑法：python 01-Basics/01_basics.py
说明：每个小节都可以单独看懂，注释后面标的是这段代码的输出
"""

import math  # 后面比较浮点数要用

print("=" * 50)
print("1. 变量：赋值即创建，不用声明类型")
print("=" * 50)

age = 24            # int
height = 1.75       # float
name = "亚美"        # str
is_student = True   # bool
nothing = None      # NoneType

# 一次给多个变量赋值
x = y = 0
# 元组解包（更常用的多变量赋值）
a, b, c = 1, 2, 3
# 交换两个变量：Python 一行搞定，不需要中间变量
a, b = b, a
print("交换后 a =", a, "b =", b)          # a = 2 b = 1

# 查看类型
print(type(age), type(height), type(name), type(is_student), type(nothing))
# <class 'int'> <class 'float'> <class 'str'> <class 'bool'> <class 'NoneType'>

print()
print("=" * 50)
print("2. 数值运算")
print("=" * 50)

p, q = 7, 2
print("7 + 2 =", p + q)      # 9
print("7 - 2 =", p - q)      # 5
print("7 * 2 =", p * q)      # 14
print("7 / 2 =", p / q)      # 3.5   ← 除法结果一定是 float
print("7 // 2 =", p // q)    # 3     ← 整除（向下取整）
print("7 % 2 =", p % q)      # 1     ← 取余
print("7 ** 2 =", p ** q)    # 49    ← 幂
print("-7 // 2 =", -7 // 2)  # -4    ← 注意是向下取整，不是 -3

print()
print("浮点数陷阱：0.1 + 0.2 =", 0.1 + 0.2)          # 0.30000000000000004
print("0.1 + 0.2 == 0.3 →", 0.1 + 0.2 == 0.3)        # False
print("正确比较方式 math.isclose →", math.isclose(0.1 + 0.2, 0.3))  # True

print()
print("=" * 50)
print("3. 比较运算和逻辑运算")
print("=" * 50)

print("3 > 2 →", 3 > 2)              # True
print("3 == 3.0 →", 3 == 3.0)        # True（数值比较，不看类型）
print("0 < x < 10 →", 0 < 5 < 10)    # True ← Python 支持连写

t = True
f = False
print("True and False →", t and f)   # False
print("True or False →", t or f)     # True
print("not True →", not t)           # False

# 短路特性：and 遇到假就停，or 遇到真就停
print("0 and (1 / 0) →", 0 and (1 / 0), " ← 右边没执行，所以不会报除零错误")

print()
print("=" * 50)
print("4. 类型转换")
print("=" * 50)

s = "42"
print("int('42') + 1 =", int(s) + 1)        # 43
print('float("3.14") =', float("3.14"))      # 3.14
print('str(3.14) + "!" =', str(3.14) + "!")  # 3.14!
print("int(3.99) =", int(3.99))              # 3  ← 直接截断，不四舍五入
print("round(3.99) =", round(3.99))          # 4  ← 这个才四舍五入

# int("3.14") 会直接报错，必须先转 float
print('int(float("3.14")) =', int(float("3.14")))  # 3

print()
print("=" * 50)
print("5. 真值判断：哪些值算「假」")
print("=" * 50)

falsy = [0, 0.0, "", [], {}, set(), None, False]
for value in falsy:
    print(f"{value!r:>10} → bool 结果是 {bool(value)}")

# 实用技巧：or 设置默认值（因为 and/or 返回的是操作数本身）
user_input = ""
display_name = user_input or "匿名用户"
print("display_name =", display_name)   # 匿名用户

print()
print("=" * 50)
print("6. f-string：最常用的字符串格式化")
print("=" * 50)

print(f"{name} 今年 {age} 岁，身高 {height} 米")
print(f"保留两位小数：{3.14159:.2f}")        # 3.14
print(f"补零到 5 位：{42:05d}")              # 00042
print(f"百分比：{0.85:.1%}")                 # 85.0%
print(f"右对齐宽度 8：{'hi':>8}|")           #        hi|

# 增强赋值：Python 里没有 x++ 这种写法
count = 0
count += 1      # 等价于 count = count + 1
count *= 5
print("count =", count)   # 5


# ============ 动手练习 ============
# 1. a = 17, b = 5：打印 和/差/积/商/整除/余数/a**b
# 2. 把 "3.14" 转 float 再转 int，每一步打印类型
# 3. 只用一行代码交换 x、y
# 4. 判断 0.1+0.2 是否等于 0.3，用 isclose 得到正确答案
# 5. 让用户输入身高（字符串），转成 float，算出「米 → 厘米」，用 f-string 打印
