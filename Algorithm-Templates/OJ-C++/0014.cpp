#include <iostream> // 引入标准输入输出流库，用于 cin 和 cout 控制台读写
#include <vector> // 引入动态数组容器库，用于存储数组 G 的数据
#include <unordered_set> // 引入无序哈希集合库，用于以 O(1) 复杂度查找元素

using namespace std; // 使用标准命名空间 std，避免后续频繁使用 std:: 前缀

// 定义单链表节点的结构体
struct ListNode
{
    int val; // 节点中存放的数据域（整型数值）
    ListNode *next; // 指向下一个链表节点的指针域
    ListNode() : val(0), next(NULL) {} // 默认构造函数：数值初始化为 0，next 指针初始化为空 (NULL)
    ListNode(int x) : val(x), next(NULL) {} // 带参构造函数：设置节点数值为 x，next 指针初始化为空 (NULL)
    ListNode(int x, ListNode *next) : val(x), next(next) {} // 全参构造函数：设置节点数值为 x，下一个节点指针设为传入的 next
};

// 解决方案封装类
class Solution {
public:
    // 求解链表组件（连续子段）数量的核心函数
    int numComponents(ListNode* head, vector<int>& G) {
        // 使用向量 G 的迭代器区间初始化无序哈希集合 g_set，将查找元素的时间复杂度降为 O(1)
        unordered_set<int> g_set(G.begin(), G.end());
        int count = 0; // 初始化组件（连续片段）计数器为 0
        ListNode* curr = head; // 定义指针 curr 初始指向链表头节点，用于遍历链表

        // 循环遍历整个单链表，直到指针移动到末尾 NULL
        while (curr != NULL) {
            // 判断当前节点是否为一个组件（连续片段）的末端节点：
            // 条件 1: g_set.count(curr->val) -> 当前节点的值属于数组 G
            // 条件 2: curr->next == NULL || !g_set.count(curr->next->val) -> 当前节点已是链表尾节点，或者下一个节点的值不在数组 G 中
            if (g_set.count(curr->val) && (curr->next == NULL || !g_set.count(curr->next->val))) {
                count++; // 找到一个有效组件的结尾，计数器加 1
            }
            curr = curr->next; // 将指针 curr 移动到链表的下一个节点
        }

        return count; // 返回最终计算出的连通组件总数
    }
};

// 主函数入口
int main()
{
    // 优化 C++ 标准输入输出流的速度，取消 C 与 C++ 流的同步
    ios_base::sync_with_stdio(false);
    // 解绑 cin 和 cout，避免每次输入前都自动刷新输出缓冲区，提升读写性能
    cin.tie(NULL);

    int len; // 声明变量 len，用于存储当前测试用例中链表的节点数量
    // 循环读取链表长度，支持多组测试用例处理（直到遇到文件结束符 EOF）
    while (cin >> len)
    {
        ListNode *head = NULL; // 初始化链表头指针为空 NULL
        ListNode *p1 = NULL, *p2 = NULL; // 定义辅助指针：p1 指向新建节点，p2 指向上一节点
        int n = 0, num; // n 记录当前已构建的节点数，num 用于暂存从控制台读取的节点数值

        // 尾插法构建无头结点的单链表
        while (n < len && cin >> num)
        {
            p1 = new ListNode(num); // 动态创建一个存放数值 num 的新节点
            n++; // 已构建节点数量自增 1
            if (n == 1) // 如果是输入的第一个节点
                head = p1; // 将其设为链表头节点 head
            else // 如果不是第一个节点
                p2->next = p1; // 将上一个节点 p2 的 next 指向新节点 p1
            p2 = p1; // 更新 p2 指向当前最末尾的节点 p1，为下一次尾插做准备
        }

        // 读取数组 G 的元素个数及元素值
        int m; // 声明变量 m，存储数组 G 的元素个数
        if (!(cin >> m)) break; // 如果无法成功读取 m（如已到达文件末尾），则跳出外层循环
        vector<int> G; // 声明整型动态数组 G，用于存储子集元素
        for (int i = 0; i < m; i++) // 循环 m 次依次读取数组 G 的每个元素
        {
            int data; // 声明变量 data 暂存当前读取到的数值
            cin >> data; // 从标准输入中读取一个整数
            G.push_back(data); // 将读取到的数值添加到向量 G 的末尾
        }

        // 创建 Solution 临时对象并调用 numComponents 计算组件数量，将结果存入 res
        int res = Solution().numComponents(head, G);
        cout << res << "\n"; // 输出计算结果并换行
    }

    return 0; // 程序正常执行完毕，返回 0
}