class ListNode:
    def __init__(self, value=None, prev=None, next=None, rand=None):
        self.data = value
        self.prev = prev
        self.next = next
        self.rand = rand


class ListRand:
    def __init__(self):
        self._head = ListNode()
        self._tail = ListNode()
        self._count = 0

    def __str__(self):
        tmp = self._head
        if not tmp.value:
            return '[]'
        res = ']'
        while tmp:
            res = ', ' + str(tmp.value) + res
            tmp = tmp.link
        res = '[' + res[2:]
        return res

    def add_l(self, value):
        if not self._head.value:
            self._head.value = value
        else:
            tmp = self._head
            self._head = ListNode(value, tmp)
            # prev = self._head
            # tmp = prev.link
            # while tmp:
            #     prev = tmp
            #     tmp = prev.link
            # tmp = Node(value)
            # prev.link = tmp


# L = SinglyLinkedList()
# L.add(2)
# L.add(5)
# L.add(3)
# print(L)
#
# print([2, 5, 3])
