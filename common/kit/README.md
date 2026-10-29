# Course kit

Every lecture, practice-problem page, quiz and handout uses `course.css` and `course.js`.
One HTML file gives three views:

| View | How to get it | Used for |
|---|---|---|
| Slides | open the file (wide screens default to it) | presenting |
| Notes | press R, or the button at top right, or add `?view=read` | studying, screen readers |
| Handout PDF | `tools/build_pdf.py <file>.html` | printing, writing, Wacom examples |

## Writing a lecture

- One `<section class="slide">` per slide, each with an `<h2>`.
- `class="step"`: appears on the next click in slide view; always shown in notes and print.
- Math: LaTeX between `\( ... \)` (inline) or `\[ ... \]` (display). Rendered to MathML.
  Avoid `\underbrace` and other stretched glyphs: they print without text meaning
  and fail the accessibility check.
- `class="notes"`: what the instructor says; notes view only, never in the handout. `class="present-only"`: slides only.
  `class="no-print"`: everywhere but the handout (credits slide, answers to questions asked live).
  The handout must not answer a question that is asked live in class.
- Examples: `<section class="slide worked-example">` or `group-example`, starting
  with `<span class="example-label">Worked example 1</span>`.
- Blank workspace for the handout: `<div class="workspace" style="--h: 2.4in" aria-hidden="true"></div>`.
- Animations and interactive widgets: wrap in `class="screen-only"` with
  `data-fallback="id"` pointing to a `class="print-only"` element (a static figure
  or table). The PDF build refuses a page that breaks this rule. An animation
  whose resting state is a complete figure (like the Lecture 1A braking race)
  needs no fallback.
- Every image needs alt text. Respect `prefers-reduced-motion` in any animation. Motion that starts by
  itself must stop within 5 s (WCAG 2.2.2); longer animations start from a button.
- Every form control needs a text label; a label that is only math needs `aria-label` too.
- Check the web page with axe (WCAG 2.1 AA) as well as the PDF with veraPDF.
- Math in the handout PDF is tagged as Formula with a spoken form ("a equals d v over d t"), made by the kit
  when `tools/build_pdf.py` prints with `?print=1`. Check new LaTeX constructs read sensibly.
- `aria-live` text must change once per event, never every animation frame. Use `class="sr-only"` for
  text only screen readers need (readings of a drawn gauge, a final result).
- Empty table cells do not get tagged. Put a visible mark such as `?` in blank
  answer cells.

## Keys in slide view

Right, Space, PageDown: next step or slide. Left, PageUp: back. Home/End.
G, a number, Enter: go to a slide. F: fullscreen. R: notes view.

## Third-party files

- `vendor/temml.min.js`, `vendor/Temml-Latin-Modern.css`, `vendor/Temml.woff2`: Temml 0.10.29, MIT (`vendor/temml-LICENSE.txt`).
- `vendor/latinmodern-math.otf`: Latin Modern Math, GUST Font License (from TeX Live).
- `fonts/source-sans-3-*.woff2`: Source Sans 3, SIL Open Font License (`fonts/OFL.txt`).
