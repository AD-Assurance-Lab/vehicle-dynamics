# Feasibility tests of vehicle-dynamics labs in CARLA 0.9.16.
# Exploratory scripts, kept so the numbers in docs/CARLA-DYNAMICS-FEASIBILITY.md can be rerun.
# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
import sys, json, math, pg, numpy as np
c, w = pg.connect(build=False)
L = 2.8605

def fresh(friction=None, y=-60.0, x=400.0):
    v = pg.spawn(w, x=x, y=y)
    if friction is not None:
        pc = v.get_physics_control(); wh = pc.wheels
        for q in wh: q.tire_friction = friction
        pc.wheels = wh; v.apply_physics_control(pc)
        for _ in range(20): w.tick()
    return v

def steer_map():
    out = []
    for s in [0.05, 0.1, 0.2, 0.3, 0.5]:
        v = fresh()
        log = pg.hold_speed(c, w, v, 3.0, s, 12.0)
        tail = log[-300:]
        kappa = np.mean([q["r"] / q["vx"] for q in tail])
        out.append(dict(steer=s, R=round(1/kappa, 2), delta_eff_deg=round(math.degrees(math.atan(L*kappa)), 3)))
    return out

def ramp(steer, friction=None, v_end=30.0, rate=0.25):
    v = fresh(friction)
    log = []
    target = 3.0
    while target < v_end:
        seg = pg.hold_speed(c, w, v, target, steer, 1.0)
        log += seg
        target += rate
        st = seg[-1]
        if abs(st["y"]) > 115 or not (10 < st["x"] < 790): break
        if abs(st["vy"]) > 0.6 * max(st["vx"], 1): break   # spun
    return log

def step(v0, steers, friction=None, hold=4.0):
    res = []
    for s in steers:
        v = fresh(friction, y=-100.0, x=20.0)
        pg.speed_up(c, w, v, v0)
        log = pg.hold_speed(c, w, v, v0, s, hold)
        tail = log[-100:]
        res.append(dict(steer=s, r_ss=float(np.mean([q["r"] for q in tail])),
                        ay_ss=float(np.mean([q["vx"]*q["r"] for q in tail])),
                        beta_deg=float(np.degrees(np.mean([math.atan2(q["vy"], q["vx"]) for q in tail]))),
                        vx=float(np.mean([q["vx"] for q in tail])),
                        r_trace=[q["r"] for q in log[::5]]))
    return res

mode = sys.argv[1]
if mode == "map":
    print(json.dumps(steer_map()))
elif mode == "ramp":
    f = None if sys.argv[3] == "none" else float(sys.argv[3])
    log = ramp(float(sys.argv[2]), f)
    json.dump(log, open(f"ramp_{sys.argv[2]}_{sys.argv[3]}.json", "w"))
    print(len(log), "samples; last", {k: round(x, 2) for k, x in log[-1].items()})
elif mode == "step":
    f = None if sys.argv[3] == "none" else float(sys.argv[3])
    res = step(float(sys.argv[2]), [0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.18], f)
    json.dump(res, open(f"step_{sys.argv[2]}_{sys.argv[3]}.json", "w"))
    for q in res: print({k: round(x, 3) for k, x in q.items() if k != "r_trace"})
