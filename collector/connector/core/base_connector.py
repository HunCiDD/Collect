from queue import Queue
from threading import Thread
from threading import Lock

from ..info import CommandInfo
from ..info import ConnectInfo
from ..info import ResultInfo
from ..info import EnumProtocolCategory

from ...util.logger import log


class BaseConnector:
    """
    # 基础链接器
    """
    # 存储实例化对象
    _instances = {}
    # 线程锁，保证线程下安全
    _lock: Lock = Lock()
    protocol_type = EnumProtocolCategory.OTHER.name
    support_cmd_category = ()

    def __new__(cls, connect_info: ConnectInfo, **kwargs):
        with cls._lock:
            key_id = connect_info.uuid
            if key_id in cls._instances:
                instance = cls._instances[key_id]
            else:
                instance = super().__new__(cls)
                cls._instances[key_id] = instance
        return instance

    def __init__(self, connect_info: ConnectInfo, version: str = "",
                 client=None, **kwargs):
        self.connect_info = connect_info
        self.client = client
        self.version = version

    def send(self, command: CommandInfo, **kwargs) -> ResultInfo:
        if command.category not in self.support_cmd_category:
            err = 'Your connector do not support the current command type'
            raise ValueError(err)
        log(self, "Connector Send Command...", level='info')
        log(self, f"Command-category({command.category.name})",
            level='info')
        log_str = f"Command-id({command.uuid}), " \
                  f"Command-index({command.index}), " \
                  f"Command-content-start({command.content_des()})"
        log(self, log_str, level='info')
        func_send_name = f'send_{command.category.name.lower()}'
        return self.map_func(func_send_name)(command, **kwargs)

    def send_base(self, command: CommandInfo, **kwargs):
        err = 'Your connector does not support sending the BASE command.'
        raise ValueError(err)

    def send_auth(self, command: CommandInfo, **kwargs):
        err = 'Your connector does not support sending the AUTH command.'
        raise ValueError(err)

    def send_file(self, command: CommandInfo, **kwargs):
        err = 'Your connector does not support sending the FILE command.'
        raise ValueError(err)

    def send_other(self, command: CommandInfo, **kwargs):
        err = 'Your connector does not support sending the OTHER command.'
        raise ValueError(err)

    def map_func(self, func_name):
        if not hasattr(self, func_name):
            err = 'Your connector does not implement the corresponding ' \
                  f'sending instruction method. func name is [{func_name}].'
            raise ValueError(err)
        func = getattr(self, func_name)
        return func

    # 提供基于命令信息，映射具体执行函数
    def map_func_specific_exe(self, command: CommandInfo,
                              default_func_name: str):
        option_map = command.option_map
        if not option_map.strip():
            func_name = default_func_name
        else:
            func_name = option_map.lower()
        return self.map_func(func_name)



class BaseConnector(Thread):

    def __init__(self, cnt_info: ConnectInfo, task_tag, commands_queue: Queue, results_queue: Queue):
        self.cnt_info = cnt_info
        self.task_tag = task_tag
        self.commands_queue = commands_queue
        self.results_queue = results_queue
        super().__init__()

    def run(self) -> None:
        while True:
            if self.commands_queue.empty():
                continue

            record_uuid, command = self.commands_queue.get()
            if command is None:
                break

            print(self.__class__.__name__, 'run')
            r = self.send(command)
            self.results_queue.put((record_uuid, r))

    def send(self, command: CommandInfo, **kwargs) -> ResultInfo:
        option_map = command.option_map()
        if hasattr(self, option_map):
            func = getattr(self, option_map)
            return func(command)
        else:
            raise ValueError('1111')


