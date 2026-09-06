#include <iostream>
using namespace std;

struct student
{
    int num;
    student *next;
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
    if (p1->num == -1)  //首输入即为-1，删除未链接结点并返回空链表
    {
        delete p1;
        return head;
    }
    while (p1->num != -1)  //num为-1，意味着用户输入结束
    {
        n = n + 1;
        if (n == 1)  //创建第一个结点
            head = p1;
        else
            p2->next = p1;
        p2 = p1;  //p2始终指向最后一个结点（即尾指针）
        p1 = new student;  //p1指向新结点
        cin >> p1->num;
    }
    p2->next = NULL;  //切记：最后一个结点的next赋值为NULL
    delete p1;  //释放读入-1的未链接结点
    return head;
}

//输出链表中的信息（num）
void displayLink(student *head)
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

//删除链表中第index个结点。index从1开始。
//由于可能删除第一个结点，所以函数返回头指针给主调函数
student *deleteNode(student *head, int index)
{
    if (head == NULL || index < 1)
    {
        return head;
    }
    student *temp;
    if (index == 1)
    {
        temp = head;
        head = head->next;
        delete temp;
        return head;
    }
    student *p = head;
    int i = 1;
    while (p != NULL && i < index - 1)
    {
        p = p->next;
        i++;
    }
    if (p == NULL || p->next == NULL)
    {
        return head;
    }
    temp = p->next;
    p->next = temp->next;
    delete temp;

    return head;
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    student *head;
    int index;
    head = createByTail();
    while (cin >> index)
    {
        head = deleteNode(head, index);
        displayLink(head);
    }
    //main结束前释放整条链表
    while (head != NULL)
    {
        student *temp = head;
        head = head->next;
        delete temp;
    }
    return 0;
}
