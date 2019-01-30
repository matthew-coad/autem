#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

def build_layout():
    layout = html.Div([
        html.Div(
            className="app-header",
            children=[
                html.Div('Plotly Dash', className="app-header--title")
            ]
        ),
        html.Div(
            children=html.Div([
                html.H5('Overview'),
                html.Div('''
                    This is an example of a simple Dash app with
                    local, customized CSS.
                ''')
            ])
        )
    ])
    return layout

def main():
    debug = True
    app = dash.Dash(__name__)
    app.layout = build_layout()
    app.run_server(debug=debug)

if __name__ == '__main__':
    main()
