# ME 4650/5950 Vehicle Dynamics

Western Michigan University, Department of Mechanical and Aerospace Engineering.
Instructor: Zachary D. Asher, AD Assurance Lab.

The course has two theory lectures and one lab each week. Lectures are web
pages: slides, full notes and a printable handout from one file. Labs use coding
and simulation (Python, ROS 2, CARLA). Learning is checked with in-person
quizzes and exams. Solutions are shared with enrolled students on eLearning.

## Layout

| Path | What it holds |
|---|---|
| `syllabus/` | Syllabus (LaTeX, tagged PDF) and its banner figures |
| `lectures/wkNN-topic/` | One HTML file per lecture: slides, notes view and printable handout |
| `labs/labNN-topic/` | Lab handouts and starter code |
| `project/` | Team project requirements, templates, rubric |
| `common/kit/` | Shared stylesheet, slide script, fonts and math renderer |
| `tools/` | PDF build and accessibility fix-up |
| `env/` | Lab software environment and CARLA test scripts |
| `docs/` | Course plan, decisions, accessibility, software, copyright checks |
| `archive/` | Past offerings by year. Local only, never committed |
| `quizzes-exams/` | Quizzes and exams. Local only; Google Drive is the record |
| `practice-problems/` | Group-example solutions. Local only; posted on eLearning |

## Building

- Lectures are plain HTML files using the course kit in
  `common/kit/` (see its README). Open them in a browser; nothing to build.
- Handout PDFs: `tools/.venv/bin/python tools/build_pdf.py <file>.html`. It prints
  with headless Chrome, fixes the PDF for accessibility and checks it with
  veraPDF. Setup: `python3 -m venv tools/.venv && tools/.venv/bin/pip install -r tools/requirements.txt`.
- Links: `python3 tools/check_links.py .` after building.
- Built PDFs are not committed. GitHub Actions builds them, checks them and
  publishes the site at https://ad-assurance-lab.github.io/vehicle-dynamics/.

## Status

Spring 2027 content is being written. Each week appears on the site when it is
finished. Each offering is tagged at the end of its semester (for example `sp27`).

## License

Documents: CC BY 4.0. Code: Apache-2.0. See `NOTICE`.

## Contributing

Former students and others are welcome. See `CONTRIBUTING.md`.
