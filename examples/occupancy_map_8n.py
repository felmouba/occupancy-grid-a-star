#!/localdisk/python3-venv/bin/python
import os
import sys
import matplotlib.pyplot as plt

parent_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
if parent_folder not in sys.path:
    sys.path.append(parent_folder)

from gridmap import OccupancyGridMap
import matplotlib.pyplot as plt
from a_star import a_star
from utils import plot_path


if __name__ == '__main__':
    # load the map
    #gmap = OccupancyGridMap.from_png('maps/example_map_occupancy.png', 1)
    gmap = OccupancyGridMap.from_png('maps/sample_map.png', 1)

    # set a start and an end node (in meters)
    start_node = (260.0, 400.0)
    goal_node = (540.0, 170.0)
    #goal_node = (400.0, 170.0)

    # run A*
    path, path_px = a_star(start_node, goal_node, gmap, movement='8N')

    gmap.plot()

    if path:
        # plot resulting path in pixels over the map
        plot_path(path_px)
    else:
        print('Goal is not reachable')

        # plot start and goal points over the map (in pixels)
        start_node_px = gmap.get_index_from_coordinates(start_node[0], start_node[1])
        goal_node_px = gmap.get_index_from_coordinates(goal_node[0], goal_node[1])

        plt.plot(start_node_px[0], start_node_px[1], 'ro')
        plt.plot(goal_node_px[0], goal_node_px[1], 'go')

    plt.show()
