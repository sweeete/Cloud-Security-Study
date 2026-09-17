# 08 · 面向对象

> 目标：会定义类、写方法、用继承，理解「属性 / 方法 / 实例 / 类」。

## 知识点

1. **类与实例**
   ```python
   class Student:
       school = "某某大学"          # 类属性：所有实例共享

       def __init__(self, name, score):
           self.name = name         # 实例属性
           self.score = score

       def show(self):              # 实例方法，第一个参数必须是 self
           return f"{self.name}: {self.score}"
   ```
   - `__init__` 是初始化方法（构造时自动调用），**不是**构造函数
   - `self` 指实例本身，调用时不用手写：`stu.show()`
2. **类属性 vs 实例属性**
   - 读的时候优先找实例属性，再找类属性
   - `stu.score = 90` 创建的是**实例属性**，不会影响其他实例
3. **方法三兄弟**
   | 装饰器 | 第一个参数 | 用途 |
   | :--- | :--- | :--- |
   | 普通方法 | `self` | 操作实例 |
   | `@classmethod` | `cls` | 操作类，常当「备用构造器」 |
   | `@staticmethod` | 无 | 逻辑相关但不需要实例/类 |
4. **封装与命名约定**（Python 没有真正的 private）
   - `name`：公开
   - `_name`：内部用，别从外面碰（约定）
   - `__name`：名字被改写（name mangling）成 `_类名__name`，防误用
   - `@property`：把方法伪装成属性访问，用于「计算属性」和「只读属性」
5. **继承与多态**
   - `class Dog(Animal):` 继承；`super().__init__(...)` 调父类初始化
   - 子类重写父类方法 = 多态：同一个方法名，不同对象不同表现
   - `isinstance(obj, Animal)` 判断类型
6. **常用魔术方法（dunder）**
   | 方法 | 触发时机 |
   | :--- | :--- |
   | `__init__` | 创建实例 |
   | `__str__` | `print(obj)` / `str(obj)`（给人看） |
   | `__repr__` | 调试显示 / 容器里显示（给开发看） |
   | `__len__` / `__getitem__` | `len(obj)` / `obj[0]` |
   | `__eq__` | `==` 比较 |
   | `__call__` | `obj()` 像函数一样调用 |
7. **`@dataclass`**（3.7+）：纯装数据的类自动生成 `__init__` / `__repr__` / `__eq__`
   ```python
   from dataclasses import dataclass

   @dataclass
   class Point:
       x: int
       y: int
   ```
8. **什么时候用类**：有「状态 + 行为」要一起维护时。只是装数据的，用 dict / dataclass 就够了

## 示例代码

| 文件 | 演示内容 |
| :--- | :--- |
| `08_oop.py` | 类与实例、类属性 vs 实例属性、property、继承与 super、多态、魔术方法、staticmethod / classmethod、dataclass、组合 |

## 易错点

- 忘写 `self`（定义或调用时）→ 报参数个数不对
- 类属性是**可变对象**（如 `items = []`）时，所有实例共享同一份 → 大坑，改放 `__init__` 里
- 忘调 `super().__init__()` → 父类属性没初始化，后面莫名其妙 `AttributeError`
- 直接改 `_name` 约定属性，绕过了校验逻辑
- `__str__` 和 `__repr__` 混用：`print` 走 `__str__`，列表里显示走 `__repr__`
- 定义了 `__eq__` 就想想要不要一起定义 `__hash__`（否则实例不能当 dict key）

## 动手练习

1. 写 `Rectangle` 类：有 `width` / `height`，提供 `area()` 和 `perimeter()`，`__str__` 打印成 `Rectangle(3x4)`
2. 给 `Rectangle` 加 `@property` 的只读属性 `is_square`
3. 写父类 `Animal.speak()`，子类 `Dog` / `Cat` 各自重写，用循环调用体验多态
4. 用 `@dataclass` 定义 `Point`，实现「两点距离」的方法
5. 写 `ShoppingCart`：能 `add_item`、`remove_item`、算总价，用 `__len__` 支持 `len(cart)`

## 参考

- 类：https://docs.python.org/zh-cn/3/tutorial/classes.html
- dataclasses：https://docs.python.org/zh-cn/3/library/dataclasses.html
