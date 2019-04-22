from .workflow import Workflow

class WorkflowContainer:

    def list_workflows(self):
        managers = [c for c in self.list_components() if isinstance(c, Workflow) ]
        return managers
