import extmem
import random
from math import ceil
from relation import R, S


def generate_data(r, s):
    for i in range(112):
        r.append(R(random.randint(1, 40), random.randint(1, 1000)))

    for i in range(224):
        s.append(S(random.randint(1, 40), random.randint(1, 1000)))


def buffer_busy():
    for i in range(buffer.blockTotalNumber):
        if buffer.data[i][0]:
            print(i)


def write_relation(relation, required_blk, addr):
    for i in range(required_blk):
        blk_num = buffer.getNewBlockInBuffer()  # 申请到的缓冲区的索引
        data = []
        for j in range(7):
            data.extend([str(relation[i * 7 + j].first_attr), str(' '), str(relation[i * 7 + j].second_attr),
                         str(' ')])
        data.append(str(addr + 1))
        if i == required_blk - 1:
            data[-1] = str(0)
        buffer.data[blk_num].append(data)
        if not buffer.writeBlockToDisk(addr, blk_num):
            print("写入磁盘文件号 %s 失败" % addr)
            exit()
        addr += 1
    return addr


def write_data(data_set, required_blk, tuple_number, addr):
    number_of_attr = len(data_set[0])  # 关系的属性数
    for i in range(required_blk - 1):
        blk_num = buffer.getNewBlockInBuffer()  # 申请到的缓冲区的索引
        data = []
        for j in range(tuple_number):
            for k in range(number_of_attr):
                data.extend([str(data_set[i * tuple_number + j][k]), str(' ')])
        data.append(str(addr + 1))
        buffer.data[blk_num].append(data)
        if not buffer.writeBlockToDisk(addr, blk_num):
            print("写入磁盘文件号 %s 失败" % addr)
            exit()
        addr += 1

    number_of_written = (required_blk - 1) * tuple_number  # 已经写入磁盘的数据个数
    blk_num = buffer.getNewBlockInBuffer()
    data = []
    for i in range(len(data_set) - number_of_written):
        for j in range(number_of_attr):
            data.extend([str(data_set[number_of_written + i][j]), str(' ')])
    data.append(str(0))
    buffer.data[blk_num].append(data)
    if not buffer.writeBlockToDisk(addr, blk_num):
        print("写入磁盘文件号 %s 失败" % addr)
        exit()
    addr += 1

    return addr


class RelationSelectionAlgorithm:
    @staticmethod
    def selection_linear(relation, attribute, value, addr):
        if relation != 'R' and relation != 'S':
            print("关系名称错误")
            return addr

        # 看选择的属性是第一个属性还是第二个属性
        if attribute == 'A' or attribute == 'C':
            attr_index = 0
        elif attribute == 'B' or attribute == 'D':
            attr_index = 1
        else:
            print("属性输入错误")
            return addr

        # 首先找到关系的起始文件块号
        relation_start_blk_number = blk_dict[relation]
        present_blk_number = relation_start_blk_number  # 这两行代码是冗余的，但是为了程序易读，我觉得是有必要的
        data = []  # 保存满足条件的元组，会写入到文件块中
        write_blk_index = buffer.getNewBlockInBuffer()  # 为选择的数据申请一个缓冲区
        if write_blk_index == -1:
            print("缓冲区已满，不能为选择的数据申请一个缓冲区")
            return addr

        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 线性搜索
            for i_ in range(int(number_of_tuple)):
                if int(read_data[i_ * 2 + attr_index]) == value:
                    data.append([read_data[i_ * 2], read_data[i_ * 2 + 1]])
                    print("关系", relation, ":", read_data[i_ * 2], read_data[i_ * 2 + 1])

            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            if present_blk_number == '0':
                break

        if len(data) == 0:
            print("没有对应的数据")
            return addr

        addr = write_data(data, int(ceil(len(data) / 7.0)), 7, addr)
        return addr

    @staticmethod
    def selection_binary_search(relation, attribute, value, blk_num):
        if relation != 'R' and relation != 'S':
            print("关系名称错误")
            return blk_num

        # 看选择的属性是第一个属性还是第二个属性
        if attribute == 'A' or attribute == 'C':
            attr_index = 0
        elif attribute == 'B' or attribute == 'D':
            attr_index = 1
        else:
            print("属性输入错误")
            return blk_num

        relation_start_blk_number = blk_dict[relation]
        present_blk_number = relation_start_blk_number  # 这两行代码是冗余的，但是为了程序易读，我觉得是有必要的
        data = []  # 保存满足条件的元组，会写入到文件块中
        write_blk_index = buffer.getNewBlockInBuffer()  # 为选择的数据申请一个缓冲区
        if write_blk_index == -1:
            print("缓冲区已满，不能为选择的数据申请一个缓冲区")
            return blk_num

        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 二分查找
            sort_data = []
            for i in range(int(number_of_tuple)):
                sort_data.append([int(read_data[i * 2]), int(read_data[i * 2 + 1])])
            sort_data = sorted(sort_data, key=lambda t: t[attr_index])
            search_low = 0  # 搜索起始低位置
            search_high = number_of_tuple - 1  # 搜索起始高位置
            while search_low <= search_high:
                search_middle = int((search_high - search_low) / 2 + search_low)
                if sort_data[search_middle][attr_index] == value:
                    data.append(sort_data[search_middle])
                    print("关系", relation, ":", sort_data[search_middle])

                    # 查看是否具有重复项,先看前面的，再看后面的
                    before_index = search_middle - 1  # 前面的
                    while before_index >= 0 and sort_data[before_index][attr_index] == value:
                        data.append(sort_data[before_index])
                        print("关系", relation, ":", sort_data[before_index])
                        before_index -= 1

                    after_index = search_middle + 1  # 后面的
                    while after_index < number_of_tuple and sort_data[after_index][
                        attr_index] == value:
                        data.append(sort_data[after_index])
                        print("关系", relation, ":", sort_data[after_index])
                        after_index += 1
                    # 搜索下个磁盘块
                    break
                elif sort_data[search_middle][attr_index] > value:
                    search_high = search_middle - 1
                else:
                    search_low = search_middle + 1

            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            if present_blk_number == '0':
                break

        if len(data) == 0:
            print("没有对应的数据")
            return blk_num

        blk_num = write_data(data, int(ceil(len(data) / 7.0)), 7, blk_num)
        return blk_num

    def sort_for_index(self, relation, index_table, attr_index, blk_number):
        data = []
        # 首先找到第一个关系的起始文件块号
        present_blk_number = blk_dict[relation]

        # 然后读取第一个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i_ in range(int(number_of_tuple)):
                data.append([int(read_data[i_ * 2]), int(read_data[i_ * 2 + 1])])
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break

        # 先建立好索引，然后再写入磁盘块
        index_blk_number = blk_number
        data = sorted(data, key=lambda t: t[attr_index])
        index_table, index_blk_number = self.create_index(data, attr_index, index_table,
                                                     index_blk_number)

        if len(data) == 0:
            print("没有对应的数据")
            return blk_number

        blk_number = write_data(data, int(ceil(len(data) / 7.0)), 7, blk_number)

        if index_blk_number != blk_number:
            print("索引建的有问题")
            exit()

        return index_table, blk_number

    @staticmethod
    def create_index(data, attr_index, index_table, blk_number):
        index = 0
        while index < len(data):
            if index + 7 < len(data) and data[index][attr_index] < data[index + 7][attr_index]:
                index_table.append([data[index][attr_index], blk_number])
                blk_number += 1
                index += 7
            elif index + 7 < len(data) and data[index][attr_index] == data[index + 7][attr_index]:
                index_table.append([data[index][attr_index], blk_number])
                blk_number += 1
                index += 7
                count = 1
                while index + 7 * count < len(data) and data[index + 7 * count - 1][attr_index] \
                        == data[index + 7 * count][attr_index]:
                    count += 1
                if index + 7 > len(data):
                    blk_number += count
                    break
                else:
                    index += 7 * count
                    blk_number += count
            else:
                index_table.append([data[index][attr_index], blk_number])
                blk_number += 1
                break
        return index_table, blk_number

    def selection_index(self, relation, attribute, value, blk_number):
        if relation != 'R' and relation != 'S':
            print("关系名称错误")
            return blk_number
        # 看选择的属性是第一个属性还是第二个属性
        if attribute == 'A' or attribute == 'C':
            attr_index = 0
        elif attribute == 'B' or attribute == 'D':
            attr_index = 1
        else:
            print("属性输入错误")
            return blk_number

        index_table = []  # 索引表
        index_table, blk_number = self.sort_for_index(relation, index_table, attr_index, blk_number)
        index_table = sorted(index_table, key=lambda t: t[0])

        hit_blk_number = -1  # 找到
        for i in range(len(index_table)):
            if index_table[i][0] == value:
                hit_blk_number = index_table[i][1]
                break
            elif index_table[i][0] < value:
                hit_blk_number = index_table[i][1]
            else:
                break
        if hit_blk_number == -1:
            print("没找到指定记录")
            return blk_number

        present_blk_number = hit_blk_number  # 这两行代码是冗余的，但是为了程序易读，我觉得是有必要的
        data = []  # 保存满足条件的元组，会写入到文件块中
        write_blk_index = buffer.getNewBlockInBuffer()  # 为选择的数据申请一个缓冲区
        if write_blk_index == -1:
            print("缓冲区已满，不能为选择的数据申请一个缓冲区")
            return blk_number

        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 搜索对应元组
            for i in range(int(number_of_tuple)):
                if int(read_data[i * 2 + attr_index]) == value:
                    data.append([int(read_data[i * 2]), int(read_data[i * 2 + 1])])
                    print("关系", relation, ":", read_data[i * 2], read_data[i * 2 + 1])
                elif int(read_data[i * 2 + attr_index]) > value:
                    next_blk_number = '0'
                    break

            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)
            if present_blk_number == '0':
                break

        if len(data) == 0:
            print("没有对应的数据")
            return blk_number

        blk_number = write_data(data, int(ceil(len(data) / 7.0)), 7, blk_number)
        return blk_number


class RelationProjectionAlgorithm:
    @staticmethod
    def project(relation, attribute, blk_number):
        if relation != 'R' and relation != 'S':
            print("关系名称错误")
            return blk_number

        # 看选择的属性是第一个属性还是第二个属性
        if attribute == 'A' or attribute == 'C':
            attr_index = 0
        elif attribute == 'B' or attribute == 'D':
            attr_index = 1
        else:
            print("属性输入错误")
            return blk_number

        # 首先找到关系的起始文件块号
        present_blk_number = blk_dict[relation]
        data = []  # 保存满足条件的元组，会写入到文件块中
        write_blk_index = buffer.getNewBlockInBuffer()  # 为选择的数据申请一个缓冲区
        if write_blk_index == -1:
            print("缓冲区已满，不能为选择的数据申请一个缓冲区")
            return blk_number

        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 投影
            for i in range(int(number_of_tuple)):
                data.append([read_data[i * 2 + attr_index]])
                print("关系", relation, ":", read_data[i * 2 + attr_index])

            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            if present_blk_number == '0':
                break

        if len(data) == 0:
            print("没有对应的数据")
            return blk_number

        blk_number = write_data(data, int(ceil(len(data) / 14.0)), 14, blk_number)
        return blk_number


class JoinOperationAlgorithm:
    @staticmethod
    def nest_loop_join(relation_first, relation_second, blk_numbers_of_first, blk_numbers_of_second,
                       blk_number):
        if blk_numbers_of_first > blk_numbers_of_second:
            out_relation = relation_second
            in_relation = relation_first
        else:
            out_relation = relation_first
            in_relation = relation_second

        # 首先找到外层关系的起始文件块号
        out_present_blk_number = blk_dict[out_relation]
        data = []  # 保存满足条件的元组，会写入到文件块中
        write_blk_index = buffer.getNewBlockInBuffer()  # 为选择的数据申请一个缓冲区
        if write_blk_index == -1:
            print("缓冲区已满，不能为选择的数据申请一个缓冲区")
            return blk_number

        while True:
            out_index = buffer.readBlockFromDisk(out_present_blk_number)  # 为关系的数据申请一个缓冲
            if out_index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            out_read_data = buffer.data[out_index][1]  # 从磁盘块中读取的数据
            out_number_of_tuple = (len(out_read_data) - 1) / 2
            out_next_blk_number = out_read_data[-1]  # 文件的后继磁盘块号

            # 首先找到关系的起始文件块号
            in_present_blk_number = blk_dict[in_relation]  # 这两行代码是冗余的，但是为了程序易读，我觉得是有必要的
            while True:
                in_index = buffer.readBlockFromDisk(in_present_blk_number)
                if in_index == -1:
                    print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                    exit()
                in_read_data = buffer.data[in_index][1]
                in_number_of_tuple = (len(in_read_data) - 1) / 2
                in_next_blk_number = in_read_data[-1]

                for i in range(int(out_number_of_tuple)):
                    for j in range(int(in_number_of_tuple)):
                        if out_read_data[i * 2] == in_read_data[j * 2]:
                            data.append([int(out_read_data[i * 2]), int(out_read_data[i * 2 + 1]),
                                         int(in_read_data[j * 2 + 1])])
                            print('关系', out_relation, '的元组',
                                  [out_read_data[i * 2], out_read_data[i * 2 + 1]],
                                  '和关系', in_relation, '的元组',
                                  [in_read_data[j * 2], in_read_data[j * 2 + 1]], '连接')
                in_present_blk_number = in_next_blk_number
                buffer.freeBlockInBuffer(in_index)
                if in_present_blk_number == '0':
                    break

            out_present_blk_number = out_next_blk_number
            buffer.freeBlockInBuffer(out_index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            if out_present_blk_number == '0':
                break

        if len(data) == 0:
            print("没有对应的数据")
            return blk_number

        blk_number = write_data(data, int(ceil(len(data) / 5.0)), 5, blk_number)
        return blk_number

    @staticmethod
    def sort_merge_join(relation_first, relation_second, blk_number):
        if relation_first != 'R' and relation_first != 'S':
            print("关系名称错误")
            return blk_number
        elif relation_second != 'R' and relation_second != 'S':
            print("关系名称错误")
            return blk_number

        first_data = []
        present_blk_number = blk_dict[relation_first]
        # 然后读取第一个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i in range(int(number_of_tuple)):
                first_data.append([int(read_data[i * 2]), int(read_data[i * 2 + 1])])
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break

        second_data = []
        present_blk_number = blk_dict[relation_second]
        # 然后读取第二个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i in range(int(number_of_tuple)):
                second_data.append([int(read_data[i * 2]), int(read_data[i * 2 + 1])])
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break
        # sort
        first_data = sorted(first_data, key=lambda t: t[0])
        second_data = sorted(second_data, key=lambda t: t[0])

        # merge
        data = []
        i = 0
        j = 0
        while i < len(first_data) or j < len(second_data):
            if i < len(first_data) and j < len(second_data):
                if first_data[i][0] == second_data[j][0]:
                    data.append([first_data[i][0], first_data[i][1], second_data[j][1]])
                    print('关系', relation_first, '的元组', first_data[i],
                          '和关系', relation_second, '的元组', second_data[j], '连接')
                    temp_index = j + 1  # 让第二个关系先移动
                    while temp_index < len(second_data) and first_data[i][0] == \
                            second_data[temp_index][0]:
                        data.append(
                            [first_data[i][0], first_data[i][1], second_data[temp_index][1]])
                        print('关系', relation_first, '的元组', first_data[i],
                              '和关系', relation_second, '的元组', second_data[temp_index], '连接')
                        temp_index += 1
                    i += 1  # 只移动第二个关系不移动第一个关系
                elif first_data[i][0] < second_data[j][0]:
                    i += 1
                elif first_data[i][0] > second_data[j][0]:
                    j += 1
            else:
                break

        if len(data) == 0:
            print("没有对应的数据")
            return blk_number

        blk_number = write_data(data, int(ceil(len(data) / 5.0)), 5, blk_number)
        return blk_number

    @staticmethod
    def hash_join(relation_first, relation_second, number_of_bucket, blk_number):
        if relation_first != 'R' and relation_first != 'S':
            print("关系名称错误")
            return blk_number
        elif relation_second != 'R' and relation_second != 'S':
            print("关系名称错误")
            return blk_number

        # 构造桶
        bucket_of_r = []
        bucket_of_s = []
        for i in range(number_of_bucket):
            bucket_of_r.append([])
            bucket_of_s.append([])

        # 首先找到第一个关系的起始文件块号
        present_blk_number = blk_dict[relation_first]
        # 然后读取第一个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i in range(int(number_of_tuple)):
                bucket_index = (int(read_data[i * 2]) + 2) % number_of_bucket  # hash一下
                bucket_of_r[bucket_index].append([int(read_data[i * 2]), int(read_data[i * 2 + 1])])
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break

        # 首先找到第二个关系的起始文件块号
        present_blk_number = blk_dict[relation_second]
        # 然后读取第二个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i in range(int(number_of_tuple)):
                bucket_index = (int(read_data[i * 2]) + 2) % number_of_bucket  # hash一下
                bucket_of_s[bucket_index].append([int(read_data[i * 2]), int(read_data[i * 2 + 1])])
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break
        # join
        data = []
        for i in range(number_of_bucket):
            for j_ in range(len(bucket_of_r[i])):
                for k_ in range(len(bucket_of_s[i])):
                    if bucket_of_r[i][j_][0] == bucket_of_s[i][k_][0]:
                        data.append(
                            [bucket_of_r[i][j_][0], bucket_of_r[i][j_][1], bucket_of_s[i][k_][1]])
                        print('关系', relation_first, '的元组', bucket_of_r[i][j_], '和关系',
                              relation_second, '的元组',
                              bucket_of_s[i][k_], '连接')

        if len(data) == 0:
            print("没有对应的数据")
            return blk_number

        blk_number = write_data(data, int(ceil(len(data) / 5.0)), 5, blk_number)
        return blk_number


class SetOperationAlgorithm:
    @staticmethod
    def set_operate(relation_first, relation_second, operation, blk_number):
        if relation_first != 'R' and relation_first != 'S':
            print("关系名称错误")
            return blk_number
        elif relation_second != 'R' and relation_second != 'S':
            print("关系名称错误")
            return blk_number

        first_data = []
        # 首先找到第一个关系的起始文件块号
        present_blk_number = blk_dict[relation_first]
        # 然后读取第一个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i in range(int(number_of_tuple)):
                first_data.append([read_data[i * 2], read_data[i * 2 + 1]])
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break

        second_data = []
        # 首先找到第二个关系的起始文件块号
        present_blk_number = blk_dict[relation_second]
        # 然后读取第二个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i in range(int(number_of_tuple)):
                second_data.append([read_data[i * 2], read_data[i * 2 + 1]])
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break

        data = []
        if operation == 'union':  # 并
            union_data = []
            union_data.extend(first_data)
            union_data.extend(second_data)
            # 去重复
            for item in union_data:
                if union_data.count(item) > 1:
                    print("关系", relation_first, '并', relation_second, ":", item[0], item[1])
                    for i in range(union_data.count(item) - 1):
                        union_data.remove(item)
                else:
                    print("关系", relation_first, '并', relation_second, ":", item[0], item[1])
            data = union_data
        elif operation == 'intersect':  # 交
            intersect_data = []
            for item in first_data:
                if item in second_data:
                    intersect_data.append(item)
                    print("关系", relation_first, '交', relation_second, ":", item[0], item[1])
            data = intersect_data
        elif operation == 'except':  # 差
            except_data = []
            for item in first_data:
                if item not in second_data:
                    except_data.append(item)
                    print("关系", relation_first, '差', relation_second, ":", item[0], item[1])
            data = except_data

        if len(data) == 0:
            print("没有对应的数据")
            return blk_number

        blk_number = write_data(data, int(ceil(len(data) / 7.0)), 7, blk_number)

        return blk_number


if __name__ == '__main__':
    blk_number = 0  # 磁盘文件号
    blk_numbers_of_R = 6  # 关系R的磁盘块数
    blk_numbers_of_S = 4  # 关系S的磁盘块数
    blk_dict = {}  # 用于记录关系和关系存放的第一个文件块的编号

    buffer = extmem.Buffer(64, 8)

    # 首先产生数据
    r = []
    s = []
    generate_data(r, s)

    # 将r写入到磁盘中
    # blk_dict['R'] = 0
    print('关系R')
    blk_dict['R'] = blk_number
    blk_number = write_relation(r, blk_numbers_of_R, blk_number)

    # 将s写入到磁盘中
    # blk_dict['S'] = 16
    print('关系S')
    blk_dict['S'] = blk_number
    blk_number = write_relation(s, blk_numbers_of_S, blk_number)

    # 选择操作：线性搜索
    print("线性搜索")
    blk_number = RelationSelectionAlgorithm.selection_linear('R', 'A', 40, blk_number)

    # 选择操作：二分搜索
    print("二分搜索")
    blk_number = RelationSelectionAlgorithm.selection_binary_search('R', 'A', 40, blk_number)

    # 选择操作：索引搜索
    print("索引搜索")
    blk_number = RelationSelectionAlgorithm().selection_index('R', 'A', 40, blk_number)

    # 投影操作
    print("投影操作")
    blk_number = RelationProjectionAlgorithm.project('R', 'A', blk_number)

    # 集合操作
    print("集合操作")
    blk_number = SetOperationAlgorithm.set_operate('R', 'S', 'except', blk_number)

    # nest-loop-join
    print("nest-loop-join", blk_number)
    blk_number = JoinOperationAlgorithm.nest_loop_join('R', 'S', blk_numbers_of_R, blk_numbers_of_S, blk_number)

    # sort_merge_join
    print("sort_merge_join", blk_number)
    blk_number = JoinOperationAlgorithm.sort_merge_join('R', 'S', blk_number)

    # hash_join
    print("hash_join", blk_number)
    blk_number = JoinOperationAlgorithm.hash_join('R', 'S', 5, blk_number)
