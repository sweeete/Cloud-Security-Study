#include <iostream>      // 引入标准输入输出流库，用于控制台输入输出 (cin, cout)
#include <vector>        // 引入动态数组 vector 容器头文件，用于存储输入的整数序列
#include <unordered_map> // 引入无序哈希表头文件，用于高效存储元素频数与结尾标记 (O(1) 查找)

using namespace std; // 使用标准命名空间 std，避免后续重复书写 std:: 前缀

/**
 * 判断给定的升序数组是否可以分割成若干个长度至少为 3 的连续递增子序列
 * @param nums 输入的按升序排列的整数向量
 * @return 是否能完全分割
 */
bool isPossible(const vector<int>& nums) {
    unordered_map<int, int> count; // 哈希表 1：记录数组中每个数字当前的剩余可用次数（频数表）
    unordered_map<int, int> tail;  // 哈希表 2：记录以数字 key 结尾的合法子序列（长度>=3）的数量（结尾表）

    // 1. 统计每个数字在原数组中出现的总频数
    for (int x : nums) { // 遍历数组中的每一个元素 x
        count[x]++;      // 将数字 x 的出现次数加 1
    }

    // 2. 贪心策略遍历：按升序依次处理每个数字，优先扩充现有子序列，其次新建长度为 3 的新子序列
    for (int x : nums) {
        // 如果数字 x 已经被之前的匹配逻辑消耗完毕（频数为 0），直接跳过处理下一个
        if (count[x] == 0) continue;

        // 贪心决策 1：优先将 x 接在已有以 x - 1 结尾的子序列后面（最节省资源）
        if (tail[x - 1] > 0) {
            tail[x - 1]--; // 以 x - 1 结尾的子序列数量减 1（旧结尾被替代）
            tail[x]++;     // 以 x 结尾的子序列数量加 1（形成新的更长子序列）
            count[x]--;    // 消耗一个数字 x，其剩余频数减 1
        } 
        // 贪心决策 2：若无法追加，则尝试将 x, x+1, x+2 组合成一个长度至少为 3 的全新子序列
        else if (count[x + 1] > 0 && count[x + 2] > 0) {
            count[x]--;     // 消耗一个数字 x，频数减 1
            count[x + 1]--; // 消耗一个数字 x + 1，频数减 1
            count[x + 2]--; // 消耗一个数字 x + 2，频数减 1
            tail[x + 2]++;  // 成功构建新子序列，以 x + 2 结尾的合规子序列数量加 1
        } 
        // 既不能追加到现有序列，也无法凑出长度为 3 的新序列，分割宣告失败。必须每个元素都能被分配到合法子序列中。
        else {
            return false; // 直接返回 false，无法完成合法分割
        }
    }

    return true; // 所有数字均被成功合规分配，返回 true
}

int main() {
    // 优化标准输入输出流读写性能，提升大输入量时的执行速度
    ios::sync_with_stdio(false); // 取消 C++ 标准流与 C 语言输入输出流的同步
    cin.tie(nullptr);            // 解绑 cin 与 cout，避免每次 cin 前强制刷新输出缓冲区

    int n; // 声明变量 n，用于存储输入的整数个数
    if (cin >> n) { // 读取数组元素数量 n，若读取成功则进入内部逻辑
        vector<int> nums(n); // 创建容量为 n 的整型向量，存储输入的数字序列
        for (int i = 0; i < n; ++i) { // 循环 n 次，读入所有元素
            cin >> nums[i]; // 读取第 i 个整数存入数组
        }

        // 调用算法判断是否可分割，并根据结果输出对应的文本
        if (isPossible(nums)) {
            cout << "true\n";  // 可分割，输出 "true" 并换行
        } else {
            cout << "false\n"; // 不可分割，输出 "false" 并换行
        }
    }
    return 0; // 程序正常执行完毕，返回状态码 0
}