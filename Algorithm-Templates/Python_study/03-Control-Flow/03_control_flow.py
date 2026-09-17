# -*- coding: utf-8 -*-
"""
03 · 流程控制
    if / elif / else、while、for、range、enumerate、zip、break / continue / else

跑法：python 03-Control-Flow/03_control_flow.py
"""

print("=" * 50)
print("1. if / elif / else")
print("=" * 50)

score = 85

if score >= 90:
    level = "优秀"
elif score >= 80:
    level = "良好"     # 85 命中这里，后面的不再判断
elif score >= 60:
    level = "及格"
else:
    level = "不及格"

print(f"{score} 分 → {level}")

# 条件直接写真值判断，不用写 == True
is_login = True
if is_login:
    print("已登录")

# 多个条件用 and / or / not 组合
age, has_ticket = 20, True
if age >= 18 and has_ticket:
    print("可以入场")

# 三元表达式：简单分支可以写一行
result = "成年" if age >= 18 else "未成年"
print("三元表达式结果：", result)

print()
print("=" * 50)
print("2. while 循环")
print("=" * 50)

# 经典写法：初始化 → 判断 → 更新
total = 0
i = 1
while i <= 5:
    total += i
    i += 1          # ← 千万别忘，忘了就死循环
print("1+2+3+4+5 =", total)     # 15

# 用 while 做「次数不确定」的循环（这里模拟猜数字，不真读输入）
secret = 7
guesses = [3, 9, 7, 1]     # 假装这是用户依次猜的
step = 0
while step < len(guesses):
    guess = guesses[step]
    step += 1
    if guess == secret:
        print(f"第 {step} 次猜中：{guess}")
        break
    print(f"第 {step} 次猜 {guess}，不对")
    if guess > secret:
        print("  提示：大了")
    else:
        print("  提示：小了")

print()
print("=" * 50)
print("3. for + range")
print("=" * 50)

print("range(5) →", list(range(5)))            # [0, 1, 2, 3, 4]
print("range(1, 6) →", list(range(1, 6)))      # [1, 2, 3, 4, 5] 含头不含尾
print("range(0, 10, 2) →", list(range(0, 10, 2)))   # [0, 2, 4, 6, 8] 步长
print("range(5, 0, -1) →", list(range(5, 0, -1)))   # 倒着数

# 遍历字符串
for ch in "abc":
    print("字符:", ch, end="  ")
print()

# 遍历 list
fruits = ["苹果", "香蕉", "橙子"]
for f in fruits:
    print("水果:", f)

# 只要下标的时候
for i in range(len(fruits)):
    print(f"  {i}: {fruits[i]}")

print()
print("=" * 50)
print("4. enumerate 和 zip：遍历的好搭档")
print("=" * 50)

for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")

scores = [90, 85, 77]
for fruit, sc in zip(fruits, scores):
    print(f"{fruit}：{sc} 分")

# 同时要下标又要并行遍历
for i, (fruit, sc) in enumerate(zip(fruits, scores), start=1):
    print(f"{i}) {fruit} → {sc}")

print()
print("=" * 50)
print("5. break / continue / 循环的 else")
print("=" * 50)

# continue：跳过本轮
for n in range(1, 11):
    if n % 2 == 0:
        continue          # 偶数跳过，只打印奇数
    print(n, end=" ")
print("← 只打印了奇数")

# break：提前跳出
for n in range(1, 100):
    if n % 7 == 0:
        print("1~99 中第一个能被 7 整除的数：", n)
        break

# 循环 else：没被 break 打断时才执行（常用于「找不到」的分支）
target = 13
numbers = [2, 4, 6, 8, 10]
for n in numbers:
    if n == target:
        print("找到了", target)
        break
else:
    print(f"{numbers} 里没有 {target}")     # ← 会走这里

print()
print("=" * 50)
print("6. 嵌套循环：九九乘法表")
print("=" * 50)

for i in range(1, 10):
    row = []
    for j in range(1, i + 1):
        row.append(f"{j}x{i}={i * j:2d}")
    print(" ".join(row))

print()
print("=" * 50)
print("7. pass：先占个位置")
print("=" * 50)

for n in range(3):
    if n == 1:
        pass          # 以后再来填逻辑，现在什么也不做
    print("n =", n)


# ============ 动手练习 ============
# 1. 成绩分级：>=90 优秀 / >=80 良好 / >=60 及格 / 其他 不及格
# 2. while 求 1~100 累加和
# 3. for 打印 1~20 里的偶数
# 4. 找 100 内第一个能被 7 整除的数，找到就 break
# 5. 九九乘法表打印成三角形（提示：内层 range 上界跟着外层走）
# 6. 进阶：让程序「猜」1~100 的数字，用二分法，最多猜 7 次
