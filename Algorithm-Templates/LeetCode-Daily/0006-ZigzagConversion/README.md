# 0006. Z 字形变换（Zigzag Conversion）

## 一、题目理解

给定字符串 `s` 和行数 `numRows`，按 Z 字形排列后，逐行读取输出。

```
numRows=3 时:
P   A   H   N
A P L S I I G
Y   I   R

逐行读取: "PAHNAPLSIIGYIR"
```

## 二、算法思路

**模拟法**：用 numRows 个"桶"（每行一个字符串）收集字符，遍历原字符串，从上往下再向上，碰到边界就掉头。

```
s = "PAYPALISHIRING", numRows = 3

过程:
P     → row 0
A  Y  → row 1, row 1
P     → row 2
...

rows[0]: P   A   H   N
rows[1]: A P L S I I G
rows[2]: Y   I   R

合并: "PAHNAPLSIIGYIR" ✅
```

**遍历方向控制**：用 `step` 变量，1 表示向下，-1 表示向上，碰到顶部或底部时反转。

```
if row == 0:
    step = 1          # 触顶 → 向下
elif row == numRows - 1:
    step = -1         # 触底 → 向上
row += step
```

## 三、复杂度

| 维度 | 值 |
|:----|:----|
| 时间 | O(n) |
| 空间 | O(n) |

## 四、文件说明

| 文件 | 说明 |
|:-----|:-----|
| `ZigzagConversion.py` | Python 实现 |
| `ZigzagConversion.c` | C 实现 |
| `README.md` | 学习笔记 |

## 五、学习 Q&A

### Q1：代码是先创建一个二维数组按 Z 字形填充，最后横向遍历吗？

❌ **不是。** 创建完整二维矩阵需要先计算列数，且矩阵中有大量空位，浪费空间。

✅ **实际做法是用 numRows 个"桶"（字符串），遍历过程只存字符不存空位：**

| | 完整二维数组 | 桶做法 |
|:----|:----|:----|
| 存储什么 | 所有位置（含空位） | **只存字符，不存空位** |
| 空间 | O(n × 列数) | **O(n)** |
| 需要知道列数？ | 需要先计算 | **不需要** |
| 最终输出 | 逐行遍历，跳过空位 | **直接拼接桶** |

**模拟过程：**
```
桶 0: P → A → H → N    → 直接就是 "PAHN"
桶 1: A → P → L → S → I → I → G  → 直接就是 "APLSIIG"
桶 2: Y → I → R          → 直接就是 "YIR"
```
→ 三行拼接 = `"PAHN" + "APLSIIG" + "YIR"` = `"PAHNAPLSIIGYIR"` ✅

---

### Q2：`rows = [''] * numRows` 是定义一个二维数组吗？

❌ **不是真正的二维数组。** 这是一维列表，每个元素是一个不可变字符串。

```
numRows = 3

rows = ['', '', '']
#        ↑    ↑    ↑
#     rows[0] rows[1] rows[2]
```

**结构上**可以理解为"多个字符序列的集合"，和 C 的 `char**` 类似：
- 取第 row 行的字符串：`rows[row]` ✅
- 取第 row 行第 index 个字符：`rows[row][index]` ✅

**但 Python 字符串不可变（immutable），不能像 C 那样直接修改：**
```python
rows[0][0] = 'X'    # ❌ 报错！字符串不可变
rows[0] += 'X'      # ✅ 创建新字符串后重新赋值
```

**安全原因：** 因为字符串不可变，`[''] * n` 不会像可变对象（如列表）那样出现共享引用的问题。
```python
rows = [[]] * 3     # ❌ 三个元素指向同一个列表！
rows[0].append(1)   # rows → [[1], [1], [1]] 全改了！
```

---

### Q3：`''.join(rows)` 返回的是什么？

返回 **拼接后的一整个字符串**。

```python
rows = ['PAHN', 'APLSIIG', 'YIR']
result = ''.join(rows)
# 等价于 'PAHN' + 'APLSIIG' + 'YIR'
# 结果: 'PAHNAPLSIIGYIR'
```

`''` 是分隔符（空字符串），`.join()` 把列表元素用分隔符拼起来：
```python
', '.join(['PAHN', 'APLSIIG', 'YIR'])  # → "PAHN, APLSIIG, YIR"
```

**为什么用 join 而不用 + 循环？** 效率更高！`join` 一次性分配好空间（O(n)），而 `+=` 循环每次创建新对象（O(n²)）。

---

### Q4：`if __name__ == "__main__"` 的作用是什么？

**守护语句**：只有直接运行该文件时，才执行下面的测试代码。

```python
python3 ZigzagConversion.py   → 执行 ✅
import ZigzagConversion       → 不执行 ❌（只导入类，不跑测试）
```

**为什么需要它？** 其他人可以 `from ZigzagConversion import Solution` 拿到类，而不会连带跑测试代码。

**测试代码拆解：**

```python
sol = Solution()                         # 实例化 Solution 类

test_cases = [
    ("PAYPALISHIRING", 3, "PAHNAPLSIIGYIR"),   # (输入, 行数, 期望输出)
    ("PAYPALISHIRING", 4, "PINALSIGYAHRPI"),
    ...
]

for s, numRows, expected in test_cases:  # 元组解包，遍历测试用例
    result = sol.convert(s, numRows)     # 调用算法
    status = "✅" if result == expected else "❌"  # 三目运算符判对错
    print(f"{status} s={s!r}, numRows={numRows} → {result!r}")
```

---

### Q5：这道题的核心收获

1. **桶思想**：不需要完整的二维矩阵，用 `numRows` 个桶即可，空间从 O(n×k) 降到 O(n)
2. **方向控制**：`step` 变量在边界处反转，模拟 Z 字形路径
3. **C vs Python**：算法逻辑完全一致，但 C 需要手动内存管理（`malloc`/`free`），Python 更简洁
