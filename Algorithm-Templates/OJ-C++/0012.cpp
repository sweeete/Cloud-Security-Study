#include <iostream> // 引入标准输入输出流库，用于 cin 和 cout 输入输出操作
using namespace std; // 使用标准命名空间 std，避免使用 std:: 前缀

// 定义单链表节点的结构体
struct ListNode
{
    int val; // 节点中存放的数据域（整型数值）
    ListNode *next; // 指向下一个链表节点的指针域
    ListNode() : val(0), next(NULL) {} // 默认构造函数：将数值初始化为 0，next 指针初始化为空
    ListNode(int x) : val(x), next(NULL) {} // 带参构造函数：设置数值为 x，next 指针初始化为空
    ListNode(int x, ListNode *next) : val(x), next(next) {} // 全参构造函数：设置数值为 x，next 指针设置为传入的节点指针
};

// 解题逻辑类
class Solution
{
public:
    // 旋转链表函数：将链表向右旋转移动 k 个位置
    ListNode *rotateRight(ListNode *head, int k)
    {
        // 边界情况判断：若链表为空、链表只有 1 个节点或者旋转步数 k 为 0，无需旋转直接返回原头节点
        if (!head || !head->next || k == 0)
        {
            return head; // 直接返回原链表的头节点
        }

        // 1. 初始化链表长度计数器为 1（因为 head 本身算第 1 个节点）
        int len = 1;
        // 定义指针 old_tail 指向链表头节点，用于遍历并找到原链表的尾节点
        ListNode *old_tail = head;
        // 遍历链表直到指针移动到最后一个节点（即 next 指向 NULL 时停止）
        while (old_tail->next != NULL)
        {
            old_tail = old_tail->next; // 指针向后移动一个节点
            len++; // 链表长度自增 1
        }

        // 2. 取模运算：当 k 大于链表长度 len 时，实际有效旋转步数是 k % len
        k = k % len;
        // 若取模后的实际有效旋转步数为 0（即 k 是 len 的整数倍）
        if (k == 0)
        {
            return head; // 相当于旋转完整一圈回到原地，直接返回原链表
        }

        // 3. 将原链表尾节点的 next 指针指向头节点 head，形成一个闭环单链表
        old_tail->next = head;

        // 4. 查找旋转后新链表的尾节点：位于从头节点出发的第 len - k - 1 个节点位置
        ListNode *new_tail = head; // 定义指针从头节点开始查找
        // 循环移动 len - k - 1 步找到新的尾节点
        for (int i = 0; i < len - k - 1; ++i)
        {
            new_tail = new_tail->next; // 指针向后移动一步
        }

        // 5. 新尾节点的下一个节点即为旋转后新链表的头节点
        ListNode *new_head = new_tail->next;
        // 将新尾节点的 next 指针置为空，断开环形链表恢复为单链表
        new_tail->next = NULL;

        // 返回旋转完成后新的链表头节点
        return new_head;
    }
};

// 辅助打印函数：格式化输出单链表结构
void displayLink(ListNode *head)
{
    ListNode *p = head; // 定义遍历指针 p，初始指向链表头节点
    cout << "head-->"; // 输出链表头部标识字符串
    while (p != NULL) // 当指针 p 不为空时遍历整个链表
    {
        cout << p->val << "-->"; // 输出当前节点的值及连接符 "-->"
        p = p->next; // 指针移动到下一个节点
    }
    cout << "tail\n"; // 输出链表尾部标识 "tail" 并换行
}

// 程序主函数入口
int main()
{
    // 优化 I/O 读写性能：取消 C 和 C++ 输入输出流的同步
    ios_base::sync_with_stdio(false);
    // 解绑 cin 和 cout，避免每次 cin 时强制刷新 cout 缓冲区
    cin.tie(NULL);

    int len; // 声明变量 len，用于存储即将输入的链表节点数量
    // 使用 while (cin >> len) 循环读取输入，支持多组测试用例处理（直到 EOF 文件结束）
    while (cin >> len)
    {
        ListNode *head = NULL; // 初始化链表头指针为空
        ListNode *p1 = NULL, *p2 = NULL; // 定义辅助指针 p1（指向新建节点）和 p2（指向上一节点）
        int n = 0, num; // n 记录当前已插入的节点个数，num 存储输入的节点数值

        // 尾插法构建无头结点的单链表
        while (n < len && cin >> num) // 当未达到指定节点数且成功读取到数值时循环
        {
            p1 = new ListNode(num); // 动态创建一个存放 num 的新节点
            n++; // 插入节点计数加 1
            if (n == 1) // 如果是输入的第一个节点
                head = p1; // 将其设为链表的头节点 head
            else // 不是第一个节点
                p2->next = p1; // 将上一个节点 p2 的 next 指向当前新节点 p1
            p2 = p1; // 更新 p2 指针，使其始终指向当前链表的最末尾节点
        }

        int k; // 声明变量 k，用于存储向右旋转的位数
        if (cin >> k) // 成功读取到旋转位数 k
        {
            head = Solution().rotateRight(head, k); // 创建 Solution 对象实例并调用 rotateRight 方法更新链表
            displayLink(head); // 调用辅助函数，打印旋转后的链表结构
        }
    }
    return 0; // 程序正常执行终止返回 0
}