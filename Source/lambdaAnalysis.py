import numpy as np
from scipy.sparse import coo_matrix
import networkx as nx
from scipy.sparse.linalg.eigen.arpack import eigsh as largest_eigsh
from os import path
import pickle

class lambdaAnalysis:
    def __init__(self, OCN):
        self.OCN = OCN
        self.areaThr = {}
        
        outlet_area = self.OCN.A[self.OCN.nodeNumber == self.OCN.outletNode]
        self.alpha = np.log(self.OCN.cellsize) / np.log(outlet_area)
        self.beta = np.log(3) / np.log(outlet_area)
    
    def generateADMatrice(self):
        print("Genearting AD matrice")
        basin_i = self.OCN.outletNode
        shed = np.ones(self.OCN.A.shape)
        shed[self.OCN.nodeNumber == basin_i] = 0
        node = self.OCN.nodeNumber[shed == 1]
        downNode = self.OCN.downNode[shed == 1]
        data = np.ones(downNode.shape)
        forward = np.concatenate((node, downNode))
        backward = np.concatenate((downNode, node))
        link = np.concatenate((data, -data))
        self.ADshedOutlet = coo_matrix((link, (forward, backward)), shape=(self.OCN.AD.shape))
        print("Done")

    def generateUpAndDownAD(self):
        
        print("Genearting UDAD")
        upPath = self.OCN.path + "upMatrix.obj"
        downPath = self.OCN.path + "downMatrix.obj"
        if path.exists(upPath):
            filehandler = open(upPath,'rb')
            self.NU = pickle.load(filehandler)
            filehandler.close()

            filehandler = open(downPath,'rb')
            self.ND = pickle.load(filehandler)
            filehandler.close()
        else:
            shortest_paths_pairsPath = self.OCN.path + "shortest_paths_pairs.obj"
            if path.exists(shortest_paths_pairsPath):
                filehandler = open(shortest_paths_pairsPath,'rb')
                shortest_paths_pairs = pickle.load(filehandler)
                filehandler.close()
            else:
                shortest_paths_pairs = dict(nx.all_pairs_shortest_path(nx.from_scipy_sparse_matrix(self.OCN.AD)))
                
                filehandler = open(shortest_paths_pairsPath,'wb')
                pickle.dump(shortest_paths_pairs, filehandler)
                filehandler.close()

            ad_shed = self.ADshedOutlet
            self.ND = np.zeros([self.OCN.dimX*self.OCN.dimY, self.OCN.dimX*self.OCN.dimY])
            self.NU = self.ND.copy()


            addok = ad_shed.todok()
            addokp = addok == 1
            addokn = addok == -1
            for node_i in shortest_paths_pairs:
                print("node_i"+str(node_i))
                for node_j in shortest_paths_pairs[node_i]:
                    if(node_i != node_j):
                        self.NU[node_i, node_j] = np.sum(addokp[shortest_paths_pairs[node_i][node_j][0:-1],shortest_paths_pairs[node_i][node_j][1:]])
                        self.ND[node_i, node_j] = np.sum(addokn[shortest_paths_pairs[node_i][node_j][0:-1],shortest_paths_pairs[node_i][node_j][1:]])

            filehandler = open(upPath,'wb')
            pickle.dump(self.NU, filehandler)
            filehandler.close()
                    
            filehandler = open(downPath,'wb')
            pickle.dump(self.ND, filehandler)
            filehandler.close()
        print("Done")
    
    def computeDispersalAD(self, a=.26, b=.03, w_u = 1):
        L = self.ND + w_u * self.NU
        self.K = a**L + b**2 / (L**2+b**2)

        for k in range(self.K.shape[0]):
            self.K[k,:] = self.K[k,:] / np.sum(self.K[k,:])

        np.fill_diagonal(self.K,0)
    
    def computeFitnessFromThreshold(self, n_i):
        Area = self.areaThr[n_i]
        
        Surface = (Area**self.alpha * Area**self.beta).flatten()
        self.F = np.outer(Surface, Surface)

    def computeLandscapeMatrix(self):
        self.M = self.F * self.K

    def setThresholdMask(self, amplitudeMin = 0, amplitudeMax = 10, nSteps = 9, step_i = 0):
        amplitude_steps = np.linspace(0, np.pi/2, num=nSteps)
        b = amplitudeMin
        m = (amplitudeMax - amplitudeMin) / (1.0)
        amplitudeRange = np.sin(amplitude_steps) * m + b
        amplitude = amplitudeRange[step_i]

        dZ_A = np.sqrt(self.OCN.dZ) * self.OCN.A
        thr = np.min(dZ_A)
        self.thrMask = dZ_A > (thr * amplitude)
    
    def computeNewAreaFromThresholdMask(self, n_i):
        self.areaThr[n_i] = np.copy(self.OCN.A / self.OCN.cellsize**2)

        rootCells = ~self.thrMask
        rootNodeNumbers = self.OCN.nodeNumber[rootCells]

        for rootNodeNumber in rootNodeNumbers:
            currentNode = rootNodeNumber
            while(currentNode != -1):
                self.areaThr[n_i][self.OCN.nodeNumber == int(currentNode)] -= 1
                currentNode = self.OCN.downNode.flatten()[int(currentNode)]
        
        self.areaThr[n_i] *= self.OCN.cellsize**2
    
    def computeLmaxes_Thresh(self, nSteps):
        self.LM = np.zeros(nSteps)
        self.LM_vect = {}
        for n_i in range(nSteps):
            print("computing step " + str(n_i))
            self.setThresholdMask(nSteps = nSteps, step_i = n_i)
            self.computeNewAreaFromThresholdMask(n_i)
            self.computeFitnessFromThreshold(n_i)
            self.computeLandscapeMatrix()

            evals_large_sparse, evecs_large_sparse = largest_eigsh(self.M, 1, which='LA')
            self.LM[n_i] = evals_large_sparse
            self.LM_vect[n_i] = evecs_large_sparse
