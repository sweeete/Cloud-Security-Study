# -*- coding: utf-8 -*-
"""
02 · 字符串
    引号、拼接、索引切片、f-string、常用方法

跑法：python 02-Strings/02_strings.py
"""

print("=" * 50)
print("1. 三种写法与拼接")
print("=" * 50)

single = '单引号也可以'
double = "双引号一样"
multi = """三引号
可以写多行
换行会保留"""

print(single, "|", double)
print(multi)
print("拼接：" + "Hello" + " " + "World")
print("重复：" + "-" * 30)          # 画分割线常用技巧
print("隐式拼接（相邻字面量自动合并）：" "看到没" "中间没加号")

# 相邻字面量拼接在写长字符串时很有用
long_text = (
    "这一段太长了，"
    "可以拆成几行写，"
    "运行时会自动拼成一句。"
)
print(long_text)

print()
print("=" * 50)
print("2. 索引与切片：含头不含尾")
print("=" * 50)

s = "Hello, Python!"
print("原串:", s)
print("长度:", len(s))              # 14
print("s[0] =", s[0])               # H
print("s[-1] =", s[-1])             # !   ← 负数从右边数
print("s[0:5] =", s[0:5])           # Hello  ← 含 0 不含 5
print("s[:5] =", s[:5])             # Hello  ← 开头可以省略
print("s[7:] =", s[7:])             # Python! ← 结尾可以省略
print("s[7:13] =", s[7:13])         # Python
print("s[::-1] =", s[::-1])         # !nohtyP ,olleH ← 反转
print("s[::2] =", s[::2])           # Hlo yhn  ← 隔一个取一个
print("s[-6:-1] =", s[-6:-1])       # Python
print("越界切片不报错:", repr(s[100:200]))  # '' 空字符串
print("但索引会报错：s[100] 会 IndexError（这里注释掉了）")

# Python 的区间用「数学半开区间」[start, end)，这个习惯贯穿所有数据结构

print()
print("=" * 50)
print("3. f-string 格式化（最常用）")
print("=" * 50)

name = "亚美"
price = 12345.6789

print(f"{name}，你好～")
print(f"保留两位小数：{price:.2f}")        # 12345.68
print(f"千分位分隔：{price:,.2f}")         # 12,345.68
print(f"右对齐宽度 12：{'abc':>12}|")
print(f"左对齐宽度 12：{'abc':<12}|")
print(f"居中宽度 12：{'abc':^12}|")
print(f"补零：{42:05d}")                   # 00042
print(f"百分比：{0.856:.1%}")              # 85.6%
print(f"十六进制：{255:#x}")               # 0xff
print(f"表达式可以直接写进去：{2 + 3 * 4}")  # 14
print(f"调试小技巧（3.8+）：{name=}")      # name='亚美'

# 老写法（见到要认识，新代码就别用了）
print("format 写法：{} 的价格是 {:.2f}".format(name, price))
print("百分号写法：%s 的价格是 %.2f" % (name, price))

print()
print("=" * 50)
print("4. 常用方法（都返回新字符串，原串不变）")
print("=" * 50)

raw = "   Hello, World!  "
print("原串:", repr(raw))
print("strip():", repr(raw.strip()))        # 'Hello, World!'
print("lower():", raw.strip().lower())      # hello, world!
print("upper():", raw.strip().upper())      # HELLO, WORLD!
print("replace():", raw.strip().replace("World", "Python"))

csv = "苹果,香蕉,橙子"
fruits = csv.split(",")                     # 按逗号切 → list
print("split(',') =", fruits)
print("join(' | ') =", " | ".join(fruits))  # 拼回去

print("find('l') =", "hello".find("l"))     # 2   第一个位置
print("find('z') =", "hello".find("z"))     # -1  找不到返回 -1
print("'ell' in 'hello' →", "ell" in "hello")           # True
print("startswith('He') →", "Hello".startswith("He"))   # True
print("endswith('!') →", "Hello!".endswith("!"))        # True
print("count('l') =", "hello".count("l"))   # 2

print("zfill(5) =", "42".zfill(5))          # 00042
print("center(11, '*') =", "标题".center(11, "*"))
print("移除前缀/后缀:", "prefix_body".removeprefix("prefix"))  # 3.9+

# 处理用户输入的经典套路：strip + 判断
user = "   "
print("清洗后为空？", not user.strip())      # True

print()
print("=" * 50)
print("5. 遍历与统计")
print("=" * 50)

sentence = "Python 是一门好用的语言"

# 直接遍历字符
vowels = "aeiou"
count = 0
for ch in sentence.lower():
    if ch in vowels:
        count += 1
print("元音字母个数：", count)

# 按单词切分统计
words = sentence.split()
print("单词列表：", words, "共", len(words), "个")

chars = {}
for ch in sentence:
    if ch != " ":
        chars[ch] = chars.get(ch, 0) + 1
print("字符统计：", chars)

print()
print("=" * 50)
print("6. 字符串不可变")
print("=" * 50)

immutable = "abc"
# immutable[0] = "x"   # 取消注释会报 TypeError
immutable = "x" + immutable[1:]   # 只能整个替换成新字符串
print("重新拼接后:", immutable)   # xbc
print("内存地址变了：", id("abc") != id(immutable))


# ============ 动手练习 ============
# 1. 从 "Hello, Python!" 取出 "Hello"、"Python" 和反转后的整串
# 2. 把 "  你好， 世界  " 清洗成 "你好，世界"（提示：strip + replace）
# 3. 用 split + join 把 "a,b,c" 变成 "a | b | c"
# 4. 统计 "the quick brown fox" 的单词数，以及字母 'o' 出现几次
# 5. 打印一张对齐的小票：商品名左对齐 10 位、价格右对齐 10 位保留 2 位小数
