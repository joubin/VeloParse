import binascii

import time
from pcapfile import savefile

from Model import FireData


def next_bytes(the_bytes, num):
    if len(the_bytes) < num:
        raise ValueError("The number requested is too large. Best I can do is: " + str(len(the_bytes)))
    return the_bytes[num:], the_bytes[0:num]


def get_int_value(my_str):
    def custom_unpack(my_str):
        my_str = binascii.hexlify(my_str).decode()
        my_str = ''.join(reversed([my_str[i:i + 2] for i in range(0, len(my_str), 2)]))
        try:
            return int(my_str, 16)
        except TypeError as err:
            print(err.__traceback__())
            exit(10)

    def with_unpack(my_str):
        import struct
        return struct.unpack("<L", my_str)

    return custom_unpack(my_str)


def get_rgb_by_int(rgb_int):
    """
    given an integer, get it on the scale from rbg
    :param rgb_int:
    :return:
    """
    return rgb_int & 255, (rgb_int >> 8) & 255, (rgb_int >> 16) & 255


def do_pcap_stuff():
    testcap = open('../test.pcap', 'rb')
    capfile = savefile.load_savefile(testcap, verbose=False)
    testcap.close()
    fire_data_collection = []
    for cap in capfile.packets:
        try:
            packet, header = next_bytes(cap.raw(), 42)
            packet, payload = next_bytes(packet, 1206)
            packet, block_fire_data = next_bytes(payload, 1200)
            fire_data = []
            for i in range(12):
                block_fire_data, data = next_bytes(block_fire_data, 100)
                fire_data.append(FireData.FireData.create_with_date(data))
            fire_data_collection.append(fire_data)
        except ValueError:
            pass

            # print(fire_data)

    return fire_data_collection
    # for fd in fire_data_collection:
    #     for fd2 in fd:
    #         print(fd2)


def make_image(data=None):
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np
    # data = [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]
    if data is not None:
        plt.imsave('filename.png', data)
    else:
        plt.imsave('filename.png', np.arange(1 * 2048).reshape(1, 2048))


def make_image2(data=None):
    from PIL import Image
    import numpy as np
    data = np.arange(1 * 2048).reshape(1, 2048)
    print(data)
    img = Image.fromarray(data, 'RGB')
    img.save('my.png')


def read_from_file(filename, limit=None):
    with open(filename, 'rb') as myFile:
        lists2 = pickle.load(myFile)
    if limit is None:
        return lists2
    else:
        return lists2[0:limit]


def save_to_file(content_to_write, file_path):
    with open(file_path, 'wb') as myFile:
        pickle.dump(content_to_write, myFile)


def make_small_cached_file(lists2):
    with open("dat2", 'wb') as myFile:
        pickle.dump(lists2[0:1000], myFile)


if __name__ == '__main__':
    import pickle
    import numpy as np

    content = read_from_file("dat2", 1000)
    print(len(content))



    # lists = None
    # with open("dat2", 'rb') as myFile:
    #     lists = pickle.load(myFile)
    #
    # new_list = []
    # for one_of_twelve in lists:
    #     this_group = []
    #     for group in one_of_twelve:
    #         if group is not None:
    #             # print(len(group.lasers))
    #             for laser in group.lasers:
    #                 this_group.append(get_rgb_by_int(laser.intensity))
    #     new_list.append(this_group)
    # new_list = np.array(new_list).reshape(1, len(new_list))
    #
    # print(len(new_list))
    # for i in new_list:
    #     for x in i:
    #         if len(x) != 384:
    #             if len(x) == 1 or x is None:
    #                 print(x)
    #                 print("butt fucker")
    #             for s in range(384 - len(x)):
    #                 x.append(get_rgb_by_int(0))
    # for i in new_list:
    #     for x in i:
    #         if len(x) != 384 and x is not None:
    #             print(len(x))
    #             del (x)
    # for i in new_list:
    #     for x in i:
    #         if len(x) == 384:
    #             for s in x:
    #                 print(len(s))
    # # print(np.array(new_list))
    #
    #
    # # make_image(new_list)
    #
    # # np.array(new_list).reshape(len(new_list), 1)
