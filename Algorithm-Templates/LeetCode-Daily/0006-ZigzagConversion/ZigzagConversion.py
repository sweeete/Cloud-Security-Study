"""
LeetCode 0006 - Z 字形变换 (Zigzag Conversion)
难度: Medium
核心: 模拟 Z 字形遍历，逐行收集字符
"""
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        rows = [''] * numRows
        row = 0
        step = 1  # 1 向下, -1 向上

        for c in s:
            rows[row] += c
            if row == 0:
                step = 1       # 碰到顶部，转向下
            elif row == numRows - 1:
                step = -1      # 碰到底部，转向上
            row += step

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
