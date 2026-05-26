/*
 * LeetCode 0005 - 最长回文子串
 * 核心: 中心扩展法 O(n²)
 *
 * 函数签名与 LeetCode 完全一致：
 *   char* longestPalindrome(char* s)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int expandAroundCenter(char* s, int left, int right, int n) {
    while (left >= 0 && right < n && s[left] == s[right]) {
        left--;
        right++;
    }
    return right - left - 1;
}

char* longestPalindrome(char* s) {
    int n = strlen(s);
    if (n < 2) {
        char* result = (char*)malloc(n + 1);
        strcpy(result, s);
        return result;
    }

    int start = 0;
    int maxLen = 1;

    for (int i = 0; i < n; i++) {
        int len1 = expandAroundCenter(s, i, i, n);
        int len2 = expandAroundCenter(s, i, i + 1, n);
        int currLen = (len1 > len2) ? len1 : len2;

        if (currLen > maxLen) {
            maxLen = currLen;
            start = i - (currLen - 1) / 2;
        }
    }

    char* result = (char*)malloc(maxLen + 1);
    strncpy(result, s + start, maxLen);
    result[maxLen] = '\0';
    return result;
}


int main() {
    char s1[] = "babad";
    char* r1 = longestPalindrome(s1);
    printf("✅ \"babad\"  → \"%s\"\n", r1); free(r1);

    char s2[] = "cbbd";
    char* r2 = longestPalindrome(s2);
    printf("✅ \"cbbd\"   → \"%s\"\n", r2); free(r2);

    char s3[] = "a";
    char* r3 = longestPalindrome(s3);
    printf("✅ \"a\"      → \"%s\"\n", r3); free(r3);

    char s4[] = "racecar";
    char* r4 = longestPalindrome(s4);
    printf("✅ \"racecar\" → \"%s\"\n", r4); free(r4);

    char s5[] = "aaaa";
    char* r5 = longestPalindrome(s5);
    printf("✅ \"aaaa\"   → \"%s\"\n", r5); free(r5);

    return 0;
}
