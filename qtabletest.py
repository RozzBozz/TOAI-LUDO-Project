import numpy as np

QTable = np.load("QTables/epsilon0.9alpha0.25gamma0.7.npy")
np.set_printoptions(threshold=np.inf)
#print(QTable.max())
#print(QTable.min())
print(QTable)
