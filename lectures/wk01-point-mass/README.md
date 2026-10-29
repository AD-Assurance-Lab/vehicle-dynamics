# Week 1: the point mass and constant acceleration

Lecture 1A (Monday): `lecture-01a.html`, "What Is the Point of Vehicle Dynamics? Starting from Basics: Point Mass Model and
Constant Acceleration" (the syllabus carries the second part). Eighteen slides: the field, a speed group example worked with
unit fractions, the point mass as kinematics, the four constant-acceleration equations derived step by step (Spring 2026 Lec3),
the two-car merge worked example with an animation, the stopping distance from equation (3), the one force this week (tire
friction, so that a_b = mu g), and the CARLA friction fit. No other forces this week. The Nissan Leaf turn opens week 2; the
Fiesta braking example and the friction circle wait for weeks 7 and 5.
Lecture 1B (Wednesday): Python, Linux and CARLA (not written yet; built from the Spring 2026 Lec1 pages 3 to 9 and Lec2).
Lab (Friday): `../../labs/wk01-braking/`.

## Figure sources
| File | Source |
|---|---|
| `figures/car-mkz.png`, `figures/car-mustang.png` | Rendered by the course from CARLA 0.9.16 (`env/carla-vd-tests/side_views.py`); background removed with CARLA's semantic camera. CARLA assets are CC BY 4.0. |
| `figures/carla-wet-road.png`, `figures/carla-lead-following.png` | Rendered by the course from CARLA 0.9.16. CARLA assets are CC BY 4.0. |
| `figures/stopping-distance.png`, `figures/braking-trace.png` | `figures/make_figures.py` from `figures/carla-brake-sweep.json` (CARLA 0.9.16, `vehicle.lincoln.mkz_2020`, `env/carla-vd-tests/brake_sweep.py`). |
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
| `ford-fiesta.jpg` (for week 7) | [1990 Ford Fiesta 1.1 Popular Plus CVT (15079530368).jpg](https://commons.wikimedia.org/wiki/File:1990_Ford_Fiesta_1.1_Popular_Plus_CVT_(15079530368).jpg) | Kieran White | CC BY 2.0 |

The CC BY-SA photos are shown unmodified beside the lecture, not adapted into it, so share-alike applies to the photo only.
The point-mass overlay on the MKZ is a separate SVG layer over the unmodified photo. The Toyota photo is cropped on screen to its grille logo with CSS; the file is unmodified.

## Content lineage
- "Did you know" facts and the era table: Spring 2026 Lec1. The 2026 photos were not reused (no license on record); the slide uses licensed Commons photos. The Ferrari and Toyota numbers were updated in 2026-10 to Ferrari's 2024 results (13,752 cars, about 38 a day) and Toyota's
  roughly 10 million a year (about 27,000 a day); the 2026 figures (13,000 and 14 a day) were out of date.
- Speed-feel group example: 2024 to 2026 (now an Ontario 100 km/h sign and a 35 m/s test on Stadium Drive).
- Point mass, standard frame and the four constant-acceleration derivations: Spring 2026 Lec3 handwritten notes, page 1.
- Two ways to merge: the Spring 2026 Lec3 two-car worked example (page 2), with car B changed so the steady car A wins by 1.0 s.
- Stadium Drive and Bronco Mart problem: Spring 2026 Lec14. Parked for week 7.
- Nissan Leaf 90° turn: Spring 2026 Lec3 group example. Opens week 2 (it is in this file's git history).
- Braking data and the CARLA fit: new for 2027. The fit gives a braking deceleration of 7.0 m/s², so mu = 0.71.
- Worked example "same car, two roads" was dropped; its braking animation became the Fiesta stop.

## Accessibility check (docs/ACCESSIBILITY.md)
- [x] Handout PDF passes veraPDF PDF/UA-1
- [x] Alt text or title/desc on every figure
- [x] Equations are MathML
- [ ] Ally score on eLearning (after upload)
- [ ] Captions: no video yet
