from __future__ import annotations
from enum import Enum

from collector.info import UUIDInfo
from collector.info import CommandInfo
from collector.info import ConnectInfo
from collector.info import ResultInfo
from collector.info import ProtocolInfo
from collector.info import DeviceInfo
from .terminal import Terminal
from .terminal import MAP_TERMINAL

from ..util.logger import log


# 命令结果数据类型
class EnumCmdRstContentType(Enum):
    TEXT = ''
    SUCCESS = '成功'
    FAILED = '失败'
    ABNORMAL = '异常'


# 记录 作用： XX命令在XX设备上，用XX协议，XX连接信息 ----执行
class Record(UUIDInfo):
    def __init__(self, command_info: CommandInfo = None,
                 device_info: DeviceInfo = None,
                 connect_info: ConnectInfo = None,
                 protocol_info: ProtocolInfo = None,
                 **kwargs):
        self.command_info = command_info
        self.connect_info = connect_info
        self.protocol_info = protocol_info
        self.device_info = device_info
        self.kwargs = kwargs
        self._result_info = None

        terminal_cls = MAP_TERMINAL.get(
            self.device_info.category.name, Terminal
        )
        self.terminal = terminal_cls(self.connect_info, self.device_info)
        self.connector_cls = self.terminal.PTL_CNT_MAP.get(
            self.protocol_info.category.name
        )
        self.uuid_tuple = (self.device_info.uuid, self.connect_info.uuid,
                           self.protocol_info.uuid, self.command_info.uuid)
        super().__init__(f'{self.uuid_tuple}')

    @property
    def result_info(self) -> ResultInfo:
        return self._result_info

    @result_info.setter
    def result_info(self, value: ResultInfo):
        if isinstance(value, ResultInfo):
            self._result_info = value

    def handle_cmd(self):
        if self.command_info is not None and self.connect_info is not None:
            # 1、优化处理命令
            self.command_info = self.terminal.handle_cmd(self.command_info,
                                                         self.protocol_info)

    def handle_rst(self):
        # 4、优化处理结果
        log(self, f"Record-uuid({self.uuid}), Put RST", level='info')
        self._result_info = self.terminal.handle_rst(
            self._result_info, self.command_info, self.protocol_info
        )

    def run(self):
        log(self, 'Run', level='info')
        # 第一步。命令处理
        #
        if self.command_info is not None and self.connect_info is not None:
            # 优化处理命令
            self.handle_cmd()
            # 从设备获取连接器
            connector = self.connector_cls(self.connect_info,
                                           version=self.terminal.version)
            # 发送命令执行，获取执行结果
            self._result_info = connector.send(self.command_info)
            # 优化处理结果
            self.handle_rst()
            # 处理结果
        else:
            log(self, f'Command jump', level='info')
            self.handle_rst()
        return self.uuid, self._result_info.expectations
