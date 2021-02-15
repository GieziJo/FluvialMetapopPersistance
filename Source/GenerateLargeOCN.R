setwd(dirname(getActiveDocumentContext()$path))
library(spam)
library(OCNet)

for(i in 1:40) {
  k = i - 1
  targetPath <- paste("../Data/OCN_data_", k, sep="")

  dir.create(targetPath)
  
  ocn <- OCNet::create_OCN(64,64,nIter = 10000, cellsize = 60)
  
  landscape <- OCNet::landscape_OCN(ocn, slope0 = 0.0075)
  
  paths <- OCNet::paths_OCN(OCNet::aggregate_OCN(landscape))
  
  save(ocn, file=paste(targetPath,"/ocn.RData" ,sep=""))
  
  cellsize <- ocn$cellsize
  save(cellsize, file = paste(targetPath,"/cellsize.RData" ,sep=""))
  
  # save ocn$FD$A, ocn$FD$W, ocn$FD$downNode, ocn$FD$X, ocn$FD$Y, landscape$FD$Z
  dimX <- ocn$dimX
  save(dimX, file = paste(targetPath,"/dimX.RData" ,sep=""))
  
  dimY <- ocn$dimY
  save(dimY, file = paste(targetPath,"/dimY.RData" ,sep=""))
  
  A <- ocn$FD$A
  save(A, file = paste(targetPath,"/A.RData" ,sep=""))
  
  A_p <- A / ocn$cellsize^2
  save(A_p, file = paste(targetPath,"/A_p.RData" ,sep=""))
  
  W <- as.data.frame(summary(as.dgCMatrix.spam(ocn$FD$W)))
  
  W_i <- W$i
  W_j <- W$j
  W_x <- W$x
  W_Dim <- W_Dim <- ocn$FD$W@dimension
  
  save(W_i, file = paste(targetPath,"/W_i.RData" ,sep=""))
  save(W_j, file = paste(targetPath,"/W_j.RData" ,sep=""))
  save(W_x, file = paste(targetPath,"/W_x.RData" ,sep=""))
  save(W_Dim, file = paste(targetPath,"/W_Dim.RData" ,sep=""))
  
  downNode <- ocn$FD$downNode
  save(downNode, file = paste(targetPath,"/downNode.RData" ,sep=""))
  
  X <- ocn$FD$X
  save(X, file = paste(targetPath,"/X.RData" ,sep=""))
  
  Y <- ocn$FD$Y
  save(Y, file = paste(targetPath,"/Y.RData" ,sep=""))
  
  Z <- landscape$FD$Z
  save(Z, file = paste(targetPath,"/Z.RData" ,sep=""))
  
  slope <- landscape$FD$slope
  save(slope, file = paste(targetPath,"/slope.RData" ,sep=""))
  
}