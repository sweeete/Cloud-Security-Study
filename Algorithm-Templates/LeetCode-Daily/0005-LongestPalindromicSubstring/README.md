# 0005. 最长回文子串（Longest Palindromic Substring）

## 一、题目理解

给定字符串 `s`，找出最长的**回文子串**。

**回文**：正着读反着读都一样，如 `"aba"`、`"abba"`、`"racecar"`

**示例**：
```
s = "babad" → "bab" 或 "aba"
s = "cbbd"  → "bb"
s = "a"     → "a"
```

## 二、算法思路

### 2.1 中心扩展法（总结）

两个函数搞定：

**① 扩展函数**：给定字符串和左右端下标，不断向两边扩展，同时判断字符是否相等，最后返回回文子串的长度。

**② 遍历函数**：遍历每个位置，分别从**奇数**（`expand(i,i)`）和**偶数**（`expand(i,i+1)`）角度调用扩展函数，记录最大值，同时计算起始位置，最后截取子串返回。

### 2.2 手动推演

`s = "babad"`：
```
i=1 'a': 奇数 expand(1,1) → "bab" (len=3) ✅
i=2 'b': 奇数 expand(2,2) → "aba" (len=3)
其余位置长度都小于3
最长: "bab" 或 "aba"
```

`s = "cbbd"`：
```
i=1 'b': 偶数 expand(1,2) → "bb" (len=2) ✅
最长: "bb"
```

### 2.3 复杂度

| 维度 | 值 |
|:----|:----|
| 时间 | O(n²) |
| 空间 | O(1) |

## 三、代码精读

### 3.1 扩展函数

```python
def expand(left: int, right: int) -> int:
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return right - left - 1
```

退出循环时 left 和 right 多走了一步，实际回文范围是 `(left+1, right-1)`，所以长度减 1。

### 3.2 遍历函数

```python
for i in range(len(s)):
    curr_len = max(expand(i, i), expand(i, i + 1))
    if curr_len > max_len:
        max_len = curr_len
        start = i - (curr_len - 1) // 2

return s[start:start + max_len]
```

**起始位置 `start` 的计算**：回文中心在 `i`，长度为 `curr_len`，左边有 `(curr_len-1)/2` 个字符，所以 `start = i - (curr_len-1)//2`。

### 3.3 C 注意点

```c
// 返回堆上分配的字符串（局部数组不能返回）
char* result = (char*)malloc(maxLen + 1);
strncpy(result, s + start, maxLen);
result[maxLen] = '\0';     // strncpy 不自动加结束符！
```

`s + start` 是指针算术，指向子串起始位置。

## 四、文件说明

| 文件 | 说明 |
|:-----|:-----|
| `LongestPalindromicSubstring.py` | Python 实现 |
| `LongestPalindromicSubstring.c` | C 实现 |
| `README.md` | 学习笔记 |
