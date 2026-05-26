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

**模拟法**：用一个数组记录每一行的字符，遍历原字符串，从上往下再向上，碰到边界就掉头。

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
