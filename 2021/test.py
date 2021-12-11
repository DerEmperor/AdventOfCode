import numpy as np

data = np.array([[1, 2, 3], [4, 5, 6]])
x=0
y=0
if (x, y) not in np.ndindex(data.shape):
    print("no")
else:
    print("yes")