#include <iostream>

// 定义链表节点结构体
struct Node {
    int data;
    Node* next;

    Node(int val = 0) : data(val), next(nullptr) {}
};

// 尾插法创建单链表
Node* createList(int n) {
    Node* head = new Node(); // 虚拟头节点
    Node* tail = head;

    for (int i = 0; i < n; ++i) {
        int val;
        std::cin >> val;
        Node* p = new Node(val);
        tail->next = p;
        tail = p;
    }
    return head;
}

// 利用有序特性的双指针求交集算法：O(N + M)
// 如果遇到相等的就插入，否则谁小谁后移
Node* getIntersection(Node* headA, Node* headB) {
    Node* headC = new Node(); // 存放交集的虚拟头节点
    Node* tailC = headC;

    Node* pA = headA->next;
    Node* pB = headB->next;

    while (pA != nullptr && pB != nullptr) {
        if (pA->data == pB->data) {
            // 找到了相等元素
            // 去重判断：只有当 C 为空（tailC == headC）或者新元素不等于 C 的最后一个元素时才插入
            if (tailC == headC || tailC->data != pA->data) {
                Node* p = new Node(pA->data);
                tailC->next = p;
                tailC = p;
            }
            pA = pA->next;
            pB = pB->next;
        } 
        else if (pA->data < pB->data) {
            pA = pA->next; // pA 较小，后移 pA
        } 
        else {
            pB = pB->next; // pB 较小，后移 pB
        }
    }

    return headC;
}

// 输出链表
void displayList(Node* head) {
    std::cout << "head";
    Node* p = head->next;
    while (p != nullptr) {
        std::cout << "-->" << p->data;
        p = p->next;
    }
    std::cout << "-->tail\n";
}

// 释放内存
void freeList(Node* head) {
    while (head != nullptr) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }
}

int main() {
    // 提升 cin/cout 读写效率
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, m;

    // 读入序列 A
    if (std::cin >> n) {
        Node* headA = createList(n);

        // 读入序列 B
        if (std::cin >> m) {
            Node* headB = createList(m);

            // 求交集
            Node* headC = getIntersection(headA, headB);

            // 输出
            displayList(headC);

            // 释放内存
            freeList(headA);
            freeList(headB);
            freeList(headC);
        }
    }

    return 0;
}