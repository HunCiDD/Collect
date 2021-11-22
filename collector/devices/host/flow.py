
from ...task.flow import TaskFLow



class GetMoBaseTaskFlow(TaskFLow):

    def start(self):

        self.queue_handlers.put()

    pass