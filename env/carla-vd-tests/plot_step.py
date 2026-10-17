import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
L, K, V = 2.8605, 0.00214, 20.0
DEG_PER_STEER = 65.3   # measured at low speed for small commands
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
s = np.linspace(0, 0.18, 50); d = np.radians(DEG_PER_STEER) * s
ax[0].plot(s, V*d/(L + K*V**2), "k--", lw=1.2, label="linear bicycle model (K from ramp test)")
for f, lab, mk in [("step_20_none.json", "CARLA, tire_friction 3.5 (default)", "o"), ("step_20_0.5.json", "CARLA, tire_friction 0.5", "s")]:
    r = json.load(open(f))
    ax[0].plot([q["steer"] for q in r], [q["r_ss"] for q in r], mk+"-", label=lab)
    ax[1].plot([q["ay_ss"]/9.81 for q in r], [q["beta_deg"] for q in r], mk+"-", label=lab)
ax[0].set_xlabel("steering command (step)"); ax[0].set_ylabel("steady yaw rate (rad/s)"); ax[0].set_title("Step steer at 20 m/s")
ax[1].set_xlabel("lateral acceleration (g)"); ax[1].set_ylabel("sideslip angle (deg)"); ax[1].set_title("Spin onset at low friction")
for a in ax: a.grid(alpha=0.3); a.legend(fontsize=8)
plt.tight_layout(); plt.savefig("step.png", dpi=80)
