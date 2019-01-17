# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import flask
from pathlib import Path

tune_energy_simulations_path = Path("experiments", "tune_energy", "simulations")
test_simulations_path = Path("tests", "simulations")
simulations_path = test_simulations_path

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True


