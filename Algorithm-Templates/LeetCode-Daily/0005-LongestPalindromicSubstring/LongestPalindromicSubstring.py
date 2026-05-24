"""
LeetCode 0005 - 最长回文子串 (Longest Palindromic Substring)
难度: Medium
核心思想: 中心扩展法 O(n²) / 动态规划 O(n²) / Manacher O(n)

这里采用「中心扩展法」—— 思路最简单，空间 O(1)
"""

from typing import List


class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        中心扩展法：
        每个字符（以及每两个相邻字符中间）都可以作为回文中心，
        从中心向两边扩展，找到最长的回文子串。
        
        奇数回文：中心是单个字符，如 "aba" 的中心是 'b'
        偶数回文：中心是两个字符之间，如 "abba" 的中心在 "bb" 中间
        """
        if not s or len(s) < 2:
            return s

        start = 0  # 最长回文子串的起始位置
        max_len = 1  # 最长回文子串的长度

        def expand_around_center(left: int, right: int) -> int:
            """
            从 (left, right) 开始向两边扩展，返回找到的回文子串长度。
            
            对于奇数回文：left = right（中心是一个字符）
            对于偶数回文：right = left + 1（中心是两个字符之间）
            """
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # 退出循环时，left 和 right 多走了一步
            # 回文长度 = (right - 1) - (left + 1) + 1 = right - left - 1
            return right - left - 1

        for i in range(len(s)):
            # 奇数长度回文（中心在 i）
            len1 = expand_around_center(i, i)
            # 偶数长度回文（中心在 i 和 i+1 之间）
            len2 = expand_around_center(i, i + 1)

            # 取两种情况中更长的
            curr_len = max(len1, len2)

            if curr_len > max_len:
                max_len = curr_len
                # 计算回文子串的起始位置
                # 回文中心在 i，长度为 curr_len
                # 起始位置 = i - (curr_len - 1) // 2
                start = i - (curr_len - 1) // 2

        return s[start:start + max_len]


# ===== 本地测试 =====
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("babad", ["bab", "aba"]),   # 两个答案都可以
        ("cbbd", "bb"),
        ("a", "a"),
        ("ac", ["a", "c"]),           # 单个字符
        ("", ""),
        ("abb", "bb"),
        ("abacdfgdcaba", "aba"),      # "aba" 而不是更长的
        ("racecar", "racecar"),       # 本身就是回文
        ("aaaa", "aaaa"),             # 全部相同
    ]

    for s, expected in test_cases:
        result = sol.longestPalindrome(s)
        if isinstance(expected, list):
            status = "✅" if result in expected else "❌"
        else:
            status = "✅" if result == expected else "❌"
        print(f"{status} s={s!r:15s} → {result!r:10s} (期望 {expected})")
