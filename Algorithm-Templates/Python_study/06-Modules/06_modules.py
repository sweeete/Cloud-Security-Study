# -*- coding: utf-8 -*-
"""
06 · 模块与包
    import 的四种写法、导入自己的模块、标准库初体验、__name__ 的意义

跑法：python 06-Modules/06_modules.py
说明：本文件和 greet_module.py 放在同一目录，所以可以直接 import 它
"""

# ===== 1. import 的四种写法 =====
print("=" * 50)
print("1. import 的四种写法")
print("=" * 50)

# 写法一：import 模块名（推荐，来源清晰）
import math
print("math.sqrt(16) =", math.sqrt(16))
print("math.pi =", math.pi)

# 写法二：起别名（名字太长时）
import statistics as st
print("st.mean([1,2,3]) =", st.mean([1, 2, 3]))

# 写法三：from ... import 具体名字（少用几个还行）
from random import randint
print("randint(1, 6) =", randint(1, 6))

# 写法四：from ... import *（❌ 不推荐，会污染命名空间）
# from math import *    # 谁也看不出 sqrt 是哪来的

# 一次导入多个
import os, sys   # noqa: E401  （正式代码建议分行写）

print()
print("=" * 50)
print("2. 导入自己写的模块")
print("=" * 50)

import greet_module     # ← 注意：这会执行 greet_module 的模块级代码

print("模块里的常量:", greet_module.AUTHOR, greet_module.VERSION)
print("调用模块里的函数:", greet_module.greet("主人"))
print("add(3, 4) =", greet_module.add(3, 4))

# 用 from 的形式导入其中的函数
from greet_module import greet
print("from 导入后直接用:", greet("Python"))

# 再 import 一次不会重新执行模块（有缓存）
import greet_module     # 上面没有重复打印「被导入了」，说明只执行过一次

print()
print("=" * 50)
print("3. 当前文件的 __name__ 是什么？")
print("=" * 50)

print("本文件 __name__ =", __name__)
print("greet_module.__name__ =", greet_module.__name__)
print("math.__name__ =", math.__name__)
if __name__ == "__main__":
    print("→ 说明本文件是被「直接运行」的（不是被别人 import）")

print()
print("=" * 50)
print("4. 模块搜索路径 sys.path")
print("=" * 50)

for index, path in enumerate(sys.path[:5], start=1):
    print(f"  [{index}] {path or '(空)'}")

# 脚本所在目录会被自动放到 sys.path[0]，所以能直接 import 同目录的 greet_module

print()
print("=" * 50)
print("5. 标准库初体验")
print("=" * 50)

# 数学
print("math: 平方根/向下取整/阶乘 =", math.sqrt(2), math.floor(3.7), math.factorial(5))

# 统计
data = [88, 92, 79, 95]
print("statistics: 平均/中位数/标准差 =",
      round(st.mean(data), 2), st.median(data), round(st.stdev(data), 2))

# 随机（可复现：固定种子，每次结果一样）
import random
random.seed(42)
print("random: 随机整数/选择/打乱 =",
      random.randint(1, 100), random.choice(["石头", "剪刀", "布"]))

deck = list(range(1, 6))
random.shuffle(deck)
print("洗牌后:", deck)

# 系统信息
print("sys: Python 版本 =", sys.version.split()[0], "| 平台 =", sys.platform)
print("os: 当前工作目录 =", os.getcwd())

print()
print("=" * 50)
print("6. 模块只执行一次的证明")
print("=" * 50)

import importlib
import greet_module as again

print("重复导入后 id 相同 →", id(greet_module) == id(again))
print("模块已加载列表里有它 →", "greet_module" in sys.modules)
# 开发时改了模块代码想立刻生效（不推荐在生产用）
# importlib.reload(greet_module)

print()
print("=" * 50)
print("7. 常用标准库一览（详细见第 10 节）")
print("=" * 50)

modules_intro = [
    ("math", "数学函数"),
    ("random", "随机数"),
    ("statistics", "统计计算"),
    ("datetime", "日期时间"),
    ("json", "JSON 读写"),
    ("os / pathlib", "文件与路径"),
    ("re", "正则表达式"),
    ("collections", "增强容器"),
    ("sys", "解释器与参数"),
    ("time", "时间与计时"),
]
for name, desc in modules_intro:
    print(f"  {name:<16} {desc}")

print()
print("=" * 50)
print("8. pip 与虚拟环境（命令备忘，不是代码）")
print("=" * 50)

print("""
  # 安装第三方库
  python -m pip install requests

  # 查看已安装 / 卸载
  python -m pip list
  python -m pip uninstall requests

  # 导出与恢复依赖清单
  python -m pip freeze > requirements.txt
  python -m pip install -r requirements.txt

  # 虚拟环境（Windows）
  python -m venv .venv
  .venv\\Scripts\\activate
  deactivate
""")


# ============ 动手练习 ============
# 1. 把第 05 节的 is_prime 放进新建的 my_tools.py，在另一个文件里 import 使用
# 2. 在 my_tools.py 里加 if __name__ == "__main__": 自测，分别直接运行 / import，观察区别
# 3. 建包 utils/（含 __init__.py），放 string_tools.py 与 math_tools.py，从外部导入
# 4. 用 math + random 写「随机出 5 道加法题」的小脚本
