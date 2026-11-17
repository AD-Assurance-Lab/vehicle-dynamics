# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
"""Lab 1 figures.  python3 make_figures.py  (run in this folder)
fit-sketch.png: the shape of the Task 3 plot, with no numbers on it."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(4.6, 3.1), dpi=150)
v = np.linspace(0, 1.05, 60)
ax.plot(v, v ** 2, lw=2.2, color="#2B5B84", label="d = v0² / (2 mu g), your mu")
x = np.array([.33, .5, .67, .83, 1.0])
ax.plot(x, x ** 2 + np.array([.04, .015, 0, 0, 0]), "o", ms=8, color="#B3261E", label="your five stops")
ax.set_xlabel("initial speed v0 (m/s)")
ax.set_ylabel("stopping distance d (m)")
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(0, 1.08); ax.set_ylim(0, 1.15)
ax.legend(loc="upper left", frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig("fit-sketch.png")
