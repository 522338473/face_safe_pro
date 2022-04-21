# -*- coding: utf-8 -*-
import math
import uuid as _uu


class ShortUUID:
    """
    生成压缩的UUID，基于https://github.com/skorokithakis/shortuuid修改
    """
    _ALPHABET = list("23456A789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
    _LENGTH = int(math.ceil(math.log(2 ** 128, len(_ALPHABET))))

    @staticmethod
    def int_to_string(number, padding=None):
        """
        Convert a number to a string, using the given alphabet.
        """
        output = ""
        alpha_len = len(ShortUUID._ALPHABET)
        while number:
            number, digit = divmod(number, alpha_len)
            output += ShortUUID._ALPHABET[digit]
        if padding:
            remainder = max(padding - len(output), 0)
            output = output + ShortUUID._ALPHABET[0] * remainder
        return output

    @staticmethod
    def uuid1(pad_length=None):
        """
         生成压缩的UUID1.
        """
        if pad_length is None:
            pad_length = ShortUUID._LENGTH

        uuid = _uu.uuid1()
        return ShortUUID.int_to_string(uuid.int, padding=pad_length)

    @staticmethod
    def uuid4(pad_length=None):
        """
         生成压缩的UUID4.
        """
        if pad_length is None:
            pad_length = ShortUUID._LENGTH

        uuid = _uu.uuid4()
        return ShortUUID.int_to_string(uuid.int, padding=pad_length)


if __name__ == '__main__':
    print(ShortUUID.uuid1())
    print(ShortUUID.uuid4())
