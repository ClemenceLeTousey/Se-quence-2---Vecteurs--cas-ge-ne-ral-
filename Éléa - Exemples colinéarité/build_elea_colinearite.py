# -*- coding: utf-8 -*-
"""
Version Éléa (Moodle) de la page « Exemples colinéarité.html » :
  - Exemples colinéarité - Éléa - Banque de questions.xml  (Moodle XML, à importer)
  - Exemples colinéarité - Éléa - Cours.html               (à coller dans une ressource Page)
  - Exemples colinéarité - Éléa - Fiche de montage.html    (mode d'emploi)
Même principe que la page HTML : sous chaque question un point méthode,
puis (après la réponse) une correction par étapes avec les droites tracées.
Mêmes vecteurs et mêmes points que « Exemples colinéarité.tex ».
Usage : python3 build_elea_colinearite.py
"""
import os, re, html, base64, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
BASE = "Exemples colinéarité - Éléa - "

# ============================================================================
# Figures TikZ → PNG (pdflatex + gs), comme pour le parcours Éléa de la séquence
# ============================================================================
PREAMBLE = r"""
\documentclass[border=4pt]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,shapes.misc}
\renewcommand{\familydefault}{\sfdefault}
\definecolor{vbleu}{HTML}{1C5FD6}
\definecolor{orange}{HTML}{E8590C}
\definecolor{vert}{HTML}{2F9E44}
\definecolor{gris}{HTML}{495057}
\definecolor{violet}{HTML}{7048E8}
\tikzset{
  vec/.style={->,very thick,>={Stealth[length=2.4mm]}},
  ref/.style={orange,thick,dashed},
  par/.style={vert,thick,dashed},
  sec/.style={gris,thick,dashed},
  ptcross/.style={cross out,draw,thick,minimum size=1.6mm,inner sep=0pt},
}
\begin{document}
\begin{tikzpicture}[x=0.5cm,y=0.5cm]
"""
POSTAMBLE = "\n\\end{tikzpicture}\n\\end{document}\n"

# ---------- Exercice 1 : dix vecteurs (repère du .tex) ----------
W1, H1 = 22, 9
EX1 = {  # nom : (x1, y1, x2, y2, décalage étiquette dx, dy)
    "u": (1, 7, 3, 8, -0.4, 0.5),
    "t": (5, 6, 6, 8, -0.5, 0),
    "w": (8, 8, 11, 6, 0.5, 0.5),
    "v": (17, 9, 13, 7, -0.4, 0.55),
    "c": (18, 6, 22, 8, -0.45, 0.55),
    "a": (20, 5, 18, 1, 0.5, 0.1),
    "b": (16, 1, 13, 3, -0.5, -0.45),
    "d": (16, 4, 19, 5, -0.4, 0.55),
    "s": (7, 0, 1, 4, 0.5, 0.5),
    "r": (8, 2, 14, 5, -0.45, 0.6),
}
# ---------- Exercice 2 : neuf points ----------
W2, H2 = 14, 8
EX2 = {"A": (1, 2, "north"), "B": (4, 3, "south"), "C": (11, 7, "south"), "D": (5, 5, "south"),
       "E": (6, 1, "north"), "F": (9, 3, "south"), "G": (13, 4, "west"), "H": (4, 1, "north"), "K": (10, 5, "south")}

def line_through(x, y, dx, dy, style):
    return r"\draw[%s] (%s,%s) -- (%s,%s);" % (style, x - 40 * dx, y - 40 * dy, x + 40 * dx, y + 40 * dy) + "\n"

def fig_ex1(lines=(), par=()):
    """lines : [(nom, style)] droites qui portent les vecteurs ; par : [(ref, at, style)] parallèle à ref par l'origine de at."""
    s = r"\draw[gray!35,thin,step=0.5cm] (0,0) grid (%d,%d);" % (W1, H1) + "\n"
    s += r"\begin{scope}\clip (0,0) rectangle (%d,%d);" % (W1, H1) + "\n"
    for n, st in lines:
        x1, y1, x2, y2 = EX1[n][:4]
        s += line_through(x1, y1, x2 - x1, y2 - y1, st)
    for ref, at, st in par:
        R, A = EX1[ref], EX1[at]
        s += line_through(A[0], A[1], R[2] - R[0], R[3] - R[1], st)
    s += r"\end{scope}" + "\n"
    for n, (x1, y1, x2, y2, dx, dy) in EX1.items():
        s += r"\draw[vec,vbleu] (%s,%s) -- (%s,%s);" % (x1, y1, x2, y2) + "\n"
        s += r"\node[vbleu] at (%s,%s) {$\vec{%s}$};" % ((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, n) + "\n"
    return s

def fig_ex2(lines=(), arrows=()):
    s = r"\draw[gray!35,thin,step=0.5cm] (0,0) grid (%d,%d);" % (W2, H2) + "\n"
    s += r"\begin{scope}\clip (0,0) rectangle (%d,%d);" % (W2, H2) + "\n"
    for n, st in lines:
        (xa, ya, _), (xb, yb, _) = EX2[n[0]], EX2[n[1]]
        s += line_through(xa, ya, xb - xa, yb - ya, st)
    s += r"\end{scope}" + "\n"
    for n, col in arrows:
        (xa, ya, _), (xb, yb, _) = EX2[n[0]], EX2[n[1]]
        s += r"\draw[vec,%s] (%s,%s) -- (%s,%s);" % (col, xa, ya, xb, yb) + "\n"
    for n, (x, y, anc) in EX2.items():
        s += r"\node[ptcross] at (%s,%s) {}; \node[anchor=%s,inner sep=3pt] at (%s,%s) {%s};" % (x, y, anc, x, y, n) + "\n"
    return s

def fig_cours():
    s = r"\begin{scope}[x=0.8cm,y=0.8cm]" + "\n"
    s += r"\draw[gray!35,thin,step=0.8cm] (0,0) grid (8,5);" + "\n"
    s += r"\begin{scope}\clip (0,0) rectangle (8,5);" + "\n"
    s += line_through(1, 3, 2, 1, "par") + line_through(5, 3, -4, -2, "par") + line_through(6, 1, 1, 2, "sec")
    s += r"\end{scope}" + "\n"
    s += r"\draw[vec,vbleu] (1,3) -- (3,4) node[midway,above left] {$\vec{u}$};" + "\n"
    s += r"\draw[vec,orange] (5,3) -- (1,1) node[midway,above=2pt] {$\vec{v}$};" + "\n"
    s += r"\draw[vec,violet] (6,1) -- (7,3) node[midway,right=2pt] {$\vec{w}$};" + "\n"
    return s + r"\end{scope}" + "\n"

FIGS = {
    "ex1": fig_ex1(),
    "ex1_q1a": fig_ex1(lines=[("u", "ref")]),
    "ex1_q1b": fig_ex1(lines=[("u", "ref"), ("v", "par"), ("c", "par"), ("r", "par")]),
    "ex1_q2wa": fig_ex1(lines=[("w", "ref")]),
    "ex1_q2wb": fig_ex1(lines=[("w", "ref"), ("b", "par"), ("s", "par")]),
    "ex1_q2ta": fig_ex1(lines=[("t", "ref")]),
    "ex1_q2tb": fig_ex1(lines=[("t", "ref"), ("a", "par")]),
    "ex1_q3a": fig_ex1(lines=[("u", "ref")], par=[("u", "d", "par")]),
    "ex1_q3b": fig_ex1(lines=[("u", "ref"), ("d", "sec")], par=[("u", "d", "par")]),
    "ex2": fig_ex2(),
    "ex2_q1a": fig_ex2(lines=[("AB", "ref"), ("CD", "par"), ("GH", "par")]),
    "ex2_q1b": fig_ex2(lines=[("AB", "ref"), ("EF", "sec")], arrows=[("AK", "vert")]),
    "ex2_q2": fig_ex2(lines=[("AB", "ref")], arrows=[("AB", "vbleu"), ("CD", "vert"), ("GH", "vert"), ("AK", "vert")]),
    "ex2_q3": fig_ex2(lines=[("CD", "ref"), ("GH", "par")], arrows=[("CD", "orange"), ("GH", "vert")]),
    "ex2_q4": fig_ex2(lines=[("AB", "ref"), ("CD", "par")], arrows=[("AK", "vert")]),
    "cours": fig_cours(),
}

def build_figures():
    os.makedirs(FIGDIR, exist_ok=True)
    for name, body in FIGS.items():
        tex = os.path.join(FIGDIR, "fig_%s.tex" % name)
        pdf, png = tex[:-4] + ".pdf", tex[:-4] + ".png"
        src = PREAMBLE + body + POSTAMBLE
        if os.path.exists(png) and os.path.exists(tex) and open(tex, encoding="utf8").read() == src:
            continue
        with open(tex, "w", encoding="utf8") as f:
            f.write(src)
        r = subprocess.run(["pdflatex", "-interaction=batchmode", "-halt-on-error", "-output-directory", FIGDIR, tex],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("pdflatex a échoué pour %s" % name)
        subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", "-r170",
                        "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4", "-sOutputFile=" + png, pdf], check=True)
    for f in os.listdir(FIGDIR):
        if f.endswith((".aux", ".log")):
            os.remove(os.path.join(FIGDIR, f))

def b64(name):
    with open(os.path.join(FIGDIR, "fig_%s.png" % name), "rb") as f:
        return base64.b64encode(f.read()).decode()

# ============================================================================
# Notation et blocs de mise en forme
# ============================================================================
def V(ab):
    return r"\(\overrightarrow{\mathrm{%s}}\)" % ab
def v(u):
    return r"\(\vec{%s}\)" % u
def M(e):
    return r"\(%s\)" % e
F32, F12 = r"\(\dfrac{3}{2}\)", r"\(\dfrac{1}{2}\)"

def fig(name, width=520):
    return '<p style="text-align:center"><img src="@@PLUGINFILE@@/fig_%s.png" alt="figure" width="%d"></p>' % (name, width)

def methode(*paras):
    return ('<div style="background:#fff6df;border-left:4px solid #d4a72c;padding:8px 12px;margin:10px 0;">'
            '<p style="color:#9a7212;margin:0 0 4px;">Point méthode</p>' + "".join("<p>%s</p>" % p for p in paras) + "</div>")

def etape(titre, texte, figure=None):
    s = '<p style="color:#2f9e44;margin:10px 0 2px;">%s</p><p>%s</p>' % (titre, texte)
    return s + (fig(figure, 460) if figure else "")

def remarque(texte):
    return ('<div style="border-top:1px dashed #2f9e44;margin-top:10px;padding-top:6px;">'
            '<p style="color:#56677a;margin:0 0 2px;">Remarque — Vérifier avec les carreaux</p><p>%s</p></div>' % texte)

def tableau(cols, h, vt):
    td = 'style="border:1px solid #cfd9e3;padding:3px 12px;text-align:center"'
    th = 'style="border:1px solid #cfd9e3;padding:3px 12px;text-align:left;color:#56677a"'
    row = lambda lab, vals: "<tr><td %s>%s</td>%s</tr>" % (th, lab, "".join("<td %s>%s</td>" % (td, x) for x in vals))
    return ('<table style="border-collapse:collapse;margin:6px 0">' + row("", cols) +
            row("Déplacement horizontal (carreaux)", h) + row("Déplacement vertical (carreaux)", vt) + "</table>")

def correction(*blocs):
    return ('<div style="background:#eaf6ec;border-left:4px solid #3f9a4f;padding:8px 14px;">'
            '<p style="color:#3f9a4f;margin:0;">Correction</p>' + "".join(blocs) + "</div>")

# ============================================================================
# Banque de questions
# ============================================================================
Q = []
def add(**kw):
    Q.append(kw)

CAT = "Séquence 2 – Vecteurs/Exemples colinéarité"
INTRO1 = "<p>On a représenté ci-dessous dix vecteurs dans un quadrillage.</p>" + fig("ex1")
INTRO2 = "<p>On considère les points placés dans le quadrillage ci-dessous.</p>" + fig("ex2", 380)

# ---------------- Exercice 1 ----------------
autres_u = {"w": "La droite qui porte " + v("w") + " est sécante avec celle qui porte " + v("u") + ".",
            "t": "La droite qui porte " + v("t") + " est sécante avec celle qui porte " + v("u") + ".",
            "d": v("d") + " ressemble à " + v("u") + ", mais la droite qui le porte n'est pas parallèle à celle de " + v("u") + " (voir la question 3).",
            "s": "La droite qui porte " + v("s") + " est sécante avec celle qui porte " + v("u") + ".",
            "b": "La droite qui porte " + v("b") + " est sécante avec celle qui porte " + v("u") + ".",
            "a": "La droite qui porte " + v("a") + " est sécante avec celle qui porte " + v("u") + "."}
add(type="mc", single=False, name="Ex1-Q1 – Vecteurs colinéaires à u",
    text=INTRO1 + "<p>Cocher <b>tous</b> les vecteurs colinéaires au vecteur " + v("u") + ".</p>" +
         methode("Deux vecteurs sont colinéaires s'ils ont la <i>même direction</i>.",
                 "Pour repérer la direction d'un vecteur, on imagine la droite qui le porte. Deux vecteurs ont la même direction lorsque les droites qui les portent sont parallèles (ou confondues). Le sens et la longueur n'ont pas d'importance.",
                 "En pratique, il est possible de lire le déplacement de chaque vecteur avec les carreaux (horizontalement et verticalement) et de regarder si ces déplacements sont proportionnels à ceux de " + v("u") + "."),
    answers=[(33.33333, v(n), fb) for n, fb in (("v", "Oui : la droite qui porte " + v("v") + " est parallèle à celle de " + v("u") + ", même si " + v("v") + " est de sens opposé."),
                                                 ("c", "Oui : la droite qui porte " + v("c") + " est parallèle à celle de " + v("u") + "."),
                                                 ("r", "Oui : la droite qui porte " + v("r") + " est parallèle à celle de " + v("u") + "."))] +
            [(-33.33333, v(n), autres_u[n]) for n in ("w", "t", "d", "s", "b", "a")],
    hints=["Trace (dans ta tête ou au crayon) la droite qui porte " + v("u") + " : elle monte d'un carreau chaque fois qu'on avance de deux carreaux vers la droite. Quels vecteurs sont portés par une droite parallèle ?",
           "Le sens ne compte pas : un vecteur qui va « dans l'autre sens » peut avoir la même direction. Il y a trois vecteurs à cocher."],
    general=correction(
        etape("Étape 1 — On repère la direction de " + v("u"), "On trace la droite qui porte le vecteur " + v("u") + " (en pointillés orange).", "ex1_q1a"),
        etape("Étape 2 — On cherche les vecteurs qui ont cette direction",
              "Seules les droites qui portent " + v("v") + ", " + v("c") + " et " + v("r") + " (en pointillés verts) sont parallèles à celle de " + v("u") + ".<br>Les droites qui portent les autres vecteurs sont sécantes avec la droite qui porte " + v("u") + ".", "ex1_q1b"),
        etape("Étape 3 — On conclut",
              "Les vecteurs " + v("v") + ", " + v("c") + " et " + v("r") + " ont la même direction que " + v("u") + ".<br>Le sens et la longueur ne comptent pas : " + v("v") + " est de sens opposé, mais il a bien la même direction.<br>Les vecteurs colinéaires à " + v("u") + " sont donc <b>" + v("v") + ", " + v("c") + " et " + v("r") + "</b>."),
        remarque("Le vecteur " + v("u") + " correspond à un déplacement de 2 carreaux vers la droite et 1 carreau vers le haut : le déplacement vertical est la moitié du déplacement horizontal." +
                 tableau([v("u"), v("v"), v("c"), v("r")], [2, 4, 4, 6], [1, 2, 2, 3]) +
                 "C'est un tableau de proportionnalité.<br>À l'inverse, " + v("w") + " correspond à un déplacement de 3 carreaux vers la droite et 2 carreaux vers le bas : 2 n'est pas la moitié de 3.")))

M2 = methode("Même démarche qu'à la question 1.",
             "On imagine la droite qui porte le vecteur de référence, puis on cherche les vecteurs portés par une droite parallèle à celle-ci (ou par la même droite).",
             "Attention, le sens n'a pas d'importance : un vecteur de sens opposé a la même direction.")
autres_w = {n: "La droite qui porte " + v(n) + " est sécante avec celle qui porte " + v("w") + "." for n in ("u", "v", "c", "r", "t", "a", "d")}
add(type="mc", single=False, name="Ex1-Q2a – Vecteurs colinéaires à w",
    text=INTRO1 + "<p>Cocher <b>tous</b> les vecteurs colinéaires au vecteur " + v("w") + ".</p>" + M2,
    answers=[(50, v("b"), "Oui : la droite qui porte " + v("b") + " est parallèle à celle de " + v("w") + " (sens opposé)."),
             (50, v("s"), "Oui : la droite qui porte " + v("s") + " est parallèle à celle de " + v("w") + " (sens opposé).")] +
            [(-25, v(n), autres_w[n]) for n in ("u", "v", "c", "r", "t", "a", "d")],
    hints=["La droite qui porte " + v("w") + " descend de 2 carreaux quand on avance de 3 carreaux vers la droite. Cherche les vecteurs portés par une droite parallèle.",
           "Les deux vecteurs à cocher sont de sens opposé à " + v("w") + "."],
    general=correction(
        etape("Étape 1 — On repère la direction de " + v("w"), "On trace la droite qui porte le vecteur " + v("w") + " (en pointillés orange).", "ex1_q2wa"),
        etape("Étape 2 — On cherche les vecteurs qui ont cette direction",
              "Les droites qui portent " + v("b") + " et " + v("s") + " (en pointillés verts) sont parallèles à la droite qui porte " + v("w") + ".<br>Les droites qui portent les autres vecteurs sont sécantes avec la droite qui porte " + v("w") + ".", "ex1_q2wb"),
        etape("Étape 3 — On conclut",
              "Les vecteurs " + v("b") + " et " + v("s") + " ont la même direction que " + v("w") + ", même s'ils sont de sens opposé.<br>Les vecteurs colinéaires à " + v("w") + " sont donc <b>" + v("b") + " et " + v("s") + "</b>."),
        remarque("Le vecteur " + v("w") + " correspond à un déplacement de 3 carreaux vers la droite et 2 carreaux vers le bas." +
                 tableau([v("w"), v("b"), v("s")], [3, 3, 6], [2, 2, 4]) +
                 "Les déplacements de " + v("b") + " et " + v("s") + " sont proportionnels à ceux de " + v("w") + ".")))

add(type="mc", name="Ex1-Q2b – Vecteur colinéaire à t",
    text=INTRO1 + "<p>Quel vecteur est colinéaire au vecteur " + v("t") + " ?</p>" + M2,
    answers=[(100, v("a"), "Exact : la droite qui porte " + v("a") + " est parallèle à celle de " + v("t") + " (sens opposé).")] +
            [(0, v(n), "La droite qui porte " + v(n) + " est sécante avec celle qui porte " + v("t") + ".") for n in ("u", "d", "r", "s")],
    hints=["La droite qui porte " + v("t") + " monte de 2 carreaux quand on avance d'1 carreau vers la droite : elle est très « pentue ».",
           "Le vecteur cherché est de sens opposé à " + v("t") + "."],
    general=correction(
        etape("Étape 1 — On repère la direction de " + v("t"), "On trace la droite qui porte le vecteur " + v("t") + " (en pointillés orange).", "ex1_q2ta"),
        etape("Étape 2 — On cherche le vecteur qui a cette direction",
              "Seule la droite qui porte " + v("a") + " (en pointillés verts) est parallèle à la droite qui porte " + v("t") + ".<br>Les droites qui portent les autres vecteurs sont sécantes avec la droite qui porte " + v("t") + ".", "ex1_q2tb"),
        etape("Étape 3 — On conclut",
              "Le vecteur " + v("a") + " a la même direction que " + v("t") + ", même s'il est de sens opposé.<br>Le vecteur colinéaire à " + v("t") + " est donc <b>" + v("a") + "</b>."),
        remarque("Le vecteur " + v("t") + " correspond à un déplacement de 1 carreau vers la droite et 2 carreaux vers le haut." +
                 tableau([v("t"), v("a")], [1, 2], [2, 4]) +
                 "Les déplacements de " + v("a") + " sont proportionnels à ceux de " + v("t") + ".")))

add(type="mc", name="Ex1-Q3 – d est-il colinéaire à u ?",
    text=INTRO1 + "<p>Le vecteur " + v("d") + " est-il colinéaire au vecteur " + v("u") + " ? Choisir la bonne réponse <b>et</b> la bonne justification.</p>" +
         methode("Pour montrer que deux vecteurs <i>ne sont pas</i> colinéaires, on montre qu'ils n'ont pas la même direction.",
                 "On imagine la droite qui porte le vecteur " + v("u") + " et la droite qui porte le vecteur " + v("d") + " : si ces droites sont sécantes, les vecteurs ne sont pas colinéaires.",
                 "Si les droites semblent presque parallèles, on trace la parallèle à la droite qui porte " + v("u") + " passant par l'origine de " + v("d") + ", et on regarde si " + v("d") + " est porté par cette droite."),
    answers=[(100, "Non, car les droites qui portent " + v("u") + " et " + v("d") + " sont sécantes.", "Exact."),
             (0, "Oui, car " + v("u") + " et " + v("d") + " ont presque la même direction.", "« Presque » ne suffit pas : les droites qui les portent doivent être parallèles."),
             (0, "Oui, car " + v("u") + " et " + v("d") + " sont de même sens.", "Le sens ne suffit pas : il faut d'abord la même direction."),
             (0, "Non, car " + v("u") + " et " + v("d") + " n'ont pas la même norme.", "La norme n'intervient pas dans la colinéarité : " + v("c") + " et " + v("u") + " n'ont pas la même norme et sont colinéaires.")],
    hints=["Trace la parallèle à la droite qui porte " + v("u") + " passant par l'origine de " + v("d") + ". Le vecteur " + v("d") + " est-il porté par cette droite ?",
           "Avec les carreaux : " + v("u") + " correspond à 2 vers la droite et 1 vers le haut, " + v("d") + " à 3 vers la droite et 1 vers le haut. Est-ce proportionnel ?"],
    general=correction(
        etape("Étape 1 — On repère la direction de " + v("u") + " et on trace la parallèle passant par l'origine de " + v("d"),
              "On trace la droite qui porte " + v("u") + " (en pointillés orange) et la droite parallèle passant par l'origine de " + v("d") + " (en pointillés verts).<br>Si " + v("d") + " avait la même direction que " + v("u") + ", il serait porté par cette droite verte.", "ex1_q3a"),
        etape("Étape 2 — On trace la droite qui porte " + v("d"),
              "La droite qui porte " + v("d") + " (en pointillés gris) ne se confond pas avec la droite verte : elles se coupent à l'origine de " + v("d") + ".<br>La droite qui porte " + v("d") + " n'est donc pas parallèle à la droite qui porte " + v("u") + " : ces deux droites sont sécantes.<br>Elles se coupent en dehors du quadrillage, mais on voit qu'elles s'écartent l'une de l'autre.", "ex1_q3b"),
        etape("Étape 3 — On conclut",
              "Les vecteurs " + v("u") + " et " + v("d") + " n'ont pas la même direction, même s'ils se ressemblent.<br>Donc <b>" + v("d") + " n'est pas colinéaire à " + v("u") + "</b>."),
        remarque("Le vecteur " + v("u") + " correspond à un déplacement de 2 carreaux vers la droite et 1 carreau vers le haut.<br>Le vecteur " + v("d") + " correspond à un déplacement de 3 carreaux vers la droite et 1 carreau vers le haut.<br>Horizontalement, on multiplie par " + F32 + " ; verticalement, par 1.<br>Ce n'est pas le même nombre : les déplacements ne sont pas proportionnels.")))

# Question 4 : dix coefficients (cloze). Les feedbacks des trous restent en texte simple (accolades interdites dans un cloze).
def sa(bonnes, pieges=()):
    """bonnes : liste de réponses acceptées ; pieges : [(réponse, feedback)] notées 0."""
    parts = ["%s%s#Exact." % ("=" if i == 0 else "%100%", b) for i, b in enumerate(bonnes)]
    parts += ["%%0%%%s#%s" % (p, fb) for p, fb in pieges]
    parts += ["*#Non. Pense au signe (même sens ou sens opposé), puis à la valeur (combien de fois la norme)."]
    return "{1:SHORTANSWER:" + "~".join(parts) + "}"

def neg(x):
    return [x, x.replace("-", "−")]

DEC = "Par convention, le coefficient de colinéarité ne s'écrit pas sous forme décimale : écris la fraction."
COEFS = [  # (vecteur, coefficient affiché, vecteur de référence, réponses acceptées, pièges)
    ("v", "−2", "u", neg("-2"), [("2", "Attention au sens : les vecteurs sont de sens opposé.")]),
    ("c", "2", "u", ["2", "+2"], [("-2", "Attention au sens : les vecteurs sont de même sens.")]),
    ("r", "3", "u", ["3", "+3"], [("-3", "Attention au sens : les vecteurs sont de même sens.")]),
    ("b", "−1", "w", neg("-1") + ["-", "−"], [("1", "Attention au sens : les vecteurs sont de sens opposé.")]),
    ("s", "−2", "w", neg("-2"), [("2", "Attention au sens : les vecteurs sont de sens opposé.")]),
    ("a", "−2", "t", neg("-2"), [("2", "Attention au sens : les vecteurs sont de sens opposé.")]),
    ("s", "2", "b", ["2", "+2"], [("-2", "Attention au sens : les vecteurs sont de même sens.")]),
    ("u", "−1/2", "v", neg("-1/2"), [("-0,5", DEC), ("-0.5", DEC), ("1/2", "Attention au sens : les vecteurs sont de sens opposé."), ("-2", "C'est l'inverse : la norme de u est la moitié de celle de v.")]),
    ("r", "3/2", "c", ["3/2", "+3/2"], [("1,5", DEC), ("1.5", DEC), ("2/3", "C'est l'inverse : la norme de r est plus grande que celle de c.")]),
    ("r", "−3/2", "v", neg("-3/2"), [("-1,5", DEC), ("-1.5", DEC), ("3/2", "Attention au sens : les vecteurs sont de sens opposé.")]),
]
EXPL = {
    0: ("de sens opposé", "La norme de " + v("v") + " est deux fois plus grande que celle de " + v("u") + ".", M(r"\vec{v}=-2\,\vec{u}")),
    1: ("de même sens", "La norme de " + v("c") + " est deux fois plus grande que celle de " + v("u") + ".", M(r"\vec{c}=2\,\vec{u}")),
    2: ("de même sens", "La norme de " + v("r") + " est trois fois plus grande que celle de " + v("u") + ".", M(r"\vec{r}=3\,\vec{u}")),
    3: ("de sens opposé", "La norme de " + v("b") + " est égale à celle de " + v("w") + ".", M(r"\vec{b}=-1\,\vec{w}") + ", que l'on écrit aussi " + M(r"\vec{b}=-\vec{w}")),
    4: ("de sens opposé", "La norme de " + v("s") + " est deux fois plus grande que celle de " + v("w") + ".", M(r"\vec{s}=-2\,\vec{w}")),
    5: ("de sens opposé", "La norme de " + v("a") + " est deux fois plus grande que celle de " + v("t") + ".", M(r"\vec{a}=-2\,\vec{t}")),
    6: ("de même sens", "La norme de " + v("s") + " est deux fois plus grande que celle de " + v("b") + ".", M(r"\vec{s}=2\,\vec{b}")),
    7: ("de sens opposé", "La norme de " + v("u") + " est deux fois plus petite que celle de " + v("v") + " : c'est la moitié.", M(r"\vec{u}=-\dfrac{1}{2}\,\vec{v}")),
    8: ("de même sens", "La norme de " + v("r") + " est une fois et demie celle de " + v("c") + ".<br>On peut se dire " + M(r"\vec{r}=1{,}5\,\vec{c}") + ", mais le coefficient de colinéarité ne s'écrit pas – par convention – sous forme décimale.<br>On sait que " + M(r"1{,}5=\dfrac{3}{2}") + ".", M(r"\vec{r}=\dfrac{3}{2}\,\vec{c}")),
    9: ("de sens opposé", "La norme de " + v("r") + " est une fois et demie celle de " + v("v") + ".<br>On peut se dire " + M(r"\vec{r}=-1{,}5\,\vec{v}") + ", mais le coefficient de colinéarité ne s'écrit pas – par convention – sous forme décimale.<br>On sait que " + M(r"1{,}5=\dfrac{3}{2}") + ".", M(r"\vec{r}=-\dfrac{3}{2}\,\vec{v}")),
}
lignes = "".join("<p>%s = %s %s</p>" % (v(x), sa(ok, pg), v(y)) for x, _, y, ok, pg in COEFS)
expl = "".join('<p style="margin:10px 0 2px;color:#2f9e44;">%s</p><p>Les vecteurs %s et %s ont même direction et sont %s.<br>%s<br>Donc %s.</p>'
               % (M(r"\vec{%s}=%s\,\vec{%s}" % (x, k.replace("−", "-").replace("3/2", r"\dfrac{3}{2}").replace("1/2", r"\dfrac{1}{2}"), y)),
                  v(x), v(y), EXPL[i][0], EXPL[i][1], EXPL[i][2])
               for i, (x, k, y, _, _) in enumerate(COEFS))
add(type="cloze", name="Ex1-Q4 – Coefficients de colinéarité",
    text=INTRO1 + "<p>Compléter avec le coefficient de colinéarité qui convient (écrire par exemple <code>-2</code> ou <code>3/2</code>).</p>" +
         methode("Le coefficient <i>k</i> s'obtient en deux temps :",
                 "⋆ son <i>signe</i> : <i>k</i> est positif si les vecteurs sont de même sens, négatif s'ils sont de sens opposés ;",
                 "⋆ sa <i>valeur</i> : par combien faut-il multiplier la longueur du second vecteur pour obtenir celle du premier ? (on compare les déplacements, ce peut être une fraction).") + lignes,
    hints=["Commence par le signe : les deux vecteurs vont-ils dans le même sens ?",
           "Pour la valeur, compare les normes : deux fois plus grande → 2 ; deux fois plus petite → " + F12 + " ; une fois et demie → " + F32 + "."],
    general=correction('<p style="margin:6px 0">Réponses : ' + " ; ".join("%s = %s %s" % (v(x), k, v(y)) for x, k, y, _, _ in COEFS) + "</p>",
                       '<div style="border-top:1px dashed #2f9e44;margin-top:8px;padding-top:4px;"><p style="color:#3f9a4f;margin:0">Explication</p>' + expl + "</div>"))

# ---------------- Exercice 2 ----------------
add(type="mc", single=False, name="Ex2-Q1 – Vecteurs colinéaires à AB",
    text=INTRO2 + "<p>Parmi les vecteurs " + V("CD") + ", " + V("EF") + ", " + V("GH") + " et " + V("AK") + ", cocher ceux qui sont colinéaires au vecteur " + V("AB") + ".</p>" +
         methode("Deux vecteurs sont colinéaires s'ils ont la <i>même direction</i>.",
                 "On trace la droite (AB), puis les droites qui portent les autres vecteurs : (CD), (EF), (GH) et (AK).",
                 "Un vecteur est colinéaire à " + V("AB") + " lorsque la droite qui le porte est parallèle à la droite (AB), ou confondue avec elle."),
    answers=[(33.33333, V("CD"), "Oui : la droite (CD) est parallèle à la droite (AB)."),
             (33.33333, V("GH"), "Oui : la droite (GH) est parallèle à la droite (AB)."),
             (33.33333, V("AK"), "Oui : le point K est sur la droite (AB), donc les droites (AK) et (AB) sont confondues."),
             (-100, V("EF"), "Non : la droite (EF) est sécante avec la droite (AB).")],
    hints=["Trace la droite (AB) et prolonge-la : passe-t-elle par un des autres points ?",
           "Trois vecteurs sont à cocher. Pour le dernier, la droite qui le porte coupe la droite (AB)."],
    general=correction(
        '<p style="margin:6px 0">Les vecteurs colinéaires à ' + V("AB") + " sont <b>" + V("CD") + ", " + V("GH") + " et " + V("AK") + "</b>.</p>",
        etape(V("CD") + " et " + V("GH"), "Les droites (CD) et (GH) (en pointillés verts) sont parallèles à la droite (AB) (en pointillés orange).<br>Donc " + V("CD") + " et " + V("GH") + " ont même direction que " + V("AB") + " : ils sont colinéaires à " + V("AB") + ".", "ex2_q1a"),
        etape(V("AK") + " et " + V("EF"), "Le point K est sur la droite (AB) : les droites (AK) et (AB) sont confondues, donc " + V("AK") + " est colinéaire à " + V("AB") + ".<br>La droite (EF) (en pointillés gris) est sécante avec la droite (AB) : " + V("EF") + " n'est pas colinéaire à " + V("AB") + ".", "ex2_q1b"),
        remarque("On part du premier point (l'origine) et on compte le déplacement jusqu'au second (l'extrémité).<br>Le vecteur " + V("AB") + " correspond à un déplacement de 3 carreaux vers la droite et 1 carreau vers le haut." +
                 tableau([V("AB"), V("CD"), V("GH"), V("AK"), V("EF")], [3, 6, 9, 9, 3], [1, 2, 3, 3, 2]) +
                 "Les déplacements de " + V("CD") + ", " + V("GH") + " et " + V("AK") + " sont proportionnels à ceux de " + V("AB") + ".<br>Pour " + V("EF") + ", 3 n'est pas le triple de 2 : ses déplacements ne sont pas proportionnels.")))

add(type="cloze", name="Ex2-Q2 – Coefficients par rapport à AB",
    text=INTRO2 + "<p>Pour chaque vecteur colinéaire à " + V("AB") + ", donner le réel <i>k</i> tel que ce vecteur soit égal à <i>k</i> " + V("AB") + ".</p>" +
         methode("Le coefficient <i>k</i> s'obtient en deux temps :",
                 "⋆ son <i>signe</i> : <i>k</i> est positif si le vecteur est de même sens que " + V("AB") + ", négatif s'il est de sens opposé ;",
                 "⋆ sa <i>valeur</i> : combien de fois la norme de " + V("AB") + " faut-il prendre pour obtenir la norme du vecteur ?") +
         "<p>" + V("CD") + " = " + sa(neg("-2"), [("2", "Attention au sens : CD va dans l'autre sens que AB.")]) + " " + V("AB") + "</p>" +
         "<p>" + V("GH") + " = " + sa(neg("-3"), [("3", "Attention au sens : GH va dans l'autre sens que AB.")]) + " " + V("AB") + "</p>" +
         "<p>" + V("AK") + " = " + sa(["3", "+3"], [("-3", "Attention au sens : AK va dans le même sens que AB.")]) + " " + V("AB") + "</p>",
    hints=["Compare d'abord le sens de chaque vecteur avec celui de " + V("AB") + ".",
           "Puis compare les normes : " + V("CD") + " est deux fois plus long que " + V("AB") + "."],
    general=correction(
        '<p style="margin:6px 0">Réponses : ' + V("CD") + " = −2 " + V("AB") + " ; " + V("GH") + " = −3 " + V("AB") + " ; " + V("AK") + " = 3 " + V("AB") + ".</p>" + fig("ex2_q2", 360),
        etape(M(r"\overrightarrow{\mathrm{CD}}=-2\,\overrightarrow{\mathrm{AB}}"), "Les vecteurs " + V("CD") + " et " + V("AB") + " ont même direction et sont de sens opposé.<br>La norme de " + V("CD") + " est deux fois plus grande que celle de " + V("AB") + ".<br>Donc " + M(r"\overrightarrow{\mathrm{CD}}=-2\,\overrightarrow{\mathrm{AB}}") + "."),
        etape(M(r"\overrightarrow{\mathrm{GH}}=-3\,\overrightarrow{\mathrm{AB}}"), "Les vecteurs " + V("GH") + " et " + V("AB") + " ont même direction et sont de sens opposé.<br>La norme de " + V("GH") + " est trois fois plus grande que celle de " + V("AB") + ".<br>Donc " + M(r"\overrightarrow{\mathrm{GH}}=-3\,\overrightarrow{\mathrm{AB}}") + "."),
        etape(M(r"\overrightarrow{\mathrm{AK}}=3\,\overrightarrow{\mathrm{AB}}"), "Les vecteurs " + V("AK") + " et " + V("AB") + " ont même direction et sont de même sens.<br>La norme de " + V("AK") + " est trois fois plus grande que celle de " + V("AB") + ".<br>Donc " + M(r"\overrightarrow{\mathrm{AK}}=3\,\overrightarrow{\mathrm{AB}}") + "."),
        remarque(V("AB") + " correspond à un déplacement de 3 carreaux vers la droite et 1 carreau vers le haut.<br>" +
                 V("CD") + " : 6 carreaux vers la gauche et 2 vers le bas, deux fois plus, dans l'autre sens.<br>" +
                 V("GH") + " : 9 carreaux vers la gauche et 3 vers le bas, trois fois plus, dans l'autre sens.<br>" +
                 V("AK") + " : 9 carreaux vers la droite et 3 vers le haut, trois fois plus, dans le même sens.")))

add(type="cloze", name="Ex2-Q3 – CD et GH",
    text=INTRO2 + "<p>Les vecteurs " + V("CD") + " et " + V("GH") + " sont-ils colinéaires ? Si oui, déterminer le réel <i>k</i> tel que " + V("GH") + " = <i>k</i> " + V("CD") + ".</p>" +
         methode("On regarde si les droites (CD) et (GH) sont parallèles : si oui, les vecteurs ont la même direction et sont colinéaires.",
                 "Pour le coefficient, on donne d'abord son signe (même sens ou sens opposé), puis sa valeur : combien de fois la norme de " + V("CD") + " faut-il prendre pour obtenir celle de " + V("GH") + " ? Ce peut être une fraction.") +
         "<p>Les vecteurs " + V("CD") + " et " + V("GH") + " {1:MULTICHOICE:=sont colinéaires#Exact : les droites (CD) et (GH) sont parallèles.~ne sont pas colinéaires#Les droites (CD) et (GH) sont parallèles : regarde à nouveau.}.</p>" +
         "<p>" + V("GH") + " = " + sa(["3/2", "+3/2"], [("1,5", DEC), ("1.5", DEC), ("-3/2", "Attention au sens : CD et GH vont tous les deux vers la gauche et vers le bas."), ("2/3", "C'est l'inverse : GH est plus long que CD.")]) + " " + V("CD") + "</p>",
    hints=["Prolonge les droites (CD) et (GH) : se coupent-elles ?",
           "La norme de " + V("GH") + " est une fois et demie celle de " + V("CD") + "."],
    general=correction(
        etape("Étape 1 — On compare les droites (CD) et (GH)", "La droite (GH) (en pointillés verts) est parallèle à la droite (CD) (en pointillés orange).<br>Les vecteurs " + V("CD") + " et " + V("GH") + " ont donc la même direction : ils sont colinéaires.", "ex2_q3"),
        etape("Étape 2 — On cherche le coefficient", "Les vecteurs " + V("GH") + " et " + V("CD") + " sont de même sens : le coefficient est positif.<br>La norme de " + V("GH") + " est une fois et demie celle de " + V("CD") + ".<br>On peut se dire " + M(r"\overrightarrow{\mathrm{GH}}=1{,}5\,\overrightarrow{\mathrm{CD}}") + ", mais le coefficient de colinéarité ne s'écrit pas – par convention – sous forme décimale.<br>On sait que " + M(r"1{,}5=\dfrac{3}{2}") + "."),
        etape("Étape 3 — On conclut", "Les vecteurs " + V("CD") + " et " + V("GH") + " sont colinéaires et <b>" + M(r"\overrightarrow{\mathrm{GH}}=\dfrac{3}{2}\,\overrightarrow{\mathrm{CD}}") + "</b>."),
        remarque(V("CD") + " correspond à un déplacement de 6 carreaux vers la gauche et 2 carreaux vers le bas.<br>" + V("GH") + " correspond à un déplacement de 9 carreaux vers la gauche et 3 carreaux vers le bas.<br>Horizontalement : " + M(r"9\div6=\dfrac{3}{2}") + ".<br>Verticalement : " + M(r"3\div2=\dfrac{3}{2}") + ".<br>On retrouve aussi ce résultat avec la question précédente : " + M(r"-3\div(-2)=\dfrac{3}{2}") + ".")))

add(type="cloze", name="Ex2-Q4 – Parallélisme et alignement",
    text=INTRO2 +
         methode("On utilise les propriétés du cours :",
                 "⋆ " + V("AB") + " et " + V("CD") + " colinéaires ⟺ les droites (AB) et (CD) sont parallèles (ou confondues) ;",
                 "⋆ " + V("AB") + " et " + V("AC") + " colinéaires ⟺ les points A, B et C sont alignés.") +
         "<p>On a " + V("CD") + " = −2 " + V("AB") + ". On en déduit que les droites (AB) et (CD) sont {1:MULTICHOICE:=parallèles#Exact : les vecteurs AB et CD sont colinéaires.~sécantes#Les vecteurs AB et CD sont colinéaires : leurs droites ont la même direction.~perpendiculaires#La colinéarité ne dit rien d'un angle droit.}.</p>" +
         "<p>On a " + V("AK") + " = 3 " + V("AB") + ". On en déduit que les points A, B et K {1:MULTICHOICE:=sont alignés#Exact : AB et AK sont colinéaires et ont le point A en commun.~ne sont pas alignés#AB et AK sont colinéaires, avec la même origine A : relis la propriété.}.</p>",
    hints=["Colinéaires = même direction. Que dire de deux droites qui ont la même direction ?",
           "Les vecteurs " + V("AB") + " et " + V("AK") + " ont la même origine A."],
    general=correction(
        fig("ex2_q4", 360),
        etape("Les droites (AB) et (CD)", "On a " + M(r"\overrightarrow{\mathrm{CD}}=-2\,\overrightarrow{\mathrm{AB}}") + ", donc " + V("AB") + " et " + V("CD") + " sont colinéaires.<br>Ainsi, <b>les droites (AB) et (CD) sont parallèles</b>."),
        etape("Les points A, B et K", "On a " + M(r"\overrightarrow{\mathrm{AK}}=3\,\overrightarrow{\mathrm{AB}}") + ", donc " + V("AB") + " et " + V("AK") + " sont colinéaires.<br>Ainsi, <b>les points A, B et K sont alignés</b>.")))

# ============================================================================
# Écriture du fichier Moodle XML
# ============================================================================
def cdata(s):
    return "<![CDATA[" + s.replace("]]>", "]]]]><![CDATA[>") + "]]>"
def esc(s):
    return html.escape(s, quote=False)
FIG_RE = re.compile(r'@@PLUGINFILE@@/(fig_[a-z0-9_]+)\.png')
def files_for(text):
    return "".join('<file name="%s.png" path="/" encoding="base64">%s</file>\n' % (n, b64(n[4:])) for n in sorted(set(FIG_RE.findall(text))))
def xml_text(tag, content):
    return '<%s format="html">\n<text>%s</text>\n%s</%s>\n' % (tag, cdata(content), files_for(content), tag)

def question_xml(q):
    t = q["type"]
    out = '<question type="%s">\n<name><text>%s</text></name>\n' % ({"mc": "multichoice", "cloze": "cloze"}[t], esc(q["name"]))
    out += xml_text("questiontext", q["text"]) + xml_text("generalfeedback", q.get("general", ""))
    out += "<defaultgrade>1</defaultgrade>\n<penalty>0.3333333</penalty>\n<hidden>0</hidden>\n"
    if t == "mc":
        out += "<single>%s</single>\n<shuffleanswers>true</shuffleanswers>\n<answernumbering>none</answernumbering>\n<showstandardinstruction>0</showstandardinstruction>\n" % ("true" if q.get("single", True) else "false")
        out += xml_text("correctfeedback", "Bonne réponse.") + xml_text("partiallycorrectfeedback", "Réponse partiellement correcte.") + xml_text("incorrectfeedback", "Réponse incorrecte.") + "<shownumcorrect/>\n"
        for frac, txt, fb in q["answers"]:
            out += '<answer fraction="%s" format="html">\n<text>%s</text>\n%s</answer>\n' % (frac, cdata(txt), xml_text("feedback", fb))
    out += "".join('<hint format="html">\n<text>%s</text>\n<shownumcorrect/>\n<clearwrong/>\n</hint>\n' % cdata(h) for h in q.get("hints", []))
    return out + "</question>\n"

def write_xml(path):
    out = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'
    out += '<question type="category">\n<category>\n<text>$course$/top/%s</text>\n</category>\n<info format="html">\n<text></text>\n</info>\n<idnumber></idnumber>\n</question>\n' % esc(CAT)
    out += "".join(question_xml(q) for q in Q) + "</quiz>\n"
    with open(path, "w", encoding="utf8") as f:
        f.write(out)

# ============================================================================
# Page « Cours » (à coller dans une ressource Page) et fiche de montage
# ============================================================================
def img_data(name, width):
    return '<p style="text-align:center"><img src="data:image/png;base64,%s" alt="figure" width="%d"></p>' % (b64(name), width)

def cours_html():
  return (
    '<div style="background:rgba(46,160,67,.07);border-left:4px solid #2ea043;padding:10px 16px;margin:0 0 16px;">'
    '<p style="color:#2ea043;margin:0 0 6px;">Définition 7 — <i>Vecteurs colinéaires</i></p>'
    "<p>Deux vecteurs " + v("u") + " et " + v("v") + " sont dits <span style=\"color:#2ea043\">colinéaires</span> s'il existe un réel <i>k</i> tel que " + M(r"\vec{v}=k\,\vec{u}") + " ou " + M(r"\vec{u}=k\,\vec{v}") + ".</p>"
    '<p>Le réel <i>k</i> est appelé <span style="color:#2ea043">coefficient de colinéarité</span>.</p></div>'
    '<div style="background:rgba(85,85,95,.06);border-left:4px solid #55555f;padding:10px 16px;margin:0 0 16px;">'
    '<p style="color:#55555f;margin:0 0 6px;">Exemple</p>' + img_data("cours", 300) +
    "<p>Les droites qui portent " + v("u") + " et " + v("v") + " (en pointillés verts) sont parallèles : " + v("u") + " et " + v("v") + " ont la même direction.<br>On a " + M(r"\vec{v}=-2\,\vec{u}") + ".<br>Donc " + v("u") + " et " + v("v") + " sont colinéaires.<br>Le coefficient de colinéarité est −2.</p>"
    "<p>La droite qui porte " + v("w") + " (en pointillés gris) est sécante avec les deux autres.<br>Donc " + v("w") + " n'est colinéaire ni à " + v("u") + ", ni à " + v("v") + ".</p></div>"
    '<div style="background:rgba(214,144,20,.09);border-left:4px solid #d69014;padding:10px 16px;">'
    '<p style="color:#b07610;margin:0 0 6px;">À noter</p>'
    "<p>⋆ Deux vecteurs sont colinéaires si et seulement s'ils ont <span style=\"color:#b07610\">même direction</span>.</p>"
    "<p>⋆ Le vecteur nul est colinéaire à n'importe quel vecteur.<br>En effet, " + M(r"\vec{0}=0\,\vec{u}") + ".</p>"
    "<p>⋆ La notion de colinéarité est fortement liée à celle de parallélisme et d'alignement.</p></div>")

def page(title, body):
    return ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8"><title>%s</title>\n'
            '<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]]}};</script>\n'
            '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>\n'
            '<style>body{font-family:"Source Sans 3",Arial,sans-serif;max-width:860px;margin:24px auto;padding:0 16px;line-height:1.5;color:#14202b;background:#fff}'
            'h1,h2{font-weight:500}code{background:#f1f3f5;padding:1px 4px}</style></head><body>\n<h1>%s</h1>\n%s\n</body></html>\n') % (title, title, body)

FICHE = """
<p>Ce dossier contient la version Éléa de la page <i>Exemples colinéarité.html</i> : le même cours, les mêmes exercices (vecteurs et points identiques à la feuille <i>Exemples colinéarité.pdf</i>), avec pour chaque question un <b>point méthode</b> affiché sous la consigne, deux <b>indices</b> successifs en cas d'erreur, puis une <b>correction par étapes</b> où les droites sont tracées sur la figure.</p>

<h2>1. Importer la banque de questions (5 min)</h2>
<p>Dans le parcours Éléa : <b>Plus → Banque de questions → Importer</b>. Format : <b>Moodle XML</b>. Fichier : <code>Exemples colinéarité - Éléa - Banque de questions.xml</code>. Laisser « Obtenir la catégorie du fichier » coché.</p>
<p>Les questions arrivent dans la catégorie <b>Séquence 2 – Vecteurs › Exemples colinéarité</b> (9 questions). Les figures sont incluses dans le fichier ; les formules s'affichent grâce au filtre MathJax d'Éléa.</p>

<h2>2. Ajouter le cours (2 min)</h2>
<p>Ajouter une activité <b>Page</b> nommée « Cours – Vecteurs colinéaires ». Ouvrir <code>Exemples colinéarité - Éléa - Cours.html</code> dans un navigateur, tout sélectionner, copier et coller dans le contenu de la Page (ou coller le code source avec le bouton « &lt;/&gt; » de l'éditeur).</p>

<h2>3. Créer le test (5 min)</h2>
<p>Ajouter une activité <b>Test</b> nommée « Exemples colinéarité », puis dans les paramètres :</p>
<ul>
<li><b>Comportement des questions</b> : « Interactif avec essais multiples » (c'est ce qui affiche les indices après une erreur) ;</li>
<li><b>Mise en page</b> : une question par page, navigation libre ;</li>
<li><b>Options de relecture</b> : cocher « Feedback spécifique », « Feedback général » et « Réponse juste », pendant et après la tentative (le feedback général contient la correction par étapes) ;</li>
<li><b>Questions</b> : ne pas mélanger, pour garder l'ordre de la feuille ;</li>
<li><b>Nombre de tentatives</b> : illimité ; <b>méthode de notation</b> : note la plus haute.</li>
</ul>
<p>Dans <b>Questions → Ajouter → depuis la banque de questions</b>, choisir la catégorie <i>Exemples colinéarité</i> et ajouter les 9 questions dans l'ordre : Ex1-Q1, Ex1-Q2a, Ex1-Q2b, Ex1-Q3, Ex1-Q4, puis Ex2-Q1 à Ex2-Q4.</p>
<p>Restriction d'accès conseillée sur le test : « Achèvement d'activité : la Page Cours doit être consultée ».</p>

<h2>4. Ce que voit l'élève</h2>
<ul>
<li>la consigne et la figure, puis le point méthode (encadré jaune) ;</li>
<li>après une mauvaise réponse : un indice, puis un second indice plus précis ;</li>
<li>une fois la question terminée : la correction (encadré vert) avec les droites tracées, et la remarque « Vérifier avec les carreaux ».</li>
</ul>
<p>Saisie des coefficients (Ex1-Q4, Ex2-Q2, Ex2-Q3) : les élèves écrivent par exemple <code>-2</code> ou <code>3/2</code>. Une écriture décimale (<code>1,5</code>) est refusée avec un message rappelant la convention.</p>

<h2>Variante H5P (sans import de banque de questions)</h2>
<p>Le fichier <code>Exemples colinéarité.h5p</code> contient tout dans une seule activité (présentation H5P de 36 diapositives) : le cours, puis pour chaque question une diapositive « question » (figure + point méthode + question interactive), suivie des diapositives de correction étape par étape, avec les droites tracées. Passer à la diapositive suivante = « étape suivante ». Une diapositive bilan donne le score à la fin.</p>
<ol>
<li>Activer le <b>mode édition</b>, puis <b>Ajouter une activité ou ressource → H5P</b>.</li>
<li>Donner un nom (« Exemples colinéarité »), puis glisser <code>Exemples colinéarité.h5p</code> dans la zone « Fichier du paquet ».</li>
<li>Enregistrer et afficher.</li>
</ol>
<p>Saisie des coefficients entiers : <code>-2</code>, <code>3</code>… Les coefficients fractionnaires sont proposés en choix (H5P ne permet pas de taper une fraction).</p>
<p>Le paquet est régénéré par <code>build_h5p_colinearite.py</code> (même dossier).</p>

<h2>Modifier le contenu</h2>
<p>Tout est généré par <code>build_elea_colinearite.py</code> (même dossier) : modifier le texte dans ce fichier puis lancer <code>python3 build_elea_colinearite.py</code> pour régénérer les trois fichiers, puis réimporter le XML.</p>
"""

if __name__ == "__main__":
    build_figures()
    write_xml(os.path.join(HERE, BASE + "Banque de questions.xml"))
    with open(os.path.join(HERE, BASE + "Cours.html"), "w", encoding="utf8") as f:
        f.write(page("Vecteurs colinéaires", cours_html()))
    with open(os.path.join(HERE, BASE + "Fiche de montage.html"), "w", encoding="utf8") as f:
        f.write(page("Exemples colinéarité – Éléa – Fiche de montage", FICHE))
    print("OK :", len(Q), "questions,", len(FIGS), "figures")
