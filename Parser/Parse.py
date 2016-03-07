#!/usr/bin/env python
"""
This file is the main for this project. It houses some helper functions.

The purpose of this project is to parse and visualize velodyne lidar readout
"""
import binascii
import pickle

import numpy as np
import sys

sys.path.append("..")  # To add the following two
from pcapfile import savefile
from Model import FireData

__author__ = "Joubin Jabbari"
__copyright__ = "Copyright 2016. Joubin Jabbari : jabbari.io"
__credits__ = []
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Joubin Jabbari"
__email__ = "joubin.j@gmail.com"
__status__ = "Development"


def next_bytes(the_bytes: bytes, num: int) -> (object, object):
    # TODO right now this throws an error if there arent enough bytes to get
    # However, this was a design choice because numpy wont allow me to create an image with missing bytes
    # This is most likely going to create a bug.
    # Look into why this would be the case.
    if len(the_bytes) < num:
        raise ValueError("The number requested is too large. Best I can do is: " + str(len(the_bytes)))
    return the_bytes[num:], the_bytes[0:num]


def get_int_value(my_str: bytes) -> int:
    # TODO replace this with the stuct.unpack with formatting for bytes of len 1,2 and 3. It already supports pairs of 4
    def custom_unpack(the_str):
        the_str = binascii.hexlify(the_str).decode()
        the_str = ''.join(reversed([the_str[i:i + 2] for i in range(0, len(the_str), 2)]))
        try:
            return int(the_str, 16)
        except TypeError as err:
            print(err.__traceback__())
            exit(10)

    def with_unpack(the_str) -> object:
        import struct
        return struct.unpack("<L", the_str)

    return custom_unpack(my_str)


def get_rgb_by_int(rgb_int: int) -> (int, int, int):
    """
    given an integer, get it on the scale from rbg
    :param rgb_int:
    :return:
    """
    return rgb_int & 255, (rgb_int >> 8) & 255, (rgb_int >> 16) & 255


def read_pcap_raw(my_pcap_file: str = '../test.pcap') -> [FireData]:
    """
    reads the pcap file and get raw content from it
    :param my_pcap_file:
    :return:
    """
    testcap = open(my_pcap_file, 'rb')
    capfile = savefile.load_savefile(testcap, verbose=False)
    testcap.close()
    fire_data_collection = []
    for cap in capfile.packets:
        try:
            packet, header = next_bytes(cap.raw(), 42)
            packet, payload = next_bytes(packet, 1206)
            packet, block_fire_data = next_bytes(payload, 1200)
            # fire_data = []
            for i in range(12):
                block_fire_data, data = next_bytes(block_fire_data, 100)
                fire_data_collection.append(FireData.FireData.create_with_date(data))
                # fire_data_collection.append(fire_data)
        except ValueError:
            # TODO this value error is caused because of packets being not containing
            # exactly what the documentation claims
            # FIX later
            pass

    return fire_data_collection


def make_image(data: list = None, image_name: str = "filename.png") -> None:
    import matplotlib.pyplot as plt
    if data is not None:
        plt.imsave(image_name, data)
    else:
        plt.imsave(image_name, np.arange(1 * 2048).reshape(1, 2048))


def make_image2(data: list = None, image_name: str = "filename.png") -> None:
    from PIL import Image
    if data is None:
        data = np.arange(1 * 2048).reshape(1, 2048)
    img = Image.fromarray(data)
    img.save(image_name)


def read_from_file(filename: str, limit: int = None) -> [FireData]:
    with open(filename, 'rb') as myFile:
        lists2 = pickle.load(myFile)
    if limit is None:
        return lists2
    else:
        return lists2[0:limit]


def save_to_file(content_to_write: [FireData], file_path: str):
    with open(file_path, 'wb') as myFile:
        pickle.dump(content_to_write, myFile)


# def make_small_cached_file(lists2):
#     with open("dat2", 'wb') as myFile:
#         pickle.dump(lists2[0:1000], myFile)


if __name__ == '__main__':
    contents = read_from_file('bin.min.dat')
    new_contents = []
    # print(type(contents))
    for content in contents:
        new_contents.append(content.lasers)

    result = np.array(new_contents).reshape(32, 1000)

    for idx, item in enumerate(result):
        for other_idx, other_item in enumerate(item):
            result[idx][other_idx] = other_item.intensity

    make_image(result)

    # print(result.shape)
    # print(result[0])
    # for item in result:
    #     print(item)

    # make_image2(result)

    # print(len(content))
    # content = read_from_file("dat2", 1000)
    # # print(len(content))
    # print(type(content))
    # for i in content:
    #     print(type(i))
    #     for x in i:
    #         print(type(x))
    #         exit(0)
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
