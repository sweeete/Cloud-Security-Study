"""
LeetCode 0004 - 寻找两个正序数组的中位数
难度: Hard
核心思想: 二分查找 + 分割法 O(log(min(m,n)))
"""

from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # 第一步：确保 nums1 是较短的数组（减少二分次数）
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        total_left = (m + n + 1) // 2  # 左半部分需要的元素个数

        # 第二步：在较短的数组 nums1 上二分查找分割点
        left, right = 0, m

        while left <= right:
            # i: nums1 的分割位置（左边有 i 个元素）
            i = (left + right) // 2
            # j: nums2 的分割位置（左边有 j 个元素）
            # 保证左半部分总共有 total_left 个元素
            j = total_left - i

            # 边界处理（用无穷大/小来处理分割在边界的情况）
            nums1_left  = nums1[i - 1] if i > 0 else float('-inf')
            nums1_right = nums1[i]     if i < m else float('inf')
            nums2_left  = nums2[j - 1] if j > 0 else float('-inf')
            nums2_right = nums2[j]     if j < n else float('inf')

            # 第三步：判断分割是否合法
            if nums1_left <= nums2_right and nums2_left <= nums1_right:
                # ✅ 找到正确分割
                if (m + n) % 2 == 1:
                    # 奇数个 → 中位数 = 左半部分的最大值
                    return max(nums1_left, nums2_left)
                else:
                    # 偶数个 → 中位数 = (左最大 + 右最小) / 2
                    return (max(nums1_left, nums2_left) +
                            min(nums1_right, nums2_right)) / 2.0

            elif nums1_left > nums2_right:
                # nums1 左边太大了 → i 往左移
                right = i - 1
            else:
                # nums1 右边太小了 → i 往右移
                left = i + 1

        # 正常情况下不会到这里
        return 0.0


# ===== 本地测试 =====
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 3], [2], 2.0),
        ([1, 2], [3, 4], 2.5),
        ([0, 0], [0, 0], 0.0),
        ([], [1], 1.0),
        ([2], [], 2.0),
        ([1, 2, 3], [4, 5, 6], 3.5),
        ([1, 3, 5, 7], [2, 4, 6, 8], 4.5),
    ]

    for nums1, nums2, expected in test_cases:
        result = sol.findMedianSortedArrays(nums1, nums2)
        status = "✅" if abs(result - expected) < 0.001 else "❌"
        print(f"{status} nums1={nums1}, nums2={nums2} → {result} (期望 {expected})")
