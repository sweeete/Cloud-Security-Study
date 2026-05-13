# 0003. 无重复字符的最长子串 — 学习笔记

> 本文档记录了一次完整的算法学习过程，从读题、看代码、逐行理解到深入底层原理。

---

## 一、题目理解

### 原题（英文）

> Given a string `s`, find the length of the **longest substring** without repeating characters.

### 原题（中文）

> 给定一个字符串 `s`，请你找出其中不含有重复字符的 **最长子串** 的长度。

**关键坑**：子串 ≠ 子序列
- **子串 (Substring)**：在原串中**连续**的一段
  - 例：`"abcabcbb"` 的子串有 `"abc"`、`"bca"`、`"cab"` 等
  - `"pwke"` **不是** `"pwwkew"` 的子串（因为跳过了中间的 `w`）
- **子序列 (Subsequence)**：可以跳字符，不要求连续
  - `"pwke"` **是** `"pwwkew"` 的子序列

### 官方示例

| 输入 | 输出 | 解释 |
|------|------|------|
| `s = "abcabcbb"` | `3` | 最长无重复子串是 `"abc"`，长度为 3 |
| `s = "bbbbb"` | `1` | 最长无重复子串是 `"b"`，长度为 1 |
| `s = "pwwkew"` | `3` | 最长无重复子串是 `"wke"` 或 `"kew"`，长度为 3 |
| `s = ""` | `0` | 空字符串 |

### 进阶挑战

> 你能用 O(n) 的时间复杂度解决这个问题吗？

---

## 二、算法思路：滑动窗口

### 2.1 直观理解

想象一个可以伸缩的窗口在字符串上滑动：

```
Initial: [a] b  c  a  b  c  b  b   窗口: "a"
          L
          R

Step:    a [b  c  a] b  c  b  b   遇到重复 a，左边跳到 a+1
             L     R
```

窗口始终保持内部无重复字符，`right` 每次右移一格，`left` 遇到重复就跳到重复字符的**下一位**。

### 2.2 复杂度

- **时间 O(n)**：每个字符最多被 left/right 各扫一遍
- **空间 O(字符集大小)**：Python 用 `dict` (动态)，C 用 `int last[256]` (固定)

---

## 三、Python 代码逐行学习

这是学习时先读到的文件，每一行都问清楚了再往下走。

### 3.1 `class Solution` — 为什么要有这个类？

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
```

LeetCode 的提交模板规定必须用 `class Solution` + 固定方法名，这样评测系统才能统一调用。本地练习也可以写成普通函数，逻辑一样。

### 3.2 `last: dict[str, int] = {}` — 哈希表存什么？

键 = 字符，值 = 该字符**最近一次出现的位置**（下标）。

比如 `s = "abcab"`，处理到第二个 `'a'` 时：
```python
last = {'a': 0, 'b': 1, 'c': 2}    # 每个字符最后出现的位置
```

看到新的 `'a'`，查表发现上次在 `0` 出现过 → 说明重复了。

### 3.3 `enumerate(s)` — 下标和字符一起拿

学习时重点问过的函数。对比三种写法：

```python
# 写法一：只有字符，没有下标
for ch in s:
    print(ch)

# 写法二：有下标，但要多写一行取字符
for i in range(len(s)):
    print(i, s[i])

# 写法三（enumerate）：下标和字符同时拿到
for right, ch in enumerate(s):
    print(right, ch)
```

**`enumerate(s)`** 是 Python 内置函数，每次循环返回一个元组 `(下标, 元素)`，配合**元组解包**直接赋值给 `right` 和 `ch`。

### 3.4 核心逻辑 — 三步走

```python
for right, ch in enumerate(s):
    # 第一步：遇到重复 → 收缩左边界
    if ch in last and last[ch] >= left:
        left = last[ch] + 1

    # 第二步：更新该字符的最新位置
    last[ch] = right

    # 第三步：算长度，更新答案
    cand = right - left + 1
    if cand > ans:
        ans = cand
```

**为什么 `left = last[ch] + 1`？**
- `last[ch]` 是重复字符的位置，这个位置本身是重复的，必须排除
- 所以跳到它**后一格**，窗口里就没有重复字符了

**为什么检查 `last[ch] >= left`？**
- 如果旧位置已经在窗口左边之外（`< left`），说明那个重复已经不在窗口里了，不需要动
- 只在旧位置**在窗口内**时才需要收缩

### 3.5 `if __name__ == "__main__"` — 什么时候执行？

```python
if __name__ == "__main__":
    # 直接运行此文件时执行 → python3 LongestSubstring.py 会跑这些测试
    # 被 import 时跳过 ← 别人 from ... import 时不会执行测试代码
```

这是 Python 的一个常用模式，让文件既是可执行脚本，也是可导入模块。

---

## 四、C 语言实现 — 指针是核心

> C 版和 Python 版算法完全一样，但**底层原理完全不同**。Python 帮你隐藏了所有指针细节，C 全暴露给你了。

### 4.1 `char* s` — 参数本身就是指针

```c
int lengthOfLongestSubstring(char* s)
```

`char* s` 是一个指向字符串首字符的指针，不是数组。它指向一块以 `\0` 结尾的连续内存。

**内存布局**：
```
   s
   ↓
 ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
 │ a │ b │ c │ a │ b │ c │ b │ b │\0 │
 └───┴───┴───┴───┴───┴───┴───┴───┴───┘
   s+0  s+1  s+2  ...                  s+8
```

### 4.2 `s[right]` 的本质是 `*(s + right)`

```c
for (int right = 0; s[right] != '\0'; right++) {
```

C 语言中，`arr[i]` 是语法糖，编译器翻译成指针算术：

| 你写的 | 实际发生的 |
|--------|-----------|
| `s[right]` | `*(s + right)` |
| 含义 | 从地址 `s` 偏移 `right` 个元素，然后解引用取值 |

`s + right` 的偏移量由指针类型决定：
- `char*` → 每次 +1 移动 **1 字节**
- `int*` → 每次 +1 移动 **4 字节**

所以 `s + 3` 在 `char*` 下就是跳过 3 个字节，正好指向第 4 个字符。

### 4.3 为什么要用 `unsigned char`？— 防止数组越界

```c
unsigned char c = (unsigned char)s[right];
```

如果不强转，直接用 `char`：

| 字符 ASCII | `char` (默认有符号) | 结果 |
|-----------|-------------------|------|
| 0x00 ~ 0x7F (0~127) | 正常正数 | ✅ |
| **0x80 ~ 0xFF (128~255)** | **变成负数**（如 0x80 → -128） | ❌ |

然后拿负数去访问数组：
```c
int last[256];
last[-128] = xxx;  // 数组下标不能为负！越界 → 段错误 (Segmentation Fault)
```

**解决方案**：转成 `unsigned char`，范围 0~255，安全访问 `last` 数组。

**这是信息安全专业的典型考点**：不注意类型转换会导致**缓冲区下标越界**，轻则段错误，重则成为漏洞利用点。

### 4.4 `last[256]` — 用数组代替哈希表

```c
int last[256];
for (int i = 0; i < 256; i++) {
    last[i] = -1;   // -1 表示"从未出现过"
}
```

为什么是 256？`unsigned char` 的取值范围是 0~255，共 256 种可能。

访问时：
```c
int prev = last[c];         // c 是 unsigned char，范围 0~255
if (prev >= left) {         // 上次出现在窗口内？
    left = prev + 1;        // 收缩
}
last[c] = right;            // 更新最新位置
```

**对比 Python**：

| 特性 | Python `dict` | C `last[256]` |
|------|-------------|---------------|
| 空间 | 只存出现过的字符，动态增长 | 固定 1024 字节（256×4） |
| 速度 | 哈希函数 + 可能的冲突 | 数组下标，绝对 O(1) |
| 适用范围 | 任意 Unicode 字符 | 仅 ASCII / Latin-1 |
| 安全风险 | 无（自动管理） | 下标越界需要手动防范 |

### 4.5 `main` 中的指针细节

```c
const char* cases[] = {
    "abcabcbb",
    "bbbbb",
    "pwwkew",
    "",
};
```

`cases` 是一个**指针数组**：
- 数组的每个元素是一个 `const char*` 指针
- 这些指针指向**只读数据段（.rodata）**中的字符串常量
- 字符串常量不可修改，所以用 `const` 修饰

函数调用时传参：
```c
int out = lengthOfLongestSubstring((char*)cases[i]);
```

这里做了**强制类型转换** `(char*)`：
- `cases[i]` 类型是 `const char*`（只读）
- 函数参数类型是 `char*`（可读写）
- 虽然本函数只读不写不会出问题，但严格来说应统一为 `const char*`

> **最佳实践**：如果函数不修改字符串，参数类型应声明为 `const char*`，让编译器帮你检查。

---

## 五、手动推演：看代码怎么跑

以 `"abcabcbb"` 为例，逐步骤跟踪：

| right | ch | `last` 状态 | 条件 | left 新值 | 窗口 | 长度 | ans |
|-------|----|-------------|------|---------|------|------|-----|
| 0 | a | `{a:0}` | 首次出现 | 0 | a | 1 | 1 |
| 1 | b | `{a:0, b:1}` | 首次出现 | 0 | ab | 2 | 2 |
| 2 | c | `{a:0, b:1, c:2}` | 首次出现 | 0 | abc | **3** | **3** |
| 3 | a | `a` 的 last=0 ≥ left=0 ✅ | **重复！** left=0+1=**1** | **1** | bca | 3 | 3 |
| 4 | b | `b` 的 last=1 ≥ left=1 ✅ | **重复！** left=1+1=**2** | **2** | cab | 3 | 3 |
| 5 | c | `c` 的 last=2 ≥ left=2 ✅ | **重复！** left=2+1=**3** | **3** | abc | 3 | 3 |
| 6 | b | `b` 的 last=4 ≥ left=3 ✅ | **重复！** left=4+1=**5** | **5** | b | 1 | 3 |
| 7 | b | `b` 的 last=6 ≥ left=5 ✅ | **重复！** left=6+1=**7** | **7** | b | 1 | 3 |

最终 ans = **3** ✅

---

## 六、Python vs C 核心差异速查

| 概念 | Python | C |
|------|--------|----|
| 字符串遍历 | `for right, ch in enumerate(s):` | `for(int i=0; s[i]!='\0'; i++)` |
| `s[i]` 的本质 | 解释器内部处理 | **`*(s + i)`** — 指针算术语法糖 |
| 字符映射表 | `dict`（哈希表，任意 Unicode） | `int last[256]`（定长数组，仅 ASCII） |
| 字符类型安全 | 自动处理 | 需 `unsigned char` 强转防越界 |
| 测试入口 | `if __name__ == "__main__":` | `int main(void)` |
| 内存管理 | 自动垃圾回收 | 本程序无动态分配，天然安全 |
| 可读性 | 高，隐藏底层细节 | 低，暴露指针和内存操作 |

---

## 七、文件说明

| 文件 | 内容 |
|------|------|
| `LongestSubstring.py` | Python 实现，每行已加详细中文注释 |
| `LongestSubstring.c` | C 实现，侧重指针操作 |
| `README.md` | **本文**，学习过程记录与知识总结 |
