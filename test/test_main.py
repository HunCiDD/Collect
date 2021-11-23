from random import randint
import unittest
from queue import Queue
import pandas as pd

from collector.core.info import ConnectInfo
from collector.core.info import PtlCategory
from collector.core.info import ProtocolInfo
from collector.core.env import Env
from collector.core.task import TaskFLow
from collector.z_host.terminal import Host
from collector.z_common.task import ComSSHCmdExecTaskFlow

from collector.role.master import Master

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_001(self):
        # 创建flow_env
        cnt_infos = {
            '201': ConnectInfo('192.168.0.201', port='22', username='winter', password='hdd123456'),
            '202': ConnectInfo('192.168.0.202', port='22', username='winter', password='hdd123456'),
            '203': ConnectInfo('192.168.0.203', port='22', username='winter', password='hdd123456'),
            '211': ConnectInfo('192.168.0.211', port='22', username='winter', password='hdd123456'),
        }
        hosts = {key: Host(cnt_info, name=f'Host_{key}') for key, cnt_info in cnt_infos.items()}

        flow_env = Env(tag='flow')
        flow_env['devices'] = hosts
        flow_env['cnt_infos'] = cnt_infos
        flow_env['ptl_infos'] = {
            'ssh': ProtocolInfo(PtlCategory.SSH)
        }
        flow_env['tag'] = 'a'
        list_cmd = [
            'ls -al', 'pwd', 'date -R', 'ps -ef', 'top', 'free', 'iostat'
        ]
        tasks = [{'cmd': list_cmd[randint(0, len(list_cmd)-1)], 'host': f'20{randint(1, 3)}'} for _ in range(20)]
        df_task = pd.DataFrame(tasks)
        map_queues = {
            'flows': Queue(100),
            'records': Queue(200),
            'results': Queue(200)
        }
        flow = ComSSHCmdExecTaskFlow(df_task, flow_env, map_queues=map_queues)
        m = Master(map_queues, timeout=20)
        m.add_flow(flow)
        m.run()


if __name__ == '__main__':
    unittest.main()
