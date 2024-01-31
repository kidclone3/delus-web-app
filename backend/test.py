# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if left == right:
            return head

        cur = head
        idx = 1

        def reverse(node_head, length):

            new_head, new_tail = None, None
            cur = node_head
            while length >= 0:
                new_cur = None
                if new_head is None:
                    new_head = cur
                    new_cur = cur.next
                elif new_tail is None:
                    new_tail = new_head
                    new_cur = cur.next
                    new_head = cur
                    new_head.next = new_tail
                else:
                    new_cur = cur.next
                    cur.next = new_head
                    new_head = cur
                cur = new_cur
                length -= 1
            if new_tail == None:
                new_tail = new_head
            return new_head, new_tail, cur

        if left == 1:
            new_head, new_tail, cur = reverse(head, right - left+1)
            new_tail.next = cur
            return new_head
        else:
            old_node = None
            while cur:
                if left == idx:
                    new_head, new_tail, cur = reverse(cur, right - left)
                    new_tail.next = cur
                    old_node.next = new_head
                    return head
                idx += 1
                old_node = cur
                cur = cur.next
        return None
def print_list(head):
    cur = head
    while cur:
        print(cur.val, end=" ")
        cur = cur.next
    print()
if __name__ == "__main__":
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    left = 2
    right = 4

    print(print_list(Solution().reverseBetween(head, left, right)))
    print("hello")
    print("hello2")
    # print(Solution().reverseBetween(head, left, right))