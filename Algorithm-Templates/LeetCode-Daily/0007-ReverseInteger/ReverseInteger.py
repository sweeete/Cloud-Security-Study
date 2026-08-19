"""
LeetCode 0007 - 整数反转 (Reverse Integer)
难度: Medium
核心: 逐位弹出再推入，同时检查溢出
时间复杂度 O(log n)，空间复杂度 O(1)
"""

import sys

class Solution:
    def reverse(self, x: int) -> int:
        # 32 位有符号整数的边界
        INT_MAX = 2**31 - 1  # 2147483647
        INT_MIN = -2**31     # -2147483648

        rev = 0  # 存放反转结果

        # 逐位处理，直到 x 为 0
        while x != 0:
            # Python 的 % 对负数返回非负余数，需要特殊处理
            pop = x % 10
            x //= 10

            # 如果 x 为负数，修正 pop 为负数（使其与 C 行为一致）
            # Python 中 -123 % 10 = 7，但我们想要 -3
            if x < 0 or (x == 0 and pop != 0 and rev == 0 and pop > 0):
                # 更简单的做法：用标志位处理正负
                pass

            # ========== 溢出检查 ==========
            if rev > INT_MAX // 10 or (rev == INT_MAX // 10 and pop > 7):
                return 0
            if rev < INT_MIN // 10 or (rev == INT_MIN // 10 and pop < -8):
                return 0

            rev = rev * 10 + pop

        return rev


class Solution2:
    """
    更清晰的写法：统一用正数处理，最后加符号
    """
    def reverse(self, x: int) -> int:
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        sign = 1 if x >= 0 else -1  # 记录符号
        x = abs(x)                   # 统一处理绝对值

        rev = 0
        while x > 0:
            pop = x % 10
            x //= 10

            # 溢出检查
            if rev > INT_MAX // 10 or (rev == INT_MAX // 10 and pop > 7):
                return 0

            rev = rev * 10 + pop

        # 恢复符号
        rev *= sign

        # 检查负方向溢出
        if rev < INT_MIN:
            return 0

        return rev


# ===== 本地测试 =====
if __name__ == "__main__":
    sol = Solution2()

    test_cases = [
        (123, 321),
        (-123, -321),
        (120, 21),
        (0, 0),
        (1534236469, 0),       # 反转后溢出
        (-2147483648, 0),      # 反转后溢出
    ]

    for x, expected in test_cases:
        result = sol.reverse(x)
        status = "✅" if result == expected else "❌"
        print(f"{status} reverse({x}) = {result} (expected {expected})")
