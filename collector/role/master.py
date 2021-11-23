from typing import Any
import datetime
from queue import Queue

from ..core.flow import TaskFLow
from .slaver import FlowSlaver
from .slaver import RecordSlaver

from ..util.logger import log


class Master:
    DEFAULT_MAX_SLAVER_FLOW = 3
    DEFAULT_MAX_SLAVER_RECORD = 6
    DEFAULT_MAX_TIMEOUT = 300

    def __init__(self, map_queues, timeout: int = 600, **kwargs):
        self.map_queues = map_queues
        self.size_flows = 0
        self.size_exit_flows = 0
        self.size_records = 0
        self.map_records = {}
        self.timeout = timeout                              # 超时设置
        self.start_time = datetime.datetime.now()

    def add_flow(self, flow: TaskFLow):
        if isinstance(flow, TaskFLow):
            self.map_queues['flows'].put(flow)

    def run(self):
        self.run_slaver_flow()
        self.run_slaver_record()
        self.watch()

    # 创建多线程处理flow
    def run_slaver_flow(self):
        self.size_flows = self.map_queues['flows'].qsize()
        if self.size_flows < self.DEFAULT_MAX_SLAVER_FLOW:
            max_slaver_flow = self.size_flows
        else:
            max_slaver_flow = self.DEFAULT_MAX_SLAVER_FLOW
        for i in range(max_slaver_flow):
            thread = FlowSlaver(
                f'FlowSlaver{i}', map_queues=self.map_queues,
                map_records=self.map_records,
                size_exit_flows=self.size_exit_flows
            )
            thread.daemon = True
            thread.start()

    # 创建多线程处理record
    def run_slaver_record(self):
        for i in range(self.DEFAULT_MAX_SLAVER_RECORD):
            thread = RecordSlaver(
                f'FlowSlaver{i}', map_queues=self.map_queues,
                map_records=self.map_records
            )
            thread.daemon = True
            thread.start()

    def watch(self):
        while True:
            cur_time = datetime.datetime.now()
            if (cur_time - self.start_time).seconds >= self.timeout:
                log(self, f'超时退出....')
                break

            if self.size_exit_flows == self.size_flows:
                log(self, f'全部完成...退出')
                break
