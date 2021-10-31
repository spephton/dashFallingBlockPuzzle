import dash
import dash_html_components as html
import dash_core_components as dcc
import json
import plotly.express as px
import numpy as np
import random
from dash.dependencies import Output, Input
from dash_extensions import Keyboard
from enum import Enum

## Classes
class GameController:
	'''Responds to player and drop-clock inputs and maintains the game state array'''
	
	class ActivePiece:
	    
	    def __init__(self, *, shape, coord):
	        self._shape = shape # should be string from shapes tuple
	        self._coord = coord # should be 
	    
	
	## Properties
	class Shapes(Enum):
	    SQUARE = 0,
	    IPIECE = 1,
	    SPIECE = 2,
	    ZPIECE = 3,
	    TPIECE = 4,
	    LPIECE = 5,
	    FPIECE = 6,
	
	defaultMapping = (
	    # square
	    (np.array([[0, 0, 0, 0],
	              [0, 1, 1, 0],
	              [0, -1, 1, 0],
	              [0, 0, 0, 0]]), # -1 marks the anchor point of the shape
	    0), # no. of rotations. squares don't rotate in tetris
	)	
	                
	shapes = ('square', 'iPiece', 'sPiece', 'zPiece', 'tPiece', 'lPiece', 'fPiece') # TODO should use an enum
	
	
	## Methods
	def _getRandShape(self) -> str:
	    return shapes[random.randrange(0,len(shapes))]
	
	def dropNewPiece(self, shape = 'rand'):
		if shape == 'rand':
			shape = self.shapes(random.randrange(0,len(shapes) - 1))
		
		
		
	def __init__(self, gameState = None):
		if gameState == None:
			self.gameState = {
				'playfield': np.zeros((24, 10), dtype = np.int8), # an empty playfield
				'level': 0,
				'activePiece': None
			}
			

## Variables TODO get rid of these and pass them instead Dash is not designed to work with globals

framebuffer = np.array([np.array([np.zeros(3, dtype = np.uint8) for i in range(10)]) for i in range(20)]) # 20 rows of 10 columns of 8 bit rgb

fig = px.imshow(framebuffer)

## Layout
app = dash.Dash(__name__)
app.layout = html.Div([
	Keyboard(id = 'keyboard'),
	html.Div(id = 'keydown-output'),
	html.Div(id = 'keyup-output'),
	dcc.Graph(id = 'video', figure = fig)
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

if __name__ == "__main__":
    app.run_server(debug = True)