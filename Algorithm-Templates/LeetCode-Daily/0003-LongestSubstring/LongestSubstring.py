class Solution:
    # LeetCode 标准提交模板，所有题统一包在 Solution 类里
    def lengthOfLongestSubstring(self, s: str) -> int:
        # last: 哈希表，记录每个字符最近一次出现时的下标
        last: dict[str, int] = {}
        left = 0  # 滑动窗口的左边界（包含）
        ans = 0   # 记录当前找到的最长无重复子串的长度

        # right 是窗口右边界下标，ch 是 s[right] 位置的字符
        for right, ch in enumerate(s):
            # 如果 ch 出现过，并且上次出现的位置仍在窗口内
            if ch in last and last[ch] >= left:
                # 把左边界跳到上次出现位置的下一个，把重复字符排除
                left = last[ch] + 1

            # 更新 ch 的最新位置为当前 right
            last[ch] = right

            # 计算当前窗口 [left, right] 的长度
            cand = right - left + 1
            # 如果比已知最长还要长，就更新 ans
            if cand > ans:
                ans = cand

        return ans  # 返回最长子串的长度


# 包装一层普通函数，方便本地测试时不用每次都写 Solution()
def length_of_longest_substring(s: str) -> int:
    """与 Solution 相同逻辑，便于本地单测。"""
    return Solution().lengthOfLongestSubstring(s)


# 仅在直接运行此文件时执行测试，被 import 时不运行
if __name__ == "__main__":
    # (输入字符串, 预期输出)  覆盖了各种情况
    samples = [
        ("abcabcbb", 3),  # 常规重复
        ("bbbbb", 1),     # 全相同字符
        ("pwwkew", 3),    # 重复在中间
        ("", 0),          # 空字符串
    ]
    for s, want in samples:
        got = length_of_longest_substring(s)  # 调用函数
        print(f"s={s!r} -> {got} (expect {want})")
