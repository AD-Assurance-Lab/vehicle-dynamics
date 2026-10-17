# Can CARLA demonstrate vehicle dynamics? Feasibility tests

Run 2026-10-14 on CARLA 0.9.16 (RTX 5090 desktop), headless, launched with the
lab's carla-determinism harness. Synchronous mode, dt = 0.01 s, physics substeps
of 0.005 s, commands sent with `apply_batch_sync`. Vehicle: `vehicle.lincoln.mkz_2020`
(mass 1696 kg, wheelbase 2.86 m). Scripts: `env/carla-vd-tests/`.

The test track is a flat OpenDRIVE road, 800 m long and 240 m wide, built at run
time with `generate_opendrive_world`. It has no buildings or walls, so there is
room for circles and step steers. The same idea can become the course proving ground.

These are feasibility checks, not study results. Each condition ran once. The
3 braking repetitions in one server session gave identical numbers.

## Findings

1. **Tire friction can be changed in 0.9.16.** Setting `tire_friction` on every
   wheel through `apply_physics_control` works, and the readback confirms it.
   Braking from 20 m/s: 28.5 m at the default 3.5, 33.6 m at 1.0, 52.5 m at 0.5,
   134 m at 0.2. The old GitHub issues on this (#4148, #5260) did not reproduce.
   Friction trigger boxes were not tested.
2. **The point-mass model works for braking above about 15 m/s.** Stopping
   distance scales with v² from 20 to 30 m/s (effective μ 0.717 at each speed).
   At 10 and 15 m/s the effective μ is lower (0.54, 0.66), likely because of
   brake build-up. Braking is capped near 0.72 g by brake torque at default friction.
3. **The kinematic bicycle model holds at low speed.** At 3 m/s the turn radius
   matches R = L / tan(δ). The steering command maps to about 65° of road-wheel
   angle per unit command for small commands.
4. **Understeer is measurable.** A constant-steer, rising-speed test (in the
   style of ISO 4138) gives a linear understeer gradient of about 1.2 deg/g, the
   same at friction 3.5 and 0.5. See `figures/carla-constant-steer-ramp.png`.
5. **The linear model predicts CARLA, then fails at the limit.** A linear
   bicycle model using the understeer gradient from finding 4 predicts the
   step-steer yaw rate at 20 m/s up to about 0.08 steering command, with no
   tuning. Beyond that, yaw rate saturates. See `figures/carla-step-steer.png`.
6. **At reduced friction the car spins.** At friction 0.5 the sideslip stays near
   zero up to 0.4 g, then grows to 17-42 degrees. The rear breaks loose, which is
   limit oversteer.
7. **The default tires are unrealistically grippy sideways.** At friction 3.5 the
   car reaches 1.76 g lateral at 20 m/s with no spin, while braking stops at
   0.72 g. A real car on dry asphalt manages about 0.9 g either way. Friction
   near 0.5 gives a lateral limit near 0.85-1.0 g, closer to a real car, but
   braking at that setting is only 0.41 g. This is a CARLA limitation worth
   showing students, not hiding.
8. **CARLA does not report tire forces, slip angles, slip ratios or wheel loads.**
   Those come from a Python model overlaid on the CARLA data.
9. **Caveats.** With low friction the car cannot accelerate to speed (0.2 reaches
   only 10.6 m/s at 40% throttle). Starting with `set_target_velocity` changes
   the braking result (37.5 m vs 28.5 m), probably because the wheels start
   stationary, so labs should drive up to speed. Partial braking gives a smooth
   increase in deceleration, with no sign of a lock-up penalty.

## What this means for the course
- Labs can show the point mass, the kinematic model, understeer, the linear
  model's success, and its failure at the limit, all in CARLA.
- The friction circle and Magic Formula curves are a Python overlay: CARLA
  supplies the measured motion, Python supplies the tire forces.
- Low-friction ("snow") labs are possible with `tire_friction` near 0.2-0.3, and
  each needs a run-up long enough to reach speed.

## Not yet tested
- g-g diagram from a single hard drive (combined braking and cornering).
- Double lane change at rising speed (ISO 3888 style).
- Other vehicles' parameters.
- Whether results hold on the lab computers' GPUs.

## ScenarioRunner and OpenSCENARIO (tested 2026-10-14)
- ScenarioRunner is a separate download: `carla-simulator/scenario_runner`, tag
  `v0.9.16` (released 2025-09-29, matching CARLA 0.9.16). It is Python only.
- Its `requirements.txt` pins `numpy==1.24.4`, which does not build on Python
  3.12 (Ubuntu 24.04). With `numpy>=1.26` in a venv the rest installs.
- It needs `PYTHONPATH` to include `<carla>/PythonAPI/carla` (for `agents`).
- On a fresh server, `FollowLeadingVehicle.xosc` (OpenSCENARIO 1.0) loaded Town01,
  spawned both vehicles and ran with `--sync`. Its pass/fail criteria reported
  failures and the process did not exit within 400 s. Not yet investigated.
- On a server left in synchronous mode by another client it hangs, and on a
  reused server it failed to spawn actors. Same lesson as determinism rule D-6:
  fresh server, one client.
- This machine runs ROS 2 Jazzy, not Humble.
