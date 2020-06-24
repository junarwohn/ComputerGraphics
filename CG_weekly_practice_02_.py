import numpy as np

# ID : 

# A
M = np.linspace(2, 26, 25)
print(M)

# B
M = M.reshape(5, 5)
print(M)

# C
M[:,0] = 0
print(M)

# D
M = M @ M
print(M)

# E
v = M[0]
mv = v @ v
mv = np.sqrt(mv)
print(mv)