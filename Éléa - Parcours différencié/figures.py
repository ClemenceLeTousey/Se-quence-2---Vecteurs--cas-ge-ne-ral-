# -*- coding: utf-8 -*-
"""Figures TikZ pour le parcours Éléa — compilées en PNG (pdflatex + gs)."""
import math, os, subprocess, shutil, base64

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")

PREAMBLE = r"""
\documentclass[border=5pt]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,shapes.misc,calc}
\renewcommand{\familydefault}{\sfdefault}
\tikzset{
  ptcross/.style={cross out,draw,thick,minimum size=1.6mm,inner sep=0pt},
  vec/.style={->,thick,>={Stealth[length=2.6mm]}},
  vecu/.style={vec,color=blue!70!black},
  vecv/.style={vec,color=red!75!black},
  vecw/.style={vec,color=green!45!black},
  grid/.style={gray!35,thin},
}
\newcommand{\Vj}[1]{\overrightarrow{\text{#1}}}
\newcommand{\pt}[4]{\node[ptcross] at (#1,#2) {}; \node[anchor=#4,inner sep=2pt] at (#1,#2) {$#3$};}
\begin{document}
\begin{tikzpicture}[x=0.75cm,y=0.75cm]
"""
POSTAMBLE = r"""
\end{tikzpicture}
\end{document}
"""

def grid(w, h):
    return r"\draw[grid] (0,0) grid (%d,%d);" % (w, h) + "\n"

def vec(x1, y1, x2, y2, style="vec", label=None, pos="above"):
    s = r"\draw[%s] (%s,%s) -- (%s,%s)" % (style, x1, y1, x2, y2)
    if label:
        s += r" node[midway,%s=1pt,inner sep=1pt] {$%s$}" % (pos, label)
    return s + ";\n"

def named_vec(a, b, x1, y1, x2, y2, anchor_a="south", anchor_b="south", style="vec"):
    return (vec(x1, y1, x2, y2, style) +
            r"\pt{%s}{%s}{%s}{%s}" % (x1, y1, a, anchor_a) + "\n" +
            r"\pt{%s}{%s}{%s}{%s}" % (x2, y2, b, anchor_b) + "\n")

FIGS = {}

# ---------- Bloc 1 ----------
# Image d'un point par une translation sur quadrillage
FIGS["b1a"] = grid(10, 8) + named_vec("A", "B", 1, 1, 4, 2, "north", "north") + \
    r"\pt{2}{4}{L}{east}" + "\n" + \
    r"\pt{5}{5}{M}{west}" + "\n" + r"\pt{5}{3}{N}{west}" + "\n" + \
    r"\pt{3}{7}{R}{south}" + "\n" + r"\pt{6}{5}{S}{south west}" + "\n"

# Six vecteurs sur quadrillage : égal, opposé, même sens norme double, autre direction
FIGS["b1b"] = grid(12, 8) + \
    named_vec("A", "B", 1, 1, 4, 2, "north", "north") + \
    named_vec("C", "D", 6, 4, 9, 5, "north", "north") + \
    named_vec("E", "F", 9, 2, 6, 1, "south", "north") + \
    named_vec("G", "H", 1, 4, 7, 6, "south east", "south") + \
    named_vec("I", "J", 8, 7, 11, 6, "south", "south") + \
    named_vec("K", "L", 10, 1, 11, 4, "north", "south")

# Parallélogramme ABCD de centre O (générique)
FIGS["b1c"] = r"""
\coordinate (A) at (0,0); \coordinate (B) at (5,0); \coordinate (C) at (6.6,2.6); \coordinate (D) at (1.6,2.6);
\coordinate (O) at ($(A)!0.5!(C)$);
\draw[thick] (A) -- (B) -- (C) -- (D) -- cycle;
\draw[gray,dashed] (A) -- (C); \draw[gray,dashed] (B) -- (D);
\pt{0}{0}{A}{north east} \pt{5}{0}{B}{north west} \pt{6.6}{2.6}{C}{south west} \pt{1.6}{2.6}{D}{south east}
\node[ptcross] at (O) {}; \node[anchor=south,inner sep=2pt] at (O) {$O$};
"""

# Représentants d'un vecteur u sur quadrillage
FIGS["b1e"] = grid(10, 8) + vec(1, 6, 3, 7, "vecu", r"\vec u", "above") + \
    "".join(r"\pt{%s}{%s}{%s}{%s}" % p + "\n" for p in
            [(2,1,"A","north"),(4,2,"B","north"),(6,4,"C","north"),(8,5,"D","north"),
             (4,5,"E","south"),(2,4,"F","south"),(7,2,"G","north"),(9,1,"H","north")])

# Hexagone régulier ABCDEF de centre O
def hexagon(with_uv=False):
    R = 2.2
    pts = {L: (R*math.cos(math.radians(60*i)), R*math.sin(math.radians(60*i))) for i, L in enumerate("ABCDEF")}
    anchors = {"A": "west", "B": "south west", "C": "south east", "D": "east", "E": "north east", "F": "north west"}
    s = r"\draw[thick] " + " -- ".join("(%.3f,%.3f)" % pts[L] for L in "ABCDEF") + " -- cycle;\n"
    for L in "ABCDEF":
        s += r"\draw[gray!60,thin] (0,0) -- (%.3f,%.3f);" % pts[L] + "\n"
        s += r"\pt{%.3f}{%.3f}{%s}{%s}" % (pts[L][0], pts[L][1], L, anchors[L]) + "\n"
    s += r"\pt{0}{0}{O}{north}" + "\n"
    if with_uv:
        s += vec(0, 0, *pts["A"], "vecu", r"\vec u", "below")
        s += vec(0, 0, *pts["B"], "vecv", r"\vec v", "left")
    return s
FIGS["hex"] = hexagon()
FIGS["hex_uv"] = hexagon(True)

# ---------- Bloc 2 ----------
FIGS["b2a"] = grid(12, 8) + vec(1, 1, 4, 2, "vecu", r"\vec u", "above") + vec(1, 4, 2, 6, "vecv", r"\vec v", "left") + \
    vec(6, 1, 10, 4, "vec", r"\vec a", "below") + vec(6, 6, 8, 5, "vec", r"\vec b", "above") + \
    vec(11, 7, 7, 4, "vec", r"\vec c", "above") + vec(5, 7, 9, 8, "vec", r"\vec d", "below")

# ---------- Bloc 3 ----------
def numberline(A, B, C, lo=-3, hi=7):
    s = r"\draw[thick,gray] (%d,0) -- (%d,0);" % (lo - 0.5, hi + 0.5) + "\n"
    for t in range(lo, hi + 1):
        s += r"\draw[gray] (%d,-0.12) -- (%d,0.12);" % (t, t) + "\n"
    s += vec(A, 0.8, B, 0.8, "vecu", r"\Vj{AB}", "above")
    s += vec(A, -0.8, C, -0.8, "vecv", r"\Vj{AC}", "below")
    s += r"\draw[gray!60,dotted] (%d,-0.8) -- (%d,0.8);" % (A, A) + "\n"
    for L, x, anc in (("A", A, "north east"), ("B", B, "south"), ("C", C, "north")):
        s += r"\node[ptcross] at (%d,0) {};" % x + "\n"
        s += r"\node[anchor=%s,inner sep=2pt] at (%d,0) {$%s$};" % (anc, x, L) + "\n"
    return s
FIGS["b3a1"] = numberline(0, 2, 6)
FIGS["b3a2"] = numberline(4, 6, 0)
FIGS["b3a3"] = numberline(0, 4, 2)
FIGS["b3a4"] = numberline(0, 3, -2)

FIGS["b3b"] = grid(10, 7) + vec(1, 1, 3, 2, "vecu", r"\vec u", "below") + \
    vec(8, 5, 4, 3, "vecv", r"\vec v", "above") + vec(1, 4, 5, 7, "vecw", r"\vec w", "above")

# ---------- Bloc 4 ----------
FIGS["b4a"] = grid(12, 8) + vec(1, 1, 3, 2, "vecu", r"\vec u", "below") + vec(2, 4, 1, 5, "vecv", r"\vec v", "right") + \
    vec(5, 1, 8, 4, "vec", r"\vec{w_1}", "below") + vec(5, 7, 9, 6, "vec", r"\vec{w_2}", "above") + \
    vec(11, 2, 8, 2, "vec", r"\vec{w_3}", "above")

FIGS["b4b"] = r"""
\coordinate (A) at (0,0); \coordinate (B) at (5,0); \coordinate (C) at (6.6,2.6); \coordinate (D) at (1.6,2.6);
\coordinate (I) at ($(C)!0.5!(D)$);
\draw[thick] (A) -- (B) -- (C) -- (D) -- cycle;
\draw[gray,dashed] (A) -- (I);
\draw[vecu] (A) -- (B) node[midway,below=1pt] {$\vec u$};
\draw[vecv] (A) -- (D) node[midway,left=1pt] {$\vec v$};
\pt{0}{0}{A}{north east} \pt{5}{0}{B}{north west} \pt{6.6}{2.6}{C}{south west} \pt{1.6}{2.6}{D}{south east}
\node[ptcross] at (I) {}; \node[anchor=south,inner sep=2pt] at (I) {$I$};
"""

# ---------- Positionnement ----------
def flag(x, y, n, rot=0, xscale=1):
    return (r"\begin{scope}[shift={(%s,%s)},rotate=%d,xscale=%d]" % (x, y, rot, xscale) +
            r"\draw[thick,fill=blue!12] (0,0) -- (0,1.6) -- (1.1,1.25) -- (0.35,0.9) -- (0.35,0) -- cycle;" +
            r"\node at (0.55,-0.45) {\bfseries %d};\end{scope}" % n + "\n")
FIGS["p1"] = flag(0, 0, 1) + flag(3, 0.7, 2) + flag(7.2, 1.6, 3, rot=180) + flag(1.5, -3.2, 4) + flag(6.2, -3.2, 5, xscale=-1)

FIGS["p2"] = "".join(
    r"\fill (%.1f,%d) circle (1.6pt); \node[anchor=south,inner sep=2pt] at (%.1f,%d) {$%s$};" % (c*1.5, 2-r, c*1.5, 2-r, L) + "\n"
    for r, row in enumerate(["ABCD", "EFGH", "IJKL"]) for c, L in enumerate(row))

FIGS["p3"] = grid(7, 7) + named_vec("A", "B", 1, 1, 4, 5, "north", "south") + \
    r"\draw[gray,dashed] (1,1) -- (4,1) -- (4,5);" + "\n"


def build(names=None, force=False):
    os.makedirs(FIGDIR, exist_ok=True)
    out = {}
    for name, body in FIGS.items():
        if names and name not in names:
            continue
        tex = os.path.join(FIGDIR, "fig_%s.tex" % name)
        pdf = tex[:-4] + ".pdf"
        png = tex[:-4] + ".png"
        src = PREAMBLE + body + POSTAMBLE
        if force or not os.path.exists(png) or open(tex, encoding="utf8").read() != src if os.path.exists(tex) else True:
            with open(tex, "w", encoding="utf8") as f:
                f.write(src)
            r = subprocess.run(["pdflatex", "-interaction=batchmode", "-halt-on-error", "-output-directory", FIGDIR, tex],
                               capture_output=True, text=True)
            if r.returncode != 0 or not os.path.exists(pdf):
                raise RuntimeError("pdflatex failed for %s\n%s" % (name, open(tex[:-4] + ".log", errors="ignore").read()[-1500:]))
            subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", "-r170",
                            "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4", "-sOutputFile=" + png, pdf], check=True)
        out[name] = png
    for ext in (".aux", ".log"):
        for f in os.listdir(FIGDIR):
            if f.endswith(ext):
                os.remove(os.path.join(FIGDIR, f))
    return out

def b64(name):
    with open(os.path.join(FIGDIR, "fig_%s.png" % name), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

if __name__ == "__main__":
    print(build(force=True))
