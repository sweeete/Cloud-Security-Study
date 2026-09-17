# 05 · 函数

> 目标：会把重复逻辑抽成函数，会写带各种参数的函数。

## 知识点

1. **定义与调用**
   ```python
   def add(a, b):
       """一行说明这个函数干什么"""
       return a + b

   add(1, 2)
   ```
   - 用 `def` 定义，**函数体必须缩进**
   - 没有 `return` 时，函数返回 `None`
2. **四类参数**
   | 类型 | 写法 | 说明 |
   | :--- | :--- | :--- |
   | 位置参数 | `def f(a, b)` | 按顺序传 |
   | 默认参数 | `def f(a, b=10)` | 不传就用默认值，**要放在后面** |
   | 关键字参数 | `f(b=2, a=1)` | 调用时按名字传，顺序随意 |
   | 可变参数 | `*args` / `**kwargs` | 收集任意个位置 / 关键字参数 |
3. **返回值**
   - 多个值用逗号返回，实际是**元组**：`return min_v, max_v` → `lo, hi = f(...)`
   - 返回 `None` 表示「没有结果」，常用于「只做事、不返回」的函数
4. **作用域 LEGB**：局部 Local → 外层 Enclosing → 全局 Global → 内置 Builtin
   - 函数内读全局变量可以，**改**全局要 `global`（不建议常用）
   - 嵌套函数里改外层变量用 `nonlocal`
5. **lambda**：匿名函数，适合「只在一处用一次」的小函数
   - `sorted(words, key=lambda w: len(w))`
   - 只能写一个表达式，不能有语句
6. **文档字符串与类型标注**（现代写法）
   ```python
   def greet(name: str, times: int = 1) -> str:
       """把 name 重复 times 次打招呼"""
   ```
   - 标注**不强制检查**，但能让 IDE 提示和可读性大幅提升
7. **函数是一等对象**：可以赋值给变量、当参数传、当返回值（第 09 节装饰器的基础）

## 示例代码

| 文件 | 演示内容 |
| :--- | :--- |
| `05_functions.py` | 定义与调用、四种参数、多返回值、作用域、lambda、类型标注、默认参数陷阱 |

## 易错点

- **可变默认参数陷阱**（最经典的坑）
  ```python
  def bad(x, lst=[]):     # ❌ 这个列表只创建一次，会被所有调用共享
      lst.append(x)
      return lst

  def good(x, lst=None):  # ✅
      if lst is None:
          lst = []
      lst.append(x)
      return lst
  ```
- 忘写 `return` → 拿到 `None` 还以为是逻辑错
- `def f(a=1, b)` 这种写法非法：默认参数必须在普通参数后面
- 函数内给变量赋值会创建**局部变量**，此时读同名全局变量会 `UnboundLocalError`
- 别用函数名和内置函数重名（`sum`、`list`、`max`…）
- 函数的「第一行字符串」才是 docstring，写在别处只是普通字符串

## 动手练习

1. 写 `is_prime(n)` 判断素数，返回 bool
2. 写 `calc(a, b, op="+")`，按 op 做加减乘除，非法 op 返回 `None`
3. 写 `stats(nums)`，一次返回最小值、最大值、平均值（元组解包接收）
4. 写 `make_multiplier(n)`，返回一个「乘以 n」的函数（体会函数当返回值）
5. 用 lambda + sorted 把 `["apple", "kiwi", "banana"]` 按长度排序

## 参考

- 函数定义：https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions
- 作用域规则：https://docs.python.org/zh-cn/3/faq/programming.html#what-are-the-rules-for-local-and-global-variables-in-python
