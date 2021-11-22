from __future__ import annotations

from collector.core.info import UUIDInfo
from collector.core.info import ConnectInfo
from collector.core.info import CommandInfo
from collector.core.info import ProtocolInfo
from collector.core.info import ResultInfo
from collector.core.termial import Terminal

from ..utils.logger import log


# 记录 作用： XX命令在XX设备上，用XX协议，XX连接信息 ----执行
class TaskRecord(UUIDInfo):
    def __init__(self, command_info: CommandInfo = None,
                 connect_info: ConnectInfo = None,
                 protocol_info: ProtocolInfo = None,
                 terminal: Terminal = None,
                 **kwargs):
        self.command_info = command_info
        self.connect_info = connect_info
        self.protocol_info = protocol_info
        self.terminal = terminal
        self.kwargs = kwargs
        self._result_info = None

        self.connector_cls = self.terminal.PTL_CNT_MAP.get(
            self.protocol_info.category.name
        )
        self.uuid_tuple = (self.terminal.uuid, self.connect_info.uuid,
                           self.protocol_info.uuid, self.command_info.uuid)
        super().__init__(f'{self.uuid_tuple}')

    @property
    def result_info(self) -> ResultInfo:
        return self._result_info

    @result_info.setter
    def result_info(self, value: ResultInfo):
        if isinstance(value, ResultInfo):
            self._result_info = value

    def run(self) -> ResultInfo:
        log(self, f'[{self.uuid}]Run', level='info')
        # 第一步。命令处理
        #
        if self.command_info is not None and self.connect_info is not None:
            connector = self.connector_cls(self.connect_info,
                                           version=self.terminal.version)
            # 发送命令执行，获取执行结果
            self._result_info = connector.send(self.command_info)
        else:
            log(self, f'Command jump', level='info')
        return self._result_info
