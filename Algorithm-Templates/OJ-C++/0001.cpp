#include <iostream>

using namespace std;

// 链表节点结构体定义
struct Node {
    int data;       // 数据域：存储学生学号
    Node* next;     // 指针域：指向下一个节点
};

int main() {
    // 优化标准输入输出流的读写速度
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    // 读取学生总数，如果读取失败则结束程序
    if (!(cin >> n)) {
        return 0;
    }

    // 1. 初始化带头结点的单链表
    Node* head = new Node{0, nullptr}; // 头结点不存储有效学号数据
    Node* tail = head;                 // 尾指针，用于尾插法建立链表

    // 2. 读取 n 个学生的学号，并使用尾插法插入链表
    for (int i = 0; i < n; ++i) {
        int studentId;
        cin >> studentId;

        // 创建新节点并链接到链表尾部
        Node* newNode = new Node{studentId, nullptr};
        tail->next = newNode;
        tail = newNode;
    }

    // 3. 处理查找请求，直到文件结束 (EOF)
    int targetId;
    while (cin >> targetId) {
        Node* current = head->next; // 从第一个有效学生节点开始查找
        int pos = 1;                // 记录当前位置序号
        bool found = false;         // 标记是否找到

        // 遍历单链表进行顺序查找
        while (current != nullptr) {
            if (current->data == targetId) {
                cout << pos << "\n"; // 找到对应的学号，输出位置并换行
                found = true;
                break;               // 查找到结果即可跳出内层循环
            }
            current = current->next; // 指向下一个节点
            pos++;                   // 位置序号加 1
        }

        // 如果遍历完整个链表都没有找到
        if (!found) {
            cout << "no\n";
        }
    }

    // 4. 释放链表内存（良好的编程习惯，防止内存泄漏）
    Node* current = head;
    while (current != nullptr) {
        Node* temp = current;
        current = current->next;
        delete temp;
    }

    return 0;
}
