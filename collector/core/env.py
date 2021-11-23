from typing import Any


class Env:
    def __init__(self, tag: str = ''):
        self.tag = tag

    # 通过对象[key]方式访问
    def __getitem__(self, key: str):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise ValueError(f"{key} does not exist")

    # 通过对象[key]方式赋值
    def __setitem__(self, key: str, value: Any):
        setattr(self, key, value)

    def exist(self, key: str):
        if hasattr(self, key):
            return True
        else:
            return False

    def get(self, key: str, default: Any):
        if self.exist(key):
            return getattr(self, key)
        else:
            return default
