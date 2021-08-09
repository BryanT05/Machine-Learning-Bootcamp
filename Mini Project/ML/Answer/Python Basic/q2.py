factorial = int(input())
num = 1
for i in range(2,factorial+1):
  num *= i
print(num)
# cara 2
import numpy as np
print(np.product([i for i in range(1,factorial+1)]))