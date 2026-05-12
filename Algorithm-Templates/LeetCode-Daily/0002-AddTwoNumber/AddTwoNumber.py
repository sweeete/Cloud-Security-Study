from typing import Optional

# 定义链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 定义解决方案
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        curr = dummy
        carry = 0
        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0 # 如果l1不为空，则取l1的值，否则取0
            val2 = l2.val if l2 else 0 # 如果l2不为空，则取l2的值，否则取0

            total = val1 + val2 + carry # 计算当前位的和
            carry = total // 10 # 计算进位

            curr.next = ListNode(total % 10) # 创建新节点，值为当前位的和的个位数，并让curr的下一个节点指向新节点
            curr = curr.next # 移动curr到新节点

            l1 = l1.next if l1 else None # 如果l1不为空，则移动l1到l1的下一个节点，否则取None
            l2 = l2.next if l2 else None # 如果l2不为空，则移动l2到l2的下一个节点，否则取None

        return dummy.next # 返回结果链表的头节点

# 根据数组创建链表
def build_list(nodes):
    dummy = ListNode(0) # 创建头节点，哑节点，不表示真实数位，只用来挂结果链表。
    curr = dummy
    for val in nodes:
        curr.next = ListNode(val) # 创建新节点，并让curr的下一个节点指向新节点
        curr = curr.next # 移动curr到新节点
    return dummy.next # 返回结果链表的头节点

# 打印链表
def print_list(node):
    res = [] # 创建一个空列表，用来存储链表的值
    while node:
        res.append(str(node.val)) # 将当前节点的值转换为字符串（str），并添加到列表中（append）
        node = node.next # 移动node到下一个节点
    print("->".join(res)) # 将列表中的所有元素用"->"连接起来（join），并打印出来

if __name__ == "__main__":
    l1 = build_list([2, 4, 3]) # 根据数组[2, 4, 3]创建链表1
    l2 = build_list([5, 6, 4]) # 根据数组[5, 6, 4]创建链表2
    print("List 1: ", end="")
    print_list(l1) # 打印链表1
    print("List 2: ", end="")
    print_list(l2) # 打印链表2
    result = Solution().addTwoNumbers(l1, l2) # 计算两个链表的和
    print("Result: ", end="")
    print_list(result) # 打印结果链表