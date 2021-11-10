import app
import numpy as np

def main():
    
    # Unit tests
    
    ## get_points_from():
    s_piece_points = app.get_points_from(np.array([[0, 1, 1],
                                                        [1, -1, 0]]))
    assert s_piece_points == [(-1, 0), (-1, 1), (0, -1)]
    print(type(s_piece_points))
    
    # No anchor 
    try:
        _ =  app.get_points_from(np.array([[0, 1, 1],
                                                [1, 1, 0]]))
        assert False # Exception not thrown
    except ValueError:
        pass
    
    print(app.gridular_rotate(s_piece_points))


if __name__ == "__main__":
    main()