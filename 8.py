import numpy as np
import matplotlib.pyplot as plt

with open ("settings.txt", "r") as settings:
    tmp = settings.read().rsplit()
    sets = tmp[2] + " " + tmp[5]
    sets = sets.partition("V")[0]
    sets = float(sets.partition("Hz ")[0]), float(sets.partition("Hz ")[2])

data = np.loadtxt("data.txt", dtype=int)
data = data * sets[1]
time = np.array([i/sets[0] for i in range(data.size)])
print(time)
fig, ax = plt.subplots(figsize = (16, 10), dpi = 300)
line, = ax.plot(time, data, color='b', markersize=2, marker='.', markevery=50, linewidth=0.2)
ax.set(xlim=(0, 1.05 * max(time)), ylim=(0, 1.05 * max(data)))
ax.set_title("Процесс заряда и разряда конденсатора в RC-цепочке", loc='center')
ax.minorticks_on()
ax.grid(which='major', color='b', linestyle='-', linewidth=0.1)
ax.grid(which='minor', color='b', linestyle='--', linewidth=0.05)
ax.set_xlabel("Время, с")
ax.set_ylabel("Напряжение, В")
line.set_label("V (t)")
ax.legend()
ax.text(60, 2.5, "Время зарядки: {:.2f}c".format(time[data.argmax()]), size=7)
ax.text(60, 2.0, "Время зарядки: {:.2f}c".format(time.max() - time[data.argmax()]), size=7)
plt.show()
fig.savefig("graph.png")   