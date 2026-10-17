# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
"""Braking sweep for Lecture 1: stopping distance and deceleration trace vs speed.
Writes brake_sweep.json (speeds, distances, one time trace per speed)."""
import json, sys, pg
c, w = pg.connect(build=True)
out = []
for v0 in [5, 10, 15, 20, 25, 30]:
    v = pg.spawn(w, x=20.0, y=-60.0)
    pg.speed_up(c, w, v, v0)
    s0 = pg.state(v); x0 = s0["x"]
    trace = []
    for i in range(4000):
        pg.control(c, v, brake=1.0); w.tick()
        st = pg.state(v)
        trace.append((round(i * pg.DT, 3), round(st["vx"], 4), round(st["x"] - x0, 4), round(st["ax"], 4)))
        if st["vx"] < 0.05: break
    out.append(dict(v0=s0["vx"], dist=st["x"] - x0, t_stop=len(trace) * pg.DT, trace=trace))
    print(round(s0["vx"], 2), round(st["x"] - x0, 2), round(len(trace) * pg.DT, 2))
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "brake_sweep.json", "w"))
