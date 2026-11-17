# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
"""Lab 1, the braking test.        python3 brake_test.py 20        (the start speed, in m/s)

Builds a long, flat, straight test road in CARLA (the first run takes about 10 s), puts a Lincoln MKZ on it,
speeds up at full throttle to the start speed, brakes fully, and prints the stopping distance. CARLA's window
follows the car. Writes brake_20.csv: time (s), speed (m/s) and distance (m) from the moment the brake goes on.
Start CARLA first, in another terminal: carla"""
import csv
import os
import sys

import carla

DT = 0.01                                   # one tick, s
BLUEPRINT = "vehicle.lincoln.mkz_2020"


def flat_road(length=800.0, lanes=30, width=4.0):
    """OpenDRIVE text for one straight, flat road: 800 m long, 30 lanes of 4 m each way."""
    lane = lambda i: (f'<lane id="{i}" type="driving" level="false"><link/>'
                      f'<width sOffset="0" a="{width}" b="0" c="0" d="0"/></lane>')
    left = "".join(lane(i) for i in range(lanes, 0, -1))
    right = "".join(lane(-i) for i in range(1, lanes + 1))
    return f"""<?xml version="1.0" standalone="yes"?>
<OpenDRIVE><header revMajor="1" revMinor="4" name="flat" version="1.00"/>
<road name="flat" length="{length}" id="1" junction="-1"><link/>
<planView><geometry s="0" x="0" y="0" hdg="0" length="{length}"><line/></geometry></planView>
<elevationProfile><elevation s="0" a="0" b="0" c="0" d="0"/></elevationProfile>
<lateralProfile/>
<lanes><laneSection s="0">
<left>{left}</left>
<center><lane id="0" type="driving" level="false"><link/></lane></center>
<right>{right}</right>
</laneSection></lanes></road></OpenDRIVE>"""


def follow(spectator, car):
    """Put CARLA's camera 10 m behind the car and 4 m up."""
    view = car.get_transform()
    view.location += view.get_forward_vector() * -10 + carla.Location(z=4)
    view.rotation.pitch = -12
    spectator.set_transform(view)


def main(v_target):
    client = carla.Client("localhost", int(os.environ.get("CARLA_PORT", 2000)))
    client.set_timeout(60.0)
    world = client.get_world()
    if not world.get_map().name.endswith("OpenDriveMap"):        # build the test road once
        print("Building the test road, about 10 s ...")
        params = carla.OpendriveGenerationParameters(
            vertex_distance=2.0, max_road_length=50.0, wall_height=0.0,
            additional_width=0.0, smooth_junctions=True, enable_mesh_visibility=True)
        client.generate_opendrive_world(flat_road(), params)
        world = client.get_world()

    before = world.get_settings()
    settings = world.get_settings()
    settings.synchronous_mode = True        # time moves only when we call tick()
    settings.fixed_delta_seconds = DT
    settings.substepping = True             # physics in steps of 5 ms or less
    settings.max_substep_delta_time = 0.005
    settings.max_substeps = 10
    world.apply_settings(settings)
    try:
        for old in world.get_actors().filter("vehicle.*"):      # remove the car of an earlier run
            old.destroy()
        bp = world.get_blueprint_library().find(BLUEPRINT)
        car = world.spawn_actor(bp, carla.Transform(carla.Location(x=20, y=-60, z=0.5)))
        spectator = world.get_spectator()

        for _ in range(100):                                      # 1 s to settle on its springs
            world.tick()
            follow(spectator, car)
        while car.get_velocity().length() < v_target:             # full throttle up to the start speed
            car.apply_control(carla.VehicleControl(throttle=1.0))
            world.tick()
            follow(spectator, car)

        start = car.get_location()
        v0 = car.get_velocity().length()
        rows, t = [(0.0, round(v0, 3), 0.0)], 0.0
        while car.get_velocity().length() > 0.05:                 # full brake until it stops
            car.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
            world.tick()
            follow(spectator, car)
            t += DT
            rows.append((round(t, 2), round(car.get_velocity().length(), 3),
                         round(car.get_location().distance(start), 3)))

        d = car.get_location().distance(start)
        print(f"start speed {v0:.2f} m/s   stopping distance {d:.2f} m   stopping time {t:.2f} s")
        name = f"brake_{v_target:g}.csv"
        with open(name, "w", newline="") as f:
            out = csv.writer(f)
            out.writerow(["t_s", "speed_mps", "distance_m"])
            out.writerows(rows)
        print("wrote", name)
    finally:
        world.apply_settings(before)        # CARLA runs on its own again


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 brake_test.py <start speed in m/s>, for example: python3 brake_test.py 20")
    main(float(sys.argv[1]))
