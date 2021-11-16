import unittest
from core.info import *
from core.record import Record
from core.Connector.ssh_connector import SSHConnector
from queue import Queue
import pandas as pd
import datetime



class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.devices = DeviceInfo(DevCategory.HOST)
        self.connects = {
            0: ConnectInfo('192.168.0.201', port=22, username='winter', password='hdd123456'),
            1: ConnectInfo('192.168.0.202', port=22, username='winter', password='hdd123456'),
            2: ConnectInfo('192.168.0.203', port=22, username='winter', password='hdd123456'),
            3: ConnectInfo('192.168.0.211', port=22, username='winter', password='hdd123456'),
        }
        self.commands = {
            0: CommandInfo(CMDCategory.BASE, option='execute_shell', content='ls -al'),
            1: CommandInfo(CMDCategory.BASE, option='execute_shell', content='pwd'),
            2: CommandInfo(CMDCategory.BASE, option='execute_shell', content='date -R'),
        }
        self.protocols = {
            0: ProtocolInfo(PtlCategory.SSH)
        }

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_001(self):
        pass
        records = [
            Record(self.devices, self.connects[0], self.protocols[0], self.commands[0]),
            Record(self.devices, self.connects[0], self.protocols[0], self.commands[2]),
            Record(self.devices, self.connects[0], self.protocols[0], self.commands[0]),
            Record(self.devices, self.connects[1], self.protocols[0], self.commands[0]),
            Record(self.devices, self.connects[1], self.protocols[0], self.commands[1]),
            Record(self.devices, self.connects[1], self.protocols[0], self.commands[2]),
            Record(self.devices, self.connects[1], self.protocols[0], self.commands[0]),
            Record(self.devices, self.connects[0], self.protocols[0], self.commands[1]),
        ]
        records_uuid_table = [r.uuid_tuple for r in records]
        records_uuid_map = {r.uuid: r for r in records}
        # 分组
        task_group = {
            '0': [records[0], records[1], records[2], records[7]],
            '1': [records[3], records[4], records[5], records[6]],
        }

        start = datetime.datetime.now()
        print('Start')
        list_threads = []
        rst_queue = Queue(100)
        for key, value in task_group.items():
            cmd_queue = Queue(20)
            connect_info = value[0].connect_info
            _ = [cmd_queue.put((r.uuid, r.command_info)) for r in value]

            thread = SSHConnector(connect_info, key, cmd_queue, rst_queue)
            thread.daemon = True
            list_threads.append(thread)

        _ = [x.start() for x in list_threads]

        while True:
            cur = datetime.datetime.now()
            if (cur - start).seconds >= 30:
                print('超时')
                break

            if rst_queue.empty():
                continue

            record_uuid, result_info = rst_queue.get()
            print(record_uuid)
            print(result_info.category.name, result_info.data)

        print('End')


if __name__ == '__main__':
    unittest.main()
