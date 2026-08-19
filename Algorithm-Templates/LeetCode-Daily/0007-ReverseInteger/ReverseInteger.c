/*
 * LeetCode 0007 - 整数反转 (Reverse Integer)
 * 核心思路：逐位弹出再推入，同时检查溢出
 * 时间复杂度 O(log n)，空间复杂度 O(1)
 */

#include <stdio.h>
#include <limits.h>  // INT_MAX, INT_MIN

/*
 * reverse: 反转 32 位有符号整数 x 的数字部分
 * @param x 输入整数（32 位有符号）
 * @return 反转后的整数，溢出则返回 0
 */
int reverse(int x) {
    int rev = 0;  // 存放反转结果

    // 逐位处理，直到 x 为 0
    while (x != 0) {
        int pop = x % 10;  // 弹出最后一位数字
        x /= 10;           // 去掉最后一位

        // ========== 溢出检查（必须在乘法之前做！）==========
        // 正向溢出：rev * 10 + pop > INT_MAX
        if (rev > INT_MAX / 10 || (rev == INT_MAX / 10 && pop > 7))
            return 0;
        // 负向溢出：rev * 10 + pop < INT_MIN
        if (rev < INT_MIN / 10 || (rev == INT_MIN / 10 && pop < -8))
            return 0;

        rev = rev * 10 + pop;  // 推入结果
    }

    return rev;
}


/*
 * main: 本地测试函数
 */
int main() {
    // 测试用例
    int test_cases[] = {123, -123, 120, 0, 1534236469, -2147483648};
    int num_cases = sizeof(test_cases) / sizeof(test_cases[0]);

    for (int i = 0; i < num_cases; i++) {
        int result = reverse(test_cases[i]);
        printf("reverse(%d) = %d\n", test_cases[i], result);
    }

    return 0;
}
