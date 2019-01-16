import math
import json

import pandas as pd
import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
from plotly import graph_objs as go

import genetic
from pathlib import Path

from app import app, simulations_path
from dashboard.components import indicator

def layout():
    meta_manager = genetic.MetaManager(simulations_path)
    simulations = meta_manager.get_simulations()
    meta_info = meta_manager.get_meta_info()
    measure_attributes = [a for a in meta_info.member_attributes if a.role == genetic.AttributeRole.KPI or a.role == genetic.AttributeRole.Measure]
    dimension_attributes = [a for a in meta_info.member_attributes if a.role == genetic.AttributeRole.Dimension]

    return [

        # top controls
        html.Div(
            [
                html.Div(
                    [dcc.Dropdown(
                        id="simulation",
                        options=[{"label": sim, "value": sim} for sim in simulations],
                        value=simulations[0],
                        clearable=False,
                    )],
                    className="two columns",
                    style={"marginBottom": "10"},
                ),
                html.Div(
                    [dcc.Dropdown(
                            id="member_kpi",
                            options=[{"label": a.label, "value": a.name} for a in measure_attributes],
                            value=measure_attributes[0].name,
                            clearable=False,
                    )],
                    className="two columns",
                    style={"marginBottom": "10"},
                ),
                html.Div(
                    [dcc.Dropdown(
                            id="member_dimension",
                            options=[{"label": a.label, "value": a.name} for a in dimension_attributes],
                            clearable=True,
                    )],
                    className="two columns",
                    style={"marginBottom": "10"},
                ),

            ],
            className="row",
            style={},
        ),

        # indicators div 
        html.Div(
            [
                indicator(
                    "#00cc96",
                    "Generation",
                    "generation_indicator",
                ),
                indicator(
                    "#119DFF",
                    "Rating",
                    "middle_cases_indicator",
                ),
                indicator(
                    "#EF553B",
                    "Exhaustion",
                    "right_cases_indicator",
                ),
            ],
            className="row",
        ),


        html.Div(
            [
                html.Div(
                    [
                        html.P("Population over time"),

                        dcc.Graph(
                            id="population_over_time",
                            config=dict(displayModeBar=False),
                            style={"height": "89%", "width": "98%"},
                        ),

                    ],
                    className="six columns chart_div",
                ),

                html.Div(
                    [
                        html.P("Measure"),
                        
                        dcc.Graph(
                            id="member_kpi_plot",
                            config=dict(displayModeBar=False),
                            style={"height": "89%", "width": "98%"},
                        ),
                    ],
                    className="six columns chart_div"
                ),
            ],
            className="row",
            style={"marginTop": "5px"},
        ),

    ]

# Generations indicator
@app.callback(
    Output("generation_indicator", "children"),
    [Input("simulation", "value")],
)
def update_generation_indicator(simulation):

    if simulation is None:
        layout = dict(annotations=[dict(text="No simulation available", showarrow=False)])
        return ""

    simulation_path = simulations_path.joinpath(simulation)
    report_manager = genetic.ReportManager(simulation_path)
    population_report = report_manager.read_population_report()
    generation = population_report["generation_prop"].max()
    return generation

@app.callback(
    Output("population_over_time", "figure"),
    [Input("simulation", "value")],
)
def update_population_over_time_summary(simulation):

    if simulation is None:
        layout = dict(annotations=[dict(text="No simulation available", showarrow=False)])
        return {"data": [], "layout": layout}

    simulation_path = simulations_path.joinpath(simulation)
    report_manager = genetic.ReportManager(simulation_path)
    population_report = report_manager.read_population_report()
    df = population_report

    # Format results
    data = [
        go.Scatter(
            x=df['generation_prop'],
            y=df['alive_measure'],
            name='active'
        ),
        go.Scatter(
            x=df['generation_prop'],
            y=df['exhausted_measure'],
            name='exhausted'
        ),
        go.Scatter(
            x=df['generation_prop'],
            y=df['dead_measure'],
            name='dead'
        )
    ]
        
    layout = go.Layout(
        xaxis=dict(showgrid=False),
        margin=dict(l=35, r=25, b=23, t=5, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {"data": data, "layout": layout}

# Member measure plot
@app.callback(
    Output("member_kpi_plot", "figure"),
    [
        Input("simulation", "value"),
        Input("member_kpi", "value"),
        Input("member_dimension", "value"),
    ],
)
def update_member_kpi_summary(simulation, kpi, dimension):
    
    if simulation is None or kpi is None:
        layout = dict(annotations=[dict(text="No results available", showarrow=False)])
        return {"data": [], "layout": layout}

    simulation_path = simulations_path.joinpath(simulation)
    report_manager = genetic.ReportManager(simulation_path)
    df = report_manager.read_member_report()

    # Format results
    if dimension is None:
        data = [
            go.Scatter(
                x=df['generation_prop'],
                y=df[kpi],
                mode='markers',
                name=kpi
            ),
        ]
    else:
        conditions = df[dimension].unique()
        data = [
            go.Scatter(
                x=df[df[dimension] == cond]['generation_prop'],
                y=df[df[dimension] == cond][kpi],
                mode='markers',
                name=str(cond)
            )
            for cond in conditions
        ]
        
    layout = go.Layout(
        xaxis=dict(showgrid=False),
        margin=dict(l=35, r=25, b=23, t=5, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {"data": data, "layout": layout}
