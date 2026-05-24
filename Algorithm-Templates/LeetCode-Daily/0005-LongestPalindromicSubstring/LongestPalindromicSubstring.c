/*
 * LeetCode 0005 - 最长回文子串 (Longest Palindromic Substring)
 * 难度: Medium
 * 核心: 中心扩展法 O(n²)
 *
 * 指针专题：
 * - char* s 作为字符串指针传入
 * - 通过下标 s[left] / s[right] 访问字符
 * - 返回堆上分配的字符串（malloc + strncpy）
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * expandAroundCenter: 从中心向两边扩展，返回回文子串长度
 *
 * 参数：
 *   s     — 字符串指针
 *   left  — 左扩展起点
 *   right — 右扩展起点
 *   n     — 字符串长度
 *
 * 对于奇数回文：left == right（中心是单个字符）
 * 对于偶数回文：right == left + 1（中心是两个字符之间）
 *
 * 返回值：找到的回文子串长度
 */
int expandAroundCenter(const char* s, int left, int right, int n) {
    while (left >= 0 && right < n && *(s + left) == *(s + right)) {
        // *(s + left) 等价于 s[left]
        left--;   // 向左扩展
        right++;  // 向右扩展
    }
    // 退出时 left 和 right 多走了一步
    // 回文长度 = (right-1) - (left+1) + 1 = right - left - 1
    return right - left - 1;
}


/*
 * longestPalindrome: 主函数
 *
 * 参数：
 *   s      — 输入字符串（指针）
 *   returnSize — 返回字符串的长度（输出参数）
 *
 * 返回：最长的回文子串（malloc 分配，调用者负责 free）
 */
char* longestPalindrome(const char* s, int* returnSize) {
    int n = strlen(s);
    if (n < 2) {
        *returnSize = n;
        char* result = (char*)malloc(n + 1);
        strcpy(result, s);
        return result;
    }

    int start = 0;      // 最长回文子串的起始位置
    int maxLen = 1;     // 最长回文子串的长度

    for (int i = 0; i < n; i++) {
        // 奇数长度回文（中心在 i）
        int len1 = expandAroundCenter(s, i, i, n);
        // 偶数长度回文（中心在 i 和 i+1 之间）
        int len2 = expandAroundCenter(s, i, i + 1, n);

        // 取更长的
        int currLen = (len1 > len2) ? len1 : len2;

        if (currLen > maxLen) {
            maxLen = currLen;
            // 计算起始位置：
            // 长度为 currLen 的回文，中心在 i
            // 左边界 = i - (currLen - 1) / 2
            start = i - (currLen - 1) / 2;
        }
    }

    // 分配堆内存返回结果
    *returnSize = maxLen;
    char* result = (char*)malloc(maxLen + 1);
    // strncpy 复制前 maxLen 个字符
    strncpy(result, s + start, maxLen);
    result[maxLen] = '\0';  // 手动加结束符

    return result;
}


// ===== main 测试 =====
int main() {
    int retLen;

    // 测试 1
    char* r1 = longestPalindrome("babad", &retLen);
    printf("✅ s=\"babad\" → \"%.*s\" (长度%d)\n", retLen, r1, retLen);
    free(r1);

    // 测试 2
    char* r2 = longestPalindrome("cbbd", &retLen);
    printf("✅ s=\"cbbd\"  → \"%.*s\" (长度%d)\n", retLen, r2, retLen);
    free(r2);

    // 测试 3: 单字符
    char* r3 = longestPalindrome("a", &retLen);
    printf("✅ s=\"a\"     → \"%.*s\" (长度%d)\n", retLen, r3, retLen);
    free(r3);

    // 测试 4: 空字符串
    char* r4 = longestPalindrome("", &retLen);
    printf("✅ s=\"\"      → \"%.*s\" (长度%d)\n", retLen, r4, retLen);
    free(r4);

    // 测试 5: 全部相同
    char* r5 = longestPalindrome("aaaa", &retLen);
    printf("✅ s=\"aaaa\"  → \"%.*s\" (长度%d)\n", retLen, r5, retLen);
    free(r5);

    // 测试 6: 本身就是回文
    char* r6 = longestPalindrome("racecar", &retLen);
    printf("✅ s=\"racecar\" → \"%.*s\" (长度%d)\n", retLen, r6, retLen);
    free(r6);

    // 测试 7: 双字符回文
    char* r7 = longestPalindrome("abb", &retLen);
    printf("✅ s=\"abb\"    → \"%.*s\" (长度%d)\n", retLen, r7, retLen);
    free(r7);

    return 0;
}
