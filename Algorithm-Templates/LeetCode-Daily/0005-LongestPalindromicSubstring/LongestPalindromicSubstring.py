"""
LeetCode 0005 - 最长回文子串 (Longest Palindromic Substring)
难度: Medium
核心: 中心扩展法 O(n²) O(1)
"""
from typing import List


class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s or len(s) < 2:
            return s

        start = 0
        max_len = 1

        def expand(left: int, right: int) -> int:
            """从 (left, right) 向两边扩展，返回回文子串长度"""
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return right - left - 1

        for i in range(len(s)):
            # 奇数回文（中心在 i）和偶数回文（中心在 i,i+1 之间）
            curr_len = max(expand(i, i), expand(i, i + 1))

            if curr_len > max_len:
                max_len = curr_len
                start = i - (curr_len - 1) // 2

        return s[start:start + max_len]


# ===== 本地测试 =====
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("babad", ["bab", "aba"]),
        ("cbbd", "bb"),
        ("a", "a"),
        ("ac", ["a", "c"]),
        ("", ""),
        ("abb", "bb"),
        ("racecar", "racecar"),
        ("aaaa", "aaaa"),
    ]

    for s, expected in test_cases:
        result = sol.longestPalindrome(s)
        if isinstance(expected, list):
            status = "✅" if result in expected else "❌"
        else:
            status = "✅" if result == expected else "❌"
        print(f"{status} s={s!r:15s} → {result!r:10s}")
