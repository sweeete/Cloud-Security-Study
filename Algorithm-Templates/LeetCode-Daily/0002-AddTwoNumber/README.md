# 0002. 两数相加（Add Two Numbers）

## 题意与「逆序」

- 两条链表表示两个非负整数，**数位逆序存储**：链表头是**个位**，往后是十位、百位……
- 「逆序」指的是**数位在链表里的排列方向**与日常书写习惯相反（书写常是高位在前），**不是**比大小、也不是排序。
- 题目要求「以相同形式返回和的链表」：和的链表也是**低位在头**。算法从 `l1`、`l2` 的头开始按位相加，新结点接在结果尾部，**数位顺序已经符合题意**，一般**不需要**再写反转链表的代码。

## 核心思路（C / Python 一致）

- **哑结点（dummy）**：占位，不表示真实数位，只用来挂结果链；真实结果从 `dummy.next` 开始。
- **`tail` / `curr`**：始终指向**结果链表的最后一个结点**；新结点接在 `tail->next` 或 `curr.next`，再后移指针。
- **进位 `carry`**：每一位 `sum = v1 + v2 + carry`，当前位 `sum % 10`（Python 为 `total % 10`），进位 `sum / 10`（Python 为 `total // 10`）。
- **循环条件**：`l1` 或 `l2` 仍有结点，或 `carry > 0`，以处理长度不同与末尾进位。
- **返回**：`dummy.next`（结果链表头）。

---

## C：`.` 与 `->`

| 写法 | 适用 |
|------|------|
| **`dummy.next`** | 左边是**结构体变量**（如栈上的 `struct ListNode dummy`）。 |
| **`p->next`** | 左边是**指向结构体的指针**（如 `struct ListNode *p`）。 |

- `p->next` 等价于 `(*p).next`。
- **`next` 成员的类型**在定义里是指针（`struct ListNode *`），**与用 `.` 还是 `->` 无关**；区别只在于**左边是对象还是指针**。
- 本题的 `dummy` 若为栈上变量，应写 **`dummy.next`**；写 **`dummy->next`** 会类型不匹配、无法通过编译。
- **`return dummy.next`** 返回的是**指针**（第一个真实结点或 `NULL`），不是「`.` 返回结构体」之类。

---

## Python 备忘

### `ListNode(total % 10)`

- 这是**类的构造函数调用**，不是 C 的 `struct` 语法。
- 参数按 **`__init__(self, val=0, next=None)`** 的**位置顺序**绑定；**不是**按类型自动匹配。只传一个数时赋给 `val`，`next` 默认为 `None`。
- 定义 `ListNode` 类：把 **`val` 与 `next`** 绑在一起，表示链表结点；也可用别的方式模拟，类写法最常见且与 LeetCode 一致。

### `class Solution` 与类型注解

- **`class Solution`**：主要是 **LeetCode 提交模板**（与其它语言「类 + 方法名」统一）；本地练习也可写成普通函数，算法相同。
- **`from typing import Optional`**：`Optional[X]` 表示 **`X` 或 `None`**，用于类型提示；不写注解程序也能跑，**题目与评测**仍会规定应返回的链表形态。
- **`self`**：实例方法第一个参数；本题里往往用不到实例状态，仅为符合方法形式。

### `build_list(nodes)` 里的 `nodes`

- **`nodes`**：函数参数名，表示传入的一串**待写入链表的数字**（如列表 `[2, 4, 3]`），**不是**已经建好的 `ListNode` 对象序列。
- 函数内部用 `ListNode(val)` 逐个建成链表结点并串联。

### `print_list`：`append` 与 `join`

- **`list.append(x)`**：在列表**末尾就地**加入一个元素；返回 `None`。
- **`"->".join(res)`**：`join` 要求 **`res` 中每一项都是字符串**，因此需 `str(node.val)`，否则会 `TypeError: expected str instance, int found`。
- 作用：把链表各结点的值拼成一行，如 `2->4->3` 并打印。

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `AddTwoNumber.c` | C 实现与本地 `main` 示例。 |
| `AddTwoNumber.py` | Python 实现（`Solution` + 本地 `build_list` / `print_list`）。 |
