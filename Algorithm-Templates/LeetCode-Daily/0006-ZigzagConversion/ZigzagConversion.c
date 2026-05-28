/*
 * LeetCode 0006 - Z 字形变换 (Zigzag Conversion)
 * 核心思路：模拟 Z 字形遍历，用 numRows 个"桶"逐行收集字符
 * 时间复杂度 O(n)，空间复杂度 O(n)
 */

#include <stdio.h>    // printf
#include <stdlib.h>   // malloc, calloc, free
#include <string.h>   // strlen, strcpy, strcat

/*
 * convert: 将字符串 s 按 Z 字形排列后逐行读取输出
 * @param s       原字符串
 * @param numRows 指定的行数
 * @return 按行读取后的新字符串（调用者需 free）
 */
char* convert(char* s, int numRows) {
    // ========== 1. 获取字符串长度 ==========
    int n = strlen(s);

    // ========== 2. 处理边界情况 ==========
    // 只有 1 行 → Z 字形就是一条直线，直接返回原串
    // 行数 >= 字符数 → 每个字符独占一行，顺序不变，直接返回
    if (numRows == 1 || numRows >= n) {
        char* result = (char*)malloc(n + 1);  // +1 给结尾 '\0'
        strcpy(result, s);
        return result;
    }

    // ========== 3. 创建 "桶"（每一行一个字符串）==========
    // rows 是一个指针数组，每个元素指向一行字符数组
    // 之所以用 char**，是因为我们要动态创建 numRows 个字符串
    char** rows = (char**)malloc(numRows * sizeof(char*));
    for (int i = 0; i < numRows; i++) {
        // calloc(n+1, 1) 分配 n+1 字节并全部置零
        // 最坏情况：所有字符可能都在同一行，所以每行预留 n+1 空间
        // calloc 比 malloc 好在自动初始化所有字节为 '\0'
        rows[i] = (char*)calloc(n + 1, 1);
    }

    // ========== 4. 模拟 Z 字形遍历 ==========
    int row = 0;    // 当前行索引（从 0 开始）
    int step = 1;   // 方向：1 表示向下移动，-1 表示向上移动

    // 遍历字符串的每一个字符
    for (int i = 0; i < n; i++) {
        // ----- 4a. 将当前字符追加到当前行 -----
        // strlen(rows[row]) 找到当前行已有内容的末尾位置
        // 直接在该位置写入字符（不需要手动加 '\0'，因为 calloc 已经全置零）
        int len = strlen(rows[row]);
        rows[row][len] = s[i];

        // ----- 4b. 方向控制 -----
        // 关键逻辑：碰到顶部（row==0）就转向下，碰到底部（row==numRows-1）就转向上
        // 其他位置保持当前方向不变
        if (row == 0)
            step = 1;               // 到达顶部 → 改为向下走
        else if (row == numRows - 1)
            step = -1;              // 到达底部 → 改为向上走
        // 注意：先判断边界再移动 row，确保拐点位置的字符落在正确行
        row += step;
    }

    // ========== 5. 合并所有行 ==========
    // 申请结果字符串空间
    char* result = (char*)malloc(n + 1);
    result[0] = '\0';  // 初始化为空字符串，为 strcat 做准备

    // 从第 0 行到第 numRows-1 行，逐行拼接到 result
    for (int i = 0; i < numRows; i++) {
        strcat(result, rows[i]);  // 将第 i 行的内容追加到 result 末尾
        free(rows[i]);            // 每行的桶用完了就释放
    }
    free(rows);  // 释放指针数组

    return result;  // 调用者记得 free 返回值
}


/*
 * main: 本地测试函数
 */
int main() {
    // 测试用例 1：numRows = 3
    char s1[] = "PAYPALISHIRING";
    char* r1 = convert(s1, 3);
    printf("✅ \"%s\" (3) → \"%s\"\n", s1, r1);
    free(r1);

    // 测试用例 2：numRows = 4
    char* r2 = convert(s1, 4);
    printf("✅ \"%s\" (4) → \"%s\"\n", s1, r2);
    free(r2);

    // 测试用例 3：单个字符
    char s2[] = "A";
    char* r3 = convert(s2, 1);
    printf("✅ \"%s\" (1) → \"%s\"\n", s2, r3);
    free(r3);

    // 测试用例 4：numRows = 2
    char s3[] = "ABC";
    char* r4 = convert(s3, 2);
    printf("✅ \"%s\" (2) → \"%s\"\n", s3, r4);
    free(r4);

    return 0;
}
