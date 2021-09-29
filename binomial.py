class Binomial:
    def __init__(self, size):
        self.size = size
        self.address = []
        self.tree = []
        self.data = None

        # make address model
        length = 2 ** size - 1
        cnt = 0
        for i in range(size):
            if i == 0:
                n = 0
                while n < length:
                    self.address.append([0])
                    n += 1
                cnt += 1
                continue
            for j in range(2**(i-1)):
                for k in range(2):
                    self.address[cnt].append(k)
                    cnt += 1
            n = cnt
            t = i+1
            while n < length:
                if n < cnt + 2**t / 2:
                    self.address[n].append(0)
                else:
                    self.address[n].append(1)
                n += 1
                if n == cnt + 2**t:
                    t += 1

    def __str__(self):
        if not self.tree:
            tree = 'Not append data'
        else:
            tree = self.tree
        return f'Binomial Object {super().__str__()}\n' + \
               f'Size: {self.size}\n' + \
               f'Address List: {str(self.address)}\n' + \
               f'Address Length: {len(self.address)}\n' + \
               f'Tree Form: {tree}'

    def append(self, data):
        if len(data) != self.size:
            raise MemoryError

        self.data = data
        node_cnt = 0
        cnt = 0
        for arr in data:
            if cnt == 0:
                try:
                    self.tree.append([self.address[cnt], arr[0]])
                except TypeError:
                    self.tree.append([self.address[cnt], arr])
                cnt += 1
                node_cnt += 1
                continue
            if 2**node_cnt != len(arr):
                raise MemoryError
            for i in arr:
                self.tree.append([self.address[cnt], i])
                cnt += 1
            node_cnt += 1
        return 1

    def path(self, node, index):
        if index >= 2**node:
            raise IndexError
        address_idx = 2**node-1+index
        return self.address[address_idx]

    def value(self, node, index):
        address = self.path(node, index)
        for i in self.tree:
            if i[0] == address:
                return i[1]
        return None

    def child(self, node, index):
        parent = self.path(node, index)
        path1 = parent.append(0)
        path2 = parent.append(1)
        children = []
        for i in self.tree:
            if i[0] == path1 or i[0] == path2:
                children.append(i[1])
        return children

    def exchange(self, node, index, value):
        address = self.path(node, index)
        i = 0
        while i < len(self.tree):
            if self.tree[i][0] == address:
                self.tree[i][1] = value
                self.data[node][index] = value
                return
            i += 1


def model(tree):
    bi = Binomial(len(tree))
    bi.append(tree)
    return bi


if __name__ == "__main__":
    irm = [
        0.0174,
        [0.0339, 0.0095],
        [0.05, 0.0256, 0.0011]
    ]
    b = Binomial(3)
    print(b)
    a = model(irm)
    print(a)
