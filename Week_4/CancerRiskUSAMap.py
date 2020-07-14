import matplotlib.pyplot as plt
import csv
import matplotlib
import functools
import matplotlib.cm as cm
import pprint
import operator
import matplotlib

USA_SVG_SIZE = [555, 352]
PP = pprint.PrettyPrinter(indent=4)


def read_csv_file(file_name):
    """
    Given a CSV file, read the data into a nested list
    Input: String corresponding to comma-separated  CSV file
    Output: Nested list consisting of the fields in the CSV file
    """

    with open(file_name, newline='') as csv_file:  # don't need to explicitly close the file now
        csv_table = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_table.append(row)
    return csv_table


def draw_USA_map(map_name, mid_points, area):
    """
    Given the name of a PNG map of the USA (specified as a string),
    draw this map using matplotlib
    """

    # Load map image, note that using 'rb'option in open() is critical since png files are binary
    usaMap = plt.imread(map_name, format='png')

    #  Get dimensions of USA map image
    newHeight = len(usaMap)
    newWidth = len(usaMap[0])
    adjusted_area = list(map(lambda x: x*(newHeight*newWidth) if x*(newWidth*newHeight)>1 else x*(newHeight*newWidth)*50, area))
    adjustedPoints = list(map(lambda x: [
        (x[2]/USA_SVG_SIZE[0]) * newWidth,
        (x[3]/USA_SVG_SIZE[1]) * newHeight
    ], mid_points))
    # Plot USA map
    plt.imshow(usaMap)
    risk_val = list(map(operator.itemgetter(1), mid_points))
    color_map = matplotlib.cm.ScalarMappable(
        norm=matplotlib.colors.Normalize(vmin=min(risk_val), vmax=max(risk_val)),
        cmap=cm.get_cmap('jet')
    )
    color_val = color_map.to_rgba(risk_val)

    # Plot green scatter point in center of map
    plt.scatter(*list(zip(*adjustedPoints)),linewidths=0, s=adjusted_area,c=color_val)

    # Plot red scatter point on Houston, Tx - include code that rescale coordinates for larger PNG files
    plt.savefig("./new.png")
    plt.show()
    plt.close()


def draw_cancer_risk_map(joined_csv_file_name, map_name, num_counties=None):
    joined_csv = read_csv_file(joined_csv_file_name)
    mid_points = [(int(p[3]),float(p[4]), float(p[5]), float(p[6])) for p in joined_csv]
    mid_points.sort(key=lambda x: x[0], reverse=True)
    total_population, *_ = functools.reduce(lambda a, b: (a[0] + b[0],), mid_points)
    if num_counties:
        mid_points = [p for p in mid_points[:num_counties]]
    area = list(map(lambda x: compute_county_circle(x[0], total_population), mid_points))
    draw_USA_map(map_name, mid_points, area)


def compute_county_circle(county_population, total_pop):
    return 3.14 * (county_population/total_pop)**2



draw_cancer_risk_map("../Week_3/Datasets/cancer_risk_joined.csv", "../Week_1/Datasets/USA_Counties_1000x634.png")