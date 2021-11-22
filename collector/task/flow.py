from enum import Enum
from queue import Queue
from .handler import Handler
from .handler import HandlerStatus
from .handler import WaitHandler


class FlowStatus(Enum):
    New = 1
    Running = 2
    Wait = 3
    Exit = 4


class TaskFLow:

    def __init__(self, env, queue_task_flows, queue_task_records, queue_record_result):
        pass
        self.queue_handlers = Queue(50)
        self.status = FlowStatus.New

        # 等待阻塞相关
        self.wait_time = 0.0
        self.wait_start_time = None

    def run(self):
        if self.status == FlowStatus.New:
            self.status = FlowStatus.Running

        while True:
            if self.queue_handlers.empty():
                continue

            handler = self.queue_handlers.get()
            if handler is None:
                break

            if not isinstance(handler, Handler):
                continue

            handler.run()
            if isinstance(handler, WaitHandler) and handler.status == HandlerStatus.SUCCESS:
                self.status = FlowStatus.Wait
                self.wait_time = handler.request
                self.wait_start_time = handler.response

            if handler.status == HandlerStatus.FAILED:
                self.status = FlowStatus.Exit
                break
