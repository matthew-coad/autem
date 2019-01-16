import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
from plotly import graph_objs as go

import genetic

# Simulation selector
def simulation_selector(root_path):
    simulations = genetic.SimulationManager(root_path).list_simulations()
    selector = dcc.Dropdown(
        id="simulation",
        options=[{"label": sim, "value": sim} for sim in simulations],
        value=simulations[0],
        clearable=False,
    )
    return selector

# Measure selector
def member_measure_selector(simulation_path):
    meta_manager = genetic.MetaManager(simulation_path)
    member_attributes = meta_manager.get_member_attributes()
    measure_attributes = [a for a in member_attributes if a.role == genetic.AttributeRole.Measure]
    selector = dcc.Dropdown(
        id="member_measure_dropdown",
        options=[{"label": m.name, "value": m.name} for m in measure_attributes],
        value=measure_attributes[0],
        clearable=False,
    )
    return selector

#returns top indicator div
def indicator(color, text, id_value):
    return html.Div(
        [
            
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
    )
