# -*- coding: utf-8 -*-
"""
05 · 函数
    定义、参数、返回值、作用域、lambda、类型标注

跑法：python 05-Functions/05_functions.py
"""

print("=" * 50)
print("1. 定义与调用")
print("=" * 50)


def greet(name):
    """最基础的函数：有参数、有返回值。"""
    return f"你好，{name}！"


print(greet("亚美"))
print(greet.__doc__)          # 打印函数自己的说明文档


def say_hello():
    """没有参数的函数。"""
    print("Hello!")


say_hello()


def do_nothing():
    # 没有 return 的函数，返回值是 None
    pass


print("没有 return 的函数返回：", do_nothing())

print()
print("=" * 50)
print("2. 四种参数")
print("=" * 50)


def show_info(name, age, city="上海", *hobbies, **extra):
    """
    name, age  : 位置参数（必填）
    city       : 默认参数
    *hobbies   : 可变位置参数 → 收集成元组
    **extra    : 可变关键字参数 → 收集成字典
    """
    print(f"姓名: {name}, 年龄: {age}, 城市: {city}")
    print("  爱好(元组):", hobbies)
    print("  其他(字典):", extra)


show_info("亚美", 24)
show_info("亚美", 24, "杭州")
show_info("亚美", 24, city="北京", 兴趣="写代码")
show_info("亚美", 24, "上海", "健身", "看论文", 学号="2026xxxx")

# 调用时用关键字传参，顺序可以打乱
show_info(age=24, name="亚美")


# 默认参数的值在「定义时」就算好，所以别写可变对象
def add_item_bad(item, box=[]):          # ❌ 经典陷阱
    box.append(item)
    return box


def add_item_good(item, box=None):       # ✅ 正确做法
    if box is None:
        box = []
    box.append(item)
    return box


print("陷阱示范 bad:", add_item_bad("a"), add_item_bad("b"), add_item_bad("c"))
# 三次调用返回的都是同一个列表 → ['a', 'b', 'c']
print("正确写法 good:", add_item_good("a"), add_item_good("b"), add_item_good("c"))

print()
print("=" * 50)
print("3. 返回值：可以返回多个")
print("=" * 50)


def min_max(nums):
    """同时返回最小值和最大值（实际返回的是元组）。"""
    return min(nums), max(nums)


result = min_max([3, 1, 4, 1, 5])
print("整体接收:", result, "| 类型:", type(result))

low, high = min_max([3, 1, 4, 1, 5])     # 元组解包
print("解包接收:", low, high)


def divide(a, b):
    """出错时返回 None，让调用方自己判断——比直接抛异常更宽松。"""
    if b == 0:
        return None
    return a / b


print("divide(10, 2) =", divide(10, 2))
print("divide(10, 0) =", divide(10, 0), "← 返回 None，调用方要判空")

print()
print("=" * 50)
print("4. 作用域：LEGB")
print("=" * 50)

counter = 0          # 全局变量


def read_global():
    """只读全局变量：不需要声明。"""
    print("  读到全局 counter =", counter)


def modify_global():
    """要修改全局变量，必须加 global。"""
    global counter
    counter += 1


read_global()
modify_global()
print("修改后 counter =", counter)


def outer():
    """嵌套函数演示 nonlocal。"""
    total = 0

    def inner():
        nonlocal total       # 声明「改的是外层的 total」
        total += 1
        return total

    return inner()


print("nonlocal 结果:", outer())


def local_demo():
    # 函数内赋值会让变量变成局部的，所以下面这句会 UnboundLocalError
    # print(counter)
    # counter = 100
    inner_var = "只在这个函数里存在"
    return inner_var


print("局部变量:", local_demo())
# print(inner_var)   # 取消注释会 NameError：外面访问不到

print()
print("=" * 50)
print("5. lambda：小到不值得起名字的函数")
print("=" * 50)

double = lambda x: x * 2          # 一般不这么用，赋值给变量反而降低可读性
print("lambda 赋值:", double(5))

# 真正的用途：当「排序 / 过滤的临时规则」
words = ["apple", "kiwi", "banana", "fig"]
print("按长度排序:", sorted(words, key=lambda w: len(w)))
print("按最后一个字母排序:", sorted(words, key=lambda w: w[-1]))

people = [("亚美", 24), ("主人", 20), ("小明", 30)]
print("按年龄排序:", sorted(people, key=lambda p: p[1]))
print("按年龄取最大:", max(people, key=lambda p: p[1]))

nums = [-3, 1, -5, 8]
print("按绝对值排序:", sorted(nums, key=lambda n: abs(n)))
print("过滤出正数:", list(filter(lambda n: n > 0, nums)))
print("每个数平方:", list(map(lambda n: n * n, nums)))
# 注意：map / filter 更常见的是写成推导式 → [n * n for n in nums]

print()
print("=" * 50)
print("6. 类型标注和文档字符串")
print("=" * 50)


def average(nums: list[float], ndigits: int = 2) -> float:
    """
    计算平均值。

    参数:
        nums     : 数字列表
        ndigits  : 保留小数位，默认 2

    返回:
        平均值（float）；空列表时返回 0.0
    """
    if not nums:
        return 0.0
    value = sum(nums) / len(nums)
    return round(value, ndigits)


print(average([90, 85, 77]))          # 84.0
print(average([1, 2], ndigits=4))     # 1.5
print("标注只是提示，传错类型运行时不一定报错 →", average([1, 2], 4))
print("查看标注:", average.__annotations__)

print()
print("=" * 50)
print("7. 函数是一等对象")
print("=" * 50)


def apply_twice(func, value):
    """函数可以作为参数传进来。"""
    return func(func(value))


print("apply_twice(double, 3) =", apply_twice(double, 3))   # 12


def make_multiplier(n: int):
    """函数也可以作为返回值（闭包，详见第 09 节）。"""
    def multiply(x):
        return x * n
    return multiply


triple = make_multiplier(3)
print("triple(7) =", triple(7))


# ============ 动手练习 ============
# 1. is_prime(n) → bool
# 2. calc(a, b, op="+")：支持 + - * /，非法 op 返回 None
# 3. stats(nums) → (最小值, 最大值, 平均值)
# 4. make_multiplier(n) → 返回「乘以 n」的函数
# 5. lambda + sorted：把 ["apple", "kiwi", "banana"] 按长度排序
# 6. 给 is_prime 加上类型标注和 docstring
