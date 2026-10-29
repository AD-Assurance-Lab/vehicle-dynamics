#!/usr/bin/env python3
# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
"""Build the printable handout PDF from a lecture (or any course) HTML file.

    tools/.venv/bin/python tools/build_pdf.py lectures/wk01-point-mass/lecture-01a.html

Steps:
1. Check the print-fallback rule: every .screen-only element names a .print-only
   element with data-fallback="id".
2. Print with headless Google Chrome (tagged PDF, letter paper from the CSS).
3. Fix what Chrome leaves out of a PDF/UA file: XMP metadata, document title
   display, a role map for non-standard tags, alt text on figures, and untagged
   drawing (borders, page numbers) marked as artifacts.
4. Validate with veraPDF (PDF/UA-1). A failing file is reported and exits nonzero.

The PDF is written next to the HTML file with the same name.
Setup: python3 -m venv tools/.venv && tools/.venv/bin/pip install -r tools/requirements.txt
veraPDF: set VERAPDF to the verapdf launcher, or put verapdf on PATH.
"""
import html.parser
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pikepdf

STANDARD_TYPES = {
    "Document", "Part", "Art", "Sect", "Div", "BlockQuote", "Caption", "TOC", "TOCI", "Index",
    "NonStruct", "Private", "P", "H", "H1", "H2", "H3", "H4", "H5", "H6", "L", "LI", "Lbl", "LBody",
    "Table", "TR", "TH", "TD", "THead", "TBody", "TFoot", "Span", "Quote", "Note", "Reference",
    "BibEntry", "Code", "Link", "Annot", "Ruby", "RB", "RT", "RP", "Warichu", "WT", "WP",
    "Figure", "Formula", "Form",
}
ROLE_FALLBACK = {"Strong": "Span", "Em": "Span", "Sub": "Span", "Sup": "Span", "Mark": "Span",
                 "Title": "H1", "FENote": "Note", "Aside": "Div", "DocumentFragment": "Div"}


# ------------------------------------------------------------------ 1. fallback rule
class FallbackCheck(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.screen_only, self.print_ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if "screen-only" in classes:
            self.screen_only.append((self.getpos()[0], a.get("data-fallback")))
        if "print-only" in classes and a.get("id"):
            self.print_ids.add(a["id"])


def check_fallbacks(path):
    p = FallbackCheck()
    p.feed(Path(path).read_text(encoding="utf-8"))
    problems = [f"line {ln}: .screen-only element has no data-fallback" if not fb else
                f"line {ln}: data-fallback '{fb}' does not match a .print-only id"
                for ln, fb in p.screen_only if not fb or fb not in p.print_ids]
    return problems


# ------------------------------------------------------------------ 2. print
def chrome():
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if shutil.which(name):
            return shutil.which(name)
    sys.exit("Google Chrome or Chromium not found")


def print_pdf(html_path, pdf_path):
    with tempfile.TemporaryDirectory() as profile:
        cmd = [chrome(), "--headless=new", "--disable-gpu", "--no-sandbox", f"--user-data-dir={profile}",
               "--no-pdf-header-footer", "--generate-pdf-document-outline", "--allow-file-access-from-files",
               "--virtual-time-budget=15000", f"--print-to-pdf={pdf_path}", Path(html_path).resolve().as_uri() + "?print=1"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not Path(pdf_path).exists():
        sys.exit("Chrome did not write a PDF:\n" + r.stderr[-2000:])


# ------------------------------------------------------------------ 3. fix-up
def walk_struct(elem, visit):
    if not isinstance(elem, pikepdf.Dictionary):
        return
    visit(elem)
    kids = elem.get("/K")
    if kids is None:
        return
    for k in (kids if isinstance(kids, pikepdf.Array) else [kids]):
        if isinstance(k, pikepdf.Dictionary) and "/S" in k:
            walk_struct(k, visit)


def has_alt_below(elem):
    found = []
    walk_struct(elem, lambda e: found.append(str(e["/Alt"])) if "/Alt" in e and e is not elem else None)
    return found[0] if found else None


def wrap_list_items(pdf, st):
    """PDF/UA wants LI -> Lbl/LBody. Chrome puts content straight under LI; wrap it in an LBody."""
    moved = {}
    def visit(e):
        if str(e["/S"]) != "/LI" or "/K" not in e:
            return
        kids = e.K if isinstance(e.K, pikepdf.Array) else pikepdf.Array([e.K])
        if all(isinstance(k, pikepdf.Dictionary) and str(k.get("/S")) in ("/Lbl", "/LBody") for k in kids):
            return
        body = pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.StructElem, S=pikepdf.Name.LBody, P=e, K=kids))
        if "/Pg" in e:
            body.Pg = e.Pg
        for k in kids:
            if isinstance(k, pikepdf.Dictionary) and "/S" in k:
                k.P = body
        e.K = pikepdf.Array([body])
        moved[e.objgen] = body
    for k in (st.K if isinstance(st.K, pikepdf.Array) else [st.K]):
        walk_struct(k, visit)
    if not moved or "/ParentTree" not in st:
        return
    def fix_tree(node):
        if "/Nums" in node:
            nums = node.Nums
            for i in range(1, len(nums), 2):
                v = nums[i]
                if isinstance(v, pikepdf.Array):
                    for j in range(len(v)):
                        if isinstance(v[j], pikepdf.Dictionary) and v[j].objgen in moved:
                            v[j] = moved[v[j].objgen]
                elif isinstance(v, pikepdf.Dictionary) and v.objgen in moved:
                    nums[i] = moved[v.objgen]
        for kid in node.get("/Kids", []):
            fix_tree(kid)
    fix_tree(st.ParentTree)


def artifact_untagged(pdf, page):
    """Wrap drawing that sits outside any marked content in /Artifact BMC ... EMC."""
    ops = pikepdf.parse_content_stream(page)
    out, run, depth = [], [], 0
    painting = {"S", "s", "f", "F", "f*", "B", "B*", "b", "b*", "Tj", "TJ", "'", '"', "Do", "sh", "BI"}

    def flush():
        nonlocal run
        if run:
            if any(str(op) in painting for _, op in run):
                out.append(([pikepdf.Name("/Artifact")], pikepdf.Operator("BMC")))
                out.extend(run)
                out.append(([], pikepdf.Operator("EMC")))
            else:
                out.extend(run)
            run = []

    for operands, op in ops:
        name = str(op)
        if name in ("BMC", "BDC"):
            if depth == 0:
                flush()
            depth += 1
            out.append((operands, op))
        elif name == "EMC":
            depth -= 1
            out.append((operands, op))
        elif depth == 0:
            run.append((operands, op))
        else:
            out.append((operands, op))
    flush()
    page.Contents = pdf.make_stream(pikepdf.unparse_content_stream(out))


def fix_pdf(pdf_path, title, lang):
    with pikepdf.open(pdf_path, allow_overwriting_input=True) as pdf:
        root = pdf.Root
        root.Lang = pikepdf.String(lang)
        root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
        root.MarkInfo = pikepdf.Dictionary(Marked=True)
        pdf.docinfo["/Title"] = title
        with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
            meta["dc:title"] = title
            meta["pdfuaid:part"] = "1"
        st = root.get("/StructTreeRoot")
        if st is not None:
            role = st.get("/RoleMap") or pikepdf.Dictionary()
            def visit(e):
                s = str(e["/S"])[1:]
                if s not in STANDARD_TYPES and pikepdf.Name("/" + s) not in role:
                    role[pikepdf.Name("/" + s)] = pikepdf.Name("/" + ROLE_FALLBACK.get(s, "Span"))
                if s == "Figure" and str(e.get("/Alt", "")).startswith("Math: "):
                    e.S = pikepdf.Name("/Formula")      # kit wrapped this formula with its spoken form
                    e.Alt = pikepdf.String(str(e.Alt)[6:])
                    return
                if s == "Figure" and "/Alt" not in e:
                    alt = has_alt_below(e)
                    if alt:
                        e.Alt = pikepdf.String(alt)
                    else:
                        e.S = pikepdf.Name("/Div")      # a grouping <figure> with no image of its own
            for k in (st.K if isinstance(st.K, pikepdf.Array) else [st.K]):
                walk_struct(k, visit)
            st.RoleMap = role
            wrap_list_items(pdf, st)
        for page in pdf.pages:
            artifact_untagged(pdf, page)
        pdf.save(pdf_path)


# ------------------------------------------------------------------ 4. validate
def verapdf(pdf_path):
    exe = os.environ.get("VERAPDF") or shutil.which("verapdf")
    if not exe:
        print("  veraPDF not found (set VERAPDF): NOT VALIDATED")
        return None
    r = subprocess.run([exe, "--flavour", "ua1", "--format", "text", str(pdf_path)], capture_output=True, text=True)
    line = (r.stdout.strip().splitlines() or ["?"])[-1]
    print("  veraPDF:", line)
    return line.startswith("PASS")


def main(paths):
    ok = True
    for html_path in paths:
        html_path = Path(html_path)
        print(html_path)
        problems = check_fallbacks(html_path)
        if problems:
            print("  print-fallback rule failed:\n   " + "\n   ".join(problems))
            ok = False
            continue
        pdf_path = html_path.with_suffix(".pdf")
        print_pdf(html_path, pdf_path)
        title = "Untitled"
        text = html_path.read_text(encoding="utf-8")
        if "<title>" in text:
            title = text.split("<title>", 1)[1].split("</title>", 1)[0].strip()
        lang = text.split('lang="', 1)[1].split('"', 1)[0] if 'lang="' in text else "en-US"
        fix_pdf(pdf_path, title, lang)
        with pikepdf.open(pdf_path) as pdf:
            print(f"  {len(pdf.pages)} pages -> {pdf_path}")
        ok = (verapdf(pdf_path) is not False) and ok
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1:] or sys.exit(__doc__))
