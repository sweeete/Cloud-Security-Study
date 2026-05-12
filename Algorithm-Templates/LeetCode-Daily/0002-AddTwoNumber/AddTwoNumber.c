#include <stdio.h>
#include <stdlib.h>

// 定义链表节点
struct ListNode {
    int val;
    struct ListNode *next;
};

struct ListNode* addTwoNumbers(struct ListNode* l1, struct ListNode* l2) {
    struct ListNode dummy;//dummy是一个结构体变量，不是指针
    dummy.next = NULL;//dummy的下一个节点就是结果节点的头结点
    struct ListNode* tail = &dummy;//tail指向dummy
    int carry = 0;//carry表示进位

    while (l1 != NULL || l2 != NULL || carry > 0) {
        int v1 =(l1 != NULL) ? l1->val : 0;//v1表示l1的当前位
        int v2 =(l2 != NULL) ? l2->val : 0;//v2表示l2的当前位

        int sum = v1 + v2 + carry;//sum表示当前位的和
        carry = sum / 10;//carry表示进位

        struct ListNode* newNode = (struct ListNode*)malloc(sizeof(struct ListNode));//分配新节点
        newNode->val = sum % 10;//更新新节点的值为sum的个位数
        newNode->next = NULL;//新节点的下一个节点为空

        tail->next = newNode;//把新节点挂到tail的下一个节点
        tail = newNode;//移动tail到新节点

        if (l1 != NULL) l1 = l1->next;//判断是否还有节点，如果非空则移动l1到l1的下一个节点
        if (l2 != NULL) l2 = l2->next;//判断是否还有节点，如果非空则移动l2到l2的下一个节点
    }

    return dummy.next;//返回结果链表的头节点
}

//根据数组创建链表
struct ListNode* createList(int* arr, int size) {
    if (size == 0) return NULL;//如果size为0，则返回空
    struct ListNode* head = (struct ListNode*)malloc(sizeof(struct ListNode));//分配头节点
    head->val = arr[0];//头节点的值为数组的第一个元素
    head->next = NULL;//头节点的下一个节点为空
    struct ListNode* curr = head;//curr表示当前遍历到的节点，先指向头节点
    for (int i = 1; i < size; i++) {//遍历数组
        curr->next = (struct ListNode*)malloc(sizeof(struct ListNode));//分配新节点，并让curr的下一个节点指向新节点
        curr->next->val = arr[i];//新节点的值为数组的当前元素
        curr->next->next = NULL;//新节点的下一个节点为空
        curr = curr->next;//移动curr到新节点
    }
    return head;//返回头节点
}

//打印链表
void printList(struct ListNode* node) {
    while (node) {//遍历链表
        printf("%d", node->val);//打印当前节点的值
        if (node->next) printf("->");//如果当前节点不是尾节点，则打印->
        node = node->next;//移动node到下一个节点
    }
    printf("\n");//打印换行符
}

int main() {//主函数
    int arr1[] = {2, 4, 3};//数组1
    int arr2[] = {5, 6, 4};//数组2
    struct ListNode* l1 = createList(arr1, 3);//根据数组1创建链表1
    struct ListNode* l2 = createList(arr2, 3);//根据数组2创建链表2
    
    printf("List 1: ");
    printList(l1);//打印链表1
    printf("List 2: ");
    printList(l2);//打印链表2
    struct ListNode* result = addTwoNumbers(l1, l2);
    printf("Result: ");
    printList(result);//打印结果链表
    return 0;//返回0
}