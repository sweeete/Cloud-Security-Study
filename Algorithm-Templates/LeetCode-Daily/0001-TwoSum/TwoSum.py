from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

if __name__ == "__main__":
    sol = Solution()
    test_nums = [2, 7, 11, 15]
    test_target = 9

    result = sol.twoSum(test_nums, test_target)
    print(f"输入: nums = {test_nums}, target = {test_target}")
    print(f"输出下标: {result}")
