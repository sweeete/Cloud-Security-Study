#include <iostream>

// 定义链表节点结构体
struct Node {
    int data;
    Node* next;

    // C++ 结构体构造函数：简化节点的创建与默认初始化
    Node(int val = 0) : data(val), next(nullptr) {}
};

// 尾插法创建带头节点的单链表
Node* createList(int n) {
    Node* head = new Node(); // 创建虚拟头节点（Dummy Head）
    Node* tail = head;       // 尾指针，初始化指向头节点

    for (int i = 0; i < n; ++i) {
        int val;
        std::cin >> val;
        Node* p = new Node(val); // 使用 new 动态分配节点内存
        tail->next = p;          // 将新节点连在末尾
        tail = p;                // 更新尾指针
    }
    return head;
}

// 在单链表中查找是否存在某个值，用 bool 类型替代 int
bool contains(Node* head, int val) {
    Node* p = head->next; // 跳过虚拟头节点，从第一个数据节点开始
    while (p != nullptr) {
        if (p->data == val) {
            return true; // 找到了
        }
        p = p->next;
    }
    return false; // 没找到
}

// 释放链表动态内存
void freeList(Node* head) {
    Node* p = head;
    while (p != nullptr) {
        Node* temp = p;
        p = p->next;
        delete temp; // 使用 delete 替代 free
    }
}

int main() {
    // 解绑 C/C++ 流同步，加快 std::cin / std::cout 性能
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, m;

    // 1. 读入序列 A 的信息并建表
    if (!(std::cin >> n)) return 0;
    Node* headA = createList(n);

    // 2. 读入序列 B 的信息并建表
    if (!(std::cin >> m)) return 0;
    Node* headB = createList(m);

    // 3. 构建交集链表 C
    Node* headC = new Node(); // 创建交集链表 C 的虚拟头节点
    Node* tailC = headC;

    Node* pA = headA->next;
    while (pA != nullptr) {
        // 若元素在 B 中存在，且尚未存入交集 C 中（去重）
        if (contains(headB, pA->data) && !contains(headC, pA->data)) {
            Node* p = new Node(pA->data);
            tailC->next = p;
            tailC = p;
        }
        pA = pA->next;
    }

    // 4. 按格式输出交集链表 C
    std::cout << "head";
    Node* pC = headC->next;
    while (pC != nullptr) {
        std::cout << "-->" << pC->data;
        pC = pC->next;
    }
    std::cout << "-->tail\n";

    // 5. 释放内存
    freeList(headA);
    freeList(headB);
    freeList(headC);

    return 0;
}