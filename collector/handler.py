from collector.info import CommandInfo
from collector.info import ResultInfo


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
