/*
 * LeetCode 0004 - 寻找两个正序数组的中位数
 * 难度: Hard
 * 核心: 二分查找 + 分割法
 *
 * 指针专题：
 * - nums1, nums2 作为函数参数本质上是指针
 * - nums1[i] 等价于 *(nums1 + i)
 * - 用条件表达式处理数组边界（避免越界）
 */

#include <stdio.h>
#include <limits.h>  // 提供 INT_MIN / INT_MAX

/*
 * 函数：findMedianSortedArrays
 * 参数：
 *   nums1   — 第一个升序数组（指针）
 *   nums1Size — nums1 的长度
 *   nums2   — 第二个升序数组（指针）
 *   nums2Size — nums2 的长度
 * 返回：两个数组合并后的中位数
 */
double findMedianSortedArrays(int* nums1, int nums1Size, int* nums2, int nums2Size) {
    // 保证 nums1 是较短的数组
    // 如果 nums1 更长，交换指针和长度
    if (nums1Size > nums2Size) {
        int* tmp_arr = nums1; nums1 = nums2; nums2 = tmp_arr;
        int tmp_len = nums1Size; nums1Size = nums2Size; nums2Size = tmp_len;
    }

    int m = nums1Size;  // 较短数组的长度
    int n = nums2Size;  // 较长数组的长度
    int total_left = (m + n + 1) / 2;  // 左半部分元素总数

    int left = 0, right = m;

    while (left <= right) {
        // i: nums1 的分割点（左边有 i 个元素）
        int i = (left + right) / 2;
        // j: nums2 的分割点（左边有 j 个元素）
        int j = total_left - i;

        // 处理边界：用条件表达式替代指针访问
        // 关键：i=0 时左边无元素 → 用 -∞
        //       i=m 时右边无元素 → 用 +∞
        int nums1_left  = (i == 0)   ? INT_MIN : *(nums1 + i - 1);
        int nums1_right = (i == m)   ? INT_MAX : *(nums1 + i);
        int nums2_left  = (j == 0)   ? INT_MIN : *(nums2 + j - 1);
        int nums2_right = (j == n)   ? INT_MAX : *(nums2 + j);

        // *(nums1 + i - 1) 等价于 nums1[i-1]
        // 这是指针算术的语法糖

        if (nums1_left <= nums2_right && nums2_left <= nums1_right) {
            // 找到正确的分割了！
            if ((m + n) % 2 == 1) {
                // 奇数个：取左半部分最大值
                int left_max = (nums1_left > nums2_left) ? nums1_left : nums2_left;
                return (double)left_max;
            } else {
                // 偶数个：(左最大 + 右最小) / 2
                int left_max = (nums1_left > nums2_left) ? nums1_left : nums2_left;
                int right_min = (nums1_right < nums2_right) ? nums1_right : nums2_right;
                return (left_max + right_min) / 2.0;
            }
        } else if (nums1_left > nums2_right) {
            // nums1 左边太大了 → 分割点左移
            right = i - 1;
        } else {
            // nums1 右边太小了 → 分割点右移
            left = i + 1;
        }
    }

    return 0.0;  // 不应到达这里
}


// ===== main 测试 =====
int main() {
    // 测试用例
    int nums1_1[] = {1, 3};
    int nums2_1[] = {2};
    double r1 = findMedianSortedArrays(nums1_1, 2, nums2_1, 1);
    printf("✅ [1,3] + [2] → %.2f (期望 2.00)\n", r1);

    int nums1_2[] = {1, 2};
    int nums2_2[] = {3, 4};
    double r2 = findMedianSortedArrays(nums1_2, 2, nums2_2, 2);
    printf("✅ [1,2] + [3,4] → %.2f (期望 2.50)\n", r2);

    int nums1_3[] = {0, 0};
    int nums2_3[] = {0, 0};
    double r3 = findMedianSortedArrays(nums1_3, 2, nums2_3, 2);
    printf("✅ [0,0] + [0,0] → %.2f (期望 0.00)\n", r3);

    // 空数组测试
    int nums1_4[] = {};
    int nums2_4[] = {1};
    double r4 = findMedianSortedArrays(nums1_4, 0, nums2_4, 1);
    printf("✅ [] + [1] → %.2f (期望 1.00)\n", r4);

    int nums1_5[] = {2};
    int nums2_5[] = {};
    double r5 = findMedianSortedArrays(nums1_5, 1, nums2_5, 0);
    printf("✅ [2] + [] → %.2f (期望 2.00)\n", r5);

    int nums1_6[] = {1, 3, 5, 7};
    int nums2_6[] = {2, 4, 6, 8};
    double r6 = findMedianSortedArrays(nums1_6, 4, nums2_6, 4);
    printf("✅ [1,3,5,7] + [2,4,6,8] → %.2f (期望 4.50)\n", r6);

    return 0;
}
