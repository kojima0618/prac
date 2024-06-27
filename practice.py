import psutil
import random

'''b1 = psutil.virtual_memory()
NN = 10000000
X = {k: random.random() for k in range(NN)}
b2 = psutil.virtual_memory()
print(b2.used - b1.used)
print(b1)
print(b2)'''

import memory_profiler as MP
import gc
import random

b1 = MP.memory_usage()[0]
NN = 10_000_000
X = {k: random.random() for k in range(NN)}
b2 = MP.memory_usage()[0]
print(b2 - b1)