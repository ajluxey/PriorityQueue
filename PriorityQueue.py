# он добавляет несравниваемые элементы в очередь и только потом понимает что не может сравнить, а очередь уже испорчена
import abc


class Comparator(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def compare(el1, el2):
        pass


class IsElementLarger(Comparator):
    @staticmethod
    def compare(el1, el2):
        return el1 > el2


class PriorityQueue:
    def __init__(self, lst=None, comparator=None):
        if lst and not isinstance(lst, list):
            raise TypeError('Passed argument is not list object')

        if comparator and not isinstance(comparator, Comparator):
            raise TypeError('Passed comparator should inherit Comparator class')

        self._queue = []
        self._comparator = comparator if comparator else IsElementLarger()

        if lst:
            self._built_heap(lst)

    @property
    def height(self):
        h = 0
        max_els_in_heap_h = 0
        while self.length > max_els_in_heap_h:
            max_els_in_heap_h += 2 ** h
            h += 1
        return h

    @property
    def is_empty(self):
        return not self._queue

    @property
    def length(self):
        return len(self._queue)

    def _built_heap(self, lst):
        def type_check(o):
            first = type(lst[0])
            return isinstance(o, first)

        if not all(map(type_check, lst)):
            raise TypeError('All elements must be same type')

        for el in lst:
            self.push(el)

    def _is_larger(self, el1, el2):
        return self._comparator.compare(el1, el2)

    def print_heap(self):
        if self.length < 1:
            return

        print('Tree:')
        h = self.height
        max_size = len(str(max(self._queue)))
        index = 0

        for i in range(h):
            for j in range(1, 2**i + 1):
                if index >= len(self._queue):
                    break
                interval = (2**(h - i) - 1) * max_size
                if j == 1:
                    print(' ' * int(interval/2), end='')
                else:
                    print(' ' * interval, end='')
                current_print = str(self._queue[index])
                index += 1
                if len(current_print) < max_size:
                    current_print += ' '
                print(current_print, end='')
            print()
            if index > len(self._queue):
                break
        print()

    def pop(self):
        if self.is_empty:
            raise IndexError('pop from empty queue')

        if self.length > 1:
            answer = self._queue[0]
            self._queue[0] = self._queue.pop()
            self._sifting_from_up_to_down()
            return answer
        else:
            return self._queue.pop()

    def push(self, el):
        self._queue.append(el)
        self._sifting_from_down_to_up()

    def _sifting_from_up_to_down(self):
        # parent = i, daughters = i*2 + 1; i*2 + 2
        max_index = self.length - 1
        index = 0

        while index <= max_index:
            large = index
            left = index * 2 + 1
            right = index * 2 + 2

            if max_index >= left and self._is_larger(self._queue[left], self._queue[large]):
                large = left
            if max_index >= right and self._is_larger(self._queue[right], self._queue[large]):
                large = right
            if index != large:
                self._queue[large], self._queue[index] = self._queue[index], self._queue[large]
                index = large
            else:
                break

    def _sifting_from_down_to_up(self):
        # parent = i, daughters = i*2 + 1; i*2 + 2
        index = self.length - 1
        while index > 0:
            parent = int((index - 1) / 2)
            if self._is_larger(self._queue[index], self._queue[parent]):
                self._queue[index], self._queue[parent] = self._queue[parent], self._queue[index]
                index = parent
            else:
                break
