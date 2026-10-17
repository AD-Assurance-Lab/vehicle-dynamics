/* ME 4650/5950 course kit: slide navigation, click-by-click steps, notes view, math.
   No dependencies except vendor/temml.min.js (LaTeX -> native MathML).
   Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.

   Authoring rules (see common/kit/README.md):
   - Each slide is <section class="slide"> with an <h2> (the title slide uses <h1>).
   - Add class "step" to anything that should appear on a click.
   - Math: \( ... \) inline and \[ ... \] display, written as LaTeX.
   - .present-only: only on the projected slides. .notes: only in notes view and print.
   - .screen-only needs data-fallback="id" pointing to a .print-only element.
   - <div class="workspace" style="--h:2.5in"></div>: blank box, printed handout only.

   Keys: Right/Space/PageDown next, Left/PageUp back, Home/End, R notes view, F fullscreen,
   G then a number and Enter to go to a slide. Presenter clickers send PageUp/PageDown. */
(function () {
  "use strict";

  // ---------- math: render \( \) and \[ \] to MathML with Temml ----------
  function renderMath(root) {
    if (!window.temml) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(n) {
        if (!/\\\(|\\\[/.test(n.nodeValue)) return NodeFilter.FILTER_REJECT;
        const p = n.parentElement;
        if (!p || p.closest("script,style,code,pre,textarea,math")) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    const re = /\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)/g;
    for (const node of nodes) {
      const text = node.nodeValue;
      const frag = document.createDocumentFragment();
      let last = 0, m;
      while ((m = re.exec(text))) {
        if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)));
        const display = m[1] !== undefined;
        const tex = display ? m[1] : m[2];
        const span = document.createElement("span");
        try {
          temml.render(tex, span, { displayMode: display, annotate: true });
        } catch (e) {
          span.textContent = tex;
          console.error("math error:", tex, e);
        }
        const math = span.firstElementChild;
        if (math) { math.setAttribute("alttext", tex); frag.appendChild(math); }
        last = re.lastIndex;
      }
      if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    }
  }

  // ---------- views ----------
  const slides = () => Array.from(document.querySelectorAll("main > section.slide"));
  let idx = 0;

  function fit() {
    const s = Math.min(window.innerWidth / 1280, (window.innerHeight - 26) / 720);
    document.documentElement.style.setProperty("--scale", s.toFixed(4));
  }

  function stepsOf(slide) { return Array.from(slide.querySelectorAll(".step")); }

  function show(i, fromBack) {
    const all = slides();
    idx = Math.max(0, Math.min(all.length - 1, i));
    all.forEach((s, k) => {
      s.classList.toggle("current", k === idx);
      s.setAttribute("aria-hidden", k === idx ? "false" : "true");
    });
    stepsOf(all[idx]).forEach(st => st.classList.toggle("shown", !!fromBack));
    const counter = document.querySelector(".slide-counter");
    if (counter) counter.textContent = (idx + 1) + " / " + all.length;
    const bar = document.querySelector(".progress");
    if (bar) bar.style.width = (100 * (idx + 1) / all.length) + "%";
    history.replaceState(null, "", "#" + (idx + 1));
    const live = document.querySelector(".live");
    if (live) live.textContent = "Slide " + (idx + 1) + ": " + (all[idx].querySelector("h1,h2") || {}).textContent;
  }

  function next() {
    const pending = stepsOf(slides()[idx]).find(s => !s.classList.contains("shown"));
    if (pending) pending.classList.add("shown");
    else if (idx < slides().length - 1) show(idx + 1);
  }

  function prev() {
    const shown = stepsOf(slides()[idx]).filter(s => s.classList.contains("shown"));
    if (shown.length) shown[shown.length - 1].classList.remove("shown");
    else if (idx > 0) show(idx - 1, true);
  }

  function setView(view) {
    document.body.classList.toggle("present", view === "present");
    document.body.classList.toggle("read", view === "read");
    const t = document.querySelector(".view-toggle");
    if (t) t.textContent = view === "present" ? "Notes view (R)" : "Slide view (R)";
    slides().forEach(s => s.removeAttribute("aria-hidden"));
    if (view === "present") { fit(); show(idx); }
    try { localStorage.setItem("course-view", view); } catch (e) { /* storage blocked */ }
  }

  // ---------- startup ----------
  function init() {
    renderMath(document.body);

    // view toggle, footer bar, progress, live region
    const toggle = document.createElement("button");
    toggle.className = "view-toggle";
    toggle.type = "button";
    toggle.addEventListener("click", () => setView(document.body.classList.contains("present") ? "read" : "present"));
    document.body.prepend(toggle);
    const bar = document.createElement("div");
    bar.className = "chrome-bar";
    bar.innerHTML = '<span>' + (document.body.dataset.course || "") + '</span><span class="slide-counter"></span>';
    document.body.appendChild(bar);
    const prog = document.createElement("div");
    prog.className = "progress";
    document.body.appendChild(prog);
    const live = document.createElement("div");
    live.className = "live";
    live.setAttribute("aria-live", "polite");
    live.style.cssText = "position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)";
    document.body.appendChild(live);

    const hash = parseInt(location.hash.slice(1), 10);
    if (hash > 0) idx = hash - 1;
    let view = new URLSearchParams(location.search).get("view") || document.body.dataset.view;
    if (!view) { try { view = localStorage.getItem("course-view"); } catch (e) { view = null; } }
    if (!view) view = window.innerWidth >= 900 ? "present" : "read";
    setView(view);

    window.addEventListener("resize", () => { if (document.body.classList.contains("present")) fit(); });

    let goto = "";
    document.addEventListener("keydown", e => {
      if (e.target.closest("input,select,textarea")) return;
      const present = document.body.classList.contains("present");
      const k = e.key;
      if (k === "r" || k === "R") { setView(present ? "read" : "present"); return; }
      if (!present) return;
      if (k === "f" || k === "F") { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); return; }
      if (k === "g" || k === "G") { goto = "g"; return; }
      if (goto && /^[0-9]$/.test(k)) { goto += k; return; }
      if (goto && k === "Enter") { const n = parseInt(goto.slice(1), 10); goto = ""; if (n) show(n - 1); return; }
      goto = "";
      if (["ArrowRight", " ", "PageDown", "ArrowDown"].includes(k)) { e.preventDefault(); next(); }
      else if (["ArrowLeft", "PageUp", "ArrowUp"].includes(k)) { e.preventDefault(); prev(); }
      else if (k === "Home") show(0);
      else if (k === "End") show(slides().length - 1);
    });
    document.querySelector("main").addEventListener("click", e => {
      if (!document.body.classList.contains("present")) return;
      if (e.target.closest("a,button,input,select,label,.interactive")) return;
      next();
    });

    document.documentElement.dataset.ready = "true";   // the PDF build waits for this
  }

  window.CourseKit = { renderMath };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
