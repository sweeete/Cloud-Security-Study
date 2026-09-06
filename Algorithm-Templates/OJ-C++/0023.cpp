#include <iostream> // 引入标准输入输出流库，用于控制台输入输出 (cin, cout)
#include <string>   // 引入字符串类 std::string 头文件
#include <vector>   // 引入动态数组 vector 容器头文件，用于频次统计与状态标记

using namespace std; // 使用标准命名空间 std，避免后续频繁书写 std:: 前缀

class Solution {
public:

    /**
     * 去除字符串中的重复字母，保证每个字母只出现一次，且结果的字典序最小
     * @param s 输入的原字符串
     * @return 去重且保持相对顺序、字典序最小的字符串
     */
    string removeDuplicateLetters(string s) {
        // 1. 统计字符串中每个字符出现的剩余频次
        vector<int> count(26, 0); // 创建大小为 26 的数组，记录 26 个小写字母出现的总次数
        for (char ch : s) {      // 遍历输入的字符串 s
            count[ch - 'a']++;   // 将字符转化为 0-25 的索引，对应频次加 1
        }

        // 2. in_stack 标记字符当前是否已经在结果栈中
        vector<bool> in_stack(26, false); // 布尔数组，记录某个字符当前是否已处于结果栈内
        string result = ""; // 使用 std::string 模拟单调栈（利用 back(), push_back(), pop_back()）

        // 3. 顺序遍历字符串中的每一个字符
        for (char ch : s) {          // 逐个字符进行决策处理
            int idx = ch - 'a';      // 计算当前字符在 26 个字母中的相对索引 (0-25)
            // 当前字符已扫描过一次，后续未处理字符串中该字符的剩余可用频次减 1
            count[idx]--;

            // 如果当前字符已经在结果栈中，直接跳过
            // 贪心依据：越靠前出现的字符越小，结果的字典序越小；前面保留的必定是更优位置
            if (in_stack[idx]) {
                continue; // 终止当前轮次，处理下一个字符
            }

            // 贪心弹栈逻辑（维护单调递增栈）：
            // 当栈不为空，且当前字符比栈顶字符更小（ch < result.back()，说明替换后字典序更小），
            // 并且栈顶字符在后续字符串中还会再次出现（count > 0，保障后续还能有机会补上该字符）时，将栈顶弹出
            while (!result.empty() && ch < result.back() && count[result.back() - 'a'] > 0) {
                char top = result.back();       // 获取当前栈顶字符
                in_stack[top - 'a'] = false;    // 撤销栈顶字符的在栈标记，表示已被弹出
                result.pop_back();              // 弹出栈顶字符（模拟栈的 pop 操作）
            }

            // 将当前字符压入栈中，并标记为已在栈中
            result.push_back(ch); // 将当前字符加入结果字符串末尾（模拟入栈）
            in_stack[idx] = true; // 标记当前字符已存在于栈内，防止后续重复添加
        }

        return result; // 返回最终通过单调栈构造出的字典序最小的去重字符串
    }
};

int main() {
    // 优化标准输入输出流读写性能
    ios_base::sync_with_stdio(false); // 取消 C++ 标准流与 C 语言标准输入输出的同步，提高效率
    cin.tie(NULL); // 解绑 cin 和 cout，避免每次 cin 前自动刷新缓冲区

    string s; // 声明字符串变量 s，用于存储输入的字符串
    // 循环读取输入，支持 OJ 的多组测试数据 (EOF 机制)
    while (cin >> s) { // 持续读取字符串直到文件结束 (EOF)
        string ans = Solution().removeDuplicateLetters(s); // 实例化 Solution 对象并调用算法求解
        cout << ans << "\n"; // 输出最终去重后的最小字典序字符串并换行
    }

    return 0; // 程序正常执行完毕，返回状态码 0
}