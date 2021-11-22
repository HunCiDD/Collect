from typing import Any
import datetime
from queue import Queue
from ..core.info import CommandInfo
from ..core.info import RstCategory
from .record import TaskRecord

class HandlerStatus(RstCategory):
    pass


class Handler:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.status = HandlerStatus.FAILED
        self.response = None

    def run(self):
        pass


class WaitHandler(Handler):
    def __init__(self, wait_time: float = 0.1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wait_time = wait_time

    def run(self):
        self.response = datetime.datetime.now()
        self.status = HandlerStatus.SUCCESS


class PutRecordHandler(Handler):

    def __init__(self, record: TaskRecord, tag: str, queue_records: Queue, **kwargs):
        self.record = record
        self.tag = tag
        self.queue_records = queue_records


    def run(self):
        self.

