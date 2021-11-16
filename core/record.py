from .info import *


class Record(UUIDInfo):

    def __init__(self, device_info: DeviceInfo, connect_info: ConnectInfo,
                 protocol_info: ProtocolInfo, command_info: CommandInfo):

        self.device_info = device_info
        self.connect_info = connect_info
        self.protocol_info = protocol_info
        self.command_info = command_info

        self.uuid_tuple = (self.device_info.uuid, self.connect_info.uuid, self.protocol_info.uuid,
                           self.command_info.uuid)
        super().__init__(f'{self.uuid_tuple}')


