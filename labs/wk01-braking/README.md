# Lab 1: Linux, Python, Braking Test in CARLA

`lab-01.html` is the lab sheet (web page and a two-page printed handout from the same file). Each part gives a goal, a
picture of the finished result and numbers to check against; students write their code with any AI assistant and
check it against the picture. Two files are downloaded with `wget` from the course site: `stopping.py`, a skeleton for Task 2
that shows the layout an engineer would want (numbered comments, `...` where code goes; the AI fills it in and students
check its code against each comment), and `brake_test.py`, which builds a flat, straight test road in CARLA, brakes a
Lincoln MKZ from a start speed and writes the stop to a CSV file. Tasks 2 and 3 follow Lecture 1A (d = v0²/(2 a_b), a_b = μ g, and the
curve fitted to stops from 15 m/s up).

Tested 2026-11-17 on the course USB image (CARLA 0.9.16) in a virtual machine and on a workstation running CARLA
0.9.16: the same stopping distances on both (9.50, 17.41, 28.49, 44.46 and 64.09 m from 10 to 30 m/s,
the same as Lecture 1A's CARLA stops). The instructor solution is on the draft branch and Drive only.

## Figure sources
| File | Source |
|---|---|
| `figures/target-hello.png`, `figures/target-carla.jpg` | Screenshots of the course USB image booted in QEMU, VS Code in its light theme to save ink, cropped to the windows. `target-carla.jpg` joins two real screens of the same test: CARLA following the car (an earlier run) and VS Code with `brake_test.py` (the GPU was busy for a second CARLA run). Ubuntu, VS Code and CARLA appear as screenshots of the software in use; CARLA assets are CC BY 4.0. |
| `figures/target-stopping.png` | The plot the instructor solution makes (Matplotlib). |
| `figures/fit-sketch.png` | `figures/make_figures.py`. Apache-2.0. |

This lab is licensed CC BY 4.0; its code is Apache-2.0.
