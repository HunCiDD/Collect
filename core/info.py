

from hashlib import sha256
from enum import Enum


class UUIDInfo:

    def __init__(self, hash_value: str):
        self.hash_value = hash_value
        self.uuid = sha256(self.hash_value.encode('utf-8')).hexdigest()


class ConnectInfo(UUIDInfo):

    def __init__(self, host: str, port: int = 0, username: str = '', password: str = ''):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        super().__init__(f'{self.host}:{self.port}:{username}')


class CMDCategory(Enum):
    BASE = 1


class CommandInfo(UUIDInfo):
    def __init__(self, category: CMDCategory = CMDCategory.BASE,
                 option: str = '', content: str = '', params: dict = None):
        self.category = category
        self.option = option
        self.content = content
        self.params = params
        if self.params is None:
            self.params = {}
        super().__init__(f'{self.content}:{self.params}')

    def option_map(self):
        return self.option


class PtlCategory(Enum):
    BASE = 1
    HTTP = 1
    SSH = 2


class ProtocolInfo(UUIDInfo):
    def __init__(self, category: PtlCategory = PtlCategory.BASE,
                 name: str = '', version: str = ''):
        self.category = category
        self.name = name
        self.version = version
        super().__init__(f'{self.name}:{self.version}')


class DevCategory(Enum):
    HOST = 1
    SWITCH = 2


class DeviceInfo(UUIDInfo):
    def __init__(self, category: DevCategory = DevCategory.HOST,
                 name: str = '', version: str = ''):
        self.category = category
        self.name = name
        self.version = version
        super().__init__(f'{self.name}:{self.version}')


class RstCategory(Enum):
    SUCCESS = 1
    FAILED = 2
    ABNORMAL = 3


class ResultInfo:
    def __init__(self, category: RstCategory = RstCategory.FAILED,
                 data=None):
        self.category = category
        self.data = data

