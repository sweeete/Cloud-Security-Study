#include <iostream>
#include <vector>
#include <string>

// 1. 定义循环单链表的节点结构体模板（无虚拟头结点）
template <typename T>
struct Node {
    T data;
    Node<T>* next;
    Node(const T& val = T(), Node<T>* nx = nullptr) : data(val), next(nx) {}
};

// 2. 设计无头结点的循环单链表类模板 (ADT)
template <typename T>
class CircularLinkList {
private:
    Node<T>* head; // 指向第一个有效节点
    Node<T>* tail; // 指向最后一个有效节点
    int length;

public:
    CircularLinkList() : head(nullptr), tail(nullptr), length(0) {}

    ~CircularLinkList() {
        clear();
    }

    // 【核心修复】：安全释放循环链表，完全不依赖 tail 指针
    void clear() {
        if (!head) return;
        
        Node<T>* curr = head->next;
        head->next = nullptr; // 1. 直接断开首尾相连的环，使其变成普通单链表
        
        while (curr != nullptr) { // 2. 顺着单链表安全释放所有节点
            Node<T>* temp = curr;
            curr = curr->next;
            delete temp;
        }
        
        head = nullptr;
        tail = nullptr;
        length = 0;
    }

    // O(1) 尾插法（保留高效建表）
    void append(const T& val) {
        Node<T>* newNode = new Node<T>(val);
        if (!head) {
            head = newNode;
            head->next = head; 
            tail = head;
        } else {
            tail->next = newNode;
            newNode->next = head; 
            tail = newNode;
        }
        length++;
    }

    Node<T>* getHead() const { return head; }
    Node<T>* getTail() const { return tail; }
    int getLength() const { return length; }

    void setHead(Node<T>* newHead) { head = newHead; }
};

// 3. 解决圆桌问题的核心算法
void solveJosephus(int n, int m) {
    if (n <= 0) return; // 防御性逻辑：防止特殊无意义输入

    // 初始化结果数组，默认全为 'G' (好人)
    std::vector<char> result(2 * n + 1, 'G');

    // 创建循环链表
    CircularLinkList<int> list;
    for (int i = 1; i <= 2 * n; ++i) {
        list.append(i);
    }

    Node<int>* prev_ptr = list.getTail();
    Node<int>* head = list.getHead();

    for (int step = 0; step < n; ++step) {
        // 数 m 个有效人
        for (int i = 0; i < m - 1; ++i) {
            prev_ptr = prev_ptr->next;
        }

        Node<int>* to_delete = prev_ptr->next;
        result[to_delete->data] = 'B'; // 标记坏人

        prev_ptr->next = to_delete->next; // 从链表中摘除

        // 如果删掉的是 head 节点，更新维护好 head 指针
        if (to_delete == head) {
            head = prev_ptr->next;
            list.setHead(head);
        }

        delete to_delete; // 安全释放单个节点
    }

    // 4. 高效格式化输出
    std::string out_buf;
    out_buf.reserve(2 * n + (2 * n) / 50 + 5);
    for (int i = 1; i <= 2 * n; ++i) {
        out_buf += result[i];
        if (i % 50 == 0) {
            out_buf += '\n';
        }
    }
    if ((2 * n) % 50 != 0) {
        out_buf += '\n';
    }
    std::cout << out_buf;
}

int main() {
    // 开启 C++ Fast I/O
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, m;
    while (std::cin >> n >> m) {
        solveJosephus(n, m);
    }
    return 0;
}