#include <stdio.h>

int lengthOfLongestSubstring(char* s) {
    int last[256];
    //初始化数组
    for (int i = 0; i < 256; i++) {
        last[i] = -1;
    }
    int left = 0;
    int ans = 0;//符合条件的子串的长度
    for (int right = 0; s[right] != '\0'; right++) {
        unsigned char c = (unsigned char)s[right];//按无符号数解释，防止出现负数
        int prev = last[c];//prev表示当前字符上一次出现的位置
        if (prev >= left) {//如果上一次出现在窗口外
            left = prev + 1;//则更新窗口左边界
        }
        last[c] = right;//更新当前字符最新出现的位置
        int len = right - left + 1;//计算长度
        if (len > ans) {//ans表示最大长度
            ans = len;
        }
    }
    return ans;//返回的是长度
}

int main(void) {
    const char* cases[] = {
        "abcabcbb",
        "bbbbb",
        "pwwkew",
        "",
    };
    int expected[] = {3, 1, 3, 0};//预期的正确值
    int n = (int)(sizeof(cases) / sizeof(cases[0]));//计算出测试用例中共有多少字符串
    for (int i = 0; i < n; i++) {
        int out = lengthOfLongestSubstring((char*)cases[i]);//这里是强制类型转换，把只读的指针改成可写的
        printf("s=\"%s\" -> %d (expect %d)\n", cases[i], out, expected[i]);//这里的反斜杠是转义字符
    }
    return 0;
}
