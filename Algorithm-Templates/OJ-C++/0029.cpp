#include <iostream>  // 引入标准输入输出流库，用于控制台交互 (cin, cout)
#include <vector>    // 引入动态数组 vector 容器头文件
#include <algorithm> // 引入标准算法库头文件，使用 std::sort 函数

using namespace std; // 使用标准命名空间 std，避免频繁书写 std:: 前缀

class Solution { // 定义解题类 Solution
public: // 公有成员访问控制标识符
    /**
     * 计算使得每个区间内至少包含集合 S 中两个元素的最小集合大小
     * @param intervals 二维数组，表示若干闭区间 [start, end]
     * @return 满足条件的最小集合 S 的元素个数
     */
    int intersectionSizeTwo(vector<vector<int>>& intervals) {
        // 1. 贪心排序：按右端点升序排列；右端点相同时，按左端点降序排列
        // 排序规则说明：右端点越小越靠前，给后续区间留出的覆盖空间更大；
        // 若右端点相同，左端点大的区间更短（包含范围更窄），应优先处理以优先满足其严格覆盖要求。
        sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
            if (a[1] != b[1]) { // 若两区间的右端点不相等
                return a[1] < b[1]; // 优先按右端点升序排序（贪心：尽可能选靠右的点）
            }
            return a[0] > b[0]; // 若右端点相同，按左端点降序排序（让短区间排在前面先被覆盖）
        }); // 结束 Lambda 表达式排序调用

        int ans = 0;   // 记录最终构成的最小集合 S 的元素总个数
        int p1 = -1;  // 记录当前集合 S 中已挑选的“倒数第二个元素”（数值较小者，初始为无效值 -1）
        int p2 = -1;  // 记录当前集合 S 中已挑选的“倒数第一个元素”（数值最大者，初始为无效值 -1）

        // 2. 遍历每一个区间进行贪心选择，确保每个区间至少包含已选的 2 个数字
        for (const auto& interval : intervals) { // 范围 for 循环遍历每一个区间
            int s = interval[0]; // 提取当前闭区间的左端点 s (start)
            int e = interval[1]; // 提取当前闭区间的右端点 e (end)

            // 情况 1：当前区间的左端点大于已选的最大值 p2，说明已选点与当前区间完全无重叠 (覆盖 0 个元素)
            if (s > p2) { // 需新增 2 个元素
                ans += 2;   // 集合大小累加 2
                p1 = e - 1; // 贪心选取当前区间最靠右侧的两个整数：倒数第二个填入 e - 1
                p2 = e;     // 最大的元素填入右端点 e，以最大限度覆盖后续潜在重叠区间
            } 
            // 情况 2：当前区间只包含了已选的较大值 p2，而较小值 p1 在区间左侧之外 (覆盖 1 个元素)
            else if (s > p1) { // 需新增 1 个元素
                ans += 1; // 集合大小累加 1
                if (p2 == e) { // 特殊边界：若当前最大值 p2 正好处于右端点 e，不能重复选 e
                    p1 = e - 1; // 只能选前一个位置 e - 1 作为新的较小值 p1，p2 保持为 e 不变
                } else { // 一般情况：p2 < e
                    p1 = p2;    // 原较大的 p2 变为新的较小值 p1
                    p2 = e;     // 补充右端点 e 作为新的最大值 p2，保持选择尽量靠右
                }
            }
            // 情况 3：s <= p1，说明已选的 p1 和 p2 均处于当前区间 [s, e] 之内 (已被覆盖 2 个元素)
            // 此时当前区间已满足“至少包含 2 个元素”的限制条件，无需进行任何添加与更新操作
        } // 结束区间遍历循环

        return ans; // 返回满足所有区间要求的最小集合 S 的大小
    } // 结束 intersectionSizeTwo 函数
}; // 结束 Solution 类定义

int main() // 主程序入口函数
{
    // 提升 IO 标准输入输出效率，防止数据量较大时超时
    ios::sync_with_stdio(false); // 取消 C++ 标准流与 C 语言标准输入输出流同步
    cin.tie(nullptr);            // 解绑 cin 与 cout，避免每次 input 前强制刷新缓冲区

    int m, n, data; // 声明输入处理临时变量：m 为区间总数，n 为未定义参数，data 为读入数据暂存
    vector<vector<int> > intervals; // 声明二维向量 intervals，存储所有输入的区间
    if (cin >> m) { // 成功读取区间总数量 m 时进入处理逻辑
        for(int j = 0; j < m; j++) // 循环 m 次读取 m 个区间
        {
            vector<int> aRow; // 创建单行动态数组，用于存放单个区间的起止点 [s, e]
            for(int i = 0; i < 2; i++) // 每个区间包含起点和终点 2 个数值
            {
                cin >> data; // 从标准输入读取端点值
                aRow.push_back(data); // 将端点值加入单行区间数组
            }
            intervals.push_back(aRow); // 将构造好的单行区间压入 intervals 集合中
        }

        int res = Solution().intersectionSizeTwo(intervals); // 实例化 Solution 并调用算法求解
        cout << res; // 输出最终求解出的最小集合大小
    }

    return 0; // 程序正常运行完毕，向系统返回状态 0
}