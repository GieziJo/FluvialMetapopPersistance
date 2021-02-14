import numpy as np
import pyreadr as pr
from scipy.sparse import coo_matrix

class OCN:
    def __init__(self, path):
        self.path = path
        self.cellsize = pr.read_r(path + "cellsize.RData")
        self.cellsize = int(self.cellsize['cellsize'].cellsize[0])

        self.dimX = pr.read_r(path + "dimX.RData")
        self.dimX = int(self.dimX['dimX'].dimX[0])

        self.dimY = pr.read_r(path + "dimY.RData")
        self.dimY = int(self.dimY['dimY'].dimY[0])

        self.nodeNumber = np.reshape(range(self.dimX * self.dimY), (self.dimX, self.dimY))

        self.A = pr.read_r(path + "A.RData")
        self.A = np.reshape(np.array(self.A['A'].A),(self.dimX, self.dimY))

        self.dZ = pr.read_r(path + "slope.RData")
        self.dZ = np.reshape(np.array(self.dZ['slope'].slope),(self.dimX, self.dimY))

        self.A_p = pr.read_r(path + "A_p.RData")
        self.A_p = np.reshape(np.array(self.A_p['A_p'].A_p),(self.dimX, self.dimY))
        
        self.downNode = pr.read_r(path + "downNode.RData")
        self.downNode = np.array(self.downNode['downNode'].downNode) - 1
        self.outletNode = np.where(self.downNode == -1)[0][0]
        # self.downNode[self.downNode == -1] = self.outletNode
        self.downNode = np.reshape(self.downNode, (self.dimX, self.dimY))
        
        self.X = pr.read_r(path + "X.RData")
        self.X = np.reshape(np.array(self.X['X'].X),(self.dimX, self.dimY))
        self.Y = pr.read_r(path + "Y.RData")
        self.Y = np.reshape(np.array(self.Y['Y'].Y),(self.dimX, self.dimY))
        self.Z = pr.read_r(path + "Z.RData")
        self.Z = np.reshape(np.array(self.Z['Z'].Z),(self.dimX, self.dimY))

        W_i = pr.read_r(path + "W_i.RData")
        W_i = np.array(W_i['W_i'].W_i)-1

        W_j = pr.read_r(path + "W_j.RData")
        W_j = np.array(W_j['W_j'].W_j)-1

        W_x = pr.read_r(path + "W_x.RData")
        W_x = np.array(W_x['W_x'].W_x)

        W_Dim = pr.read_r(path + "W_Dim.RData")
        W_Dim = W_Dim['W_Dim'].W_Dim

        self.AD = coo_matrix((W_x, (W_i, W_j)), shape=W_Dim)
    
    
            

