#include <iostream> // 引入标准输入输出流库，用于 cin 和 cout 控制台输入输出
#include <vector>   // 引入动态数组 vector 容器头文件，用于存储节点数值及返回结果
#include <stack>    // 引入栈 stack 容器头文件，用于构建单调栈

using namespace std; // 使用标准命名空间 std，避免后续频繁书写 std:: 前缀

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
     * 寻找链表中每个节点的下一个更大节点
     * @param head 原链表头节点
     * @return 包含下一个更大数值的 vector
     */
    vector<int> nextLargerNodes(ListNode* head) {
        // 1. 将链表中的节点值复制到 vector 中，方便通过下标快速访问
        vector<int> nums; // 声明整型动态数组 nums，用于顺序接收链表节点的值
        ListNode* curr = head; // 定义辅助遍历指针 curr，初始指向链表头节点
        while (curr != NULL) { // 当指针非空时遍历整个链表
            nums.push_back(curr->val); // 将当前节点的值追加存入 nums 动态数组末尾
            curr = curr->next; // 将指针 curr 移动到链表中的下一个节点
        }

        int n = nums.size(); // 获取链表节点的总数量（即 nums 数组的长度）
        vector<int> res(n, 0); // 创建大小为 n 的结果数组 res，默认全部填充为 0
        stack<int> st;         // 声明单调栈 st，专门用于保存数组元素的下标，保持对应数值单调递减

        // 2. 使用单调栈遍历数组寻找“下一个更大元素”
        for (int i = 0; i < n; ++i) { // 遍历数组 nums 中的每一个元素（下标从 0 到 n-1）
            // 当栈不为空，且当前遍历到的数值 nums[i] 大于栈顶下标 st.top() 对应的数值时循环：
            // 说明找到了栈顶元素右侧出现的“第一个更大值”
            while (!st.empty() && nums[st.top()] < nums[i]) {
                int prev_idx = st.top(); // 获取并保存此时栈顶存入的元素下标
                st.pop();                // 将已找到下一个更大值的下标弹出栈
                res[prev_idx] = nums[i]; // 将找到了更大值的元素对应的结果位置填充为当前数值 nums[i]
            }
            // 将当前元素的下标 i 压入单调栈中，等待后续更大的元素来将其弹出并更新结果
            st.push(i);
        }

        return res; // 返回存储了所有节点“下一个更大数值”的结果数组
    }
};

int main()
{
    // 优化 I/O 性能
    ios_base::sync_with_stdio(false); // 取消 C++ 标准输入输出流与 C 语言流的同步，提升输入输出效率
    cin.tie(NULL); // 解绑 cin 和 cout，避免每次输入前自动刷新输出缓冲区

    int len; // 声明变量 len，用于存储每组测试数据中输入的链表节点数量
    // 循环读取，支持 OJ 多组测试数据 (EOF 机制)
    while (cin >> len) // 持续从标准输入读取链表长度，直至文件末尾 EOF
    {
        ListNode *head = NULL; // 初始化链表头指针为空指针 NULL
        ListNode *p1 = NULL, *p2 = NULL; // 定义辅助指针：p1 用于指向动态创建的新节点，p2 保持指向链表末尾
        int n = 0, num; // n 记录当前已创建的节点个数，num 用于暂存从标准输入读入的节点数值

        // 尾插法构建无头结点单链表
        while (n < len && cin >> num) // 当已构建节点数小于 len 且成功读入节点数值时循环
        {
            p1 = new ListNode(num); // 动态申请内存，创建一个存储数值 num 的新节点
            n++; // 已构建节点计数自增 1
            if (n == 1) // 如果是建立的第一个节点
                head = p1; // 将其设为整条链表的起始头节点 head
            else // 如果不是第一个节点
                p2->next = p1; // 将当前末尾节点 p2 的 next 指针指向新创建的节点 p1
            p2 = p1; // 更新 p2 指针，使其重新指向链表的最末尾节点
        }

        // 调用解题函数计算结果
        vector<int> res = Solution().nextLargerNodes(head); // 实例化 Solution 对象并调用 nextLargerNodes 函数，获取结果数组

        // 输出结果，按题目格式要求用空格隔开
        for (size_t i = 0; i < res.size(); i++) // 遍历输出结果数组 res 中的所有元素
        {
            if (i > 0) cout << " "; // 若不是输出第一个元素，则在前补充一个空格作为分割
            cout << res[i]; // 输出当前下标的结果数值
        }
        cout << "\n"; // 当前测试用例处理完毕，输出换行符
    }

    return 0; // 程序执行成功，返回状态码 0
}