
from ..core.info import PtlCategory
from ..connector.ssh_connector import SSHConnector
from ..core.terminal import Terminal


class Host(Terminal):
    PTL_CNT_MAP = {
        PtlCategory.SSH.name: SSHConnector
    }
    pass




