#include <stdio.h>
#include <stdlib.h>

// 定义链表节点
struct ListNode {
    int val;
    struct ListNode *next;
};

struct ListNode* addTwoNumbers(struct ListNode* l1, struct ListNode* l2) {
    struct ListNode dummy;
    dummy.next = NULL;
    struct ListNode* tail = &dummy;
    int carry = 0;

    while (l1 != NULL || l2 != NULL || carry > 0) {
        int v1 =(l1 != NULL) ? l1->val : 0;
        int v2 =(l2 != NULL) ? l2->val : 0;

        int sum = v1 + v2 + carry;
        carry = sum / 10;

        struct ListNode* newNode = (struct ListNode*)malloc(sizeof(struct ListNode));
        newNode->val = sum % 10;
        newNode->next = NULL;

        tail->next = newNode;
        tail = newNode;

        if (l1 != NULL) l1 = l1->next;
        if (l2 != NULL) l2 = l2->next;
    }

    return dummy.next;
}

struct ListNode* createList(int* arr, int size) {
    if (size == 0) return NULL;
    struct ListNode* head = (struct ListNode*)malloc(sizeof(struct ListNode));
    head->val = arr[0];
    head->next = NULL;
    struct ListNode* curr = head;
    for (int i = 1; i < size; i++) {
        curr->next = (struct ListNode*)malloc(sizeof(struct ListNode));
        curr->next->val = arr[i];
        curr->next->next = NULL;
        curr = curr->next;
    }
    return head;
}

void printList(struct ListNode* node) {
    while (node) {
        printf("%d", node->val);
        if (node->next) printf("->");
        node = node->next;
    }
    printf("\n");
}

int main() {
    int arr1[] = {2, 4, 3};
    int arr2[] = {5, 6, 4};
    struct ListNode* l1 = createList(arr1, 3);
    struct ListNode* l2 = createList(arr2, 3);
    
    printf("List 1: ");
    printList(l1);
    printf("List 2: ");
    printList(l2);
    struct ListNode* result = addTwoNumbers(l1, l2);
    printf("Result: ");
    printList(result);
    return 0;
}