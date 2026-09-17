# -*- coding: utf-8 -*-
"""
09 · 进阶特性
    迭代器、生成器、闭包、装饰器、上下文管理器

跑法：python 09-Advanced/09_advanced.py
"""

import functools
import time
from contextlib import contextmanager

print("=" * 50)
print("1. 可迭代对象 vs 迭代器")
print("=" * 50)

nums = [1, 2, 3]
print("list 能用 for，但它是可迭代对象，不是迭代器 →", hasattr(nums, "__next__"))

it = iter(nums)                       # 用 iter() 得到迭代器
print("iter(list) 才有 __next__ →", hasattr(it, "__next__"))
print("next(it) =", next(it))
print("next(it) =", next(it))
print("next(it) =", next(it))
# print(next(it))   # 取消注释会 StopIteration：取完了

# for 循环的本质
print("for 循环其实就是：iter() + 反复 next() + 捕获 StopIteration")


# 手写一个迭代器类
class Countdown:
    """倒计时迭代器：for i in Countdown(3) → 3 2 1"""

    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self                    # 迭代器返回自己

    def __next__(self):
        if self.current <= 0:
            raise StopIteration        # 取完必须抛这个异常
        value = self.current
        self.current -= 1
        return value


print("手写迭代器:", [n for n in Countdown(3)])

print()
print("=" * 50)
print("2. 生成器函数：有 yield 就是生成器")
print("=" * 50)


def countdown_gen(start: int):
    """和上面的类完全等价，但短得多。"""
    while start > 0:
        yield start        # ← 执行到这里「暂停」，把值交出去
        start -= 1


print("生成器版本:", list(countdown_gen(3)))

gen = countdown_gen(3)
print("第一次 next:", next(gen))     # 每次 next 从上次暂停处继续
print("第二次 next:", next(gen))

# 生成器是「惰性」的：不取就不算
def verbose_square(n):
    for i in range(n):
        print(f"    (正在计算 {i})")
        yield i * i


print("惰性求值演示：")
squares = verbose_square(3)
print("  创建生成器时什么都没发生")
print("  逐个取：")
print("   得到", next(squares))
print("   得到", next(squares))

# 用 for 一次性消费
print("  for 消费剩余:", [v for v in squares])

# 生成器只能遍历一次
print("  再遍历一次是空的:", list(squares))

print()
print("=" * 50)
print("3. 生成器实战：读大文件、管道式处理")
print("=" * 50)


def read_lines(path):
    """逐行产出文件内容，不会一次性把整个文件读进内存。"""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


def only_valid(lines):
    """过滤：产出非空行。"""
    for line in lines:
        if line.strip():
            yield line


def to_numbers(lines):
    """转换：把每行转成数字，脏数据跳过。"""
    for line in lines:
        try:
            yield int(line)
        except ValueError:
            print(f"    跳过脏数据: {line!r}")


from pathlib import Path

base = Path(__file__).parent
tmp = base / "numbers.txt"
tmp.write_text("10\n\n20\nabc\n30\n", encoding="utf-8")

# 三个生成器串成流水线，全程不占额外内存
pipeline = to_numbers(only_valid(read_lines(tmp)))
print("流水线结果:", list(pipeline))

print()
print("=" * 50)
print("4. 生成器表达式（把 [ ] 换成 ( )）")
print("=" * 50)

list_comp = [x * x for x in range(5)]
gen_expr = (x * x for x in range(5))

print("列表推导式:", list_comp, "| 类型:", type(list_comp).__name__)
print("生成器表达式:", gen_expr, "| 类型:", type(gen_expr).__name__)
print("展开后:", list(gen_expr))

# 生成器适合做「一次性汇总」，不用建中间列表
print("生成器求和:", sum(x * x for x in range(5)))
print("any / all:", any(x > 3 for x in range(5)), all(x >= 0 for x in range(5)))

print()
print("=" * 50)
print("5. 闭包：内层函数记住了外层变量")
print("=" * 50)


def make_counter():
    count = 0

    def step():
        nonlocal count        # 要修改外层的 count
        count += 1
        return count

    return step               # 返回的是「函数 + 它记住的 count」


c1 = make_counter()
c2 = make_counter()           # 各自有独立的 count
print("c1:", c1(), c1(), c1())
print("c2:", c2())

# 闭包经典陷阱：循环变量是「引用」
funcs_bad = [lambda: n for n in range(3)]
print("陷阱（全是 2）:", [f() for f in funcs_bad])

funcs_good = [lambda n=n: n for n in range(3)]     # 用默认参数把当前值绑住
print("正确（0 1 2）:", [f() for f in funcs_good])

print()
print("=" * 50)
print("6. 装饰器：给函数加功能，不改函数本身")
print("=" * 50)


def timer(func):
    """计时装饰器：前置记时间，后置算耗时。"""
    @functools.wraps(func)            # 保留原函数的名字/docstring（很重要）
    def wrapper(*args, **kwargs):     # 万能签名，支持任意参数
        start = time.perf_counter()
        result = func(*args, **kwargs)
        cost = (time.perf_counter() - start) * 1000
        print(f"    [{func.__name__}] 耗时 {cost:.2f} ms")
        return result
    return wrapper


@timer
def slow_sum(n: int) -> int:
    """累加 0~n-1。"""
    return sum(range(n))


print("调用被装饰的函数：")
print("    结果:", slow_sum(1_000_00))
print("    函数名没被覆盖:", slow_sum.__name__)
print("    docstring 还在:", slow_sum.__doc__)

# @timer 等价于手工包装
def raw_func(x):
    return x * 2


wrapped = timer(raw_func)
print("手工包装也成立:", wrapped(3))


def log_calls(func):
    """日志装饰器：每次调用都记一笔。"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"    → 调用 {func.__name__}({args}, {kwargs})")
        return func(*args, **kwargs)
    return wrapper


@log_calls
def add(a, b=0):
    return a + b


add(1, 2)
add(1, b=5)

print()
print("=" * 50)
print("7. 带参数的装饰器（三层嵌套）")
print("=" * 50)


def repeat(times: int):
    """最外层收装饰器参数，中间层收函数，最内层收调用参数。"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for i in range(times):
                result = func(*args, **kwargs)
                print(f"    第 {i + 1}/{times} 次执行完成")
            return result
        return wrapper
    return decorator


@repeat(times=3)
def say(text):
    print(f"    {text}")
    return text


say("你好呀")


def retry(times: int = 3, delay: float = 0.0):
    """失败自动重试——真实项目里很常用。"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"    第 {attempt} 次失败: {e}")
                    if delay:
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator


attempts = {"count": 0}


@retry(times=3)
def unstable():
    attempts["count"] += 1
    if attempts["count"] < 3:
        raise RuntimeError("网络抖动")
    return "第 3 次终于成功"


print(unstable())

print()
print("=" * 50)
print("8. functools 常用工具")
print("=" * 50)


# lru_cache：自动缓存重复调用的结果
@functools.lru_cache(maxsize=None)
def fib(n: int) -> int:
    print(f"    (真正计算 fib({n}))")
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print("fib(10) =", fib(10))          # 递归树里的重复计算被缓存了
print("fib(10) 再来一次 =", fib(10))  # 直接命中缓存，没打印计算过程
print("缓存信息:", fib.cache_info())

# partial：固定部分参数，生成新函数
def power(base, exponent):
    return base ** exponent


square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)
print("partial 平方/立方:", square(5), cube(3))

# reduce：累积计算（对比内置 sum）
from functools import reduce
print("reduce 连乘:", reduce(lambda a, b: a * b, [1, 2, 3, 4]))

# 解包操作符 * / **
def show(a, b, c):
    return a + b + c


args = (1, 2, 3)
kwargs = {"a": 1, "b": 2, "c": 3}
print("* 解包:", show(*args), "| ** 解包:", show(**kwargs))

print()
print("=" * 50)
print("9. 上下文管理器：with 背后是什么")
print("=" * 50)


class Timer:
    """用类实现上下文管理器：__enter__ / __exit__。"""

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cost = (time.perf_counter() - self.start) * 1000
        print(f"    耗时 {self.cost:.2f} ms")
        return False          # False = 不吞异常


with Timer():
    sum(range(100_000))


@contextmanager
def section(title: str):
    """用装饰器写上下文管理器，更简洁。"""
    print(f"    === {title} 开始 ===")
    yield                     # yield 之前的收尾放上面，之后放下面
    print(f"    === {title} 结束 ===")


with section("数据加载"):
    total = sum(range(1000))
    print("    结果:", total)


# ============ 动手练习 ============
# 1. 手写 Countdown 迭代器类，for 循环输出 3 2 1
# 2. 生成器 fib() 无限产出斐波那契，next() 取前 10 个
# 3. 生成器逐行读大文件，对比 readlines() 的内存占用
# 4. 闭包 counter()：每次调用返回递增计数
# 5. 装饰器 @timer 打印耗时
# 6. 带参数装饰器 @repeat(times=3)
# 7. 进阶：@retry(times=3) + @timer 叠加使用，观察装饰顺序
