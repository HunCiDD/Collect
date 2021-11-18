from threading import Lock

from collector.info import CommandInfo
from collector.info import ConnectInfo
from collector.info import ResultInfo
from collector.info import DeviceInfo
from collector.info import ProtocolInfo

MAP_TERMINAL = {}


class Terminal:
    # 需要实现单例
    _instances = {}
    # 线程锁，保证线程下安全
    _lock: Lock = Lock()

    PTL_CNT_MAP = {}  # 协议链接映射

    def __new__(cls, connect_info: ConnectInfo, device_info: DeviceInfo,
                *args, **kwargs):
        with cls._lock:
            uuid = (connect_info.uuid, device_info.uuid)
            if uuid in cls._instances:
                instance = cls._instances[uuid]
            else:
                instance = super().__new__(cls)
                cls._instances[uuid] = instance
        return instance

    def __init__(self, connect_info: ConnectInfo, device_info: DeviceInfo,
                 *args, **kwargs):
        self.connect_info = connect_info
        self.device_info = device_info
        self.connect_info_maps = {"self": connect_info}

    @property
    def category(self):
        return self.device_info.category

    @property
    def version(self):
        return self.device_info.version

    def handle_rst(self, rst_info: ResultInfo, cmd_info: CommandInfo,
                   ptl_info: ProtocolInfo, **kwargs) -> ResultInfo:
        return rst_info

    def handle_cmd(self, cmd_info: CommandInfo,
                   ptl_info: ProtocolInfo, **kwargs) -> CommandInfo:
        return cmd_info
