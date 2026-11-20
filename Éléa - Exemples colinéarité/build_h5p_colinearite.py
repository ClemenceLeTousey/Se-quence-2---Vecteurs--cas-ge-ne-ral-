# -*- coding: utf-8 -*-
"""
Version H5P (« Course Presentation ») de la page « Exemples colinéarité.html » :
  Exemples colinéarité.h5p  → à déposer dans une activité H5P d'Éléa.
Même principe que la page HTML :
  - une diapositive par question : figure + point méthode à gauche, question à droite ;
  - puis une diapositive par étape de correction (droites tracées sur la figure) :
    passer à la diapositive suivante = « étape suivante ».
Les textes avec des vecteurs (méthode, corrections) sont mis en image par LaTeX pour
que les flèches s'affichent partout ; les questions interactives sont écrites en toutes lettres
(« le vecteur u »).
Les bibliothèques H5P sont reprises du paquet officiel du Hub (H5P.CoursePresentation) :
  dossier « h5p-libs » (téléchargé si absent).
Usage : python3 build_h5p_colinearite.py
"""
import os, json, uuid, zipfile, subprocess, shutil, urllib.request, struct
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Exemples colinéarité.h5p")
IMG = os.path.join(HERE, "figures_h5p")
LIBS = os.path.join(HERE, "h5p-libs")

spec = importlib.util.spec_from_file_location("elea", os.path.join(HERE, "build_elea_colinearite.py"))
elea = importlib.util.module_from_spec(spec); spec.loader.exec_module(elea)

# ============================================================================
# Bibliothèques H5P (Hub)
# ============================================================================
def ensure_libs():
    if os.path.isdir(LIBS) and os.path.exists(os.path.join(LIBS, "H5P.CoursePresentation-1.26", "library.json")):
        return
    os.makedirs(LIBS, exist_ok=True)
    tmp = os.path.join(LIBS, "_hub.h5p")
    subprocess.run(["curl", "-sL", "-o", tmp, "https://api.h5p.org/v1/content-types/H5P.CoursePresentation"], check=True)
    with zipfile.ZipFile(tmp) as z:
        for n in z.namelist():
            if n.startswith("content/") or n == "h5p.json":
                continue
            z.extract(n, LIBS)
    os.remove(tmp)

def lib_dir(machine):
    return [d for d in os.listdir(LIBS) if d.split("-")[0] == machine][0]

def lib_version(machine):
    j = json.load(open(os.path.join(LIBS, lib_dir(machine), "library.json"), encoding="utf8"))
    return "%s %d.%d" % (machine, j["majorVersion"], j["minorVersion"]), j

def defaults(machine):
    """Paramètres par défaut d'une bibliothèque, avec les libellés français (language/fr.json)."""
    d = os.path.join(LIBS, lib_dir(machine))
    sem = json.load(open(os.path.join(d, "semantics.json"), encoding="utf8"))
    frp = os.path.join(d, "language", "fr.json")
    fr = json.load(open(frp, encoding="utf8"))["semantics"] if os.path.exists(frp) else []
    def walk(fields, trs):
        out = {}
        for i, f in enumerate(fields):
            tr = trs[i] if i < len(trs) and isinstance(trs[i], dict) else {}
            val = value(f, tr)
            if val is not None:
                out[f["name"]] = val
        return out
    def value(f, tr):
        t = f.get("type")
        if t == "group":
            sub = walk(f.get("fields", []), tr.get("fields", []))
            return sub
        if t in ("text", "number", "boolean", "select"):
            if "default" in tr:
                return tr["default"]
            return f.get("default")
        return None
    return walk(sem, fr)

def merge(a, b):
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            merge(a[k], v)
        else:
            a[k] = v
    return a

# ============================================================================
# Images LaTeX (figures + textes avec vecteurs)
# ============================================================================
PRE = elea.PREAMBLE.replace(r"\begin{tikzpicture}[x=0.5cm,y=0.5cm]", "")
PRE = PRE.replace(r"\begin{document}", r"\usepackage{array}" "\n" r"\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}" "\n"
                  r"\newcommand{\V}[1]{\overrightarrow{\mathrm{#1}}}" "\n" r"\begin{document}")
IMAGES = {}

def tikz(body, scale=1):
    return r"\begin{tikzpicture}[x=%scm,y=%scm]" % (0.5 * scale, 0.5 * scale) + "\n" + body.replace("step=0.5cm", "step=%scm" % (0.5 * scale)) + r"\end{tikzpicture}"

def latex_img(name, body, width=16):
    IMAGES[name] = PRE + r"\begin{minipage}{%scm}" % width + body + r"\end{minipage}" + "\n\\end{document}\n"
    return name

def text_box(name, title, color, paras, width=8.2):
    """Encadré coloré (méthode, étape de correction…) mis en image."""
    t = r"\colorbox{%s!8}{\begin{minipage}{%scm}\vspace{4pt}{\color{%s}\large %s}\par %s\vspace{4pt}\end{minipage}}" % (
        color, width, color, title, r"\par ".join(paras))
    return latex_img(name, r"\large " + t, width + 0.3)

def step_img(name, title, paras, figbody=None, color="vert", stacked=None):
    """Diapositive de correction. stacked=True : figure au-dessus du texte (figures larges de l'exercice 1)."""
    head = r"{\color{%s}\Large %s}\par\vspace{4pt}" % (color, title)
    if figbody is None:
        return latex_img(name, r"\large " + head + r"\par ".join(paras), 16)
    if stacked is None:
        stacked = "x=0.46cm" in figbody  # figures de l'exercice 1
    if stacked:
        body = r"\large " + head + r"{\centering " + figbody + r"\par}\vspace{4pt}" + r"\par ".join(paras)
        return latex_img(name, body, 16)
    body = (r"\large \begin{minipage}[c]{9.4cm}\centering " + figbody + r"\end{minipage}\hspace{0.5cm}"
            r"\begin{minipage}[c]{7.1cm}" + head + r"\par ".join(paras) + r"\end{minipage}")
    return latex_img(name, body, 17)

def build_images():
    os.makedirs(IMG, exist_ok=True)
    for name, src in IMAGES.items():
        tex = os.path.join(IMG, name + ".tex")
        png = tex[:-4] + ".png"
        if os.path.exists(png) and os.path.exists(tex) and open(tex, encoding="utf8").read() == src:
            continue
        open(tex, "w", encoding="utf8").write(src)
        r = subprocess.run(["pdflatex", "-interaction=batchmode", "-halt-on-error", "-output-directory", IMG, tex], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("pdflatex a échoué pour " + name + "\n" + open(tex[:-4] + ".log", errors="ignore").read()[-1200:])
        subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", "-r150", "-dTextAlphaBits=4",
                        "-dGraphicsAlphaBits=4", "-sOutputFile=" + png, tex[:-4] + ".pdf"], check=True)
    for f in os.listdir(IMG):
        if f.endswith((".aux", ".log")):
            os.remove(os.path.join(IMG, f))

def png_size(name):
    with open(os.path.join(IMG, name + ".png"), "rb") as f:
        f.read(16)
        return struct.unpack(">II", f.read(8))

# ============================================================================
# Éléments de diapositive
# ============================================================================
def sid():
    return str(uuid.uuid4())

def element(x, y, w, h, library, params, title, **extra):
    e = {"x": x, "y": y, "width": w, "height": h,
         "action": {"library": library, "params": params, "subContentId": sid(),
                    "metadata": {"contentType": library.split(" ")[0].split(".")[-1], "license": "U", "title": title}},
         "alwaysDisplayComments": False, "backgroundOpacity": 0, "displayAsButton": False,
         "buttonSize": "big", "goToSlideType": "specified", "invisible": False, "solution": ""}
    e.update(extra)
    return e

def image_el(name, x, y, wmax, hmax, alt="figure"):
    """Image placée dans un cadre (en % de la diapositive 16:9) ; proportions résolues à l'assemblage."""
    return {"_img": (name, x, y, wmax, hmax, alt)}

def resolve(e):
    if "_img" not in e:
        return e
    name, x, y, wmax, hmax, alt = e["_img"]
    iw, ih = png_size(name)
    a = iw / ih
    w = wmax
    h = w * (16 / 9) / a
    if h > hmax:
        h = hmax
        w = h * a * 9 / 16
    p = {"contentName": "Image", "decorative": False, "alt": alt,
         "file": {"path": "images/%s.png" % name, "mime": "image/png", "copyright": {"license": "U"}, "width": iw, "height": ih}}
    return element(x + (wmax - w) / 2, y, w, h, lib_version("H5P.Image")[0], p, alt)

def title_el(text):
    return element(1, 0.5, 98, 9, lib_version("H5P.AdvancedText")[0],
                   {"text": '<p style="text-align:center;"><span style="font-size:1.25em;">%s</span></p>' % text}, text)

def multichoice(question, answers, single=False):
    p = defaults("H5P.MultiChoice")
    merge(p, {"question": "<p>%s</p>" % question,
              "answers": [{"text": "<div>%s</div>" % t, "correct": ok,
                           "tipsAndFeedback": {"tip": "", "chosenFeedback": "<div>%s</div>" % fb, "notChosenFeedback": ""}}
                          for t, ok, fb in answers],
              "behaviour": {"enableRetry": True, "enableSolutionsButton": True, "enableCheckButton": True,
                            "type": "single" if single else "multi", "singlePoint": False, "randomAnswers": True,
                            "showSolutionsRequiresInput": True, "confirmCheckDialog": False, "confirmRetryDialog": False,
                            "autoCheck": False, "passPercentage": 100, "showScorePoints": True}})
    p.pop("media", None)
    return lib_version("H5P.MultiChoice")[0], p

def mark_words(task, words):
    """words : [(lettre, correcte)] → l'élève clique sur les lettres des vecteurs colinéaires."""
    p = defaults("H5P.MarkTheWords")
    merge(p, {"taskDescription": "<p>%s</p>" % task,
              "textField": "<p>" + " &nbsp; ".join(("*%s*" % w) if ok else w for w, ok in words) + "</p>",
              "behaviour": {"enableRetry": True, "enableSolutionsButton": True, "enableCheckButton": True, "showScorePoints": True}})
    p.pop("media", None)
    return lib_version("H5P.MarkTheWords")[0], p

def blanks(intro, lines):
    p = defaults("H5P.Blanks")
    merge(p, {"text": "<p>%s</p>" % intro, "questions": ["<p>%s</p>" % l for l in lines],
              "behaviour": {"enableRetry": True, "enableSolutionsButton": True, "enableCheckButton": True,
                            "autoCheck": False, "caseSensitive": False, "showSolutionsRequiresInput": True,
                            "separateLines": False, "confirmCheckDialog": False, "confirmRetryDialog": False,
                            "acceptSpellingErrors": False}})
    p.pop("media", None)
    return lib_version("H5P.Blanks")[0], p

def single_choice_set(items):
    """items : [(question, [bonne réponse, autres…])] — la première réponse est la bonne."""
    p = defaults("H5P.SingleChoiceSet")
    p["choices"] = [{"subContentId": sid(), "question": "<p>%s</p>" % q, "answers": ["<p>%s</p>" % a for a in ans]} for q, ans in items]
    merge(p, {"behaviour": {"autoContinue": False, "enableRetry": True, "enableSolutionsButton": True, "passPercentage": 100}})
    return lib_version("H5P.SingleChoiceSet")[0], p

ensure_libs()
SLIDES = []
def slide(keyword, elements):
    SLIDES.append({"elements": elements, "slideBackgroundSelector": {}, "keywords": [{"main": keyword}]})

def question_slide(keyword, titre, fig_name, meth_name, lib_params, qtitle):
    lib, params = lib_params
    slide(keyword, [title_el(titre),
                    image_el(fig_name, 1, 11, 48, 42),
                    image_el(meth_name, 1, 55, 48, 44, "Point méthode"),
                    element(51, 11, 48, 87, lib, params, qtitle)])

def step_slide(keyword, titre, img_name):
    slide(keyword, [title_el(titre), image_el(img_name, 1, 11, 98, 88, titre)])

# ============================================================================
# Contenu (mêmes exercices que la page HTML et la feuille PDF)
# ============================================================================
F = elea.FIGS
fig_ex1 = latex_img("fig_ex1", r"\centering " + tikz(F["ex1"]), 11.6)
fig_ex2 = latex_img("fig_ex2", r"\centering " + tikz(F["ex2"]), 7.8)
def fstep(key):
    return tikz(F[key], 0.92 if key.startswith("ex1") else 1.25)

def tableau(cols, h, v):
    n = len(cols)
    return (r"{\normalsize\begin{tabular}{l|%s}" % ("c" * n) + " & " + " & ".join(cols) + r"\\\hline " +
            "Horizontal (carreaux) & " + " & ".join(map(str, h)) + r"\\ " +
            "Vertical (carreaux) & " + " & ".join(map(str, v)) + r"\end{tabular}}")

u, vv = r"$\vec{u}$", r"$\vec{v}$"
def vec(x):
    return r"$\vec{%s}$" % x
def VV(x):
    return r"$\V{%s}$" % x

# ---------- Cours ----------
cours = latex_img("cours", r"\large " +
    r"\colorbox{vert!8}{\begin{minipage}{15.5cm}\vspace{4pt}{\color{vert}Définition 7 — \textit{Vecteurs colinéaires}}\par "
    r"Deux vecteurs $\vec{u}$ et $\vec{v}$ sont dits {\color{vert}colinéaires} s'il existe un réel $k$ tel que $\vec{v}=k\,\vec{u}$ ou $\vec{u}=k\,\vec{v}$.\par "
    r"Le réel $k$ est appelé {\color{vert}coefficient de colinéarité}.\vspace{4pt}\end{minipage}}\par\vspace{8pt}"
    r"\colorbox{gray!10}{\begin{minipage}{15.5cm}\vspace{4pt}{\color{gris}Exemple}\par "
    r"\begin{minipage}[c]{6.6cm}" + elea.fig_cours().replace(r"\begin{scope}[x=0.8cm,y=0.8cm]", r"\begin{tikzpicture}[x=0.8cm,y=0.8cm]").replace(r"\end{scope}" + "\n", "", 0)
    .rsplit(r"\end{scope}", 1)[0] + r"\end{tikzpicture}\end{minipage}\hspace{0.4cm}"
    r"\begin{minipage}[c]{8.4cm}Les droites qui portent $\vec{u}$ et $\vec{v}$ (pointillés verts) sont parallèles : $\vec{u}$ et $\vec{v}$ ont la même direction.\\ "
    r"On a $\vec{v}=-2\,\vec{u}$. Donc $\vec{u}$ et $\vec{v}$ sont colinéaires.\\ Le coefficient de colinéarité est $-2$.\par "
    r"La droite qui porte $\vec{w}$ (pointillés gris) est sécante avec les deux autres.\\ Donc $\vec{w}$ n'est colinéaire ni à $\vec{u}$, ni à $\vec{v}$.\end{minipage}\vspace{4pt}\end{minipage}}")
noter = latex_img("noter", r"\large \colorbox{orange!8}{\begin{minipage}{15.5cm}\vspace{4pt}{\color{orange}À noter}\par "
    r"$\star$ Deux vecteurs sont colinéaires si et seulement s'ils ont {\color{orange}même direction}.\par "
    r"$\star$ Le vecteur nul est colinéaire à n'importe quel vecteur. En effet, $\vec{0}=0\,\vec{u}$.\par "
    r"$\star$ La notion de colinéarité est fortement liée à celle de parallélisme et d'alignement.\vspace{4pt}\end{minipage}}")
slide("Cours", [title_el("Cours — Vecteurs colinéaires"), image_el(cours, 1, 11, 98, 88, "Définition 7 et exemple")])
slide("À noter", [title_el("Cours — À noter"), image_el(noter, 5, 25, 90, 60, "À noter")])

# ---------- Exercice 1, question 1 ----------
E1 = "Exercice 1 — "
m = text_box("m_e1q1", "Point méthode", "orange", [
    r"Deux vecteurs sont colinéaires s'ils ont la \textit{même direction}.",
    r"On imagine la droite qui porte chaque vecteur : deux vecteurs ont la même direction lorsque ces droites sont parallèles (ou confondues). Le sens et la longueur n'ont pas d'importance.",
    r"En pratique, il est possible de lire les déplacements avec les carreaux et de regarder s'ils sont proportionnels à ceux de $\vec{u}$."])
question_slide("Ex1 – Q1", E1 + "Question 1", fig_ex1, m, mark_words(
    "Cliquer sur <strong>toutes</strong> les lettres des vecteurs colinéaires au vecteur u, puis sur « Vérifier ».",
    [("v", True), ("w", False), ("c", True), ("t", False), ("d", False), ("r", True), ("s", False), ("b", False), ("a", False)]), "Question 1")
step_slide("Ex1 – Q1 étape 1", E1 + "Correction de la question 1", step_img("s_e1q1_1", r"Étape 1 — On repère la direction de $\vec{u}$",
    [r"On trace la droite qui porte le vecteur $\vec{u}$ (en pointillés orange)."], fstep("ex1_q1a")))
step_slide("Ex1 – Q1 étape 2", E1 + "Correction de la question 1", step_img("s_e1q1_2", r"Étape 2 — On cherche les vecteurs qui ont cette direction",
    [r"Seules les droites qui portent $\vec{v}$, $\vec{c}$ et $\vec{r}$ (en pointillés verts) sont parallèles à celle de $\vec{u}$.",
     r"Les droites qui portent les autres vecteurs sont sécantes avec la droite qui porte $\vec{u}$."], fstep("ex1_q1b")))
step_slide("Ex1 – Q1 étape 3", E1 + "Correction de la question 1", step_img("s_e1q1_3", r"Étape 3 — On conclut",
    [r"Les vecteurs $\vec{v}$, $\vec{c}$ et $\vec{r}$ ont la même direction que $\vec{u}$.",
     r"Le sens et la longueur ne comptent pas : $\vec{v}$ est de sens opposé, mais il a bien la même direction.",
     r"Les vecteurs colinéaires à $\vec{u}$ sont donc {\color{red!70!black}$\vec{v}$, $\vec{c}$ et $\vec{r}$}."], fstep("ex1_q1b")))
step_slide("Ex1 – Q1 remarque", E1 + "Correction de la question 1", step_img("s_e1q1_4", r"Remarque — Vérifier avec les carreaux",
    [r"Le vecteur $\vec{u}$ correspond à un déplacement de 2 carreaux vers la droite et 1 carreau vers le haut : le déplacement vertical est la moitié du déplacement horizontal.",
     tableau([u, vv, vec("c"), vec("r")], [2, 4, 4, 6], [1, 2, 2, 3]),
     r"C'est un tableau de proportionnalité.\\ À l'inverse, $\vec{w}$ correspond à un déplacement de 3 carreaux vers la droite et 2 vers le bas : 2 n'est pas la moitié de 3."], color="gris"))

# ---------- Exercice 1, question 2 ----------
m2 = text_box("m_e1q2", "Point méthode", "orange", [
    r"Même démarche qu'à la question 1.",
    r"On imagine la droite qui porte le vecteur de référence, puis on cherche les vecteurs portés par une droite parallèle à celle-ci (ou par la même droite).",
    r"Attention, le sens n'a pas d'importance : un vecteur de sens opposé a la même direction."])
question_slide("Ex1 – Q2 (w)", E1 + "Question 2 — le vecteur w", fig_ex1, m2, mark_words(
    "Cliquer sur <strong>toutes</strong> les lettres des vecteurs colinéaires au vecteur w, puis sur « Vérifier ».",
    [("u", False), ("v", False), ("b", True), ("c", False), ("t", False), ("s", True), ("r", False), ("a", False), ("d", False)]), "Question 2 (w)")
step_slide("Ex1 – Q2 (w) étape 1", E1 + "Correction de la question 2 — le vecteur w", step_img("s_e1q2w_1", r"Étape 1 — On repère la direction de $\vec{w}$",
    [r"On trace la droite qui porte le vecteur $\vec{w}$ (en pointillés orange)."], fstep("ex1_q2wa")))
step_slide("Ex1 – Q2 (w) étape 2", E1 + "Correction de la question 2 — le vecteur w", step_img("s_e1q2w_2", r"Étape 2 — On cherche les vecteurs qui ont cette direction",
    [r"Les droites qui portent $\vec{b}$ et $\vec{s}$ (en pointillés verts) sont parallèles à la droite qui porte $\vec{w}$.",
     r"Les droites qui portent les autres vecteurs sont sécantes avec la droite qui porte $\vec{w}$."], fstep("ex1_q2wb")))
step_slide("Ex1 – Q2 (w) étape 3", E1 + "Correction de la question 2 — le vecteur w", step_img("s_e1q2w_3", r"Étape 3 — On conclut",
    [r"Les vecteurs $\vec{b}$ et $\vec{s}$ ont la même direction que $\vec{w}$, même s'ils sont de sens opposé.",
     r"Les vecteurs colinéaires à $\vec{w}$ sont donc {\color{red!70!black}$\vec{b}$ et $\vec{s}$}.",
     r"{\color{gris}Avec les carreaux :} " + tableau([vec("w"), vec("b"), vec("s")], [3, 3, 6], [2, 2, 4])], fstep("ex1_q2wb")))
question_slide("Ex1 – Q2 (t)", E1 + "Question 2 — le vecteur t", fig_ex1, m2, multichoice(
    "Quel vecteur est colinéaire au vecteur t ?",
    [("le vecteur a", True, "Exact : la droite qui porte a est parallèle à celle de t (sens opposé).")] +
    [("le vecteur " + n, False, "Non : la droite qui porte %s est sécante avec celle de t." % n) for n in "udrs"], single=True), "Question 2 (t)")
step_slide("Ex1 – Q2 (t) étape 1", E1 + "Correction de la question 2 — le vecteur t", step_img("s_e1q2t_1", r"Étape 1 — On repère la direction de $\vec{t}$",
    [r"On trace la droite qui porte le vecteur $\vec{t}$ (en pointillés orange)."], fstep("ex1_q2ta")))
step_slide("Ex1 – Q2 (t) étape 2", E1 + "Correction de la question 2 — le vecteur t", step_img("s_e1q2t_2", r"Étape 2 — On cherche le vecteur qui a cette direction",
    [r"Seule la droite qui porte $\vec{a}$ (en pointillés verts) est parallèle à la droite qui porte $\vec{t}$.",
     r"Les droites qui portent les autres vecteurs sont sécantes avec la droite qui porte $\vec{t}$."], fstep("ex1_q2tb")))
step_slide("Ex1 – Q2 (t) étape 3", E1 + "Correction de la question 2 — le vecteur t", step_img("s_e1q2t_3", r"Étape 3 — On conclut",
    [r"Le vecteur $\vec{a}$ a la même direction que $\vec{t}$, même s'il est de sens opposé.",
     r"Le vecteur colinéaire à $\vec{t}$ est donc {\color{red!70!black}$\vec{a}$}.",
     r"{\color{gris}Avec les carreaux :} " + tableau([vec("t"), vec("a")], [1, 2], [2, 4])], fstep("ex1_q2tb")))

# ---------- Exercice 1, question 3 ----------
m3 = text_box("m_e1q3", "Point méthode", "orange", [
    r"Pour montrer que deux vecteurs \textit{ne sont pas} colinéaires, on montre qu'ils n'ont pas la même direction.",
    r"Si les droites qui portent $\vec{u}$ et $\vec{d}$ sont sécantes, les vecteurs ne sont pas colinéaires.",
    r"Si elles semblent presque parallèles, on trace la parallèle à la droite de $\vec{u}$ passant par l'origine de $\vec{d}$."])
question_slide("Ex1 – Q3", E1 + "Question 3", fig_ex1, m3, multichoice(
    "Le vecteur d est-il colinéaire au vecteur u ? Choisir la bonne réponse et la bonne justification.",
    [("Non, car les droites qui portent u et d sont sécantes.", True, "Exact."),
     ("Oui, car u et d ont presque la même direction.", False, "« Presque » ne suffit pas : les droites qui les portent doivent être parallèles."),
     ("Oui, car u et d sont de même sens.", False, "Le sens ne suffit pas : il faut d'abord la même direction."),
     ("Non, car u et d n'ont pas la même norme.", False, "La norme n'intervient pas : c et u n'ont pas la même norme et sont colinéaires.")], single=True), "Question 3")
step_slide("Ex1 – Q3 étape 1", E1 + "Correction de la question 3", step_img("s_e1q3_1", r"Étape 1 — La parallèle passant par l'origine de $\vec{d}$",
    [r"On trace la droite qui porte $\vec{u}$ (en orange) et la droite parallèle passant par l'origine de $\vec{d}$ (en vert).",
     r"Si $\vec{d}$ avait la même direction que $\vec{u}$, il serait porté par cette droite verte."], fstep("ex1_q3a")))
step_slide("Ex1 – Q3 étape 2", E1 + "Correction de la question 3", step_img("s_e1q3_2", r"Étape 2 — La droite qui porte $\vec{d}$",
    [r"La droite qui porte $\vec{d}$ (en gris) ne se confond pas avec la droite verte : elles se coupent à l'origine de $\vec{d}$.",
     r"La droite qui porte $\vec{d}$ n'est donc pas parallèle à celle de $\vec{u}$ : ces deux droites sont sécantes.",
     r"Elles se coupent en dehors du quadrillage, mais on voit qu'elles s'écartent."], fstep("ex1_q3b")))
step_slide("Ex1 – Q3 étape 3", E1 + "Correction de la question 3", step_img("s_e1q3_3", r"Étape 3 — On conclut",
    [r"Les vecteurs $\vec{u}$ et $\vec{d}$ n'ont pas la même direction, même s'ils se ressemblent.",
     r"Donc {\color{red!70!black}$\vec{d}$ n'est pas colinéaire à $\vec{u}$}.",
     r"{\color{gris}Avec les carreaux :} $\vec{u}$ : 2 vers la droite, 1 vers le haut ; $\vec{d}$ : 3 vers la droite, 1 vers le haut. Horizontalement on multiplie par $\dfrac32$, verticalement par 1 : ce n'est pas proportionnel."], fstep("ex1_q3b")))

# ---------- Exercice 1, question 4 ----------
m4 = text_box("m_e1q4", "Point méthode", "orange", [
    r"Le coefficient $k$ s'obtient en deux temps :",
    r"$\star$ son \textit{signe} : $k$ est positif si les vecteurs sont de même sens, négatif s'ils sont de sens opposés ;",
    r"$\star$ sa \textit{valeur} : par combien faut-il multiplier la norme du second vecteur pour obtenir celle du premier ? (ce peut être une fraction)."])
def ent(x):
    return "*%s/%s*" % (x, x.replace("-", "−")) if x.startswith("-") else "*%s/+%s*" % (x, x)
question_slide("Ex1 – Q4 (a)", E1 + "Question 4 — coefficients entiers", fig_ex1, m4, blanks(
    "Compléter avec le coefficient de colinéarité (écrire par exemple -2).",
    ["Le vecteur v est égal à %s fois le vecteur u." % ent("-2"),
     "Le vecteur c est égal à %s fois le vecteur u." % ent("2"),
     "Le vecteur r est égal à %s fois le vecteur u." % ent("3"),
     "Le vecteur b est égal à %s fois le vecteur w." % ent("-1"),
     "Le vecteur s est égal à %s fois le vecteur w." % ent("-2"),
     "Le vecteur a est égal à %s fois le vecteur t." % ent("-2"),
     "Le vecteur s est égal à %s fois le vecteur b." % ent("2")]), "Question 4 (a)")
question_slide("Ex1 – Q4 (b)", E1 + "Question 4 — coefficients fractionnaires", fig_ex1, m4, single_choice_set([
    ("Le vecteur u est égal à … fois le vecteur v.", ["−1/2", "1/2", "−2", "−0,5"]),
    ("Le vecteur r est égal à … fois le vecteur c.", ["3/2", "2/3", "−3/2", "1,5"]),
    ("Le vecteur r est égal à … fois le vecteur v.", ["−3/2", "3/2", "−2/3", "−1,5"])]), "Question 4 (b)")
rep = latex_img("rep_e1q4", r"\large \begin{minipage}{15.5cm}{\color{vert}\Large Réponses}\par\vspace{6pt}"
    r"\renewcommand{\arraystretch}{1.6}\begin{tabular}{lllll}"
    r"$\vec{v}=-2\,\vec{u}$ & $\vec{c}=2\,\vec{u}$ & $\vec{r}=3\,\vec{u}$ & $\vec{b}=-1\,\vec{w}$ & $\vec{s}=-2\,\vec{w}$\\"
    r"$\vec{a}=-2\,\vec{t}$ & $\vec{s}=2\,\vec{b}$ & $\vec{u}=-\dfrac12\,\vec{v}$ & $\vec{r}=\dfrac32\,\vec{c}$ & $\vec{r}=-\dfrac32\,\vec{v}$\end{tabular}"
    r"\par\vspace{8pt}{\color{gris}Rappel : par convention, le coefficient de colinéarité ne s'écrit pas sous forme décimale ($\dfrac32$ et non 1,5).}\end{minipage}")
slide("Ex1 – Q4 réponses", [title_el(E1 + "Correction de la question 4"), image_el(rep, 1, 14, 98, 60, "Réponses")])
EXPL = [("v", "-2", "u", "de sens opposé", r"La norme de $\vec{v}$ est deux fois plus grande que celle de $\vec{u}$."),
        ("c", "2", "u", "de même sens", r"La norme de $\vec{c}$ est deux fois plus grande que celle de $\vec{u}$."),
        ("r", "3", "u", "de même sens", r"La norme de $\vec{r}$ est trois fois plus grande que celle de $\vec{u}$."),
        ("b", "-1", "w", "de sens opposé", r"La norme de $\vec{b}$ est égale à celle de $\vec{w}$ (on écrit aussi $\vec{b}=-\vec{w}$)."),
        ("s", "-2", "w", "de sens opposé", r"La norme de $\vec{s}$ est deux fois plus grande que celle de $\vec{w}$."),
        ("a", "-2", "t", "de sens opposé", r"La norme de $\vec{a}$ est deux fois plus grande que celle de $\vec{t}$."),
        ("s", "2", "b", "de même sens", r"La norme de $\vec{s}$ est deux fois plus grande que celle de $\vec{b}$."),
        ("u", r"-\dfrac12", "v", "de sens opposé", r"La norme de $\vec{u}$ est deux fois plus petite que celle de $\vec{v}$ : c'est la moitié."),
        ("r", r"\dfrac32", "c", "de même sens", r"La norme de $\vec{r}$ est une fois et demie celle de $\vec{c}$. On peut se dire $\vec{r}=1{,}5\,\vec{c}$, mais le coefficient ne s'écrit pas – par convention – sous forme décimale. On sait que $1{,}5=\dfrac32$."),
        ("r", r"-\dfrac32", "v", "de sens opposé", r"La norme de $\vec{r}$ est une fois et demie celle de $\vec{v}$. On peut se dire $\vec{r}=-1{,}5\,\vec{v}$, mais le coefficient ne s'écrit pas – par convention – sous forme décimale. On sait que $1{,}5=\dfrac32$.")]
def expl(i):
    x, k, y, sens, n = EXPL[i]
    return (r"{\color{vert}$\vec{%s}=%s\,\vec{%s}$} : les vecteurs $\vec{%s}$ et $\vec{%s}$ ont même direction et sont %s. %s"
            % (x, k, y, x, y, sens, n))
for part, idx in ((1, range(0, 4)), (2, range(4, 7)), (3, range(7, 10))):
    img = latex_img("expl_e1q4_%d" % part, r"\large \begin{minipage}{15.5cm}{\color{vert}\Large Explication (%d/3)}\par\vspace{4pt}" % part +
                    r"\par\vspace{6pt}".join(expl(i) for i in idx) + r"\end{minipage}")
    slide("Ex1 – Q4 explication %d" % part, [title_el(E1 + "Correction de la question 4"), image_el(img, 1, 12, 98, 86, "Explication")])

# ---------- Exercice 2 ----------
E2 = "Exercice 2 — "
m21 = text_box("m_e2q1", "Point méthode", "orange", [
    r"Deux vecteurs sont colinéaires s'ils ont la \textit{même direction}.",
    r"On trace la droite (AB), puis les droites (CD), (EF), (GH) et (AK).",
    r"Un vecteur est colinéaire à $\V{AB}$ lorsque la droite qui le porte est parallèle à la droite (AB), ou confondue avec elle."])
question_slide("Ex2 – Q1", E2 + "Question 1", fig_ex2, m21, multichoice(
    "Parmi les vecteurs CD, EF, GH et AK, cocher ceux qui sont colinéaires au vecteur AB.",
    [("le vecteur CD", True, "Oui : la droite (CD) est parallèle à la droite (AB)."),
     ("le vecteur GH", True, "Oui : la droite (GH) est parallèle à la droite (AB)."),
     ("le vecteur AK", True, "Oui : K est sur la droite (AB), donc les droites (AK) et (AB) sont confondues."),
     ("le vecteur EF", False, "Non : la droite (EF) est sécante avec la droite (AB).")]), "Question 1")
step_slide("Ex2 – Q1 CD et GH", E2 + "Correction de la question 1", step_img("s_e2q1_1", r"$\V{CD}$ et $\V{GH}$",
    [r"Les droites (CD) et (GH) (en pointillés verts) sont parallèles à la droite (AB) (en pointillés orange).",
     r"Donc $\V{CD}$ et $\V{GH}$ ont même direction que $\V{AB}$ : {\color{red!70!black}ils sont colinéaires à $\V{AB}$}."], fstep("ex2_q1a")))
step_slide("Ex2 – Q1 AK et EF", E2 + "Correction de la question 1", step_img("s_e2q1_2", r"$\V{AK}$ et $\V{EF}$",
    [r"Le point K est sur la droite (AB) : les droites (AK) et (AB) sont confondues, donc {\color{red!70!black}$\V{AK}$ est colinéaire à $\V{AB}$}.",
     r"La droite (EF) (en gris) est sécante avec la droite (AB) : {\color{red!70!black}$\V{EF}$ n'est pas colinéaire à $\V{AB}$}."], fstep("ex2_q1b")))
step_slide("Ex2 – Q1 remarque", E2 + "Correction de la question 1", step_img("s_e2q1_3", r"Remarque — Vérifier avec les carreaux",
    [r"On part du premier point (l'origine) et on compte le déplacement jusqu'au second (l'extrémité).",
     tableau([VV("AB"), VV("CD"), VV("GH"), VV("AK"), VV("EF")], [3, 6, 9, 9, 3], [1, 2, 3, 3, 2]),
     r"Les déplacements de $\V{CD}$, $\V{GH}$ et $\V{AK}$ sont proportionnels à ceux de $\V{AB}$.\\ Pour $\V{EF}$, 3 n'est pas le triple de 2 : ce n'est pas proportionnel."], color="gris"))
m22 = text_box("m_e2q2", "Point méthode", "orange", [
    r"Le coefficient $k$ s'obtient en deux temps :",
    r"$\star$ son \textit{signe} : positif si le vecteur est de même sens que $\V{AB}$, négatif s'il est de sens opposé ;",
    r"$\star$ sa \textit{valeur} : combien de fois la norme de $\V{AB}$ faut-il prendre pour obtenir la norme du vecteur ?"])
question_slide("Ex2 – Q2", E2 + "Question 2", fig_ex2, m22, blanks(
    "Pour chaque vecteur colinéaire à AB, donner le réel k (écrire par exemple -2).",
    ["Le vecteur CD est égal à %s fois le vecteur AB." % ent("-2"),
     "Le vecteur GH est égal à %s fois le vecteur AB." % ent("-3"),
     "Le vecteur AK est égal à %s fois le vecteur AB." % ent("3")]), "Question 2")
step_slide("Ex2 – Q2 explication", E2 + "Correction de la question 2", step_img("s_e2q2_1", "Explication",
    [r"{\color{vert}$\V{CD}=-2\,\V{AB}$} : même direction, sens opposé ; la norme de $\V{CD}$ est deux fois plus grande que celle de $\V{AB}$.",
     r"{\color{vert}$\V{GH}=-3\,\V{AB}$} : même direction, sens opposé ; la norme de $\V{GH}$ est trois fois plus grande que celle de $\V{AB}$.",
     r"{\color{vert}$\V{AK}=3\,\V{AB}$} : même direction, même sens ; la norme de $\V{AK}$ est trois fois plus grande que celle de $\V{AB}$.",
     r"{\color{gris}Avec les carreaux :} $\V{AB}$ : 3 vers la droite, 1 vers le haut ; $\V{CD}$ : 6 vers la gauche, 2 vers le bas ; $\V{GH}$ : 9 vers la gauche, 3 vers le bas ; $\V{AK}$ : 9 vers la droite, 3 vers le haut."], fstep("ex2_q2")))
m23 = text_box("m_e2q3", "Point méthode", "orange", [
    r"On regarde si les droites (CD) et (GH) sont parallèles : si oui, les vecteurs sont colinéaires.",
    r"Pour le coefficient : d'abord le signe (même sens ou sens opposé), puis la valeur (combien de fois la norme de $\V{CD}$ ?). Ce peut être une fraction."])
question_slide("Ex2 – Q3", E2 + "Question 3", fig_ex2, m23, multichoice(
    "Les vecteurs CD et GH sont-ils colinéaires ? Si oui, quel est le réel k tel que le vecteur GH soit égal à k fois le vecteur CD ?",
    [("Oui, et k = 3/2.", True, "Exact : les droites sont parallèles, les vecteurs sont de même sens et la norme de GH est une fois et demie celle de CD."),
     ("Oui, et k = −3/2.", False, "Attention au sens : CD et GH vont tous les deux vers la gauche et vers le bas."),
     ("Oui, et k = 2/3.", False, "C'est l'inverse : GH est plus long que CD."),
     ("Oui, et k = 1,5.", False, "La valeur est juste, mais par convention le coefficient de colinéarité ne s'écrit pas sous forme décimale."),
     ("Non, ils ne sont pas colinéaires.", False, "Les droites (CD) et (GH) sont parallèles : regarde à nouveau.")], single=True), "Question 3")
step_slide("Ex2 – Q3 étape 1", E2 + "Correction de la question 3", step_img("s_e2q3_1", "Étape 1 — On compare les droites (CD) et (GH)",
    [r"La droite (GH) (en vert) est parallèle à la droite (CD) (en orange).",
     r"Les vecteurs $\V{CD}$ et $\V{GH}$ ont donc la même direction : ils sont colinéaires."], fstep("ex2_q3")))
step_slide("Ex2 – Q3 étape 2", E2 + "Correction de la question 3", step_img("s_e2q3_2", "Étape 2 — On cherche le coefficient et on conclut",
    [r"$\V{GH}$ et $\V{CD}$ sont de même sens : le coefficient est positif.",
     r"La norme de $\V{GH}$ est une fois et demie celle de $\V{CD}$. On peut se dire $\V{GH}=1{,}5\,\V{CD}$, mais le coefficient ne s'écrit pas – par convention – sous forme décimale. On sait que $1{,}5=\dfrac32$.",
     r"Donc {\color{red!70!black}$\V{GH}=\dfrac32\,\V{CD}$}.",
     r"{\color{gris}Avec les carreaux :} $9\div6=\dfrac32$ et $3\div2=\dfrac32$."], fstep("ex2_q3")))
m24 = text_box("m_e2q4", "Point méthode", "orange", [
    r"On utilise les propriétés du cours :",
    r"$\star$ $\V{AB}$ et $\V{CD}$ colinéaires $\Leftrightarrow$ (AB) et (CD) parallèles (ou confondues) ;",
    r"$\star$ $\V{AB}$ et $\V{AC}$ colinéaires $\Leftrightarrow$ A, B et C alignés."])
question_slide("Ex2 – Q4", E2 + "Question 4", fig_ex2, m24, single_choice_set([
    ("On a : vecteur CD = −2 × vecteur AB. Les droites (AB) et (CD) sont…", ["parallèles", "sécantes", "perpendiculaires"]),
    ("On a : vecteur AK = 3 × vecteur AB. Les points A, B et K…", ["sont alignés", "ne sont pas alignés"])]), "Question 4")
step_slide("Ex2 – Q4 correction", E2 + "Correction de la question 4", step_img("s_e2q4_1", "Correction",
    [r"On a $\V{CD}=-2\,\V{AB}$, donc $\V{AB}$ et $\V{CD}$ sont colinéaires. Ainsi, {\color{red!70!black}les droites (AB) et (CD) sont parallèles}.",
     r"On a $\V{AK}=3\,\V{AB}$, donc $\V{AB}$ et $\V{AK}$ sont colinéaires. Ainsi, {\color{red!70!black}les points A, B et K sont alignés}."], fstep("ex2_q4")))

# ============================================================================
# Assemblage du paquet .h5p
# ============================================================================
def build():
    build_images()
    slides = [dict(sl, elements=[resolve(e) for e in sl["elements"]]) for sl in SLIDES]
    cp = defaults("H5P.CoursePresentation")
    merge(cp, {"presentation": {"slides": slides, "keywordListEnabled": True, "globalBackgroundSelector": {},
                                "keywordListAlwaysShow": False, "keywordListAutoHide": False, "keywordListOpacity": 90},
               "override": {"activeSurface": False, "hideSummarySlide": False, "enablePrintButton": False,
                            "summarySlideSolutionButton": True, "summarySlideRetryButton": True}})
    used = ["H5P.CoursePresentation", "H5P.AdvancedText", "H5P.Image", "H5P.MultiChoice", "H5P.Blanks", "H5P.SingleChoiceSet", "H5P.MarkTheWords"]
    deps = []
    for m in used:
        j = lib_version(m)[1]
        deps.append({"machineName": m, "majorVersion": j["majorVersion"], "minorVersion": j["minorVersion"]})
    h5p = {"title": "Exemples colinéarité", "language": "fr", "mainLibrary": "H5P.CoursePresentation",
           "embedTypes": ["iframe"], "license": "U", "defaultLanguage": "fr", "preloadedDependencies": deps}
    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("h5p.json", json.dumps(h5p, ensure_ascii=False, indent=1))
        z.writestr("content/content.json", json.dumps(cp, ensure_ascii=False))
        for name in IMAGES:
            z.write(os.path.join(IMG, name + ".png"), "content/images/%s.png" % name)
        for root, dirs, files in os.walk(LIBS):
            for f in files:
                if f.startswith("."):
                    continue
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, LIBS))
    print("OK :", OUT, "—", len(slides), "diapositives,", len(IMAGES), "images")

if __name__ == "__main__":
    build()
