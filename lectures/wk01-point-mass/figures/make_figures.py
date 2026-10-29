# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
"""Figures for Lecture 1A. Run from this folder: python3 make_figures.py
Data: carla-brake-sweep.json, from env/carla-vd-tests/brake_sweep.py
(CARLA 0.9.16, vehicle.lincoln.mkz_2020, full brake, flat OpenDRIVE test track)."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, FancyBboxPatch

BROWN, GOLD, GRAY = "#532E1F", "#C9A200", "#8A8A8A"
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13})
HERE = os.path.dirname(os.path.abspath(__file__))
g = 9.81
data = json.load(open(os.path.join(HERE, "carla-brake-sweep.json")))
v0 = np.array([d["v0"] for d in data]); dist = np.array([d["dist"] for d in data])


def clean(ax):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.grid(alpha=0.25)


# 1. stopping distance vs speed, CARLA vs point mass
hi = v0 >= 15
a_fit = np.sum(v0[hi]**4) / np.sum(2 * v0[hi]**2 * dist[hi])   # least squares on d = v^2/(2a)
v = np.linspace(0, 31, 200)
fig, ax = plt.subplots(figsize=(7, 4.3))
ax.plot(v, v**2 / (2 * a_fit), color=BROWN, lw=2.5, label=f"theory: d = v₀²/(2μg) on a fine grid of v₀, μ = {a_fit / 9.81:.2f}")
ax.plot(v0, dist, "o", color=GOLD, ms=9, mec=BROWN, label="CARLA: measured full-brake stops")
for vi, di in zip(v0, dist):
    ax.annotate(f"$v_0$ = {vi:.0f} m/s", (vi, di), xytext=(8, -14), textcoords="offset points", fontsize=9, color=GRAY)
ax.set_xlabel("initial speed (m/s)"); ax.set_ylabel("stopping distance (m)")
ax.legend(frameon=False); clean(ax)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "stopping-distance.png"), dpi=160)
print(f"fitted deceleration = {a_fit:.2f} m/s^2, mu = {a_fit / 9.81:.3f}")

# 2. speed trace during braking
fig, ax = plt.subplots(figsize=(7, 4.0))
for d, col in [(data[3], BROWN), (data[5], GOLD)]:
    t = np.array([p[0] for p in d["trace"]]); vx = np.array([p[1] for p in d["trace"]])
    ax.plot(t, vx, color=col, lw=2.5, label=f"CARLA from {d['v0']:.0f} m/s")
    ax.plot(t, np.maximum(d["v0"] - a_fit * t, 0), "--", color=GRAY, lw=1.5)
ax.plot([], [], "--", color=GRAY, label=f"theory: constant deceleration, {a_fit:.1f} m/s²")
ax.set_xlabel("time since brake applied (s)"); ax.set_ylabel("speed (m/s)")
ax.legend(frameon=False); clean(ax)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "braking-trace.png"), dpi=160)

# 3. free-body diagram of the point mass, braking on a flat road
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.set_xlim(-4, 4); ax.set_ylim(-1.6, 2.4); ax.axis("off"); ax.set_aspect("equal")
ax.plot([-4, 4], [-0.6, -0.6], color=GRAY, lw=2)
ax.add_patch(Circle((0, 0.4), 0.55, color=BROWN))
ax.text(0, 0.4, "m", color="white", ha="center", va="center", fontsize=16, fontweight="bold")
def arrow(x0, y0, x1, y1, label, lx, ly, col=BROWN):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=18, lw=2, color=col))
    ax.text(lx, ly, label, ha="center", va="center", fontsize=13)
arrow(0.6, 0.4, 2.6, 0.4, "", 0, 0, GRAY); ax.text(2.75, 0.4, "x, v", va="center", fontsize=13, color=GRAY)
arrow(-0.6, 0.6, -2.3, 0.6, "", 0, 0); ax.text(-2.45, 0.6, "$F_{aero}$", ha="right", va="center")
arrow(-0.6, 0.2, -1.8, 0.2, "", 0, 0); ax.text(-1.95, 0.2, "$F_{roll}$", ha="right", va="center")
arrow(-0.3, -0.78, -2.0, -0.78, "", 0, 0, GOLD); ax.text(-2.1, -1.1, "$F_x$ (braking, at the road)", ha="center", va="center")
arrow(0, -0.15, 0, -1.4, "", 0, 0); ax.text(0.25, -1.3, "$mg$", va="center")
arrow(0.9, -0.6, 0.9, 0.9, "", 0, 0, GRAY); ax.text(1.05, 1.0, "$N$", va="center")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fbd-point-mass.png"), dpi=160)

# 4. ISO 8855 vehicle frame, top view, and CARLA's frame
fig, axs = plt.subplots(1, 2, figsize=(8, 3.6))
for ax, title, ysign in [(axs[0], "ISO 8855 (this course)", 1), (axs[1], "CARLA / Unreal", -1)]:
    ax.set_xlim(-2.2, 3.2); ax.set_ylim(-2.2, 2.2); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(FancyBboxPatch((-1.2, -0.6), 2.4, 1.2, boxstyle="round,pad=0.05", color=GOLD, alpha=0.6))
    ax.add_patch(FancyArrowPatch((0, 0), (2.4, 0), arrowstyle="-|>", mutation_scale=18, lw=2, color=BROWN))
    ax.add_patch(FancyArrowPatch((0, 0), (0, 1.7 * ysign), arrowstyle="-|>", mutation_scale=18, lw=2, color=BROWN))
    ax.text(2.55, 0, "x forward", va="center", fontsize=12)
    ax.text(0.15, 1.85 * ysign, "y left" if ysign > 0 else "y right", va="center", fontsize=12)
    ax.text(-0.4, -0.25 if ysign > 0 else 0.25, "z up" if ysign > 0 else "z up", fontsize=11, color=BROWN)
    ax.set_title(title, color=BROWN, fontweight="bold", fontsize=13)
axs[0].text(-1.9, -1.9, "right-handed", fontsize=11, color=GRAY)
axs[1].text(-1.9, -1.9, "left-handed", fontsize=11, color=GRAY)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "vehicle-frames.png"), dpi=160)
print("wrote stopping-distance.png braking-trace.png fbd-point-mass.png vehicle-frames.png")
