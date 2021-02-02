import numpy as np
import pandas as pd

arr = np.array([1, 2, 3, 4, 5])

print(arr)

mydataset = {
  'cars': ["BMW", "Volvo", "Ford"],
  'passings': [3, 7, 2]
}

myvar = pd.DataFrame(mydataset)

print(myvar)
