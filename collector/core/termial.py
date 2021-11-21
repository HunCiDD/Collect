from threading import Lock

from .info import UUIDInfo
from collector.core.info import ConnectInfo


class Terminal(UUIDInfo):
    # 需要实现单例
    _instances = {}
    # 线程锁，保证线程下安全
    _lock: Lock = Lock()

    PTL_CNT_MAP = {}  # 协议链接映射

    def __new__(cls, connect_info: ConnectInfo, *args, **kwargs):
        with cls._lock:
            uuid = connect_info.uuid
            if uuid in cls._instances:
                instance = cls._instances[uuid]
            else:
                instance = super().__new__(cls)
                cls._instances[uuid] = instance
        return instance

    def __init__(self, connect_info: ConnectInfo, name: str = '', version: str = '', **kwargs):
        self._connect_info = connect_info
        self.name = name
        self.version = version
        self._category = self.__class__.__name__
        self.kwargs = kwargs
        super().__init__(f'{self._category}:{self.version}')

    @property
    def category(self):
        return self._category




