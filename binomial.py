class Binomial:
    def __init__(self, size):
        self.size = size
        self.address = []
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
        return f'Size: {self.size}\n' + \
               f'Address List: {str(self.address)}\n' + \
               f'Address Length: {len(self.address)}'

    # def append(self, ):


if __name__ == "__main__":
    b = Binomial(4)
    print(b)
