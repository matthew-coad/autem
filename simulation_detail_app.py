import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

from pathlib import Path
import simulation_detail

df = simulation_detail.load_simulation_detail(pathlib.Path(".", "test_run"))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='First Model Status'),

    "Generation:", dcc.Input(value='MTL', type='text', readOnly = True)

])

if __name__ == '__main__':
    app.run_server(debug=True)