import dash
import dash_html_components as html
import dash_core_components as dcc
import json
import plotly.express as px
import numpy as np
from dash.dependencies import Output, Input
from dash_extensions import Keyboard

## Functions


## Variables

framebuffer = np.array([np.array([np.zeros(3, dtype = np.uint8) for i in range(10)]) for i in range(20)])

fig = px.imshow(framebuffer)

## Layout
app = dash.Dash(__name__)
app.layout = html.Div([
	Keyboard(id = 'keyboard'),
	html.Div(id = 'keydown-output'),
	html.Div(id = 'keyup-output'),
	dcc.Graph(id = 'playfield', figure = fig)
	])

## Callbacks
@app.callback(
	Output(component_id = 'keydown-output', component_property = 'children'), # was so confused to be getting errors with a previous variable name here. turned out I needed to reload the page, presumably client-side JS didn't know what to do. 
	Input('keyboard', 'keydown')
)
def keydown(event):
    return json.dumps(event)
    
@app.callback(
	Output(component_id = 'keyup-output', component_property = 'children'), # was so confused to be getting errors with a previous variable name here. turned out I needed to reload the page, presumably client-side JS didn't know what to do. 
	Input('keyboard', 'keyup')
)
def keyup(event):
    return json.dumps(event)

if __name__ == "__main__"":
    app.run_server(debug = True)