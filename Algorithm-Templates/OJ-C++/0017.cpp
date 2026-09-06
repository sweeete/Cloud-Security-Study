#include <iostream> // 引入标准输入输出流库，用于 cin 和 cout 控制台读写操作

using namespace std; // 使用标准命名空间 std，避免后续频繁使用 std:: 前缀

// 定义单链表节点的结构体
struct ListNode
{
    int val;        // 节点中存放的数据域（整型数值）
    ListNode *next; // 指向下一个链表节点的指针域
    ListNode() : val(0), next(NULL) {} // 默认构造函数：数据域初始化为 0，next 指针初始化为空 (NULL)
    ListNode(int x) : val(x), next(NULL) {} // 单参构造函数：设置数据域为 x，next 指针初始化为空 (NULL)
    ListNode(int x, ListNode *next) : val(x), next(next) {} // 双参构造函数：设置数据域为 x，next 指针指向传入的节点
};

class Solution {
public:
    /**
     * 两两交换链表中的相邻节点
     * @param head 原链表头节点
     * @return 交换后的链表头节点
     */
    ListNode* swapPairs(ListNode* head) {
        // 使用虚拟头节点 (Dummy Node) 栈对象，避免对真实头节点改变时进行单独特判
        ListNode dummy(0);
        // 将虚拟头节点的 next 指向原链表的真实头节点 head
        dummy.next = head;
        // 定义前驱指针 prev 指向虚拟头节点，作为当前待交换节点对的前驱节点
        ListNode* prev = &dummy;

        // 只有当 prev 后面至少存在两个非空节点时，才需要执行两两交换操作
        while (prev->next != NULL && prev->next->next != NULL) {
            // 记录当前待交换的第一节点 node1
            ListNode* node1 = prev->next;
            // 记录当前待交换的第二节点 node2
            ListNode* node2 = prev->next->next;

            // 指针调整逻辑：
            // 变更前: prev -> node1 -> node2 -> node3
            // 变更后: prev -> node2 -> node1 -> node3
            node1->next = node2->next; // 步骤1: 将 node1 的 next 指向 node2 后面的节点（node3）
            node2->next = node1;       // 步骤2: 将 node2 的 next 指向 node1，完成 node1 与 node2 的反转
            prev->next = node2;        // 步骤3: 将 prev 的 next 指向 node2，重新连接前半部分链表

            // prev 指针后移：更新为交换后的 node1（它现在是这一对节点的末尾，也是下一对的前驱节点）
            prev = node1;
        }

        // 返回虚拟头节点的下一个节点，即交换完成后新的真实链表头节点
        return dummy.next;
    }
};

// 辅助打印函数，格式化输出单链表结构
void displayLink(ListNode *head)
{
    ListNode *p = head; // 定义遍历指针 p，初始指向链表头节点
    cout << "head-->"; // 输出链表头部起始标识符
    while (p != NULL) // 遍历链表直至末尾指针 NULL
    {
        cout << p->val << "-->"; // 输出当前节点的值并附带连接符号 "-->"
        p = p->next; // 移动指针 p 到下一个节点
    }
    cout << "tail\n"; // 输出链表尾部标识 "tail" 并换行
}

// 主程序入口函数
int main()
{
    // 优化 I/O 读写性能
    ios_base::sync_with_stdio(false); // 取消 C++ 标准流与 C 标准输入输出流的同步，提升运行速度
    cin.tie(NULL); // 解绑 cin 和 cout，避免每次输入时自动刷新输出缓冲区

    int len; // 声明变量 len，存储每组测试用例输入的链表节点总数量
    // 使用 while (cin >> len) 循环读取，支持 OJ 多组测试数据 (EOF 机制)
    while (cin >> len) // 持续读取链表节点长度，直到遇到文件结束符 EOF
    {
        ListNode *head = NULL; // 初始化原链表头指针为空指针
        ListNode *p1 = NULL, *p2 = NULL; // 定义辅助指针：p1 用于指向新建节点，p2 指向当前链表末端
        int n = 0, num; // n 记录当前已生成的节点数量，num 用于暂存读入的节点数值

        // 尾插法构建无头结点单链表
        while (n < len && cin >> num) // 当已构建节点数小于 len 且成功读入节点值时循环
        {
            p1 = new ListNode(num); // 动态申请内存，创建一个值为 num 的新节点
            n++; // 节点计数加 1
            if (n == 1) // 如果是输入的第一个节点
                head = p1; // 将其设为链表的起始头节点 head
            else // 如果不是第一个节点
                p2->next = p1; // 将上一个节点 p2 的 next 指针指向新创建的节点 p1
            p2 = p1; // 更新 p2 指针，让其始终指向当前链表的末尾节点
        }

        // 调用两两交换函数并输出结果
        head = Solution().swapPairs(head); // 创建 Solution 临时对象并调用 swapPairs 重新排列链表，更新头节点
        displayLink(head); // 调用 displayLink 函数打印重排后的链表结构
    }

    return 0; // 程序正常执行完毕，返回 0
}