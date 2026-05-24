# 0005. 最长回文子串（Longest Palindromic Substring）

## 一、题目理解

**问题**：给定字符串 `s`，找出其中最长的**回文子串**。

**回文**：正着读和反着读都一样，如 `"aba"`、`"abba"`、`"racecar"`

**示例**：
```
s = "babad"  →  "bab" 或 "aba"  （两个都是答案）
s = "cbbd"   →  "bb"
s = "a"      →  "a"
s = "ac"     →  "a" 或 "c"      （单个字符）
```

## 二、算法思路：中心扩展法

### 2.1 暴力法（不推荐）

```python
# 枚举所有子串，判断是否是回文 O(n³)
for i in range(n):
    for j in range(i, n):
        if is_palindrome(s[i:j+1]): ...
```

### 2.2 中心扩展法（最优解）

**核心思想**：每个回文都有一个"中心"，从中心向两边扩展可以找到完整的回文。

**两种中心**：
- **奇数回文**：中心是**一个字符**，如 `"aba"` → 中心 `'b'`
- **偶数回文**：中心是**两个字符之间**，如 `"abba"` → 中心在 `"bb"` 中间

```
奇数回文:  a  b  a         ← 'b' 是中心
            ↑  ↑  ↑
           ← 扩展方向

偶数回文:  a  b  b  a      ← "bb" 中间是中心
               ↑↑
           ←  扩展方向
```

**步骤**：
1. 遍历每个字符 `i`
2. 以 `i` 为中心找奇数回文（`expand(i, i)`）
3. 以 `i, i+1` 为中心找偶数回文（`expand(i, i+1)`）
4. 更新全局最长

### 2.3 复杂度

| 维度 | 值 | 说明 |
|:----|:---|:-----|
| 时间 | **O(n²)** | 每个中心扩展最多 n 步 |
| 空间 | **O(1)** | 只用了几个变量 |

**Manacher 算法可以做到 O(n)**，但实现复杂，面试中中心扩展法足够。

## 三、Python 代码逐行学习

### 3.1 核心函数 `expand_around_center`

```python
def expand_around_center(left: int, right: int) -> int:
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return right - left - 1  # 注意这里减了1
```

**扩展过程**（以 `"babad"` 为例，中心在 `i=1` 即 `'a'`）：

```
初始: left=1, right=1 → s[1]='a' 自相等 ✅
  → left=0, right=2  → s[0]='b' == s[2]='b' ✅
  → left=-1, right=3 → left<0 ❌ 退出
  回文长度 = 3 - (-1) - 1 = 3 ✓  ("bab")
```

**为什么减 1**：退出循环时 left 和 right 都多走了一步，真实边界是 `(left+1, right-1)`。

### 3.2 主循环

```python
for i in range(len(s)):
    len1 = expand_around_center(i, i)       # 奇数
    len2 = expand_around_center(i, i + 1)   # 偶数
    curr_len = max(len1, len2)

    if curr_len > max_len:
        max_len = curr_len
        start = i - (curr_len - 1) // 2     # 计算起始位置
```

**起始位置怎么算？** 回文中心在 `i`，长度为 `curr_len`：
- 奇数时：中心就是中间，左边有 `(curr_len-1)/2` 个字符
- 偶数时：中心偏左，左边也有 `(curr_len-1)/2` 个字符（整数除法）

```
奇数 "bab":  i=1, curr_len=3, start=1-(3-1)//2=0  ✅
偶数 "abba": 当中心在 i=1时找到
  expand(1,2) → left=0,right=3 → curr_len=4
  start = 1 - (4-1)//2 = 1-1 = 0  ✅
```

## 四、C 语言底层 — 指针与内存

### 4.1 字符串作为指针

```c
char* longestPalindrome(const char* s, int* returnSize)
```

`const char* s` — 指向只读字符串的指针，函数不修改输入。

### 4.2 指针访问 vs 下标

```c
// 等价写法
*(s + left) == s[left]    // 指针算术
*(s + right) == s[right]
```

### 4.3 堆内存分配

```c
char* result = (char*)malloc(maxLen + 1);
strncpy(result, s + start, maxLen);  // 复制子串
result[maxLen] = '\0';               // 手动加结束符
```

因为要返回函数内部的字符串，**局部数组在函数退出后失效**，必须用 `malloc` 在堆上分配。

### 4.4 `strncpy` 不自动加 `\0`

```c
strncpy(result, s + start, maxLen);  // 复制 maxLen 个字符
result[maxLen] = '\0';               // ⚠️ 必须手动加！
```

这是 C 新手常犯的错误 —— `strncpy` 在达到长度限制时**不会**追加 `\0`。

## 五、手动推演

### `s = "babad"`

```
i=0 'b': 奇数: "b" (len=1)      偶数: 无 (len=0)
i=1 'a': 奇数: "bab" (len=3) ✅  偶数: 无 (len=0)
i=2 'b': 奇数: "aba" (len=3)    偶数: 无 (len=0)
i=3 'a': 奇数: "a" (len=1)      偶数: "bad"? → 不相等 (len=0)
i=4 'd': 奇数: "d" (len=1)      偶数: 无 (len=0)

最长: "bab" (或 "aba") ✅
```

### `s = "cbbd"`

```
i=0 'c': 奇数: "c" (len=1)              偶数: 无
i=1 'b': 奇数: "b" (len=1)              偶数: "bb" (len=2) ✅
i=2 'b': 奇数: "b" (len=1)              偶数: "bd"? → 不相等
i=3 'd': 奇数: "d" (len=1)              偶数: 无

最长: "bb" ✅
```

## 六、复杂度对比

| 方法 | 时间 | 空间 | 说明 |
|:----|:----|:-----|:-----|
| 暴力法 | O(n³) | O(1) | 枚举所有子串，逐个判断 |
| 中心扩展 | **O(n²)** | **O(1)** | 每个中心 O(n)，共 2n 个中心 |
| 动态规划 | O(n²) | O(n²) | dp[i][j] 记录 s[i..j] 是否回文 |
| Manacher | O(n) | O(n) | 利用对称性优化，实现复杂 |

## 七、文件说明

| 文件 | 说明 |
|:-----|:-----|
| `LongestPalindromicSubstring.py` | Python 实现，中心扩展法 |
| `LongestPalindromicSubstring.c` | C 实现，指针 + malloc 堆内存 |
| `README.md` | 学习笔记 |
