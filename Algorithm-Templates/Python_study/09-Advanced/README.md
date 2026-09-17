# 09 · 进阶特性

> 目标：理解迭代协议、会写生成器、看懂装饰器、会写闭包。
> 这一节偏抽象，建议**多跑代码、多打印中间值**，别硬背。

## 知识点

1. **可迭代对象 vs 迭代器**
   - 可迭代对象（iterable）：能用 `for` 遍历的，都要实现 `__iter__`
   - 迭代器（iterator）：实现 `__iter__` + `__next__`，用 `next()` 一个个取；取完抛 `StopIteration`
   - list 是可迭代对象但**不是**迭代器；`iter(lst)` 才得到迭代器
2. **生成器函数**：函数里有 `yield`，返回生成器对象
   - 每次 `next()` 执行到 `yield` 就暂停，返回值并记住现场
   - 优点：**惰性求值**，处理大文件/大数据不占内存
   - `send()` 可以往生成器里送值；`yield from` 委托给另一个生成器
3. **生成器表达式**：`(x * x for x in range(5))`——和列表推导式只差括号，但不占内存
4. **闭包**：内层函数记住了外层函数的变量（即使外层已返回）
   - 三个条件：嵌套函数 + 引用外层变量 + 外层返回内层函数
   - 经典陷阱：循环里创建闭包都用同一个变量（用默认参数 `lambda x=n:` 固定）
5. **装饰器**：接收函数、返回新函数的函数
   ```python
   def timer(func):
       @functools.wraps(func)          # 保留原函数的名字和文档
       def wrapper(*args, **kwargs):
           ...                          # 前置动作
           result = func(*args, **kwargs)
           ...                          # 后置动作
           return result
       return wrapper

   @timer
   def slow(): ...
   ```
   - `@timer` 等价于 `slow = timer(slow)`
   - **带参数的装饰器**：再套一层（三层嵌套）→ `@retry(times=3)`
   - 用途：计时、日志、缓存、权限校验、重试
6. **常用 functools**：`wraps`、`lru_cache`（缓存）、`partial`（固定部分参数）、`reduce`
7. **其他值得知道的**
   - `*` 和 `**` 在调用处解包：`func(*args, **kwargs)`
   - `enumerate` / `zip` / `any` / `all` / `sum(gen)` 与生成器搭配很好用
   - **上下文管理器**：`with` 背后的 `__enter__` / `__exit__`，可用 `contextlib.contextmanager` 简化

## 示例代码

| 文件 | 演示内容 |
| :--- | :--- |
| `09_advanced.py` | 手写迭代器、生成器与惰性求值、生成器表达式、闭包与陷阱、装饰器（含带参数和 lru_cache）、上下文管理器 |

## 易错点

- 生成器**只能遍历一次**，用完之后是空的（要重来就重新创建）
- 忘了 `@functools.wraps` → 被装饰函数的名字变成 `wrapper`，调试很痛苦
- 闭包在循环里捕获变量是**引用**不是值 → 所有闭包最终都指向最后一次的值
- 装饰器要写 `*args, **kwargs`，否则被装饰函数带参数就报错
- `lru_cache` 的参数必须可哈希（不能缓存 list / dict 参数）
- 迭代器里同时用 `next()` 和 `for` 遍历同一个对象，容易搞乱状态

## 动手练习

1. 手写一个 `Countdown` 迭代器类，`for i in Countdown(3)` 依次输出 3 2 1
2. 写生成器 `fib()` 无限产出斐波那契数列，用 `next()` 取前 10 个
3. 写生成器读取一个大文件的行（提示：`yield` 每行），对比 `readlines()` 的内存差异
4. 写闭包 `counter()`：每次调用返回递增的计数
5. 写装饰器 `@timer`，打印被装饰函数的耗时
6. 写带参数的装饰器 `@repeat(times=3)`，让函数重复执行 3 次

## 参考

- 迭代器与生成器：https://docs.python.org/zh-cn/3/tutorial/classes.html#generators
- functools：https://docs.python.org/zh-cn/3/library/functools.html
- contextlib：https://docs.python.org/zh-cn/3/library/contextlib.html
