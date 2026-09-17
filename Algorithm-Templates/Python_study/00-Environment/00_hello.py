# -*- coding: utf-8 -*-
"""
00 · 环境准备 —— 第一个 Python 脚本

怎么跑：
    在 Python_study 目录下执行
        python 00-Environment/00_hello.py
"""

# ===== 1. 注释 =====
# 以 # 开头的是单行注释，Python 会直接跳过

"""
用三个双引号包起来的是「多行字符串」，
写在文件最开头时通常当作文件的说明文档（docstring）。
"""

# ===== 2. print：最基本的输出 =====
print("Hello, Python!")
print("你好，主人～")  # 字符串可以用中文

# 多个值用逗号分隔，print 会自动用空格连接
print("1 + 1 =", 1 + 1)

# sep 控制分隔符，end 控制结尾（默认是换行）
print("2026", "09", "17", sep="-")      # 2026-09-17
print("这一行不换行", end=" | ")
print("接在后面")

# ===== 3. 转义字符 =====
print("换行\n制表\t制表")        # \n 换行，\t 制表符
print("反斜杠本身要写两个：\\")   # 输出一个 \
print("他说：\"你好\"")          # 引号也可以转义

# 如果字符串里反斜杠很多（比如 Windows 路径），加 r 变成原始字符串
print(r"C:\Users\Girlorn\Desktop")  # 不会把 \U 当转义符

# ===== 4. type() 初体验 =====
# type() 返回对象的类型，调试时非常有用
print(type("文本"))   # <class 'str'>   字符串
print(type(123))      # <class 'int'>   整数
print(type(3.14))     # <class 'float'> 浮点数
print(type(True))     # <class 'bool'>  布尔值
print(type(None))     # <class 'NoneType'> 空值

# ===== 5. 交互式输入（这里注释掉，取消注释后可以玩）=====
# input() 会暂停程序等你输入，返回的永远是「字符串」
# name = input("请输入你的名字：")
# print("你好，" + name + "！")

# ===== 6. 文件是怎么被执行的 =====
# 每个 .py 文件都有一个内置变量 __name__
#   - 直接运行这个文件时，__name__ 的值是 "__main__"
#   - 被别的文件 import 时，__name__ 是模块名
# 这就是下面这个 if 的用途（第 06 节会详细讲）
if __name__ == "__main__":
    print("__name__ 的值是：", __name__)  # 直接运行时输出 __main__


# ============ 动手练习 ============
# 1. 打印三行内容，每行之间不要有多余空行
# 2. 用 sep 和 end 拼出一行 "A-B-C-D"
# 3. 打印 10 / 3 的结果，再打印 10 // 3 和 10 % 3，观察区别
# 4. 新建 practice.py，把上面的练习写进去，跑一遍
