#include <iostream>
#include <string>
#include <ctime>

// 定义链表节点结构体
struct Node {
    char data;
    Node* next;

    // C++ 结构体构造函数，简化节点的创建和初始化
    Node(char c = '\0') : data(c), next(nullptr) {}
};

// 根据输入字符串创建链表，模拟 Home/End 键效果
Node* create(const std::string& text) {
    Node* head = new Node(); // 创建虚拟头节点（Dummy Head）
    Node* current = head;    // 当前光标插入位置的指针
    Node* tail = head;       // 尾指针，始终指向链表末尾

    for (char ch : text) {
        if (ch == '[') {
            // '[' 相当于 Home 键：把光标移动到链表最前面（头节点位置），转到最前方开始插入
            current = head;
        } 
        else if (ch == ']') {
            // ']' 相当于 End 键：把光标移动到链表最后面（尾节点位置），回到刚刚的位置继续插入
            current = tail;
        } 
        else {
            // 普通字符：在当前光标 current 后面插入新节点
            Node* p = new Node(ch);
            p->next = current->next;
            current->next = p;
            current = p; // 光标移动到新插入的节点之后

            // 如果插入到了最末尾，需要更新尾指针 tail
            if (current->next == nullptr) {
                tail = current;
            }
        }
    }
    return head;
}

// 统计链表中的单词数量（由空格分隔）
int count(Node* head) {
    int wordCount = 0;
    bool inWord = false;   // 状态标志：false 表示当前不在单词中，true 表示正在遍历单词
    Node* p = head->next;  // 从第一个实际数据节点（跳过虚拟头节点）开始遍历

    while (p != nullptr) {
        if (p->data != ' ') {
            // 当前字符不是空格，且之前不在单词中，说明遇到了新单词的开头
            if (!inWord) {
                wordCount++;
                inWord = true; // 切换状态为“在单词中”
            }
        } 
        else {
            // 遇到空格，说明前一个单词结束
            inWord = false;
        }
        
        p = p->next; // 移动指针到下一个节点
    }

    return wordCount;
}

// 释放链表内存，防止内存泄漏
void destroyList(Node* head) {
    while (head != nullptr) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }
}

int main() {
    // 优化标准输入输出流的性能
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string text;

    // 循环按行读取输入，替代已废弃的危险函数 gets()
    while (std::getline(std::cin, text)) {
        Node* head = create(text);
        
        int num = count(head);
        std::cout << num << "\n";

        // 清理链表内存
        destroyList(head);
    }

    return 0;
}