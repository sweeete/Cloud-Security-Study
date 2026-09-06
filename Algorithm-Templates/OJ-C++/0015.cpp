#include <iostream> // 引入标准输入输出流头文件，用于 cin 和 cout 输入输出操作
#include <vector>   // 引入动态数组 vector 容器头文件，用于存储分隔后的多段链表头节点

using namespace std; // 使用标准命名空间 std，避免后续使用 iostream 和 vector 时频繁书写 std::

// 单链表节点结构体定义
struct ListNode
{
    int val;        // 节点中存放的数据域（整型数值）
    ListNode *next; // 指向链表中下一个节点的指针域
    ListNode() : val(0), next(NULL) {} // 默认无参构造函数：将数据域初始化为 0，next 指针初始化为空 (NULL)
    ListNode(int x) : val(x), next(NULL) {} // 单参构造函数：设置数据域为 x，next 指针初始化为空 (NULL)
    ListNode(int x, ListNode *next) : val(x), next(next) {} // 双参构造函数：设置数据域为 x，next 指针指向传入的节点
};

class Solution
{
public:
    /**
     * 将链表分隔为 k 个连续的部分
     * @param root 原链表头节点
     * @param k 分隔的部分数量
     * @return 包含 k 个部分头节点指针的 vector
     */
    vector<ListNode*> splitListToParts(ListNode* root, int k)
    {
        // 1. 遍历计算链表节点总数 N
        int N = 0; // 初始化链表长度计数器 N 为 0
        ListNode* curr = root; // 定义辅助指针 curr，初始指向链表头节点 root
        while (curr != NULL) { // 循环遍历整个单链表，直到指针移动到末尾 NULL
            N++; // 当前节点有效，节点总数计数加 1
            curr = curr->next; // 将指针 curr 移动到链表中的下一个节点
        }

        // 2. 计算每部分的平均长度 width 以及余数 rem
        // 前 rem 个部分的长度为 width + 1，其余部分的长度为 width
        int width = N / k; // 计算每个部分的基础节点数量（整除向下取整）
        int rem = N % k;   // 计算余数，即前 rem 个部分需要多分配 1 个节点

        vector<ListNode*> res(k, NULL); // 初始化大小为 k 的 vector 数组，所有元素预置为 NULL，用于保存 k 个部分的头节点
        curr = root; // 重置指针 curr，使其重新指向原链表的头节点 root，准备进行拆分操作

        // 3. 依次构建 k 个子链表
        for (int i = 0; i < k; ++i) { // 循环 k 次，依次切割并处理第 i 个子链表（索引从 0 到 k-1）
            // 如果已经没有节点可用，直接赋予 NULL
            if (curr == NULL) { // 检查当前指针是否为空（说明原链表节点已分配完毕）
                res[i] = NULL; // 若无剩余节点，第 i 个子链表的头节点设为 NULL
                continue;      // 跳过本次循环后续操作，继续处理下一个部分
            }

            // 记录当前子链表的头节点
            res[i] = curr; // 将当前节点指针赋给 res[i]，作为第 i 个子链表的起始头节点
            // 计算当前子链表应该分配的节点数
            int current_part_size = width + (i < rem ? 1 : 0); // 若当前索引 i < rem，则分配 width + 1 个节点，否则分配 width 个节点

            // 指针移动到当前部分的最后一个节点
            for (int j = 0; j < current_part_size - 1; ++j) { // 循环 current_part_size - 1 次，将指针推进到当前部分的尾节点
                if (curr != NULL) { // 安全检查，确保当前指针非空
                    curr = curr->next; // 将指针 curr 向后移动一步
                }
            }

            // 断开当前部分与后续链表的连接
            if (curr != NULL) { // 如果找到了当前部分的尾节点
                ListNode* next_part_head = curr->next; // 暂存下一个部分的起始头节点地址
                curr->next = NULL;     // 将当前部分尾节点的 next 指针置为空，实现切割断开（关键点）
                curr = next_part_head; // 将指针 curr 更新指向下一个部分的起始节点，为下一次循环做准备
            }
        }

        return res; // 返回包含 k 个分隔链表头节点的 vector 容器
    }
};

// 辅助打印函数，输出 vector<ListNode*> 中每个链表的信息
void display(vector<ListNode *> lnVec)
{
    for (size_t i = 0; i < lnVec.size(); i++) // 遍历存储各个子链表头节点的 vector 容器
    {
        ListNode *p = lnVec[i]; // 定义指针 p 指向当前子链表的头节点
        cout << "head-->"; // 输出链表头部起始标记字符串
        while (p != NULL) // 遍历当前子链表，直到遇到末尾 NULL
        {
            cout << p->val << "-->"; // 输出当前节点的值，并附带箭头连接符
            p = p->next; // 指针 p 移动到当前子链表的下一个节点
        }
        cout << "tail\n"; // 输出当前子链表末尾标记 "tail" 并换行
    }
}

int main()
{
    // 优化 I/O 性能
    ios_base::sync_with_stdio(false); // 取消 C 与 C++ 标准流的同步，提高 cin/cout 运行速度
    cin.tie(NULL); // 解绑 cin 与 cout 的绑定，避免每次 cin 前自动刷新缓冲区

    int len; // 声明变量 len，用于接收输入的链表节点总数
    // 使用 while (cin >> len) 循环读取，支持 OJ 多组测试数据 (EOF 机制)
    while (cin >> len) // 持续读取链表长度，直到遇到 EOF（文件结束符）
    {
        ListNode *head = NULL; // 初始化原链表头指针为 NULL
        ListNode *p1 = NULL, *p2 = NULL; // 定义辅助指针：p1 指向新创建节点，p2 指向当前链表末尾节点
        int n = 0, num; // n 记录当前已插入节点个数，num 暂存从标准输入读入的节点值

        // 尾插法构建无头结点单链表
        while (n < len && cin >> num) // 当已构建节点数小于指定长度 len 且成功读入数值时循环
        {
            p1 = new ListNode(num); // 动态申请内存，创建存储数值 num 的新节点
            n++; // 插入节点计数加 1
            if (n == 1) // 如果是创建的第一个节点
                head = p1; // 将其设为整条链表的头节点 head
            else // 如果不是第一个节点
                p2->next = p1; // 将上一节点 p2 的 next 指针指向新创建的节点 p1
            p2 = p1; // 更新 p2 指向当前最末尾节点 p1，为下一次插入做准备
        }

        int k; // 声明变量 k，用于接收分隔的部分数量
        if (cin >> k) // 成功读取分隔参数 k
        {
            // 调用核心分隔函数
            vector<ListNode*> lnVec = Solution().splitListToParts(head, k); // 实例化 Solution 对象并调用 splitListToParts 函数进行链表拆分
            // 输出结果
            display(lnVec); // 调用 display 函数打印拆分后的所有子链表结构
        }
    }

    return 0; // 程序正常执行完毕，返回 0
}