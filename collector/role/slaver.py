import time
from queue import Queue
from threading import Thread

from ..task.record import TaskRecord

from ..utils.logger import log


class TaskRecordSlaver(Thread):
    # 采集奴隶
    def __init__(self, tag: str, queue_task_records: Queue = None,
                 queue_results: Queue = None, **kwargs):
        super().__init__()
        self.tag = tag
        self.queue_task_records = queue_task_records
        self.queue_results = queue_results

    def run(self, ) -> None:
        while True:
            if self.queue_task_records.empty():
                continue
            task_flow_id, record = self.queue_task_records.get()

            if not isinstance(record, TaskRecord):
                continue
            rst_info = record.run()
            self.queue_results.put(task_flow_id, record.uuid)




class TaskFlowSlaver(Thread):
    pass