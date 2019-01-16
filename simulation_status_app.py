import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import genetic
from pathlib import Path

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

simulation_name = "highest_id"
report_path = Path("tests", "simulations", simulation_name)
population_report = genetic.read_population_report(report_path)

def select_simulation_dropdown():
    return dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    )

def simulation_population_status_graph(df):
    graph = dcc.Graph(
        id='population_status_graph',
        figure={
            'data': [
                go.Scatter(
                    x=df['generation'],
                    y=df['alive'],
                    name='alive'
                ),
                go.Scatter(
                    x=df['generation'],
                    y=df['exhausted'],
                    name='exhausted'
                ),
                go.Scatter(
                    x=df['generation'],
                    y=df['dead'],
                    name='dead'
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Generation'},
                yaxis={'title': 'Count'}
            )
        }
    )
    return graph

app.layout = html.Div([
    html.H1(children='Simulation Status'),
    population_status_graph(population_report)
])

if __name__ == '__main__':
    app.run_server(debug=True)