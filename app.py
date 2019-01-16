# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import flask

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True
