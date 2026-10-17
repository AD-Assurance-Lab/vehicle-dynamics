# Accessibility

Researched 2026-10-14. Recheck WMU's pages each fall.

## Requirement
- Federal: ADA Title II web rule (DOJ, 2024). Standard: WCAG 2.1 Level AA.
  Course materials in an LMS are in scope. DOJ moved the compliance date for
  large public entities from 2026-04-24 to 2027-04-26 (interim final rule,
  2026-04-20). The standard did not change.
- WMU: 100% compliance by 2027-04-26. That date falls inside the Spring 2027
  semester. New or copied eLearning content must already meet the standard.
  Ally in eLearning is the checker (aim for green). Slides shared with students
  must be tagged, structured and screen-reader readable. PDFs must be "born
  accessible". Equations must not be images. Videos need checked captions.
- Archive exception: content stored separately, labeled Archived/Historic, with
  a contact for an accessible version. Only for items that will not be reused.
- Contact: WMU Digital Accessibility, https://wmich.edu/digital-accessibility

## What this means for the build
- Plain Beamer cannot produce tagged PDFs. The LaTeX tagging project does not
  support it. Options: `ltx-talk` (tagging-first slide class, experimental,
  v0.6.0 2026-08), standard LaTeX classes with `\DocumentMetadata` tagging
  (TeX Live 2025 or later; this machine has TeX Live 2026), or HTML with MathJax.
- Handwritten annotated PDFs (Wacom) are not accessible on their own. Post the
  typed instructor version next to them as the accessible equivalent.
- Every figure: alt text. Every plot: readable colors and labeled axes.
- Lab videos: captions checked by a person.

## Per-week check
- [ ] Ally score green on every file posted to eLearning
- [ ] PDF tagged (check with veraPDF or Acrobat), or HTML passes an axe check
- [ ] Alt text on every figure
- [ ] Equations are text (MathML or tagged math), not images
- [ ] Captions checked on any video

## Sources
- https://wmich.edu/digital-accessibility/faqs
- https://wmich.edu/digital-accessibility/timeline
- https://campustechnology.com/articles/2026/04/27/doj-extends-deadline-for-ada-title-ii-compliance.aspx
- https://www.duanemorris.com/alerts/doj_extends_ada_title_ii_digital_accessibility_deadlines_one_year_0426.html
- https://ctan.org/tex-archive/macros/latex/contrib/ltx-talk
- https://www.latex-project.org/publications/2025-UFi-FMi-TUB-tb143fischer-tagging25.pdf

## How each PDF is made accessible (syllabus is the first example)
- LaTeX source starts with `\DocumentMetadata{lang=en-US, pdfstandard=ua-2,
  tagging=on}` and is built with LuaLaTeX (TeX Live 2025 or later). This tags
  headings, lists, tables, links and math, and sets the language and title.
- Tables declare a header row: `\tagpdfsetup{table/header-rows={1}}`.
- Every link has descriptive text. No meaning is carried by color alone. The
  draft highlights (`\confirm`) are switched off for the student copy.
- Validate with veraPDF before posting: `verapdf --flavour ua2 file.pdf` must
  print PASS. veraPDF 1.30.3 is installed at `~/.local/opt/verapdf-1.30.3`
  (`verapdf` on PATH, 2026-10-17). GitHub Actions installs the same version.
- After uploading to eLearning, check the Ally score is green.
- Result 2026-10-14: `syllabus/syllabus.pdf` passes PDF/UA-2 in both the draft
  and final builds.
- A machine check is necessary but not sufficient. Before the semester, a person
  should read one PDF with a screen reader (NVDA or Orca) and fix anything that
  reads badly.
