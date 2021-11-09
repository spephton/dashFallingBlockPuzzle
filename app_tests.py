import app
import numpy as np

def main():
    
    # Shape unit tests
    
    ## get_points_from:
    s_piece_points = app.Shape.get_points_from(np.array([[0, 1, 1],
                                                        [1, -1, 0]]))
    assert s_piece_points == [(-1, 0), (-1, 1), (0, -1)]
    
    ### No anchor 
    try:
        _ =  app.Shape.get_points_from(np.array([[0, 1, 1],
                                                [1, -1, 0]]))
        assert False
    except ValueError as ve:
        pass
    


if __name__ == "__main__":
    main()