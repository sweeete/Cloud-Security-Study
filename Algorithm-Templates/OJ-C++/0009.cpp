#include <iostream>
#include <string>
#include <iomanip>

using namespace std;

// 双向链表节点定义
struct Node {
    int data;
    Node* prev;
    Node* next;
    Node(int val = 0) : data(val), prev(nullptr), next(nullptr) {}
};

// 去除输入字符串中多余的前导 0，并规范化 "-0" 为 "0"
void sanitizeInputString(string& str) {
    if (str.empty()) return;
    int start = 0;
    bool negative = false;
    if (str[0] == '-') {
        negative = true;
        start = 1;
    } else if (str[0] == '+') {
        start = 1;
    }
    while (start < (int)str.length() - 1 && str[start] == '0') {
        start++;
    }
    string sanitized = str.substr(start);
    if (negative && sanitized != "0") {
        str = "-" + sanitized;
    } else {
        str = sanitized;
    }
}

// 将字符串转为带头结点的双向链表，每4位一个节点
Node* createList(const string& str) {
    Node* head = new Node(1); // 默认符号为正 (1)
    int start = 0;
    if (str[0] == '-') {
        head->data = -1;
        start = 1;
    } else if (str[0] == '+') {
        head->data = 1;
        start = 1;
    }
    
    int len = str.length() - start;
    if (len <= 0) {
        Node* p = new Node(0);
        head->next = p;
        p->prev = head;
        return head;
    }
    
    // 第一组（高位）的长度可能不足4位
    int first_group_len = len % 4;
    if (first_group_len == 0) first_group_len = 4;
    
    Node* tail = head;
    auto addNode = [&](int val) {
        Node* p = new Node(val);
        tail->next = p;
        p->prev = tail;
        tail = p;
    };
    
    // 解析第一组
    int val = 0;
    for (int i = 0; i < first_group_len; ++i) {
        val = val * 10 + (str[start + i] - '0');
    }
    addNode(val);
    
    // 解析后续的4位分组
    for (int i = start + first_group_len; i < (int)str.length(); i += 4) {
        val = 0;
        for (int j = 0; j < 4; ++j) {
            val = val * 10 + (str[i + j] - '0');
        }
        addNode(val);
    }
    
    // 如果值全为 0，强制将符号置为正 (1)
    bool all_zero = true;
    Node* curr = head->next;
    while (curr) {
        if (curr->data != 0) {
            all_zero = false;
            break;
        }
        curr = curr->next;
    }
    if (all_zero) {
        head->data = 1;
    }
    
    return head;
}

// 比较两数绝对值大小。返回 1 表示 A>B，-1 表示 A<B，0 表示相等
int compareAbsolute(Node* headA, Node* headB) {
    int lenA = 0, lenB = 0;
    Node* currA = headA->next;
    while (currA) { lenA++; currA = currA->next; }
    Node* currB = headB->next;
    while (currB) { lenB++; currB = currB->next; }
    
    if (lenA > lenB) return 1;
    if (lenA < lenB) return -1;
    
    currA = headA->next;
    currB = headB->next;
    while (currA && currB) {
        if (currA->data > currB->data) return 1;
        if (currA->data < currB->data) return -1;
        currA = currA->next;
        currB = currB->next;
    }
    return 0;
}

// 绝对值无符号加法（尾插+逆向操作，头插法构建新链表）
Node* absoluteAddition(Node* headA, Node* headB) {
    Node* tailA = headA;
    while (tailA->next) tailA = tailA->next;
    Node* tailB = headB;
    while (tailB->next) tailB = tailB->next;
    
    Node* headC = new Node(1);
    int carry = 0;
    
    Node* pA = tailA;
    Node* pB = tailB;
    
    // 从右往左遍历计算，并使用“头插法”插入新链表，使高位保持在前面
    while (pA != headA || pB != headB || carry > 0) {
        int sum = carry;
        if (pA != headA) {
            sum += pA->data;
            pA = pA->prev;
        }
        if (pB != headB) {
            sum += pB->data;
            pB = pB->prev;
        }
        
        carry = sum / 10000;
        int val = sum % 10000;
        
        Node* p = new Node(val);
        p->next = headC->next;
        if (headC->next) headC->next->prev = p;
        headC->next = p;
        p->prev = headC;
    }
    
    return headC;
}

// 绝对值无符号减法（要求 A >= B）
Node* absoluteSubtraction(Node* headA, Node* headB) {
    Node* tailA = headA;
    while (tailA->next) tailA = tailA->next;
    Node* tailB = headB;
    while (tailB->next) tailB = tailB->next;
    
    Node* headC = new Node(1);
    int borrow = 0;
    
    Node* pA = tailA;
    Node* pB = tailB;
    
    while (pA != headA) {
        int diff = pA->data - borrow;
        pA = pA->prev;
        
        if (pB != headB) {
            diff -= pB->data;
            pB = pB->prev;
        }
        
        if (diff < 0) {
            diff += 10000;
            borrow = 1;
        } else {
            borrow = 0;
        }
        
        Node* p = new Node(diff);
        p->next = headC->next;
        if (headC->next) headC->next->prev = p;
        headC->next = p;
        p->prev = headC;
    }
    
    // 清除高位多余的 0 节点（例如 10001 - 10000 产生的 00001 中的前导0）
    while (headC->next && headC->next->data == 0 && headC->next->next != nullptr) {
        Node* temp = headC->next;
        headC->next = temp->next;
        temp->next->prev = headC;
        delete temp;
    }
    
    return headC;
}

// 带符号的完整加法
Node* addSigned(Node* headA, Node* headB) {
    int signA = headA->data;
    int signB = headB->data;
    Node* headC = nullptr;
    
    if (signA == signB) {
        // 同号相加
        headC = absoluteAddition(headA, headB);
        headC->data = signA;
    } else {
        // 异号相减
        int cmp = compareAbsolute(headA, headB);
        if (cmp == 0) {
            headC = new Node(1);
            Node* p = new Node(0);
            headC->next = p;
            p->prev = headC;
        } else if (cmp > 0) {
            headC = absoluteSubtraction(headA, headB);
            headC->data = signA;
        } else {
            headC = absoluteSubtraction(headB, headA);
            headC->data = signB;
        }
    }
    
    // 检查结果是否为 0，防止输出 "-0"
    bool all_zero = true;
    Node* curr = headC->next;
    while (curr) {
        if (curr->data != 0) {
            all_zero = false;
            break;
        }
        curr = curr->next;
    }
    if (all_zero) {
        headC->data = 1;
    }
    
    return headC;
}

// 格式化输出长整数（高位到低位打印，除第一组外每组保留4位宽度）
void printList(Node* head) {
    if (!head || !head->next) return;
    if (head->data == -1) {
        cout << "-";
    }
    Node* curr = head->next;
    cout << curr->data; // 第一项不需要补前导0
    curr = curr->next;
    while (curr) {
        // 后续项必须补齐 4 位
        cout << "," << setfill('0') << setw(4) << curr->data;
        curr = curr->next;
    }
    cout << "\n";
}

// 释放链表内存
void freeList(Node* head) {
    Node* curr = head;
    while (curr) {
        Node* temp = curr;
        curr = curr->next;
        delete temp;
    }
}

int main() {
    string x_str, y_str;
    if (cin >> x_str >> y_str) {
        sanitizeInputString(x_str);
        sanitizeInputString(y_str);
        
        Node* headA = createList(x_str);
        Node* headB = createList(y_str);
        
        printList(headA);
        printList(headB);
        cout << "\n"; // 输出格式要求的空行
        
        Node* headC = addSigned(headA, headB);
        printList(headC);
        
        freeList(headA);
        freeList(headB);
        freeList(headC);
    }
    return 0;
}