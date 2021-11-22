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

    def run(self):
        pass


class WaitHandler(Handler):
    def __init__(self, wait_time: float = 0.1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wait_time = wait_time

    def run(self):
        self.response = datetime.datetime.now()
        self.status = HandlerStatus.SUCCESS
