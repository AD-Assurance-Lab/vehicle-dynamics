# Feasibility tests of vehicle-dynamics labs in CARLA 0.9.16.
# Exploratory scripts, kept so the numbers in docs/CARLA-DYNAMICS-FEASIBILITY.md can be rerun.
# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
import sys, json, pg, numpy as np
c, w = pg.connect(build=False)

def run(v0, friction=None):
    v = pg.spawn(w)
    if friction is not None:
        pc = v.get_physics_control()
        wh = pc.wheels
        for x in wh: x.tire_friction = friction
        pc.wheels = wh
        v.apply_physics_control(pc)
        for _ in range(20): w.tick()
        got = [x.tire_friction for x in v.get_physics_control().wheels]
    else:
        got = None
    pg.speed_up(c, w, v, v0)
    s0 = pg.state(v); x0 = s0["x"]; vstart = s0["vx"]
    axs = []
    for i in range(3000):
        pg.control(c, v, brake=1.0)
        w.tick()
        st = pg.state(v); axs.append(st["ax"])
        if st["vx"] < 0.05: break
    d = st["x"] - x0
    mu = vstart**2 / (2 * 9.81 * d)
    return dict(v0=round(vstart,2), dist=round(d,2), mu_eff=round(mu,3),
                peak_decel_g=round(-min(axs)/9.81,3), friction_readback=got)

mode = sys.argv[1]
if mode == "speeds":
    for v0 in [10, 15, 20, 25, 30]:
        print(json.dumps(run(v0)))
elif mode == "reps":
    for r in range(3): print(json.dumps(run(20)))
elif mode == "friction":
    for f in [3.5, 1.0, 0.5, 0.2]:
        print(f, json.dumps(run(20, f)))
