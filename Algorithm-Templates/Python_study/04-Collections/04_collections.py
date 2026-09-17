# -*- coding: utf-8 -*-
"""
04 · 内置容器
    list / tuple / dict / set 的常用操作

跑法：python 04-Collections/04_collections.py
"""

print("=" * 50)
print("1. list：有序、可变、允许重复")
print("=" * 50)

nums = [3, 1, 4, 1, 5, 9, 2, 6]
print("原列表:", nums)

# --- 增 ---
nums.append(7)               # 尾部加一个元素
nums.insert(0, 0)            # 在下标 0 处插入
nums.extend([8, 8])          # 拼接另一个列表
print("增之后:", nums)

# --- 删 ---
nums.remove(8)               # 按值删第一个匹配项
last = nums.pop()            # 弹出最后一个，并返回它
first = nums.pop(0)          # 弹出指定下标
del nums[0]                  # 按位置删
print("删之后:", nums, "| 弹出的元素:", last, first)

# --- 查 ---
print("len =", len(nums))
print("最大值/最小值/总和 =", max(nums), min(nums), sum(nums))
print("3 在列表里？", 3 in nums)
print("下标 1 到 4:", nums[1:4])       # 含头不含尾
print("1 出现了", nums.count(1), "次")

# --- 排序 ---
nums.sort()                          # 原地升序，返回 None
print("sort() 升序:", nums)
nums.sort(reverse=True)              # 降序
print("降序:", nums)
print("sorted() 返回新列表，原列表不变:", sorted(nums))

words = ["banana", "apple", "Cherry"]
print("默认按字典序（大写字母排前面）:", sorted(words))
print("按长度排:", sorted(words, key=len))
print("忽略大小写排:", sorted(words, key=str.lower))

# --- 遍历 ---
for index, value in enumerate(nums[:3], start=1):
    print(f"  第 {index} 个: {value}")

# --- 反转与拷贝 ---
a = [1, 2, 3]
b = a                 # 只是多了一个名字，指向同一个列表！
c = a.copy()          # 真正的浅拷贝
b.append(99)
print("a =", a, "  ← a 被改了，因为 b 和 a 是同一个对象")
print("c =", c, "  ← copy 出来的没被影响")

print()
print("=" * 50)
print("2. tuple：有序、不可变")
print("=" * 50)

point = (3, 5)
print("元组:", point, "| 第 0 项:", point[0])

single = (1,)      # ← 一个元素的元组必须带逗号
not_tuple = (1)    # 这只是整数 1
print("type((1,)) =", type(single), "| type((1)) =", type(not_tuple))

# 解包：把元组里的值分给变量
x, y = point
print(f"解包后 x={x}, y={y}")

# 用 * 收集剩余元素
first, *rest = (1, 2, 3, 4)
print("first =", first, "rest =", rest)

# 元组常用于「不会被改的数据」和字典的 key
locations = {(31.2, 121.4): "上海", (39.9, 116.4): "北京"}
print("坐标查询:", locations[(31.2, 121.4)])

print()
print("=" * 50)
print("3. dict：键值对")
print("=" * 50)

student = {"name": "亚美", "age": 24, "city": "上海"}
print("字典:", student)

# --- 增 / 改 ---
student["python"] = "学习中"        # 键不存在 = 新增
student["age"] = 25                 # 键已存在 = 修改
print("增改之后:", student)

# --- 查 ---
print('student["name"] =', student["name"])
print('get("不存在的键", "默认值") =', student.get("不存在的键", "默认值"))
print("直接取不存在的键会 KeyError（这里注释掉了）")

# --- 删 ---
removed = student.pop("python")     # 弹出并返回
print("pop 掉的值:", removed, "| 剩下:", student)
student["temp"] = 1
del student["temp"]                 # 直接删

# --- 遍历 ---
for key in student:
    print("  键:", key)
for key, value in student.items():
    print(f"  {key} → {value}")

keys = list(student.keys())
values = list(student.values())
print("所有键:", keys)
print("所有值:", values)

# --- 合并 ---
extra = {"height": 165, "city": "杭州"}   # city 会覆盖前面的
merged = student | extra                  # 3.9+ 的写法
print("合并后:", merged)

# --- 嵌套：字典里放列表、列表里放字典 ---
class_scores = {
    "数学": [90, 85, 77],
    "英语": [88, 92, 79],
}
for subject, scores in class_scores.items():
    print(f"{subject}: 平均 {sum(scores) / len(scores):.1f}")

print()
print("=" * 50)
print("4. set：去重 + 集合运算")
print("=" * 50)

raw = [1, 2, 2, 3, 3, 3, 4]
unique = set(raw)
print("原列表:", raw)
print("去重后:", unique)

s = {1, 2, 3}
s.add(4)
s.discard(1)          # 不存在也不会报错（remove 会报 KeyError）
print("add/discard 后:", s)
print("空集合要写 set()，写 {} 是空字典：", type(set()), type({}))

A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
print("A | B 并集:", A | B)      # {1, 2, 3, 4, 5, 6}
print("A & B 交集:", A & B)      # {3, 4}
print("A - B 差集:", A - B)      # {1, 2}
print("A ^ B 对称差:", A ^ B)    # {1, 2, 5, 6}
print("A 是 B 的子集？", {1, 2}.issubset(A))

# 成员判断：set 是哈希表，比 list 快很多
big_list = list(range(10000))
big_set = set(big_list)
print("9999 in big_set →", 9999 in big_set)

print()
print("=" * 50)
print("5. 小例子：词频统计")
print("=" * 50)

sentence = "the quick brown fox jumps over the lazy dog the fox"
counter = {}
for word in sentence.split():
    counter[word] = counter.get(word, 0) + 1

# 按出现次数从多到少排序
top = sorted(counter.items(), key=lambda item: item[1], reverse=True)
for word, times in top[:3]:
    print(f"  {word}: {times} 次")


# ============ 动手练习 ============
# 1. [3, 1, 4, 1, 5, 9, 2, 6]：去重、排序、最大值、平均值
# 2. 统计一句话里每个单词出现次数，按次数降序打印前 3
# 3. 两个列表求交集、并集、差集
# 4. 用推导式生成 1~20 中偶数的平方
# 5. [("数学", 90), ("英语", 85)] → {"数学": 90, "英语": 85}
# 6. 写函数：输入 {"张三": 88, "李四": 92}，返回分数最高的人名
