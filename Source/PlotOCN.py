import numpy as np

def plotNetwork(ocn, axis):
    for x_i in range(ocn.dimX):
        for y_i in range(ocn.dimY):
            dn = ocn.downNode[x_i, y_i]
            if dn != -1:
                position = np.where(ocn.nodeNumber == dn)
                position = (position[0][0], position[1][0])

                axis.plot(np.array([y_i,position[1]]), np.array([x_i, position[0]]),'r-')

def plotNetworkLineWidths(ocn, axis):
    a_min = 1
    a_max = np.max(ocn.A_p.flatten())

    linewidth_min = .2
    linewidth_max = 1.5
    for x_i in range(ocn.dimX):
        for y_i in range(ocn.dimY):
            dn = ocn.downNode[x_i, y_i]
            if dn != -1:
                position = np.where(ocn.nodeNumber == dn)
                position = (position[0][0], position[1][0])

                rescaled = (ocn.A_p[x_i, y_i] - a_min) / (a_max - a_min)

                linewidth = rescaled * (linewidth_max - linewidth_min) + linewidth_min

                axis.plot(np.array([y_i,position[1]]), np.array([x_i, position[0]]),'r-', linewidth=linewidth)

def plotNetworkLineWidthsCustomArea(ocn, Area, a_min, a_max, axis):
    # a_min = np.min(Area.flatten())
    # a_max = np.max(Area.flatten())

    linewidth_min = .2
    linewidth_max = 1.5
    for x_i in range(ocn.dimX):
        for y_i in range(ocn.dimY):
            dn = ocn.downNode[x_i, y_i]
            if dn != -1 and Area[x_i, y_i] > 0:
                position = np.where(ocn.nodeNumber == dn)
                position = (position[0][0], position[1][0])

                rescaled = (Area[x_i, y_i] - a_min) / (a_max - a_min)

                linewidth = rescaled * (linewidth_max - linewidth_min) + linewidth_min

                axis.plot(np.array([y_i,position[1]]), np.array([x_i, position[0]]),'b-', linewidth=linewidth)