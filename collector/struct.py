
from typing import List
import pandas as pd


# Table数据结构 列族
class TableColFamily:
    FAMILY_NAME = None
    COL_FIELDS: List[str] = []

    def __init__(self):
        for field in self.COL_FIELDS:
            attr_name = self.get_attr_name(field)
            setattr(self, attr_name, '')

    # 通过对象[key]方式访问
    def __getitem__(self, key):
        attr_name = self.get_attr_name(key)
        if hasattr(self, attr_name):
            return getattr(self, attr_name)
        else:
            raise ValueError(f"{attr_name} does not exist")

    # 通过对象[key] 方式赋值
    def __setitem__(self, key, value):
        attr_name = self.get_attr_name(key)
        setattr(self, attr_name, value)

    # 通过字段名称映射对应属性名
    def get_attr_name(self, field_name: str) -> str:
        field_name = field_name.strip()
        if self.FAMILY_NAME is None:
            attr_name = f"_{field_name}"
        else:
            family_name = str(self.FAMILY_NAME).strip()
            attr_name = f"_{family_name}_{field_name}"
        return attr_name

    def to_dict(self) -> dict:
        dict_tmp = {}
        for field in self.COL_FIELDS:
            dict_tmp[field] = self[field]
        return dict_tmp


# Table数据结构 行数据
class TableRowData:
    def __init__(self, **kwargs):
        self._source = kwargs
        # 支持多个列族
        self.families: List[TableColFamily] = []

    def to_dict(self) -> dict:
        dict_tmp = {}
        for family in self.families:
            dict_tmp.update(family.to_dict())
        return dict_tmp

    def get_value(self, name, default_value=""):
        value = self._source.get(name, default_value)
        if value is None:
            value = default_value
        return value


class TableData:

    def __init__(self, data: list = None):
        self._data = [] if data is None else data
        self.func_check_row_data = None
        self.func_handler_row_data = None
        self.data = []

    def pares_data(self):
        if isinstance(self._data, list):
            for i, data in enumerate(self._data):
                if self.func_check_row_data is not None:
                    self.func_check_row_data(data)
                if self.func_handler_row_data is not None:
                    pares_row_data = self.func_handler_row_data(data, i)
                    self.data.extend(pares_row_data)

        elif isinstance(self._data, pd.DataFrame):
            for i, row in self._data.iterrows():
                data = row.to_dict()
                if self.func_check_row_data is not None:
                    self.func_check_row_data(dict(data))
                if self.func_handler_row_data is not None:
                    pares_row_data = self.func_handler_row_data(dict(data), i)
                    self.data.extend(pares_row_data)


class MapTableColFamily(TableColFamily):
    FAMILY_NAME = 'MapTable'
    COL_FIELDS = [
        'MapKey',
        'MapValue',
        'MapSrc',
    ]
