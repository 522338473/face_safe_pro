# -*- coding: utf-8 -*-
import uuid

import basehash


class Hasher:
    """
    对数据库ID进行散列化计算
    """

    base36 = basehash.base62(11)

    @classmethod
    def from_model(cls, obj):
        if obj.pk is None:
            return None
        return cls.make_hash(obj.pk)

    @classmethod
    def make_hash(cls, object_pk):
        """
        数据库模型整型ID改为UUID4
        """
        if isinstance(object_pk, int):
            return cls.base36.hash("%(object_pk)d" % {"object_pk": object_pk})
        elif isinstance(object_pk, uuid.UUID):
            return str(object_pk)
        else:
            return object_pk

    @classmethod
    def to_object_pk(cls, obj_hash):
        """
        数据库模型整型ID改为UUID4
        """
        if cls.check_uuid4(obj_hash):
            if isinstance(obj_hash, str):
                return uuid.UUID(obj_hash)
            else:
                return uuid.UUID(str(obj_hash))
        else:
            if not isinstance(obj_hash, uuid.UUID):
                un_hashed = "%d" % cls.base36.unhash(obj_hash)
                object_pk = int(un_hashed)
                return object_pk

    @staticmethod
    def check_uuid4(u_str, version=4):
        """检验字符串是否为UUID4"""
        try:
            return uuid.UUID(u_str).version == version
        except ValueError:
            return False
