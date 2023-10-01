import math

def cartesian_to_polar(coord):
    x, y = coord[0], coord[1]
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return int(r*100), int(math.degrees(theta))
