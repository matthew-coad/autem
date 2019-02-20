from ..simulators import Controller
from .utility import get_report_columns, get_report_frame

import pandas as pd

class Reporter(Controller):

    def get_battle_frame(self, simulation):
        records = simulation.reports
        if not records:
            return None
        frame = get_report_frame(records)
        return frame

    def get_outline_frame(self, simulation):
        outline = simulation.outline

        rows = [(attr.name, attr.dataset.value, role.value, attr.label) for attr in outline.attributes for role in attr.roles]
        d = {
            'name': [r[0] for r in rows],
            'dataset': [r[1] for r in rows],
            'role': [r[2] for r in rows],
            'label': [r[3] for r in rows]
        }
        df = pd.DataFrame(data=d)
        return df

    def report_simulation(self, simulation):
        """
        Report on the progress of a simulation
        """
        raise NotImplementedError("Report_simulation not implemented")
