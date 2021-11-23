from threading import Lock

from ..core.info import CommandInfo
from ..core.info import ConnectInfo
from ..core.info import ResultInfo

from ..util.logger import log


class BaseConnector:
    """
    # 基础链接器
    """
    # 存储实例化对象
    _instances = {}
    # 线程锁，保证线程下安全
    _lock: Lock = Lock()

    def __new__(cls, connect_info: ConnectInfo, **kwargs):
        with cls._lock:
            key_id = connect_info.uuid
            if key_id in cls._instances:
                instance = cls._instances[key_id]
            else:
                instance = super().__new__(cls)
                cls._instances[key_id] = instance
        return instance

    def __init__(self, connect_info: ConnectInfo, *args, **kwargs):
        self.connect_info = connect_info
        self.is_auth = False
        self.client = None

    def send_cmd(self, command_info: CommandInfo, **kwargs) -> ResultInfo:
        log(self, "Connector Send Command...", level='info')
        log(self, f"Command-category({command_info.category})",
            level='info')
        log_str = f"Command-id({command_info.uuid}), " \
                  f"Command-index({command_info.index}), " \
                  f"Command-content-start({command_info.content_des()})"
        log(self, log_str, level='info')
        func = self.map_func_specific_exe(command_info, 'default')
        return func(command_info, **kwargs)

    def map_func(self, func_name):
        if not hasattr(self, func_name):
            err = 'Your connector does not implement the corresponding ' \
                  f'sending instruction method. func name is [{func_name}].'
            raise ValueError(err)
        func = getattr(self, func_name)
        return func

    # 提供基于命令信息，映射具体执行函数
    def map_func_specific_exe(self, command_info: CommandInfo,
                              default_func_name: str):
        option_map = command_info.option_map
        if not option_map.strip():
            func_name = default_func_name
        else:
            func_name = option_map.lower()
        return self.map_func(func_name)




