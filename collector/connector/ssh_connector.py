
import paramiko

from ..core.info import ConnectInfo
from ..core.info import CommandInfo
from ..core.info import RstCategory
from ..core.info import ResultInfo
from ..connector.base_connector import BaseConnector


class SSHConnector(BaseConnector):

    def __init__(self, connect_info: ConnectInfo, **kwargs):
        super().__init__(connect_info, **kwargs)
        self.is_auth = False
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.auth()

    def __del__(self):
        self.client.close()

    def auth(self):
        if not self.is_auth:
            print('login')
            self.client.connect(hostname=self.connect_info.host_name,
                                port=self.connect_info.port,
                                username=self.connect_info.username,
                                password=self.connect_info.password)

    def execute_shell(self, command: CommandInfo, **kwargs) -> ResultInfo:
        stdin, stdout, stderr = self.client.exec_command(command.content)
        result = stdout.read().decode('utf-8')
        return ResultInfo(RstCategory.SUCCESS, code=0, msg='', data=result)

