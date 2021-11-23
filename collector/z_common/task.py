import time

import pandas as pd
from queue import Queue
from ..core.info import CommandInfo
from ..core.task import TaskRecord
from ..core.task import TaskHandlerStatus
from ..core.task import TaskHandler
from ..core.task import TaskFlowStatus
from ..core.task import TaskFLow

from ..util.logger import log

class ComSSHRecordHandler(TaskHandler):

    def __init__(self, df_task: pd.DataFrame, flow_env, map_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df_task = df_task
        self.flow_env = flow_env
        self.tag = self.flow_env['tag']
        self.queue_records: Queue = map_queue['records']

    def run(self, *args, **kwargs):
        for index, row in self.df_task.iterrows():
            ser = pd.Series(row)
            host = ser.get('host', '')
            host_name = f'Host_{host}'
            cmd_content = ser.get('cmd', '')
            cmd_info = CommandInfo(option='#[EXECUTE_SHELL]', content=cmd_content)
            record = TaskRecord(command_info=cmd_info, connect_info=self.flow_env['cnt_infos'][host],
                                protocol_info=self.flow_env['ptl_infos']['ssh'],
                                terminal=self.flow_env['devices'][host])
            self.queue_records.put((self.tag, record))
        self.flow_env['size_records'] = self.df_task.shape[1]
        self.status = TaskHandlerStatus.SUCCESS


class ComSSHResultHandler(TaskHandler):
    def __init__(self, flow_env, map_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flow_env = flow_env
        self.tag = self.flow_env['tag']
        self.queue_records: Queue = map_queue['records']
        self.queue_results: Queue = map_queue['results']

    def run(self, *args, **kwargs):
        cur_size = 0
        while True:
            if self.queue_results.empty():
                if cur_size == self.flow_env['size_records']:
                    self.status = TaskHandlerStatus.SUCCESS
                    break
                else:
                    continue

            flow_tag, record = self.queue_results.get()
            log(self, flow_tag, self.tag)
            if flow_tag != self.tag:
                self.queue_records.put(flow_tag, record)
                time.sleep(0.2)
                continue
            else:
                cur_size += 1
                log(self, record.result_info.data)
                continue


class ComSSHCmdExecTaskFlow(TaskFLow):
    def __init__(self, df_task, flow_env, map_queues):
        super().__init__(df_task, flow_env, map_queues)

        self.queue_handlers.put(
            ComSSHRecordHandler(df_task, flow_env, map_queues)
        )
        self.queue_handlers.put(
            ComSSHResultHandler(flow_env, map_queues)
        )
