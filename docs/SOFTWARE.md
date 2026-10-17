# Lab software

## Target stack for Spring 2027
- Ubuntu (version to match CARLA 0.9.16 and the ROS 2 release)
- CARLA 0.9.16 with its built-in ROS 2 support (replaces the separate bridge
  used with 0.9.15). Every lab that used the old bridge needs rework.
- ROS 2, Python, Chrono (week 10)

## Current delivery
Students boot Ubuntu from USB drives on regular lab computers.
Reported issue: slow, most drives are USB 3.0.

## Open questions
- What GPU and RAM do the lab computers have? CARLA needs a capable GPU.
- Are the drives slow because of the port or because of the flash drive?
  Cheap flash drives have poor random I/O even on USB 3. A USB SSD may fix it.
- Alternatives: Ubuntu installed on the lab machines by IT, a Docker image on
  lab Linux machines, or remote CARLA servers.
- One pinned environment (image or Dockerfile) tested before week 1.

## Before January
- [ ] List the labs that depend on the 0.9.15 bridge
- [ ] Port and test each lab on 0.9.16
- [ ] Benchmark boot and CARLA start time on one USB flash drive vs one USB SSD

## ScenarioRunner (needed for OpenSCENARIO labs)
- Separate install from CARLA. Use tag v0.9.16. See
  `docs/CARLA-DYNAMICS-FEASIBILITY.md` for the Python 3.12 fix and PYTHONPATH.
- [ ] Add to the lab image and test one scenario per lab before week 1.
