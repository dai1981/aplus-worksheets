# -*- coding: utf-8 -*-
"""Sverige årskurs 7–9: geometri（vinklar, area, cirkeln, enheter, skala, polygoner, volym, begränsningsarea, Pythagoras, likformighet, cirkelsektorer）"""
import math
import re
from fractions import Fraction as F
from se_h import (gen, MQ, lista, ri, ch, sh, cap, fr, fq, d, par, sg, M, MN, rd, sup, unit, tab, K, num, kr, NB, MIN, coin, expr, figure,
                  wrap, text, line, fig, INK, GREEN, FILL, RED, BLUE)
import gen_au_maths_y5_angles as AU
import tr_g

PI = F(314, 100)


def rl(svg, label):
    return re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1)


def cm(x, u="cm"):
    return d(x) + NB + u


def tri(a, b, labels, rights=()):
    try:
        return fig(rl(AU.shape_svg(AU.tri_pts(a, b), labels, "triangel", rights=rights), "triangel"))
    except AssertionError:
        raise ValueError("label")


def nz(a, b):
    while True:
        v = ri(a, b)
        if v:
            return v


def poly(pts, sides, label="figur", rights=(), dashed=(), unit_=""):
    return fig(rl(tr_g.poly(pts, sides, (), unit_, label, rights=rights, dashed=dashed), label))


def kryss(theta, labels):
    return fig(rl(tr_g.parallel_fig(theta, labels), "två parallella linjer och en linje som skär dem"))


# ------------------------------------------------------------ kroppar med mått
def solid(kind, a="", b="", c=""):
    s = []
    if kind == "cylinder":
        s.append("<ellipse cx='110' cy='40' rx='70' ry='18' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, INK))
        s.append("<path d='M40 40 L40 170 A70 18 0 0 0 180 170 L180 40' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, INK))
        s.append("<path d='M40 170 A70 18 0 0 1 180 170' fill='none' stroke='%s' stroke-width='1.4' stroke-dasharray='5 4'/>" % INK)
        s.append(line(110, 40, 180, 40, RED, 2.2) + text(145, 32, a, 14, col=RED) + text(192, 110, b, 14, anchor="start", col=BLUE))
        return wrap(260, 200, "".join(s), "cylinder")
    if kind == "kon":
        s.append("<path d='M40 170 L110 25 L180 170' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, INK))
        s.append("<ellipse cx='110' cy='170' rx='70' ry='16' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, INK))
        s.append(line(110, 25, 110, 170, BLUE, 1.6, " stroke-dasharray='5 4'") + line(110, 170, 180, 170, RED, 2.2))
        s.append(text(145, 198, a, 14, col=RED) + text(116, 100, b, 14, anchor="start", col=BLUE))
        if c:
            s.append(text(156, 92, c, 14, anchor="start", col=GREEN))
        return wrap(260, 206, "".join(s), "kon")
    if kind == "klot":
        s.append("<circle cx='110' cy='100' r='75' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, INK))
        s.append("<ellipse cx='110' cy='100' rx='75' ry='18' fill='none' stroke='%s' stroke-width='1.4' stroke-dasharray='5 4'/>" % INK)
        s.append(line(110, 100, 185, 100, RED, 2.2) + text(148, 136, a, 14, col=RED))
        return wrap(230, 200, "".join(s), "klot")
    if kind == "pyramid":
        A_, B_, C_, D_, T = (40, 160), (150, 160), (200, 125), (90, 125), (120, 25)
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='2'/>" % (A_ + B_ + T + (FILL, INK)))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='#e3f1e8' stroke='%s' stroke-width='2'/>" % (B_ + C_ + T + (INK,)))
        s.append(line(A_[0], A_[1], D_[0], D_[1], INK, 1.4, " stroke-dasharray='5 4'") + line(D_[0], D_[1], C_[0], C_[1], INK, 1.4, " stroke-dasharray='5 4'") + line(D_[0], D_[1], T[0], T[1], INK, 1.4, " stroke-dasharray='5 4'"))
        s.append(line(120, 25, 120, 142, BLUE, 1.6, " stroke-dasharray='5 4'"))
        s.append(text(95, 182, a, 14, col=RED) + text(186, 154, b if b else "", 14, anchor="start", col=RED) + text(126, 96, c, 14, anchor="start", col=BLUE))
        return wrap(270, 200, "".join(s), "pyramid med kvadratisk bas")
    if kind == "prisma":
        A_, B_, T = (30, 160), (150, 160), (90, 70)
        o = (70, -40)
        s.append("<polygon points='%d,%d %d,%d %d,%d %d,%d' fill='#e3f1e8' stroke='%s' stroke-width='2'/>" % (B_ + (B_[0] + o[0], B_[1] + o[1]) + (T[0] + o[0], T[1] + o[1]) + T + (INK,)))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='2'/>" % (A_ + B_ + T + (FILL, INK)))
        s.append(line(T[0], T[1], T[0] + o[0], T[1] + o[1], INK, 2))
        s.append(line(A_[0], A_[1], A_[0] + o[0], A_[1] + o[1], INK, 1.4, " stroke-dasharray='5 4'") + line(A_[0] + o[0], A_[1] + o[1], B_[0] + o[0], B_[1] + o[1], INK, 1.4, " stroke-dasharray='5 4'"))
        s.append(line(T[0], T[1], T[0], 160, BLUE, 1.6, " stroke-dasharray='5 4'"))
        s.append(text(90, 182, a, 14, col=RED) + text(96, 125, b, 14, anchor="start", col=BLUE) + text(196, 140, c, 14, anchor="start", col=GREEN))
        return wrap(280, 200, "".join(s), "prisma med triangulär bas")
    raise ValueError(kind)


def box(a, b, c):
    import kr_pics56
    return rl(kr_pics56.box_svg(a, b, c, "cm"), "rätblock")


def sf(kind, *a):
    return "<div class='qfig'>%s</div>" % fig(solid(kind, *a)).replace("<svg ", "<svg data-pf='lg' ", 1) if False else fig(solid(kind, *a))


# ============================================================ vinklar (åk 7)
def vinklar(lv):
    def triangel():
        a, b = ri(25, 95), ri(25, 95)
        c = 180 - a - b
        if c < 15:
            return None
        return MN("Hur stor är vinkeln med frågetecknet?" + tri(a, b, {0: "%d°" % a, 1: "%d°" % b, 2: "?"}, [i for i, x in enumerate((a, b)) if x == 90]), c, [360 - a - b, a + b, c + 10], "Vinkelsumman i en triangel är 180°. 180° − %d° − %d° = <b>%d°</b>." % (a, b, c), "°")

    def kors():
        t = ri(35, 145)
        if 80 <= t <= 100:
            return None
        code = ch([1, 2, 3, 4])
        ask = ch([c for c in (1, 2, 3, 4) if c != code])
        val = {1: t, 2: 180 - t, 3: t, 4: 180 - t}
        lab = {code: "%d°" % val[code], ask: "x"}
        v = val[ask]
        kind = "vertikalvinklar och lika stora" if (code + ask) % 2 == 0 else "sidovinklar och har summan 180°"
        return MN("Två linjer skär varandra. Hur stor är vinkeln x?" + kryss(t, lab), v, [180 - v, 360 - v, 90 - v if v < 90 else v - 90], "Vinklarna är %s: <b>x = %d°</b>." % (kind, v), "°")

    def likbent():
        k = ri(0, 2)
        if k == 0:
            top = ri(10, 80) * 2
            b = (180 - top) // 2
            return MN("En likbent triangel har toppvinkeln %d°. Hur stor är varje basvinkel?" % top, b, [180 - top, top // 2, 90 - top // 2 + 10], "Basvinklarna är lika stora: (180° − %d°)/2 = <b>%d°</b>." % (top, b), "°")
        if k == 1:
            b = ri(20, 85)
            return MN("I en likbent triangel är en basvinkel %d°. Hur stor är toppvinkeln?" % b, 180 - 2 * b, [180 - b, 2 * b, 90 - b], "180° − 2 · %d° = <b>%d°</b>." % (b, 180 - 2 * b), "°")
        b = ri(15, 75)
        if b == 45:
            return M("En rätvinklig triangel har en vinkel på 45°. Vilken sorts triangel är det?", "Likbent och rätvinklig", ["Liksidig", "Trubbvinklig", "Likbent och spetsvinklig"], "Den tredje vinkeln är 45°. Två lika vinklar ger en <b>likbent och rätvinklig</b> triangel.")
        return MN("En rätvinklig triangel har en vinkel på %d°. Hur stor är den tredje vinkeln?" % b, 90 - b, [180 - b, 90 + b, b], "180° − 90° − %d° = <b>%d°</b>." % (b, 90 - b), "°")

    def fyr():
        a, b, c = ri(50, 140), ri(50, 140), ri(50, 140)
        e = 360 - a - b - c
        if not 30 <= e <= 170:
            return None
        return MN("En fyrhörning har vinklarna %d°, %d° och %d°. Hur stor är den fjärde vinkeln?" % (a, b, c), e, [180 - e, e + 10, 360 - e, e - 10], "Vinkelsumman i en fyrhörning är 360°. 360° − %d° − %d° − %d° = <b>%d°</b>." % (a, b, c, e), "°")

    def ekv():
        k = ri(0, 2)
        if k == 0:
            m = ch([(1, 2, 3), (1, 2, 6), (2, 3, 4), (1, 1, 2), (1, 3, 5), (2, 3, 5), (1, 4, 4), (3, 4, 5), (2, 2, 5), (1, 3, 8)])
            s = sum(m)
            if 180 % s:
                return None
            x = 180 // s
            ex = ["%sx" % (str(n) if n > 1 else "") for n in m]
            return MN("Vinklarna i en triangel är %s. Hur stor är x?" % lista(ex), x, [180 - s, 360 // s, x * m[-1]], "%s = 180° ger %dx = 180° och <b>x = %d°</b>." % (" + ".join(ex), s, x), "°")
        a = ri(10, 50)
        x = ri(15, 60)
        if 2 * x + a >= 180:
            return None
        return MN("Två sidovinklar är x och 2x + %d°. Hur stor är x?" % a, F(180 - a, 3), [180 - a, F(180, 3), F(180 - a, 2)], "x + 2x + %d° = 180° ger 3x = %d° och <b>x = %s°</b>." % (a, 180 - a, d(F(180 - a, 3))), "°") if (180 - a) % 3 == 0 else None

    sets = [("Vinkelsumman i en triangel", [(triangel, 20)]), ("Sidovinklar och vertikalvinklar", [(kors, 20)]), ("Likbenta och rätvinkliga trianglar", [(likbent, 20)]),
            ("Vinklar i fyrhörningar", [(fyr, 20)]), ("Vinklar med ekvationer", [(ekv, 20)])]
    return unit("vinklar", "G", "Vinklar: vinkelsumma, sidovinklar och vertikalvinklar", "Vinklar",
                "Geometriska objekt och deras egenskaper. Vinklar, vinkelsumman i trianglar och fyrhörningar samt sidovinklar och vertikalvinklar, även med ekvationer.",
                "Arbetsblad om vinklar för årskurs 7: vinkelsumman i en triangel, sidovinklar, vertikalvinklar, likbenta trianglar, fyrhörningar och vinklar med ekvationer. 100 uppgifter med facit.",
                "Triangel 180°, fyrhörning 360°", "Sidovinklar blir 180°, vertikalvinklar är lika stora.", sets,
                ["Vinkelsumman i en triangel är 180° och i en fyrhörning 360°.",
                 "När två linjer skär varandra bildas fyra vinklar. Två vinklar bredvid varandra är sidovinklar och har summan 180°. Två vinklar mitt emot varandra är vertikalvinklar och är lika stora.",
                 "I en likbent triangel är basvinklarna lika stora. I en liksidig triangel är alla vinklar 60°."],
                [("Triangel med 48° och 67°", ["180° − 48° − 67°"], "65°"), ("Sidovinkel till 115°", ["180° − 115°"], "65°")],
                [["Vinkelsumman i en triangel är 360°", "Den är 180°"], ["Vertikalvinklar har summan 180°", "Vertikalvinklar är lika stora, sidovinklar har summan 180°"], ["Basvinkel = 180° − toppvinkeln", "Dela med 2: (180° − toppvinkeln)/2"]],
                [("Varför är vinkelsumman i en triangel 180°?", "Klipp av hörnen och lägg dem bredvid varandra. De bildar en rak vinkel."), ("Vad är en toppvinkel?", "Vinkeln mellan de två lika långa sidorna i en likbent triangel."),
                 ("Hur använder jag ekvationer med vinklar?", "Skriv att summan av vinklarna är 180° eller 360° och lös ut x.")])


# ============================================================ vinklar och polygoner (åk 8)
def polygoner(lv):
    def parallell():
        t = ri(35, 145)
        if 80 <= t <= 100:
            return None
        code = ri(1, 8)
        ask = ch([c for c in range(1, 9) if c != code and (c - 1) % 4 != (code - 1) % 4])
        val = {i: (t if i % 2 == 1 else 180 - t) for i in range(1, 9)}
        v = val[ask]
        same = val[code] == v
        rel = "likbelägna" if (ask - code) % 4 == 0 else "alternatvinklar" if same else "vinklar som tillsammans blir 180°"
        return MN("Linjerna d₁ och d₂ är parallella. Hur stor är vinkeln x?" + kryss(t, {code: "%d°" % val[code], ask: "x"}), v, [180 - v, 360 - v, v + 10], "Vid parallella linjer är vinklarna %s: <b>x = %d°</b>." % ("lika stora" if same else "tillsammans 180°", v), "°")

    def summa():
        n = ri(5, 12)
        S_ = 180 * (n - 2)
        if coin():
            return MN("Hur stor är vinkelsumman i en %d-hörning?" % n, S_, [180 * n, 180 * (n - 1), 360 * (n - 2)], "(n − 2) · 180° = (%d − 2) · 180° = <b>%s°</b>." % (n, num(S_)), "°")
        known = [ri(100, 160) for _ in range(n - 1)]
        x = S_ - sum(known)
        if not 60 <= x <= 175 or n > 6:
            return None
        return MN("En %d-hörning har vinklarna %s och x. Hur stor är x?" % (n, lista("%d°" % v for v in known)), x, [x + 180, 360 - sum(known) % 360 if 360 - sum(known) % 360 != x else x + 10, x - 20], "Vinkelsumman är %s°. %s − %s = <b>%d°</b>." % (num(S_), num(S_), num(sum(known)), x), "°")

    def regelbunden():
        n = ch([3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
        inner = F(180 * (n - 2), n)
        if coin():
            return MN("Hur stor är varje vinkel i en regelbunden %d-hörning?" % n, inner, [F(180 * (n - 2), 1), F(360, n), 180 * (n - 2) // n + 10 if inner.denominator == 1 else 100], "(%d − 2) · 180°/%d = <b>%s°</b>." % (n, n, d(inner)), "°")
        return MN("Hur stor är varje yttervinkel i en regelbunden %d-hörning?" % n, F(360, n), [inner, F(180, n), F(360, n - 1) if F(360, n - 1).denominator == 1 else F(360, n) + 5], "Yttervinklarna har summan 360°: 360°/%d = <b>%s°</b>." % (n, d(F(360, n))), "°")

    def antal():
        k = ri(0, 1)
        n = ch(range(5, 25)) if k == 0 else ch([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
        if k == 0:
            return MN("Vinkelsumman i en månghörning är %s°. Hur många hörn har den?" % num(180 * (n - 2)), n, [n - 2, n + 2, n - 1], "(n − 2) · 180 = %s ger n − 2 = %d och <b>n = %d</b>." % (num(180 * (n - 2)), n - 2, n), "hörn")
        return MN("Varje vinkel i en regelbunden månghörning är %s°. Hur många hörn har den?" % d(F(180 * (n - 2), n)), n, [n - 2, n + 1, F(360, F(180 * (n - 2), n)).limit_denominator() if F(360, F(180 * (n - 2), n)).denominator == 1 and F(360, F(180 * (n - 2), n)) != n else n + 2], "Yttervinkeln är 180° − %s° = %s°. 360°/%s° = <b>%d</b>." % (d(F(180 * (n - 2), n)), d(F(360, n)), d(F(360, n)), n), "hörn")

    def tri_ext():
        a, b = ri(30, 80), ri(30, 80)
        return MN("I en triangel är två vinklar %d° och %d°. Hur stor är yttervinkeln vid det tredje hörnet?" % (a, b), a + b, [180 - a - b, 360 - a - b, a + b + 10], "Yttervinkeln är lika stor som summan av de två motstående vinklarna: <b>%d°</b>." % (a + b), "°")

    sets = [("Vinklar vid parallella linjer", [(parallell, 20)]), ("Vinkelsumman i en månghörning", [(summa, 20)]), ("Regelbundna månghörningar", [(regelbunden, 20)]),
            ("Hur många hörn?", [(antal, 20)]), ("Yttervinklar och blandat", [(tri_ext, 10), (parallell, 10)])]
    return unit("vinklar-och-polygoner", "G", "Vinklar och polygoner: parallella linjer och vinkelsummor", "Vinklar och polygoner",
                "Geometriska objekt och deras egenskaper. Vinklar vid parallella linjer, vinkelsumman i månghörningar och vinklar i regelbundna månghörningar.",
                "Arbetsblad om vinklar och polygoner för årskurs 8: vinklar vid parallella linjer, vinkelsumman i en månghörning, regelbundna månghörningar och yttervinklar. 100 uppgifter med facit.",
                "Vinkelsumma = (n − 2) · 180°", "Yttervinklarna har alltid summan 360°.", sets,
                ["När en linje skär två parallella linjer blir likbelägna vinklar och alternatvinklar lika stora.",
                 "En månghörning med n hörn kan delas i n − 2 trianglar. Vinkelsumman är därför (n − 2) · 180°.",
                 "I en regelbunden månghörning är alla vinklar lika stora. Varje yttervinkel är 360°/n."],
                [("Vinkelsumman i en sexhörning", ["(6 − 2) · 180°"], "720°"), ("Vinkel i regelbunden åttahörning", ["(8 − 2) · 180° = 1 080°", "1 080°/8"], "135°")],
                [["Vinkelsumman är n · 180°", "Den är (n − 2) · 180°"], ["Alternatvinklar har summan 180°", "Alternatvinklar är lika stora"], ["Yttervinkeln i en sexhörning är 120°", "360°/6 = 60°. 120° är innervinkeln"]],
                [("Vad är en yttervinkel?", "Vinkeln mellan en sida och förlängningen av nästa sida. Den och innervinkeln blir 180°."), ("Vad betyder regelbunden?", "Att alla sidor och alla vinklar är lika stora."),
                 ("Fungerar formeln för alla månghörningar?", "Ja, för alla månghörningar utan inåtböjda hörn och även för många med.")])


# ============================================================ omkrets och area (åk 7)
def area(lv):
    def parallellogram():
        b, h = ri(3, 20), ri(2, 15)
        s = h + ri(1, 5)
        pic = poly([(0, 110), (b * 10 + 0, 110), (b * 10 + 40, 30), (40, 30)], [cm(b), "", "", cm(s)], "parallellogram", dashed=[])
        return MN("Parallellogrammet har basen %s, höjden %s och den sneda sidan %s. Vad är arean?" % (cm(b), cm(h), cm(s)) + pic, b * h, [b * s, 2 * (b + s), F(b * h, 2)], "A = b · h = %d · %d = <b>%d cm²</b>. Den sneda sidan används inte." % (b, h, b * h), "cm²")

    def triangel():
        b, h = ri(3, 24), ri(2, 18)
        return MN("En triangel har basen %s och höjden %s. Vad är arean?" % (cm(b), cm(h)), F(b * h, 2), [b * h, b + h, F(b * h, 4)], "A = b · h/2 = %d · %d/2 = <b>%s cm²</b>." % (b, h, d(F(b * h, 2))), "cm²")

    def trapets():
        a, b, h = ri(3, 15), ri(4, 20), ri(2, 12)
        if a == b:
            return None
        return MN("En parallelltrapets har de parallella sidorna %s och %s och höjden %s. Vad är arean?" % (cm(a), cm(b), cm(h)), F((a + b) * h, 2), [(a + b) * h, a * b * h, F(a * b, 2)], "A = (a + b) · h/2 = (%d + %d) · %d/2 = <b>%s cm²</b>." % (a, b, h, d(F((a + b) * h, 2))), "cm²")

    def sammansatt():
        a, b = ri(6, 14), ri(5, 12)
        c, e = ri(2, a - 2), ri(2, b - 2)
        if coin():
            pts = [(0, 0), (a * 12, 0), (a * 12, e * 12), (c * 12, e * 12), (c * 12, b * 12), (0, b * 12)]
            sides = [cm(a), cm(e), "", "", "", cm(b)]
            pic = poly(pts, sides, "sammansatt figur")
            A_ = a * e + c * (b - e)
            tc = cm(c)
            return MN("Figuren är sammansatt av två rektanglar. Den smala delen är %s bred. Vad är arean?" % tc + pic, A_, [a * b, 2 * (a + b), a * b - c * e], "Dela i två rektanglar: %d · %d + %d · %d = <b>%d cm²</b>." % (a, e, c, b - e, A_), "cm²")
        h = ri(3, 10)
        pts = [(0, 60 + h * 10), (a * 12, 60 + h * 10), (a * 12, 60), (a * 6, 0), (0, 60)]
        pic = poly(pts, [cm(a), cm(5), "", "", ""], "rektangel med en triangel ovanpå")
        A_ = a * 5 + F(a * h, 2)
        return MN("Figuren är en rektangel (%s × %s) med en triangel ovanpå. Triangelns höjd är %s. Vad är arean?" % (cm(a), cm(5), cm(h)) + pic, A_, [a * 5 + a * h, a * (5 + h), a * 5], "%d · 5 + %d · %d/2 = <b>%s cm²</b>." % (a, a, h, d(A_)), "cm²")

    def baklanges():
        k = ri(0, 2)
        if k == 0:
            b, h = ri(3, 15), ri(2, 12)
            return MN("En triangel har arean %s cm² och basen %s. Hur hög är den?" % (d(F(b * h, 2)), cm(b)), h, [F(h, 2), b * h, h * 2], "h = 2A/b = %d/%d = <b>%d cm</b>." % (b * h, b, h), "cm")
        if k == 1:
            b, h = ri(3, 20), ri(2, 15)
            return MN("Ett parallellogram har arean %d cm² och höjden %s. Hur lång är basen?" % (b * h, cm(h)), b, [b * h - h, F(b, 2) if b % 2 == 0 else b + 1, b * 2], "b = A/h = %d/%d = <b>%d cm</b>." % (b * h, h, b), "cm")
        a = ri(2, 9) * 100
        return MN("En rektangulär tomt är %s m lång och %s m bred. Hur många kvadratmeter är den?" % (num(a // 10), num(a // 20)), (a // 10) * (a // 20), [2 * (a // 10 + a // 20), a, (a // 10) * (a // 20) * 10], "%d · %d = <b>%s m²</b>." % (a // 10, a // 20, num((a // 10) * (a // 20))), "m²")

    sets = [("Parallellogram", [(parallellogram, 20)]), ("Triangel", [(triangel, 20)]), ("Parallelltrapets", [(trapets, 20)]),
            ("Sammansatta figurer", [(sammansatt, 20)]), ("Räkna baklänges", [(baklanges, 20)])]
    return unit("omkrets-och-area", "G", "Area: parallellogram, triangel, trapets och sammansatta figurer", "Omkrets och area",
                "Metoder för beräkning av area och omkrets hos olika tvådimensionella geometriska figurer, även sammansatta figurer. Geometriska formler.",
                "Arbetsblad om omkrets och area för årskurs 7: parallellogram, triangel, parallelltrapets, sammansatta figurer och att räkna ut en sida baklänges. 100 uppgifter med facit.",
                "Triangel: A = b · h/2", "Höjden står alltid vinkelrätt mot basen.", sets,
                ["Ett parallellogram har arean A = b · h. Höjden mäts vinkelrätt mot basen, inte längs den sneda sidan.",
                 "En triangel är ett halvt parallellogram: A = b · h/2. En parallelltrapets har A = (a + b) · h/2.",
                 "En sammansatt figur delar du i rektanglar och trianglar, räknar ut arean av varje del och lägger ihop."],
                [("Triangel med b = 10 cm och h = 7 cm", ["A = 10 · 7/2"], "35 cm²"), ("Trapets med a = 6, b = 10, h = 4", ["A = (6 + 10) · 4/2"], "32 cm²")],
                [["Använder den sneda sidan som höjd", "Höjden står vinkelrätt mot basen"], ["Triangelns area är b · h", "Dela med 2: b · h/2"], ["Svarar i cm i stället för cm²", "Area har enheten cm², m² och så vidare"]],
                [("Varför delar man med 2 för en triangel?", "Två likadana trianglar bildar ett parallellogram med arean b · h."), ("Vad är skillnaden på omkrets och area?", "Omkretsen är längden runt figuren, arean är ytan inuti."),
                 ("Hur hittar jag höjden?", "Dra en linje från motstående hörn vinkelrätt ner mot basen, eller dess förlängning.")])


# ============================================================ cirkeln (åk 7)
def cirkeln(lv):
    def omkrets():
        r = ri(2, 30)
        if coin():
            return MN("En cirkel har radien %s. Vad är omkretsen? Använd π ≈ 3,14." % cm(r), 2 * PI * r, [PI * r, PI * r * r, 2 * PI * r * r], "O = 2πr = 2 · 3,14 · %d = <b>%s cm</b>." % (r, d(2 * PI * r)), "cm")
        return MN("En cirkel har diametern %s. Vad är omkretsen? Använd π ≈ 3,14." % cm(2 * r), 2 * PI * r, [4 * PI * r, PI * r * r, PI * r], "O = π · d = 3,14 · %d = <b>%s cm</b>." % (2 * r, d(2 * PI * r)), "cm")

    def area_():
        r = ri(2, 30)
        if coin():
            return MN("En cirkel har radien %s. Vad är arean? Använd π ≈ 3,14." % cm(r), PI * r * r, [2 * PI * r, PI * 4 * r * r, PI * r * 2 * r * 2 / 4 * 2], "A = πr² = 3,14 · %d² = <b>%s cm²</b>." % (r, d(PI * r * r)), "cm²")
        return MN("En cirkel har diametern %s. Vad är arean? Använd π ≈ 3,14." % cm(2 * r), PI * r * r, [PI * 4 * r * r, 2 * PI * r, PI * 2 * r], "Radien är %d cm. A = 3,14 · %d² = <b>%s cm²</b>." % (r, r, d(PI * r * r)), "cm²")

    def bak():
        d_ = ri(2, 40)
        k = ri(0, 1)
        if k == 0:
            return MN("En cirkel har omkretsen %s cm. Hur stor är diametern? Använd π ≈ 3,14." % d(PI * d_), d_, [F(d_, 2), d_ * 2, PI * d_ * 2], "d = O/π = %s/3,14 = <b>%d cm</b>." % (d(PI * d_), d_), "cm")
        r = ri(2, 15)
        return MN("En cirkel har arean %s cm². Hur stor är radien? Använd π ≈ 3,14." % d(PI * r * r), r, [r * r, 2 * r, r + 1], "r² = %s/3,14 = %d, så <b>r = %d cm</b>." % (d(PI * r * r), r * r, r), "cm")

    def halv():
        r = ri(2, 20)
        k = ri(0, 1)
        if k == 0:
            return MN("Vad är arean av en halvcirkel med radien %s? Använd π ≈ 3,14." % cm(r), PI * r * r / 2, [PI * r * r, PI * r, 2 * PI * r], "Hälften av πr²: 3,14 · %d²/2 = <b>%s cm²</b>." % (r, d(PI * r * r / 2)), "cm²")
        return MN("Vad är omkretsen av en halvcirkel med diametern %s? Räkna med både bågen och diametern. Använd π ≈ 3,14." % cm(2 * r), PI * r + 2 * r, [PI * r, 2 * PI * r + 2 * r, PI * 2 * r], "Bågen: 3,14 · %d/2 = %s. Plus diametern %d: <b>%s cm</b>." % (2 * r, d(PI * r), 2 * r, d(PI * r + 2 * r)), "cm")

    def vardag():
        k = ri(0, 3)
        if k == 0:
            dd = ch([50, 55, 60, 65, 70])
            n = ri(10, 200)
            v = PI * dd * n / 100
            return MN("Ett cykelhjul har diametern %d cm. Hur långt rullar cykeln när hjulet snurrar %d varv? Svara i meter. Använd π ≈ 3,14." % (dd, n), v, [v * 2, PI * dd * n, v / 2], "Ett varv: 3,14 · %d = %s cm. %d varv: %s cm = <b>%s m</b>." % (dd, d(PI * dd), n, d(PI * dd * n), d(v)), "m")
        if k == 1:
            r = ri(2, 12)
            return MN("En rund matta har radien %s m. Hur många kvadratmeter är den? Använd π ≈ 3,14." % d(r), PI * r * r, [2 * PI * r, PI * r * r * 2, PI * r], "A = 3,14 · %d² = <b>%s m²</b>." % (r, d(PI * r * r)), "m²")
        if k == 2:
            r = ri(3, 20)
            return MN("Ett runt bord har diametern %s dm. Hur lång kant behövs runt bordet? Använd π ≈ 3,14." % d(2 * r), 2 * PI * r, [PI * r * r, PI * r, 4 * PI * r], "O = 3,14 · %d = <b>%s dm</b>." % (2 * r, d(2 * PI * r)), "dm")
        r = ri(2, 10)
        R2 = r + ri(1, 5)
        return MN("En rund rabatt har radien %s m. Runt den läggs en gång så att den yttre radien blir %s m. Vad är gångens area? Använd π ≈ 3,14." % (d(r), d(R2)), PI * (R2 * R2 - r * r), [PI * (R2 - r) ** 2, PI * R2 * R2, 2 * PI * (R2 - r)], "3,14 · %d² − 3,14 · %d² = <b>%s m²</b>." % (R2, r, d(PI * (R2 * R2 - r * r))), "m²")

    sets = [("Omkrets", [(omkrets, 20)]), ("Area", [(area_, 20)]), ("Räkna baklänges", [(bak, 20)]), ("Halvcirklar", [(halv, 20)]), ("Cirklar i vardagen", [(vardag, 20)])]
    return unit("cirkeln", "G", "Cirkeln: omkrets, area och π", "Cirkeln",
                "Metoder för beräkning av area och omkrets hos olika tvådimensionella geometriska figurer, bland annat cirklar. Talet π.",
                "Arbetsblad om cirkeln för årskurs 7: omkrets och area med radie och diameter, räkna baklänges, halvcirklar och cirklar i vardagen. 100 uppgifter med facit.",
                "O = πd = 2πr och A = πr²", "π ≈ 3,14. Radien är halva diametern.", sets,
                ["Radien r är avståndet från medelpunkten till cirkeln. Diametern d är dubbelt så lång: d = 2r.",
                 "Omkretsen är O = π · d = 2πr, där π ≈ 3,14.",
                 "Arean är A = πr². Har du diametern delar du först med 2 för att få radien."],
                [("Radie 5 cm. Omkrets?", ["O = 2 · 3,14 · 5"], "31,4 cm"), ("Diameter 10 cm. Area?", ["r = 5 cm", "A = 3,14 · 5²"], "78,5 cm²")],
                [["Area med diametern: π · 10²", "Använd radien: π · 5²"], ["A = 2πr", "2πr är omkretsen, arean är πr²"], ["πr² = (π · r)²", "Bara r upphöjs: π · r · r"]],
                [("Vad är π?", "Förhållandet mellan omkretsen och diametern i alla cirklar, ungefär 3,14159."), ("Varför ska jag använda 3,14?", "Det är ett närmevärde som räcker för de flesta beräkningar. Miniräknarens π-knapp ger fler decimaler."),
                 ("Vilken enhet har arean?", "Kvadratenheter, till exempel cm² eller m².")])


# ============================================================ enheter (åk 7)
def enheter(lv):
    LEN = [("mm", F(1, 1000)), ("cm", F(1, 100)), ("dm", F(1, 10)), ("m", F(1)), ("km", F(1000)), ("mil", F(10000))]
    AREA = [("mm²", F(1, 10 ** 6)), ("cm²", F(1, 10 ** 4)), ("dm²", F(1, 100)), ("m²", F(1)), ("km²", F(10 ** 6))]
    VOL = [("ml", F(1, 1000)), ("cl", F(1, 100)), ("dl", F(1, 10)), ("liter", F(1)), ("cm³", F(1, 1000)), ("dm³", F(1)), ("m³", F(1000))]

    def conv(T, close=2):
        i = ri(0, len(T) - 1)
        j = ri(max(0, i - close), min(len(T) - 1, i + close))
        if i == j:
            return None
        a, fa = T[i]
        b, fb = T[j]
        x = F(ri(2, 999), ch([1, 10, 100]))
        v = x * fa / fb
        if (v * 10 ** 6).denominator != 1 or v > 10 ** 7:
            return None
        r = fb / fa
        try:
            w = [d(x * fb / fa), d(v * 10), d(v / 10)]
        except ValueError:
            return None
        return M("Hur mycket är %s %s i %s?" % (d(x), a, b), d(v) + NB + b, [z + NB + b for z in w], "1 %s = %s %s. %s %s = <b>%s %s</b>." % (a, d(fa / fb), b, d(x), a, d(v), b))

    def langd():
        return conv(LEN)

    def area_():
        return conv(AREA, 1)

    def vol():
        return conv(VOL, 2)

    def massa():
        T = [("mg", F(1, 1000)), ("g", F(1)), ("hg", F(100)), ("kg", F(1000)), ("ton", F(10 ** 6))]
        return conv(T, 2)

    def vardag():
        k = ri(0, 3)
        if k == 0:
            l, b, h = ri(2, 9) * 10, ri(2, 6) * 10, ri(1, 5) * 10
            v = F(l * b * h, 1000)
            return MN("Ett akvarium är %d cm långt, %d cm brett och %d cm högt. Hur många liter rymmer det?" % (l, b, h), v, [v * 10, l * b * h, v / 10], "%d · %d · %d = %s cm³ = <b>%s liter</b>, eftersom 1 liter = 1 000 cm³." % (l, b, h, num(l * b * h), d(v)), "liter")
        if k == 1:
            l, b = ri(3, 12), ri(2, 9)
            return MN("Ett golv är %d m långt och %d m brett. Hur många kvadratdecimeter är det?" % (l, b), l * b * 100, [l * b * 10, l * b, l * b * 1000], "%d · %d = %d m² = <b>%s dm²</b>, eftersom 1 m² = 100 dm²." % (l, b, l * b, num(l * b * 100)), "dm²")
        if k == 2:
            n = ri(3, 30)
            s = ri(12, 50) * 10
            return MN("%d glas med %d ml i varje fylls från en kanna. Hur många liter behövs?" % (n, s), F(n * s, 1000), [F(n * s, 100), n * s, F(n * s, 10000)], "%d · %d = %s ml = <b>%s liter</b>." % (n, s, num(n * s), d(F(n * s, 1000))), "liter")
        km_ = ri(5, 95)
        return MN("Avståndet mellan två orter är %d mil. Hur många kilometer är det?" % km_, km_ * 10, [km_, km_ * 100, F(km_, 10)], "1 mil = 10 km. %d mil = <b>%d km</b>." % (km_, km_ * 10), "km")

    sets = [("Längd", [(langd, 20)]), ("Area", [(area_, 20)]), ("Volym", [(vol, 20)]), ("Massa", [(massa, 20)]), ("Enheter i vardagen", [(vardag, 20)])]
    return unit("enheter", "G", "Enheter: längd, area, volym och massa", "Enheter",
                "Jämförelse, uppskattning och mätning av längd, area, volym, massa och tid med lämpliga måttenheter samt omvandling mellan enheter.",
                "Arbetsblad om enheter för årskurs 7: omvandla enheter för längd, area, volym och massa samt enheter i vardagen. 100 uppgifter med facit.",
                "1 m² = 100 dm², 1 dm³ = 1 liter", "För area är steget 100, för volym 1 000.", sets,
                ["Längdenheterna går i steg om 10: 1 m = 10 dm = 100 cm = 1 000 mm. 1 mil = 10 km.",
                 "För area är steget 100 eftersom det är två dimensioner: 1 m² = 100 dm² = 10 000 cm².",
                 "För volym är steget 1 000: 1 dm³ = 1 000 cm³. 1 dm³ = 1 liter och 1 cm³ = 1 ml."],
                [("3,5 m² i dm²", ["1 m² = 100 dm²", "3,5 · 100"], "350 dm²"), ("2 400 cm³ i liter", ["1 000 cm³ = 1 liter", "2 400 : 1 000"], "2,4 liter")],
                [["1 m² = 10 dm²", "1 m² = 100 dm²"], ["1 dm³ = 100 cm³", "1 dm³ = 1 000 cm³"], ["1 mil = 1 km", "1 mil = 10 km"]],
                [("Varför är steget 100 för area?", "En kvadrat på 1 m · 1 m är 10 dm · 10 dm = 100 dm²."), ("Hur många liter är 1 m³?", "1 000 liter."),
                 ("Vad betyder prefixen?", "Milli = tusendel, centi = hundradel, deci = tiondel, kilo = tusen.")])


# ============================================================ skala (åk 8)
def skala(lv):
    def karta():
        s = ch([10000, 20000, 25000, 50000, 100000, 200000, 500000])
        c = ri(2, 15)
        v = F(c * s, 100000)
        return MN("En karta har skalan 1 : %s. Avståndet på kartan är %s. Hur långt är det i verkligheten?" % (num(s), cm(c)), v, [v * 10, v / 10, F(c * s, 1000)], "%d cm · %s = %s cm = <b>%s km</b>." % (c, num(s), num(c * s), d(v)), "km")

    def tillkarta():
        s = ch([10000, 20000, 25000, 50000, 100000, 200000])
        km_ = F(ri(1, 30), 2)
        c = km_ * 100000 / s
        if (c * 10).denominator != 1:
            return None
        return MN("Två orter ligger %s km från varandra. Hur långt är det på en karta med skalan 1 : %s?" % (d(km_), num(s)), c, [c * 10, c / 10, km_ * s], "%s km = %s cm. %s/%s = <b>%s cm</b>." % (d(km_), num(int(km_ * 100000)), num(int(km_ * 100000)), num(s), d(c)), "cm")

    def bestam():
        k = ri(0, 1)
        if k == 0:
            s = ch([50, 100, 200, 500, 1000, 2000])
            m = ri(2, 20)
            c = F(m * 100, s)
            if (c * 10).denominator != 1:
                return None
            return M("Ett rum är %d m långt. På en ritning är det %s cm. Vilken skala har ritningen?" % (m, d(c)), "1 : %s" % num(s), ["1 : %s" % num(s * 10), "1 : %s" % num(s // 10) if s >= 100 else "1 : %d" % (s * 2), "%s : 1" % num(s)], "%d m = %s cm. %s/%s = %s: <b>1 : %s</b>." % (m, num(m * 100), num(m * 100), d(c), num(s), num(s)))
        f = ch([2, 3, 4, 5, 10, 20, 50])
        mm = ri(2, 9)
        return M("En myra är %d mm lång. På en bild är den %d mm. Vilken skala har bilden?" % (mm, mm * f), "%d : 1" % f, ["1 : %d" % f, "%d : 1" % (f * mm), "%d : 1" % (f * 10)], "Bilden är %d gånger större: <b>%d : 1</b>. Det är en förstoring." % (f, f))

    def forstoring():
        f = ch([2, 3, 4, 5, 10])
        mm = ri(2, 30)
        if coin():
            return MN("En bild är förstorad i skalan %d : 1. Ett frö är %s mm på bilden. Hur stort är det i verkligheten?" % (f, d(mm * f)), mm, [mm * f * f, mm * f + f, F(mm, f)], "%d/%d = <b>%d mm</b>." % (mm * f, f, mm), "mm")
        s = ch([10, 20, 50, 100])
        c = ri(2, 30)
        return MN("En modellbil är byggd i skalan 1 : %d och är %s lång. Hur lång är den riktiga bilen i meter?" % (s, cm(c)), F(c * s, 100), [c * s, F(c * s, 10), F(c, s)], "%d · %d = %s cm = <b>%s m</b>." % (c, s, num(c * s), d(F(c * s, 100))), "m")

    def areaskala():
        k = ch([2, 3, 4, 5, 10])
        a = ri(2, 30)
        if coin():
            return MN("En figur förstoras i längdskalan %d : 1. Arean var %d cm². Vad blir den nya arean?" % (k, a), a * k * k, [a * k, a * k * 2, a + k * k], "Areaskalan är %d² : 1 = %d : 1. %d · %d = <b>%s cm²</b>." % (k, k * k, a, k * k, num(a * k * k)), "cm²")
        s = ch([100, 1000, 2000, 5000])
        c = ri(2, 12)
        return MN("På en ritning i skalan 1 : %s är en tomt %d cm². Hur stor är tomten i verkligheten i m²?" % (num(s), c), F(c * s * s, 10000), [F(c * s, 10000), F(c * s * s, 100), F(c * s, 100)], "Areaskala 1 : %s². %d · %s cm² = %s m²: <b>%s m²</b>." % (num(s), c, num(s * s), d(F(c * s * s, 10000)), d(F(c * s * s, 10000))), "m²")

    sets = [("Från karta till verklighet", [(karta, 20)]), ("Från verklighet till karta", [(tillkarta, 20)]), ("Bestäm skalan", [(bestam, 20)]),
            ("Förstoring och modeller", [(forstoring, 20)]), ("Area och skala", [(areaskala, 20)])]
    return unit("skala", "G", "Skala: kartor, ritningar, förstoring och areaskala", "Skala",
                "Skala vid förminskning och förstoring av två- och tredimensionella objekt. Avbildning och konstruktion av geometriska objekt, kartor och ritningar.",
                "Arbetsblad om skala för årskurs 8: kartor och ritningar, från verklighet till karta, bestäm skalan, förstoring, modeller och areaskala. 100 uppgifter med facit.",
                "1 : 50 000 betyder 1 cm = 50 000 cm", "Areaskalan är längdskalan i kvadrat.", sets,
                ["Skalan 1 : 50 000 betyder att 1 cm på kartan är 50 000 cm = 500 m i verkligheten.",
                 "En förstoring har skalan med det större talet först: 5 : 1 betyder att bilden är 5 gånger större.",
                 "När längderna förstoras k gånger blir arean k² gånger större."],
                [("4 cm på en karta i 1 : 25 000", ["4 · 25 000 = 100 000 cm"], "1 km"), ("Längdskala 3 : 1, area 8 cm²", ["Areaskala 9 : 1", "8 · 9"], "72 cm²")],
                [["1 : 100 är en förstoring", "1 : 100 är en förminskning, 100 : 1 är en förstoring"], ["Areaskalan är samma som längdskalan", "Areaskalan är längdskalan i kvadrat"], ["Glömmer att byta enhet", "Räkna först i cm och byt sedan till m eller km"]],
                [("Vad betyder skala 1 : 1?", "Att bilden är lika stor som verkligheten."), ("Varför kvadrat för area?", "Både längden och bredden förstoras, alltså två gånger."),
                 ("Hur omvandlar jag snabbt?", "1 km = 100 000 cm och 1 m = 100 cm.")])


# ============================================================ prisma och cylinder (åk 8)
def volym8(lv):
    def ratblock():
        a, b, c = ri(2, 15), ri(2, 12), ri(2, 10)
        return MN("Vad är volymen av rätblocket?" + box(a, b, c), a * b * c, [2 * (a * b + a * c + b * c), a + b + c, a * b], "V = l · b · h = %d · %d · %d = <b>%s cm³</b>." % (a, b, c, num(a * b * c)), "cm³")

    def prisma():
        b, h, l = ri(2, 12), ri(2, 10), ri(3, 15)
        B = F(b * h, 2)
        return MN("Prismats bas är en triangel med basen %s och höjden %s. Prismat är %s långt. Vad är volymen?" % (cm(b), cm(h), cm(l)) + fig(solid("prisma", cm(b), cm(h), cm(l))), B * l, [b * h * l, B + l, B * 2 * l + 1], "V = B · h = %s · %d = <b>%s cm³</b>." % (d(B), l, d(B * l)), "cm³")

    def cylinder():
        r, h = ri(2, 12), ri(2, 20)
        V = PI * r * r * h
        return MN("En cylinder har radien %s och höjden %s. Vad är volymen? Använd π ≈ 3,14." % (cm(r), cm(h)) + fig(solid("cylinder", "r = " + cm(r), "h = " + cm(h))), V, [2 * PI * r * h, PI * 4 * r * r * h, PI * r * h], "V = πr²h = 3,14 · %d² · %d = <b>%s cm³</b>." % (r, h, d(V)), "cm³")

    def liter():
        k = ri(0, 1)
        if k == 0:
            r, h = ri(2, 6), ri(5, 30)
            V = PI * r * r * h
            return M("En burk är en cylinder med radien %s cm och höjden %s cm. Hur många liter rymmer den? Använd π ≈ 3,14 och avrunda till två decimaler." % (d(r), d(h)), rd(V / 1000, 2) + NB + "liter", [rd(V / 100, 2) + NB + "liter", rd(V / 10000, 2) + NB + "liter", rd(2 * PI * r * h / 1000, 2) + NB + "liter"], "V = 3,14 · %d² · %d = %s cm³ ≈ <b>%s liter</b>." % (r, h, d(V), rd(V / 1000, 2)))
        a, b, c = ri(2, 10), ri(2, 8), ri(2, 6)
        return MN("En container är %d m lång, %d m bred och %d m hög. Hur många liter rymmer den?" % (a, b, c), a * b * c * 1000, [a * b * c, a * b * c * 100, a * b * c * 10], "%d m³ = <b>%s liter</b>, eftersom 1 m³ = 1 000 liter." % (a * b * c, num(a * b * c * 1000)), "liter")

    def bak():
        k = ri(0, 1)
        if k == 0:
            a, b, c = ri(2, 15), ri(2, 12), ri(2, 10)
            return MN("Ett rätblock har volymen %d cm³. Basen är %d cm × %d cm. Hur högt är det?" % (a * b * c, a, b), c, [a * b * c - a * b, c * 2, a * b], "h = V/B = %d/%d = <b>%d cm</b>." % (a * b * c, a * b, c), "cm")
        r, h = ri(2, 10), ri(2, 20)
        V = PI * r * r * h
        return MN("En cylinder har volymen %s cm³ och radien %d cm. Hur hög är den? Använd π ≈ 3,14." % (d(V), r), h, [h * r, F(h, 2) if h % 2 == 0 else h + 1, h * 2], "Basytan är 3,14 · %d² = %s. h = %s/%s = <b>%d cm</b>." % (r, d(PI * r * r), d(V), d(PI * r * r), h), "cm")

    sets = [("Rätblock", [(ratblock, 20)]), ("Prisma", [(prisma, 20)]), ("Cylinder", [(cylinder, 20)]), ("Volym i liter", [(liter, 20)]), ("Räkna baklänges", [(bak, 20)])]
    return unit("prisma-och-cylinder", "G", "Volym: rätblock, prisma och cylinder", "Prisma och cylinder",
                "Metoder för beräkning av volym hos olika tredimensionella geometriska objekt, till exempel prismor och cylindrar. Geometriska formler och enheter för volym.",
                "Arbetsblad om volym för årskurs 8: rätblock, prisma med triangulär bas, cylinder, volym i liter och att räkna baklänges. 100 uppgifter med facit.",
                "Volym = basyta · höjd", "Gäller för alla prismor och cylindrar.", sets,
                ["Ett prisma har samma tvärsnitt hela vägen. Volymen är basytan gånger höjden: V = B · h.",
                 "En cylinder har en cirkel som bas: V = πr² · h.",
                 "1 dm³ = 1 liter och 1 m³ = 1 000 liter."],
                [("Cylinder med r = 3 cm och h = 10 cm", ["V = 3,14 · 3² · 10"], "282,6 cm³"), ("Triangelprisma: b = 4, h = 3, längd 10", ["B = 4 · 3/2 = 6", "V = 6 · 10"], "60 cm³")],
                [["Cylinderns volym = πr · h", "Radien ska i kvadrat: πr² · h"], ["Triangelprismats basyta = b · h", "Triangeln: b · h/2"], ["1 m³ = 100 liter", "1 m³ = 1 000 liter"]],
                [("Vad är en basyta?", "Arean av den yta som prismat eller cylindern står på."), ("Hur vet jag vad som är höjden?", "Höjden är avståndet mellan de två lika basytorna."),
                 ("Varför är 1 dm³ en liter?", "Det är definitionen av en liter.")])


# ============================================================ begränsningsarea (åk 8)
def begransning(lv):
    def kub():
        s = ri(2, 15)
        u = ch(["cm", "dm", "m"])
        if coin():
            return MN("Vad är begränsningsarean av en kub med sidan %s?" % cm(s, u), 6 * s * s, [s ** 3, 4 * s * s, 12 * s], "En kub har 6 lika sidor: 6 · %d² = <b>%d %s²</b>." % (s, 6 * s * s, u), u + "²")
        return MN("En kub har begränsningsarean %s %s². Hur lång är en sida?" % (num(6 * s * s), u), s, [s * s, 6 * s, F(6 * s * s, 4)], "En sida har arean %s/6 = %d %s². √%d = <b>%d %s</b>." % (num(6 * s * s), s * s, u, s * s, s, u), u)

    def ratblock():
        a, b, c = ri(2, 12), ri(2, 10), ri(2, 9)
        A_ = 2 * (a * b + a * c + b * c)
        return MN("Vad är begränsningsarean av rätblocket?" + box(a, b, c), A_, [a * b * c, a * b + a * c + b * c, 6 * a * b], "2 · (%d · %d + %d · %d + %d · %d) = <b>%d cm²</b>." % (a, b, a, c, b, c, A_), "cm²")

    def cylinder():
        r, h = ri(2, 10), ri(2, 20)
        A_ = 2 * PI * r * r + 2 * PI * r * h
        if coin():
            return MN("En cylinder har radien %s och höjden %s. Vad är begränsningsarean? Använd π ≈ 3,14." % (cm(r), cm(h)) + fig(solid("cylinder", "r = " + cm(r), "h = " + cm(h))), A_, [PI * r * r * h, 2 * PI * r * h, PI * r * r + 2 * PI * r * h], "Två cirklar: 2 · 3,14 · %d² = %s. Mantel: 2 · 3,14 · %d · %d = %s. Summa <b>%s cm²</b>." % (r, d(2 * PI * r * r), r, h, d(2 * PI * r * h), d(A_)), "cm²")
        return MN("Vad är mantelytan (sidan utan lock och botten) av en cylinder med radien %s och höjden %s? Använd π ≈ 3,14." % (cm(r), cm(h)), 2 * PI * r * h, [PI * r * h, A_, PI * r * r * h], "Mantelytan är en rektangel: omkretsen · höjden = 2 · 3,14 · %d · %d = <b>%s cm²</b>." % (r, h, d(2 * PI * r * h)), "cm²")

    def prisma():
        a, b = ch([(3, 4), (6, 8), (5, 12), (9, 12), (8, 15)])
        c = int(math.hypot(a, b))
        l = ri(3, 15)
        A_ = a * b + (a + b + c) * l
        return MN("Ett prisma har en rätvinklig triangel som bas med sidorna %s, %s och %s. Prismat är %s långt. Vad är begränsningsarean?" % (cm(a), cm(b), cm(c), cm(l)), A_, [F(a * b, 2) * l, a * b * l, (a + b + c) * l], "Två trianglar: 2 · %d · %d/2 = %d. Tre rektanglar: (%d + %d + %d) · %d = %d. Summa <b>%d cm²</b>." % (a, b, a * b, a, b, c, l, (a + b + c) * l, A_), "cm²")

    def vardag():
        k = ri(0, 2)
        if k == 0:
            l, b, h = ri(3, 8), ri(3, 6), ri(2, 3)
            A_ = 2 * (l * h + b * h)
            return MN("Väggarna i ett rum ska målas. Rummet är %d m långt, %d m brett och %d m högt. Hur stor är väggytan (utan fönster och dörr)?" % (l, b, h), A_, [l * b * h, 2 * (l * b + l * h + b * h), l * b], "2 · %d · %d + 2 · %d · %d = <b>%d m²</b>." % (l, h, b, h, A_), "m²")
        if k == 1:
            a, b, c = ri(10, 40), ri(10, 30), ri(5, 20)
            A_ = 2 * (a * b + a * c + b * c)
            return MN("En kartong utan lock ska tillverkas. Den är %d cm lång, %d cm bred och %d cm hög. Hur mycket kartong går åt?" % (a, b, c), A_ - a * b, [A_, a * b * c, A_ - 2 * a * b], "Botten och fyra sidor: %d + 2 · %d + 2 · %d = <b>%s cm²</b>." % (a * b, a * c, b * c, num(A_ - a * b)), "cm²")
        r, h = ri(3, 6), ri(8, 15)
        return MN("En etikett ska täcka hela sidan på en burk med radien %d cm och höjden %d cm. Hur stor är etiketten? Använd π ≈ 3,14." % (r, h), 2 * PI * r * h, [PI * r * h, PI * r * r * h, 2 * PI * r * r + 2 * PI * r * h], "2 · 3,14 · %d · %d = <b>%s cm²</b>." % (r, h, d(2 * PI * r * h)), "cm²")

    sets = [("Kub", [(kub, 20)]), ("Rätblock", [(ratblock, 20)]), ("Cylinder", [(cylinder, 20)]), ("Prisma", [(prisma, 20)]), ("Begränsningsarea i vardagen", [(vardag, 20)])]
    return unit("begransningsarea", "G", "Begränsningsarea: kub, rätblock, prisma och cylinder", "Begränsningsarea",
                "Metoder för beräkning av area hos tredimensionella geometriska objekt. Begränsningsarea hos kuber, rätblock, prismor och cylindrar.",
                "Arbetsblad om begränsningsarea för årskurs 8: kub, rätblock, cylinder, prisma med triangulär bas och vardagsproblem som att måla väggar. 100 uppgifter med facit.",
                "Lägg ihop arean av alla sidoytor", "Tänk dig kroppen uppvecklad som ett nät.", sets,
                ["Begränsningsarean är den sammanlagda arean av alla ytor som begränsar kroppen.",
                 "Ett rätblock har tre par lika stora sidor: A = 2(lb + lh + bh).",
                 "En cylinder har två cirklar och en mantelyta. Mantelytan är en rektangel med omkretsen 2πr som bredd: A = 2πr² + 2πrh."],
                [("Kub med sidan 4 cm", ["6 · 4²"], "96 cm²"), ("Cylinder r = 2 cm, h = 5 cm", ["2 · 3,14 · 2² = 25,12", "2 · 3,14 · 2 · 5 = 62,8"], "87,92 cm²")],
                [["Räknar volymen i stället", "Volymen är cm³, arean cm²"], ["Bara tre sidor av rätblocket", "Varje sida finns två gånger"], ["Glömmer cylinderns lock och botten", "Två cirklar plus mantelytan"]],
                [("Vad är skillnaden på volym och begränsningsarea?", "Volymen är hur mycket som får plats inuti. Begränsningsarean är hur mycket material som behövs utanpå."),
                 ("Vad är ett nät?", "En kropp som har vecklats ut och lagts platt."), ("Varför är mantelytan en rektangel?", "Om du klipper upp en toarulle blir pappret en rektangel.")])


# ============================================================ Pythagoras sats (åk 9)
TRIP = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (7, 24, 25), (9, 12, 15), (12, 16, 20), (15, 20, 25), (9, 40, 41), (20, 21, 29), (10, 24, 26), (12, 35, 37), (15, 36, 39), (18, 24, 30), (16, 30, 34)]


def pythagoras(lv):
    def rtri(a, b, la, lb, lc):
        pts = [(0, 0), (a * 160.0 / max(a, b), 0), (0, b * 160.0 / max(a, b))]
        P = [(x, 170 - y) for x, y in pts]
        return poly(P, [la, lc, lb], "rätvinklig triangel", rights=[0], unit_="")

    def hyp():
        a, b, c = ch(TRIP)
        m = ch([1, 1, 2, 3]) if c <= 15 else 1
        a, b, c = a * m, b * m, c * m
        if coin():
            a, b = b, a
        return MN("Hur lång är hypotenusan x?" + rtri(a, b, cm(a), cm(b), "x"), c, [a + b, abs(b - a) + c if False else a * b // 2 if a * b // 2 not in (c, a + b) else c + 1, c + 2], "x² = %d² + %d² = %d. x = √%d = <b>%d cm</b>." % (a, b, c * c, c * c, c), "cm")

    def katet():
        a, b, c = ch(TRIP)
        m = ch([1, 1, 2, 3]) if c <= 15 else 1
        a, b, c = a * m, b * m, c * m
        if coin():
            a, b = b, a
        return MN("Hur lång är kateten x?" + rtri(a, b, cm(a), "x", cm(c)), b, [c - a, c + a, int(round(math.hypot(a, c)))] if int(round(math.hypot(a, c))) not in (b, c - a, c + a) else [c - a, c + a, b + 1], "x² = %d² − %d² = %d. x = √%d = <b>%d cm</b>." % (c, a, b * b, b * b, b), "cm")

    def ungef():
        a, b = ri(2, 15), ri(2, 15)
        c = math.hypot(a, b)
        if abs(c - round(c)) < 1e-9:
            return None
        if coin():
            return M("En rätvinklig triangel har kateterna %s och %s. Hur lång är hypotenusan? Avrunda till en decimal." % (cm(a), cm(b)), rd(c, 1) + NB + "cm", [rd(a + b, 1) + NB + "cm", rd(c + 0.5, 1) + NB + "cm", rd(math.sqrt(abs(a * a - b * b)), 1) + NB + "cm" if a != b else rd(c - 1, 1) + NB + "cm"], "√(%d² + %d²) = √%d ≈ <b>%s cm</b>." % (a, b, a * a + b * b, rd(c, 1)))
        hh = max(a, b) + ri(1, 6)
        k = min(a, b)
        v = math.sqrt(hh * hh - k * k)
        if abs(v - round(v)) < 1e-9:
            return None
        return M("En rätvinklig triangel har hypotenusan %s och en katet %s. Hur lång är den andra kateten? Avrunda till en decimal." % (cm(hh), cm(k)), rd(v, 1) + NB + "cm", [rd(math.hypot(hh, k), 1) + NB + "cm", rd(hh - k, 1) + NB + "cm", rd(v + 1, 1) + NB + "cm"], "√(%d² − %d²) = √%d ≈ <b>%s cm</b>." % (hh, k, hh * hh - k * k, rd(v, 1)))

    def ratv():
        if coin():
            a, b, c = ch(TRIP)
            m = ri(1, 3)
            r = "%d cm, %d cm och %d cm" % (a * m, b * m, c * m)
            w = ["%d cm, %d cm och %d cm" % (a * m, b * m, c * m + 1), "%d cm, %d cm och %d cm" % (a * m + 1, b * m, c * m), "%d cm, %d cm och %d cm" % (a * m, b * m + 2, c * m + 1)]
            return MQ("Vilken triangel är rätvinklig:", r, w, "%d² + %d² = %d = %d²: <b>%s</b>." % (a * m, b * m, (c * m) ** 2, c * m, r))
        a, b = ri(3, 12), ri(3, 12)
        c = ri(max(a, b) + 1, a + b - 1)
        s = a * a + b * b
        ok = s == c * c
        return M("Är en triangel med sidorna %d cm, %d cm och %d cm rätvinklig?" % (a, b, c), "Ja, %d² + %d² = %d²" % (a, b, c) if ok else "Nej, %d² + %d² = %d men %d² = %d" % (a, b, s, c, c * c), ["Ja, %d² + %d² = %d²" % (a, b, c) if not ok else "Nej, %d + %d > %d" % (a, b, c), "Ja, alla trianglar med en lång sida är rätvinkliga", "Nej, sidorna måste vara lika långa"],
                 "Jämför %d² + %d² = %d med %d² = %d: <b>%s</b>." % (a, b, s, c, c * c, "ja" if ok else "nej"))

    def vardag():
        k = ri(0, 3)
        a, b, c = ch(TRIP[:10])
        m = ch([1, F(1, 2), F(1, 10)]) if k < 3 else 1
        if k == 0:
            return MN("En stege som är %s m lång står mot en vägg. Stegens fot är %s m från väggen. Hur högt upp når stegen?" % (d(c * m), d(a * m)), b * m, [(c - a) * m, (c + a) * m, c * m], "√(%s² − %s²) = <b>%s m</b>." % (d(c * m), d(a * m), d(b * m)), "m")
        if k == 1:
            return MN("En rektangulär tomt är %s m lång och %s m bred. Hur lång är diagonalen?" % (d(b * m), d(a * m)), c * m, [(a + b) * m, (b - a) * m, c * m + 1], "√(%s² + %s²) = <b>%s m</b>." % (d(b * m), d(a * m), d(c * m)), "m")
        if k == 2:
            return MN("%s går %s km rakt norrut och sedan %s km rakt österut. Hur långt är det fågelvägen tillbaka till starten?" % (K().name(), d(a * m), d(b * m)), c * m, [(a + b) * m, (b - a) * m, c * m + 1], "√(%s² + %s²) = <b>%s km</b>." % (d(a * m), d(b * m), d(c * m)), "km")
        x1, y1 = nz(-6, 6), nz(-6, 6)
        x2, y2 = x1 + a, y1 + b
        return MN("Hur långt är det mellan punkterna (%s, %s) och (%s, %s) i ett koordinatsystem?" % (d(x1), d(y1), d(x2), d(y2)), c, [a + b, abs(x2 - x1) + abs(y2 - y1) - 1, c + 1], "Skillnaderna är %d och %d. √(%d² + %d²) = <b>%d</b>." % (a, b, a, b, c), "längdenheter")

    sets = [("Beräkna hypotenusan", [(hyp, 20)]), ("Beräkna en katet", [(katet, 20)]), ("Ungefärliga svar", [(ungef, 20)]),
            ("Är triangeln rätvinklig?", [(ratv, 20)]), ("Pythagoras i vardagen", [(vardag, 20)])]
    return unit("pythagoras-sats", "G", "Pythagoras sats: hypotenusa, kateter och rätvinkliga trianglar", "Pythagoras sats",
                "Geometriska satser och formler och behovet av argumentation för deras giltighet. Pythagoras sats och dess användning i vardagliga och matematiska situationer.",
                "Arbetsblad om Pythagoras sats för årskurs 9: beräkna hypotenusan och en katet, ungefärliga svar, avgör om en triangel är rätvinklig och vardagsproblem. 100 uppgifter med facit.",
                "a² + b² = c²", "c är hypotenusan, mitt emot den räta vinkeln.", sets,
                ["I en rätvinklig triangel kallas de två sidorna vid den räta vinkeln kateter och den längsta sidan hypotenusa.",
                 "Pythagoras sats: a² + b² = c², där c är hypotenusan.",
                 "Söker du en katet drar du bort i stället: a² = c² − b². Satsen gäller också omvänt: om a² + b² = c² är triangeln rätvinklig."],
                [("Kateter 6 cm och 8 cm", ["c² = 36 + 64 = 100", "c = √100"], "10 cm"), ("Hypotenusa 13 cm, katet 5 cm", ["a² = 169 − 25 = 144", "a = √144"], "12 cm")],
                [["c = a + b", "c² = a² + b², c = √(a² + b²)"], ["Adderar när kateten söks", "Subtrahera: a² = c² − b²"], ["Glömmer att dra roten ur", "c² = 100 betyder c = 10"]],
                [("Gäller satsen för alla trianglar?", "Nej, bara för rätvinkliga trianglar."), ("Vad är en pythagoreisk trippel?", "Tre heltal som passar i satsen, till exempel 3, 4, 5 och 5, 12, 13."),
                 ("Vem var Pythagoras?", "En grekisk matematiker som levde på 500-talet före vår tideräkning. Satsen var känd ännu tidigare.")])


# ============================================================ likformighet (åk 9)
def likformighet(lv):
    def skal():
        a, b, c = ri(3, 12), ri(3, 12), ri(3, 12)
        k = ch([F(2), F(3), F(3, 2), F(5, 2), F(4), F(1, 2)])
        A2, B2 = a * k, b * k
        if (A2 * 10).denominator != 1 or (B2 * 10).denominator != 1 or a == b:
            return None
        return MN("Två trianglar är likformiga. I den lilla är sidorna %s och %s. I den stora motsvarar sidan %s den lilla sidan %s. Hur lång är den sida som motsvarar %s?" % (cm(a), cm(b), cm(A2), cm(a), cm(b)), B2, [b + A2 - a, b * a, B2 + 1], "Skalfaktorn är %s/%d = %s. %d · %s = <b>%s cm</b>." % (d(A2), a, d(k), b, d(k), d(B2)), "cm")

    def topp():
        h1, b1 = ri(2, 8), ri(2, 8)
        k = ri(2, 4)
        H, B = h1 * k, b1 * k
        pts = [(0, 0), (B * 18, 0), (0, H * 18)]
        mid = [(0, (H - h1) * 18), (b1 * 18, (H - h1) * 18)]
        P = [(x, 200 - y) for x, y in pts]
        Q = [(x, 200 - y) for x, y in mid]
        svg = tr_g.poly(P, ["", "", ""], (), "", "triangel med en parallell linje", rights=[0])
        svg = svg.replace("</svg>", "%s</svg>" % line(Q[0][0] + 50 - min(p[0] for p in P), Q[0][1] + 30 - min(p[1] for p in P), Q[1][0] + 50 - min(p[0] for p in P), Q[1][1] + 30 - min(p[1] for p in P), RED, 2.4))
        return MN("I en rätvinklig triangel är höjden %s och basen %s. En linje parallell med basen dras %s under toppen. Hur lång är linjen?" % (cm(H), cm(B), cm(h1)) + fig(rl(svg, "triangel med en parallell linje")), b1, [B - (H - h1), F(B, 2) if B % 2 == 0 else b1 + 1, h1], "Topptriangeln är likformig med hela: %d/%d = x/%d ger <b>x = %d cm</b>." % (h1, H, B, b1), "cm")

    def skugga():
        p, s = F(ri(15, 19), 10), ri(2, 6)
        k = ri(4, 12)
        T = s * k
        H = p * k
        return MN("En person som är %s m lång kastar en %s m lång skugga. Samtidigt kastar ett träd en %s m lång skugga. Hur högt är trädet?" % (d(p), d(s), d(T)), H, [T + p - s, T * s, H + 1], "Likformiga trianglar: %s/%s = x/%s ger x = <b>%s m</b>." % (d(p), d(s), d(T), d(H)), "m")

    def areaf():
        k = ch([2, 3, 4, 5])
        a = ri(2, 20)
        if coin():
            return MN("Två likformiga figurer har längdskalan 1 : %d. Den lilla har arean %d cm². Vad är den stora figurens area?" % (k, a), a * k * k, [a * k, a * k ** 3, a + k], "Areaskalan är 1 : %d. %d · %d = <b>%d cm²</b>." % (k * k, a, k * k, a * k * k), "cm²")
        return MN("Två likformiga kroppar har längdskalan 1 : %d. Den lilla har volymen %d cm³. Vad är den stora kroppens volym?" % (k, a), a * k ** 3, [a * k * k, a * k, a * 3 * k], "Volymskalan är 1 : %d. %d · %d = <b>%s cm³</b>." % (k ** 3, a, k ** 3, num(a * k ** 3)), "cm³")

    def vilka():
        a, b, c = ri(3, 9), ri(3, 9), ri(3, 9)
        if len({a, b, c}) < 3 or a + b <= c or a + c <= b or b + c <= a:
            return None
        k = ri(2, 3)
        r = "%d, %d och %d cm" % (a * k, b * k, c * k)
        w = ["%d, %d och %d cm" % (a * k, b * k, c * k + 1), "%d, %d och %d cm" % (a + k, b + k, c + k), "%d, %d och %d cm" % (a * k, b * k + k, c * k)]
        return MQ("En triangel har sidorna %d, %d och %d cm. Vilken triangel är likformig med den:" % (a, b, c), r, w, "Alla sidor är %d gånger så långa: <b>%s</b>." % (k, r))

    sets = [("Skalfaktor", [(skal, 20)]), ("Vilken är likformig?", [(vilka, 20)]), ("Topptriangeln", [(topp, 20)]),
            ("Skuggor och höjder", [(skugga, 20)]), ("Area- och volymskala", [(areaf, 20)])]
    return unit("likformighet", "G", "Likformighet: skalfaktor, topptriangel och areaskala", "Likformighet",
                "Likformighet och symmetri i planet. Geometriska satser och formler och behovet av argumentation för deras giltighet. Skala vid förminskning och förstoring.",
                "Arbetsblad om likformighet för årskurs 9: skalfaktor, likformiga trianglar, topptriangeln, höjder med skuggor och area- och volymskala. 100 uppgifter med facit.",
                "Lika vinklar, proportionella sidor", "Alla sidor förstoras med samma skalfaktor.", sets,
                ["Två figurer är likformiga om de har samma form: vinklarna är lika stora och alla sidor har samma förhållande.",
                 "Skalfaktorn får du genom att dela en sida i den stora figuren med motsvarande sida i den lilla.",
                 "Om längdskalan är 1 : k blir areaskalan 1 : k² och volymskalan 1 : k³."],
                [("Sida 4 cm motsvarar 10 cm. Vad motsvarar 6 cm?", ["Skalfaktor 10/4 = 2,5", "6 · 2,5"], "15 cm"), ("Längdskala 1 : 3, liten area 5 cm²", ["Areaskala 1 : 9", "5 · 9"], "45 cm²")],
                [["Lägger till samma tal på alla sidor", "Multiplicera alla sidor med samma tal"], ["Areaskalan är samma som längdskalan", "Areaskalan är längdskalan i kvadrat"], ["Jämför fel sidor", "Jämför sidor som ligger mot lika stora vinklar"]],
                [("Är alla kvadrater likformiga?", "Ja, alla vinklar är 90° och sidorna har alltid förhållandet 1 : 1."), ("Vad är kongruenta figurer?", "Figurer som är likformiga med skalfaktorn 1, alltså exakt lika stora."),
                 ("Varför fungerar skuggmetoden?", "Solstrålarna kommer med samma vinkel, så trianglarna blir likformiga.")])


# ============================================================ pyramid, kon och klot (åk 9)
def kroppar9(lv):
    def pyramid():
        s, h = ri(2, 12), ri(3, 15)
        V = F(s * s * h, 3)
        return MN("En pyramid har en kvadratisk bas med sidan %s och höjden %s. Vad är volymen?" % (cm(s), cm(h)) + fig(solid("pyramid", cm(s), "", "h = " + cm(h))), V, [s * s * h, F(s * h, 3), F(s * s * h, 2)], "V = B · h/3 = %d · %d/3 = <b>%s cm³</b>." % (s * s, h, d(V) if V.denominator == 1 else rd(V, 1)), "cm³") if V.denominator == 1 else None

    def kon():
        r, h = ri(2, 10), ri(3, 18)
        V = PI * r * r * h / 3
        if (V * 100).denominator != 1:
            return None
        return MN("En kon har radien %s och höjden %s. Vad är volymen? Använd π ≈ 3,14." % (cm(r), cm(h)) + fig(solid("kon", "r = " + cm(r), "h = " + cm(h))), V, [PI * r * r * h, PI * r * h / 3 if (PI * r * h / 3 * 100).denominator == 1 else PI * r * h, PI * r * r * h / 2], "V = πr²h/3 = 3,14 · %d² · %d/3 = <b>%s cm³</b>." % (r, h, d(V)), "cm³")

    def klot():
        r = ri(1, 12) * 3
        V = 4 * PI * r ** 3 / 3
        if (V * 100).denominator != 1:
            return None
        if coin():
            return MN("Ett klot har radien %s. Vad är volymen? Använd π ≈ 3,14." % cm(r) + fig(solid("klot", "r = " + cm(r))), V, [4 * PI * r * r, PI * r ** 3, 4 * PI * r ** 3], "V = 4πr³/3 = 4 · 3,14 · %d³/3 = <b>%s cm³</b>." % (r, d(V)), "cm³")
        return MN("Ett klot har radien %s. Vad är begränsningsarean? Använd π ≈ 3,14." % cm(r), 4 * PI * r * r, [V, PI * r * r, 2 * PI * r * r], "A = 4πr² = 4 · 3,14 · %d² = <b>%s cm²</b>." % (r, d(4 * PI * r * r)), "cm²")

    def jamfor():
        r = ri(2, 10)
        k = ri(0, 2)
        if k == 0:
            return M("En cylinder och en kon har samma bas och samma höjd. Hur förhåller sig konens volym till cylinderns?", "Konen är en tredjedel av cylindern", ["Konen är hälften av cylindern", "De är lika stora", "Konen är två tredjedelar av cylindern"], "V<sub>kon</sub> = πr²h/3, alltså <b>en tredjedel</b>.") if r == 2 else None
        if k == 1:
            h = ri(3, 15)
            Vc = PI * r * r * h
            return MN("En cylinder har radien %d cm och höjden %d cm. En kon med samma radie och höjd fylls med vatten och hälls i cylindern. Hur mycket vatten är det? Använd π ≈ 3,14." % (r, h), Vc / 3, [Vc, Vc / 2, Vc * 2 / 3], "Konen rymmer en tredjedel: 3,14 · %d² · %d/3 = <b>%s cm³</b>." % (r, h, d(Vc / 3)), "cm³") if (Vc / 3 * 100).denominator == 1 else None
        rr = r * 3
        V = 4 * PI * rr ** 3 / 3
        return MN("En glasskula har diametern %d cm. Hur många liter är den? Använd π ≈ 3,14. Avrunda till en decimal." % (2 * rr), V / 1000, [V / 100, 4 * PI * rr * rr / 1000, V * 8 / 1000], "r = %d cm. V = 4 · 3,14 · %d³/3 = %s cm³ ≈ <b>%s liter</b>." % (rr, rr, d(V), rd(V / 1000, 1)), "liter") if False else None

    def vardag():
        k = ri(0, 2)
        if k == 0:
            r = ri(2, 5)
            h = ri(8, 15)
            V = PI * r * r * h / 3
            if (V * 100).denominator != 1:
                return None
            return MN("En glasstrut är formad som en kon med radien %d cm och höjden %d cm. Hur många cm³ glass får plats i struten? Använd π ≈ 3,14." % (r, h), V, [PI * r * r * h, PI * r * h, V * 2], "V = 3,14 · %d² · %d/3 = <b>%s cm³</b>." % (r, h, d(V)), "cm³")
        if k == 1:
            s, h = ch([(230, 146), (100, 60), (150, 90), (60, 30), (90, 45), (120, 75)])
            V = F(s * s * h, 3)
            return M("En pyramid i Egypten har en kvadratisk bas med sidan %d m och är %d m hög. Vad är volymen ungefär?" % (s, h), num(int(V)) + NB + "m³", [num(s * s * h) + NB + "m³", num(int(F(s * h, 3))) + NB + "m³", num(int(V / 10)) + NB + "m³"], "V = %d² · %d/3 ≈ <b>%s m³</b>." % (s, h, num(int(V)))) if V.denominator == 1 else None
        r = ri(1, 5) * 3
        V = 4 * PI * r ** 3 / 3
        thing = ch(["En boll", "En badboll", "En jordglob", "En julgranskula", "En ballong"])
        if coin():
            return MN("%s har radien %d cm. Hur stor är volymen? Använd π ≈ 3,14." % (thing, r), V, [4 * PI * r * r, PI * r ** 3, V * 2], "V = 4 · 3,14 · %d³/3 = <b>%s cm³</b>." % (r, d(V)), "cm³")
        return MN("%s har diametern %d cm. Hur stor är volymen? Använd π ≈ 3,14." % (thing, 2 * r), V, [4 * PI * (2 * r) ** 3 / 3, 4 * PI * r * r, V * 2], "Radien är %d cm. V = 4 · 3,14 · %d³/3 = <b>%s cm³</b>." % (r, r, d(V)), "cm³")

    sets = [("Pyramid", [(pyramid, 20)]), ("Kon", [(kon, 20)]), ("Klot", [(klot, 20)]), ("Jämför kroppar", [(jamfor, 6), (kon, 7), (pyramid, 7)]), ("Kroppar i vardagen", [(vardag, 20)])]
    return unit("pyramid-kon-och-klot", "G", "Volym: pyramid, kon och klot", "Pyramid, kon och klot",
                "Metoder för beräkning av volym och area hos olika tredimensionella geometriska objekt, till exempel pyramider, koner och klot.",
                "Arbetsblad om pyramid, kon och klot för årskurs 9: volym av pyramid och kon, volym och begränsningsarea av klot, jämför kroppar och vardagsproblem. 100 uppgifter med facit.",
                "Pyramid och kon: V = B · h/3", "Klot: V = 4πr³/3 och A = 4πr².", sets,
                ["En pyramid och en kon har spetsen uppåt. Volymen är en tredjedel av ett prisma eller en cylinder med samma bas och höjd: V = B · h/3.",
                 "För en kon är basen en cirkel: V = πr²h/3.",
                 "Ett klot har volymen V = 4πr³/3 och begränsningsarean A = 4πr²."],
                [("Kon med r = 3 cm och h = 10 cm", ["V = 3,14 · 9 · 10/3"], "94,2 cm³"), ("Klot med r = 3 cm", ["V = 4 · 3,14 · 27/3"], "113,04 cm³")],
                [["Glömmer att dela med 3", "Pyramid och kon: dela med 3"], ["Klotets volym med r²", "Volym har r³: 4πr³/3"], ["Använder diametern som radie", "Dela diametern med 2 först"]],
                [("Varför delar man med 3?", "Tre pyramider fyller ett prisma med samma bas och höjd. Det kan visas med vatten eller sand."),
                 ("Vad är ett klot?", "En rund kropp där alla punkter på ytan har samma avstånd till medelpunkten, som en boll."), ("Hur mycket mer rymmer en dubbelt så stor boll?", "Åtta gånger så mycket, eftersom 2³ = 8.")])


# ============================================================ cirkelsektorer (åk 9)
def sektorer(lv):
    def sector_svg(v):
        cx, cy, r = 110, 110, 90
        a0, a1 = -math.pi / 2, -math.pi / 2 + math.radians(v)
        big = 1 if v > 180 else 0
        s = ["<circle cx='%d' cy='%d' r='%d' fill='#ffffff' stroke='%s' stroke-width='1.6'/>" % (cx, cy, r, INK),
             "<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, big, cx + r * math.cos(a1), cy + r * math.sin(a1), FILL, GREEN)]
        m = (a0 + a1) / 2
        s.append(text(cx + 28 * math.cos(m), cy + 28 * math.sin(m) + 5, "%d°" % v, 14, col=RED))
        return fig(wrap(220, 220, "".join(s), "cirkelsektor med medelpunktsvinkeln %d°" % v))

    V = [30, 36, 40, 45, 60, 72, 90, 120, 135, 144, 150, 180, 210, 240, 270, 300]

    def bage():
        v = ch(V)
        r = ri(2, 20)
        L = F(v, 360) * 2 * PI * r
        if (L * 100).denominator != 1:
            return None
        return MN("En cirkelsektor har radien %s och medelpunktsvinkeln %d°. Hur lång är bågen? Använd π ≈ 3,14." % (cm(r), v) + sector_svg(v), L, [F(v, 360) * PI * r * r, 2 * PI * r, L * 2], "Bågen = %d/360 · 2 · 3,14 · %d = <b>%s cm</b>." % (v, r, d(L)), "cm")

    def arean():
        v = ch(V)
        r = ri(2, 15)
        A_ = F(v, 360) * PI * r * r
        if (A_ * 100).denominator != 1:
            return None
        return MN("En cirkelsektor har radien %s och medelpunktsvinkeln %d°. Vad är arean? Använd π ≈ 3,14." % (cm(r), v) + sector_svg(v), A_, [PI * r * r, F(v, 360) * 2 * PI * r, A_ * 2], "A = %d/360 · 3,14 · %d² = <b>%s cm²</b>." % (v, r, d(A_)), "cm²")

    def exakt():
        v = ch(V)
        r = ri(2, 12)
        k = coin()
        val = F(v, 360) * (2 * r if k else r * r)
        def pis(x):
            x = F(x)
            if x.denominator == 1:
                return ("" if x == 1 else d(x)) + "π"
            return "%dπ/%d" % (x.numerator, x.denominator)
        w = [pis(val * 2), pis(F(v, 360) * (r * r if k else 2 * r)), pis(val + 1)]
        return M("Vad är %s av en cirkelsektor med radien %d cm och vinkeln %d°? Svara exakt med π." % ("båglängden" if k else "arean", r, v), pis(val) + NB + ("cm" if k else "cm²"), [x + NB + ("cm" if k else "cm²") for x in w],
                 "%d/360 · %s = <b>%s</b>." % (v, "2π · %d" % r if k else "π · %d²" % r, pis(val) + NB + ("cm" if k else "cm²")))

    def vinkel():
        v = ch(V)
        r = ri(2, 12)
        L = F(v, 360) * 2 * PI * r
        if (L * 100).denominator != 1:
            return None
        return MN("En cirkelsektor har radien %d cm och bågen %s cm. Hur stor är medelpunktsvinkeln? Använd π ≈ 3,14." % (r, d(L)), v, [360 - v, v // 2, F(v * 2) if v * 2 < 360 else v + 30], "Hela omkretsen är %s cm. %s/%s · 360° = <b>%d°</b>." % (d(2 * PI * r), d(L), d(2 * PI * r), v), "°")

    def vardag():
        k = ri(0, 2)
        if k == 0:
            n = ch([4, 6, 8, 10, 12])
            r = ri(10, 20)
            A_ = PI * r * r / n
            return MN("En rund pizza med radien %d cm delas i %d lika bitar. Vad är arean av en bit? Använd π ≈ 3,14." % (r, n), A_, [PI * r * r, 2 * PI * r / n, A_ * 2], "Hela pizzan: 3,14 · %d² = %s cm². Delat med %d: <b>%s cm²</b>." % (r, d(PI * r * r), n, d(A_)), "cm²") if (A_ * 100).denominator == 1 else None
        if k == 1:
            v = ch([60, 90, 120, 150, 180, 270])
            r = ri(2, 9)
            A_ = F(v, 360) * PI * r * r
            return MN("En vattenspridare sprutar %d m långt och vrider sig %d°. Hur stor yta blir vattnad? Använd π ≈ 3,14." % (r, v), A_, [PI * r * r, F(v, 360) * 2 * PI * r, A_ * 2], "%d/360 · 3,14 · %d² = <b>%s m²</b>." % (v, r, d(A_)), "m²") if (A_ * 100).denominator == 1 else None
        mins = ch([10, 15, 20, 30, 40, 45])
        L = ri(5, 15)
        b = F(mins, 60) * 2 * PI * L
        return MN("Minutvisaren på en klocka är %d cm lång. Hur långt rör sig spetsen på %d minuter? Använd π ≈ 3,14." % (L, mins), b, [2 * PI * L, F(mins, 60) * PI * L * L, b * 2], "%d minuter är %d/60 av ett varv. %d/60 · 2 · 3,14 · %d = <b>%s cm</b>." % (mins, mins, mins, L, d(b)), "cm") if (b * 100).denominator == 1 else None

    sets = [("Båglängd", [(bage, 20)]), ("Sektorns area", [(arean, 20)]), ("Exakta svar med π", [(exakt, 20)]), ("Medelpunktsvinkeln", [(vinkel, 20)]), ("Sektorer i vardagen", [(vardag, 20)])]
    return unit("cirkelsektorer", "G", "Cirkelsektorer: båglängd, area och medelpunktsvinkel", "Cirkelsektorer",
                "Metoder för beräkning av area och omkrets hos olika tvådimensionella geometriska figurer, bland annat cirkelsektorer. Exakta svar med π.",
                "Arbetsblad om cirkelsektorer för årskurs 9: båglängd, sektorns area, exakta svar med π, medelpunktsvinkeln och sektorer i vardagen. 100 uppgifter med facit.",
                "Sektorn är v/360 av cirkeln", "Båglängd = v/360 · 2πr och area = v/360 · πr².", sets,
                ["En cirkelsektor är en del av en cirkel, som en pizzabit. Medelpunktsvinkeln v avgör hur stor del av cirkeln det är: v/360.",
                 "Båglängden är v/360 av omkretsen: v/360 · 2πr.",
                 "Arean är v/360 av cirkelns area: v/360 · πr². Ett exakt svar behåller π, till exempel 4π cm²."],
                [("r = 6 cm, v = 60°. Båglängd?", ["60/360 = 1/6", "1/6 · 2 · 3,14 · 6"], "6,28 cm"), ("r = 4 cm, v = 90°. Area exakt?", ["90/360 = 1/4", "1/4 · π · 16"], "4π cm²")],
                [["Delar med 180 i stället för 360", "Ett helt varv är 360°"], ["Båglängd med πr²", "Båglängd använder omkretsen 2πr"], ["Glömmer att π står kvar i exakta svar", "Skriv till exempel 4π cm²"]],
                [("Vad är en medelpunktsvinkel?", "Vinkeln vid cirkelns medelpunkt mellan de två radierna."), ("Varför svara exakt med π?", "Då blir svaret helt rätt, utan avrundning."),
                 ("Hur hänger sektorer ihop med cirkeldiagram?", "Varje del i ett cirkeldiagram är en sektor. 25 % motsvarar 90°.")])


UNITS = {"vinklar": vinklar, "vinklar-och-polygoner": polygoner, "omkrets-och-area": area, "cirkeln": cirkeln, "enheter": enheter, "skala": skala,
         "prisma-och-cylinder": volym8, "begransningsarea": begransning, "pythagoras-sats": pythagoras, "likformighet": likformighet,
         "pyramid-kon-och-klot": kroppar9, "cirkelsektorer": sektorer}
