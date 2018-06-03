import os


def dropBlockOnDisk(addr):
    """
    从磁盘上删除地址为addr的磁盘块内的数据。
    :return:若删除成功，则返回True；否则，返回False。
    """
    filename = "%s.blk" % addr
    if os.path.exists(filename):
        os.remove(filename)
        print("删除成功")
        return True
    print("删除失败")
    return False


class Buffer:
    def __init__(self, buf_size, blk_size):
        """
        初始化
        """
        self.ioCounter = 0
        self.bufferSize = buf_size
        self.blockSize = blk_size
        self.blockTotalNumber = buf_size / blk_size
        self.blockFreeNumber = self.blockTotalNumber
        self.data = []
        for i in range(int(self.blockTotalNumber)):
            self.data.append([False])

    def __del__(self):
        print("缓冲区已释放")

    def getNewBlockInBuffer(self):
        if self.blockFreeNumber == 0:
            print("Buffer is full!")
            return -1

        for i in range(int(self.blockTotalNumber)):
            if not self.data[i][0]:
                self.data[i][0] = True
                self.blockFreeNumber -= 1
                return i

    def freeBlockInBuffer(self, index):
        self.data[index] = [False]
        self.blockFreeNumber += 1

    def readBlockFromDisk(self, addr):
        if self.blockFreeNumber == 0:
            print("缓存区已满")
            return -1

        index = 0
        for i in range(int(self.blockTotalNumber)):
            if not self.data[i][0]:
                index = i

        filename = "%s.blk" % addr
        f = open(filename)
        if not f:
            print("打开文件失败")
            return -1

        self.data[index] = [True]
        self.blockFreeNumber -= 1
        self.ioCounter += 1

        data = []
        lines = f.readlines()
        for line in lines:
            line = line.split()  # 去掉blk文件中的空格
            data.extend(line)

        self.data[index].append(data)
        f.close()
        return index

    def writeBlockToDisk(self, addr, index):
        filename = "%s.blk" % addr
        f = open(filename, 'w')

        if not f:
            print("打开文件失败")
            return False

        f.writelines(self.data[index][1])
        f.close()
        self.data[index] = [False]  # 写入后该块释放
        self.blockFreeNumber += 1
        self.ioCounter += 1
        return True
