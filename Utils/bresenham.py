__author__ = 'Noam'

import numpy as np
#TODO use https://stackoverflow.com/questions/40884680/how-to-use-bresenhams-line-drawing-algorithm-with-clipping
#TODO for a bresenham with clipping implmentation.

# TODO use opengl/other to hardware accelarate this.
# TODO could also use opencv's line iterator
def get_point_list_bresenham_pixels(start, end):
    """

    :rtype : returns a list of all the pixls (2-tuples) that start at 'start' and end at 'end'
    """
    x1, y1 = start
    x2, y2 = end

    # notice start and end are not integers but we force them to be here.
    # this may be the wrong way to go, but this is what we have now
    x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)

    dx = x2 - x1
    dy = y2 - y1

    is_steep = abs(dy) > abs(dx)

    # rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # swap start and nd points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

            # reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()

    #TODO return this as np.ndaarray of ind, by collcting all the x and all the y, and then np.unravel_multi_index
    return points



def calculate_bresenham_xy(start, end):
    """
    :rtype : returns a ndarray of shape (n,2) of all the pixls (x,y) that start at 'start'=x,y and end at 'end'=x,y
    """
    x1, y1 = start
    x2, y2 = end

    # notice start and end are not integers but we force them to be here.
    # this may be the wrong way to go, but this is what we have now
    x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)

    dx = x2 - x1
    dy = y2 - y1

    is_steep = abs(dy) > abs(dx)

    # rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # iterate over bounding box generating points between start and end
    y = y1

    bb_range = range(x1, x2 + 1)
    points_xy = np.zeros((len(bb_range),2), dtype=np.int)

    for i, x in enumerate(bb_range):
        coord = (y, x) if is_steep else (x, y)
        points_xy[i,:] = np.asarray(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # reverse the list if the coordinates were swapped
    if swapped:
        points_xy = np.flipud(points_xy)

    return points_xy


def bresenham(start, end):
    # return get_point_list_bresenham_pixels(start, end)
    return calculate_bresenham_xy(start, end)