import time
from typing import List
from queue import Queue
from threading import Thread

from ..core.record import TaskRecord
from ..core.flow import TaskFlowStatus
from ..util.logger import log


class Slaver(Thread):
    def __init__(self, slaver_tag: str, *args, **kwargs):
        super().__init__()
        self.tag = slaver_tag

    def run(self) -> None:
        pass


class FlowSlaver(Slaver):
    # 奴隶
    def __init__(self, slaver_tag: str, map_queues: dict = None,
                 *args, **kwargs):
        super().__init__(slaver_tag)
        self.queue_flows: Queue = map_queues.get('flows', None)

    def run(self, ) -> None:
        while True:
            if self.queue_flows.empty():
                continue

            flow = self.queue_flows.get()
            flow.run()
            if flow.status == TaskFlowStatus.Blocking:
                self.queue_flows.put(flow)
            elif flow.status == '完成':
                break

            if flow is None:
                log(self, f'None, Cur Connector End')
                break


class RecordSlaver(Slaver):
    # 采集奴隶
    def __init__(self, tag: str, queue_record: Queue = None,
                 queue_cnt_rst: Queue = None, **kwargs):
        super().__init__(tag)
        self.tag = tag
        self.queue_record = queue_record
        self.queue_cnt_rst = queue_cnt_rst

    def run(self, ) -> None:
        while True:
            if self.queue_record.empty():
                continue
            record = self.queue_record.get()
            if record is None:
                log(self, f'None, Cur Connector End')
                break

            if not isinstance(record, TaskRecord):
                break

            self.queue_cnt_rst.put(record.run())
            time.sleep(0.2)
