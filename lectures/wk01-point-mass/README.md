# Week 1: the point mass and constant acceleration

Lecture 1A (Monday): `lecture-01a.html`, "What Is the Point of Vehicle Dynamics? Starting from Basics: Point Mass Model and
Constant Acceleration" (the syllabus carries the second part). Eighteen slides: the field, a speed group example worked with
unit fractions, the point mass as kinematics, the four constant-acceleration equations derived step by step (Spring 2026 Lec3),
the two-car merge worked example with an animation, the stopping distance from equation (3), the one force this week (tire
friction, so that a_b = mu g), and the CARLA friction fit. No other forces this week. The Nissan Leaf turn opens week 2; the
Fiesta braking example and the friction circle wait for weeks 7 and 5.
Lecture 1B (Wednesday): `lecture-01b.html`, "How Do You Talk to a Simulated Car? Toolchain: Python, Linux and CARLA"
(the syllabus carries the second part). Thirty slides for a room without student laptops. Slide 2 builds a map of the
toolchain as nested boxes (everything inside Linux; the Python API inside Python, between Python and CARLA); a waiter
analogy explains the API; the map then opens each of four parts with that part outlined in a rainbow (screen only): Linux
(desktop and terminal), Python and its API, CARLA, and all together. It ends with the map as the recap and one look ahead at
ROS 2 (an automatic emergency braking drawing and five reasons to use ROS 2). Every code box is drawn as one of the two
windows on the course USB drive (the Ubuntu terminal or VS Code's Dark Modern theme), and the terminal and VS Code slides use
real screenshots of the drive. Interactive pieces: the waiter animation, a click-through of six real screens (hello world:
write, save, run), a simulated terminal with the drive's home folder, a code stepper with variable boxes, messages between a
script and the CARLA server, a replay of a real CARLA run, and the braking drawing. Built from the Spring 2026 Lec1 (pages 3
to 9) and Lec2.
Lab (Friday): `../../labs/wk01-braking/`.

## Figure sources
| File | Source |
|---|---|
| `figures/car-mkz.png`, `figures/car-mustang.png` | Rendered by the course from CARLA 0.9.16 (`env/carla-vd-tests/side_views.py`); background removed with CARLA's semantic camera. CARLA assets are CC BY 4.0. |
| `figures/py-test-drive.png`, `figures/py-braking-answer.png` (Lecture 1B) | `figures/make_figures_1b.py`, Matplotlib default style, the code shown on the slides. The braking answer plot is no longer on the slides (group example 3 is a scaffold with hints); kept for the instructor solution. |
| `figures/carla-wet-road.png`, `figures/carla-lead-following.png` | Rendered by the course from CARLA 0.9.16. CARLA assets are CC BY 4.0. |
| `figures/carla-stops.png`, `figures/stopping-distance.png`, `figures/braking-trace.png` | `figures/make_figures.py` from `figures/carla-brake-sweep.json` (CARLA 0.9.16, `vehicle.lincoln.mkz_2020`, `env/carla-vd-tests/brake_sweep.py`). |
| `screens/*.png` (Lecture 1B) | Screenshots of the course USB image (`me4650.img`, built 2026-11-16: Ubuntu 22.04, VS Code, CARLA 0.9.16, ROS 2 Humble) booted in QEMU on a throwaway overlay and driven with `course--me3580--usb-image/test/vm.py`; cropped and reduced to 128 colors. Ubuntu, GNOME and VS Code interface elements appear as screenshots of the software in use. |
| `screens/*.jpg` (Lecture 1B) | Frames of the CARLA recordings below, taken before the cursor and captions are drawn: CARLA's window, and the run with CARLA beside the terminal. |
| `figures/icon-terminal.png`, `figures/icon-vscode.png`, `figures/icon-python.png` (Lecture 1B) | Copied from the course USB image and resized to 128 px: Ubuntu's Yaru terminal icon (Yaru icon theme, Sam Hewitt and others, CC BY-SA 4.0); the VS Code icon (`/usr/share/pixmaps/vscode.png`), a trademark of Microsoft; the Python logo (from the VS Code Python extension), a trademark of the Python Software Foundation. The two logos name the software on the map, as the brand guides allow, and are excluded from the course licenses. |
| `videos/*.mp4` (Lecture 1B, not committed; published as the release [lecture-1b-videos](https://github.com/AD-Assurance-Lab/vehicle-dynamics/releases/tag/lecture-1b-videos)) | Screen recordings of the same USB image in QEMU, opened from the Watch buttons on four slides (the page plays a local `videos/` copy if there is one, else the release): open a terminal, write and run `hello.py` in VS Code (`c3-hello.mp4`), start CARLA, run `watch_it_drive.py`. Recorded with `tools/screencast/takes.py` (drawn cursor, key badges, captions). CARLA runs from the image inside the VM, rendered on the host GPU (QEMU Venus); its 15 s load and the script's drive are played 4 times faster, marked on screen. Silent; each video's numbered step list is its text alternative. |
| `figures/carla-we2-chase.jpg`, `figures/carla-we2-run.json` (Lecture 1B) | Worked example 2 run exactly as on the slide in CARLA 0.9.16 (Town10HD_Opt, spawn point 0, `vehicle.lincoln.mkz_2020`), `env/carla-vd-tests/we2_run.py`. The lecture shows the distance the script printed. CARLA assets are CC BY 4.0. |
| Toolchain map, waiter animation and ROS 2 braking drawing (Lecture 1B) | Drawn in the lecture file. The braking drawing uses round numbers (15 m/s, a stopped car 45 m ahead, 8 m/s² when gap over speed falls below 1.4 s), not a CARLA run. Topic names follow CARLA 0.9.16's ROS 2 naming for a vehicle named hero (`/carla/hero/vehicle_control_cmd` seen in a real run; the radar topic by the same pattern). Apache-2.0. |
| `figures/fbd-point-mass.png`, `figures/vehicle-frames.png` | `figures/make_figures.py`. Not used by the current lecture; kept for 1B and week 2. |
| Inline SVG (timeline, course road, gauges, point-mass overlay, merge speed graph, stopping bars, free-body diagram, CARLA fit) | Drawn in the lecture file. Apache-2.0. |
| `../../common/brand/wmu-logo-horizontal.png` | WMU long horizontal logo, from wmich.edu/marcom/creative/visual-identity/logo (2026 digital PNG, resized). Registered trademark, used as the university's own faculty per its visual identity guide. Excluded from the course licenses. |

## Photos (`photos/`)
From Wikimedia Commons (one from Flickr), resized to 1600 px wide, otherwise unmodified. Each keeps its own license. Credits are on the lecture's last slide, not under each photo.

| File | Commons file | Author | License |
|---|---|---|---|
| `freeway-traffic.jpg` | [110 Freeway @ Rush Hour (18322206624).jpg](https://commons.wikimedia.org/wiki/File:110_Freeway_@_Rush_Hour_(18322206624).jpg) | Prayitno | CC BY 2.0 |
| `parking-lot.jpg` | [Flying over Denver Parking lot (4290932798).jpg](https://commons.wikimedia.org/wiki/File:Flying_over_Denver_Parking_lot_(4290932798).jpg) | Heath Alseike | CC BY 2.0 |
| `toyota-corolla.jpg` | [2011 Toyota Corolla -- NHTSA.jpg](https://commons.wikimedia.org/wiki/File:2011_Toyota_Corolla_--_NHTSA.jpg) | NHTSA | Public domain |
| `ferrari-factory.jpg` | [Ferrari Factory (Maranello, Modena) in 2018.08.jpg](https://commons.wikimedia.org/wiki/File:Ferrari_Factory_(Maranello,_Modena)_in_2018.08.jpg) | CAPTAIN RAJU | CC BY-SA 4.0 |
| `vanity-plate.jpg` | [Michigan 2010 Vanity License Plate VANITAS.jpg](https://commons.wikimedia.org/wiki/File:Michigan_2010_Vanity_License_Plate_VANITAS.jpg) | Dwight Burdette | CC BY 3.0 |
| `car-radio.jpg` (unused) | [Tuning the car radio (Unsplash).jpg](https://commons.wikimedia.org/wiki/File:Tuning_the_car_radio_(Unsplash).jpg) | Courtney Recker | CC0 |
| `ontario-100-sign.jpg` | [Speed Limit 100, Kings Highway 402, Warwick, Ontario (21652555320).jpg](https://commons.wikimedia.org/wiki/File:Speed_Limit_100,_Kings_Highway_402,_Warwick,_Ontario_(21652555320).jpg) | Ken Lund | CC BY-SA 2.0 |
| `stadium-drive.jpg` | [Stadium Drive, Kalamazoo, Michigan.JPG](https://commons.wikimedia.org/wiki/File:Stadium_Drive,_Kalamazoo,_Michigan.JPG) | SydneySmith | CC BY-SA 4.0 |
| `lincoln-mkz.jpg` | [LINCOLN MKZ (CD4) China (9).jpg](https://commons.wikimedia.org/wiki/File:LINCOLN_MKZ_(CD4)_China_(9).jpg) | Dinkun Chen | CC BY-SA 4.0 |
| `nissan-leaf.jpg` (for week 2) | [Nissan Leaf (ZE1) at Budi Luhur University (2024-03-20).jpg](https://commons.wikimedia.org/wiki/File:Nissan_Leaf_(ZE1)_at_Budi_Luhur_University_(2024-03-20).jpg) | VulcanSphere | CC BY 4.0 |
| `singing-in-car.jpg` | [Road Trip Sing -a- long](https://www.flickr.com/photos/bellatrix6/130912241/) (Flickr) | nikoretro | CC BY-SA 2.0 |
| `restaurant-order.jpg` (Lecture 1B) | [DSC 7056 A waiter takes an order from a smiling group of friends ... .jpg](https://commons.wikimedia.org/wiki/File:DSC_7056_A_waiter_takes_an_order_from_a_smiling_group_of_friends_seated_at_a_cozy_restaurant_table_set_with_red_linens_and_wine_while_bottles_line_the_wall_behind_them.jpg) | PattayaPatrol | CC BY-SA 4.0 |
| `waiter-plates.jpg` (Lecture 1B) | [Carrying four plates (4456993086).jpg](https://commons.wikimedia.org/wiki/File:Carrying_four_plates_(4456993086).jpg) | US Army Africa | CC BY 2.0 |
| `kitchen-cooking.jpg` (Lecture 1B) | [Cooking, 2015.jpg](https://commons.wikimedia.org/wiki/File:Cooking,_2015.jpg) | Matthias Ripp | CC BY 2.0 |
| `ford-fiesta.jpg` (for week 7) | [1990 Ford Fiesta 1.1 Popular Plus CVT (15079530368).jpg](https://commons.wikimedia.org/wiki/File:1990_Ford_Fiesta_1.1_Popular_Plus_CVT_(15079530368).jpg) | Kieran White | CC BY 2.0 |

The CC BY-SA photos are shown unmodified beside the lecture, not adapted into it, so share-alike applies to the photo only.
The point-mass overlay on the MKZ is a separate SVG layer over the unmodified photo. The Toyota photo is cropped on screen to its grille logo with CSS; the file is unmodified. The three restaurant photos are cropped on screen with CSS.

## Content lineage
- "Did you know" facts and the era table: Spring 2026 Lec1. The 2026 photos were not reused (no license on record); the slide uses licensed Commons photos. The Ferrari and Toyota numbers were updated in 2026-10 to Ferrari's 2024 results and Toyota's
  yearly production; the 2026 figures were out of date.
- Speed-feel group example: 2024 to 2026 (now an Ontario 100 km/h sign and a 35 m/s test on Stadium Drive).
- Point mass, standard frame and the four constant-acceleration derivations: Spring 2026 Lec3 handwritten notes, page 1.
- Two ways to merge: the Spring 2026 Lec3 two-car worked example (page 2), with car B changed so the race is close.
- Stadium Drive and Bronco Mart problem: Spring 2026 Lec14. Parked for week 7.
- Nissan Leaf 90° turn: Spring 2026 Lec3 group example. Opens week 2 (it is in this file's git history).
- Braking data and the CARLA fit: new for 2027.
- Worked example "same car, two roads" was dropped; its braking animation became the Fiesta stop.

## Accessibility check (docs/ACCESSIBILITY.md)
- [x] Handout PDF passes veraPDF PDF/UA-1
- [x] Web page passes axe 4.10 (WCAG 2.1 A and AA, plus best practice): 0 violations in notes and slide views, 2026-10-29; Lecture 1B, 2026-11-17 (notes view and every interactive slide)
- [x] Text in drawings at least 4.5:1 contrast (lowest 4.6:1); no motion over 5 s that starts by itself
- [x] Screen-reader read-through, 2026-10-29: web accessibility tree and PDF tag tree read in order. Fixed: duplicate photo description (slide 8), gauge readings not spoken (slide 7), counters that announced every animation frame (slides 2 and 14), and PDF math read as bare symbols (now Formula tags with spoken text)
- [x] Alt text or title/desc on every figure
- [x] Equations are MathML
- [ ] Ally score on eLearning (after upload)
- [ ] Videos (Lecture 1B): silent, burned-in captions, a step list beside each as the text alternative. Check the step lists against the videos by watching them
