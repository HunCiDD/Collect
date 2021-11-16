

from queue import Queue
from threading import Thread

from ..info import *


class BaseConnector(Thread):

    def __init__(self, cnt_info: ConnectInfo, task_tag, commands_queue: Queue, results_queue: Queue):
        self.cnt_info = cnt_info
        self.task_tag = task_tag
        self.commands_queue = commands_queue
        self.results_queue = results_queue
        super().__init__()

    def run(self) -> None:
        while True:
            if self.commands_queue.empty():
                continue

            command = self.commands_queue.get()
            if command is None:
                break

            r = self.send(command)
            self.results_queue.put((self.task_tag, r))

    def send(self, command: CommandInfo, **kwargs) -> ResultInfo:
        option_map = command.option_map()
        if hasattr(self, option_map):
            func = getattr(self, option_map)
            return func(command)
        else:
            raise ValueError('1111')


