#include <iostream> // 引入标准输入输出流库，用于控制台交互 (cin, cout)
#include <vector>   // 引入动态数组 vector 容器头文件
#include <string>   // 引入 string 字符串头文件

using namespace std; // 使用标准命名空间 std，简化标准库组件调用

class Solution { // 定义解题类 Solution
public:
    /**
     * 判断两个等长且互为字母异位词的字符串是否相似
     * @param s1 第一个字符串
     * @param s2 第二个字符串
     * @return 若相同或仅有两处字符不同（即交换一次可重合）则返回 true，否则返回 false
     */
    bool isSimilar(const string& s1, const string& s2) {
        int diffCount = 0; // 记录两字符串在对应位置上字符不相等的次数
        int len = s1.length(); // 获取字符串长度（s1 和 s2 长度相同）

        for (int i = 0; i < len; ++i) { // 逐位对比两个字符串的字符
            if (s1[i] != s2[i]) { // 发现当前位置字符不相同
                diffCount++; // 不同字符计数自增 1
                if (diffCount > 2) { // 贪心剪枝：不同位数超过 2 个，绝对无法通过一次交换变得相同
                    return false; // 直接判定为不相似，提前返回 false
                }
            }
        }
        // 由于互为字母异位词，异位字符数量只可能是 0（完全相同）或 2（交换一对字符后相同）
        return diffCount == 0 || diffCount == 2;
    }

    /**
     * 深度优先搜索 (DFS)，递归遍历与当前字符串相连通的所有相似字符串
     * @param u 当前访问的字符串索引
     * @param strs 所有字符串构成的向量引用
     * @param visited 访问标记数组引用
     */
    void dfs(int u, const vector<string>& strs, vector<bool>& visited) {
        visited[u] = true; // 将当前节点 u 标记为已访问，防止重复搜索导致死循环
        int n = strs.size(); // 获取字符串列表的总数量 n

        for (int v = 0; v < n; ++v) { // 尝试与图中所有其他节点 v 进行连通性检查
            if (!visited[v] && isSimilar(strs[u], strs[v])) { // 若节点 v 未被访问且与当前节点 u 相似
                dfs(v, strs, visited); // 沿相似关系递归深入访问节点 v
            }
        }
    }

    /**
     * 计算字符串列表中相似字符串组（连通分量）的总数量
     * @param strs 字符串列表
     * @return 相似字符串组的数量
     */
    int numSimilarGroups(vector<string>& strs) {
        int n = strs.size(); // 获取字符串列表的总长度 n
        vector<bool> visited(n, false); // 创建大小为 n 的布尔向量，记录每个字符串是否已被归类到某个组中
        int groupCount = 0; // 声明并初始化相似字符串组的计数器为 0

        for (int i = 0; i < n; ++i) { // 遍历列表中的每一个字符串节点
            if (!visited[i]) { // 如果当前字符串还没有归属于任何已有分组
                groupCount++; // 发现一个新的连通分量，分组总数加 1
                dfs(i, strs, visited); // 调用 DFS 将与当前字符串直接或间接相似的所有字符串全部标记为已访问
            }
        }

        return groupCount; // 返回计算得出的连通分量（相似字符串组）总数
    }
};

int main() {
    // 提升 IO 输入输出效率，加速大文本读取
    ios::sync_with_stdio(false); // 取消 C++ 标准流与 C 语言标准输入输出流同步
    cin.tie(nullptr);            // 解绑 cin 与 cout，避免每次输入前自动刷新输出缓冲区

    int n; // 声明变量 n，表示输入的字符串数量
    if (cin >> n) { // 从标准输入中读取字符串个数 n
        vector<string> strs(n); // 创建容量为 n 的字符串向量
        for (int i = 0; i < n; ++i) { // 循环 n 次读入每个字符串
            cin >> strs[i]; // 读取单行字符串并存入向量中
        }

        Solution solver; // 实例化解题类对象
        int res = solver.numSimilarGroups(strs); // 调用函数计算相似组数量
        cout << res << "\n"; // 输出最终结果并打印换行符
    }

    return 0; // 程序正常执行完毕，向操作系统返回状态码 0
}