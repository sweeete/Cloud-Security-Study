# 04 · 内置容器

> 目标：选对容器、会用四种容器的常用操作、会写推导式。

## 知识点

1. **list 列表**（有序、可变、允许重复）
   - 增：`append`（尾部加一个）、`extend`（拼接另一个序列）、`insert(i, x)`
   - 删：`pop()` / `pop(i)`、`remove(值)`、`del lst[i]`、`clear()`
   - 查：索引、切片、`in`、`index()`、`count()`
   - 排序：`lst.sort()`（原地改）、`sorted(lst)`（返回新列表）
   - 其他：`reverse()`、`copy()`、`sum/max/min/len`
2. **tuple 元组**（有序、**不可变**）
   - 单元素要写 `(1,)`，否则 `(1)` 只是数字
   - 可解包：`a, b = (1, 2)`；函数返回多值其实就是返回元组
   - 用途：不会被改的数据、字典的 key、函数返回多个值
3. **dict 字典**（键值对，键必须可哈希）
   - 增改：`d["k"] = v`；读：`d["k"]`（不存在报 `KeyError`）
   - 安全读：`d.get("k", 默认值)`
   - 遍历：`d.keys()` / `d.values()` / `d.items()`
   - 合并：`d1 | d2`（3.9+）；`update()`
   - 3.7+ 保证**插入顺序**
4. **set 集合**（无序、去重、元素可哈希）
   - 运算：`|`（并）、`&`（交）、`-`（差）、`^`（对称差）
   - 方法：`add`、`discard`、`remove`、`issubset`
   - 最常用：**去重** `set(lst)`、**快速成员判断**（比 list 快）
5. **推导式**（重点）
   - 列表：`[x * 2 for x in range(5)]`
   - 带条件：`[x for x in nums if x > 0]`
   - 字典：`{k: v for k, v in items}`
   - 集合：`{x % 3 for x in nums}`
6. **深浅拷贝**：`b = a` 只是多了个名字；`b = a.copy()` 才是浅拷贝；
   `copy.deepcopy(a)` 用于嵌套结构
7. **判断用什么**：要顺序和重复 → list；不可变/当 key → tuple；
   按键取值 → dict；去重/集合运算 → set

## 示例代码

| 文件 | 演示内容 |
| :--- | :--- |
| `04_collections.py` | list 全套操作、tuple 解包、dict 增删查改与遍历、set 去重与运算、统计词频小例子 |
| `04_comprehensions.py` | 列表 / 字典 / 集合推导式 + 嵌套与条件，和 for 写法对比 |

## 易错点

- `a = [1, 2]` 后 `b = a`，改 `b` 会连带改 `a`（同一个对象）；要独立就 `a.copy()`
- `lst.sort()` 返回 `None`，写 `x = lst.sort()` 会拿到 `None`（要用 `sorted`）
- 遍历字典时改字典大小 → `RuntimeError`；要改就遍历 `list(d.items())`
- `d.get` 和 `d["k"]` 混用导致 `KeyError`：拿不准就用 `get`
- `set()` 空集合不能写 `{}`（那是空字典）
- 推导式写太长会难读，超过一层条件 + 一层嵌套就该换回 for

## 动手练习

1. 列表 `[3, 1, 4, 1, 5, 9, 2, 6]`：去重、排序、求最大值和平均值
2. 用 dict 统计一句话里每个单词出现的次数（词频统计，超经典）
3. 用 set 求两个列表的交集、并集、差集
4. 用推导式生成 1~20 中所有偶数的平方
5. 把 `[("数学", 90), ("英语", 85)]` 转成字典
6. 写一个函数，输入学生成绩字典，返回平均分最高的那个人

## 参考

- 内置容器：https://docs.python.org/zh-cn/3/library/stdtypes.html
- 推导式：https://docs.python.org/zh-cn/3/tutorial/datastructures.html#list-comprehensions
