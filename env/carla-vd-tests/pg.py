"""Proving-ground helpers for CARLA vehicle-dynamics feasibility tests.

Follows the lab determinism rules: synchronous mode, fixed dt with full substepping,
commands via apply_batch_sync.
"""
import math
import carla
import numpy as np

DT = 0.01
G = 9.81


def xodr(length=800.0, lanes=30, width=4.0):
    def lane(i, side):
        return (f'<lane id="{side*i}" type="driving" level="false"><link/>'
                f'<width sOffset="0" a="{width}" b="0" c="0" d="0"/></lane>')
    left = "".join(lane(i, 1) for i in range(lanes, 0, -1))
    right = "".join(lane(i, -1) for i in range(1, lanes + 1))
    return f"""<?xml version="1.0" standalone="yes"?>
<OpenDRIVE><header revMajor="1" revMinor="4" name="pg" version="1.00"/>
<road name="pg" length="{length}" id="1" junction="-1"><link/>
<planView><geometry s="0" x="0" y="0" hdg="0" length="{length}"><line/></geometry></planView>
<elevationProfile><elevation s="0" a="0" b="0" c="0" d="0"/></elevationProfile>
<lateralProfile/>
<lanes><laneSection s="0">
<left>{left}</left>
<center><lane id="0" type="driving" level="false"><link/></lane></center>
<right>{right}</right>
</laneSection></lanes></road></OpenDRIVE>"""


def connect(port=3000, build=True):
    client = carla.Client("localhost", port)
    client.set_timeout(120.0)
    if build:
        params = carla.OpendriveGenerationParameters(
            vertex_distance=2.0, max_road_length=50.0, wall_height=0.0,
            additional_width=0.0, smooth_junctions=True, enable_mesh_visibility=True)
        client.generate_opendrive_world(xodr(), params)
    world = client.get_world()
    s = world.get_settings()
    s.synchronous_mode = True
    s.fixed_delta_seconds = DT
    s.substepping = True
    s.max_substep_delta_time = 0.005
    s.max_substeps = 10
    world.apply_settings(s)
    world.tick()
    return client, world


def spawn(world, bp_id="vehicle.lincoln.mkz_2020", x=20.0, y=0.0, yaw=0.0):
    for a in world.get_actors().filter("vehicle.*"):
        a.destroy()
    bp = world.get_blueprint_library().find(bp_id)
    v = world.spawn_actor(bp, carla.Transform(carla.Location(x=x, y=y, z=0.5),
                                              carla.Rotation(yaw=yaw)))
    for _ in range(100):
        world.tick()
    return v


def control(client, v, throttle=0.0, steer=0.0, brake=0.0):
    client.apply_batch_sync([carla.command.ApplyVehicleControl(
        v.id, carla.VehicleControl(throttle=float(throttle), steer=float(steer),
                                   brake=float(brake)))], False)


def state(v):
    t = v.get_transform()
    vel = v.get_velocity()
    acc = v.get_acceleration()
    w = v.get_angular_velocity()
    yaw = math.radians(t.rotation.yaw)
    c, s = math.cos(yaw), math.sin(yaw)
    vx = c * vel.x + s * vel.y
    vy = -s * vel.x + c * vel.y
    ax = c * acc.x + s * acc.y
    ay = -s * acc.x + c * acc.y
    return dict(x=t.location.x, y=t.location.y, yaw=yaw, vx=vx, vy=vy, ax=ax, ay=ay,
                r=math.radians(w.z))


def params(v):
    pc = v.get_physics_control()
    w = pc.wheels
    # wheel positions are in cm, world frame
    front = (np.array([w[0].position.x, w[0].position.y]) +
             np.array([w[1].position.x, w[1].position.y])) / 2 / 100
    rear = (np.array([w[2].position.x, w[2].position.y]) +
            np.array([w[3].position.x, w[3].position.y])) / 2 / 100
    com = v.get_transform().location
    L = float(np.linalg.norm(front - rear))
    return dict(mass=pc.mass, L=L, max_steer_deg=w[0].max_steer_angle,
                tire_friction=[x.tire_friction for x in w],
                lat_stiff=[x.lat_stiff_value for x in w],
                long_stiff=[x.long_stiff_value for x in w],
                com_offset=(pc.center_of_mass.x, pc.center_of_mass.y, pc.center_of_mass.z),
                front=front.tolist(), rear=rear.tolist(), loc=(com.x, com.y))


def speed_up(client, world, v, target, steer=0.0, kp=0.5, max_t=60):
    """Drive straight (or at fixed steer) until vx reaches target."""
    for i in range(int(max_t / DT)):
        st = state(v)
        if st["vx"] >= target:
            return st
        control(client, v, throttle=1.0, steer=steer)
        world.tick()
    return state(v)


def hold_speed(client, world, v, target, steer, seconds, log=None, kp=0.6):
    out = []
    for i in range(int(seconds / DT)):
        st = state(v)
        e = target - st["vx"]
        thr = max(0.0, min(1.0, 0.3 + kp * e))
        brk = max(0.0, min(1.0, -kp * e)) if e < -1.0 else 0.0
        control(client, v, throttle=thr, steer=steer, brake=brk)
        world.tick()
        st["steer"] = steer
        out.append(st)
    return out
