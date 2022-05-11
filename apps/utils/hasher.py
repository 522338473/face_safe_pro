# -*- coding: utf-8 -*-
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
        return cls.base36.hash("%(object_pk)d" % {"object_pk": object_pk})

    @classmethod
    def to_object_pk(cls, obj_hash):
        un_hashed = "%d" % cls.base36.unhash(obj_hash)
        object_pk = int(un_hashed)
        return object_pk
