#include <iostream>

// 定义学生结构体，C++ 中使用类型名时可省略 struct 关键字
struct Student {
    int num;
    Student* next;

    // C++ 结构体构造函数，方便初始化
    Student(int val = 0) : num(val), next(nullptr) {}
};

// 尾插法创建单链表，输入 -1 表示结束
Student* createByTail() {
    Student* head = nullptr;
    Student* tail = nullptr; // 尾指针，始终指向当前链表末尾
    int num;

    // 循环读取输入，当输入 -1 时停止
    while (std::cin >> num && num != -1) {
        Student* newNode = new Student(num); // 使用 new 动态分配结点内存
        if (head == nullptr) {
            head = newNode; // 第一个结点作为头结点
        } else {
            tail->next = newNode; // 插入到末尾
        }
        tail = newNode; // 更新尾指针
    }
    return head;
}

// 打印链表信息
void displayLink(Student* head) {
    Student* p = head;
    std::cout << "head-->";
    while (p != nullptr) {
        std::cout << p->num << "-->";
        p = p->next;
    }
    std::cout << "tail\n";
}

// 将结点 stu 按升序插入到有序链表中
Student* insertNodeInOrder(Student* head, Student* stu) {
    Student* p1 = head;
    Student* p0 = stu;
    Student* p2 = nullptr;

    // 若当前为空链表，直接作为头结点
    if (head == nullptr) {
        p0->next = nullptr;
        return p0;
    }

    // 查找合适的插入位置，p2 跟踪 p1 的前驱
    while (p0->num > p1->num && p1->next != nullptr) {
        p2 = p1;
        p1 = p1->next;
    }

    // 判断是由哪个条件退出的 while 循环
    if (p0->num <= p1->num) {
        // 插在 p1 结点之前
        if (head == p1) {
            head = p0; // 插入在头结点之前
        } else {
            p2->next = p0; // 插入在 p2 与 p1 之间
        }
        p0->next = p1;
    } else {
        // p0->num 最大，插在链表末尾
        p1->next = p0;
        p0->next = nullptr;
    }

    return head;
}

// 对链表进行插入排序
Student* sort(Student* head) {
    Student* p = head;
    Student* s = nullptr;
    head = nullptr;

    while (p != nullptr) {
        s = p;
        p = p->next;
        head = insertNodeInOrder(head, s);
    }
    return head;
}

// 将链表 LB 合并到链表 LA 中（升序插入）
Student* merge(Student* LA, Student* LB) {
    Student* p = LB;
    Student* s = nullptr;

    while (p != nullptr) {
        s = p;
        p = p->next;
        LA = insertNodeInOrder(LA, s);
    }
    return LA;
}

// 从链表 LA 中减去在 LB 中出现的元素 (集合差集: LA = LA - LB)
Student* subtract(Student* LA, Student* LB) {
    Student* p = LB;

    while (p != nullptr) {
        Student* q = LA;
        Student* pre = nullptr; // 指向 q 的前驱

        // 在 LA 中查找是否存在值与 p->num 相同的结点
        while (q != nullptr && q->num != p->num) {
            pre = q;
            q = q->next;
        }

        // 若找到相同元素，则从 LA 中删除 q 结点并释放内存
        if (q != nullptr) {
            if (q == LA) {
                LA = LA->next; // 删除的是头结点
            } else {
                pre->next = q->next; // 删除的是中间或尾部结点
            }
            delete q; // C++ 释放内存
        }
        p = p->next;
    }
    return LA;
}

// 删除已排序链表中的重复元素
void purge(Student* head) {
    if (head == nullptr || head->next == nullptr) return;

    Student* p = head;
    while (p->next != nullptr) {
        if (p->num == p->next->num) {
            Student* q = p->next;
            p->next = q->next;
            delete q; // 释放重复结点的内存
        } else {
            p = p->next;
        }
    }
}

// 混合逻辑函数：
// 若 L2 中的元素在 L1 中存在，则从 L1 中删除该元素，并释放 L2 对应结点；
// 若不存在，则将 L2 的该结点按序插入到 L1 中。
Student* fun(Student* L1, Student* L2) {
    Student* p = L2;

    while (p != nullptr) {
        Student* next_p = p->next; // 暂存 L2 的下一个结点
        Student* q = L1;
        Student* pre = nullptr;

        // 查找 L1 中是否存在与 p->num 匹配的结点
        while (q != nullptr && q->num != p->num) {
            pre = q;
            q = q->next;
        }

        if (q != nullptr) {
            // L1 中存在匹配值：从 L1 中移除 q，同时销毁 q 与 p 结点
            if (q == L1) {
                L1 = L1->next;
            } else {
                pre->next = q->next;
            }
            delete q;
            delete p;
        } else {
            // L1 中不存在：将 p 结点插入到 L1 中
            L1 = insertNodeInOrder(L1, p);
        }

        p = next_p;
    }
    return L1;
}

// 释放链表内存（防止内存泄漏）
void destroyList(Student* head) {
    while (head != nullptr) {
        Student* temp = head;
        head = head->next;
        delete temp;
    }
}

int main() {
    Student *headA, *headB, *headC, *headD;
    int n;

    // 循环处理输入的组数
    while (std::cin >> n) {
        for (int i = 0; i < n; ++i) {
            // 创建 4 个链表
            headA = createByTail();
            headB = createByTail();
            headC = createByTail();
            headD = createByTail();

            // 对链表进行升序排序
            headA = sort(headA);
            headB = sort(headB);
            headC = sort(headC);
            headD = sort(headD);

            // 执行核心逻辑
            headA = merge(headA, headB);      // 合并 A 和 B
            purge(headA);                      // 去重 A
            headA = subtract(headA, headC);   // A 减去 C 中的元素
            headA = fun(headA, headD);        // A 与 D 进行混合交并集逻辑

            // 打印结果链表
            displayLink(headA);

            // 清理最终链表的内存
            destroyList(headA);
        }
    }
    return 0;
}