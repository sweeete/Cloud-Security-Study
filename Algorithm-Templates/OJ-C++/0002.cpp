#include <iostream>
using namespace std;
struct student
{
    int  num;
    student  *next;
};
//从键盘读入数据创建链表，新结点插入到尾部
student *createByTail()
{
    student *head;
    student *p1, *p2;
    int n;
    n = 0;
    p1 = p2 = new student;
    cin >> p1->num;
    head = NULL;  //首先置链表为空链表
    if (p1->num == -1)    //num为-1，意味着用户输入结束
    {
        delete p1;
        return head;
    }
    while (p1->num != -1)    //num为-1，意味着用户输入结束
    {
        n = n + 1;
        if (n == 1)            //创建第一个结点
            head = p1;
        else
            p2->next = p1;
        p2 = p1;            //p2始终指向最后一个结点（即尾指针）
        p1 = new student; //p1指向新结点
        cin >> p1->num;
    }
    p2->next = NULL;  //最后一个结点的next赋值为NULL
    delete p1;
    return head;
}
//输出链表中的信息（num）
void  displayLink(student *head)
{
    student *p;
    p = head;
    cout << "head-->";
    while (p != NULL)
    {
        cout << p->num << "-->";
        p = p->next;
    }
    cout << "tail\n";
}
//在链表中第index处插入s指针所指向的结点。index从1开始。
//由于可能插在第一个结点，所以函数返回头指针给主调函数
student *insertNode(student *head, student *s, int index)
{
    // 如果插入位置小于 1，属于非法位置，直接返回原头指针
    if (index < 1)
    {
        return head;
    }

    // 情况1：插入到第 1 个位置（改变头指针）
    if (index == 1)
    {
        s->next = head;
        return s; // s 成为新的头结点
    }

    // 情况2：插入到其他位置（需要找到第 index - 1 个结点）
    student *p = head;
    int i = 1;

    // 遍历链表，找第 index - 1 个结点
    while (p != NULL && i < index - 1)
    {
        p = p->next;
        i++;
    }

    // 如果 p 为 NULL，说明 index 超出了链表的有效范围 (index > n + 1)
    if (p == NULL)
    {
        return head; // 不进行插入，直接返回原链表
    }

    // 执行插入操作：将 s 插入到 p 的后面
    s->next = p->next;
    p->next = s;

    return head;
}
int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    student *head;
    int index, data;
    head = createByTail();
    while (cin >> index >> data)
    {
        student *s = new student;
        s->num = data;
        s->next = NULL;
        student *newHead = insertNode(head, s, index);
        bool linked = (newHead == s);
        for (student *p = newHead; p != NULL && !linked; p = p->next)
        {
            if (p->next == s)
            {
                linked = true;
            }
        }
        if (linked)
        {
            head = newHead;
        }
        else
        {
            delete s;
        }
        displayLink(head);
    }
    while (head != NULL)
    {
        student *temp = head;
        head = head->next;
        delete temp;
    }
    return 0;
}
