import time
from queue import Queue
from threading import Thread

from collector.record import Record
from ..util.logger import log


class CollectSlaver(Thread):
    # 采集奴隶
    def __init__(self, tag: str, queue_tasks: Queue = None,
                 queue_results: Queue = None, **kwargs):
        super().__init__()
        self.tag = tag
        self.queue_tasks = queue_tasks
        self.queue_results = queue_results

    def run(self, ) -> None:
        while True:
            if self.queue_tasks.empty():
                continue
            record = self.queue_tasks.get()
            if record is None:
                log(self, f'None, Cur Connector End')
                break

            if not isinstance(record, Record):
                break

            self.queue_results.put(record.run())
            time.sleep(0.2)
