import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from genetic import ReportManager

import config

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    color="primary",
    dark="True",    
    brand="Autem",
    brand_href="#",
    sticky="top",
)

# control_column = dbc.Col(dbc.Form([simulation_group]), width = 3)

graph1 = html.Div(
    [
        html.P("Population over time"),

        dcc.Graph(
            config=dict(displayModeBar=False),
            style={"height": "98%", "width": "98%"},
        ),

    ],
    className="six columns chart_div",
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

def chi(args): return [a for a in args]

def container(*args): return html.Div(children = chi(args), className="container-fluid")

def row(*args): return html.Div(children = chi(args), className="row")

def tool_col(*args): return html.Div(children = chi(args))

def content_col(*args): return html.Div(children = chi(args), className="col-5")

def div(*args): return html.Div(children = chi(args))

def P(arg): return html.P(arg)

def H(*args): return html.Div(children = chi(args), className="badge badge-primary text-wrap")

def graph_place(id, label):
    return div(
        H(label),
        dcc.Graph(
            id=id,
            config=dict(displayModeBar=False),
            style={"height": "300px"},
        )
    )

def graph_layout(x_title, y_title):
    return go.Layout(
        xaxis={'title': x_title},
        yaxis={'title': y_title},
        margin={'l': 40, 'b': 50, 't': 20, 'r': 20},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )

def layout_app():
    report_manager = ReportManager(config.REPOSITORY_PATH)
    simulations = report_manager.get_simulations()
    layout = container(
        row(
            content_col(
                dcc.Dropdown(
                    id="simulation",
                    options=[{"label": sim.name, "value": sim.name} for sim in simulations],
                    value=simulations[0].name,
                    clearable=False,
                ),
            ),
        ),

        row(
            content_col(
                graph_place("kpi_progress", "Kpi progress")
            ),
            content_col(
                graph_place("progress", "Simulation Progress")
            ),
        )
    )
    return layout

app.layout = layout_app

@app.callback(
    Output("kpi_progress", "figure"),
    [
        Input("simulation", "value"),
    ],
)
def update_kpi_progress(simulation):
    
    if simulation is None:
        layout = dict(annotations=[dict(text="No results available", showarrow=False)])
        return {"data": [], "layout": layout}

    report_manager = ReportManager(config.REPOSITORY_PATH)
    simulation_info = report_manager.get_simulation(simulation)
    df = report_manager.read_battle_report(simulation_info)

    # Format results
    data = [
        go.Scatter(
            x=df['step'],
            y=df['test_score'],
            mode='markers',
            name='score',
            marker = dict(
                size = 2,
            ),

        ),
    ]
    return {"data": data, "layout": graph_layout("step", "score")}

@app.callback(
    Output("progress", "figure"),
    [
        Input("simulation", "value"),
    ],
)
def update_progress(simulation):
    
    if simulation is None:
        layout = dict(annotations=[dict(text="No results available", showarrow=False)])
        return {"data": [], "layout": layout}

    report_manager = ReportManager(config.REPOSITORY_PATH)
    simulation_info = report_manager.get_simulation(simulation)
    df = report_manager.read_battle_report(simulation_info)

    # Format results
    data = [
        go.Scatter(
            x=df['step'],
            y=df['n_evaluation'],
            mode='markers',
            name='Evaluations',
            marker = dict(
                size = 2,
            ),
        ),
        go.Scatter(
            x=df['step'],
            y=df['n_contest'],
            mode='markers',
            name='contests',
            marker = dict(
                size = 2,
            ),
        ),
        go.Scatter(
            x=df['step'],
            y=df['n_victory'],
            mode='markers',
            name='Victories',
            marker = dict(
                size = 2,
            ),
        ),
        go.Scatter(
            x=df['step'],
            y=df['n_defeat'],
            mode='markers',
            name='Defeats',
            marker = dict(
                size = 2,
            ),
        )
    ]

    return {"data": data, "layout": graph_layout("step", "score")}

if __name__ == "__main__":
    app.run_server(debug=True)