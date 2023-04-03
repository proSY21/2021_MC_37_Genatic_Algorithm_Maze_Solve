import matplotlib.pyplot as plt
import numpy as np

sizes = [5, 10, 12, 15]
times1 = [0.005095005, 0.208242178, 0.47719388, 5.771011353]
times2 = [0.002477884, 0.388456345, 0.36933279, 6.419968128]
times3 = [0.00094533, 0.089000225, 0.945460558, 4.283327341]
times4 = [0.008844614, 0.062156439, 1.361827612, 4.817198753]
times5 = [0.00199461, 0.107887506, 0.474394846, 6.943977594]

fig, ax = plt.subplots()

ax.plot(sizes, times1, label='Run1')
ax.plot(sizes, times2, label='Run2')
ax.plot(sizes, times3, label='Run3')
ax.plot(sizes, times4, label='Run4')
ax.plot(sizes, times5, label='Run5')

ax.set_xlabel('Size')
ax.set_ylabel('Time')
ax.legend()

plt.show()
