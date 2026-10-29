# Operating rules for this repository

## What must never be committed
- Grades of any kind, gradebook exports, eLearning exports.
- Named student work (exams, quizzes, reports, slides) unless the student gave
  written consent, recorded in the week or project README.
- Quiz and exam questions or solutions, and practice-problem solutions. Those
  live on Google Drive only (students get them through eLearning).
- Third-party figures or code without a recorded license that allows CC BY or
  Apache-2.0 redistribution. Record source and license in the week README.
- Videos, model weights, zips, ISOs. Link to Drive or a release asset instead.

The `.gitignore` is an allowlist. Do not widen it to make a file commit.

## Where things live
- `archive/<year>/`: past offerings, local only (see docs/ARCHIVE-PLAN.md). Read for reference. Never move
  files out of it into tracked paths without the copyright and privacy checks.
- `quizzes-exams/`: local working copies only. Google Drive is their record.
- Google Drive is the backup of record. The local copy came from Drive with rclone.
- Deleting: never `rm` course material. Move it to `_to_delete/` for Zach.

## Publishing
- Two branches. `draft` holds everything in progress and is never pushed to the
  public repo. `main` is public (AD-Assurance-Lab/vehicle-dynamics) and is the
  site on GitHub Pages.
- Publish a finished item by copying it from draft:
  `git switch main && git checkout draft -- <paths> && git commit`.
  Never merge draft into main: its history holds unfinished versions.
- GitHub Actions builds every PDF, requires veraPDF PASS and working links,
  then deploys main. A link to an unpublished page fails the build.
- Not yet public (Zach revising): the syllabus and Lab 1. Lecture 1A was published 2026-10-29.

## Building content
- Lectures are single HTML files in `lectures/wkNN-topic/` using `common/kit/`
  (rules in `common/kit/README.md`). The handout PDF is printed from the same file
  with `tools/build_pdf.py`, which must report veraPDF PASS.
- Figures come from a `make_figures.py` next to them.
- Group-example solutions live in `practice-problems/` (local only) and go on
  eLearning after class. Worked-example solutions are handwritten, Drive only.
- Every PDF must pass veraPDF (PDF/UA) before it is posted.
- Content is built one week at a time. A week is done when its README lists
  every figure source, passes the accessibility check in `docs/ACCESSIBILITY.md`,
  and builds cleanly.
- Writing: short sentences, no em dashes.
- Before Zach reviews a lecture or lab, run the `student-reviewer` agent
  (`.claude/agents/`, local only) and bring its findings with yours.

## Commits
- Lab conventions apply (`../CONVENTIONS.md`): subject <= 72 chars, body <= 15 lines.
- Record course decisions in `docs/DECISIONS.md`, not in commit bodies.
