
import paramiko
from queue import Queue

from collector.info import *
from collector.connector.core.base_connector import BaseConnector


class SSHConnector(BaseConnector):

    def __init__(self, cnt_info: ConnectInfo, task_tag, commands_queue: Queue, results_queue: Queue):
        super().__init__(cnt_info, task_tag, commands_queue, results_queue)
        self.is_auto = False
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.auto()

    def __del__(self):
        self.client.close()

    def auto(self):
        if not self.is_auto:
            print('login')
            self.client.connect(hostname=self.cnt_info.host, port=self.cnt_info.port,
                                username=self.cnt_info.username, password=self.cnt_info.password)

    def execute_shell(self, command: CommandInfo, **kwargs) -> ResultInfo:
        stdin, stdout, stderr = self.client.exec_command(command.content)
        result = stdout.read().decode('utf-8')
        return ResultInfo(RstCategory.SUCCESS, result)

