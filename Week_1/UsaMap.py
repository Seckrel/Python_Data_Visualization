"""
Week 1 practice project template for Python Data Visualization
Load a county-level PNG map of the USA and draw it using matplotlib
"""

import matplotlib.pyplot as plt
from xml.dom import minidom
import re
import functools
import pprint
# Houston location

USA_SVG_SIZE = [555, 352]
PP = pprint.PrettyPrinter(indent=4)


def draw_USA_map(map_name):
    """
    Given the name of a PNG map of the USA (specified as a string),
    draw this map using matplotlib
    """

    # Load map image, note that using 'rb'option in open() is critical since png files are binary
    svg = minidom.parse("./Datasets/USA_Counties_2014.svg")
    svg = [path.getAttribute('d') for path in svg.getElementsByTagName('path')][:-2]
    svg = [re.split("[LMCz]", a)[1:] for a in svg]  # creatte list of coordinate by removing L, M, and C from <path d="...">
    points = []  # Stores points in float form, here points are x, and y coordinate for boundry
    for setPoint in svg:
        temp = []
        for point in setPoint:
            splited = point.split(",")
            try:
                temp.append([float(splited[0]), float(splited[1])])
            except:
                temp.append([0,0])
        points.append(temp)

    length = list(map(lambda x: len(x), points))  # Number of x, and y coordinate representing boundry of county
    midPoint = list(map(lambda x: functools.reduce(
        lambda a,b: [a[0]+b[0], a[1]+b[1]], x
    ), points))  # gets sum of x, and y points of each country's boundry

    midPoint = list(map(lambda p,l: [p[0]/l, p[1]/l], midPoint, length))  # gets midpoint of each country, by dividing sum by length
    PP.pprint(len(midPoint))
    usaMap = plt.imread('./Datasets/' + map_name, format='png')

    #  Get dimensions of USA map image
    newHeight = len(usaMap)
    newWidth = len(usaMap[0])
    adjustedPoints = list(map(lambda x: [
        (x[0]/USA_SVG_SIZE[0]) * newWidth,
        (x[1]/USA_SVG_SIZE[1]) * newHeight
    ], midPoint))
    # Plot USA map

    plt.imshow(usaMap)

    # Plot green scatter point in center of map
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(adjustedPoints)
    plt.scatter(*list(zip(*adjustedPoints)), c='green',marker='.',linewidths=0.2)

    # Plot red scatter point on Houston, Tx - include code that rescale coordinates for larger PNG files

    plt.show()
    plt.close()


# draw_USA_map("USA_Counties_555x352.png")
draw_USA_map("USA_Counties_1000x634.png")