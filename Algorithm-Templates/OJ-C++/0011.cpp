#include <iostream> // 引入输入输出流库，用于 cin 和 cout 控制台交互
#include <vector>   // 引入动态数组容器库，用于按顺序存储链表节点指针

using namespace std; // 使用标准命名空间 std，避免使用 std:: 前缀

// 定义单链表的节点结构体
struct ListNode
{
    int val; // 节点存储的整型数值
    ListNode *next; // 指向下一个链表节点的指针
    ListNode() : val(0), next(NULL) {} // 默认构造函数：数值初始化为 0，next 指针初始化为空
    ListNode(int x) : val(x), next(NULL) {} // 带参构造函数：指定数值 x，next 指针初始化为空
    ListNode(int x, ListNode *next) : val(x), next(next) {} // 全参构造函数：指定数值 x 和下一个节点指针 next
};

// 解题逻辑封装类
class Solution
{
public:
    // 重排链表函数：将 L0->L1->...->Ln-1->Ln 重排为 L0->Ln->L1->Ln-1->L2->Ln-2...
    void reorderList(ListNode* head)
    {
        // 边界条件判断：若链表为空或仅有一个节点，无需进行任何重排操作，直接返回
        if (head == NULL || head->next == NULL) {
            return; // 结束函数执行
        }

        // 1. 将链表所有节点的指针顺序存入数组/向量中，以便通过下标直接随机访问节点
        vector<ListNode*> vec; // 声明一个存储 ListNode 指针的动态数组 vec
        ListNode* curr = head; // 定义遍历指针 curr，初始指向链表头节点 head
        while (curr != NULL) { // 遍历整个链表，直到 curr 走到链表末尾 NULL
            vec.push_back(curr); // 将当前节点的指针存入数组 vec 的末尾
            curr = curr->next; // 将遍历指针移动到下一个节点
        }

        // 2. 使用双指针（一头一尾）进行重新连接
        int i = 0; // 头指针 i，指向数组开头（第 0 个节点，即 L0）
        int j = vec.size() - 1; // 尾指针 j，指向数组结尾（最后一个节点，即 Ln）

        while (i < j) { // 当头指针 i 小于尾指针 j 时，交替重新连接节点
            vec[i]->next = vec[j]; // 将头侧节点 vec[i] 的 next 指向尾侧节点 vec[j] (例：L0 -> Ln)
            i++; // 头指针向右移动一位，指向下一个待处理的头侧节点
            if (i == j) break;     // 特殊检查：若 i 与 j 重合（节点总数为偶数时），说明节点已全部连接完，提前退出循环

            vec[j]->next = vec[i]; // 将尾侧节点 vec[j] 的 next 指向新头侧节点 vec[i] (例：Ln -> L1)
            j--; // 尾指针向左移动一位，指向下一个待处理的尾侧节点
        }

        // 3. 最后一个节点的 next 必须置为空，防止链表产生环
        vec[i]->next = NULL; // 断开重排后最后一个节点的 next 连接，避免形成环形链表
    }
};

// 辅助函数：格式化打印链表结构
void displayLink(ListNode *head)
{
    ListNode *p = head; // 定义遍历指针 p，初始指向链表头节点
    cout << "head-->"; // 输出链表头部标识字符串
    while (p != NULL) // 当指针 p 不为空时遍历链表
    {
        cout << p->val << "-->"; // 输出当前节点的值及连接符 "-->"
        p = p->next; // 移动指针 p 到下一个节点
    }
    cout << "tail\n"; // 输出链表尾部标识 "tail" 并换行
}

// 程序执行主入口函数
int main()
{
    // 优化 I/O 性能：解绑 C 与 C++ 流同步，提高 cin/cout 运行速度
    ios_base::sync_with_stdio(false); // 关闭 C++ 与 C 标准输入输出流的同步
    cin.tie(NULL); // 解绑 cin 与 cout 的绑定，避免每次 cin 前自动刷新 cout 缓冲区

    int len; // 声明变量 len，用于存储即将输入的链表节点个数
    // 循环读取节点长度 len，支持多组测试数据连续读取直至文件结束 (EOF)
    while (cin >> len)
    {
        ListNode *head = NULL; // 初始化链表头指针为空
        ListNode *p1 = NULL, *p2 = NULL; // 定义临时指针 p1（当前新建节点）和 p2（记录上一个节点）
        int n = 0, num; // 初始化已读取节点计数器 n 为 0，声明临时变量 num 用于存储节点数值

        // 尾插法构建无头结点单链表
        while (n < len && cin >> num) // 当未达到指定长度且成功读取数据时循环
        {
            p1 = new ListNode(num); // 动态申请内存，创建一个值为 num 的新节点
            n++; // 成功创建节点，计数器 n 加 1
            if (n == 1) // 如果是输入的第一个节点
                head = p1; // 将其设为链表头节点 head
            else // 如果不是第一个节点
                p2->next = p1; // 将上一个节点 p2 的 next 指向当前新节点 p1
            p2 = p1; // 更新 p2，让其指向当前最新插入的节点，为下一次尾插做准备
        }

        // 重排并打印
        Solution().reorderList(head); // 创建 Solution 临时对象并调用 reorderList 函数重排链表
        displayLink(head); // 调用辅助函数，打印重排后的链表
    }
    return 0; // 程序正常终止并返回 0
}