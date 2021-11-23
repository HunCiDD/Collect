import copy
from typing import Any
from hashlib import sha256
from enum import Enum


# 生成信息Info的唯一标识uuid
class UUIDInfo:
    def __init__(self, hash_value):

        self._hash_value = hash_value
        self._uuid = sha256(f'{self._hash_value}'.encode()).hexdigest()

    @property
    def hash_value(self):
        return self._hash_value

    @property
    def uuid(self):
        return self._uuid


# 链接信息
class ConnectInfo(UUIDInfo):
    def __init__(self, host_name: str, port: str, **kwargs):
        self._host_name = host_name                    # 主机域名或IP
        self._port = port                              # 主机端口
        self._username = kwargs.get('username')        # 主机登录用户名
        self._password = kwargs.get('password')        # 主机登录密码
        super().__init__(f'{self._host_name}:{self._port}:{self._username}')

    @property
    def host_name(self):
        return self._host_name

    @property
    def port(self):
        return self._port

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password


# 命令信息
class CommandInfo(UUIDInfo):
    OPTION_START_TAG = '#['
    OPTION_END_TAG = ']'

    def __init__(self, index: str = '0',
                 category: str = '',
                 option: str = '',
                 content: str = '',
                 params: dict = None):
        self.index = index
        self.category = category
        self._option = option
        self._content = content.strip()
        self._params = params  # 命令参数
        if self._params is None:
            self._params = {}
        # 根据文本内容进行hash计算
        super().__init__(f"{self._content}:{self._params}")
        self.option_map = self._option_map()

    @property
    def option(self):
        return self._option

    @option.setter
    def option(self, value):
        if isinstance(value, str):
            self._option = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value: str):
        self._content = str(value).strip()

    def content_des(self):
        if len(self._content) >= 10:
            return self._content[0:10]
        else:
            return self._content[0: len(self._content)]

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        if isinstance(value, dict):
            self._params = value

    # 获取内部映射
    def _option_map(self) -> str:
        if self._option.startswith(self.OPTION_START_TAG) \
                and self._option.endswith(self.OPTION_END_TAG):
            option = self.option
            option = option.lstrip(self.OPTION_START_TAG).rstrip(self.OPTION_END_TAG)
            option = '_'.join([i.upper() for i in option.split(' ') if i])
        else:
            option = ''
        return option

    @property
    def kwargs(self):
        dict_tmp = copy.deepcopy(self.params)
        dict_tmp['content'] = self.content
        return dict_tmp


class PtlCategory(Enum):
    OTHER = 0
    LOCAL_FILE = 1
    HTTP = 11
    HTTPS = 12
    SSH = 13
    TELNET = 14
    SNMP = 15
    MML = 16
    CLIENT_T_QUERY = 51


PtlCategoryList = [i for i, _ in PtlCategory.__members__.items()]


class ProtocolInfo(UUIDInfo):
    def __init__(self, category: PtlCategory = PtlCategory.OTHER,
                 name: str = '', version: str = ''):
        self.category = category
        self.name = name
        self.version = version
        super().__init__(f'{self.name}:{self.version}')


class RstCategory(Enum):
    SUCCESS = 1
    FAILED = 2
    ABNORMAL = 3


RstCategoryList = [i for i, _ in RstCategory.__members__.items()]


class ResultInfo:
    def __init__(self, category: RstCategory = RstCategory.FAILED,
                 code: int = 0, msg: str = '', data: Any = None):
        self.category = category
        self.code = code
        self.msg = msg
        self.data = data

    @property
    def err_msg(self):
        return f'{self.category.name}[{self.code}]:{self.msg}'
