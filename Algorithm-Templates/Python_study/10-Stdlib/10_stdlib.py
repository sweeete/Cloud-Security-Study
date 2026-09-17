# -*- coding: utf-8 -*-
"""
10 · 常用标准库
    pathlib / json / datetime / re / collections / itertools / hashlib / random

跑法：python 10-Stdlib/10_stdlib.py
说明：会在同目录下自动创建 data/ 存放示例文件
"""

import hashlib
import json
import random
import re
from collections import Counter, defaultdict, deque, namedtuple
from datetime import date, datetime, timedelta
from itertools import chain, combinations, groupby, product
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)

print("=" * 50)
print("1. pathlib：路径与文件")
print("=" * 50)

print("当前脚本目录:", BASE.name)
print("拼路径:", BASE / "data" / "demo.json")

# 遍历当前目录下的 .py 文件
py_files = sorted(BASE.glob("*.py"))
print("同目录的 .py 文件:")
for p in py_files:
    print(f"    {p.name:<22} {p.stat().st_size:>6} 字节")

# 用 / 拼接、创建多级目录
nested = DATA / "a" / "b"
nested.mkdir(parents=True, exist_ok=True)
print("多级目录创建成功:", nested.relative_to(BASE))

print()
print("=" * 50)
print("2. json：结构化数据读写")
print("=" * 50)

config = {
    "name": "亚美",
    "version": 1,
    "tags": ["python", "学习"],
    "nested": {"debug": True, "level": 3},
}

# 转成字符串（注意 ensure_ascii=False，否则中文会变成 \uXXXX）
text = json.dumps(config, ensure_ascii=False, indent=2)
print("dumps 结果（截取）:")
print("\n".join(text.splitlines()[:4]))

# 字符串转回对象
back = json.loads(text)
print("loads 后取嵌套值:", back["nested"]["level"])

# 直接读写文件
json_file = DATA / "config.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
with open(json_file, "r", encoding="utf-8") as f:
    loaded = json.load(f)
print("从文件读回:", loaded["name"], loaded["tags"])

print()
print("=" * 50)
print("3. datetime：日期与时间")
print("=" * 50)

now = datetime.now()
today = date.today()
print("现在:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("今天:", today, "| 星期:", today.isoweekday(), "（1=周一）")

# 日期加减
tomorrow = today + timedelta(days=1)
week_ago = today - timedelta(days=7)
new_year = date(2027, 1, 1)
print("明天:", tomorrow, "| 一周前:", week_ago)
print("距离 2027-01-01 还有", (new_year - today).days, "天")

# 格式化与解析
formatted = today.strftime("%Y年%m月%d日")
parsed = datetime.strptime("2026-09-17", "%Y-%m-%d")
print("中文格式:", formatted)
print("解析字符串:", parsed, "| 星期几:", parsed.strftime("%A"))

# 计时用 perf_counter
import time
start = time.perf_counter()
total = sum(range(500_000))
cost = (time.perf_counter() - start) * 1000
print(f"累加 50 万个数耗时 {cost:.2f} ms，结果 {total}")

print()
print("=" * 50)
print("4. re：正则表达式（记住要加 r 前缀）")
print("=" * 50)

text = """
联系方式：张三 13812345678，邮箱 zhangsan@example.com
李四 15900001111，邮箱 lisi@test.org.cn
座机 021-12345678（这个不是手机号）
"""

phones = re.findall(r"1[3-9]\d{9}", text)
emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
print("手机号:", phones)
print("邮箱:", emails)

# search 找第一个，返回 Match 对象或 None
match = re.search(r"(\d{4})-(\d{4})", "座机 021-12345678")
if match:
    print("search 找到:", match.group(), "| 分组:", match.group(1), match.group(2))

# sub 替换 / split 切分
print("脱敏:", re.sub(r"1[3-9]\d{9}", "***********", text.split("\n")[1]))
print("按逗号或空格切:", re.split(r"[,\s]+", "a, b,c  d"))

# 编译后复用（批量处理时更快）
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
print("compile 复用:", EMAIL_RE.findall("x@a.com y@b.cn"))

print()
print("=" * 50)
print("5. collections：四个好用的容器")
print("=" * 50)

# Counter：计数
sentence = "the quick brown fox jumps over the lazy dog the fox"
word_count = Counter(sentence.split())
print("出现最多的 3 个词:", word_count.most_common(3))
print("'the' 出现次数:", word_count["the"])

# defaultdict：分组不用先判断 key
pairs = [("水果", "苹果"), ("蔬菜", "白菜"), ("水果", "香蕉"), ("蔬菜", "萝卜")]
groups = defaultdict(list)
for category, item in pairs:
    groups[category].append(item)
print("分组结果:", dict(groups))

# namedtuple：有名字的元组
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(f"namedtuple: p.x={p.x}, p.y={p.y}, 也可以用下标 p[0]={p[0]}")

# deque：双端队列
queue = deque([1, 2, 3])
queue.appendleft(0)
queue.append(4)
print("deque:", queue, "| popleft:", queue.popleft(), "| pop:", queue.pop())

print()
print("=" * 50)
print("6. itertools：排列组合与迭代工具")
print("=" * 50)

print("chain 拼接:", list(chain([1, 2], [3, 4])))
print("product 笛卡尔积:", list(product("AB", [1, 2])))
print("combinations 组合:", list(combinations([1, 2, 3], 2)))

# groupby 前要先按同一标准排序
students = [("一班", "张三"), ("二班", "李四"), ("一班", "王五")]
students.sort(key=lambda s: s[0])
for klass, members in groupby(students, key=lambda s: s[0]):
    print(f"  {klass}: {[m[1] for m in members]}")

print()
print("=" * 50)
print("7. hashlib：哈希（校验文件完整性）")
print("=" * 50)

content = "这是一段要校验的内容"
md5_hex = hashlib.md5(content.encode("utf-8")).hexdigest()
sha256_hex = hashlib.sha256(content.encode("utf-8")).hexdigest()
print("md5   :", md5_hex)
print("sha256:", sha256_hex[:32], "...")

# 小文件校验的写法（大文件要分块读）
target = DATA / "hash_demo.txt"
target.write_text(content, encoding="utf-8")
file_hash = hashlib.sha256(target.read_bytes()).hexdigest()
print("文件内容一致？", file_hash == sha256_hex)

print()
print("=" * 50)
print("8. random：抽样（固定 seed 可复现）")
print("=" * 50)

random.seed(2026)
print("randint:", random.randint(1, 100))
print("choice:", random.choice(["石头", "剪刀", "布"]))
print("sample 不重复抽 3 个:", random.sample(range(1, 50), 3))

deck = list(range(1, 11))
random.shuffle(deck)
print("shuffle 后:", deck)


# ============ 动手练习 ============
# 1. 遍历当前目录所有 .py，打印文件名 + 大小
# 2. 把字典写成 config.json 再读回，检查中文是否乱码
# 3. 算距离 2027-01-01 还有多少天；今天格式化成 2026年09月17日
# 4. 正则提取一段文本里的所有手机号、邮箱
# 5. Counter 统计英文中出现最多的 5 个单词
# 6. defaultdict(list) 把 (类别, 项目) 列表分组
# 7. 进阶：写一个脚本，扫描目录下所有文件并打印它们的 sha256 前 8 位
