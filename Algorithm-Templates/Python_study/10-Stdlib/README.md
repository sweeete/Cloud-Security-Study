# 10 · 常用标准库

> 目标：知道「哪个轮子在哪」，用到时能查文档、会用最常用的那几个。
> Python 的口号之一就是「**自带电池**」——标准库很全，先别急着装第三方库。

## 知识点

### 1. 路径与系统：`pathlib` / `os` / `sys`
- `pathlib.Path`：`/` 拼路径、`exists()`、`mkdir(parents=True, exist_ok=True)`、`iterdir()`、`glob("*.py")`、`read_text()` / `write_text()`
- `os`：`getcwd()`、`environ`、`listdir()`（老写法，新代码优先 `pathlib`）
- `sys`：`argv`（命令行参数）、`path`、`version`、`exit()`

### 2. 数据格式：`json` / `csv`
- `json.dumps(obj, ensure_ascii=False, indent=2)` → 字符串
- `json.loads(text)` → Python 对象
- `json.dump(obj, f, ensure_ascii=False, indent=2)` / `json.load(f)` → 直接读写文件
- **`ensure_ascii=False`** 才不会被转成 `\u4e2d` 这种转义
- `csv.reader` / `csv.writer` / `csv.DictReader` / `csv.DictWriter`

### 3. 日期时间：`datetime`
- `datetime.now()`、`date.today()`、`timedelta`（日期加减）
- 格式化：`dt.strftime("%Y-%m-%d %H:%M:%S")`
- 解析：`datetime.strptime("2026-09-17", "%Y-%m-%d")`
- 计时：`time.perf_counter()`（比 `time.time()` 更适合测耗时）

### 4. 正则：`re`（够用就行，别写太复杂）
- `re.search` 找第一个；`re.findall` 找全部；`re.sub` 替换；`re.split` 切分
- 常用元字符：`.` `\d` `\w` `\s` `*` `+` `?` `{n}` `[]` `()` `^` `$`
- **原始字符串** `r"\d+"` 一定要加 `r`，否则 `\d` 会被 Python 先处理
- `re.match` 只匹配开头，`re.search` 全文找；两者都返回 `Match` 或 `None`
- 编译复用：`pattern = re.compile(r"...")`

### 5. 增强容器：`collections`
| 工具 | 用途 |
| :--- | :--- |
| `Counter` | 计数（词频统计神器），`.most_common(n)` |
| `defaultdict` | 分组时不用先判断 key 是否存在 |
| `namedtuple` | 轻量不可变记录，可用属性名访问 |
| `deque` | 双端队列，`appendleft` / `popleft` 是 O(1) |
| `OrderedDict` | 现在普通 dict 也有序了，几乎不用了 |

### 6. 其他高频
- `random`：`randint` / `choice` / `shuffle` / `sample` / `seed`
- `math`：`sqrt` / `ceil` / `floor` / `pi` / `log` / `gcd`
- `itertools`：`chain` / `product` / `combinations` / `groupby`（组合数学常用）
- `time`：`sleep` / `perf_counter`
- `hashlib`：`md5` / `sha256`（校验文件完整性）
- `argparse`：写命令行工具（比手撸 `sys.argv` 规范）

## 示例代码

| 文件 | 演示内容 |
| :--- | :--- |
| `10_stdlib.py` | pathlib 遍历、json 读写中文、datetime 与 timedelta、re 提取手机号/邮箱、collections 四件套、itertools、hashlib、random 抽样 |

## 易错点

- `json.dumps` 忘了 `ensure_ascii=False` → 中文变 `\uXXXX`
- 正则忘了 `r` 前缀 → `\d` 报错或被转义
- `re.search` 返回的是 `Match` 对象，取内容要 `.group()`；找不到返回 `None`，不判空就 `AttributeError`
- `strftime` / `strptime` 的格式串容易记混：`%m` 是月、`%M` 是分，`%H` 小时、`%d` 日
- `defaultdict(int)` 会给每个不存在的 key 建默认值，用错容器会「凭空多出 key」
- `hashlib.md5()` 的入参必须是 **bytes**，字符串要先 `.encode()`

## 动手练习

1. 遍历当前目录下所有 `.py` 文件，打印文件名和大小
2. 把一个字典写成 `config.json`，再读回来，检查中文是否正常
3. 用 `datetime` 算：距离 2027-01-01 还有多少天；把今天格式化成 `2026年09月17日`
4. 用正则从一段文本里提取所有手机号和邮箱
5. 用 `Counter` 统计一段英文里出现最多的 5 个单词
6. 用 `defaultdict(list)` 把 `[("水果","苹果"), ("蔬菜","白菜"), ("水果","香蕉")]` 按类别分组

## 参考

- 标准库索引：https://docs.python.org/zh-cn/3/library/index.html
- collections：https://docs.python.org/zh-cn/3/library/collections.html
- re 语法：https://docs.python.org/zh-cn/3/howto/regex.html
