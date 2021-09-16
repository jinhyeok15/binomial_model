class Binomial:
    def __init__(self, size):
        self.size = size
        self.address = []
        self.tree = {}
        # make address model
        cnt = 0
        for i in range(size):
            length = 2**size-1
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
                while n < length:
                    if n < cnt + (length - cnt) / 2:
                        self.address[n].append(0)
                    else:
                        self.address[n].append(1)
                    n += 1

    def __str__(self):
        if self.tree == {}:
            tree = 'Not append data'
        else:
            tree = self.tree
        return f'Binomial Object {self.__class__}\n' + \
               f'Size: {self.size}\n' + \
               f'Address List: {str(self.address)}\n' + \
               f'Address Length: {len(self.address)}\n' + \
               f'Tree Form: {tree}'

    def append(self, data):
        if len(data) != self.size:
            raise MemoryError
        cnt = 0
        for arr in data:
            if cnt == 0:
                self.tree[arr] = self.address[cnt]
                cnt += 1
                continue
            for i in arr:
                self.tree[i] = self.address[cnt]
                cnt += 1
        return 1

    def path(self, node, index):
        if index >= 2**node:
            raise IndexError
        address_idx = 2**node-1+index
        return self.address[address_idx]

    def value(self, node, index):
        address = self.path(node, index)
        for key, value in self.tree.items():
            if address == value:
                return key
        return None


if __name__ == "__main__":
    irm = [
        0.0174,
        [0.0339, 0.0095]
    ]
    b = Binomial(2)
    print(b)
    b.append(irm)
    print(str(b.tree))
    print(b.value(0, 0))
    print(b.value(1, 0))
