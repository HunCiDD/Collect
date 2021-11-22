

from ...task.handler import Handler


class ConfConvertHandler(Handler):
    def __init__(self, task_conf: list = None, *args, **kwargs):
        super(ConfConvertHandler, self).__init__(*args, **kwargs)
        self.task_conf = task_conf

    def run(self):
        pass


class SetRecordsHandler(Handler):
    def __init__(self, task_conf: list = None, *args, ** kwargs):
        super(SetRecordsHandler, self).__init__(*args, **kwargs)
        self.task_conf = task_conf

    def run(self):
        pass




class CMDContentLimiterHandler(Handler):

    def run(self, request: CommandInfo):
        command_info = request
        if not isinstance(command_info, CommandInfo):
            return request


from collector.core.info import CommandInfo
from collector.core.info import ResultInfo


class CMDHandler:
    def run(self, command: CommandInfo, **kwargs) -> CommandInfo:
        return command


class CMDHandlerFlow:
    HANDLERS_FLOW = []

    def run(self, command: CommandInfo, **kwargs) -> CommandInfo:
        for handler_cls in self.HANDLERS_FLOW:
            handler = handler_cls()
            command = handler.run(command, **kwargs)
        return command


class RSTHandler:
    def run(self, cnt_result: ResultInfo, command: CommandInfo = None,
            **kwargs) -> ResultInfo:
        return cnt_result


class RSTHandlerFlow:
    HANDLERS_FLOW = []

    def run(self, cnt_result: ResultInfo, command: CommandInfo = None,
            **kwargs) -> ResultInfo:
        for handler_cls in self.HANDLERS_FLOW:
            handler = handler_cls()
            cnt_result = handler.run(cnt_result, command, **kwargs)
        return cnt_result
