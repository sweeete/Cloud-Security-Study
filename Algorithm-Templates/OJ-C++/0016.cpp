#include <iostream> // 引入标准输入输出流头文件，用于 cin 和 cout 输入输出操作

using namespace std; // 使用标准命名空间 std，避免后续频繁使用 std:: 前缀

// 单链表节点结构体定义
struct ListNode
{
    int val;        // 节点中存放的数据域（整型数值）
    ListNode *next; // 指向下一个链表节点的指针域
    ListNode() : val(0), next(NULL) {} // 默认无参构造函数：将数值初始化为 0，next 指针初始化为空 (NULL)
    ListNode(int x) : val(x), next(NULL) {} // 单参构造函数：设置数值为 x，next 指针初始化为空 (NULL)
    ListNode(int x, ListNode *next) : val(x), next(next) {} // 双参构造函数：设置数值为 x，next 指针指向传入的节点
};

class Solution {
public:
    /**
     * 将链表按节点序号的奇偶性拆分并重新拼接
     * @param head 原链表头节点（无头结点单链表）
     * @return 重新排列后的链表头节点
     */
    ListNode* oddEvenList(ListNode* head) {
        // 特判：如果链表为空，或者只有一个节点、两个节点，直接返回
        if (head == NULL || head->next == NULL) { // 检查链表是否为空指针或仅包含一个节点
            return head; // 无需进行奇偶拆分，直接返回原头节点
        }

        // odd 指向当前奇链表的尾节点（初始指向第 1 个节点）
        ListNode* odd = head; // 初始化奇数指针 odd 指向第一个节点（奇数节点）
        // even 指向当前偶链表的尾节点（初始指向第 2 个节点）
        ListNode* even = head->next; // 初始化偶数指针 even 指向第二个节点（偶数节点）
        // 保存偶链表的头节点，方便最后与奇链表末尾相连
        ListNode* evenHead = even; // 记录偶数链表的起始头节点地址

        // 当后方至少还有一个偶数节点时继续循环
        while (even != NULL && even->next != NULL) { // 只要偶节点及其下一个节点都不为空就继续穿插
            // 1. 将奇节点的 next 指向下一个奇节点（即偶节点的下一个节点）
            odd->next = even->next; // 跳过当前偶节点，把奇节点的 next 指向下一个奇节点
            // 奇指针后移一步
            odd = odd->next; // 将奇数指针 odd 更新为刚刚接上的下一个奇节点

            // 2. 将偶节点的 next 指向下一个偶节点（即新奇节点的下一个节点）
            even->next = odd->next; // 跳过刚刚处理过的奇节点，把偶节点的 next 指向下一个偶节点
            // 偶指针后移一步
            even = even->next; // 将偶数指针 even 更新为刚刚接上的下一个偶节点
        }

        // 3. 将奇数链表的末尾连接到偶数链表的头部
        odd->next = evenHead; // 将奇数链表最后一个节点的 next 指针指向偶数链表的第一个节点

        return head; // 返回奇链表头部（即原链表的 head）
    }
};

// 格式化输出链表结构的辅助函数
void displayLink(ListNode *head)
{
    ListNode *p = head; // 定义遍历指针 p，初始指向链表头节点
    cout << "head-->"; // 输出链表头部起始标记
    while (p != NULL) // 当指针 p 未到达链表末尾 NULL 时循环
    {
        cout << p->val << "-->"; // 输出当前节点的值并附带箭头表示连接关系
        p = p->next; // 指针 p 向后移动一步指向下一个节点
    }
    cout << "tail\n"; // 输出链表末尾标记 "tail" 并换行
}

int main()
{
    // 优化 I/O 标准输入输出流读写性能
    ios_base::sync_with_stdio(false); // 取消 C++ 输入输出流与 C 标准输入输出的同步，提升性能
    cin.tie(NULL); // 解绑 cin 与 cout 的关联，避免每次 cin 时刷新 cout 缓冲区

    int len; // 声明变量 len，用于存储即将构建的链表节点数量
    // 使用 while (cin >> len) 循环读取，支持 OJ 多组测试数据 (EOF 机制)
    while (cin >> len) // 持续从标准输入读取链表长度，直到遇到文件结束符 EOF
    {
        ListNode *head = NULL; // 初始化链表头指针为空指针
        ListNode *p1 = NULL, *p2 = NULL; // 定义辅助指针：p1 指向新建节点，p2 指向链表当前末尾节点
        int n = 0, num; // n 记录当前已创建的节点数，num 用于暂存输入的节点值

        // 尾插法构建无头结点单链表
        while (n < len && cin >> num) // 当未读取完指定数量节点且成功读入数值时循环
        {
            p1 = new ListNode(num); // 动态申请内存，创建一个存储数值 num 的新节点
            n++; // 已构建节点数加 1
            if (n == 1) // 如果是建立的第 1 个节点
                head = p1; // 将其设为链表的起始头节点 head
            else // 如果不是第 1 个节点
                p2->next = p1; // 将上一个节点 p2 的 next 指向新节点 p1
            p2 = p1; // 更新 p2，让其始终指向当前链表的末尾节点
        }

        // 调用解题函数并输出结果
        head = Solution().oddEvenList(head); // 创建 Solution 临时对象并调用 oddEvenList 方法重排链表
        displayLink(head); // 调用 displayLink 函数，打印重排后的链表结构
    }

    return 0; // 程序正常执行完成，返回状态码 0
}