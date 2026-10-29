# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
"""Side views of CARLA cars with a transparent background, for lecture figures.
A long lens from the car's left side; the semantic camera's car pixels become the alpha mask.
Usage: python side_views.py OUTDIR [blueprint:color:name ...]"""
import sys, queue
import numpy as np
import carla
from PIL import Image
import pg

W, H, FOV, D = 1600, 800, 14.0, 34.0
CAR_TAGS = (14, 15, 16)   # car, truck, bus in CARLA's semantic tags
cars = sys.argv[2:] or ["vehicle.lincoln.mkz_2020:60,60,64:mkz", "vehicle.ford.mustang:190,20,20:mustang"]
out = sys.argv[1] if len(sys.argv) > 1 else "."

c, w = pg.connect(build=True)
w.set_weather(carla.WeatherParameters.ClearNoon)
lib = w.get_blueprint_library()
for spec in cars:
    bp_id, color, name = spec.split(":")
    for a in w.get_actors().filter("vehicle.*"):
        a.destroy()
    bp = lib.find(bp_id)
    if bp.has_attribute("color"):
        bp.set_attribute("color", color)
    v = w.spawn_actor(bp, carla.Transform(carla.Location(x=100, y=0, z=0.5)))
    for _ in range(150):
        w.tick()
    ext = v.bounding_box.extent
    cam_tf = carla.Transform(carla.Location(x=100 + v.bounding_box.location.x, y=D, z=ext.z),
                             carla.Rotation(yaw=-90))
    imgs = {}
    sensors = []
    for kind in ("rgb", "semantic_segmentation"):
        cb = lib.find(f"sensor.camera.{kind}")
        cb.set_attribute("image_size_x", str(W)); cb.set_attribute("image_size_y", str(H)); cb.set_attribute("fov", str(FOV))
        s = w.spawn_actor(cb, cam_tf)
        q = queue.Queue(); s.listen(q.put); sensors.append(s); imgs[kind] = q
    for _ in range(30):
        w.tick()
    frames = {k: None for k in imgs}
    for k, q in imgs.items():
        while not q.empty():
            frames[k] = q.get()
    rgb = np.frombuffer(frames["rgb"].raw_data, np.uint8).reshape(H, W, 4)[:, :, :3][:, :, ::-1]
    tag = np.frombuffer(frames["semantic_segmentation"].raw_data, np.uint8).reshape(H, W, 4)[:, :, 2]
    alpha = np.isin(tag, CAR_TAGS).astype(np.uint8) * 255
    ys, xs = np.nonzero(alpha)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    im = Image.fromarray(np.dstack([rgb, alpha]), "RGBA").crop(box)
    im.save(f"{out}/car-{name}.png")
    print(name, im.size, sorted(set(np.unique(tag)) - {0}))
    for s in sensors:
        s.destroy()
