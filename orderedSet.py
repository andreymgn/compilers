from collections import OrderedDict


class OrderedSet:
    def __init__(self, values):
        self.s = OrderedDict()
        for v in values:
            self.s[v] = None

    def contains(self, value):
        return value in self.s

    def add(self, value):
        self.s[value] = None

    def union(self, rhs):
        result = OrderedSet([])
        for v in self.s:
            result.add(v)
        for v in rhs.s:
            result.add(v)
        return result

    def __or__(self, rhs):
        return self.union(rhs)

    def __iter__(self):
        return self.s.__iter__()

    def __next__(self):
        return self.s.next()

    def __eq__(self, rhs):
        return self.s == rhs.s

    def __len__(self):
        return len(self.s)
