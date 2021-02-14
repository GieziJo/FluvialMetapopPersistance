import Source.OCN as OCN
import Source.lambdaAnalysis as lambdaAnalysis
import numpy as np

class AnalyseMultipleOCNs:
        
    def launchAnalysis(self, nSteps):
        self.las = []
        for k in range(39):
            print("starting " + str(k))
            path = 'Data/OCN_data_' + str(k) + '/'
            ocn = OCN.OCN(path)
            la = lambdaAnalysis.lambdaAnalysis(ocn)
            self.las.append(la)
            la.generateADMatrice()
            la.generateUpAndDownAD()
            la.computeDispersalAD()
            la.computeLmaxes_Thresh(nSteps)
            print("finished " + str(k))