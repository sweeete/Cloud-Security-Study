# -*- coding: utf-8 -*-
"""
07 · 异常处理与文件读写

跑法：python 07-Files-and-Exceptions/07_files_and_exceptions.py
说明：脚本会在同目录下自动创建 data/ 文件夹放示例文件
"""

from pathlib import Path

BASE = Path(__file__).parent          # 本文件所在目录（比 os.getcwd() 可靠）
DATA = BASE / "data"                  # 用 / 拼路径，pathlib 的写法
DATA.mkdir(exist_ok=True)             # 目录不存在就建，存在也不报错

print("=" * 50)
print("1. 常见异常长什么样")
print("=" * 50)

samples = [
    ("int('abc')", lambda: int("abc")),
    ("10 / 0", lambda: 10 / 0),
    ("'a' + 1", lambda: "a" + 1),
    ("{}['k']", lambda: {}["k"]),
    ("[1, 2][9]", lambda: [1, 2][9]),
    ("open('没有这个文件.txt')", lambda: open("没有这个文件.txt")),
]

for label, func in samples:
    try:
        func()
    except Exception as e:
        print(f"  {label:<28} → {type(e).__name__}: {e}")

print()
print("=" * 50)
print("2. try / except：基础用法")
print("=" * 50)


def safe_int(text):
    """把字符串转整数，失败就返回 None（不让程序崩）。"""
    try:
        return int(text)
    except ValueError:
        print(f"  语法错误：{text!r} 不是整数")
        return None


print("safe_int('42') =", safe_int("42"))
print("safe_int('3.14') =", safe_int("3.14"))


def divide(a, b):
    """捕获多种异常类型。"""
    try:
        return a / b
    except ZeroDivisionError:
        print("  除数不能为 0")
    except TypeError as e:
        print(f"  类型不对：{e}")
    return None


print("divide(10, 2) =", divide(10, 2))
print("divide(10, 0) =", divide(10, 0))
print("divide(10, 'x') =", divide(10, "x"))

print()
print("=" * 50)
print("3. 完整结构：try / except / else / finally")
print("=" * 50)


def parse_age(text):
    try:
        age = int(text)
    except ValueError:
        print("  ❌ 转换失败，走了 except")
    else:
        print(f"  ✅ 没出异常，走了 else，age = {age}")
        return age
    finally:
        # 不管成不成功都会执行：适合放收尾动作（关连接、删临时文件、写日志）
        print("  → finally：收尾动作执行完毕")


parse_age("20")
parse_age("二十")

print()
print("=" * 50)
print("4. raise 主动抛异常 + 自定义异常")
print("=" * 50)


class ScoreError(Exception):
    """自定义异常：继承 Exception 即可。"""


def check_score(score):
    if not isinstance(score, (int, float)):
        raise TypeError(f"分数必须是数字，收到 {type(score).__name__}")
    if not 0 <= score <= 100:
        raise ScoreError(f"分数必须在 0~100 之间，收到 {score}")
    return f"{score} 分，合法"


for value in [85, 120, "优秀"]:
    try:
        print("  ", check_score(value))
    except ScoreError as e:
        print("   ScoreError:", e)
    except TypeError as e:
        print("   TypeError:", e)

# assert 只用于「绝不该发生」的自检，不用来做用户输入校验
def average(nums):
    assert len(nums) > 0, "nums 不能为空"
    return sum(nums) / len(nums)


print("  average([1,2,3]) =", average([1, 2, 3]))

print()
print("=" * 50)
print("5. 文件写入与读取（with open 自动关闭）")
print("=" * 50)

text_file = DATA / "notes.txt"

# "w" 模式：文件不存在就创建，存在则清空
with open(text_file, "w", encoding="utf-8") as f:   # ← encoding 一定要写
    f.write("第一行：今天开始学 Python\n")
    f.write("第二行：异常和文件\n")
    f.writelines(["第三行：pathlib 真好用\n", "第四行：记得写 encoding\n"])

print("写入完成 →", text_file)

# 一次性读全部
with open(text_file, "r", encoding="utf-8") as f:
    content = f.read()
print("read() 结果：")
print(content)

# 逐行读（大文件的标准姿势，不会一次性载入内存）
print("逐行读（去掉换行符）：")
with open(text_file, "r", encoding="utf-8") as f:
    for index, line in enumerate(f, start=1):
        print(f"  {index}: {line.rstrip()}")     # rstrip 去掉行尾换行

# 按行读成列表
with open(text_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
print("readlines() 得到列表，共", len(lines), "行")

print()
print("=" * 50)
print("6. 追加模式 a：不会清空原内容")
print("=" * 50)

with open(text_file, "a", encoding="utf-8") as f:
    f.write("第五行：这是追加进去的\n")

print("追加后的行数:", len(text_file.read_text(encoding="utf-8").splitlines()))

print()
print("=" * 50)
print("7. pathlib：更现代的路径操作")
print("=" * 50)

print("脚本所在目录:", BASE)
print("文件是否存在:", text_file.exists())
print("文件名 parts:", text_file.name, "| 后缀:", text_file.suffix, "| 父目录名:", text_file.parent.name)
print("文件大小:", text_file.stat().st_size, "字节")

# 一次性读写（小文件很方便）
one_shot = DATA / "quick.txt"
one_shot.write_text("pathlib 一行写入\n", encoding="utf-8")
print("一行读出:", repr(one_shot.read_text(encoding="utf-8")))

# 遍历目录
print("data/ 目录内容:")
for p in sorted(DATA.iterdir()):
    print("   ", p.name)

print()
print("=" * 50)
print("8. 实战：读文件 + 异常处理（处理脏数据）")
print("=" * 50)

csv_like = DATA / "scores.txt"
csv_like.write_text("张三,88\n李四,abc\n王五,95\n赵六\n", encoding="utf-8")

total, count = 0, 0
with open(csv_like, "r", encoding="utf-8") as f:
    for line_no, line in enumerate(f, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            name, score_text = line.split(",")      # 可能 ValueError（字段不够）
            score = int(score_text)                 # 可能 ValueError（不是数字）
        except ValueError as e:
            print(f"  第 {line_no} 行数据有问题，跳过：{line!r}（{e}）")
            continue
        total += score
        count += 1

print(f"有效记录 {count} 条，平均分 {total / count:.1f}")

print()
print("=" * 50)
print("9. 读一个不存在的文件：友好提示")
print("=" * 50)

missing = DATA / "不存在.txt"
try:
    missing.read_text(encoding="utf-8")
except FileNotFoundError:
    print(f"文件 {missing.name} 不存在，先创建空文件占位")
    missing.write_text("", encoding="utf-8")
    print("已创建，再读一次:", repr(missing.read_text(encoding="utf-8")))


# ============ 动手练习 ============
# 1. safe_divide(a, b)：b 为 0 返回 None，另外用 try/except 捕获 TypeError
# 2. 用 with open 写 notes2.txt 三行，再读出来打印
# 3. 用 "a" 模式追加一行，确认原内容还在
# 4. 读不存在的文件，捕获 FileNotFoundError 给友好提示
# 5. 自定义 ScoreError：成绩不在 0~100 时抛出并打印错误信息
# 6. 进阶：读 data/scores.txt，把合法记录写进 data/clean_scores.csv
