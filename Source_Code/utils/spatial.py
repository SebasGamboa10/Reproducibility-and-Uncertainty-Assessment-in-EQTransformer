from collections import namedtuple
from linecache import getline
from math import atan, degrees, tan, radians

import numpy as np
from pyproj import Proj, transform


def read_ascDEM(asc_filepath):
    """Reads digital elevation model ASC file



    Parameters
    ----------
    asc_filepath : str
        Path to ArcASCII format Digital Elevation Model file

    Returns
    -------
    x : np array
        Contains the points x coordinate
    y : np array
        Contains the points y coordinate
    cellsize : float
        Cell size
    zz : np 2d array
        2 dimension array containing elevation data

    """
    header = [getline(asc_filepath, i) for i in range(1, 7)]
    values = [float(line.split(' ')[-1].strip()) for line in header]
    ncols, nrows, xmin, ymin, cellsize, no_data = values

    xmax     = xmin + cellsize*(ncols - 1)
    ymax     = ymin + cellsize*(nrows - 1)
    x        = np.arange(xmin, xmax + cellsize, cellsize)
    y        = np.arange(ymin, ymax + cellsize, cellsize)
    # y = np.arange(ymax + cellsize, ymin, -cellsize)

    cellsize = float(cellsize)
    # zz       = np.loadtxt(asc_filepath, skiprows=6)[::-1]
    zz       = np.loadtxt(asc_filepath, skiprows=6)
    zz[zz == no_data] = np.nan

    return x, y, cellsize, zz


def trim_DEM(x, y, zz, xmin, xmax, ymin, ymax):
    """ Trim DEM

    Trims a digital elevation model some x and y coordinates extremes

    Parameters
    ----------
    x : np array
        Contains the points x coordinate
    y : np array
        Contains the points y coordinate
    zz : np 2d array
        2 dimension array containing elevation data
    xmin : float or int
        Minimum x
    xmax : float or int
        Maximum x
    ymin : float or int
        Minimum y
    ymax : float or int
        Maximum y

    Returns
    -------

    """
    imin = np.argmin(np.abs(x-xmin))
    imax = np.argmin(np.abs(x-xmax))
    jmin = np.argmin(np.abs(y-ymin))
    jmax = np.argmin(np.abs(y-ymax))

    x = x[imin:imax]
    y = y[jmin:jmax]
    zz = zz[imin:imax, jmin:jmax]
    return


def get_cartesian_corners_from_DEM(asc_filepath, cart_proj='5367'):
    """ Get cartesian corners from DEM

    Reads a digital elevation model in .asc format and WGS projection and
    returns a cartesian corners


    Parameters
    ----------
    dem : str
        Path to .asc file
    cart_proj_code : str
        EPSG cartesian projection code

    Returns
    -------
    grid : list
        Contains x, y and z np 3D arrays

    """
    geo_proj = Proj(init='epsg:4326')
    cart_proj = Proj(init='epsg:'+cart_proj)

    lon, lat, cellsize, zz = read_ascDEM(asc_filepath)
    x, y = [], []
    for longitude, latitude in zip(lon, lat):
        _x, _y = transform(geo_proj, cart_proj, longitude, latitude)
        x.append(_x)
        y.append(_y)


    return np.array(x), np.array(y), cellsize, zz


def get_profile_trend(x1, x2, y1, y2):
    """Determines trend between two points



    Parameters
    ----------
    x1 : float
        X coordinate of left profile extreme
    x2 : float
        X coordinate of right profile extreme
    y1 : float
        Y coordinate of left profile extreme
    y2 : float
        Y coordinate of right profile extreme

    Returns
    -------
    trend : float
        Azimuth direction in degrees

    """
    # xmin = min([x1, x2])
    # xmax = max([x1, x2])
    # ymin = min([y1, y2])
    # ymax = max([y1, y2])

    xmin = min(x1, x2)
    xmax = max(x1, x2)
    ymin = min(y1, y2)
    ymax = max(y1, y2)

    delta_x = xmax - xmin
    delta_y = ymax - ymin

    if x1 == xmin and y1 == ymin:
        trend = degrees(atan(delta_x/delta_y))
    elif x1 == xmin and y1 == ymax:
        trend = 180 - degrees(atan(delta_y/delta_x))
    elif x1 == xmax and y1 == ymax:
        trend = 180 + degrees(atan(delta_x/delta_y))
    else:
        trend = 360 - degrees(atan(delta_x/delta_y))

    return trend


def project_points(x1, x2, y1, y2, x, y):
    """Projects points to vertical profile plane

    Project points to a vertical profile plane

    Parameters
    ----------
    x1 : float
        X coordinate of left profile extreme
    x2 : float
        X coordinate of right profile extreme
    y1 : float
        Y coordinate of left profile extreme
    y2 : float
        Y coordinate of right profile extreme
    x : np 1d array
        X coordinate of points to project
    y : np 1d array
        Y coordinate of points to project

    Returns
    -------
    d : np 1d array
        Transformed horizontal coordinate of projected points
    """

    # Get profile trend
    trend = get_profile_trend(x1, x2, y1, y2)

    # Create auxiliary points that creates a perpendicular line to the profile
    # section with the original point
    x_aux = x + np.sin(np.deg2rad(trend+90))
    y_aux = y + np.cos(np.deg2rad(trend+90))

    # Slopes
    ## Perpendicular line 
    m1 = (y - y_aux) / (x - x_aux)
    ## Profile
    m2 = (y2 - y1) / (x2 - x1)

    # Intercepts
    ## Perpendicular line 
    b1 = y - m1*x
    ## Profile
    b2 = y1 - m2*x1

    # Intersection between profile and perpendicular line
    x_proj = (b2 - b1) / (m1 - m2)
    y_proj = m1*x_proj + b1

    # Transformation
    d = np.sin(np.deg2rad(trend))*x_proj + np.cos(np.deg2rad(trend))*y_proj
    d1 = np.sin(np.deg2rad(trend))*x1 + np.cos(np.deg2rad(trend))*y1
    d -= d1

    return d


def cross_section(x, y, zz, x1, x2, y1, y2, dp, cellsize):
    """ Cross section

    Gets the elevation profile between two points (x1, y1) and (x2, y2)

    Solves the 3 equation system for dx and dy unkwowns:

        dy/dx = ry/rx
        r  = sqrt(rx**2 + ry**2)
        dp = sqrt(dx**2 + dy**2)

    Parameters
    ----------
    x : np array
        Contains the points x coordinate
    y : np array
        Contains the points y coordinate
    zz : np 2d array
        2 dimension array containing elevation data
    x1 : float
        X coordinate of left profile extreme
    x2 : float
        X coordinate of right profile extreme
    y1 : float
        Y coordinate of left profile extreme
    y2 : float
        Y coordinate of right profile extreme
    dp : float
        Distance between profile points [m]
    cellsize : float
        Cell size

    Returns
    -------
    distance : np array
        X transformed coordinate
    elevation : np array
        Elevation data for point along profile
    xy_profile :  np 2D array
        Contains X and Y original coordinates of profile points
        [n_points, dimension]

    """
    rx = x2 - x1
    ry = y2 - y1
    r  = np.sqrt(rx**2 + ry**2)

    if rx == 0:
        dy = dp
        y_line = np.arange(y1, y2, dy)
        x_line = np.zeros(len(y_line)) + x1
    elif ry == 0:
        dx = dp
        x_line = np.arange(x1, x2, dx)
        y_line = np.zeros(len(x_line)) + y1
    else:
        dx = np.sqrt(dp**2 / (1 + ry**2/rx**2))
        dy = ry/rx * dx
        x_line = np.arange(x1, x2, dx)
        y_line = np.arange(y1, y2, dy)

    xy_profile = np.transpose(np.array([x_line, y_line]))

    distance = np.arange(0, r, dp)

    dx = cellsize
    dy = cellsize

    elevation = np.zeros(distance.shape)
    for i, _  in enumerate(x_line):
        distances_x = abs(x - x_line[i])
        distances_y = abs(y - y_line[i])
        elevation[i] = zz[::-1][np.argmin(distances_y)][np.argmin(distances_x)]

    return distance, elevation, xy_profile


def get_profile_extremes(xc, yc, azimuth, rx, ry):
    """Get profile extremes

    Calculates the coordinantes of the extremes of a cross-section profile with
    azimuth, passing at center point (xc, yc) and bounded by a box 2rx by 2ry
    centered at (xc, yc).

                                    (x2, y2)
                        _________________*______
                        |           | a /       |
                        |           |  /        |
                        |       ry  | /         |
                        |  rx       |/          |
                        |- - - - - -*- - - - - -|
                        |          /| (xc, yc)  |
                        |         / |           |
                        |        /  |           |
                        |       /   |           |
                        _______*____|____________
                            (x1, y1)

    Intersection points with the 4 lines composing the bounding box are
    obtained by solving the linear equations:
        y = ax + b
        x = (y - b)/a


    Parameters
    ----------
    xc : float
        X coordinate of the center point
    yc : float
        Y coordinate of the center point
    azimuth : float
        Azimuth direction in degrees
    rx : float
        Distance between the center point and the bounding box in the X
        direction
    ry : float
        Distance between the center point and the bounding box in the Y
        direction

    Returns
    -------
    x1 : float
        X coordinate of the section extreme to the left
    x2 : float
        X coordinate of the section extreme to the right
    y1 : float
        Y coordinate of the section extreme to the left
    y2 : float
        Y coordinate of the section extreme to the right

    """
    xmin = xc - rx/2
    xmax = xc + rx/2
    ymin = yc - ry/2
    ymax = yc + ry/2

    if azimuth >= 180:
        azimuth -= 180
    if azimuth == 0:
        return xc, xc, ymin, ymax
    elif azimuth == 90:
        return xmin, xmax, yc, yc

    angle = 90 - azimuth
    a = tan(radians(angle))
    b = yc - a * xc

    intersections = []
    Point = namedtuple('Point', ['x', 'y'])
    for x, y in zip([xmin, xmax], [ymin, ymax]):
        intersections.append(Point(x=x, y=a*x+b))
        intersections.append(Point(x=(y-b)/a, y=y))

    points_x, points_y = [], []
    for point in intersections:
        if point.x == xmin and point.y >= ymin and point.y <= ymax:
            points_x.append(point)
            points_y.append(point)
        elif point.x == xmax and point.y >= ymin and point.y <= ymax:
            points_x.append(point)
            points_y.append(point)
        elif point.y == ymin and point.x >= xmin and point.x <= xmax:
            points_x.append(point)
            points_y.append(point)
        elif point.y == ymax and point.x >= xmin and point.x <= xmax:
            points_x.append(point)
            points_y.append(point)

    x1 = min([p.x for p in points_x])
    x2 = max([p.x for p in points_x])
    for point in points_y:
        if point.x == x1:
            y1 = point.y
        else:
            y2 = point.y

    return x1, x2, y1, y2


def deg2km(distance):
    return distance * (2.0 * 6371 * np.pi / 360.0)
