/*
 * LeetCode 0006 - Z 字形变换 (Zigzag Conversion)
 * 核心: 模拟 Z 字形遍历
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* convert(char* s, int numRows) {
    int n = strlen(s);
    if (numRows == 1 || numRows >= n) {
        char* result = (char*)malloc(n + 1);
        strcpy(result, s);
        return result;
    }

    // 为每一行分配字符串空间
    char** rows = (char**)malloc(numRows * sizeof(char*));
    for (int i = 0; i < numRows; i++) {
        rows[i] = (char*)calloc(n + 1, 1);
    }

    int row = 0;
    int step = 1;

    for (int i = 0; i < n; i++) {
        // 将字符追加到当前行
        int len = strlen(rows[row]);
        rows[row][len] = s[i];

        if (row == 0)
            step = 1;
        else if (row == numRows - 1)
            step = -1;
        row += step;
    }

    // 合并所有行
    char* result = (char*)malloc(n + 1);
    result[0] = '\0';
    for (int i = 0; i < numRows; i++) {
        strcat(result, rows[i]);
        free(rows[i]);
    }
    free(rows);

    return result;
}


int main() {
    char s1[] = "PAYPALISHIRING";
    char* r1 = convert(s1, 3);
    printf("✅ \"%s\" (3) → \"%s\"\n", s1, r1); free(r1);

    char* r2 = convert(s1, 4);
    printf("✅ \"%s\" (4) → \"%s\"\n", s1, r2); free(r2);

    char s2[] = "A";
    char* r3 = convert(s2, 1);
    printf("✅ \"%s\" (1) → \"%s\"\n", s2, r3); free(r3);

    char s3[] = "ABC";
    char* r4 = convert(s3, 2);
    printf("✅ \"%s\" (2) → \"%s\"\n", s3, r4); free(r4);

    return 0;
}
