# -*- coding: utf-8 -*-
"""
08 · 面向对象
    类与实例、属性、property、继承、多态、魔术方法、dataclass

跑法：python 08-OOP/08_oop.py
"""

from dataclasses import dataclass

print("=" * 50)
print("1. 类与实例")
print("=" * 50)


class Student:
    school = "某某大学"            # 类属性：所有实例共享

    def __init__(self, name: str, score: int = 0):
        """创建实例时自动调用，用来初始化数据。"""
        self.name = name          # 实例属性
        self.score = score

    def show(self) -> str:        # 实例方法：第一个参数必须是 self
        return f"{self.name}({self.score} 分, {self.school})"

    def add_score(self, delta: int) -> None:
        self.score += delta


s1 = Student("亚美", 90)
s2 = Student("主人")
print(s1.show())          # 调用时不用自己传 self
print(s2.show())

# 改实例属性只影响自己
s1.add_score(5)
print("s1 加分后:", s1.score, "| s2 没变:", s2.score)

# 类属性可以通过类名读写
print("类属性:", Student.school, "| 实例也能读:", s2.school)

print()
print("=" * 50)
print("2. 类属性 vs 实例属性（可变对象的坑）")
print("=" * 50)


class BadRoom:
    members = []              # ❌ 类属性是 list，所有实例共享同一份


class GoodRoom:
    def __init__(self):
        self.members = []     # ✅ 每个实例各有一份


r1, r2 = BadRoom(), BadRoom()
r1.members.append("亚美")
print("BadRoom 的坑：r2 也被改了 →", r2.members)

g1, g2 = GoodRoom(), GoodRoom()
g1.members.append("亚美")
print("GoodRoom 正常：g1 =", g1.members, "| g2 =", g2.members)

print()
print("=" * 50)
print("3. @property：把方法变成属性用")
print("=" * 50)


class Circle:
    def __init__(self, radius: float):
        self._radius = radius          # 下划线表示「内部属性」

    @property
    def radius(self) -> float:         # 读的时候：circle.radius
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0:
            raise ValueError("半径必须为正数")
        self._radius = value

    @property
    def area(self) -> float:           # 计算属性：不存值，用时算
        return round(3.14159 * self._radius ** 2, 2)


c = Circle(2)
print("读取 radius:", c.radius)        # 没写括号，像访问属性
print("面积 area:", c.area)            # 自动按当前半径算
c.radius = 3                           # 走 setter，带校验
print("改半径后 area:", c.area)

try:
    c.radius = -1                      # 校验生效
except ValueError as e:
    print("非法赋值被拦下:", e)

print()
print("=" * 50)
print("4. 继承与 super()")
print("=" * 50)


class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "……"

    def intro(self) -> str:
        return f"我是 {self.name}，我说 {self.speak()}"


class Dog(Animal):
    def __init__(self, name: str, breed: str = "中华田园犬"):
        super().__init__(name)         # ← 别忘了调父类初始化
        self.breed = breed

    def speak(self) -> str:            # 重写父类方法
        return "汪汪"

    def fetch(self) -> str:            # 子类独有
        return f"{self.name} 叼回了球"


class Cat(Animal):
    def speak(self) -> str:
        return "喵～"


dog = Dog("旺财", "金毛")
cat = Cat("咪咪")
print(dog.intro())
print(cat.intro())
print("子类独有方法:", dog.fetch())
print("类型判断 isinstance(dog, Animal) →", isinstance(dog, Animal))

print()
print("=" * 50)
print("5. 多态：同一个方法名，不同表现")
print("=" * 50)

for animal in [dog, cat, Animal("神秘生物")]:
    print(f"  {animal.name}: {animal.speak()}")

print()
print("=" * 50)
print("6. 魔术方法")
print("=" * 50)


class Book:
    def __init__(self, title: str, pages: int):
        self.title = title
        self.pages = pages

    def __str__(self) -> str:
        """给人看的：print(book)"""
        return f"《{self.title}》"

    def __repr__(self) -> str:
        """给开发看的：在列表里、调试时显示"""
        return f"Book(title={self.title!r}, pages={self.pages})"

    def __len__(self) -> int:
        """len(book)"""
        return self.pages

    def __eq__(self, other) -> bool:
        """== 比较：页数相同就算相等"""
        return isinstance(other, Book) and self.pages == other.pages

    def __lt__(self, other) -> bool:
        """< 比较：按页数排序"""
        return self.pages < other.pages


b1 = Book("Python入门", 300)
b2 = Book("算法图解", 300)
b3 = Book("大部头", 800)

print("__str__  :", b1)
print("__repr__ :", repr(b1))
print("放到列表里显示的是 __repr__ :", [b1, b3])
print("__len__  :", len(b1))
print("__eq__   : b1 == b2 →", b1 == b2, "| b1 == b3 →", b1 == b3)
print("__lt__   : 排序 →", [b.title for b in sorted([b3, b1, b2])])

# __call__：让实例能像函数一样调用
class Counter:
    def __init__(self):
        self.n = 0

    def __call__(self) -> int:
        self.n += 1
        return self.n


counter = Counter()
print("__call__ :", counter(), counter(), counter())   # 1 2 3

print()
print("=" * 50)
print("7. classmethod / staticmethod")
print("=" * 50)


class Date:
    def __init__(self, year: int, month: int, day: int):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_string(cls, text: str) -> "Date":
        """备用构造器：cls 就是类本身。"""
        y, m, d = map(int, text.split("-"))
        return cls(y, m, d)

    @staticmethod
    def is_leap(year: int) -> bool:
        """和类相关的工具函数，不需要实例也不需要类。"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02d}-{self.day:02d}"


d = Date.from_string("2026-09-17")
print("classmethod 构造:", d)
print("staticmethod 调用:", Date.is_leap(2024), Date.is_leap(2026))

print()
print("=" * 50)
print("8. dataclass：装数据的类，少写样板代码")
print("=" * 50)


@dataclass
class Point:
    x: int
    y: int

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


p1, p2 = Point(0, 0), Point(3, 4)
print("自动生成的 __repr__:", p1)
print("自动生成的 __eq__  :", p1 == Point(0, 0))
print("距离:", p1.distance_to(p2))       # 5.0

print()
print("=" * 50)
print("9. 组合：一个类用另一个类的对象")
print("=" * 50)


class Engine:
    def start(self) -> str:
        return "引擎启动"


class Car:
    def __init__(self, brand: str):
        self.brand = brand
        self.engine = Engine()          # 组合：把别的对象当零件装进来

    def run(self) -> str:
        return f"{self.brand}: {self.engine.start()}，出发！"


print(Car("比亚迪").run())


# ============ 动手练习 ============
# 1. Rectangle(width, height)：area() / perimeter() / __str__ 输出 Rectangle(3x4)
# 2. 给 Rectangle 加 @property 的只读属性 is_square
# 3. Animal.speak() 的 Dog / Cat 版本，用循环体验多态
# 4. @dataclass 定义 Point + 两点距离
# 5. ShoppingCart：add_item / remove_item / total()，并支持 len(cart)
# 6. 进阶：给 ShoppingCart 加 @classmethod from_dict()，从字典创建购物车
