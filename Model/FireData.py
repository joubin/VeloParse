from Model.Laser import Laser
from Parser.Parse import next_bytes, get_int_value
import binascii


class FireData(object):
    """
    Based on Appendix B
    http://velodynelidar.com/docs/manuals/63-9113%20HDL-32E%20manual_Rev%20H_Sept.pdf

    FireData has the the block_id and rotation along with an Array of 32 @Laser objects
    """

    def __init__(self, block_id, rotation, lasers):
        """

        :param block_id: the actual id
        :param rotation: the rotational angle
        :param lasers: an array of 32 @Laser objects
        :return:
        """
        self.block_id = block_id
        self.rotation = rotation
        self.lasers = lasers

    def __str__(self):
        """

        :return: a human readable string
        """
        result = "block id: " + str(self.block_id) \
                 + " rotation: " + str(self.rotation) \
                 + " lasers:[ "
        for i in self.lasers:
            result += " { "
            result += str(i)
            result += " } "
        result += " ] "
        return result

    def __repr__(self, *args, **kwargs):
        """
        calls the __str__ so that it prints correctly within the list
        :param args:
        :param kwargs:
        :return:
        """
        return self.__str__()

    @classmethod
    def create_with_date(cls, data):
        """

        :param data: is the raw 1200 bytes of the udp packet
        :return: a constructed class
        """
        try:
            data, rotation = next_bytes(data, 2)
            data, block_id = next_bytes(data, 2)
            # print(rotation)
            rotation = get_int_value(rotation)
            block_id = get_int_value(block_id)
            # rotation = str(rotation)
            # print(block_id)
            lasers = []
            for i in range(32):
                data, distance = next_bytes(data, 2)
                data, intensity = next_bytes(data, 1)
                tmp = Laser.create_from_hex_data(distance, intensity)
                lasers.append(tmp)

            return cls(block_id, rotation, lasers)
        except ValueError as ve:
            return None


