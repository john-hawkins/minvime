import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

M = 300
b = 30
c = 15
x = np.linspace(0,99,100)
ll = (c/b)*x
ul = (c/b)*x + (M/b)
fplim = (30-(M/b)) * (b/c)

fig = plt.figure(figsize=(12,5))
ax = fig.add_subplot(111)
ax.plot(x, ll, '--r', lw=1, label='$tp = \\frac{C \cdot fp}{B}$')
ax.plot(x, ul, '-k', lw=1, label='$tp = \\frac{C \cdot fp - M}{B}$')
ax.plot([0,0], [M/b,100], ':b', lw=5, label="$N \cdot r - \\frac{M}{B}$")
ax.plot([0,fplim], [30,30], ':g', lw=5, label="$\\frac{B}{C} \cdot (N \cdot r - \\frac{M}{B})$")


ax.set_xlim(0, 90)
ax.set_ylim(0, 30)
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.xlabel('False Positives (fp) : Max = $N \cdot (1-r)$')
plt.ylabel('True Positives (tp) : Max  = $N \cdot r$')
plt.legend(loc='lower right')

plt.savefig("../paper/images/simplicity.png")



