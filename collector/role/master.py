from typing import List
import datetime
import pandas as pd
from queue import Queue
from collector.record import Record
from ..core.terminal import MAP_TERMINAL
from ..devices.platform_dv.terminal import PlatformDV
from .slaver import CollectSlaver
from ..util.logger import log
MAP_TERMINAL.update({EnumDeviceCategory.PLATFORM_DV.name: PlatformDV})


class CollectMaster:
    DEFAULT_MAX_SLAVER = 10
    DEFAULT_MAX_TIMEOUT = 300

    def __init__(self, records: List[Record] = None, timeout: int = 600,
                 **kwargs):
        if records is None:
            self.list_records = []
        else:
            self.list_records = records
        self.map_records = {}
        self.df_records_tag = None
        self.queue_results = Queue(200)
        self.queue_records = Queue(len(self.list_records))
        self.timeout = timeout                              # 超时设置
        self.records_size = 0
        self.start_time = datetime.datetime.now()

    def run(self):
        self.tag_records()
        self.run_records()
        self.watch_records()

    def tag_records(self):
        list_tmp = []
        for i, record in enumerate(self.list_records):
            list_tmp.append({
                'uuid': record.uuid, 'index': i,
                'command_info_category': record.command_info.category.name,
                'device_info_category': record.device_info.category.name,
                'connect_info_uuid': record.connect_info.uuid,
                'protocol_info_uuid': record.protocol_info.uuid,
                'protocol_info_category': record.protocol_info.category.name
            })
        self.df_records_tag = pd.DataFrame(list_tmp)

    # 运行 records
    def run_records(self):
        self.records_size = len(self.list_records)
        for record in self.list_records:
            self.queue_records.put(record)

        for i in range(self.DEFAULT_MAX_SLAVER):
            thread = CollectSlaver(tag=str(i),
                                   queue_tasks=self.queue_records,
                                   queue_results=self.queue_results)
            thread.daemon = True
            thread.start()

    def watch_records(self):
        cur_records = 0
        while True:
            cur_time = datetime.datetime.now()
            if (cur_time - self.start_time).seconds >= 30:
                log(self, f'超时....')
                break

            while not self.queue_results.empty():
                record_uuid, expectations = self.queue_results.get()
                cur_records += 1
                new_size = self.handler_expectations(record_uuid, expectations)
                self.records_size += new_size

            if cur_records >= self.records_size:
                print('全部完成。。。。。')
                break
