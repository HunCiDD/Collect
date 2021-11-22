from queue import Queue


class Env:

    def __init__(self):
        self.map_queues = {
            'task_flow': Queue(50),
            'task_records'
        }