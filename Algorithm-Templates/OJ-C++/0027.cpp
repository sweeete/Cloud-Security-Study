#include <iostream>  // 引入标准输入输出流头文件，用于控制台输入输出 (cin, cout)
#include <vector>    // 引入动态数组 vector 容器头文件，用于存储数字序列
#include <algorithm> // 引入常用算法库头文件，使用其中的 std::max 和 std::min 函数

using namespace std; // 使用标准命名空间 std，简化代码中对标准库组件的调用

class Solution { // 定义解题类 Solution
public: // 公有成员访问权限控制标识符
    /**
     * 主函数：从 nums1 和 nums2 中挑选 k 个数字，拼接出字典序最大的组合
     * @param nums1 第一个输入数字数组
     * @param nums2 第二个输入数字数组
     * @param k 需要挑选的数字总个数
     * @return 字典序最大的长度为 k 的数字组合向量
     */
    vector<int> maxNumber(vector<int>& nums1, vector<int>& nums2, int k) {
        int m = nums1.size(); // 获取数组 nums1 的元素总个数 m
        int n = nums2.size(); // 获取数组 nums2 的元素总个数 n
        vector<int> maxResult(k, 0); // 初始化长度为 k 的答案向量，用于存储并更新全局最大字典序组合，默认初始化为 0

        // 计算从 nums1 中选取的元素个数 i 的合法范围
        int start = max(0, k - n); // 确定从 nums1 选取的最小元素个数：若所需 k 超过 nums2 长度 n，则 nums1 必须至少贡献 k - n 个元素
        int end = min(m, k);       // 确定从 nums1 选取的最大元素个数：最多只能选 m 个，且不能超过需要获取的总数 k

        // 枚举所有可能的元素分配方案
        for (int i = start; i <= end; ++i) { // 循环遍历每一种分配可能：从 nums1 选 i 个，从 nums2 选 k - i 个
            // 1. 分别提取长度为 i 和 k - i 的最大子序列
            vector<int> sub1 = maxSubsequence(nums1, i);     // 调用单调栈算法，提取 nums1 中长度为 i 的字典序最大子序列
            vector<int> sub2 = maxSubsequence(nums2, k - i); // 调用单调栈算法，提取 nums2 中长度为 k - i 的字典序最大子序列

            // 2. 贪心合并两个子序列
            vector<int> candidate = merge(sub1, sub2); // 将两个最大子序列按字典序贪心规则归并成长度为 k 的候选数组

            // 3. 按照字典序更新最大结果
            if (candidate > maxResult) { // C++ vector 默认重载了 > 运算符，直接支持按字典序比较数组大小
                maxResult = candidate;  // 若当前候选数组字典序更大，则更新全局最大结果数组 maxResult
            } // 结束字典序更新条件判断
        } // 结束穷举遍历循环

        return maxResult; // 返回求解出的字典序最大的长度为 k 的数字序列
    } // 结束 maxNumber 函数

private: // 私有成员访问权限控制标识符，封装内部辅助算法函数
    // 利用单调栈原理求单个数组中长度为 count 的最大子序列
    vector<int> maxSubsequence(const vector<int>& nums, int count) {
        int n = nums.size(); // 获取当前输入数组 nums 的总长度
        vector<int> stk;     // 使用 vector 模拟单调递减栈结构
        int drop = n - count; // 计算最多允许丢弃（弹出）的元素个数，确保最终留下的元素不少于 count 个

        for (int x : nums) { // 范围 for 循环，依次遍历数组 nums 中的每一个数字 x
            while (drop > 0 && !stk.empty() && stk.back() < x) { // 当还能丢弃元素、栈非空且栈顶元素小于当前数字 x 时进行循环
                stk.pop_back(); // 弹出小于 x 的栈顶元素，以保持高位数字尽可能大（维护单调递减性质）
                drop--;         // 丢弃次数消耗 1
            } // 结束单调栈弹栈循环
            stk.push_back(x); // 将当前数字 x 压入栈中
        } // 结束元素遍历循环

        stk.resize(count); // 若入栈元素数量超过所需的 count 个，直接截断只保留前 count 个元素
        return stk;        // 返回构建完成的单数组最大子序列
    } // 结束 maxSubsequence 函数

    // 比较两个后缀子序列的字典序
    bool compare(const vector<int>& nums1, int i, const vector<int>& nums2, int j) {
        int m = nums1.size(); // 获取 nums1 数组的总长度
        int n = nums2.size(); // 获取 nums2 数组的总长度
        while (i < m && j < n) { // 当两个后缀子序列均未遍历到末尾时持续比较
            if (nums1[i] != nums2[j]) { // 遇到第一个不相等的字符/数字时判断大小
                return nums1[i] > nums2[j]; // 若 nums1[i] 更大，返回 true 表示 nums1 的后缀字典序更大；反之返回 false
            } // 结束不相等比较分支
            i++; // nums1 的比较指针向后移动一位
            j++; // nums2 的比较指针向后移动一位
        } // 结束双指针逐位对比循环
        return (m - i) > (n - j); // 当存在相同前缀时，剩余较长的后缀序列字典序更大，返回比较结果
    } // 结束 compare 函数

    // 按字典序贪心合并两个子序列
    vector<int> merge(const vector<int>& nums1, const vector<int>& nums2) {
        int m = nums1.size(); // 获取子序列 nums1 的长度
        int n = nums2.size(); // 获取子序列 nums2 的长度
        vector<int> res(m + n); // 创建大小为 m + n 的结果数组 res
        int i = 0, j = 0, r = 0; // 初始化指针：i 指向 nums1，j 指向 nums2，r 指向结果数组 res

        while (i < m || j < n) { // 只要还有元素未被合并就继续循环
            if (compare(nums1, i, nums2, j)) { // 调用 compare 比较后续子序列字典序，若 nums1 后续字典序更大
                res[r++] = nums1[i++]; // 优先选取 nums1[i] 填入结果数组，并将指针 i 和 r 分别自增 1
            } else { // 若 nums2 后续字典序更大或相等
                res[r++] = nums2[j++]; // 选取 nums2[j] 填入结果数组，并将指针 j 和 r 分别自增 1
            } // 结束合并选择分支
        } // 结束归并循环
        return res; // 返回合并后的最大组合序列
    } // 结束 merge 函数
}; // 结束 Solution 类定义

int main() // 主程序入口函数
{ // 主函数体开始
    int m, n, k, data; // 声明变量：m (nums1长度), n (nums2长度), k (目标组合长度), data (输入暂存变量)
    vector<int> nums1, nums2; // 声明两个整型向量用于存储输入的数字序列
    cin >> m; // 从标准输入读取 nums1 数组的长度 m
    for(int i = 0; i < m; i++) // 循环 m 次以读取 nums1 的各个元素
    { // 循环体开始
        cin >> data; // 读入单个数存入 data
        nums1.push_back(data); // 将 data 追加到 nums1 向量末尾
    } // 结束 nums1 读入循环
    cin >> n; // 从标准输入读取 nums2 数组的长度 n
    for(int i = 0; i < n; i++) // 循环 n 次以读取 nums2 的各个元素
    { // 循环体开始
        cin >> data; // 读入单个数存入 data
        nums2.push_back(data); // 将 data 追加到 nums2 向量末尾
    } // 结束 nums2 读入循环
    cin >> k; // 读取目标挑选的序列长度 k
    vector<int> res = Solution().maxNumber(nums1, nums2, k); // 创建 Solution 临时对象并调用 maxNumber 获取求解结果
    for(int i = 0; i < res.size(); i++) // 循环遍历最终结果数组中的每个数字
        cout << res[i]; // 依次打印结果数组中的数字，拼接成最大数输出

    return 0; // 程序正常结束，向系统返回状态码 0
} // 结束 main 函数