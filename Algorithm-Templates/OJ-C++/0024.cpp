#include <iostream>  // 引入标准输入输出流库，用于控制台输入与输出 (cin, cout)
#include <vector>    // 引入动态数组 vector 容器头文件，用于存储区间集合
#include <algorithm> // 引入标准算法库，使用其中的 std::sort 函数

using namespace std; // 使用标准命名空间 std，避免后续重复书写 std:: 前缀

// 定义区间结构体
struct Interval {
    int start; // 区间的左端点（起始时间/位置）
    int end;   // 区间的右端点（结束时间/位置）
};

class Solution {
public:

    /**
     * 计算最少需要移除的区间数量，使得剩余区间互不重叠
     * @param intervals 区间结构体向量
     * @return 最少移除的区间个数
     */
    int eraseOverlapIntervals(vector<Interval>& intervals) {
        // 边界情况处理：若输入的区间数组为空，则无需移除任何区间，直接返回 0
        if (intervals.empty()) {
            return 0; 
        }

        // 1. 贪心核心：按区间的右边界（右端点 end）进行升序排序
        // 贪心原理：右端点越小，说明结束得越早，给后续可选区间留出的剩余空间就更大，越不容易冲突
        sort(intervals.begin(), intervals.end(), [](const Interval& a, const Interval& b) {
            return a.end < b.end; // Lambda 比较函数：按右端点从小到大排序
        });

        int count = 1; // 记录可以保留的最大不重叠区间数量，初始默认包含排序后的第 1 个区间
        int prev_end = intervals[0].end; // 记录上一个被选中保留区间的右端点位置

        // 2. 顺序遍历后续的每一个区间
        for (size_t i = 1; i < intervals.size(); ++i) {
            // 如果当前区间的左端点 >= 上一个保留区间的右端点，说明两区间不冲突（允许端点重合接触）
            if (intervals[i].start >= prev_end) {
                count++; // 可以保留当前区间，不重叠区间计数加 1
                prev_end = intervals[i].end; // 更新当前已选区间的右端点，作为后续比较的新基准
            }
            // 若当前区间的左端点 < prev_end，说明与前一区间冲突，由于已按右端点升序排序，
            // 当前区间的右端点一定 >= prev_end，因此直接舍弃当前区间（不更新 prev_end）是最优解
        }

        // 3. 转化关系：最少需要移除的区间数量 = 总区间总数 - 最多可保留的不重叠区间数量
        return intervals.size() - count;
    }
};

int main() {
    // 优化标准输入输出流性能，防止大输入量数据读写超时
    ios_base::sync_with_stdio(false); // 取消 C++ 标准流与 C 语言标准输入输出的同步，提高效率
    cin.tie(NULL); // 解绑 cin 和 cout，避免每次输入前自动刷新输出缓冲区

    int n; // 声明变量 n，用于存储当前测试用例的区间总数
    // 循环读取，支持多组测试数据 (支持在线测评系统的 EOF 结束机制)
    while (cin >> n) {
        vector<Interval> intervals(n); // 创建容量为 n 的 Interval 结构体向量
        for (int i = 0; i < n; ++i) {
            cin >> intervals[i].start >> intervals[i].end; // 依次读入每个区间的起点和终点
        }

        // 实例化 Solution 临时对象并调用解题函数计算结果
        int ans = Solution().eraseOverlapIntervals(intervals);
        cout << ans << "\n"; // 输出计算出的最少移除区间数并换行
    }

    return 0; // 程序正常执行完毕，返回状态码 0
}