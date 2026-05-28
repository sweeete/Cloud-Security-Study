"""
LeetCode 0006 - Z 字形变换 (Zigzag Conversion)
难度: Medium
核心: 模拟 Z 字形遍历，用 numRows 个"桶"逐行收集字符
时间复杂度 O(n)，空间复杂度 O(n)
"""
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        # ========== 1. 边界情况处理 ==========
        # 只有 1 行 → Z 字形就是一条直线，直接返回原串
        # 行数 >= 字符数 → 每个字符独占一行，顺序不变，直接返回
        if numRows == 1 or numRows >= len(s):
            return s

        # ========== 2. 创建"桶"（每一行一个字符串）==========
        # Python 里直接用字符串列表，不用手动管理内存
        # 每个空字符串 '' 就是一个桶
        rows = [''] * numRows

        # ========== 3. 模拟 Z 字形遍历 ==========
        row = 0    # 当前行索引（从 0 开始）
        step = 1   # 方向：1 向下, -1 向上

        # 遍历字符串的每一个字符（直接遍历字符，不需要下标）
        for c in s:
            # ----- 3a. 将当前字符追加到当前行的桶 -----
            # Python 里直接用 += 拼接字符串，简洁方便
            # （注意：Python 字符串不可变，+= 会创建新对象，但 LeetCode 上够用）
            rows[row] += c

            # ----- 3b. 方向控制 -----
            # 逻辑和 C 完全一样
            if row == 0:
                step = 1           # 到达顶部 → 改为向下走
            elif row == numRows - 1:
                step = -1          # 到达底部 → 改为向上走
            row += step

        # ========== 4. 合并所有行 ==========
        # ''.join(rows) 比 += 循环拼接更高效（减少字符串拷贝）
        # 相当于 rows[0] + rows[1] + ... + rows[numRows-1]
        return ''.join(rows)


# ===== 本地测试 =====
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("PAYPALISHIRING", 3, "PAHNAPLSIIGYIR"),
        ("PAYPALISHIRING", 4, "PINALSIGYAHRPI"),
        ("A", 1, "A"),
        ("AB", 1, "AB"),
        ("ABC", 2, "ACB"),
    ]

    for s, numRows, expected in test_cases:
        result = sol.convert(s, numRows)
        status = "✅" if result == expected else "❌"
        print(f"{status} s={s!r}, numRows={numRows} → {result!r}")
