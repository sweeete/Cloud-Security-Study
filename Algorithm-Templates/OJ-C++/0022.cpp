#include <iostream>  // 引入标准输入输出流库，用于控制台输入输出 (cin, cout)
#include <vector>    // 引入动态数组 vector 容器头文件，用于存储人员体重数据
#include <algorithm> // 引入常用算法库，主要使用其中的 std::sort 函数

using namespace std; // 使用标准命名空间 std，避免后续频繁书写 std:: 前缀

class Solution {
public:

    /**
     * 计算救离所有人需要的最少救援船只数量
     * @param people 包含每个人体重的数组
     * @param limit 每艘船的最大载重上限（每艘船最多只能坐两个人）
     * @return 最少需要的船只数量
     */
    int numRescueBoats(vector<int>& people, int limit) {
        // 1. 先对体重数组进行升序排序，方便后续双指针进行首尾贪心匹配
        sort(people.begin(), people.end()); // 将人员体重按照从小到大重新排列

        int left = 0;                  // 左指针：指向当前剩余未登船人员中最轻的人
        int right = people.size() - 1; // 右指针：指向当前剩余未登船人员中最重的人
        int boats = 0;                  // 记录累计需要的救援船只数量，初始为 0

        // 2. 双指针向中间收拢，直到所有人都有船坐
        while (left <= right) {
            // 如果只剩下最后一个人，独占一艘船
            if (left == right) {
                boats++; // 增加一艘船给最后这一个人
                break;   // 所有人处理完毕，直接跳出循环
            }

            // 贪心决策：尝试将最重的人 (people[right]) 和最轻的人 (people[left]) 同乘一船
            if (people[left] + people[right] <= limit) {
                // 如果最轻和最重的人体重之和未超过载重上限 limit
                left++; // 最轻的人可以一起上船，左指针右移指向下一个最轻的人
            }

            // 无论最轻的人能否同乘，最重的人 (people[right]) 这趟都必须坐走一艘船
            right--; // 最重的人已上船，右指针左移指向下一个最重的人
            boats++; // 消耗一艘救援船，船只计数加 1
        }

        return boats; // 返回最终计算出的最少救援船只总数
    }
};

int main() {
    // 优化 C++ 标准输入输出流性能，防止大量数据读写超时
    ios_base::sync_with_stdio(false); // 取消 C++ 输入输出流与 C 语言标准流的同步，提升效率
    cin.tie(NULL); // 解绑 cin 和 cout，防止每次 cin 输入前强制刷新 cout 输出缓冲区

    int n; // 声明变量 n，用于存储当前测试用例的人员总数
    // 使用 while (cin >> n) 读取，支持 OJ 多组测试数据与 EOF 机制
    while (cin >> n) { // 持续读取人员数量，直到文件读取结束 (EOF)
        vector<int> people(n); // 创建大小为 n 的 vector 容器存储每个人员的体重
        for (int i = 0; i < n; ++i) { // 循环 n 次，读入所有人的体重
            cin >> people[i]; // 读取单个人员的体重数值
        }

        int limit; // 声明变量 limit，用于存储船只的载重上限
        cin >> limit; // 读取每艘船的最大载重量 limit

        // 调用算法计算最少船只数
        int ans = Solution().numRescueBoats(people, limit); // 实例化 Solution 对象并调用 numRescueBoats 计算结果
        cout << ans << "\n"; // 输出最少需要的船只数量并换行
    }

    return 0; // 程序正常执行完毕，返回状态码 0
}