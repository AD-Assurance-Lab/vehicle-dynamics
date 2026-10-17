import json, sys, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
L = 2.8605; DELTA = np.radians(3.266)
fig, ax = plt.subplots(1, 3, figsize=(15, 4.3))
for f, lab in [("ramp_0.05_none.json", "tire_friction 3.5 (default)"), ("ramp_0.05_0.5.json", "tire_friction 0.5")]:
    d = json.load(open(f))
    vx = np.array([q["vx"] for q in d]); r = np.array([q["r"] for q in d]); vy = np.array([q["vy"] for q in d])
    k = 25; sm = lambda a: np.convolve(a, np.ones(k)/k, mode="same")
    ay = sm(vx * r); kap = sm(r / np.maximum(vx, 0.5)); beta = np.degrees(sm(np.arctan2(vy, vx)))
    m = vx > 3.5
    ax[0].plot(ay[m]/9.81, np.degrees(L*kap[m]), lw=1, label=lab)
    ax[1].plot(vx[m], ay[m]/9.81, lw=1, label=lab)
    ax[2].plot(ay[m]/9.81, beta[m], lw=1, label=lab)
    sel = m & (ay < 3.0)
    K = -np.polyfit(ay[sel], L*kap[sel], 1)[0]
    print(lab, "understeer gradient K (rad per m/s^2) =", round(K, 5), " deg/g =", round(np.degrees(K)*9.81, 3),
          " max ay (g) =", round(ay[m].max()/9.81, 3))
ax[0].axhline(np.degrees(DELTA), color="k", ls=":", lw=0.8)
ax[0].set_xlabel("lateral acceleration (g)"); ax[0].set_ylabel("Ackermann angle L/R (deg)"); ax[0].set_title("Constant steer, rising speed")
ax[1].set_xlabel("speed (m/s)"); ax[1].set_ylabel("lateral acceleration (g)")
ax[2].set_xlabel("lateral acceleration (g)"); ax[2].set_ylabel("sideslip angle (deg)")
for a in ax: a.grid(alpha=0.3); a.legend(fontsize=8)
plt.tight_layout(); plt.savefig("ramp.png", dpi=80)
