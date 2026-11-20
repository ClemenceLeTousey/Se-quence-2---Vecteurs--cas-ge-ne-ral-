# -*- coding: utf-8 -*-
"""
Génère le parcours Éléa (Moodle) différencié de la Séquence 2 – Vecteurs :
  - Séquence 2 - Éléa - Banque de questions.xml   (format Moodle XML, à importer)
  - Bloc N - Je révise.html                       (pages « Je révise », à coller dans une ressource Page)
  - Séquence 2 - Éléa - Fiche de montage.html     (mode d'emploi du montage dans Éléa)
Usage : python3 build_elea.py
"""
import os, html, re
import figures

HERE = os.path.dirname(os.path.abspath(__file__))
figures.build()

# ----------------------------------------------------------------------------
# Références (cours, vidéos, exercices) utilisées dans les indices et feedbacks
# ----------------------------------------------------------------------------
YT = "https://www.youtube.com/watch?v="
VIDEOS = {
    "translation": ("Construire l'image d'une figure par une translation", "8Jb9cMOeYSk"),
    "point":       ("Construire un point à partir de vecteurs", "zcQPz4dfnn0"),
    "proprietes":  ("Utiliser des propriétés sur les vecteurs", "XokpP_8mTOE"),
    "somme":       ("Construire un point à partir d'une somme de vecteurs", "nzABUzFM6p8"),
    "chasles":     ("Appliquer la relation de Chasles", "vqkWtfsCfOo"),
    "produit":     ("Construire un vecteur comme produit et somme de vecteurs", "ak1WcdhOaFA"),
    "colineaires": ("Démontrer que deux vecteurs sont colinéaires", "62Uh6UKz-Wk"),
    "egalite":     ("Construire un point à partir d'une égalité vectorielle", "1C6KEwbO-b8"),
    "exprimer":    ("Exprimer un vecteur en fonction de deux autres", "ODZGKdIKewo"),
    "cours":       ("LE COURS : Les vecteurs (révision complète)", "aSSDBNn_rRI"),
    "qcm":         ("QCM : Les vecteurs (auto-évaluation)", "AwzchpN8S9g"),
}
CAPYTALE = {
    "definitions": ("Définitions", "183d-11585990"),
    "somme":       ("Somme", "b218-11585991"),
    "colinearite": ("Colinéarité", "bd09-11585993"),
    "alignes":     ("Points alignés (F3¾ Ex 4)", "414a-11688973"),
}
def capy(k):
    t, c = CAPYTALE[k]
    return '<a href="https://capytale2.ac-paris.fr/web/c/%s/edn" target="_blank">Capytale « %s » (code %s)</a>' % (c, t, c)

def video(k):
    t, i = VIDEOS[k]
    return '<a href="%s%s" target="_blank">vidéo « %s »</a>' % (YT, i, t)

# Sections du cours (polycopié « Séquence 2 - Cours - Vecteurs.pdf »)
SEC = {
    "1.1": ("§ 1.1 Translations et vecteurs", 1),
    "1.2": ("§ 1.2 Égalité de vecteurs", 2),
    "1.3": ("§ 1.3 Vecteurs particuliers (vecteur nul, vecteur opposé)", 2),
    "1.4": ("§ 1.4 Interprétation géométrique (parallélogramme)", 2),
    "2.1": ("§ 2.1 Somme : construction bout à bout", 3),
    "2.2": ("§ 2.2 Relation de Chasles", 4),
    "2.3": ("§ 2.3 Méthode du parallélogramme", 4),
    "3":   ("§ 3 Multiplication par un scalaire", 5),
    "4":   ("§ 4 Vecteurs colinéaires", 6),
    "4b":  ("§ 4 Colinéarité, parallélisme et alignement", 7),
    "M":   ("encadré « Méthode – démontrer avec des vecteurs » (Feuille 3¾, page 2)", None),
}
def relis(sec, vid=None):
    t, p = SEC[sec]
    s = "Relis <b>%s</b>" % t
    if p:
        s += " du cours (page %d)" % p
    if vid:
        s += ", et regarde la " + video(vid)
    return s + "."

# ----------------------------------------------------------------------------
# Petits helpers de notation MathJax
# ----------------------------------------------------------------------------
def V(ab):            # \(\overrightarrow{AB}\)
    return r"\(\overrightarrow{%s}\)" % ab
def v(u):             # \(\vec u\)
    return r"\(\vec %s\)" % u
def M(expr):          # math inline brute
    return r"\(%s\)" % expr
NUL = r"\(\vec 0\)"
def fig(name, width=380):
    return '<p><img src="@@PLUGINFILE@@/fig_%s.png" alt="figure" width="%d"></p>' % (name, width)

# ----------------------------------------------------------------------------
# Banque de questions
# ----------------------------------------------------------------------------
# Chaque question : dict(type, name, text, answers, hints, general, fig, single, tol)
#   answers : liste de (fraction, texte, feedback)
Q = []
def add(cat, **kw):
    kw["cat"] = cat
    Q.append(kw)

CAT_TOP = "Séquence 2 – Vecteurs"
C0 = CAT_TOP + "/0 – Positionnement (prérequis)"
C1 = CAT_TOP + "/Bloc 1 – Définition d'un vecteur"
C2 = CAT_TOP + "/Bloc 2 – Somme et relation de Chasles"
C3 = CAT_TOP + "/Bloc 3 – Produit par un réel, colinéarité"
C4 = CAT_TOP + "/Bloc 4 – Décomposition, alignement, milieu"
C5 = CAT_TOP + "/Bilan – synthèse"

# ======================= 0. POSITIONNEMENT =======================
add(C0, type="mc", single=False, name="P1 – Figures translatées",
    text="Les cinq figures ci-dessous sont superposables. Cocher <b>toutes</b> les figures qui sont l'image de la figure 1 par une translation." + fig("p1", 420),
    answers=[(50, "Figure 2", "Oui : même orientation, simplement déplacée."),
             (50, "Figure 4", "Oui : même orientation, simplement déplacée."),
             (-50, "Figure 3", "Non : la figure 3 a fait un demi-tour, c'est une rotation."),
             (-50, "Figure 5", "Non : la figure 5 est retournée comme dans un miroir, c'est une symétrie axiale.")],
    hints=["Une translation <i>glisse</i> la figure sans la tourner ni la retourner : l'orientation est conservée.",
           "Compare le drapeau : dans une translation, la pointe reste du même côté et vers le même haut."],
    general="Les figures 2 et 4 ont exactement la même orientation que la figure 1 : ce sont ses images par translation. La figure 3 est tournée d'un demi-tour (rotation), la figure 5 est retournée (symétrie).")

add(C0, type="mc", name="P2 – Image d'un point (réseau de points)",
    text="Par la translation qui transforme A en F, quelle est l'image du point G ?" + fig("p2", 300),
    answers=[(100, "L", "Exact : on se décale d'une colonne vers la droite et d'une ligne vers le bas."),
             (0, "K", "Tu es descendu d'une ligne, mais il faut aussi aller d'une colonne vers la droite."),
             (0, "H", "Tu es allé d'une colonne vers la droite, mais il faut aussi descendre d'une ligne."),
             (0, "B", "C'est le déplacement inverse (de F vers A).")],
    hints=["Regarde le déplacement de A vers F : combien de colonnes ? combien de lignes ? Dans quel sens ?",
           "De A à F on va d'une colonne vers la droite et d'une ligne vers le bas. Applique le même déplacement à partir de G."],
    general="La translation qui transforme A en F déplace d'une colonne vers la droite et d'une ligne vers le bas. À partir de G, on arrive en L.")

add(C0, type="num", name="P3 – Longueur sur quadrillage (Pythagore)",
    text="Les carreaux ont pour côté 1. Le vecteur " + V("AB") + " correspond à un déplacement de 3 carreaux vers la droite et 4 carreaux vers le haut. Quelle est sa norme " + M(r"\lVert\overrightarrow{AB}\rVert") + ", c'est-à-dire la longueur AB ?" + fig("p3", 260),
    answers=[(100, "5", "Exact : " + M(r"AB=\sqrt{3^2+4^2}=\sqrt{25}=5") + ".")],
    hints=["Le déplacement horizontal et le déplacement vertical forment un triangle rectangle avec [AB].",
           "Théorème de Pythagore : " + M(r"AB^2=3^2+4^2") + "."],
    general="Dans le triangle rectangle formé par les deux déplacements, " + M(r"AB^2=3^2+4^2=25") + " donc " + M("AB=5") + ". Ce calcul de norme revient dans les automatismes (Série 3).")

add(C0, type="mc", name="P4 – Parallélogramme : diagonales",
    text="Dans un parallélogramme, les diagonales…",
    answers=[(100, "se coupent en leur milieu.", "Exact. C'est la propriété qu'on utilisera pour caractériser un parallélogramme avec des vecteurs."),
             (0, "sont perpendiculaires.", "Ce n'est vrai que pour les losanges."),
             (0, "ont la même longueur.", "Ce n'est vrai que pour les rectangles."),
             (0, "sont parallèles.", "Deux diagonales se coupent toujours : elles ne peuvent pas être parallèles.")],
    hints=["Pense à un parallélogramme quelconque, ni rectangle ni losange.", "Propriété de collège : le centre d'un parallélogramme est le milieu commun de ses diagonales."],
    general="Dans un parallélogramme, les diagonales se coupent en leur milieu (et réciproquement). Cette propriété est rappelée au § 1.1 du cours (page 1).")

add(C0, type="mc", name="P5 – Ce que conserve une translation",
    text="Vrai ou faux : une translation conserve les longueurs, les angles et les aires.",
    answers=[(100, "Vrai", "Exact : une translation est un déplacement sans déformation."),
             (0, "Faux", "Une translation glisse la figure sans la déformer : tout est conservé.")],
    hints=["Une figure translatée est superposable à la figure de départ.", "Relis la fiche de rappel sur les translations (collège) : c'est un déplacement sans déformation."],
    general="Une translation transforme une figure en une figure superposable : longueurs, angles, aires et parallélisme sont conservés.")

# ======================= BLOC 1 =======================
add(C1, type="mc", name="B1-01 – Image d'un point par une translation",
    text="Quel point est l'image de L par la translation de vecteur " + V("AB") + " ?" + fig("b1a"),
    answers=[(100, "M", "Exact : même déplacement que de A vers B (3 carreaux vers la droite, 1 vers le haut)."),
             (0, "N", "Tu es descendu d'un carreau : le vecteur " + V("AB") + " monte d'un carreau."),
             (0, "R", "Tu as échangé les déplacements horizontal et vertical."),
             (0, "S", "Le déplacement horizontal est de 3 carreaux, pas 4 : la norme n'est pas respectée.")],
    hints=["Le vecteur " + V("AB") + " correspond à un déplacement de 3 carreaux vers la droite et 1 carreau vers le haut. Applique le même déplacement à partir de L.",
           relis("1.1", "point")],
    general="L'image L' de L vérifie " + V("LL'") + " = " + V("AB") + " : même direction, même sens, même norme. À partir de L, 3 carreaux vers la droite et 1 vers le haut : c'est M.<br>Pour t'entraîner : Feuille 2, Ex 1 et 2 ; manuel Ex 15 p. 183.")

def b1b_common(correct, feed):
    opts = {"CD": "Ce vecteur a même direction, même sens et même norme que " + V("AB") + " : il lui est égal.",
            "EF": V("EF") + " a même direction et même norme que " + V("AB") + " mais le sens opposé : c'est " + M(r"-\overrightarrow{AB}") + ".",
            "GH": V("GH") + " a même direction et même sens que " + V("AB") + " mais une norme double.",
            "IJ": V("IJ") + " n'a pas la même direction que " + V("AB") + " (il descend au lieu de monter).",
            "KL": V("KL") + " n'a pas la même direction que " + V("AB") + "."}
    return [(100 if k == correct else 0, V(k), (feed if k == correct else opts[k])) for k in opts]

add(C1, type="mc", name="B1-02 – Vecteur égal",
    text="Quel vecteur est <b>égal</b> à " + V("AB") + " ?" + fig("b1b", 460),
    answers=b1b_common("CD", "Exact : même direction, même sens, même norme."),
    hints=["Deux vecteurs sont égaux s'ils ont <b>même direction, même sens et même norme</b>. Vérifie les trois critères, un par un.",
           relis("1.2", "proprietes")],
    general="Seul " + V("CD") + " vérifie les trois critères (3 carreaux vers la droite, 1 vers le haut). " + V("EF") + " est l'opposé, " + V("GH") + " a une norme double, " + V("IJ") + " et " + V("KL") + " n'ont pas la même direction.<br>Pour t'entraîner : Feuille 2, Ex 5 et 6 ; manuel Ex 18 p. 183.")

add(C1, type="mc", name="B1-03 – Vecteur opposé",
    text="Quel vecteur est <b>opposé</b> à " + V("AB") + " ?" + fig("b1b", 460),
    answers=b1b_common("EF", "Exact : même direction, même norme, sens opposé : " + V("EF") + " = " + M(r"-\overrightarrow{AB}") + " = " + V("BA") + "."),
    hints=["Le vecteur opposé a la même direction et la même norme, mais le sens contraire.", relis("1.3", "proprietes")],
    general="Le vecteur opposé à " + V("AB") + " est " + V("BA") + " : même direction, même norme, sens opposé. Sur la figure, c'est " + V("EF") + " (3 carreaux vers la gauche, 1 vers le bas).<br>Pour t'entraîner : Feuille 2, Ex 6 et 11.")

add(C1, type="mc", name="B1-04 – Même direction, même sens, norme différente",
    text="Quel vecteur a <b>même direction et même sens</b> que " + V("AB") + ", mais <b>pas la même norme</b> ?" + fig("b1b", 460),
    answers=b1b_common("GH", "Exact : " + V("GH") + " est deux fois plus long que " + V("AB") + ", dans la même direction et le même sens."),
    hints=["Cherche un vecteur parallèle à " + V("AB") + ", qui pointe du même côté, mais plus long ou plus court.",
           relis("1.2", "proprietes")],
    general=V("GH") + " correspond à 6 carreaux vers la droite et 2 vers le haut : même direction et même sens que " + V("AB") + ", norme double. (On écrira plus tard " + V("GH") + " = " + M(r"2\overrightarrow{AB}") + ".)<br>Pour t'entraîner : Évaluation formative 2, Ex 2 ; Feuille 2, Ex 6.")

add(C1, type="mc", name="B1-05 – AB et BA",
    text="Vrai ou faux : les vecteurs " + V("AB") + " et " + V("BA") + " ont la même direction.",
    answers=[(100, "Vrai", "Exact : ils ont même direction (la droite (AB)) et même norme (AB), seul le sens change."),
             (0, "Faux", "La direction est la droite (AB) pour les deux. Ce qui change, c'est le <b>sens</b> : " + V("BA") + " = " + M(r"-\overrightarrow{AB}") + ".")],
    hints=["Direction = la droite qui porte le vecteur. Sens = de quel côté il pointe. Ne confonds pas les deux.", relis("1.1")],
    general="Direction : la droite (AB) pour les deux ; norme : AB pour les deux ; sens : opposés. Ainsi " + V("BA") + " = " + M(r"-\overrightarrow{AB}") + ". C'est l'« Attention » du § 1.1.")

add(C1, type="mc", name="B1-06 – Parallélogramme : égalité fausse",
    text="ABCD est un parallélogramme. Vrai ou faux : " + V("AD") + " = " + V("CB") + "." + fig("b1c", 320),
    answers=[(0, "Vrai", V("AD") + " et " + V("CB") + " ont même direction et même norme, mais des sens opposés. L'égalité correcte est " + V("AD") + " = " + V("BC") + "."),
             (100, "Faux", "Exact : " + V("AD") + " = " + V("BC") + ", et " + V("CB") + " est son opposé.")],
    hints=["Suis les flèches sur la figure : " + V("AD") + " va de A vers D. Dans quel sens va " + V("CB") + " ?",
           relis("1.4", "proprietes")],
    general="Dans le parallélogramme ABCD : " + V("AB") + " = " + V("DC") + " et " + V("AD") + " = " + V("BC") + ". Le vecteur " + V("CB") + " est l'opposé de " + V("BC") + ", donc " + V("AD") + " ≠ " + V("CB") + ".<br>Pour t'entraîner : Feuille 2, Ex 11 ; manuel Ex 23 p. 184.")

add(C1, type="mc", name="B1-07 – Parallélogramme : compléter une égalité",
    text="ABCD est un parallélogramme. Compléter : " + V("AB") + " = …" + fig("b1c", 320),
    answers=[(100, V("DC"), "Exact : c'est la caractérisation du parallélogramme."),
             (0, V("CD"), "Sens opposé : " + V("CD") + " = " + M(r"-\overrightarrow{AB}") + "."),
             (0, V("AD"), "Direction différente : ce sont deux côtés consécutifs."),
             (0, V("BD"), V("BD") + " est une diagonale, elle n'a pas la même direction que (AB).")],
    hints=["Le côté opposé à [AB] est [DC]. Reste à choisir le bon sens : de D vers C ou de C vers D ?", relis("1.4", "proprietes")],
    general="ABCD est un parallélogramme si et seulement si " + V("AB") + " = " + V("DC") + " (théorème du § 1.4). Attention à l'ordre des lettres : c'est " + V("DC") + ", pas " + V("CD") + ".<br>Pour t'entraîner : Feuille 2, Ex 11 ; automatismes Série 2 J4.")

add(C1, type="cloze", name="B1-08 – Parallélogramme de centre O",
    text="ABCD est un parallélogramme de centre O. Compléter chaque égalité avec <b>la lettre</b> du point qui convient." + fig("b1c", 320) +
         "<p>" + M(r"\overrightarrow{BO}=\overrightarrow{O\,?}") + " → le point manquant est {1:SHORTANSWER:=D#Exact : O est le milieu de [BD].~%0%B#Sens opposé.~%0%C#Ce n'est pas la bonne diagonale.}</p>" +
         "<p>" + M(r"\overrightarrow{AO}=\overrightarrow{?\,C}") + " → le point manquant est {1:SHORTANSWER:=O#Exact : O est le milieu de [AC].~%0%A#Le vecteur AC est deux fois trop long.}</p>",
    hints=["O est le milieu des deux diagonales : " + V("BO") + " et " + V("OD") + " sont égaux (même direction, même sens, même norme).", relis("1.4", "proprietes")],
    general="Les diagonales d'un parallélogramme se coupent en leur milieu O, donc " + V("BO") + " = " + V("OD") + " et " + V("AO") + " = " + V("OC") + ".<br>Pour t'entraîner : Feuille 2, Ex 11 (question 3).")

add(C1, type="mc", name="B1-09 – Représentant d'origine donnée",
    text="Quel est le représentant du vecteur " + v("u") + " d'<b>origine</b> C ?" + fig("b1e"),
    answers=[(100, V("CD"), "Exact : de C, 2 carreaux vers la droite et 1 vers le haut, on arrive en D."),
             (0, V("DC"), "Sens opposé : " + V("DC") + " = " + M(r"-\vec u") + "."),
             (0, V("FE"), V("FE") + " est bien un représentant de " + v("u") + ", mais son origine est F, pas C."),
             (0, V("CE"), V("CE") + " n'a pas la même direction que " + v("u") + ".")],
    hints=["Un représentant de " + v("u") + " d'origine C est un vecteur " + V("CX") + " égal à " + v("u") + " : même déplacement, en partant de C.",
           relis("1.2", "point")],
    general=v("u") + " correspond à 2 carreaux vers la droite et 1 vers le haut. En partant de C on arrive en D : le représentant cherché est " + V("CD") + ". Les vecteurs " + V("AB") + ", " + V("CD") + " et " + V("FE") + " sont tous des représentants de " + v("u") + ".<br>Pour t'entraîner : Feuille 2, Ex 10 et 12.")

add(C1, type="mc", name="B1-10 – Représentant d'extrémité donnée",
    text="Quel est le représentant du vecteur " + v("u") + " d'<b>extrémité</b> E ?" + fig("b1e"),
    answers=[(100, V("FE"), "Exact : de F à E, 2 carreaux vers la droite et 1 vers le haut."),
             (0, V("EF"), "Sens opposé : l'extrémité doit être E, l'origine F."),
             (0, V("AB"), V("AB") + " est un représentant de " + v("u") + ", mais son extrémité est B."),
             (0, V("ED"), V("ED") + " n'a pas la même direction que " + v("u") + ".")],
    hints=["Cherche le point X tel que " + V("XE") + " = " + v("u") + " : il faut partir de E et faire le déplacement <i>à l'envers</i>.",
           relis("1.2", "point")],
    general="Pour arriver en E avec le déplacement de " + v("u") + " (2 vers la droite, 1 vers le haut), il faut partir de F. Le représentant est " + V("FE") + ".<br>Pour t'entraîner : Feuille 2, Ex 12 ; Évaluation formative 2, Ex 2.")

add(C1, type="mc", name="B1-11 – Translation et représentant",
    text="Quel point est l'image de F par la translation de vecteur " + v("u") + " ?" + fig("b1e"),
    answers=[(100, "E", "Exact : " + V("FE") + " = " + v("u") + "."),
             (0, "D", "C'est l'image de C, pas de F."),
             (0, "B", "C'est l'image de A, pas de F."),
             (0, "G", V("FG") + " n'est pas égal à " + v("u") + ".")],
    hints=["L'image F' de F vérifie " + V("FF'") + " = " + v("u") + ". Applique le déplacement de " + v("u") + " à partir de F.", relis("1.1", "point")],
    general="La translation de vecteur " + v("u") + " transforme F en E car " + V("FE") + " = " + v("u") + ". De même elle transforme A en B et C en D.<br>Pour t'entraîner : Feuille 2, Ex 1 et 2.")

add(C1, type="mc", name="B1-12 – Nombre de représentants",
    text="Combien de représentants possède un vecteur non nul ?",
    answers=[(100, "Une infinité.", "Exact : on peut choisir n'importe quel point comme origine."),
             (0, "Un seul.", "Non : l'origine d'un vecteur n'est pas fixée, on peut le « poser » n'importe où."),
             (0, "Deux (lui-même et son opposé).", "L'opposé n'est pas un représentant : il n'a pas le même sens."),
             (0, "Autant que de points sur sa direction.", "On peut choisir l'origine <i>partout</i> dans le plan, pas seulement sur une droite.")],
    hints=["Un vecteur est défini par direction, sens et norme, pas par son origine.", relis("1.2")],
    general="Un vecteur n'est pas caractérisé par son origine et son extrémité : il admet une infinité de représentants (« À noter » du § 1.2).")

add(C1, type="mc", name="B1-13 – Vecteur nul",
    text="Vrai ou faux : le vecteur nul " + NUL + " a une norme égale à 0, mais sa direction et son sens ne sont pas définis.",
    answers=[(100, "Vrai", "Exact."),
             (0, "Faux", "C'est la définition du § 1.3 : norme 0, pas de direction ni de sens.")],
    hints=["Le vecteur nul est associé à la translation qui laisse tous les points fixes.", relis("1.3")],
    general="Le vecteur nul " + NUL + " = " + V("AA") + " correspond à la translation qui ne déplace rien : sa norme est 0, et il n'a ni direction ni sens (§ 1.3).")

add(C1, type="mc", name="B1-14 – De l'égalité au parallélogramme",
    text="A, B, C, D sont quatre points tels que " + V("AB") + " = " + V("DC") + ". Que peut-on en déduire ?",
    answers=[(100, "ABCD est un parallélogramme.", "Exact (éventuellement aplati)."),
             (0, "ABDC est un parallélogramme.", "Attention à l'ordre des lettres : " + V("AB") + " = " + V("DC") + " caractérise ABCD, pas ABDC."),
             (0, V("AC") + " = " + V("BD"), "Ce sont les diagonales : elles ne sont pas égales en général."),
             (0, "Les points A, B, C, D sont alignés.", "Ils ne le sont que si le parallélogramme est aplati.")],
    hints=["Théorème du § 1.4 : ABCD est un parallélogramme si et seulement si " + V("AB") + " = " + V("DC") + ".", relis("1.4", "proprietes")],
    general="D'après le théorème du § 1.4, " + V("AB") + " = " + V("DC") + " équivaut à : ABCD est un parallélogramme. (Automatismes Série 2 J4.)<br>Pour t'entraîner : Feuille 2, Ex 7, 8, 9 ; DS 1, Ex 4.")

add(C1, type="mc", name="B1-15 – Translation dans un parallélogramme",
    text="ABCD est un parallélogramme. Quelle est l'image de D par la translation de vecteur " + V("AB") + " ?" + fig("b1c", 320),
    answers=[(100, "C", "Exact : " + V("DC") + " = " + V("AB") + "."),
             (0, "A", "Ce serait la translation de vecteur " + V("DA") + "."),
             (0, "B", "Ce serait la translation de vecteur " + V("DB") + " (une diagonale)."),
             (0, "Aucun point de la figure.", "Si, l'image est un sommet du parallélogramme : cherche X tel que " + V("DX") + " = " + V("AB") + ".")],
    hints=["L'image X de D vérifie " + V("DX") + " = " + V("AB") + ". Quel vecteur de la figure est égal à " + V("AB") + " ?", relis("1.4", "translation")],
    general="Dans un parallélogramme ABCD, " + V("AB") + " = " + V("DC") + ". Donc la translation de vecteur " + V("AB") + " transforme D en C (Propriété 1 du § 1.1).<br>Pour t'entraîner : Exemple 1 du cours (page 1) ; manuel Ex 27 p. 184.")

# ======================= BLOC 2 =======================
add(C2, type="mc", name="B2-01 – Somme de deux vecteurs (figure)",
    text="Quel vecteur est égal à " + M(r"\vec u+\vec v") + " ?" + fig("b2a", 460),
    answers=[(100, v("a"), "Exact : 3 + 1 = 4 carreaux vers la droite, 1 + 2 = 3 carreaux vers le haut."),
             (0, v("b"), "C'est " + M(r"\vec u-\vec v") + " : tu as retranché " + v("v") + " au lieu de l'ajouter."),
             (0, v("c"), "C'est " + M(r"-(\vec u+\vec v)") + " : bonne direction, mais sens opposé."),
             (0, v("d"), "Le déplacement horizontal est bon (4), mais il faut aussi ajouter les déplacements verticaux : 1 + 2 = 3.")],
    hints=["Place " + v("v") + " bout à bout après " + v("u") + " : le vecteur somme va de l'origine de " + v("u") + " à l'extrémité de " + v("v") + ".",
           relis("2.1", "somme")],
    general=v("u") + " : 3 vers la droite, 1 vers le haut ; " + v("v") + " : 1 vers la droite, 2 vers le haut. Bout à bout : 4 vers la droite, 3 vers le haut, c'est " + v("a") + ".<br>Pour t'entraîner : Feuille 2, Ex 13 ; manuel Ex 39 p. 186 ; " + capy("somme") + ".")

add(C2, type="mc", name="B2-02 – Différence de deux vecteurs (figure)",
    text="Quel vecteur est égal à " + M(r"\vec u-\vec v") + " ?" + fig("b2a", 460),
    answers=[(100, v("b"), "Exact : " + M(r"\vec u-\vec v=\vec u+(-\vec v)") + " : 3 − 1 = 2 vers la droite, 1 − 2 = −1 (1 vers le bas)."),
             (0, v("a"), "C'est " + M(r"\vec u+\vec v") + "."),
             (0, v("c"), "C'est " + M(r"-(\vec u+\vec v)") + "."),
             (0, v("d"), "Ce vecteur n'est ni la somme ni la différence.")],
    hints=["Soustraire " + v("v") + ", c'est ajouter son opposé " + M(r"-\vec v") + " (même direction, même norme, sens contraire).", relis("2.1", "somme")],
    general=M(r"\vec u-\vec v=\vec u+(-\vec v)") + ". On place " + M(r"-\vec v") + " (1 vers la gauche, 2 vers le bas) bout à bout après " + v("u") + " : on obtient 2 vers la droite et 1 vers le bas, c'est " + v("b") + ".<br>Pour t'entraîner : Exemple 4 du cours (page 3) ; DS 1, Ex 6.")

add(C2, type="sa", name="B2-03 – Chasles : TR + RP",
    text="Simplifier " + M(r"\overrightarrow{TR}+\overrightarrow{RP}") + " à l'aide de la relation de Chasles.<br><i>Réponse attendue : le nom du vecteur, avec ses deux lettres (par exemple : AB).</i>",
    answers=[(100, "TP", "Exact : " + M(r"\overrightarrow{TR}+\overrightarrow{RP}=\overrightarrow{TP}") + "."),
             (100, "*{TP}", "Exact."),
             (0, "PT", "Sens opposé : on part de T et on arrive en P."),
             (0, "*", "Relis la relation de Chasles : " + M(r"\overrightarrow{AM}+\overrightarrow{MB}=\overrightarrow{AB}") + ".")],
    hints=["Relation de Chasles : " + M(r"\overrightarrow{AM}+\overrightarrow{MB}=\overrightarrow{AB}") + ". Le point du milieu (R) disparaît.", relis("2.2", "chasles")],
    general="La lettre R est extrémité du premier vecteur et origine du second : elle « s'efface ». " + M(r"\overrightarrow{TR}+\overrightarrow{RP}=\overrightarrow{TP}") + ".<br>Pour t'entraîner : Feuille 2, Ex 14 ; manuel Ex 42, 43 p. 187.")

add(C2, type="sa", name="B2-04 – Chasles : GT + AG",
    text="Simplifier " + M(r"\overrightarrow{GT}+\overrightarrow{AG}") + " à l'aide de la relation de Chasles.<br><i>Réponse attendue : le nom du vecteur, avec ses deux lettres (par exemple : AB).</i>",
    answers=[(100, "AT", "Exact : " + M(r"\overrightarrow{GT}+\overrightarrow{AG}=\overrightarrow{AG}+\overrightarrow{GT}=\overrightarrow{AT}") + "."),
             (100, "*{AT}", "Exact."),
             (0, "TA", "Sens opposé : on part de A et on arrive en T."),
             (0, "*", "Commence par réordonner : " + M(r"\overrightarrow{AG}+\overrightarrow{GT}") + ".")],
    hints=["L'ordre n'a pas d'importance dans une somme : réécris " + M(r"\overrightarrow{AG}+\overrightarrow{GT}") + " pour faire apparaître deux fois la lettre G au milieu.", relis("2.2", "chasles")],
    general=M(r"\overrightarrow{GT}+\overrightarrow{AG}=\overrightarrow{AG}+\overrightarrow{GT}=\overrightarrow{AT}") + " (Exemple 5 du cours).<br>Pour t'entraîner : Feuille 2, Ex 14 ; manuel Ex 45, 46 p. 187.")

add(C2, type="mc", name="B2-05 – Chasles avec des soustractions",
    text="Simplifier " + M(r"\overrightarrow{AB}-\overrightarrow{AC}-\overrightarrow{CB}") + ".",
    answers=[(100, NUL, "Exact : " + M(r"\overrightarrow{AC}+\overrightarrow{CB}=\overrightarrow{AB}") + ", donc l'expression vaut " + M(r"\overrightarrow{AB}-\overrightarrow{AB}=\vec 0") + "."),
             (0, V("AB"), "Tu as oublié de retrancher " + M(r"\overrightarrow{AC}+\overrightarrow{CB}") + ", qui vaut " + V("AB") + "."),
             (0, M(r"2\overrightarrow{AB}"), "Attention aux signes : " + M(r"-\overrightarrow{AC}-\overrightarrow{CB}=-(\overrightarrow{AC}+\overrightarrow{CB})=-\overrightarrow{AB}") + "."),
             (0, V("CB"), "Regroupe d'abord " + M(r"\overrightarrow{AC}+\overrightarrow{CB}") + ".")],
    hints=["Regroupe les deux vecteurs soustraits : " + M(r"-\overrightarrow{AC}-\overrightarrow{CB}=-(\overrightarrow{AC}+\overrightarrow{CB})") + ". Puis Chasles.", relis("2.2", "chasles")],
    general=M(r"\overrightarrow{AB}-\overrightarrow{AC}-\overrightarrow{CB}=\overrightarrow{AB}-(\overrightarrow{AC}+\overrightarrow{CB})=\overrightarrow{AB}-\overrightarrow{AB}=\vec 0") + ". Autre méthode : passer aux opposés, " + M(r"\overrightarrow{AB}+\overrightarrow{CA}+\overrightarrow{BC}=\overrightarrow{AB}+\overrightarrow{BC}+\overrightarrow{CA}=\vec 0") + " (rappel automatismes Série 3).<br>Pour t'entraîner : Exemple 5 du cours ; automatismes Série 3 J4.")

add(C2, type="sa", name="B2-06 – Chasles : quatre vecteurs",
    text="Simplifier " + M(r"\overrightarrow{BC}-\overrightarrow{BA}+\overrightarrow{BD}-\overrightarrow{BC}") + ".<br><i>Réponse attendue : le nom du vecteur, avec ses deux lettres.</i>",
    answers=[(100, "AD", "Exact : " + M(r"\overrightarrow{BD}-\overrightarrow{BA}=\overrightarrow{AB}+\overrightarrow{BD}=\overrightarrow{AD}") + "."),
             (100, "*{AD}", "Exact."),
             (0, "DA", "Sens opposé."),
             (0, "*", "Commence par simplifier " + M(r"\overrightarrow{BC}-\overrightarrow{BC}") + ", puis remplace " + M(r"-\overrightarrow{BA}") + " par " + V("AB") + ".")],
    hints=[M(r"\overrightarrow{BC}-\overrightarrow{BC}=\vec 0") + ". Il reste " + M(r"\overrightarrow{BD}-\overrightarrow{BA}") + ". Rappel : " + M(r"-\overrightarrow{BA}=\overrightarrow{AB}") + ".", relis("2.2", "chasles")],
    general=M(r"\overrightarrow{BC}-\overrightarrow{BA}+\overrightarrow{BD}-\overrightarrow{BC}=\overrightarrow{BD}-\overrightarrow{BA}=\overrightarrow{AB}+\overrightarrow{BD}=\overrightarrow{AD}") + " (Exemple 5 du cours).<br>Pour t'entraîner : Feuille 2, Ex 14 ; DS 1, Ex 5.")

add(C2, type="mc", name="B2-07 – Chasles (type DS)",
    text="Simplifier " + M(r"\overrightarrow{UV}-\overrightarrow{WV}+\overrightarrow{WX}") + ".",
    answers=[(100, V("UX"), "Exact : " + M(r"-\overrightarrow{WV}=\overrightarrow{VW}") + ", puis " + M(r"\overrightarrow{UV}+\overrightarrow{VW}+\overrightarrow{WX}=\overrightarrow{UX}") + "."),
             (0, V("XU"), "Sens opposé : on part de U."),
             (0, V("UW"), "Tu as oublié le dernier vecteur " + V("WX") + "."),
             (0, V("VX"), "Tu as perdu le premier vecteur " + V("UV") + ".")],
    hints=["Transforme la soustraction : " + M(r"-\overrightarrow{WV}=\overrightarrow{VW}") + ". Ensuite les lettres s'enchaînent : U→V→W→X.", relis("2.2", "chasles")],
    general=M(r"\overrightarrow{UV}-\overrightarrow{WV}+\overrightarrow{WX}=\overrightarrow{UV}+\overrightarrow{VW}+\overrightarrow{WX}=\overrightarrow{UX}") + " (DS 1, Ex 5).")

add(C2, type="mc", name="B2-08 – Hexagone : AB + CD",
    text="ABCDEF est un hexagone régulier de centre O. Compléter : " + M(r"\overrightarrow{AB}+\overrightarrow{CD}=") + " …" + fig("hex", 260),
    answers=[(100, V("OD"), "Exact : " + V("AB") + " = " + V("OC") + " (ABCO est un parallélogramme), puis " + M(r"\overrightarrow{OC}+\overrightarrow{CD}=\overrightarrow{OD}") + "."),
             (0, V("AD"), V("AD") + " est deux fois trop long : c'est " + M(r"2\overrightarrow{OD}") + "."),
             (0, V("BD"), "Remplace d'abord " + V("AB") + " par un vecteur égal d'extrémité C."),
             (0, V("AC"), "Ce n'est pas la bonne direction.")],
    hints=["Pour utiliser Chasles, remplace " + V("AB") + " par un représentant qui <i>arrive</i> en C. Sur la figure, quel vecteur d'extrémité C est égal à " + V("AB") + " ?",
           "ABCO est un parallélogramme (côtés parallèles et de même longueur), donc " + V("AB") + " = " + V("OC") + ". " + relis("2.2", "chasles")],
    general="Dans l'hexagone régulier, ABCO est un parallélogramme donc " + V("AB") + " = " + V("OC") + ". Alors " + M(r"\overrightarrow{AB}+\overrightarrow{CD}=\overrightarrow{OC}+\overrightarrow{CD}=\overrightarrow{OD}") + " (on peut aussi répondre " + V("AO") + " ou " + V("FE") + ", qui lui sont égaux).<br>Pour t'entraîner : Feuille 2, Ex 15.")

add(C2, type="mc", name="B2-09 – Hexagone : OB + OE",
    text="ABCDEF est un hexagone régulier de centre O. Compléter : " + M(r"\overrightarrow{OB}+\overrightarrow{OE}=") + " …" + fig("hex", 260),
    answers=[(100, NUL, "Exact : E est le symétrique de B par rapport à O, donc " + V("OE") + " = " + M(r"-\overrightarrow{OB}") + "."),
             (0, V("BE"), "Regarde les sens : " + V("OB") + " et " + V("OE") + " sont opposés, leur somme est nulle."),
             (0, V("OD"), "Non : " + V("OB") + " et " + V("OE") + " ont la même direction et des sens contraires."),
             (0, M(r"2\overrightarrow{OB}"), "Ce serait " + M(r"\overrightarrow{OB}+\overrightarrow{OB}") + ".")],
    hints=["O est le milieu de [BE]. Que dire des vecteurs " + V("OB") + " et " + V("OE") + " ?", relis("1.3", "chasles")],
    general="O est le milieu de [BE], donc " + V("OE") + " = " + V("BO") + " = " + M(r"-\overrightarrow{OB}") + ". Ainsi " + M(r"\overrightarrow{OB}+\overrightarrow{OE}=\vec 0") + ".<br>Pour t'entraîner : Feuille 2, Ex 15 et 16.")

add(C2, type="mc", name="B2-10 – Hexagone : FO + DO",
    text="ABCDEF est un hexagone régulier de centre O. Compléter : " + M(r"\overrightarrow{FO}+\overrightarrow{DO}=") + " …" + fig("hex", 260),
    answers=[(100, V("OB"), "Exact : " + V("DO") + " = " + V("OA") + " et " + V("FO") + " = " + V("AB") + ", donc la somme vaut " + M(r"\overrightarrow{OA}+\overrightarrow{AB}=\overrightarrow{OB}") + "."),
             (0, V("OE"), "Sens opposé."),
             (0, V("FD"), "Ce n'est pas " + M(r"\overrightarrow{FO}+\overrightarrow{OD}") + " : attention, le second vecteur est " + V("DO") + "."),
             (0, V("AC"), "Mauvaise direction.")],
    hints=["Remplace " + V("DO") + " par " + V("OA") + " (O milieu de [DA]) et " + V("FO") + " par un vecteur égal qui part de A. Puis Chasles.", relis("2.3", "chasles")],
    general=V("DO") + " = " + V("OA") + " et " + V("FO") + " = " + V("AB") + " (FOBA est un parallélogramme). Donc " + M(r"\overrightarrow{FO}+\overrightarrow{DO}=\overrightarrow{AB}+\overrightarrow{OA}=\overrightarrow{OA}+\overrightarrow{AB}=\overrightarrow{OB}") + ". Autre méthode : méthode du parallélogramme avec les représentants " + V("OC") + " et " + V("OA") + ".<br>Pour t'entraîner : Feuille 2, Ex 15.")

add(C2, type="mc", name="B2-11 – Milieu et somme",
    text="ABC est un triangle et I est le milieu de [BC]. Compléter : " + M(r"\overrightarrow{AB}+\overrightarrow{AC}=") + " …",
    answers=[(100, M(r"2\overrightarrow{AI}"), "Exact : " + M(r"\overrightarrow{AB}+\overrightarrow{AC}=(\overrightarrow{AI}+\overrightarrow{IB})+(\overrightarrow{AI}+\overrightarrow{IC})=2\overrightarrow{AI}+\vec 0") + "."),
             (0, V("AI"), "Il manque un facteur 2 : chaque vecteur contient un " + V("AI") + "."),
             (0, V("BC"), M(r"\overrightarrow{BC}=\overrightarrow{AC}-\overrightarrow{AB}") + ", c'est une différence, pas une somme."),
             (0, M(r"2\overrightarrow{AB}"), "Les vecteurs " + V("AB") + " et " + V("AC") + " ne sont pas égaux.")],
    hints=["Décompose chaque vecteur en passant par I : " + M(r"\overrightarrow{AB}=\overrightarrow{AI}+\overrightarrow{IB}") + " et " + M(r"\overrightarrow{AC}=\overrightarrow{AI}+\overrightarrow{IC}") + ".",
           "I milieu de [BC] donne " + M(r"\overrightarrow{IB}+\overrightarrow{IC}=\vec 0") + ". " + relis("2.2", "chasles")],
    general=M(r"\overrightarrow{AB}+\overrightarrow{AC}=\overrightarrow{AI}+\overrightarrow{IB}+\overrightarrow{AI}+\overrightarrow{IC}=2\overrightarrow{AI}+(\overrightarrow{IB}+\overrightarrow{IC})=2\overrightarrow{AI}") + " car I est le milieu de [BC].<br>Pour t'entraîner : Feuille 2, Ex 16 ; Feuille 3¾, encadré Méthode.")

add(C2, type="mc", name="B2-12 – Méthode du parallélogramme",
    text="On a " + M(r"\vec u=\overrightarrow{MN}") + " et " + M(r"\vec v=\overrightarrow{MP}") + ". On construit le point Q tel que MNQP soit un parallélogramme. Alors " + M(r"\vec u+\vec v=") + " …",
    answers=[(100, V("MQ"), "Exact : c'est la diagonale du parallélogramme issue de M."),
             (0, V("NP"), "C'est " + M(r"\vec v-\vec u") + " (l'autre diagonale)."),
             (0, V("PN"), "C'est " + M(r"\vec u-\vec v") + "."),
             (0, V("QM"), "Sens opposé : la somme part de l'origine commune M.")],
    hints=["MNQP parallélogramme donne " + V("NQ") + " = " + V("MP") + " = " + v("v") + ". Puis Chasles : " + M(r"\overrightarrow{MN}+\overrightarrow{NQ}") + ".", relis("2.3", "somme")],
    general="Avec une origine commune M, la somme est la diagonale du parallélogramme : " + M(r"\vec u+\vec v=\overrightarrow{MN}+\overrightarrow{NQ}=\overrightarrow{MQ}") + " (§ 2.3).<br>Pour t'entraîner : Feuille 2, Ex 13 ; " + capy("somme") + ".")

add(C2, type="mc", name="B2-13 – Ordre dans une somme",
    text="Vrai ou faux : pour tous vecteurs " + v("u") + " et " + v("v") + ", on a " + M(r"\vec u+\vec v=\vec v+\vec u") + ".",
    answers=[(100, "Vrai", "Exact : l'ordre n'a pas d'importance (c'est visible sur le parallélogramme)."),
             (0, "Faux", "L'ordre n'a pas d'importance : les deux chemins bout à bout arrivent au même point (parallélogramme).")],
    hints=["Construis les deux sommes bout à bout à partir du même point : où arrive-t-on ?", relis("2.1", "somme")],
    general="« À noter » du § 2.1 : l'ordre dans une somme de vecteurs n'a pas d'importance. Attention, ce n'est pas le cas pour une différence : " + M(r"\vec u-\vec v=-(\vec v-\vec u)") + ".")

add(C2, type="cloze", name="B2-14 – Compléter avec Chasles",
    text="Compléter chaque égalité avec <b>la lettre</b> du point qui convient (relation de Chasles).<br>" +
         "<p>" + M(r"\overrightarrow{AB}+\overrightarrow{B\,?}=\overrightarrow{AC}") + " → {1:SHORTANSWER:=C#Exact.~%0%A#Il faut arriver en C.}</p>" +
         "<p>" + M(r"\overrightarrow{MN}=\overrightarrow{M\,?}+\overrightarrow{KN}") + " → {1:SHORTANSWER:=K#Exact : on passe par K.~%0%N#La lettre du milieu doit être la même dans les deux vecteurs.}</p>" +
         "<p>" + M(r"\overrightarrow{?\,S}+\overrightarrow{SR}=\overrightarrow{TR}") + " → {1:SHORTANSWER:=T#Exact.~%0%R#Le point de départ est T.}</p>",
    hints=["Dans " + M(r"\overrightarrow{AM}+\overrightarrow{MB}=\overrightarrow{AB}") + ", la lettre du milieu apparaît deux fois et disparaît dans le résultat.", relis("2.2", "chasles")],
    general="Relation de Chasles : " + M(r"\overrightarrow{AB}+\overrightarrow{BC}=\overrightarrow{AC}") + ", " + M(r"\overrightarrow{MN}=\overrightarrow{MK}+\overrightarrow{KN}") + ", " + M(r"\overrightarrow{TS}+\overrightarrow{SR}=\overrightarrow{TR}") + ".<br>Pour t'entraîner : Feuille 2, Ex 14 ; manuel Ex 42 p. 187.")

add(C2, type="mc", name="B2-15 – Construction bout à bout",
    text="Pour construire " + M(r"\vec u+\vec v") + " par la méthode « bout à bout », on place l'origine de " + v("v") + "…",
    answers=[(100, "à l'extrémité de " + v("u") + ".", "Exact : le vecteur somme va alors de l'origine de " + v("u") + " à l'extrémité de " + v("v") + "."),
             (0, "à l'origine de " + v("u") + ".", "C'est le point de départ de la méthode du parallélogramme, pas du bout à bout."),
             (0, "n'importe où.", "Il faut enchaîner les deux déplacements : " + v("v") + " commence là où " + v("u") + " finit."),
             (0, "au milieu de " + v("u") + ".", "Non : on enchaîne les déplacements, le second commence à la fin du premier.")],
    hints=["La somme correspond à l'<i>enchaînement</i> des deux translations : d'abord " + v("u") + ", puis " + v("v") + ".", relis("2.1", "somme")],
    general="Méthode bout à bout (§ 2.1) : on construit N tel que " + V("MN") + " = " + v("u") + ", puis P tel que " + V("NP") + " = " + v("v") + " ; alors " + M(r"\vec u+\vec v=\overrightarrow{MP}") + ".<br>Pour t'entraîner : Feuille 2, Ex 13 ; " + capy("somme") + ".")

# ======================= BLOC 3 =======================
def kq(name, figname, k, ktext, hint_extra):
    add(C3, type="num", name=name,
        text="Les points A, B et C sont placés sur une droite graduée (les graduations sont régulières). On a " + M(r"\overrightarrow{AC}=k\,\overrightarrow{AB}") + ". Donner la valeur de " + M("k") + ".<br><i>Si besoin, écrire le nombre avec une virgule (par exemple 1,5).</i>" + fig(figname, 440),
        answers=[(100, str(k), "Exact : " + ktext)],
        hints=["Compare d'abord les <b>sens</b> de " + V("AB") + " et " + V("AC") + " (signe de k), puis les <b>longueurs</b> : AC vaut combien de fois AB ? " + hint_extra, relis("3", "produit")],
        general=ktext + "<br>Pour t'entraîner : Feuille 3, Ex 1 et 2 ; manuel Ex 18, 19 p. 207.")

kq("B3-01 – Coefficient k (même sens)", "b3a1", 3, "AB = 2 graduations, AC = 6 graduations, même sens : " + M(r"k=\dfrac{6}{2}=3") + ".", "")
kq("B3-02 – Coefficient k (sens opposé)", "b3a2", -2, "AB = 2 graduations, AC = 4 graduations, sens opposés : " + M(r"k=-\dfrac{4}{2}=-2") + ".", "Ici les vecteurs sont de sens contraires : k est négatif.")
kq("B3-03 – Coefficient k (plus court)", "b3a3", 0.5, "AB = 4 graduations, AC = 2 graduations, même sens : " + M(r"k=\dfrac{2}{4}=0{,}5") + ".", "Ici AC est plus court que AB : k est entre 0 et 1.")

add(C3, type="mc", name="B3-04 – Coefficient k (fraction négative)",
    text="Les points A, B et C sont placés sur une droite graduée. On a " + M(r"\overrightarrow{AC}=k\,\overrightarrow{AB}") + ". Que vaut " + M("k") + " ?" + fig("b3a4", 440),
    answers=[(100, M(r"k=-\dfrac{2}{3}"), "Exact : sens opposés, et AC = 2 graduations pour AB = 3 graduations."),
             (0, M(r"k=\dfrac{2}{3}"), "La longueur est bonne, mais les vecteurs sont de sens contraires : k est négatif."),
             (0, M(r"k=-\dfrac{3}{2}"), "C'est AB qui vaut 3 graduations et AC qui en vaut 2 : " + M(r"AC=\dfrac{2}{3}AB") + "."),
             (0, M(r"k=-2"), "k n'est pas la longueur AC, c'est le rapport " + M(r"\dfrac{AC}{AB}") + ".")],
    hints=["Signe : les vecteurs sont-ils de même sens ? Valeur : " + M(r"\dfrac{AC}{AB}") + ".", relis("3", "produit")],
    general=V("AC") + " et " + V("AB") + " sont de sens contraires, et " + M(r"AC=\dfrac{2}{3}AB") + ". Donc " + M(r"\overrightarrow{AC}=-\dfrac{2}{3}\overrightarrow{AB}") + ".<br>Pour t'entraîner : Feuille 3, Ex 1 (cas 3 à 6).")

add(C3, type="mc", name="B3-05 – Lire v = −2u",
    text="On sait que " + M(r"\vec v=-2\,\vec u") + " (avec " + v("u") + " non nul). Alors le vecteur " + v("v") + "…",
    answers=[(100, "a la même direction que " + v("u") + ", le sens opposé, et une norme double.", "Exact."),
             (0, "a la même direction et le même sens que " + v("u") + ", et une norme double.", "Le coefficient est négatif : le sens est opposé."),
             (0, "a la même direction que " + v("u") + ", le sens opposé, et une norme moitié.", "|−2| = 2 : la norme est multipliée par 2, pas divisée."),
             (0, "n'a pas la même direction que " + v("u") + ".", "Multiplier par un réel ne change jamais la direction.")],
    hints=["Le signe de k donne le sens, |k| donne le rapport des normes. La direction ne change jamais.", relis("3", "produit")],
    general="Définition du § 3 : " + M(r"k\vec u") + " a la même direction que " + v("u") + " ; même sens si k > 0, sens contraire si k < 0 ; norme |k| fois celle de " + v("u") + ".<br>Pour t'entraîner : Exemple 6 du cours (page 5) ; Feuille 3, Ex 2.")

def mq(name, expr, val, sol):
    add(C3, type="num", name=name,
        text="A et B sont deux points. Déterminer le réel " + M(expr[0]) + " tel que " + M(expr[1]) + ".<br><i>Si besoin, écrire le nombre avec une virgule.</i>",
        answers=[(100, str(val), "Exact : " + sol)],
        hints=["Remplace " + V("BA") + " par " + M(r"-\overrightarrow{AB}") + " s'il apparaît, puis regroupe les coefficients devant " + V("AB") + " comme en calcul littéral.", relis("3", "produit")],
        general=sol + "<br>Pour t'entraîner : Feuille 3, Ex 3 ; manuel Ex 41, 42 p. 208.")

mq("B3-06 – Coefficient m", ("m", r"3\overrightarrow{AB}+\dfrac12\overrightarrow{AB}=m\,\overrightarrow{AB}"), 3.5, M(r"3+\dfrac12=\dfrac72=3{,}5") + ", donc m = 3,5.")
mq("B3-07 – Coefficient n", ("n", r"2\,(3\,\overrightarrow{BA})=n\,\overrightarrow{AB}"), -6, M(r"2\times3\,\overrightarrow{BA}=6\,\overrightarrow{BA}=-6\,\overrightarrow{AB}") + ", donc n = −6.")
mq("B3-08 – Coefficient p", ("p", r"2\overrightarrow{AB}-\overrightarrow{BA}=p\,\overrightarrow{AB}"), 3, M(r"-\overrightarrow{BA}=+\overrightarrow{AB}") + ", donc " + M(r"2\overrightarrow{AB}+\overrightarrow{AB}=3\overrightarrow{AB}") + " : p = 3.")
mq("B3-09 – Coefficient q", ("q", r"3\overrightarrow{BA}-4\overrightarrow{AB}=q\,\overrightarrow{AB}"), -7, M(r"3\overrightarrow{BA}=-3\overrightarrow{AB}") + ", donc " + M(r"-3\overrightarrow{AB}-4\overrightarrow{AB}=-7\overrightarrow{AB}") + " : q = −7.")

add(C3, type="mc", name="B3-10 – Reconnaître des vecteurs colinéaires",
    text="Sur le quadrillage ci-dessous, quels vecteurs sont colinéaires ?" + fig("b3b", 400),
    answers=[(100, v("u") + " et " + v("v"), "Exact : " + M(r"\vec v=-2\,\vec u") + " (4 vers la gauche et 2 vers le bas, contre 2 vers la droite et 1 vers le haut)."),
             (0, v("u") + " et " + v("w"), "Non : " + v("u") + " monte de 1 pour 2 vers la droite, " + v("w") + " monte de 3 pour 4 vers la droite. Les pentes sont différentes."),
             (0, v("v") + " et " + v("w"), "Non : ils n'ont pas la même direction."),
             (0, "Aucun.", "Si : deux des trois vecteurs ont la même direction. Cherche un réel k tel que l'un soit k fois l'autre.")],
    hints=["Deux vecteurs sont colinéaires s'ils ont la même direction, c'est-à-dire s'il existe un réel k tel que l'un soit égal à k fois l'autre. Compare les déplacements (droite / haut).", relis("4", "colineaires")],
    general=v("u") + " : 2 vers la droite, 1 vers le haut ; " + v("v") + " : 4 vers la gauche, 2 vers le bas. Donc " + M(r"\vec v=-2\,\vec u") + " : ils sont colinéaires. " + v("w") + " (4 vers la droite, 3 vers le haut) n'est colinéaire à aucun des deux.<br>Pour t'entraîner : Exemple 9 du cours (page 6) ; " + capy("colinearite") + ".")

add(C3, type="mc", name="B3-11 – Vecteur nul et colinéarité",
    text="Vrai ou faux : le vecteur nul est colinéaire à n'importe quel vecteur.",
    answers=[(100, "Vrai", "Exact : " + M(r"\vec 0=0\times\vec u") + "."),
             (0, "Faux", "Si : " + M(r"\vec 0=0\times\vec u") + " pour tout vecteur " + v("u") + " (« À noter » du § 4).")],
    hints=["Cherche un réel k tel que " + M(r"\vec 0=k\,\vec u") + ".", relis("4")],
    general="Pour tout vecteur " + v("u") + ", " + M(r"\vec 0=0\times\vec u") + " : le vecteur nul est colinéaire à tout vecteur (« À noter » du § 4).")

add(C3, type="mc", name="B3-12 – De la colinéarité à l'alignement",
    text="A, B, C sont trois points distincts tels que " + M(r"\overrightarrow{AB}=\dfrac35\,\overrightarrow{AC}") + ". Que peut-on en déduire ?",
    answers=[(100, "Les points A, B et C sont alignés.", "Exact : " + V("AB") + " et " + V("AC") + " sont colinéaires et ont le point A en commun."),
             (0, "Les droites (AB) et (AC) sont parallèles et distinctes.", "Elles ont le point A en commun : elles sont confondues, donc les points sont alignés."),
             (0, "B est le milieu de [AC].", "Ce serait le cas avec le coefficient " + M(r"\dfrac12") + ", pas " + M(r"\dfrac35") + "."),
             (0, V("AB") + " = " + V("AC"), "Le coefficient est " + M(r"\dfrac35") + ", pas 1.")],
    hints=["Deux vecteurs " + V("AB") + " et " + V("AC") + " colinéaires, avec la même origine A : que dire des points A, B, C ?", relis("4b", "colineaires")],
    general="Propriété 5 (§ 4) : A, B, C alignés ⟺ " + V("AB") + " et " + V("AC") + " colinéaires. Ici " + M(r"\overrightarrow{AB}=\dfrac35\overrightarrow{AC}") + " donc les points sont alignés (Exemple 11 du cours, page 7).<br>Pour t'entraîner : Feuille 3¾, Ex 1 et 4.")

add(C3, type="mc", name="B3-13 – De la colinéarité au parallélisme",
    text="A, B, C, D sont quatre points tels que " + V("AB") + " et " + V("CD") + " sont colinéaires (et non nuls). Que peut-on en déduire ?",
    answers=[(100, "Les droites (AB) et (CD) sont parallèles (ou confondues).", "Exact : c'est la Propriété 4 du § 4."),
             (0, "Les points A, B, C et D sont alignés.", "Seulement si les droites sont confondues. En général elles sont parallèles et distinctes."),
             (0, "ABCD est un parallélogramme.", "Il faudrait en plus " + V("AB") + " = " + V("DC") + " (même norme et même sens)."),
             (0, V("AB") + " = " + V("CD"), "Colinéaires ne veut pas dire égaux : les normes et les sens peuvent différer.")],
    hints=["Colinéaires = même direction. Deux droites qui ont la même direction sont…", relis("4b", "colineaires")],
    general="Propriété 4 (§ 4) : " + V("AB") + " et " + V("CD") + " colinéaires ⟺ (AB) ∥ (CD) (ou confondues).<br>Pour t'entraîner : Feuille 3¾, Ex 2 et 3.")

add(C3, type="mc", name="B3-14 – Montrer une colinéarité",
    text="Pour démontrer que deux vecteurs " + v("u") + " et " + v("v") + " (non nuls) sont colinéaires, il suffit de…",
    answers=[(100, "trouver un réel k tel que " + M(r"\vec v=k\,\vec u") + ".", "Exact : c'est la définition."),
             (0, "vérifier qu'ils ont la même norme.", "Deux vecteurs de même norme peuvent avoir des directions différentes."),
             (0, "vérifier qu'ils ont le même sens.", "Le sens ne suffit pas et n'est même pas nécessaire (k peut être négatif)."),
             (0, "montrer que " + M(r"\vec u+\vec v=\vec 0") + ".", "Cela montre que " + M(r"\vec v=-\vec u") + " : c'est un cas particulier, mais ce n'est pas nécessaire.")],
    hints=["Relis la définition : « il existe un réel k tel que… ».", relis("4", "colineaires")],
    general="Définition (§ 4) : " + v("u") + " et " + v("v") + " sont colinéaires s'il existe un réel k tel que " + M(r"\vec v=k\vec u") + " (ou " + M(r"\vec u=k\vec v") + "). En pratique on exprime les deux vecteurs en fonction des mêmes vecteurs, puis on cherche k (encadré Méthode, Feuille 3¾).")

add(C3, type="mc", name="B3-15 – Trouver k dans une démonstration (★★★)",
    text="ABC est un triangle, M et N sont définis par " + M(r"\overrightarrow{BM}=2\,\overrightarrow{AC}") + " et " + M(r"\overrightarrow{AN}=\dfrac12\,\overrightarrow{BC}") + ". On a montré que " +
         M(r"\overrightarrow{CM}=\overrightarrow{CB}+2\,\overrightarrow{AC}") + " et " + M(r"\overrightarrow{CN}=-\dfrac12\,\overrightarrow{CB}-\overrightarrow{AC}") + ".<br>Quel réel k vérifie " + M(r"\overrightarrow{CM}=k\,\overrightarrow{CN}") + " ?",
    answers=[(100, M("k=-2"), "Exact : " + M(r"-2\left(-\dfrac12\overrightarrow{CB}-\overrightarrow{AC}\right)=\overrightarrow{CB}+2\overrightarrow{AC}=\overrightarrow{CM}") + ". Donc C, M, N sont alignés."),
             (0, M("k=2"), "Vérifie le signe : " + M(r"2\overrightarrow{CN}=-\overrightarrow{CB}-2\overrightarrow{AC}") + ", ce n'est pas " + V("CM") + "."),
             (0, M(r"k=-\dfrac12"), "C'est le rapport dans l'autre sens : " + M(r"\overrightarrow{CN}=-\dfrac12\overrightarrow{CM}") + ", donc " + M(r"\overrightarrow{CM}=-2\overrightarrow{CN}") + "."),
             (0, M(r"k=\dfrac12"), "Compare les coefficients devant " + V("CB") + " : 1 dans " + V("CM") + ", " + M(r"-\dfrac12") + " dans " + V("CN") + ".")],
    hints=["Compare les coefficients devant " + V("CB") + " : 1 d'un côté, " + M(r"-\dfrac12") + " de l'autre. Par quoi multiplier " + M(r"-\dfrac12") + " pour obtenir 1 ? Vérifie ensuite avec " + V("AC") + ".", relis("M", "colineaires")],
    general=M(r"\overrightarrow{CM}=-2\,\overrightarrow{CN}") + " : les vecteurs sont colinéaires, donc les points C, M et N sont alignés (Feuille 3¾, Ex 1).<br>Pour t'entraîner : Feuille 3¾, Ex 1 à 4.")

# ======================= BLOC 4 =======================
def w_opts(correct, feeds):
    return [(100 if i == 0 else 0, t, f) for i, (t, f) in enumerate(feeds)]

add(C4, type="mc", name="B4-01 – Décomposer w1",
    text="Exprimer " + M(r"\vec{w_1}") + " en fonction de " + v("u") + " et " + v("v") + "." + fig("b4a", 460),
    answers=[(100, M(r"\vec{w_1}=2\vec u+\vec v"), "Exact : 2 fois (2 à droite, 1 en haut) plus (1 à gauche, 1 en haut) donne (3 à droite, 3 en haut)."),
             (0, M(r"\vec{w_1}=\vec u+2\vec v"), "Vérifie : " + M(r"\vec u+2\vec v") + " donnerait 0 carreau horizontal."),
             (0, M(r"\vec{w_1}=2\vec u-\vec v"), M(r"2\vec u-\vec v") + " donnerait 5 vers la droite et 1 vers le haut."),
             (0, M(r"\vec{w_1}=-2\vec u+\vec v"), "Sens opposé pour " + v("u") + ".")],
    hints=["Compte les carreaux : " + v("u") + " = (2 à droite, 1 en haut), " + v("v") + " = (1 à gauche, 1 en haut). Cherche a et b tels que a" + v("u") + " + b" + v("v") + " donne le déplacement de " + M(r"\vec{w_1}") + ".", relis("4", "exprimer")],
    general=M(r"\vec{w_1}") + " : 3 à droite, 3 en haut. " + M(r"2\vec u+\vec v") + " : (4 − 1 = 3 à droite, 2 + 1 = 3 en haut). Donc " + M(r"\vec{w_1}=2\vec u+\vec v") + ".<br>Pour t'entraîner : Feuille 3, Ex 4 et 5.")

add(C4, type="mc", name="B4-02 – Décomposer w2",
    text="Exprimer " + M(r"\vec{w_2}") + " en fonction de " + v("u") + " et " + v("v") + "." + fig("b4a", 460),
    answers=[(100, M(r"\vec{w_2}=\vec u-2\vec v"), "Exact : (2 à droite, 1 en haut) − 2 × (1 à gauche, 1 en haut) = (4 à droite, 1 en bas)."),
             (0, M(r"\vec{w_2}=\vec u+2\vec v"), "Avec + 2" + v("v") + " on monterait de 3 carreaux ; or " + M(r"\vec{w_2}") + " descend."),
             (0, M(r"\vec{w_2}=2\vec u-\vec v"), "Cela donnerait 5 vers la droite et 1 vers le haut."),
             (0, M(r"\vec{w_2}=-\vec u-2\vec v"), "Sens opposé pour " + v("u") + ".")],
    hints=["" + M(r"\vec{w_2}") + " descend légèrement : il faut « retirer » du " + v("v") + ", donc un coefficient négatif devant " + v("v") + ".", relis("4", "exprimer")],
    general=M(r"\vec{w_2}") + " : 4 à droite, 1 en bas. " + M(r"\vec u-2\vec v") + " : (2 + 2 = 4 à droite, 1 − 2 = −1 soit 1 en bas). Donc " + M(r"\vec{w_2}=\vec u-2\vec v") + ".<br>Pour t'entraîner : Feuille 3, Ex 4 et 5.")

add(C4, type="mc", name="B4-03 – Décomposer w3",
    text="Exprimer " + M(r"\vec{w_3}") + " en fonction de " + v("u") + " et " + v("v") + "." + fig("b4a", 460),
    answers=[(100, M(r"\vec{w_3}=-\vec u+\vec v"), "Exact : (2 à gauche, 1 en bas) + (1 à gauche, 1 en haut) = (3 à gauche, 0)."),
             (0, M(r"\vec{w_3}=\vec u-\vec v"), "C'est l'opposé : " + M(r"\vec u-\vec v") + " va vers la droite."),
             (0, M(r"\vec{w_3}=\vec u+\vec v"), "Cela donnerait 1 à droite et 2 en haut."),
             (0, M(r"\vec{w_3}=-\vec u-\vec v"), "Cela donnerait 1 à gauche et 2 en bas.")],
    hints=[M(r"\vec{w_3}") + " est horizontal : les déplacements verticaux de a" + v("u") + " et b" + v("v") + " doivent se compenser.", relis("4", "exprimer")],
    general=M(r"\vec{w_3}") + " : 3 à gauche, 0 en hauteur. " + M(r"-\vec u+\vec v") + " : (−2 − 1 = −3, −1 + 1 = 0). Donc " + M(r"\vec{w_3}=-\vec u+\vec v") + ".<br>Pour t'entraîner : Feuille 3, Ex 5 et 6.")

add(C4, type="mc", name="B4-04 – Parallélogramme et milieu",
    text="ABCD est un parallélogramme et I est le milieu de [CD]. On pose " + M(r"\vec u=\overrightarrow{AB}") + " et " + M(r"\vec v=\overrightarrow{AD}") + ". Exprimer " + V("AI") + " en fonction de " + v("u") + " et " + v("v") + "." + fig("b4b", 340),
    answers=[(100, M(r"\overrightarrow{AI}=\vec v+\dfrac12\vec u"), "Exact : " + M(r"\overrightarrow{AI}=\overrightarrow{AD}+\overrightarrow{DI}") + " avec " + M(r"\overrightarrow{DI}=\dfrac12\overrightarrow{DC}=\dfrac12\overrightarrow{AB}") + "."),
             (0, M(r"\overrightarrow{AI}=\vec u+\dfrac12\vec v"), "Tu as inversé les rôles : I est sur [DC], qui est parallèle à [AB] (" + v("u") + ")."),
             (0, M(r"\overrightarrow{AI}=\dfrac12(\vec u+\vec v)"), "Ce serait le vecteur " + V("AO") + " avec O le centre du parallélogramme."),
             (0, M(r"\overrightarrow{AI}=\vec u+\vec v"), "C'est " + V("AC") + " : I n'est pas en C.")],
    hints=["Chasles en passant par D : " + M(r"\overrightarrow{AI}=\overrightarrow{AD}+\overrightarrow{DI}") + ". Puis " + V("DI") + " = ½ " + V("DC") + " et " + V("DC") + " = " + V("AB") + ".", relis("4", "exprimer")],
    general=M(r"\overrightarrow{AI}=\overrightarrow{AD}+\overrightarrow{DI}=\vec v+\dfrac12\overrightarrow{DC}=\vec v+\dfrac12\overrightarrow{AB}=\vec v+\dfrac12\vec u") + " (Feuille 3, Ex 7).<br>Pour t'entraîner : Feuille 3, Ex 6 et 7 ; manuel Ex 45 p. 209.")

def hexq(name, target, correct, wrongs, sol):
    answers = [(100, M(r"\overrightarrow{%s}=%s" % (target, correct)), "Exact.")] + [(0, M(r"\overrightarrow{%s}=%s" % (target, w)), f) for w, f in wrongs]
    add(C4, type="mc", name=name,
        text="ABCDEF est un hexagone régulier de centre O. On pose " + M(r"\vec u=\overrightarrow{OA}") + " et " + M(r"\vec v=\overrightarrow{OB}") + ". Exprimer " + V(target) + " en fonction de " + v("u") + " et " + v("v") + "." + fig("hex_uv", 260),
        answers=answers,
        hints=["Utilise la relation de Chasles en passant par O, puis remplace chaque vecteur " + V("OX") + " par " + M(r"\pm\vec u") + " ou " + M(r"\pm\vec v") + " (O est le milieu de [AD], [BE], [CF] et ABCO est un parallélogramme).", relis("4", "exprimer")],
        general=sol + "<br>Pour t'entraîner : Feuille 3, Ex 8 ; Feuille 2, Ex 15.")

hexq("B4-05 – Hexagone : OD", "OD", r"-\vec u", [(r"\vec u", "O est le milieu de [AD] : " + V("OD") + " est l'opposé de " + V("OA") + "."), (r"\vec v", "D n'est pas sur (OB)."), (r"-\vec v", "D est le symétrique de A, pas de B.")],
     "O est le milieu de [AD], donc " + M(r"\overrightarrow{OD}=-\overrightarrow{OA}=-\vec u") + ".")
hexq("B4-06 – Hexagone : OC", "OC", r"\vec v-\vec u", [(r"\vec u-\vec v", "Sens opposé : " + M(r"\vec u-\vec v=\overrightarrow{BA}") + "."), (r"\vec u+\vec v", "Cela donnerait un vecteur vers la droite, or C est à gauche de B."), (r"-\vec v", "C n'est pas le symétrique de B par rapport à O (c'est E).")],
     "ABCO est un parallélogramme, donc " + M(r"\overrightarrow{OC}=\overrightarrow{AB}=\overrightarrow{AO}+\overrightarrow{OB}=-\vec u+\vec v=\vec v-\vec u") + ".")
hexq("B4-07 – Hexagone : DB", "DB", r"\vec u+\vec v", [(r"\vec u-\vec v", "Vérifie le signe devant " + v("v") + " : " + V("OB") + " = +" + v("v") + "."), (r"\vec v-\vec u", "C'est " + V("OC") + " (ou " + V("AB") + ")."), (r"2\vec v", "D n'est pas sur (OB).")],
     M(r"\overrightarrow{DB}=\overrightarrow{DO}+\overrightarrow{OB}=\vec u+\vec v") + " car " + V("DO") + " = " + V("OA") + " = " + v("u") + " (exemple de la Feuille 3, Ex 8).")
hexq("B4-08 – Hexagone : AB", "AB", r"\vec v-\vec u", [(r"\vec u-\vec v", "Sens opposé : c'est " + V("BA") + "."), (r"\vec u+\vec v", "C'est " + V("DB") + ", pas " + V("AB") + "."), (r"-\vec u-\vec v", "C'est " + V("BD") + ".")],
     M(r"\overrightarrow{AB}=\overrightarrow{AO}+\overrightarrow{OB}=-\vec u+\vec v=\vec v-\vec u") + ".")

add(C4, type="mc", single=False, name="B4-09 – Caractérisations du milieu",
    text="A et B sont deux points distincts. Cocher <b>toutes</b> les affirmations équivalentes à : « I est le milieu de [AB] ».",
    answers=[(33.33333, V("AI") + " = " + V("IB"), "Oui : même direction, même sens, même norme."),
             (33.33333, M(r"\overrightarrow{IA}+\overrightarrow{IB}=\vec 0"), "Oui : " + V("IA") + " et " + V("IB") + " sont opposés."),
             (33.33333, M(r"\overrightarrow{AI}=\dfrac12\,\overrightarrow{AB}"), "Oui : I est sur [AB], à mi-chemin."),
             (-50, V("AI") + " = " + V("AB"), "Non : cela signifie I = B."),
             (-50, V("IA") + " = " + V("IB"), "Non : cela signifie A = B, impossible.")],
    hints=["Traduis chaque égalité avec direction, sens et norme. Par exemple " + V("IA") + " = " + V("IB") + " voudrait dire que A et B sont au même endroit.", relis("M", "egalite")],
    general="Encadré Méthode (Feuille 3¾) : I milieu de [AB] ⟺ " + V("AI") + " = " + V("IB") + " ⟺ " + M(r"\overrightarrow{IA}+\overrightarrow{IB}=\vec 0") + " ⟺ " + M(r"\overrightarrow{AI}=\dfrac12\overrightarrow{AB}") + ".<br>Pour t'entraîner : Feuille 2, Ex 16 ; Feuille 3¾, Ex 5.")

add(C4, type="mc", name="B4-10 – Milieu et point quelconque",
    text="I est le milieu de [AB] et M est un point quelconque du plan. Compléter : " + M(r"\overrightarrow{MA}+\overrightarrow{MB}=") + " …",
    answers=[(100, M(r"2\,\overrightarrow{MI}"), "Exact : " + M(r"(\overrightarrow{MI}+\overrightarrow{IA})+(\overrightarrow{MI}+\overrightarrow{IB})=2\overrightarrow{MI}+\vec 0") + "."),
             (0, V("MI"), "Il manque un facteur 2."),
             (0, V("AB"), M(r"\overrightarrow{AB}=\overrightarrow{MB}-\overrightarrow{MA}") + " : c'est une différence."),
             (0, M(r"2\,\overrightarrow{AB}"), "Non : la somme de deux vecteurs partant de M part encore de M.")],
    hints=["Chasles en passant par I dans chacun des deux vecteurs, puis utilise " + M(r"\overrightarrow{IA}+\overrightarrow{IB}=\vec 0") + ".", relis("M", "chasles")],
    general=M(r"\overrightarrow{MA}+\overrightarrow{MB}=\overrightarrow{MI}+\overrightarrow{IA}+\overrightarrow{MI}+\overrightarrow{IB}=2\overrightarrow{MI}") + " car I est le milieu de [AB]. C'est la même démonstration que pour " + M(r"\overrightarrow{AB}+\overrightarrow{AC}=2\overrightarrow{AI}") + " (Bloc 2).")

add(C4, type="mc", name="B4-11 – Exprimer MN (parallélisme)",
    text="ABC est un triangle. M et N sont définis par " + M(r"\overrightarrow{AM}=-\dfrac12\,\overrightarrow{AB}") + " et " + M(r"\overrightarrow{AN}=-\dfrac12\,\overrightarrow{AC}") + ". Exprimer " + V("MN") + " en fonction de " + V("BC") + ".",
    answers=[(100, M(r"\overrightarrow{MN}=-\dfrac12\,\overrightarrow{BC}"), "Exact : " + M(r"\overrightarrow{MN}=\overrightarrow{MA}+\overrightarrow{AN}=\dfrac12\overrightarrow{AB}-\dfrac12\overrightarrow{AC}=\dfrac12\overrightarrow{CB}=-\dfrac12\overrightarrow{BC}") + "."),
             (0, M(r"\overrightarrow{MN}=\dfrac12\,\overrightarrow{BC}"), "Vérifie le signe : " + M(r"\dfrac12(\overrightarrow{AB}-\overrightarrow{AC})=\dfrac12\overrightarrow{CB}") + "."),
             (0, M(r"\overrightarrow{MN}=-2\,\overrightarrow{BC}"), "Les coefficients sont ½, pas 2 : MN est deux fois plus court que BC."),
             (0, M(r"\overrightarrow{MN}=\overrightarrow{BC}"), "M et N sont à mi-distance : la norme est divisée par 2.")],
    hints=["Chasles en passant par A : " + M(r"\overrightarrow{MN}=\overrightarrow{MA}+\overrightarrow{AN}") + ". Attention : " + M(r"\overrightarrow{MA}=-\overrightarrow{AM}=+\dfrac12\overrightarrow{AB}") + ".",
           "Factorise par ½ : " + M(r"\dfrac12(\overrightarrow{AB}-\overrightarrow{AC})") + ", puis " + M(r"\overrightarrow{AB}-\overrightarrow{AC}=\overrightarrow{AB}+\overrightarrow{CA}=\overrightarrow{CB}") + ". " + relis("M", "exprimer")],
    general=M(r"\overrightarrow{MN}=\overrightarrow{MA}+\overrightarrow{AN}=\dfrac12\overrightarrow{AB}-\dfrac12\overrightarrow{AC}=\dfrac12(\overrightarrow{AB}-\overrightarrow{AC})=\dfrac12\overrightarrow{CB}=-\dfrac12\overrightarrow{BC}") + " (Feuille 3¾, Ex 3).")

add(C4, type="mc", name="B4-12 – Conclure une démonstration",
    text="On a démontré que " + M(r"\overrightarrow{MN}=-\dfrac12\,\overrightarrow{BC}") + " (avec M, N, B, C quatre points distincts). Que peut-on conclure ?",
    answers=[(100, "Les droites (MN) et (BC) sont parallèles.", "Exact : les vecteurs sont colinéaires, donc les droites sont parallèles (ou confondues)."),
             (0, "Les points M, N, B et C sont alignés.", "Colinéarité de " + V("MN") + " et " + V("BC") + " donne le parallélisme, pas l'alignement (les droites peuvent être distinctes)."),
             (0, "MNBC est un parallélogramme.", "Il faudrait " + V("MN") + " = " + V("CB") + " ; ici les normes sont différentes."),
             (0, "N est le milieu de [MB].", "Rien ne l'indique : l'égalité ne relie pas N et le segment [MB].")],
    hints=["Propriété 4 du § 4 : deux vecteurs colinéaires ⟺ droites parallèles.", relis("4b", "colineaires")],
    general=V("MN") + " = " + M(r"-\dfrac12\overrightarrow{BC}") + " : les vecteurs sont colinéaires, donc (MN) ∥ (BC) (Propriété 4). Pour de l'alignement il faudrait deux vecteurs colinéaires ayant un point commun (Propriété 5).<br>Pour t'entraîner : Feuille 3¾, Ex 2 et 3.")

add(C4, type="mc", name="B4-13 – Points alignés (★★★)",
    text="ABCD est un parallélogramme, " + M(r"\overrightarrow{BE}=\dfrac12\,\overrightarrow{BC}") + " et " + M(r"\overrightarrow{DF}=2\,\overrightarrow{DC}") + ". On a établi " + M(r"\overrightarrow{AE}=\overrightarrow{AB}+\dfrac12\overrightarrow{AD}") + " et " + M(r"\overrightarrow{AF}=2\,\overrightarrow{AB}+\overrightarrow{AD}") + ".<br>Quel réel k vérifie " + M(r"\overrightarrow{AF}=k\,\overrightarrow{AE}") + ", et que peut-on en déduire ?",
    answers=[(100, M("k=2") + " ; les points A, E et F sont alignés.", "Exact : " + M(r"2\overrightarrow{AE}=2\overrightarrow{AB}+\overrightarrow{AD}=\overrightarrow{AF}") + ", et les deux vecteurs ont l'origine A en commun."),
             (0, M("k=2") + " ; les droites (AE) et (AF) sont parallèles et distinctes.", "Elles passent toutes les deux par A : elles sont confondues, les points sont alignés."),
             (0, M(r"k=\dfrac12") + " ; les points A, E et F sont alignés.", "C'est " + M(r"\overrightarrow{AE}=\dfrac12\overrightarrow{AF}") + " ; on demande " + M(r"\overrightarrow{AF}=k\overrightarrow{AE}") + ", donc k = 2."),
             (0, "Il n'existe pas de tel k.", "Si : compare les coefficients, ils sont proportionnels (1 et ½ contre 2 et 1).")],
    hints=["Compare les coefficients : (1 ; ½) pour " + V("AE") + " et (2 ; 1) pour " + V("AF") + ". Sont-ils proportionnels ?", relis("M", "colineaires")],
    general=M(r"\overrightarrow{AF}=2\overrightarrow{AE}") + " donc " + V("AE") + " et " + V("AF") + " sont colinéaires ; comme ils ont A pour origine commune, les points A, E et F sont alignés (Feuille 3¾, Ex 4, et " + capy("alignes") + ").")

add(C4, type="mc", name="B4-14 – Démontrer qu'un quadrilatère est un parallélogramme",
    text="Pour démontrer avec des vecteurs que le quadrilatère CDNM est un parallélogramme, il suffit de montrer que…",
    answers=[(100, V("CD") + " = " + V("MN"), "Exact : ABCD parallélogramme ⟺ " + V("AB") + " = " + V("DC") + " ; ici avec les sommets C, D, N, M dans l'ordre."),
             (0, V("CD") + " = " + V("NM"), "Mauvais sens : avec les sommets dans l'ordre C, D, N, M, c'est " + V("CD") + " = " + V("MN") + "."),
             (0, V("CN") + " = " + V("DM"), "Ce sont les diagonales : elles ne sont pas égales dans un parallélogramme."),
             (0, V("CD") + " et " + V("MN") + " sont colinéaires.", "Cela donne seulement (CD) ∥ (MN) ; il faut aussi même norme et même sens.")],
    hints=["Théorème du § 1.4 : ABCD est un parallélogramme ⟺ " + V("AB") + " = " + V("DC") + ". Renomme les sommets : A→C, B→D, C→N, D→M.", relis("1.4", "proprietes")],
    general="Avec les sommets dans l'ordre C, D, N, M : CDNM parallélogramme ⟺ " + V("CD") + " = " + V("MN") + " (ou de façon équivalente " + V("CM") + " = " + V("DN") + "). C'est la méthode du DS 1, Ex 4.")

add(C4, type="mc", name="B4-15 – Milieu par les vecteurs (★★★)",
    text="ABCD est un parallélogramme. E est le symétrique de A par rapport à B, F le symétrique de A par rapport à D. Exprimer " + V("CE") + " en fonction de " + V("AB") + " et " + V("AD") + ".",
    answers=[(100, M(r"\overrightarrow{CE}=\overrightarrow{AB}-\overrightarrow{AD}"), "Exact : " + M(r"\overrightarrow{CE}=\overrightarrow{CB}+\overrightarrow{BE}=-\overrightarrow{AD}+\overrightarrow{AB}") + ". De même " + M(r"\overrightarrow{CF}=\overrightarrow{AD}-\overrightarrow{AB}=-\overrightarrow{CE}") + " : C est le milieu de [EF]."),
             (0, M(r"\overrightarrow{CE}=\overrightarrow{AB}+\overrightarrow{AD}"), "Vérifie " + V("CB") + " : c'est " + M(r"-\overrightarrow{AD}") + " (car " + V("BC") + " = " + V("AD") + ")."),
             (0, M(r"\overrightarrow{CE}=\overrightarrow{AD}-\overrightarrow{AB}"), "C'est " + V("CF") + ", l'opposé de " + V("CE") + "."),
             (0, M(r"\overrightarrow{CE}=2\overrightarrow{AB}-\overrightarrow{AD}"), M(r"\overrightarrow{BE}=\overrightarrow{AB}") + " (E symétrique de A par rapport à B), pas " + M(r"2\overrightarrow{AB}") + ".")],
    hints=["Chasles en passant par B : " + M(r"\overrightarrow{CE}=\overrightarrow{CB}+\overrightarrow{BE}") + ". E symétrique de A par rapport à B signifie " + V("BE") + " = " + V("AB") + ".", relis("M", "exprimer")],
    general=M(r"\overrightarrow{CE}=\overrightarrow{CB}+\overrightarrow{BE}=-\overrightarrow{AD}+\overrightarrow{AB}") + " et " + M(r"\overrightarrow{CF}=\overrightarrow{CD}+\overrightarrow{DF}=-\overrightarrow{AB}+\overrightarrow{AD}") + ". Donc " + M(r"\overrightarrow{CE}+\overrightarrow{CF}=\vec 0") + " : C est le milieu de [EF] (Feuille 3¾, Ex 5).")

# ======================= BILAN – synthèse =======================
add(C5, type="mc", name="S1 – Parallélogramme : l'égalité fausse",
    text="ABCD est un parallélogramme. Laquelle de ces égalités est <b>fausse</b> ?",
    answers=[(100, V("AC") + " = " + V("BD"), "Exact, elle est fausse : les diagonales n'ont pas la même direction."),
             (0, V("AB") + " = " + V("DC"), "Celle-ci est vraie (caractérisation du parallélogramme)."),
             (0, V("AD") + " = " + V("BC"), "Celle-ci est vraie."),
             (0, V("BA") + " = " + V("CD"), "Celle-ci est vraie : ce sont les opposés de " + V("AB") + " et " + V("DC") + ".")],
    hints=["Fais une figure et suis les flèches.", relis("1.4", "proprietes")],
    general="Dans un parallélogramme ABCD : " + V("AB") + " = " + V("DC") + ", " + V("AD") + " = " + V("BC") + " (et leurs opposés). Les diagonales " + V("AC") + " et " + V("BD") + " ne sont jamais égales.")

add(C5, type="mc", name="S2 – Simplifier une somme de quatre vecteurs",
    text="Simplifier " + M(r"\overrightarrow{AB}+\overrightarrow{CD}-\overrightarrow{AD}-\overrightarrow{CB}") + ".",
    answers=[(100, NUL, "Exact : " + M(r"(\overrightarrow{AB}+\overrightarrow{BC})+(\overrightarrow{CD}+\overrightarrow{DA})=\overrightarrow{AC}+\overrightarrow{CA}=\vec 0") + "."),
             (0, V("AC"), "Tu as oublié la seconde moitié : " + M(r"\overrightarrow{CD}+\overrightarrow{DA}=\overrightarrow{CA}") + "."),
             (0, M(r"2\overrightarrow{AC}"), "Attention aux signes : " + M(r"-\overrightarrow{AD}=\overrightarrow{DA}") + "."),
             (0, V("CA"), "Regroupe : " + M(r"\overrightarrow{AB}-\overrightarrow{CB}=\overrightarrow{AB}+\overrightarrow{BC}=\overrightarrow{AC}") + ".")],
    hints=["Remplace chaque soustraction par l'addition de l'opposé : " + M(r"-\overrightarrow{AD}=\overrightarrow{DA}") + ", " + M(r"-\overrightarrow{CB}=\overrightarrow{BC}") + ". Puis réordonne pour enchaîner les lettres.", relis("2.2", "chasles")],
    general=M(r"\overrightarrow{AB}+\overrightarrow{BC}+\overrightarrow{CD}+\overrightarrow{DA}=\overrightarrow{AC}+\overrightarrow{CA}=\vec 0") + " (automatismes Série 3 J4).")

add(C5, type="mc", name="S3 – Alignement : la bonne condition",
    text="A, B, C sont trois points distincts. Ils sont alignés si et seulement si…",
    answers=[(100, V("AB") + " et " + V("AC") + " sont colinéaires.", "Exact (Propriété 5)."),
             (0, V("AB") + " = " + V("AC"), "Cela signifierait B = C."),
             (0, V("AB") + " + " + V("AC") + " = " + NUL, "Cela signifie que A est le milieu de [BC] : c'est un cas particulier d'alignement, pas une équivalence."),
             (0, "AB + BC = AC (longueurs).", "C'est vrai quand B est entre A et C, mais l'outil du chapitre est la colinéarité des vecteurs.")],
    hints=["Deux vecteurs colinéaires avec un point commun…", relis("4b", "colineaires")],
    general="Propriété 5 (§ 4) : A, B, C alignés ⟺ " + V("AB") + " et " + V("AC") + " colinéaires ⟺ il existe k tel que " + M(r"\overrightarrow{AC}=k\overrightarrow{AB}") + ".")

add(C5, type="mc", name="S4 – Translation : ce qu'il faut vérifier",
    text="Que faut-il vérifier pour affirmer que E est l'image de M par la translation de vecteur " + V("AB") + " ?",
    answers=[(100, V("ME") + " = " + V("AB"), "Exact : c'est la définition de la translation."),
             (0, V("EM") + " = " + V("AB"), "Sens inverse : ce serait M image de E."),
             (0, "ABME est un parallélogramme.", "Dans cet ordre, ABME parallélogramme signifie " + V("AB") + " = " + V("EM") + " : c'est le sens inverse. Le bon parallélogramme est ABEM."),
             (0, "(AB) et (ME) sont parallèles.", "Le parallélisme ne suffit pas : il faut aussi même sens et même norme.")],
    hints=["Définition du § 1.1 : l'image M' de M vérifie " + V("MM'") + " = " + v("u") + ".", relis("1.1", "point")],
    general="E est l'image de M par la translation de vecteur " + V("AB") + " ⟺ " + V("ME") + " = " + V("AB") + " ⟺ ABEM est un parallélogramme (éventuellement aplati).")

# ----------------------------------------------------------------------------
# Écriture du Moodle XML
# ----------------------------------------------------------------------------
def cdata(s):
    return "<![CDATA[" + s.replace("]]>", "]]]]><![CDATA[>") + "]]>"

def esc(s):
    return html.escape(s, quote=False)

FIG_RE = re.compile(r'@@PLUGINFILE@@/(fig_[a-z0-9_]+)\.png')

def files_for(text):
    out = ""
    for name in sorted(set(FIG_RE.findall(text))):
        out += '<file name="%s.png" path="/" encoding="base64">%s</file>\n' % (name, figures.b64(name[4:]))
    return out

def xml_text(tag, content, fmt="html"):
    return '<%s format="%s">\n<text>%s</text>\n%s</%s>\n' % (tag, fmt, cdata(content), files_for(content), tag)

def hints_xml(hints):
    return "".join('<hint format="html">\n<text>%s</text>\n<shownumcorrect/>\n<clearwrong/>\n</hint>\n' % cdata(h) for h in hints)

def question_xml(q):
    t = q["type"]
    name = esc(q["name"])
    head = '<question type="%s">\n<name><text>%s</text></name>\n' % ({"mc": "multichoice", "sa": "shortanswer", "num": "numerical", "cloze": "cloze"}[t], name)
    head += xml_text("questiontext", q["text"])
    head += xml_text("generalfeedback", q.get("general", ""))
    head += "<defaultgrade>1</defaultgrade>\n<penalty>0.3333333</penalty>\n<hidden>0</hidden>\n"
    body = ""
    if t == "mc":
        single = q.get("single", True)
        body += "<single>%s</single>\n<shuffleanswers>true</shuffleanswers>\n<answernumbering>abc</answernumbering>\n" % ("true" if single else "false")
        body += "<showstandardinstruction>0</showstandardinstruction>\n"
        body += xml_text("correctfeedback", "Bonne réponse.")
        body += xml_text("partiallycorrectfeedback", "Réponse partiellement correcte.")
        body += xml_text("incorrectfeedback", "Réponse incorrecte.")
        body += "<shownumcorrect/>\n"
        for frac, txt, fb in q["answers"]:
            body += '<answer fraction="%s" format="html">\n<text>%s</text>\n%s</answer>\n' % (frac, cdata(txt), xml_text("feedback", fb))
    elif t == "sa":
        body += "<usecase>0</usecase>\n"
        for frac, txt, fb in q["answers"]:
            body += '<answer fraction="%s" format="moodle_auto_format">\n<text>%s</text>\n%s</answer>\n' % (frac, esc(txt), xml_text("feedback", fb))
    elif t == "num":
        for frac, txt, fb in q["answers"]:
            body += '<answer fraction="%s" format="moodle_auto_format">\n<text>%s</text>\n<tolerance>%s</tolerance>\n%s</answer>\n' % (frac, esc(txt), q.get("tol", 0), xml_text("feedback", fb))
        body += "<unitgradingtype>0</unitgradingtype>\n<unitpenalty>0.1</unitpenalty>\n<showunits>3</showunits>\n<unitsleft>0</unitsleft>\n"
    elif t == "cloze":
        pass
    body += hints_xml(q.get("hints", []))
    return head + body + "</question>\n"

def category_xml(cat):
    return '<question type="category">\n<category>\n<text>$course$/top/%s</text>\n</category>\n<info format="html">\n<text></text>\n</info>\n<idnumber></idnumber>\n</question>\n' % esc(cat)

def write_xml(path):
    out = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'
    current = None
    for q in Q:
        if q["cat"] != current:
            current = q["cat"]
            out += category_xml(current)
        out += question_xml(q)
    out += "</quiz>\n"
    with open(path, "w", encoding="utf8") as f:
        f.write(out)

# ----------------------------------------------------------------------------
# Pages « Je révise » (HTML à coller dans une ressource Page d'Éléa)
# ----------------------------------------------------------------------------
def img_data(name, width=380):
    return '<p style="text-align:center"><img src="data:image/png;base64,%s" alt="figure" width="%d"></p>' % (figures.b64(name), width)

def yt(k):
    t, i = VIDEOS[k]
    return ('<div style="margin:10px 0"><div style="position:relative;padding-bottom:56.25%%;height:0;max-width:560px">'
            '<iframe src="https://www.youtube-nocookie.com/embed/%s" title="%s" style="position:absolute;top:0;left:0;width:100%%;height:100%%;border:0" allowfullscreen></iframe></div>'
            '<p><a href="%s%s" target="_blank">%s</a> (Yvan Monka)</p></div>') % (i, esc(t), YT, i, esc(t))

def box(title, inner, color="#1C7ED6"):
    return ('<div style="border-left:4px solid %s;background:#f4f8fc;padding:8px 14px;margin:14px 0;border-radius:0 6px 6px 0">'
            '<p style="margin:0 0 6px 0;color:%s"><b>%s</b></p>%s</div>') % (color, color, title, inner)

def details(summary, inner):
    return '<details style="margin:6px 0 12px 0"><summary style="cursor:pointer;color:#1C7ED6">%s</summary><div style="padding:6px 0 0 12px">%s</div></details>' % (summary, inner)

def exo(num, star, text, corr):
    return ('<div style="margin:10px 0"><p><span style="background:#1C7ED6;color:#fff;padding:1px 8px;border-radius:4px"><b>Exercice %s</b></span> '
            '<span style="color:#40C057">%s</span></p>%s%s</div>') % (num, star, text, details("Voir le corrigé", corr))

STAR1 = "★☆☆"

PAGES = {}

PAGES[1] = ("Bloc 1 – Je révise : définition d'un vecteur",
    "<p>Tu as eu moins de 50 % au test d'entrée du Bloc 1 : pas de panique, on reprend l'essentiel, puis tu refais quelques exercices avant le test de validation.</p>" +
    box("À retenir (cours § 1.1 à 1.4, pages 1 et 2)",
        "<ul>"
        "<li>Le vecteur " + V("AB") + " est caractérisé par sa <b>direction</b> (la droite (AB)), son <b>sens</b> (de A vers B) et sa <b>norme</b> (la longueur AB). Attention : " + V("AB") + " et " + V("BA") + " ont le même direction et la même norme mais des sens opposés : " + M(r"\overrightarrow{BA}=-\overrightarrow{AB}") + ".</li>"
        "<li>La <b>translation de vecteur " + v("u") + "</b> transforme tout point A en l'unique point A' tel que " + M(r"\overrightarrow{AA'}=\vec u") + ".</li>"
        "<li>Deux vecteurs sont <b>égaux</b> s'ils ont même direction, même sens et même norme. Un vecteur a une infinité de <b>représentants</b>.</li>"
        "<li>Le <b>vecteur nul</b> " + NUL + " a une norme nulle et pas de direction. Le <b>vecteur opposé</b> à " + V("AB") + " est " + V("BA") + ".</li>"
        "<li><b>Théorème :</b> ABCD est un parallélogramme (éventuellement aplati) ⟺ " + M(r"\overrightarrow{AB}=\overrightarrow{DC}") + ". On a alors aussi " + M(r"\overrightarrow{AD}=\overrightarrow{BC}") + ".</li>"
        "</ul>") +
    "<h4>Vidéos</h4>" + yt("point") + yt("proprietes") +
    "<h4>Exercices (avec corrigé dépliable)</h4>" +
    exo("A", STAR1, "<p>Sur la figure, citer : (a) un vecteur égal à " + V("AB") + " ; (b) un vecteur opposé à " + V("AB") + " ; (c) un vecteur de même direction et même sens que " + V("AB") + " mais de norme différente.</p>" + img_data("b1b", 460),
        "<p>(a) " + V("CD") + " : 3 carreaux vers la droite et 1 vers le haut, comme " + V("AB") + ".<br>(b) " + V("EF") + " : même direction, même norme, sens opposé.<br>(c) " + V("GH") + " : même direction et même sens, norme double.<br>" + V("IJ") + " et " + V("KL") + " n'ont pas la même direction que " + V("AB") + ".</p>") +
    exo("B", STAR1, "<p>Sur la figure, " + v("u") + " est donné. (a) Quelle est l'image de A par la translation de vecteur " + v("u") + " ? (b) Citer le représentant de " + v("u") + " d'origine C, puis celui d'extrémité E.</p>" + img_data("b1e"),
        "<p>" + v("u") + " correspond à un déplacement de 2 carreaux vers la droite et 1 carreau vers le haut.<br>(a) À partir de A on arrive en B : l'image de A est B.<br>(b) D'origine C : " + V("CD") + ". D'extrémité E : " + V("FE") + " (on part de E et on fait le déplacement à l'envers pour trouver l'origine F).</p>") +
    exo("C", STAR1, "<p>ABCD est un parallélogramme de centre O. Compléter : " + M(r"\overrightarrow{AB}=\overrightarrow{\ldots}") + " ; " + M(r"\overrightarrow{AD}=\overrightarrow{\ldots}") + " ; " + M(r"\overrightarrow{AO}=\overrightarrow{\ldots}") + " ; un vecteur opposé à " + V("AB") + " est " + M(r"\overrightarrow{\ldots}") + ".</p>" + img_data("b1c", 320),
        "<p>" + M(r"\overrightarrow{AB}=\overrightarrow{DC}") + " ; " + M(r"\overrightarrow{AD}=\overrightarrow{BC}") + " ; " + M(r"\overrightarrow{AO}=\overrightarrow{OC}") + " (O milieu de [AC]) ; un vecteur opposé à " + V("AB") + " est " + V("BA") + " ou " + V("CD") + ".</p>") +
    box("Sur la feuille d'exercices", "<p>Feuille 2 : exercices 1, 2 (translation), 5, 6 (égalité), 10, 11 (représentants). Manuel : Ex 15 et 18 p. 183. Puis GeoGebra : " + capy("definitions") + ".</p>", "#F08C00"))

PAGES[2] = ("Bloc 2 – Je révise : somme de vecteurs et relation de Chasles",
    "<p>Tu as eu moins de 50 % au test d'entrée du Bloc 2 : on reprend la construction d'une somme et la relation de Chasles, puis quelques exercices avant le test de validation.</p>" +
    box("À retenir (cours § 2.1 à 2.3, pages 3 et 4)",
        "<ul>"
        "<li><b>Bout à bout :</b> pour construire " + M(r"\vec u+\vec v") + ", on place " + v("v") + " à la suite de " + v("u") + " ; le vecteur somme va de l'origine de " + v("u") + " à l'extrémité de " + v("v") + ". L'ordre n'a pas d'importance : " + M(r"\vec u+\vec v=\vec v+\vec u") + ".</li>"
        "<li><b>Parallélogramme :</b> si " + M(r"\vec u=\overrightarrow{MN}") + " et " + M(r"\vec v=\overrightarrow{MP}") + " ont la même origine M, alors " + M(r"\vec u+\vec v=\overrightarrow{MQ}") + " où MNQP est un parallélogramme.</li>"
        "<li><b>Relation de Chasles :</b> pour tous points A, M, B : " + M(r"\overrightarrow{AM}+\overrightarrow{MB}=\overrightarrow{AB}") + ". « Aller d'Annoville à Brainville puis de Brainville à Coutances, c'est aller d'Annoville à Coutances. »</li>"
        "<li><b>Soustraire</b>, c'est ajouter l'opposé : " + M(r"\vec u-\vec v=\vec u+(-\vec v)") + " et " + M(r"-\overrightarrow{AB}=\overrightarrow{BA}") + ".</li>"
        "</ul>") +
    "<h4>Vidéos</h4>" + yt("somme") + yt("chasles") +
    "<h4>Exercices (avec corrigé dépliable)</h4>" +
    exo("A", STAR1, "<p>Sur la figure, quel vecteur est égal à " + M(r"\vec u+\vec v") + " ? à " + M(r"\vec u-\vec v") + " ?</p>" + img_data("b2a", 460),
        "<p>" + v("u") + " : 3 vers la droite, 1 vers le haut ; " + v("v") + " : 1 vers la droite, 2 vers le haut.<br>" + M(r"\vec u+\vec v") + " : 4 vers la droite, 3 vers le haut, c'est " + v("a") + ".<br>" + M(r"\vec u-\vec v") + " : 3 − 1 = 2 vers la droite, 1 − 2 = −1 (1 vers le bas), c'est " + v("b") + ".</p>") +
    exo("B", STAR1, "<p>Simplifier à l'aide de la relation de Chasles : (a) " + M(r"\overrightarrow{TR}+\overrightarrow{RP}") + " ; (b) " + M(r"\overrightarrow{GT}+\overrightarrow{AG}") + " ; (c) " + M(r"\overrightarrow{TR}+\overrightarrow{UT}+\overrightarrow{RU}") + " ; (d) " + M(r"\overrightarrow{ST}-\overrightarrow{VU}+\overrightarrow{TU}") + ".</p>",
        "<p>(a) " + M(r"\overrightarrow{TP}") + ".<br>(b) " + M(r"\overrightarrow{AG}+\overrightarrow{GT}=\overrightarrow{AT}") + ".<br>(c) " + M(r"\overrightarrow{UT}+\overrightarrow{TR}+\overrightarrow{RU}=\overrightarrow{UU}=\vec 0") + ".<br>(d) " + M(r"\overrightarrow{ST}+\overrightarrow{TU}+\overrightarrow{UV}=\overrightarrow{SV}") + " (car " + M(r"-\overrightarrow{VU}=\overrightarrow{UV}") + ").</p>") +
    exo("C", STAR1, "<p>ABCDEF est un hexagone régulier de centre O. Compléter : " + M(r"\overrightarrow{AB}+\overrightarrow{CD}=\ldots") + " ; " + M(r"\overrightarrow{OB}+\overrightarrow{OE}=\ldots") + "</p>" + img_data("hex", 260),
        "<p>" + M(r"\overrightarrow{AB}=\overrightarrow{OC}") + " (ABCO est un parallélogramme), donc " + M(r"\overrightarrow{AB}+\overrightarrow{CD}=\overrightarrow{OC}+\overrightarrow{CD}=\overrightarrow{OD}") + ".<br>O est le milieu de [BE] donc " + M(r"\overrightarrow{OE}=-\overrightarrow{OB}") + " et " + M(r"\overrightarrow{OB}+\overrightarrow{OE}=\vec 0") + ".</p>") +
    box("Sur la feuille d'exercices", "<p>Feuille 2 : exercices 13 (constructions) et 14 (Chasles). Manuel : Ex 39 p. 186, Ex 42, 43, 45, 46 p. 187. Puis GeoGebra : " + capy("somme") + ".</p>", "#F08C00"))

PAGES[3] = ("Bloc 3 – Je révise : produit par un réel et colinéarité",
    "<p>Tu as eu moins de 50 % au test d'entrée du Bloc 3 : on reprend la multiplication d'un vecteur par un nombre et la colinéarité, puis quelques exercices avant le test de validation.</p>" +
    box("À retenir (cours § 3 et § 4, pages 5 à 7)",
        "<ul>"
        "<li>Pour " + v("u") + " non nul et k réel non nul, le vecteur " + M(r"k\vec u") + " a <b>la même direction</b> que " + v("u") + " ; <b>même sens</b> si k > 0, <b>sens contraire</b> si k < 0 ; sa norme est |k| fois celle de " + v("u") + ".</li>"
        "<li>Pour trouver k tel que " + M(r"\overrightarrow{AC}=k\overrightarrow{AB}") + " : on regarde le sens (signe de k) puis on calcule le rapport des longueurs " + M(r"\dfrac{AC}{AB}") + ".</li>"
        "<li>On calcule avec les vecteurs comme en calcul littéral : " + M(r"3\overrightarrow{AB}+\dfrac12\overrightarrow{AB}=\dfrac72\overrightarrow{AB}") + ", et " + M(r"\overrightarrow{BA}=-\overrightarrow{AB}") + ".</li>"
        "<li>Deux vecteurs sont <b>colinéaires</b> s'il existe un réel k tel que " + M(r"\vec v=k\vec u") + " (ou " + M(r"\vec u=k\vec v") + ") : ils ont la même direction. Le vecteur nul est colinéaire à tout vecteur.</li>"
        "<li>" + V("AB") + " et " + V("CD") + " colinéaires ⟺ (AB) ∥ (CD). &nbsp; " + V("AB") + " et " + V("AC") + " colinéaires ⟺ A, B, C alignés.</li>"
        "</ul>") +
    "<h4>Vidéos</h4>" + yt("produit") + yt("colineaires") +
    "<h4>Exercices (avec corrigé dépliable)</h4>" +
    exo("A", STAR1, "<p>Dans chaque cas, exprimer " + V("AC") + " en fonction de " + V("AB") + ".</p>" + img_data("b3a1", 440) + img_data("b3a2", 440) + img_data("b3a3", 440),
        "<p>Cas 1 : même sens, AC = 6 et AB = 2 graduations : " + M(r"\overrightarrow{AC}=3\overrightarrow{AB}") + ".<br>Cas 2 : sens contraires, AC = 4 et AB = 2 : " + M(r"\overrightarrow{AC}=-2\overrightarrow{AB}") + ".<br>Cas 3 : même sens, AC = 2 et AB = 4 : " + M(r"\overrightarrow{AC}=\dfrac12\overrightarrow{AB}") + ".</p>") +
    exo("B", STAR1, "<p>A et B sont deux points. Déterminer m, n, p, q tels que : (a) " + M(r"3\overrightarrow{AB}+\dfrac12\overrightarrow{AB}=m\overrightarrow{AB}") + " ; (b) " + M(r"2(3\overrightarrow{BA})=n\overrightarrow{AB}") + " ; (c) " + M(r"2\overrightarrow{AB}-\overrightarrow{BA}=p\overrightarrow{AB}") + " ; (d) " + M(r"3\overrightarrow{BA}-4\overrightarrow{AB}=q\overrightarrow{AB}") + ".</p>",
        "<p>(a) m = 3 + ½ = 3,5. (b) " + M(r"6\overrightarrow{BA}=-6\overrightarrow{AB}") + " : n = −6. (c) " + M(r"2\overrightarrow{AB}+\overrightarrow{AB}") + " : p = 3. (d) " + M(r"-3\overrightarrow{AB}-4\overrightarrow{AB}") + " : q = −7.</p>") +
    exo("C", STAR1, "<p>Sur le quadrillage, quels vecteurs sont colinéaires ? Justifier par une égalité.</p>" + img_data("b3b", 400),
        "<p>" + v("u") + " : 2 à droite, 1 en haut. " + v("v") + " : 4 à gauche, 2 en bas, donc " + M(r"\vec v=-2\vec u") + " : " + v("u") + " et " + v("v") + " sont colinéaires. " + v("w") + " (4 à droite, 3 en haut) n'est colinéaire ni à " + v("u") + " ni à " + v("v") + ".</p>") +
    box("Sur la feuille d'exercices", "<p>Feuille 3 : exercices 1, 2 (lire et construire k" + V("AB") + ") et 3 (coefficients). Manuel : Ex 18, 19 p. 207, Ex 41, 42 p. 208. Puis GeoGebra : " + capy("colinearite") + ".</p>", "#F08C00"))

PAGES[4] = ("Bloc 4 – Je révise : décomposer un vecteur, démontrer",
    "<p>Tu as eu moins de 50 % au test d'entrée du Bloc 4 : on reprend la décomposition d'un vecteur en fonction de deux autres et les trois méthodes de démonstration, puis quelques exercices avant le test de validation.</p>" +
    box("À retenir (cours § 4, page 7, et encadré Méthode de la Feuille 3¾)",
        "<ul>"
        "<li>Pour <b>exprimer un vecteur en fonction de " + v("u") + " et " + v("v") + "</b> : on utilise la relation de Chasles pour passer par des points « utiles », puis on remplace chaque morceau par " + M(r"\pm\vec u") + ", " + M(r"\pm\vec v") + " ou une fraction de ceux-ci. Sur quadrillage, on compte les carreaux.</li>"
        "<li><b>Parallèles :</b> (AB) ∥ (CD) ⟺ " + V("AB") + " et " + V("CD") + " colinéaires.</li>"
        "<li><b>Alignés :</b> A, B, C alignés ⟺ " + V("AB") + " et " + V("AC") + " colinéaires.</li>"
        "<li><b>Milieu :</b> I milieu de [AB] ⟺ " + M(r"\overrightarrow{AI}=\overrightarrow{IB}") + " ⟺ " + M(r"\overrightarrow{IA}+\overrightarrow{IB}=\vec 0") + " ⟺ " + M(r"\overrightarrow{AI}=\dfrac12\overrightarrow{AB}") + ".</li>"
        "<li><b>Plan de démonstration :</b> exprimer les vecteurs concernés en fonction de <b>deux mêmes vecteurs</b>, puis chercher le réel k qui les relie.</li>"
        "</ul>") +
    "<h4>Vidéos</h4>" + yt("exprimer") + yt("egalite") +
    "<h4>Exercices (avec corrigé dépliable)</h4>" +
    exo("A", STAR1, "<p>Exprimer " + M(r"\vec{w_1}") + ", " + M(r"\vec{w_2}") + " et " + M(r"\vec{w_3}") + " en fonction de " + v("u") + " et " + v("v") + ".</p>" + img_data("b4a", 460),
        "<p>" + v("u") + " = (2 à droite, 1 en haut), " + v("v") + " = (1 à gauche, 1 en haut).<br>" + M(r"\vec{w_1}") + " = (3, 3) = " + M(r"2\vec u+\vec v") + " ; " + M(r"\vec{w_2}") + " = (4, −1) = " + M(r"\vec u-2\vec v") + " ; " + M(r"\vec{w_3}") + " = (−3, 0) = " + M(r"-\vec u+\vec v") + ".</p>") +
    exo("B", STAR1, "<p>ABCD est un parallélogramme, I le milieu de [CD], " + M(r"\vec u=\overrightarrow{AB}") + ", " + M(r"\vec v=\overrightarrow{AD}") + ". Exprimer " + V("AI") + " en fonction de " + v("u") + " et " + v("v") + ".</p>" + img_data("b4b", 340),
        "<p>" + M(r"\overrightarrow{AI}=\overrightarrow{AD}+\overrightarrow{DI}=\vec v+\dfrac12\overrightarrow{DC}=\vec v+\dfrac12\overrightarrow{AB}=\vec v+\dfrac12\vec u") + ".</p>") +
    exo("C", STAR1, "<p>ABCDEF est un hexagone régulier de centre O, " + M(r"\vec u=\overrightarrow{OA}") + " et " + M(r"\vec v=\overrightarrow{OB}") + ". Exprimer " + V("OD") + ", " + V("OC") + " et " + V("DB") + " en fonction de " + v("u") + " et " + v("v") + ".</p>" + img_data("hex_uv", 260),
        "<p>" + M(r"\overrightarrow{OD}=-\vec u") + " (O milieu de [AD]).<br>" + M(r"\overrightarrow{OC}=\overrightarrow{AB}=\overrightarrow{AO}+\overrightarrow{OB}=-\vec u+\vec v") + ".<br>" + M(r"\overrightarrow{DB}=\overrightarrow{DO}+\overrightarrow{OB}=\vec u+\vec v") + ".</p>") +
    box("Sur la feuille d'exercices", "<p>Feuille 3 : exercices 4 et 5 (décomposer sur quadrillage), puis 6 et 7. Feuille 3¾ : exercices 1 et 2 (démonstrations guidées à trous). Manuel : Ex 45 p. 209.</p>", "#F08C00"))

MATHJAX = '<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]]}};</script><script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>'

def page_html(title, body, standalone=True):
    if not standalone:
        return body
    return ('<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>%s</title>%s'
            '<style>body{font-family:-apple-system,Helvetica,Arial,sans-serif;max-width:860px;margin:24px auto;padding:0 16px;line-height:1.5;color:#222}h4{margin-top:22px}</style>'
            '</head><body><h3>%s</h3>%s</body></html>') % (esc(title), MATHJAX, esc(title), body)

# ----------------------------------------------------------------------------
# Fiche de montage
# ----------------------------------------------------------------------------
def fiche_html():
    counts = {}
    for q in Q:
        counts[q["cat"]] = counts.get(q["cat"], 0) + 1
    rows = "".join("<tr><td>%s</td><td style='text-align:center'>%d</td></tr>" % (esc(c.split("/")[-1]), n) for c, n in counts.items())
    bloc_rows = ""
    blocs = [
        (1, "Définition d'un vecteur (Obj. 1, 2, 3)", "Feuille 2 : Ex 1, 2, 5, 6, 10, 11 · Manuel Ex 15, 18 p. 183, Ex 23, 27 p. 184", "Feuille 2 : Ex 3, 7, 12 · Manuel Ex 28 p. 184, Ex 30, 31 p. 185", "Feuille 2 : Ex 4, 8, 9 · Manuel Ex 35 p. 185, Ex 37, 38 p. 186 · Capytale Définitions"),
        (2, "Somme et relation de Chasles (Obj. 4)", "Feuille 2 : Ex 13, 14 · Manuel Ex 39 p. 186, Ex 42, 43, 45, 46 p. 187", "Feuille 2 : Ex 15, 16 · Manuel Ex 41 p. 186", "Manuel Ex 71, 72, 73 p. 192 · Capytale Somme"),
        (3, "Produit par un réel, colinéarité (Obj. 5)", "Feuille 3 : Ex 1, 2 · Manuel Ex 18, 19 p. 207, Ex 41, 42 p. 208", "Feuille 3 : Ex 3 · Feuille 3¾ : Ex 1, 2, 3 · Manuel Ex 43, 44 p. 209", "Feuille 3¾ : Ex 4 · Capytale Colinéarité"),
        (4, "Décomposition, alignement, milieu (Obj. 6, 7)", "Feuille 3 : Ex 4, 5", "Feuille 3 : Ex 6, 7 · Manuel Ex 45 p. 209, Ex 74 p. 212", "Feuille 3 : Ex 8 · Feuille 3¾ : Ex 5 · Manuel Ex 75, 78 p. 212"),
    ]
    for n, t, g, b, r in blocs:
        bloc_rows += "<tr><td><b>Bloc %d</b><br>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (n, t, g, b, r)

    body = """
<h2>Séquence 2 – Vecteurs : parcours Éléa différencié</h2>
<p><i>Fiche de montage. Temps estimé : 1 h à 1 h 30 pour tout assembler une première fois. Les fichiers à utiliser sont dans le même dossier que cette fiche.</i></p>

<h3>1. Principe</h3>
<p>Le parcours est découpé en 4 blocs qui suivent le cours. Dans chaque bloc, un <b>test d'entrée</b> (6 questions tirées au hasard dans la banque du bloc) aiguille automatiquement l'élève, grâce aux <b>restrictions d'accès</b> de Moodle :</p>
<table border="1" cellpadding="6" style="border-collapse:collapse">
<tr style="background:#eef"><th>Note au test d'entrée</th><th>Ce que l'élève voit ensuite</th></tr>
<tr><td>&lt; 50 %</td><td><b>Je révise</b> : page de rappel + vidéos + 3 exercices corrigés + exercices ★ des feuilles</td></tr>
<tr><td>50 % à 79 %</td><td><b>Je m'entraîne</b> : exercices ★★ des feuilles et du manuel (corrigé PDF déposé)</td></tr>
<tr><td>≥ 80 %</td><td><b>Je vais plus loin</b> : exercices ★★★ + activité Capytale du bloc</td></tr>
<tr><td>—</td><td><b>Je valide</b> : test de validation (6 autres questions de la même banque), visible une fois l'étape précédente achevée. Il débloque le bloc suivant.</td></tr>
</table>
<p>Pendant les tests, chaque question fournit deux <b>indices</b> successifs (le second renvoie au paragraphe exact du cours et à la vidéo), puis un <b>corrigé</b> avec renvoi aux exercices. C'est le mode « interactif avec essais multiples » de Moodle.</p>

<h3>2. Importer la banque de questions (5 min)</h3>
<ol>
<li>Dans le parcours Éléa : menu <b>Plus → Banque de questions → Importer</b>.</li>
<li>Format : <b>Moodle XML</b>. Fichier : <code>Séquence 2 - Éléa - Banque de questions.xml</code>. Laisser « Obtenir la catégorie du fichier » coché.</li>
<li>Après l'import, la banque contient la catégorie <b>Séquence 2 – Vecteurs</b> et ses sous-catégories :</li>
</ol>
<table border="1" cellpadding="6" style="border-collapse:collapse"><tr style="background:#eef"><th>Sous-catégorie</th><th>Questions</th></tr>__ROWS__</table>
<p>Les figures sont incluses dans le fichier XML (il n'y a rien d'autre à téléverser). Les formules s'affichent grâce au filtre MathJax, activé par défaut sur Éléa. Vérifier sur une question : <b>Aperçu</b>.</p>

<h3>3. Créer les sections et les activités</h3>
<p>Réglages communs à <b>tous les tests</b> (Test → Paramètres) :</p>
<ul>
<li><b>Comportement des questions :</b> « Interactif avec essais multiples » (c'est ce qui affiche les indices).</li>
<li><b>Nombre de tentatives :</b> 2 pour les tests d'entrée, illimité pour les tests de validation. Méthode de notation : note la plus haute.</li>
<li><b>Options de relecture :</b> cocher « Feedback spécifique », « Feedback général », « Réponse juste » pendant et après la tentative.</li>
<li><b>Mise en page :</b> une question par page, questions mélangées.</li>
<li><b>Achèvement d'activité :</b> « L'élève doit recevoir une note ».</li>
</ul>
<p>Pour remplir un test : <b>Questions → Ajouter → une question aléatoire</b>, choisir la sous-catégorie du bloc, nombre de questions = 6. Les deux tests (entrée et validation) d'un même bloc tirent dans la même sous-catégorie : Moodle ne retire pas les questions déjà vues, mais avec 15 questions par bloc le recouvrement est faible ; on peut aussi ajouter à la main 6 questions fixes pour le test d'entrée et laisser l'aléatoire pour la validation.</p>

<h4>Section 0 – Avant de commencer</h4>
<ul>
<li><b>Test « Positionnement »</b> : 5 questions de la sous-catégorie <i>0 – Positionnement</i>, 1 tentative, non comptabilisé (note maximale 0 ou catégorie de notes « hors total »).</li>
<li><b>Fichier</b> : <i>Séquence 2 - Cours - Vecteurs.pdf</i> ; <b>Fichier</b> : version Grands Caractères, avec restriction d'accès « Groupe » = le groupe des élèves concernés (à créer dans Participants → Groupes).</li>
<li><b>Fichiers</b> : Feuilles d'exercices 2, 3 et 3¾ (et leurs corrigés, éventuellement cachés jusqu'à une date).</li>
</ul>

<h4>Sections 1 à 4 – un bloc par section (même schéma)</h4>
<table border="1" cellpadding="6" style="border-collapse:collapse">
<tr style="background:#eef"><th>Activité</th><th>Type</th><th>Restriction d'accès</th><th>Contenu</th></tr>
<tr><td>Je me teste</td><td>Test</td><td>Bloc 1 : aucune. Blocs 2 à 4 : <i>Note</i> « Je valide (bloc précédent) » ≥ 80 %</td><td>6 questions aléatoires de la sous-catégorie du bloc, 2 tentatives</td></tr>
<tr><td>Je révise</td><td>Page</td><td><i>Note</i> « Je me teste » &lt; 50 %</td><td>Coller le contenu du fichier <code>Bloc N - Je révise.html</code> (voir § 4)</td></tr>
<tr><td>Je m'entraîne</td><td>Page (ou Étiquette)</td><td><i>Note</i> « Je me teste » ≥ 50 % <b>et</b> &lt; 80 %</td><td>Liste des exercices ★★ du bloc (tableau ci-dessous) + lien vers le corrigé PDF</td></tr>
<tr><td>Je vais plus loin</td><td>Page + URL</td><td><i>Note</i> « Je me teste » ≥ 80 %</td><td>Exercices ★★★ + lien Capytale du bloc</td></tr>
<tr><td>Je valide</td><td>Test</td><td><i>Achèvement d'activité</i> : « Je révise » OU « Je m'entraîne » OU « Je vais plus loin » marqué achevé (ensemble de restrictions, « au moins une »)</td><td>6 questions aléatoires de la même sous-catégorie, tentatives illimitées</td></tr>
</table>
<p>Pour saisir une restriction de note : Paramètres de l'activité → <b>Restreindre l'accès → Ajouter une restriction → Note</b>, choisir l'activité, cocher « doit être ≥ » et/ou « doit être &lt; ». Pour « Je valide », utiliser <b>Ajouter une restriction → Ensemble de restrictions</b> puis « L'étudiant doit satisfaire <b>au moins une</b> » et trois restrictions d'achèvement. Laisser l'œil <b>ouvert</b> (l'élève voit l'activité grisée avec la condition) ou <b>barré</b> (activité invisible tant que la condition n'est pas remplie) : le barré est préférable ici, pour que chaque élève ne voie que son chemin.</p>
<p>Pour que les restrictions sur l'achèvement fonctionnent, activer dans les pages « Je révise / Je m'entraîne / Je vais plus loin » l'achèvement <b>« L'élève doit afficher cette activité »</b> (ou « marquer manuellement » si tu préfères que l'élève coche).</p>

<h4>Renvois par bloc et par niveau (pour les pages « Je m'entraîne » et « Je vais plus loin »)</h4>
<table border="1" cellpadding="6" style="border-collapse:collapse">
<tr style="background:#eef"><th>Bloc</th><th style="color:#40C057">★ (Je révise)</th><th style="color:#228BE6">★★ (Je m'entraîne)</th><th style="color:#FA5252">★★★ (Je vais plus loin)</th></tr>__BLOCROWS__</table>

<h4>Section 5 – Bilan</h4>
<ul>
<li><b>Test « Bilan »</b> : 12 questions aléatoires de la catégorie <i>Séquence 2 – Vecteurs</i> en cochant « inclure les sous-catégories », plus les 4 questions de <i>Bilan – synthèse</i>. Restriction : « Je valide (Bloc 4) » ≥ 80 %. Comportement « Feedback a posteriori » cette fois (pas d'indices) pour se rapprocher des conditions du DS.</li>
<li><b>URL</b> : les deux vidéos de révision d'Yvan Monka (LE COURS et le QCM), en accès libre.</li>
<li><b>Badge</b> (facultatif) : Administration → Badges → « Vecteurs », critère : test Bilan ≥ 80 %.</li>
</ul>

<h3>4. Les pages « Je révise »</h3>
<p>Quatre fichiers <code>Bloc N - Je révise.html</code>. Pour chacun : ouvrir le fichier dans un éditeur de texte, copier <b>tout</b> le contenu entre les repères <code>&lt;!-- DEBUT --&gt;</code> et <code>&lt;!-- FIN --&gt;</code>, puis dans Éléa : ajouter une <b>Page</b>, dans le contenu cliquer sur l'outil <b>« Code HTML » (&lt;/&gt;)</b> de l'éditeur, coller, enregistrer. Les fichiers <code>… (aperçu).html</code> permettent de visualiser le rendu dans un navigateur avant de coller.</p>
<p>Les figures sont incluses dans le code (images encodées) ; si Éléa refuse une image, elle est aussi disponible en PNG dans le dossier <code>figures</code>, à insérer avec le bouton image de l'éditeur. Les vidéos sont intégrées ; si l'intégration est bloquée par l'établissement, le lien texte sous chaque vidéo reste fonctionnel.</p>

<h3>5. Ce que tu vois côté enseignante</h3>
<ul>
<li><b>Notes</b> : le carnet de notes montre, pour chaque élève, le score d'entrée et le score de validation de chaque bloc — donc le chemin suivi.</li>
<li><b>Rapport d'activité → Achèvement d'activités</b> : tableau élèves × activités, pour repérer qui est passé par « Je révise ».</li>
<li><b>Test → Résultats → Statistiques</b> : le taux de réussite par question montre les points du chapitre qui posent problème à la classe.</li>
</ul>

<h3>6. Pistes d'évolution</h3>
<ul>
<li>Remplacer les QCM « quel point est l'image… » par des questions <b>glisser-déposer sur image</b> (type de question Moodle) une fois le montage rodé.</li>
<li>Ajouter des questions <b>Calculée</b> à valeurs aléatoires pour les coefficients k (Bloc 3).</li>
<li>Réutiliser les mêmes sous-catégories pour un test « Automatismes vecteurs » hebdomadaire de 3 questions.</li>
</ul>
""".replace("__ROWS__", rows).replace("__BLOCROWS__", bloc_rows)
    return page_html("Séquence 2 – Éléa – Fiche de montage", body)

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    write_xml(os.path.join(HERE, "Séquence 2 - Éléa - Banque de questions.xml"))
    for n, (title, body) in PAGES.items():
        with open(os.path.join(HERE, "Bloc %d - Je révise (aperçu).html" % n), "w", encoding="utf8") as f:
            f.write(page_html(title, body))
        with open(os.path.join(HERE, "Bloc %d - Je révise.html" % n), "w", encoding="utf8") as f:
            f.write("<!-- DEBUT -->\n<h3>%s</h3>\n%s\n<!-- FIN -->\n" % (esc(title), body))
    with open(os.path.join(HERE, "Séquence 2 - Éléa - Fiche de montage.html"), "w", encoding="utf8") as f:
        f.write(fiche_html())
    from collections import Counter
    c = Counter(q["cat"].split("/")[-1] for q in Q)
    for k, n in c.items():
        print("%-45s %d" % (k, n))
    print("total", len(Q))
