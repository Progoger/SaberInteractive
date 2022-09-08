# coding=utf-8
class ListNode:
    def __init__(self, data=None, prev=None, next=None, rand=None):
        self.data = data
        self.prev = prev
        self.next = next
        self.rand = rand


class ListRand:
    def __init__(self):
        self._head = ListNode()
        self._tail = ListNode()
        self._count = 0

    def __str__(self):
        """
        Вывод списка
        :return:
        """
        tmp1 = self._head
        tmp2 = self._tail
        if not tmp1.data:
            return '[]'
        elif tmp1 == tmp2:
            return '[' + str(tmp1.data) + ']'
        else:
            res1 = ''
            res2 = ''
            while tmp1 != tmp2 and (tmp1.prev is None or tmp1.prev != tmp2):
                res1 = ', ' + str(tmp1.data) + res1
                res2 = res2 + str(tmp2.data) + ', '
                tmp2 = tmp2.prev
                tmp1 = tmp1.next

            if tmp1 == tmp2:
                res1 = str(tmp1.data) + res1
            elif tmp1.prev == tmp2:
                res1 = res1[2:]
            return '[' + res2 + res1 + ']'

    def add_h(self, data):
        """
        добавление с головы
        :param data:
        :return:
        """
        if not self._head.data:
            self._head.data = data
            self._tail = self._head
        elif self._head == self._tail:
            self._head = ListNode(data, next=self._tail)
            self._tail.prev = self._head
        else:
            tmp = self._head
            self._head = ListNode(data, next=tmp)
            tmp.prev = self._head
        self._count += 1

    def add_t(self, data):
        """
        Добавление с хвоста
        :param data:
        :return:
        """
        if not self._head.data:
            self._head.data = data
            self._tail = self._head
        elif self._head == self._tail:
            self._tail = ListNode(data, prev=self._head)
            self._head.next = self._tail
        else:
            tmp = self._tail
            self._tail = ListNode(data, prev=tmp)
            tmp.next = self._tail
        self._count += 1

    def pop_h(self):
        """
        Получение элемента с головы
        :return:
        """
        res = self._head
        if self._tail == self._head:
            self._tail = ListNode()
            self._head = ListNode()
        else:
            self._head = self._head.next
            self._head.prev = None
        return res

    def pop_t(self):
        """
        Получение элемента с хвоста
        :return:
        """
        res = self._tail
        if self._tail == self._head:
            self._tail = ListNode()
            self._head = ListNode()
        else:
            self._tail = self._tail.prev
            self._tail.next = None
        return res

    def get_elem_by_index(self, i):
        """
        Получение элемента по индексу
        :param i:
        :return:
        """
        if i < 0 or i >= self._count:
            raise Warning('Index out of range')
        else:
            if self._count/2 > i:
                tmp_count = 0
                tmp = self._head
                while tmp_count != i:
                    tmp = tmp.next
                    tmp_count += 1
                return tmp
            else:
                tmp_count = self._count-1
                tmp = self._tail
                while tmp_count != i:
                    tmp = tmp.prev
                    tmp_count -= 1
                return tmp

    def serialize(self, file):
        """
        Система в файле такова:
        индекс элемента, значение элемента, (индекс элемента по случайной ссылке/или '')
        :param file:
        :return:
        """
        tmp1 = self._head
        tmp2 = self._tail
        f = open(str(file)+".txt", 'w')
        if not tmp1.data:
            f.write('')
        elif tmp1 == tmp2:
            if tmp1.rand:
                f.write('0,' + str(tmp1.data) + ',0,')
            else:
                f.write('0,' + str(tmp1.data)+',')
        else:
            tmp_count = 0
            rand = {}
            while tmp_count < self._count / 2:# Заходим с двух концов, чтобы ускорить метод
                rand[tmp1] = tmp_count
                rand[tmp2] = self._count-1-tmp_count
                tmp2 = tmp2.prev
                tmp1 = tmp1.next
                tmp_count += 1

            if self._count % 2 != 0:
                rand[tmp1] = tmp_count

            for key, value in rand.items():
                if key.rand:
                    f.write(str(value) + ',' + str(key.data) + ',' + str(rand[key.rand]) + ',\n')
                else:
                    f.write(str(value) + ',' + str(key.data) + ',,\n')
        f.close()

    def deserialize(self, file):
        """
        Структура словаря, который заполняем, а затем по нему воссоздаём список:
        key - индекс элемента
        value - кортеж(экземпляр класса ListNode, индекс элемента по случайной ссылке/или '')
        экземпляр класса ListNode в кортеже первоначально хранит только значение
        :param file:
        :return:
        """
        f = open(str(file)+".txt", "r")
        rand = {}
        for line in f:
            elems = line.split(',')
            rand[int(elems[0])] = (ListNode(data=elems[1]), elems[2])
        f.close()
        self._count = len(rand)
        if len(rand) == 1:
            self._head = rand[0][0]
            if rand[0][1]:
                self._head.rand = self._head
            self._tail = self._head
        elif len(rand) > 1:
            self._head = rand[0][0]
            if rand[0][1]:
                self._head.rand = rand[int(rand[0][1])][0]
            self._tail = rand[self._count-1][0]
            if rand[self._count-1][1]:
                self._head.rand = rand[int(rand[self._count-1][1])][0]
            tmp1 = self._head
            tmp2 = self._tail

            tmp_count = 0
            while tmp_count < self._count / 2:
                tmp1.next = rand[tmp_count][0]
                if rand[tmp_count][1]:
                    tmp1.rand = rand[int(rand[tmp_count][1])][0]
                tmp2.prev = rand[self._count-tmp_count-1][0]
                if rand[self._count-tmp_count-1][1]:
                    tmp2.rand = rand[int(rand[tmp_count][1])][0]
                tmp1.next.prev = tmp1
                tmp2.prev.next = tmp2
                tmp1 = tmp1.next
                tmp2 = tmp2.prev
                tmp_count += 1
            if self._count % 2 == 0:
                tmp1.next = tmp2
                tmp2.prev = tmp1
            else:
                tmp1.next = rand[tmp_count][0]
                tmp2.prev = rand[tmp_count][0]
                rand[tmp_count][0].next = tmp2
                rand[tmp_count][0].prev = tmp1
                if rand[tmp_count][1]:
                    rand[tmp_count][0].rand = rand[int(rand[tmp_count][1])][0]


L = ListRand()
# L.add_t(2)
# L.add_t(5)
# L.add_t(3)
# L.add_t(1)
# L.add_t(7)
# L.add_t(6)

print(L)
# L.get_elem_by_index(0).rand = L.get_elem_by_index(0)
L.serialize('data1')
A = ListRand()
A.deserialize('data1')
print(A)
A.serialize('data2')
