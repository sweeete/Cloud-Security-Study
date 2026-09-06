#include <iostream> // 引入标准输入输出流库，用于 cin 和 cout 操作
#include <vector>   // 引入动态数组容器库，用于临时存储输入的序列数据

using namespace std; // 使用标准命名空间，避免频繁使用 std:: 前缀

// 定义多项式单链表节点的结构体
struct PolyNode {
    int coef; // 节点的成员变量：存储多项式项的系数 (Coefficient)
    int exp;  // 节点的成员变量：存储多项式项的指数 (Exponent)
    PolyNode* next; // 指针域：指向链表中下一个多项式节点的指针
    PolyNode(int c = 0, int e = 0) : coef(c), exp(e), next(nullptr) {} // 构造函数：初始化系数、指数并将 next 置空
};

// 函数：从标准输入读取数据并构建带头结点的有序单链表
PolyNode* readPoly() {
    int n; // 定义变量 n，用于保存多项式的项数
    if (!(cin >> n)) { // 尝试读取项数 n，若读取失败（如文件末尾或非法输入）
        return new PolyNode(); // 直接返回一个空的头结点指针，终止后续读取
    }
    PolyNode* head = new PolyNode(); // 动态创建一个虚拟头结点（Dummy Head），方便统一链表插入逻辑
    if (n == 0) { // 如果输入的项数为 0，说明是零多项式
        return head; // 直接返回仅包含虚拟头结点的空链表
    }
    vector<int> coefs(n); // 创建大小为 n 的动态数组，用于临时存储所有系数
    for (int i = 0; i < n; ++i) { // 循环 n 次
        cin >> coefs[i]; // 依次读取每一个多项式项的系数
    }
    vector<int> exps(n); // 创建大小为 n 的动态数组，用于临时存储所有指数
    for (int i = 0; i < n; ++i) { // 循环 n 次
        cin >> exps[i]; // 依次读取每一个多项式项的指数
    }
    PolyNode* tail = head; // 定义尾指针 tail，初始时指向虚拟头结点
    for (int i = 0; i < n; ++i) { // 遍历刚刚读取的系数和指数数组
        if (coefs[i] != 0) { // 过滤掉系数为 0 的无效项，只处理非零项
            PolyNode* p = new PolyNode(coefs[i], exps[i]); // 动态创建一个存放当前项系数和指数的新节点
            tail->next = p; // 将新节点 p 挂在当前尾节点 tail 的后面（尾插法）
            tail = p; // 更新尾指针 tail，使其指向新插入的节点 p
        }
    }
    return head; // 返回创建好的多项式链表的头结点指针
}

// 函数：按格式输出多项式链表
void printPoly(PolyNode* head) {
    if (head->next == nullptr) { // 检查链表是否为空（首元节点为空说明是零多项式）
        cout << "0 0\n"; // 如果是空多项式，按要求输出 "0 0" 并换行
        return; // 直接结束函数
    }
    PolyNode* curr = head->next; // 定义指针 curr，初始指向链表中的第一个有效数据节点（首元节点）
    while (curr != nullptr) { // 循环遍历链表，直到指针指向末尾的 nullptr
        cout << curr->coef << " " << curr->exp << "\n"; // 输出当前节点的系数和指数，中间用空格分隔并换行
        curr = curr->next; // 将指针 curr 移动到下一个节点
    }
}

// 函数：释放链表占用的所有动态内存，防止内存泄漏
void freePoly(PolyNode* head) {
    PolyNode* curr = head; // 定义指针 curr，初始指向链表的头结点
    while (curr != nullptr) { // 当指针不为空时继续循环
        PolyNode* temp = curr; // 用临时指针 temp 保存当前要释放的节点地址
        curr = curr->next; // 将 curr 指针安全地后移到下一个节点
        delete temp; // 释放 temp 保存的节点动态内存
    }
}

// 主函数：程序的入口
int main() {
    int op; // 定义变量 op，用于存储运算操作符（0 表示加法，1 表示减法）
    if (!(cin >> op)) return 0; // 读取操作符，如果读取失败则直接正常退出程序

    PolyNode* headA = readPoly(); // 调用 readPoly 函数构建多项式 A 的链表
    PolyNode* headB = readPoly(); // 调用 readPoly 函数构建多项式 B 的链表

    printPoly(headA); // 输出原始多项式 A 的内容
    cout << "\n"; // 输出一个空行隔开

    printPoly(headB); // 输出原始多项式 B 的内容
    cout << "\n"; // 输出一个空行隔开

    if (op == 1) { // 如果操作符为 1，说明要执行减法运算 (A - B)
        PolyNode* curr = headB->next; // 定义指针 curr 指向多项式 B 的首元节点
        while (curr != nullptr) { // 遍历多项式 B 的所有有效节点
            curr->coef = -curr->coef; // 将多项式 B 中每一项的系数取相反数（转换为加法 A + (-B)）
            curr = curr->next; // 指针移动到下一个节点
        }
    }

    // 核心算法：将多项式 B 原地有序归并到多项式 A 中
    PolyNode* prevA = headA; // prevA 指向 A 链表中当前比较节点的前驱节点，初始为头结点
    PolyNode* currA = headA->next; // currA 指向 A 链表中当前正在比较的有效节点
    PolyNode* currB = headB->next; // currB 指向 B 链表中当前正在比较的有效节点

    while (currA != nullptr && currB != nullptr) { // 当链表 A 和 B 都未遍历完时循环
        if (currA->exp < currB->exp) { // 情况 1：当前 A 节点的指数小于 B 节点的指数
            prevA = currA; // 将前驱指针 prevA 后移到当前 A 节点
            currA = currA->next; // 将当前指针 currA 后移到下一个 A 节点
        } 
        else if (currA->exp > currB->exp) { // 情况 2：当前 A 节点的指数大于 B 节点的指数
            PolyNode* nextB = currB->next; // 暂存 B 链表中 currB 的下一个节点地址
            currB->next = currA; // 将节点 currB 的 next 指向当前 A 节点 currA
            prevA->next = currB; // 将前驱节点 prevA 的 next 指向节点 currB（插入到 A 链表中）
            prevA = currB; // 更新前驱指针 prevA 为刚插入的节点 currB
            currB = nextB; // 将 B 链表指针 currB 移动到暂存的下一个节点
        } 
        else { // 情况 3：当前 A 节点与 B 节点的指数相同，需要合并同类项
            currA->coef += currB->coef; // 将 B 节点的系数加到 A 节点的系数上
            PolyNode* nextB = currB->next; // 暂存 B 链表中 currB 的下一个节点地址
            delete currB; // 节点 B 已合并完，释放其内存空间
            currB = nextB; // 将 B 链表指针 currB 移动到暂存的下一个节点
            
            if (currA->coef == 0) { // 如果合并后 A 节点的系数变为 0（相互抵消）
                PolyNode* temp = currA; // 暂存系数为 0 的 A 节点地址以便释放
                prevA->next = currA->next; // 将前驱节点 prevA 的 next 绕过当前节点，指向下一个 A 节点
                currA = currA->next; // 将当前指针 currA 后移到下一个 A 节点
                delete temp; // 释放系数抵消归零的节点内存
            } else { // 如果合并后系数不为 0
                prevA = currA; // 正常更新前驱指针 prevA 为当前合并后的 A 节点
                currA = currA->next; // 将当前指针 currA 后移到下一个 A 节点
            }
        }
    }

    if (currB != nullptr) { // 如果循环结束后 B 链表中还有剩余节点（说明这些节点的指数都大于 A 中现有节点）
        prevA->next = currB; // 直接将剩余的 B 链表整个挂在 A 链表的末尾
    }

    headB->next = nullptr; // 切断 B 链表头结点与有效节点之间的连接，防止误操作
    delete headB; // 释放已经失去作用的多项式 B 的虚拟头结点

    printPoly(headA); // 格式化输出最终合并计算完成的多项式 A

    freePoly(headA); // 释放结果链表 A 的所有动态内存空间

    return 0; // 程序正常执行完毕，返回 0
}