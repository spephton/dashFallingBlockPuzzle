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

# Classes

class Colors(Enum):
        WHITE = np.array([255,255,255], np.uint8)

class Shape:
    '''All play pieces are shapes.'''
    def __init__(self, *, default_mapping, color = Colors.WHITE,
                 rotation_cycle_length = 4):
        
        self.default_mapping = default_mapping
        self.color = color
        self.current_rotindex = 0
        self.rotation_cycle_length = rotation_cycle_length
        self.points = [self.get_points_from(default_mapping)]
        
        for _ in range(rotation_cycle_length):
            points.append(self.gridular_rotate(points[-1]))
        
    # instance methods
    
    def _next_index(self):
        return (self.current_rotindex + 1) % self.rotation_cycle_length
        
    def current_points(self):
        return self.points[self.current_rotindex]
        
    def next_points(self):
        return self.points[self._next_index()]
        
    def rotated_points(self):
        self.current_rotindex = self._next_index()
        return self.currentPoints()
    
    
    
    


class ActivePiece:
    def __init__(self, *, shape, coord):
        self._shape = shape # should be string from shapes tuple
        self._coord = coord # should be  


class GameController:
    '''Responds to player and drop-clock inputs and maintains the game state array'''
    
    ## Properties
    class Shapes(Enum):
        SQUARE = 0,
        IPIECE = 1,
        SPIECE = 2,
        ZPIECE = 3,
        TPIECE = 4,
        LPIECE = 5,
        FPIECE = 6,
    
        
    default_mapping = ( # instead of each piece's properties in a tuple we could make them 
                       # objects and store them in the enum directly.
                       # This'd be neater but we'll stick with the tuple for now. 
        # square
        (np.array([[0, 0, 0, 0],
                  [0, -1, 1, 0],
                  [0, 1, 1, 0],
                  [0, 0, 0, 0]]), # -1 marks the anchor point of the shape
        0), # no. of rotations. squares don't rotate in tetris
        # I piece
        (np.array([[0, 0, 0, 0],
        	      [1, -1, 1, 1], # For two-rotation symmetry we can make matrix transpose
                  [0, 0, 0, 0],  # the rotation function. Put the anchor point on the
                  [0, 0, 0, 0]]), # major axis so transpose doesn't move the anchor
        2), # two rotations: horizontal and vertical. transpose is 2-cycle operation
        # sPiece
        (np.array([[0, 1, 1, 0],
                  [1, -1, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]),
        0),
        
        
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
            
def gridular_rotate(points): 
    '''Given a list of points on a discrete 2d grid, rotate it 90 degrees clockwise about the origin'''
    new_points = []
    for point in points:
        new_points.append((point[1], -point[0]))
        #new_points.append((-point[1], point[0])) # CCW (array coord system)
    return new_points

def get_points_from(shape_mapping):
    '''Returns a list of points specifying filled positions in an array relative to an anchor. Input is a 2-d array. The 'anchor' is defined as the first entry (L->R, row by row) equal to '-1', and from the anchor the relative position of all cells equal to '1' is returned.'''
    anchor = None
    points = []
    for row_index in range(len(shape_mapping)):
        for column_index in range(len(shape_mapping[row_index])):
            if shape_mapping[row_index, column_index] == 1:
                points.append((row_index, column_index))
            elif shape_mapping[row_index, column_index] == -1:
                anchor = (row_index, column_index)
    if anchor == None: raise ValueError('Anchor not found in shape mapping')
    
    row, column = zip(*points) # moving origin to anchor
    new_row = (row - anchor[0] for row in row) 
    new_column = (column - anchor[1] for column in column)
    points = list(zip(new_row, new_column))
    return points




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