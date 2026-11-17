# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
"""Figures for Lecture 1B. Run from this folder: python3 make_figures_1b.py
Each plot is made by exactly the code shown on its slide, with Matplotlib's default style,
so students see what their own code will draw."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

# slide "Plotting": speed during a test drive (the code on the slide)
time = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
speed = np.array([0, 10, 25, 35, 50, 55, 60, 55, 45, 30, 0])
plt.figure(figsize=(6, 4))
plt.plot(time, speed, marker="o", label="Speed")
plt.title("Vehicle Speed Over Time")
plt.xlabel("Time (s)")
plt.ylabel("Speed (km/h)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(HERE, "py-test-drive.png"), dpi=150)
plt.close()

# group example: 72 km/h, braking at 4 m/s^2, speed every second until it stops
def kmh_to_ms(speed_kmh):
    return speed_kmh / 3.6

v = kmh_to_ms(72)
a_b = 4.0
t = 0.0
times, speeds = [t], [v]
while v > 0:
    t = t + 1.0
    v = max(v - a_b * 1.0, 0.0)
    times.append(t); speeds.append(v)
plt.figure(figsize=(6, 4))
plt.plot(times, speeds, marker="o")
plt.title("Braking from 72 km/h at 4 m/s²")
plt.xlabel("Time (s)")
plt.ylabel("Speed (m/s)")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(HERE, "py-braking-answer.png"), dpi=150)
plt.close()
print("wrote py-test-drive.png py-braking-answer.png")
