#include <iostream> // 引入标准输入输出流库，用于控制台输入输出 (cin, cout)

using namespace std; // 使用标准命名空间 std，避免后续频繁书写 std:: 前缀

// 单链表节点结构体定义
struct ListNode
{
    int val;        // 节点的数据域（存储整型数值）
    ListNode *next; // 节点的指针域（指向下一个链表节点）
    ListNode() : val(0), next(NULL) {} // 默认构造函数：数据域赋值为 0，next 指针置为空 (NULL)
    ListNode(int x) : val(x), next(NULL) {} // 单参构造函数：设置数值为 x，next 指针置为空 (NULL)
    ListNode(int x, ListNode *next) : val(x), next(next) {} // 双参构造函数：设置数值为 x，并指定 next 指向传入的节点
};

class Solution {
public:
    /**
     * K 个一组翻转链表
     * @param head 原链表头节点
     * @param k 每组的节点个数
     * @return 翻转后的链表头节点
     */
    ListNode* reverseKGroup(ListNode* head, int k) {
        // 特判：如果链表为空、只有一个节点或者 k=1，无需进行任何翻转，直接返回原头节点
        if (head == NULL || head->next == NULL || k == 1) {
            return head; // 直接返回原链表头节点
        }

        // 使用虚拟头节点 (Dummy Node) 栈对象，统一处理头节点发生变更的情况，避免单独特判
        ListNode dummy(0);
        // 将虚拟头节点的 next 指向原链表头节点 head
        dummy.next = head;
        // 定义 prev 指针，始终指向当前待翻转组的前驱节点（初始为虚拟头节点）
        ListNode* prev = &dummy;

        // 无限循环处理各组节点的翻转，直到剩余节点不足 k 个时退出
        while (true) {
            // 1. 检查从 prev 开始后面是否还有至少 k 个节点
            ListNode* check = prev; // 定义探路指针 check，初始指向当前组的前驱节点
            for (int i = 0; i < k && check != NULL; ++i) { // 尝试向后步进 k 次
                check = check->next; // 探路指针向后移动一步
            }
            // 如果检查过程中发现后续节点不足 k 个（check 为空），保持剩余节点原有顺序，直接结束翻转
            if (check == NULL) {
                break; // 退出外层主循环
            }

            // 2. 当前组确认有 k 个节点，采用“头插法”在原链表上完成组内翻转（空间复杂度 O(1)）
            // curr 始终指向当前组翻转前的首节点（随着头插过程不断向后推，最终变成翻转后的尾节点）
            ListNode* curr = prev->next;
            for (int i = 0; i < k - 1; ++i) { // k 个节点只需要执行 k - 1 次局部头插操作
                ListNode* nxt = curr->next; // 记录当前待拔出并头插到前面的节点 nxt
                curr->next = nxt->next;     // 步骤1: 将 curr 的 next 跳过 nxt，指向 nxt 的下一个节点
                nxt->next = prev->next;     // 步骤2: 将 nxt 的 next 指向当前组的最前端节点 (prev->next)
                prev->next = nxt;           // 步骤3: 将 prev 的 next 指向 nxt，完成将 nxt 插入到组内最前头的操作
            }

            // 3. 组内翻转完成后，curr 移动到了该组的末尾，将其赋值给 prev，作为下一组的前驱节点
            prev = curr;
        }

        // 返回虚拟头节点的下一个节点，即翻转完成后整条新链表的真实头节点
        return dummy.next;
    }
};

// 辅助打印函数：格式化输出单链表结构
void displayLink(ListNode *head)
{
    ListNode *p = head; // 定义遍历指针 p，初始指向链表头节点
    cout << "head-->"; // 打印头部起始标识符
    while (p != NULL)  // 遍历链表直到节点指针为空
    {
        cout << p->val << "-->"; // 输出当前节点的数据域及连接符
        p = p->next; // 指针 p 移动至下一个节点
    }
    cout << "tail\n"; // 打印尾部标识符并换行
}

// 主程序入口函数
int main()
{
    // 优化 I/O 标准输入输出流性能
    ios_base::sync_with_stdio(false); // 取消 C++ 输入输出流与 C 语言标准流的同步，大幅提升读写效率
    cin.tie(NULL); // 解绑 cin 和 cout，防止每次 cin 输入前自动刷新输出缓冲区

    int len; // 声明变量 len，用于存储每组测试用例中的链表节点总数
    // 使用 while (cin >> len) 循环读取，支持系统的多组测试数据连续输入 (EOF 机制)
    while (cin >> len)
    {
        ListNode *head = NULL; // 初始化链表头指针为空
        ListNode *p1 = NULL, *p2 = NULL; // 定义辅助指针：p1 用于新建节点，p2 始终指向当前链表末端
        int n = 0, num; // n 记录当前已创建节点数，num 用于暂存从控制台读入的数值

        // 尾插法构建无头结点单链表
        while (n < len && cin >> num) // 当构建节点数未达到 len 且读入成功时循环
        {
            p1 = new ListNode(num); // 动态申请内存，创建一个存储值为 num 的新节点
            n++; // 节点计数自增 1
            if (n == 1) // 如果是建立的第一个节点
                head = p1; // 将其设为链表的头节点 head
            else // 不是第一个节点
                p2->next = p1; // 将当前末尾节点 p2 的 next 指向新节点 p1
            p2 = p1; // 更新 p2，使其重新指向链表的最末尾节点
        }

        int k; // 声明变量 k，用于存储组内翻转的目标节点个数
        if (cin >> k) // 读取目标值 k
        {
            // 调用解题函数处理链表并更新头节点，随后输出结果
            head = Solution().reverseKGroup(head, k); // 实例化 Solution 对象，调用 reverseKGroup 进行翻转
            displayLink(head); // 调用 displayLink 输出翻转后的链表结构
        }
    }

    return 0; // 程序正常结束，返回状态码 0
}