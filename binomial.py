class Binomial:
    def __init__(self, size, first_data):
        self.size = size
        self.first_data = first_data
        self.last_node = 0
        self.tree = [first_data]

    def append(self, num, data):
        if self.last_node == 0:
            print("Cannot append")
            return
        self.tree[num].append(data)

    def forward(self):
        if self.last_node == self.tree.list_size:
            raise MemoryError
        self.tree.insertFirst([])

    def select(self, num):
        self.tree.selectNode(num)

    def size():
        return self.size


if __name__ == "__main__":
    bi = Binomial(3, 1.74)
    bi.forward()
    bi.append(3.39)

