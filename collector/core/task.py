from __future__ import annotations
from enum import Enum
from typing import Optional
from queue import Queue
import datetime
from collector.core.info import UUIDInfo
from collector.core.info import ConnectInfo
from collector.core.info import CommandInfo
from collector.core.info import ProtocolInfo
from collector.core.info import ResultInfo
from collector.core.terminal import Terminal

from collector.util.logger import log


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
            self._result_info = connector.send_cmd(self.command_info)
        else:
            log(self, f'Command jump', level='info')
        return self._result_info


class TaskHandlerStatus(Enum):
    SUCCESS = 1
    FAILED = 2
    ABNORMAL = 3
    BLOCKING = 4


class TaskHandler:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.status = TaskHandlerStatus.FAILED

    def run(self, *args, **kwargs):
        pass


class TaskFlowStatus(Enum):
    New = 1
    Running = 2
    Blocking = 3
    Exit = 4


class TaskFLow:

    def __init__(self, df_task, flow_env, map_queues):
        self.df_task = df_task
        self.flow_env = flow_env
        self.map_queues = map_queues
        self.cur_handler: Optional[TaskHandler] = None
        self.queue_handlers = Queue(50)
        self.status = TaskFlowStatus.New
        # 等待阻塞相关
        self.wait_time = 0.0
        self.wait_start_time = None

    def run(self):
        log(self, 'Run...')
        if self.cur_handler is None and self.status == TaskFlowStatus.New:
            self.status = TaskFlowStatus.Running

        while True:

            if self.queue_handlers.empty():
                if self.cur_handler is None:
                    log(self, 'Queue Handler Empty, So End...')
                    self.status = TaskFlowStatus.Exit
                    break
                elif self.cur_handler.status in [TaskHandlerStatus.SUCCESS, TaskHandlerStatus.FAILED]:
                    self.status = TaskFlowStatus.Exit
                    break
                elif self.cur_handler.status == TaskHandlerStatus.BLOCKING:
                    self.status = TaskFlowStatus.Blocking
            else:
                self.cur_handler = self.queue_handlers.get()




            if self.status == TaskFlowStatus.New:
                if self.queue_handlers.empty():
                    log(self, 'Queue Handler Empty, So End...')
                    self.status = TaskFlowStatus.Exit
                    break
                else:
                    cur_handler = self.queue_handlers.get()
                    self.cur_handler = cur_handler
                    cur_handler.run()
                    self.status = TaskFlowStatus.Running
            elif self.status == TaskFlowStatus.Running:
                if self.queue_handlers.empty():
                    if self.cur_handler.status in [TaskHandlerStatus.SUCCESS,
                                                   TaskHandlerStatus.FAILED]:
                        log(self, 'Queue Handler Empty, So End...')
                        self.status = TaskFlowStatus.Exit
                        break
                    elif self.cur_handler.status == TaskHandlerStatus.ABNORMAL:
                        if self.cur_handler.run_num > 3:
                            self.status = TaskFlowStatus.Exit
                            break
                        else:
                            cur_handler = self.cur_handler
                    else:


                else:
                    pass
            elif self.status == TaskFlowStatus.Blocking:
                # 校验时间是否满足
                datetime_cur = datetime.datetime.now()
                if datetime_cur - self.wait_start_time
                pass



            if self.queue_handlers.empty():
                if self.cur_handler.status in [TaskHandlerStatus.SUCCESS,
                                               TaskHandlerStatus.FAILED]:
                    log(self, 'Queue Handler Empty, So End...')
                    self.status = TaskFlowStatus.Exit
                    break
                elif self.cur_handler.status == TaskHandlerStatus.BLOCKING:




            if self.status == TaskFlowStatus.New:
                if self.queue_handlers.empty():
                    log(self, 'Queue Handler Empty, So End...')
                    self.status = TaskFlowStatus.Exit
                    break
            elif self.status == TaskFlowStatus.Running:
                if self.queue_handlers.empty():




            if self.queue_handlers.empty():
                log(self, 'Queue Handler Empty, So End...')
                self.status = TaskFlowStatus.Exit
                break
            # 刚开始
            if self.cur_handler is None and self.status == TaskFlowStatus.New:
                self.status = TaskFlowStatus.Running
            # 从队列中获取一个新的
            cur_handler = self.queue_handlers.get()
            if not isinstance(cur_handler, TaskHandler):
                logs = f'Your cls[{cur_handler.__class__.__name__}] is ' \
                       f'not TaskHandler.'
                log(self, logs, level='warning')
            self.cur_handler = cur_handler
            cur_handler.run()
            if cur_handler.status == TaskHandlerStatus.SUCCESS:
                continue
            elif cur_handler.status == TaskHandlerStatus.FAILED:
                logs = f'Your cls[{cur_handler.__class__.__name__}] is FAILED.'
                log(self, logs, level='warning')
                self.status = TaskFlowStatus.Exit
                break
            elif cur_handler.status == TaskHandlerStatus.BLOCKING:
                self.wait_time = 0.1
                self.wait_start_time = datetime.datetime.now()
                self.status = TaskFlowStatus.Blocking
                break
            else:
                pass

