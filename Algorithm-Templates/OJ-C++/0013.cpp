#include <iostream> // 引入标准输入输出流库，用于 cin 和 cout 输入输出操作
using namespace std; // 使用标准命名空间 std，避免使用 std:: 前缀

// 链表节点结构体定义
struct ListNode
{
    int val; // 节点中存放的数据域（整型数值）
    ListNode *next; // 指向下一个链表节点的指针域
    ListNode() : val(0), next(NULL) {} // 默认构造函数：数值初始化为 0，next 指针初始化为空
    ListNode(int x) : val(x), next(NULL) {} // 带参构造函数：设置数值为 x，next 指针初始化为空
    ListNode(int x, ListNode *next) : val(x), next(next) {} // 全参构造函数：设置数值为 x，next 指针设为传入的节点指针
};

// 解题算法封装类
class Solution {
private:
    // 辅助函数：将两个升序排列的单链表 l1 和 l2 合并为一个新的升序链表
    ListNode* merge(ListNode* l1, ListNode* l2) {
        ListNode dummy(0); // 在栈上创建虚拟头节点 dummy，初始值为 0，简化边界节点的拼接逻辑
        ListNode* tail = &dummy; // 定义尾指针 tail 指向虚拟头节点，用于在尾部链接新节点

        while (l1 != NULL && l2 != NULL) { // 当 l1 和 l2 都不为空时，持续比较两个链表的当前节点
            if (l1->val <= l2->val) { // 如果 l1 当前节点的值小于或等于 l2 当前节点的值
                tail->next = l1; // 将 tail 的 next 指向 l1 当前节点
                l1 = l1->next; // l1 指针向后移动一位
            } else { // 如果 l2 当前节点的值更小
                tail->next = l2; // 将 tail 的 next 指向 l2 当前节点
                l2 = l2->next; // l2 指针向后移动一位
            }
            tail = tail->next; // 移动尾指针 tail，指向刚刚接上的节点
        }

        // 接上剩余未比较完的节点
        if (l1 != NULL) tail->next = l1; // 若 l1 仍有剩余节点，直接将剩余部分挂在 tail 后面
        if (l2 != NULL) tail->next = l2; // 若 l2 仍有剩余节点，直接将剩余部分挂在 tail 后面

        return dummy.next; // 返回合并后链表的真正头节点（即虚拟头节点的下一个节点）
    }

public:
    // 归并排序主函数：对以 head 为头节点的链表进行升序排序
    ListNode* sortList(ListNode* head) {
        // 递归终止条件：链表为空或只有一个节点，天然有序
        if (head == NULL || head->next == NULL) {
            return head; // 无需排序，直接返回原头节点
        }

        // 1. 使用快慢指针找到链表的中点
        ListNode* slow = head; // 定义慢指针 slow 初始指向头节点（每次向前走一步）
        ListNode* fast = head->next; // 让 fast 先走一步，保证节点总数为偶数时 slow 停在前半段末尾

        while (fast != NULL && fast->next != NULL) { // 当快指针及快指针的下一节点均不为空时继续循环
            slow = slow->next; // 慢指针向前移动一步
            fast = fast->next->next; // 快指针向前移动两步
        }

        // 2. 从中点断开链表，分为两半
        ListNode* mid = slow->next; // 定义后半段链表的头节点 mid 为 slow 的下一个节点
        slow->next = NULL; // 切断前半段与后半段的连接，将前半段尾节点的 next 置为空

        // 3. 递归排序左右两半
        ListNode* left = sortList(head); // 递归对前半段链表（以 head 为头）进行归并排序
        ListNode* right = sortList(mid); // 递归对后半段链表（以 mid 为头）进行归并排序

        // 4. 合并两个已排序的半边链表
        return merge(left, right); // 调用 merge 函数合并两个有序子链表，并返回排序后的新头节点
    }
};

// 辅助打印函数：格式化输出单链表结构
void displayLink(ListNode *head)
{
    ListNode *p = head; // 定义遍历指针 p，初始指向链表头节点
    cout << "head-->"; // 输出链表头部标识字符串
    while (p != NULL) // 当指针 p 不为空时遍历链表
    {
        cout << p->val << "-->"; // 输出当前节点的值及箭头指示符 "-->"
        p = p->next; // 指针 p 向后移动到下一个节点
    }
    cout << "tail\n"; // 输出链表末尾标识 "tail" 并换行
}

// 程序主函数入口
int main()
{
    // 优化 I/O 性能：取消 C 和 C++ 输入输出流的同步
    ios_base::sync_with_stdio(false);
    // 解绑 cin 和 cout，避免每次 cin 时自动刷新 cout 缓冲区
    cin.tie(NULL);

    int len; // 声明变量 len，用于存储每组测试用例的链表节点数量
    // 循环读取支持多组测试数据 (EOF 机制)：持续读取 len 直到遇到 EOF（文件结束符）
    while (cin >> len)
    {
        ListNode *head = NULL; // 初始化链表头指针为空
        ListNode *p1 = NULL, *p2 = NULL; // 定义辅助指针 p1（指向新节点）和 p2（指向上一节点）
        int n = 0, num; // 初始化已插入节点计数器 n 为 0，声明临时变量 num 存储输入的节点数值

        // 尾插法构建单链表
        while (n < len && cin >> num) // 当未达到指定节点数且成功读取数值时循环
        {
            p1 = new ListNode(num); // 动态创建存放 num 的新节点
            n++; // 插入节点计数加 1
            if (n == 1) // 如果是构建的第一个节点
                head = p1; // 将其设为整个链表的头节点 head
            else // 不是第一个节点
                p2->next = p1; // 将上一个节点 p2 的 next 指向新节点 p1
            p2 = p1; // 更新 p2 指针，使之保持指向当前链表的末尾节点
        }

        // 排序并打印
        head = Solution().sortList(head); // 实例化 Solution 对象并调用 sortList 函数排序，更新头节点
        displayLink(head); // 调用辅助打印函数输出排序后的链表结构
    }
    return 0; // 程序正常执行完毕返回 0
}