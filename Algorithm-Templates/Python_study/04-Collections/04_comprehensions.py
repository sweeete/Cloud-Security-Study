# -*- coding: utf-8 -*-
"""
04 · 推导式（comprehensions）
    一行生成列表 / 字典 / 集合，比 for 循环更 Pythonic

跑法：python 04-Collections/04_comprehensions.py
"""

print("=" * 50)
print("1. 列表推导式 vs for 循环")
print("=" * 50)

# for 写法（4 行）
squares_loop = []
for x in range(1, 6):
    squares_loop.append(x * x)

# 推导式写法（1 行），结果完全一样
squares = [x * x for x in range(1, 6)]

print("for 写法:", squares_loop)
print("推导式  :", squares)

print()
print("=" * 50)
print("2. 加条件：if 过滤 / if-else 变形")
print("=" * 50)

nums = [1, -2, 3, -4, 5, -6]

# 只保留正数（过滤，if 写在后面）
positives = [n for n in nums if n > 0]
print("过滤正数:", positives)

# 偶数（取模判断）
evens = [n for n in nums if n % 2 == 0]
print("偶数:", evens)

# 变形：正负都保留，但取绝对值（if-else 写在前面）
abs_values = [n if n > 0 else -n for n in nums]
print("绝对值:", abs_values)

# 两个条件同时过滤
scores = [95, 58, 77, 82, 43]
qualified = [s for s in scores if s >= 60 and s <= 90]
print("60~90 之间的分数:", qualified)

print()
print("=" * 50)
print("3. 处理字符串")
print("=" * 50)

words = ["  apple ", "BANANA", "", "Cherry  "]

cleaned = [w.strip() for w in words]              # 去空白
nonempty = [w.strip() for w in words if w.strip()]  # 去掉空串
lowered = [w.strip().lower() for w in words if w.strip()]
lengths = [len(w.strip()) for w in words]

print("清洗:", cleaned)
print("去掉空串:", nonempty)
print("转小写:", lowered)
print("各长度:", lengths)

sentence = "Python 是一门好用的语言"
print("取每个字的长度:", [len(ch) for ch in sentence])

print()
print("=" * 50)
print("4. 字典推导式")
print("=" * 50)

# 用两个列表配对
subjects = ["数学", "英语", "计算机"]
scores = [90, 85, 95]
score_map = {k: v for k, v in zip(subjects, scores)}
print("学科 → 分数:", score_map)

# 把原字典的 key / value 对调
inverted = {v: k for k, v in score_map.items()}
print("对调后:", inverted)

# 加条件：只保留及格的
passed = {k: v for k, v in score_map.items() if v >= 90}
print("90 分以上:", passed)

# 给每个学科加分（值做变换）
bonus = {k: v + 5 for k, v in score_map.items()}
print("各加 5 分:", bonus)

print()
print("=" * 50)
print("5. 集合推导式")
print("=" * 50)

numbers = [1, 2, 3, 4, 5, 6, 7, 8]
remainders = {n % 3 for n in numbers}          # 自动去重
print("除以 3 的余数种类:", remainders)         # {0, 1, 2}

first_letters = {w[0].upper() for w in ["apple", "avocado", "banana"]}
print("首字母集合:", first_letters)             # {'A', 'B'}

print()
print("=" * 50)
print("6. 嵌套推导式（了解即可，别写太复杂）")
print("=" * 50)

matrix = [
    [1, 2, 3],
    [4, 5, 6],
]
# 二维 → 一维（展平）
flat = [n for row in matrix for n in row]
print("展平:", flat)

# 转置（行列互换）
transposed = [[row[i] for row in matrix] for i in range(3)]
print("转置:", transposed)

# 等价于嵌套 for 的清晰写法
transposed_loop = []
for i in range(3):
    new_row = []
    for row in matrix:
        new_row.append(row[i])
    transposed_loop.append(new_row)
print("等价写法:", transposed_loop)

print()
print("=" * 50)
print("7. 什么时候别用推导式")
print("=" * 50)

# ❌ 超过一层条件 + 一层嵌套就该换回 for，可读性优先
# ✅ 只是提示：推导式适合「简单变换 + 简单过滤」

# 副作用型操作（比如 print、写文件）不要塞进推导式
# ❌ [print(n) for n in range(3)]
# ✅ 正常写循环
for n in range(3):
    print("正常循环打印:", n)


# ============ 动手练习 ============
# 1. 用推导式生成 1~20 中偶数的平方
# 2. 从 ["a", "b", "c"] 生成 {"a": 0, "b": 1, "c": 2}（提示：enumerate）
# 3. 把一段话里长度 > 3 的单词挑出来，全部转小写
# 4. 二维列表 [[1,2],[3,4]] 展平成一维
# 5. 用推导式把 [1, 2, 3, 4, 5] 变成 ["奇数", "偶数", ...] 这样的列表
