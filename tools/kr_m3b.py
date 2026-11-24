# -*- coding: utf-8 -*-
"""
대한민국 중학교 3학년 수학（2022 개정）：도형과 측정・자료와 가능성の 7 単元
  trig  : 삼각비 [9수03-16]
  trigx : 삼각비의 활용 [9수03-17]
  chord : 원의 현과 접선 [9수03-18]
  insc  : 원주각 [9수03-19]
  var   : 분산과 표준편차 [9수04-07]
  box   : 상자그림 [9수04-08]
  scat  : 산점도와 상관관계 [9수04-09]
誤答は「sin과 cos의 변을 바꾼다」「tan를 빗변으로 나눈다」「원주각을 중심각과 같다고 한다」「편차의 합을 분산으로 쓴다」
「분산과 표준편차를 바꾼다」「사분위수범위를 범위로 쓴다」から作る。
"""
import math
import random
from fractions import Fraction as Fr
from kr_common import josa, Names, num, fr
from kr_mid import M, N, neg, par, dec, rt, unit, figure, fig, svg_wrap, text, line, INK, RED, BLUE, GREEN

R = random.Random(82910)
NM = Names(R)
G = "grade-9"

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29), (12, 16, 20), (9, 40, 41), (12, 35, 37)]


def deg(v):
    return "%s°" % neg(v)


def cm(v):
    return "%s cm" % neg(v)


def svgf(W, H, body, label):
    return fig(svg_wrap(int(W), int(H), body, label).replace("<svg ", "<svg data-pf='lg' ", 1))


def ratio(a, b):
    f = Fr(a, b)
    return neg(f)


# ------------------------------------------------------------------ 삼각비
SV = {("sin", 30): "½", ("sin", 45): fr("√2", 2), ("sin", 60): fr("√3", 2), ("cos", 30): fr("√3", 2), ("cos", 45): fr("√2", 2), ("cos", 60): "½",
      ("tan", 30): fr("√3", 3), ("tan", 45): "1", ("tan", 60): "√3", ("sin", 0): "0", ("cos", 0): "1", ("tan", 0): "0", ("sin", 90): "1", ("cos", 90): "0"}
SVAL = {("sin", 30): 0.5, ("sin", 45): math.sqrt(2) / 2, ("sin", 60): math.sqrt(3) / 2, ("cos", 30): math.sqrt(3) / 2, ("cos", 45): math.sqrt(2) / 2, ("cos", 60): 0.5,
        ("tan", 30): math.sqrt(3) / 3, ("tan", 45): 1.0, ("tan", 60): math.sqrt(3), ("sin", 0): 0, ("cos", 0): 1, ("tan", 0): 0, ("sin", 90): 1, ("cos", 90): 0}


def rtri(a, b, c, unknown=None, lab=("A", "B", "C")):
    """∠C = 90°, BC = a, AC = b, AB = c"""
    A, B, C = lab
    pts = {A: (b, 0), B: (0, a), C: (0, 0)}
    s = {"a": str(a), "b": str(b), "c": str(c)}
    if unknown:
        s[unknown] = "x"
    return figure(pts, [(A, B), (B, C), (C, A)], label="∠C = 90°인 직각삼각형", right=[(C, A, B)], sides=[(B, C, s["a"]), (C, A, s["b"]), (A, B, s["c"])])


def t_ratio(kinds=("sin", "cos", "tan", "find")):
    def mk():
        how = R.choice(kinds)
        a, b, c = R.choice(TRIPLES)
        if R.random() < 0.5:
            a, b = b, a
        g = rtri(a, b, c)
        if how in ("sin", "cos", "tan"):
            ang = R.choice(["A", "B"])
            opp, adj = (a, b) if ang == "A" else (b, a)
            v = {"sin": Fr(opp, c), "cos": Fr(adj, c), "tan": Fr(opp, adj)}[how]
            w = [Fr(adj, c), Fr(opp, c), Fr(opp, adj), Fr(adj, opp), Fr(c, opp)]
            return N("그림의 직각삼각형에서 <b>%s %s</b>의 값은?%s" % (how, ang, g), v, w,
                     "%s %s = %s. <b>%s</b>" % (how, ang, {"sin": "(높이) ÷ (빗변)", "cos": "(밑변) ÷ (빗변)", "tan": "(높이) ÷ (밑변)"}[how], neg(v)))
        k = R.choice(["sin", "cos", "tan"])
        if k == "sin":
            return N("∠C = 90°인 직각삼각형 ABC에서 AB = %d cm, sin A = %s일 때, BC의 길이는?" % (c, fr(a, c) if Fr(a, c).denominator == c else neg(Fr(a, c))), a, [b, c - a, Fr(c * c, a), a + 1], "BC = AB × sin A = <b>%d cm</b>" % a, f=cm)
        if k == "cos":
            return N("∠C = 90°인 직각삼각형 ABC에서 AB = %d cm, cos A = %s일 때, AC의 길이는?" % (c, neg(Fr(b, c))), b, [a, c - b, Fr(c * c, b), b + 1], "AC = AB × cos A = <b>%d cm</b>" % b, f=cm)
        return N("∠C = 90°인 직각삼각형 ABC에서 AC = %d cm, tan A = %s일 때, BC의 길이는?" % (b, neg(Fr(a, b))), a, [c, Fr(b * b, a), b - a if b > a else a + b, a + 1], "BC = AC × tan A = <b>%d cm</b>" % a, f=cm)
    return mk


def t_one(kinds=("other",)):
    def mk():
        a, b, c = R.choice(TRIPLES)
        k = R.choice(["sin", "cos", "tan"])
        given = {"sin": Fr(a, c), "cos": Fr(b, c), "tan": Fr(a, b)}[k]
        ask = R.choice([x for x in ("sin", "cos", "tan") if x != k])
        v = {"sin": Fr(a, c), "cos": Fr(b, c), "tan": Fr(a, b)}[ask]
        w = [Fr(b, c), Fr(a, c), Fr(a, b), Fr(b, a), Fr(c, a)]
        return N("∠A가 예각이고 <b>%s A = %s</b>일 때, %s A의 값은?" % (k, neg(given), ask), v, w, "직각삼각형을 그려 세 변을 %d, %d, %d로 놓아요. <b>%s</b>" % (a, b, c, neg(v)))
    return mk


def t_special(kinds=("val", "expr", "ang", "side")):
    def mk():
        how = R.choice(kinds)
        if how == "val":
            f, t = R.choice([("sin", 30), ("sin", 45), ("sin", 60), ("cos", 30), ("cos", 45), ("cos", 60), ("tan", 30), ("tan", 45), ("tan", 60), ("sin", 90), ("cos", 0), ("cos", 90), ("tan", 0)])
            ok = SV[(f, t)]
            pool = list(dict.fromkeys(SV.values()))
            return M("<b>%s %d°</b>의 값은?" % (f, t), ok, R.sample([p for p in pool if p != ok], 3), "<b>%s</b>" % ok)
        if how == "expr":
            (f1, t1), (f2, t2) = R.sample([("sin", 30), ("cos", 60), ("tan", 45), ("sin", 90), ("cos", 0), ("tan", 60), ("sin", 60), ("cos", 30), ("sin", 45), ("cos", 45)], 2)
            op = R.choice(["+", "×", "−"])
            v1, v2 = SVAL[(f1, t1)], SVAL[(f2, t2)]
            v = {"+": v1 + v2, "×": v1 * v2, "−": v1 - v2}[op]
            # 결과를 문자열로
            cand = {}

            def add(x, s):
                cand.setdefault(round(x, 6), s)
            for s_, x in [("0", 0), ("½", .5), ("1", 1), ("3/2", 1.5), ("2", 2), ("−½", -.5), ("¼", .25), ("¾", .75), ("√3", math.sqrt(3)), ("√2", math.sqrt(2)),
                          ("√3/2", math.sqrt(3) / 2), ("√2/2", math.sqrt(2) / 2), ("√3/3", math.sqrt(3) / 3), ("1 + √3", 1 + math.sqrt(3)), ("1 − √3", 1 - math.sqrt(3)),
                          ("½ + √3/2", .5 + math.sqrt(3) / 2), ("1 + √3/2", 1 + math.sqrt(3) / 2), ("√3 − 1", math.sqrt(3) - 1), ("√3/2 − ½", math.sqrt(3) / 2 - .5),
                          ("½ − √3/2", .5 - math.sqrt(3) / 2), ("√2", math.sqrt(2)), ("√6/4", math.sqrt(6) / 4), ("√6/2", math.sqrt(6) / 2), ("2√3", 2 * math.sqrt(3)),
                          ("√2 + ½", math.sqrt(2) + .5), ("1 + √2/2", 1 + math.sqrt(2) / 2), ("√2/2 − 1", math.sqrt(2) / 2 - 1), ("1 − √2/2", 1 - math.sqrt(2) / 2),
                          ("√3 − ½", math.sqrt(3) - .5), ("½ − √3", .5 - math.sqrt(3)), ("√2/2 + √3/2", (math.sqrt(2) + math.sqrt(3)) / 2), ("√3/2 − √2/2", (math.sqrt(3) - math.sqrt(2)) / 2),
                          ("√2/2 − √3/2", (math.sqrt(2) - math.sqrt(3)) / 2), ("√2/2 − ½", math.sqrt(2) / 2 - .5), ("½ − √2/2", .5 - math.sqrt(2) / 2), ("√2/2 + ½", math.sqrt(2) / 2 + .5),
                          ("√3/2 + ½", math.sqrt(3) / 2 + .5), ("√3 + √3/2", 1.5 * math.sqrt(3)), ("√3 + √2/2", math.sqrt(3) + math.sqrt(2) / 2), ("√3/4", math.sqrt(3) / 4), ("√2/4", math.sqrt(2) / 4),
                          ("√3 − √2/2", math.sqrt(3) - math.sqrt(2) / 2), ("√2/2 − √3", math.sqrt(2) / 2 - math.sqrt(3)), ("√3 + √3", 2 * math.sqrt(3)), ("−√3/2", -math.sqrt(3) / 2),
                          ("√3 − √3/2", math.sqrt(3) / 2), ("1 − √3/2", 1 - math.sqrt(3) / 2), ("√3/2 − 1", math.sqrt(3) / 2 - 1), ("−½ + √3/2", math.sqrt(3) / 2 - .5),
                          ("1 + √2", 1 + math.sqrt(2)), ("√2 − 1", math.sqrt(2) - 1), ("1 − √2", 1 - math.sqrt(2)), ("√3/2 + √2/2", (math.sqrt(3) + math.sqrt(2)) / 2), ("3√3/2", 1.5 * math.sqrt(3)),
                          ("√2 − √3", math.sqrt(2) - math.sqrt(3))]:
                add(x, s_)
            key = round(v, 6)
            if key not in cand:
                return None
            ok = cand[key]
            others = [s_ for k_, s_ in cand.items() if k_ != key]
            near = sorted(others, key=lambda s_: abs([k_ for k_, t_ in cand.items() if t_ == s_][0] - v))[:6]
            R.shuffle(near)
            ok = ok.replace("3/2", "3/2")
            return M("<b>%s %d° %s %s %d°</b>의 값은?" % (f1, t1, op, f2, t2), ok, near[:3], "%s %d° = %s, %s %d° = %s. <b>%s</b>" % (f1, t1, SV[(f1, t1)], f2, t2, SV[(f2, t2)], ok))
        if how == "ang":
            f, t = R.choice([("sin", 30), ("sin", 45), ("sin", 60), ("cos", 30), ("cos", 45), ("cos", 60), ("tan", 30), ("tan", 45), ("tan", 60)])
            return N("<b>%s x = %s</b>를 만족하는 예각 x의 크기는?" % (f, SV[(f, t)]), t, [x for x in (30, 45, 60, 90) if x != t], "<b>%d°</b>" % t, f=deg)
        t = R.choice([30, 45, 60])
        h = R.choice([2, 4, 6, 8, 10, 12])
        k = R.choice(["opp", "adj"])
        if t == 45:
            return M("∠C = 90°, ∠A = 45°인 직각삼각형 ABC에서 AB = %s cm일 때, BC의 길이는?" % rt(2 * h * h), "%d cm" % h, ["%s cm" % rt(2 * h * h), "%d cm" % (2 * h), "%s cm" % rt(3 * h * h)], "BC = AB × sin 45° = %s × √2/2 = <b>%d cm</b>" % (rt(2 * h * h), h))
        if k == "opp":
            ok = "%d cm" % (h // 2) if t == 30 else "%s cm" % rt(3 * (h // 2) ** 2)
            return M("∠C = 90°, ∠A = %d°인 직각삼각형 ABC에서 빗변 AB = %d cm일 때, BC의 길이는?" % (t, h), ok, ["%d cm" % (h // 2) if t == 60 else "%s cm" % rt(3 * (h // 2) ** 2), "%d cm" % h, "%s cm" % rt(2 * (h // 2) ** 2)],
                     "BC = AB × sin %d° = %d × %s = <b>%s</b>" % (t, h, SV[("sin", t)], ok))
        ok = "%s cm" % rt(3 * (h // 2) ** 2) if t == 30 else "%d cm" % (h // 2)
        return M("∠C = 90°, ∠A = %d°인 직각삼각형 ABC에서 빗변 AB = %d cm일 때, AC의 길이는?" % (t, h), ok, ["%d cm" % (h // 2) if t == 30 else "%s cm" % rt(3 * (h // 2) ** 2), "%d cm" % h, "%s cm" % rt(2 * (h // 2) ** 2)],
                 "AC = AB × cos %d° = %d × %s = <b>%s</b>" % (t, h, SV[("cos", t)], ok))
    return mk


TABLE = {d: (math.sin(math.radians(d)), math.cos(math.radians(d)), math.tan(math.radians(d))) for d in range(20, 71)}


def ttab(ds):
    rows = "".join("<tr><td>%d°</td><td>%.4f</td><td>%.4f</td><td>%.4f</td></tr>" % (d, *TABLE[d]) for d in ds)
    return "<div class='sn-tw'><table class='sn-table'><tr><th>각도</th><th>사인(sin)</th><th>코사인(cos)</th><th>탄젠트(tan)</th></tr>%s</table></div>" % rows


def t_table(kinds=("read", "len", "inv")):
    def mk():
        how = R.choice(kinds)
        d0 = R.randint(20, 66)
        ds = list(range(d0, d0 + 5))
        tb = ttab(ds)
        d = R.choice(ds)
        s, c, t = TABLE[d]
        if how == "read":
            f = R.choice(["sin", "cos", "tan"])
            v = {"sin": s, "cos": c, "tan": t}[f]
            ok = "%.4f" % v
            w = ["%.4f" % x for x in (s, c, t) if "%.4f" % x != ok] + ["%.4f" % TABLE[d + 1 if d + 1 <= 70 else d - 1][["sin", "cos", "tan"].index(f)]]
            return M("삼각비의 표를 보고 <b>%s %d°</b>의 값을 구하면?%s" % (f, d, tb), ok, w, "<b>%s</b>" % ok)
        if how == "len":
            L = R.choice([10, 20, 50, 100])
            f = R.choice(["sin", "cos"])
            v = (s if f == "sin" else c) * L
            ok = "%.2f" % v
            w = ["%.2f" % ((c if f == "sin" else s) * L), "%.2f" % (t * L), "%.2f" % (L / (s if f == "sin" else c))]
            return M("∠C = 90°인 직각삼각형 ABC에서 AB = %d, ∠A = %d°일 때, %s의 길이는? (표를 이용)%s" % (L, d, "BC" if f == "sin" else "AC", tb), ok, w, "%s = %d × %s %d° = <b>%s</b>" % ("BC" if f == "sin" else "AC", L, f, d, ok))
        f = R.choice(["sin", "cos", "tan"])
        v = {"sin": s, "cos": c, "tan": t}[f]
        return N("%s x = %.4f일 때, 표에서 x의 크기를 구하면?%s" % (f, v, tb), d, [x for x in ds if x != d][:3], "<b>%d°</b>" % d, f=deg)
    return mk


# ------------------------------------------------------------------ 삼각비의 활용
def x_height(kinds=("tree", "build", "slope", "river")):
    def mk():
        how = R.choice(kinds)
        t = R.choice([30, 45, 60])
        d = R.choice([6, 9, 10, 12, 15, 18, 20, 24, 30])
        if how in ("tree", "build"):
            h0 = R.choice([0, 1.5]) if how == "tree" else 0
            obj = "나무" if how == "tree" else "건물"
            ht = {30: "%s√3" % fr(d, 3).replace("<span class='fr'><span class='fn'>", "").replace("</span><span class='fd'>", "/").replace("</span></span>", "") if d % 3 else "%d√3" % (d // 3) if d // 3 != 1 else "√3", 45: "%d" % d, 60: "%d√3" % d}[t]
            if t == 30 and d % 3:
                return None
            ok = "%s m" % ht
            w = ["%d m" % d if t != 45 else "%d√2 m" % d, "%d√3 m" % d if t != 60 else "%d√3 m" % (d // 3 if d % 3 == 0 else d * 2), "%d√2 m" % d if t == 45 else "%s m" % rt(d * d * 2)]
            return M("%s에서 %d m 떨어진 지점에서 %s의 꼭대기를 올려다본 각의 크기가 %d°였어요. %s의 높이는? (눈높이는 생각하지 않아요)" % (obj, d, obj, t, obj), ok, w, "높이 = %d × tan %d° = %d × %s = <b>%s</b>" % (d, t, d, SV[("tan", t)], ok))
        if how == "slope":
            L = R.choice([10, 20, 40, 60, 100])
            k = R.choice(["h", "x"])
            if k == "h":
                ok = "%d m" % (L // 2) if t == 30 else ("%s m" % ("%d√2" % (L // 2)) if t == 45 else "%d√3 m" % (L // 2))
                return M("경사각이 %d°인 비탈길을 따라 %d m 올라갔을 때, 수직으로 올라간 높이는?" % (t, L), ok, ["%d m" % L, "%d√3 m" % (L // 2) if t != 60 else "%d m" % (L // 2), "%d√2 m" % L],
                         "높이 = %d × sin %d° = <b>%s</b>" % (L, t, ok))
            ok = "%d√3 m" % (L // 2) if t == 30 else ("%d√2 m" % (L // 2) if t == 45 else "%d m" % (L // 2))
            return M("경사각이 %d°인 비탈길을 따라 %d m 올라갔을 때, 수평으로 이동한 거리는?" % (t, L), ok, ["%d m" % L, "%d m" % (L // 2) if t != 60 else "%d√3 m" % (L // 2), "%d√3 m" % L],
                     "수평 거리 = %d × cos %d° = <b>%s</b>" % (L, t, ok))
        if t == 30 and d % 3:
            return None
        ok = {30: ("%d√3 m" % (d // 3)) if d // 3 != 1 else "√3 m", 45: "%d m" % d, 60: "%d√3 m" % d}[t]
        return M("강의 한쪽 A 지점에서 강 건너 C 지점이 강변과 수직이 되도록 B 지점을 잡았어요. AB = %d m, ∠BAC = %d°일 때, 강의 폭 BC는? (∠B = 90°)" % (d, t), ok, ["%d m" % d if t != 45 else "%d√2 m" % d, "%d√3 m" % d if t != 60 else "%d m" % d, "%d m" % (d * 2)],
                 "BC = AB × tan %d° = <b>%s</b>" % (t, ok))
    return mk


def x_area(kinds=("tri", "obtuse", "para", "side")):
    def mk():
        how = R.choice(kinds)
        a, b = R.randint(2, 12), R.randint(2, 12)
        if how == "tri":
            t = R.choice([30, 45, 60])
            v = {30: (Fr(a * b, 4), ""), 45: (Fr(a * b, 4), "√2"), 60: (Fr(a * b, 4), "√3")}[t]
            ok = (neg(v[0]) if v[0] != 1 or not v[1] else "") + v[1] + " cm²"
            w = [(neg(v[0] * 2) if v[1] or True else "") + v[1] + " cm²", neg(Fr(a * b, 2)) + " cm²" if t != 30 else neg(Fr(a * b, 4)) + "√3 cm²", neg(v[0]) + ("√3" if t != 60 else "√2") + " cm²"]
            return M("두 변의 길이가 %d cm, %d cm이고 그 끼인각이 %d°인 삼각형의 넓이는?" % (a, b, t), ok, w, "½ × %d × %d × sin %d° = <b>%s</b>" % (a, b, t, ok))
        if how == "obtuse":
            t = R.choice([120, 135, 150])
            r = {120: "√3", 135: "√2", 150: ""}[t]
            v = Fr(a * b, 4)
            ok = (neg(v) if v != 1 or not r else "") + r + " cm²"
            w = [neg(v * 2) + r + " cm²", neg(v) + ("√2" if t != 135 else "√3") + " cm²", neg(Fr(a * b, 2)) + " cm²" if t != 150 else neg(v) + "√3 cm²"]
            return M("두 변의 길이가 %d cm, %d cm이고 그 끼인각이 %d°인 삼각형의 넓이는?" % (a, b, t), ok, w, "½ × %d × %d × sin(180° − %d°) = <b>%s</b>" % (a, b, t, ok))
        if how == "para":
            t = R.choice([30, 45, 60, 120, 135, 150])
            tt = min(t, 180 - t)
            r = {30: "", 45: "√2", 60: "√3"}[tt]
            v = Fr(a * b, 2) if tt != 30 else Fr(a * b, 2)
            ok = (neg(v) if v != 1 or not r else "") + r + " cm²"
            w = [neg(v * 2) + r + " cm²", neg(Fr(a * b, 4)) + r + " cm²", neg(v) + ("√3" if r != "√3" else "√2") + " cm²"]
            return M("이웃한 두 변의 길이가 %d cm, %d cm이고 그 끼인각이 %d°인 평행사변형의 넓이는?" % (a, b, t), ok, w, "%d × %d × sin %d° = <b>%s</b>" % (a, b, tt, ok))
        t = 60
        # 두 변과 끼인각 60° → 나머지 변 (코사인 법칙은 고등) 대신 높이로 구하기: 한 변 a, ∠B=60°, BC=b → AH = a sin60
        h = R.choice([2, 4, 6, 8, 10])
        ok = "%s cm" % rt(3 * (h // 2) ** 2)
        return M("△ABC에서 AB = %d cm, ∠B = 60°일 때, 꼭짓점 A에서 BC에 내린 수선의 길이 AH는?" % h, ok, ["%d cm" % (h // 2), "%d cm" % h, "%s cm" % rt(2 * (h // 2) ** 2)], "AH = AB × sin 60° = %d × √3/2 = <b>%s</b>" % (h, ok))
    return mk


# ------------------------------------------------------------------ 원의 현과 접선
def c_chord(kinds=("half", "dist", "radius", "equal")):
    def mk():
        how = R.choice(kinds)
        a, b, c = R.choice(TRIPLES)
        if how == "half":
            return N("반지름의 길이가 %d cm인 원 O에서 중심으로부터 거리가 %d cm인 현 AB의 길이는?" % (c, a), 2 * b, [b, 2 * a, c + a, 2 * c], "현의 수직이등분선은 중심을 지나요. AM = √(%d² − %d²) = %d → AB = <b>%d cm</b>" % (c, a, b, 2 * b), f=cm)
        if how == "dist":
            return N("반지름의 길이가 %d cm인 원 O에서 길이가 %d cm인 현 AB와 중심 O 사이의 거리는?" % (c, 2 * b), a, [b, c - b, 2 * a, a + 1], "AM = %d, OM = √(%d² − %d²) = <b>%d cm</b>" % (b, c, b, a), f=cm)
        if how == "radius":
            return N("원 O의 중심에서 길이가 %d cm인 현까지의 거리가 %d cm일 때, 원의 반지름의 길이는?" % (2 * b, a), c, [a + b, 2 * b, c + 1, b], "√(%d² + %d²) = <b>%d cm</b>" % (b, a, c), f=cm)
        k = R.randint(3, 15)
        F_ = [("한 원에서 중심으로부터 같은 거리에 있는 두 현의 길이는?", "서로 같아요", ["항상 달라요", "중심에 가까운 현이 짧아요", "반지름과 같아요"], "<b>서로 같아요</b>."),
              ("원의 중심에서 현에 내린 수선은 그 현을 어떻게 할까요?", "이등분해요", ["삼등분해요", "현과 평행해요", "현의 끝점을 지나요"], "현을 <b>이등분</b>해요."),
              ("현의 수직이등분선은 어디를 지날까요?", "원의 중심", ["원 위의 한 점", "현의 끝점", "접점"], "<b>원의 중심</b>을 지나요.")]
        if R.random() < 0.3:
            return M(*R.choice(F_))
        return N("원 O에서 두 현 AB, CD가 중심으로부터 같은 거리에 있어요. AB = %d cm일 때, CD의 길이는?" % (2 * k), 2 * k, [k, 4 * k, 2 * k + 2, k + 2], "중심으로부터 같은 거리의 현은 길이가 같아요. <b>%d cm</b>" % (2 * k), f=cm)
    return mk


def c_tan(kinds=("len", "eq", "angle", "quad", "tri")):
    def mk():
        how = R.choice(kinds)
        a, b, c = R.choice(TRIPLES)
        if how == "len":
            return N("원 O 밖의 한 점 P에서 원에 그은 접선의 접점을 T라 해요. 원의 반지름이 %d cm, PO = %d cm일 때, PT의 길이는?" % (a, c), b, [c - a, a + c, b + 1, a], "OT ⊥ PT이므로 PT = √(%d² − %d²) = <b>%d cm</b>" % (c, a, b), f=cm)
        if how == "eq":
            k = R.randint(4, 20)
            return N("원 O 밖의 한 점 P에서 원에 그은 두 접선의 접점을 A, B라 해요. PA = %d cm일 때, PB의 길이는?" % k, k, [2 * k, Fr(k, 2), k + 2, k - 2], "한 점에서 그은 두 접선의 길이는 같아요. <b>%d cm</b>" % k, f=cm)
        if how == "angle":
            t = R.choice(range(30, 131, 2))
            return N("원 O 밖의 한 점 P에서 그은 두 접선의 접점을 A, B라 해요. ∠APB = %d°일 때, ∠AOB의 크기는?" % t, 180 - t, [t, 2 * t if 2 * t < 180 else t // 2, 90 - t if t < 90 else t - 90, 360 - t], "∠OAP = ∠OBP = 90°이므로 360° − 180° − %d° = <b>%d°</b>" % (t, 180 - t), f=deg)
        if how == "quad":
            p, q, r = R.randint(4, 15), R.randint(4, 15), R.randint(4, 15)
            s = p + r - q
            if s <= 0:
                return None
            return N("원에 외접하는 사각형 ABCD에서 AB = %d cm, BC = %d cm, CD = %d cm일 때, AD의 길이는?" % (p, q, r), s, [p + q - r if p + q - r > 0 else s + 2, q + r - p if q + r - p > 0 else s + 1, Fr(p + q + r, 3), s + 1],
                     "AB + CD = AD + BC이므로 %d + %d = AD + %d, AD = <b>%d cm</b>" % (p, r, q, s), f=cm)
        x, y, z = R.randint(2, 8), R.randint(2, 8), R.randint(2, 8)
        return N("△ABC의 내접원이 세 변 AB, BC, CA와 접하는 점을 D, E, F라 해요. AD = %d cm, BE = %d cm, CF = %d cm일 때, △ABC의 둘레의 길이는?" % (x, y, z), 2 * (x + y + z), [x + y + z, 3 * (x + y + z), 2 * (x + y + z) + 2, x * y * z if x * y * z < 100 else x + y + z + 10],
                 "AD = AF, BD = BE, CE = CF이므로 2 × (%d + %d + %d) = <b>%d cm</b>" % (x, y, z, 2 * (x + y + z)), f=cm)
    return mk


# ------------------------------------------------------------------ 원주각
def circ_svg(n_on, center=True, label="원과 원주각"):
    """원 위의 점 n_on개 (각도 리스트, 이름)"""
    cx, cy, r = 150, 120, 90
    s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2.2'/>" % (cx, cy, r, INK)]
    P = {}
    for nm, ang in n_on:
        x, y = cx + r * math.cos(math.radians(ang)), cy - r * math.sin(math.radians(ang))
        P[nm] = (x, y)
        s.append("<circle cx='%.1f' cy='%.1f' r='3.5' fill='%s'/>" % (x, y, INK))
        s.append(text(cx + (r + 18) * math.cos(math.radians(ang)), cy - (r + 18) * math.sin(math.radians(ang)) + 6, nm, 17))
    if center:
        P["O"] = (cx, cy)
        s.append("<circle cx='%d' cy='%d' r='3.5' fill='%s'/>" % (cx, cy, INK) + text(cx + 12, cy + 18, "O", 16))
    return P, s


def insc_fig(segs, pts, extra=()):
    P, s = circ_svg(pts)
    for a, b in segs:
        s.append(line(P[a][0], P[a][1], P[b][0], P[b][1], INK, 2))
    return svgf(300, 240, "".join(s) + "".join(extra), "원과 원주각")


def i_basic(kinds=("cen", "ins", "same", "semi")):
    def mk():
        how = R.choice(kinds)
        t = R.choice(range(20, 81, 2))
        if how == "cen":
            g = insc_fig([("P", "A"), ("P", "B"), ("O", "A"), ("O", "B")], [("A", 210), ("B", 330), ("P", 95)])
            return N("원 O에서 ∠AOB = %d°일 때, 원주각 ∠APB의 크기는?%s" % (2 * t, g), t, [2 * t, 180 - 2 * t, 4 * t if 4 * t < 180 else 90 - t, 180 - t], "원주각은 중심각의 ½이에요. <b>%d°</b>" % t, f=deg)
        if how == "ins":
            g = insc_fig([("P", "A"), ("P", "B"), ("O", "A"), ("O", "B")], [("A", 210), ("B", 330), ("P", 95)])
            return N("원 O에서 원주각 ∠APB = %d°일 때, 중심각 ∠AOB의 크기는?%s" % (t, g), 2 * t, [t, Fr(t, 2), 180 - t, 180 - 2 * t], "중심각은 원주각의 2배예요. <b>%d°</b>" % (2 * t), f=deg)
        if how == "same":
            g = insc_fig([("P", "A"), ("P", "B"), ("Q", "A"), ("Q", "B")], [("A", 200), ("B", 340), ("P", 60), ("Q", 130)])
            return N("한 원에서 호 AB에 대한 원주각 ∠APB = %d°일 때, ∠AQB의 크기는? (P, Q는 같은 쪽 호 위의 점)%s" % (t, g), t, [2 * t, 180 - t, Fr(t, 2), 90 - t], "같은 호에 대한 원주각의 크기는 모두 같아요. <b>%d°</b>" % t, f=deg)
        g = insc_fig([("P", "A"), ("P", "B"), ("A", "B")], [("A", 180), ("B", 0), ("P", 70)])
        return N("선분 AB가 원 O의 지름이고 점 P가 원 위의 점일 때, ∠PAB = %d°이면 ∠PBA의 크기는?%s" % (t, g), 90 - t, [t, 180 - t, 90, 2 * t], "지름에 대한 원주각은 90°이므로 ∠APB = 90°. 90° − %d° = <b>%d°</b>" % (t, 90 - t), f=deg)
    return mk


def i_more(kinds=("cyc", "cycext", "tanchord", "arc")):
    def mk():
        how = R.choice(kinds)
        t = R.choice(range(50, 131, 2))
        if how == "cyc":
            g = insc_fig([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")], [("A", 130), ("B", 220), ("C", 320), ("D", 40)])
            return N("원에 내접하는 사각형 ABCD에서 ∠A = %d°일 때, ∠C의 크기는?%s" % (t, g), 180 - t, [t, 360 - t, 90 - t if t < 90 else t - 90, 2 * t if 2 * t < 180 else t // 2], "원에 내접하는 사각형의 대각의 합은 180°예요. <b>%d°</b>" % (180 - t), f=deg)
        if how == "cycext":
            return N("원에 내접하는 사각형 ABCD에서 ∠A = %d°일 때, ∠C의 외각의 크기는?" % t, t, [180 - t, 360 - t, t // 2, 90], "내접사각형의 한 외각의 크기는 그 내대각의 크기와 같아요. <b>%d°</b>" % t, f=deg)
        if how == "tanchord":
            t = R.choice(range(30, 81, 2))
            return N("원 위의 점 A에서 그은 접선과 현 AB가 이루는 각의 크기가 %d°일 때, 호 AB에 대한 원주각 ∠ACB의 크기는? (C는 반대쪽 호 위의 점)" % t, t, [2 * t, 90 - t, 180 - t, Fr(t, 2)],
                     "접선과 현이 이루는 각의 크기는 그 각의 내부에 있는 호에 대한 원주각과 같아요. <b>%d°</b>" % t, f=deg)
        a = R.choice(range(20, 61, 5))
        k = R.choice([2, 3])
        L = R.randint(2, 8)
        return N("한 원에서 호 AB에 대한 원주각이 %d°이고 호 AB의 길이가 %d cm일 때, 원주각이 %d°인 호 CD의 길이는?" % (a, L, a * k), L * k, [L * k * k, L + k, Fr(L, k), L * 2 * k], "호의 길이는 원주각의 크기에 정비례해요. <b>%d cm</b>" % (L * k), f=cm)
    return mk


# ------------------------------------------------------------------ 분산과 표준편차
def data_mean(n, lo, hi, mean_int=True):
    for _ in range(200):
        xs = [R.randint(lo, hi) for _ in range(n)]
        m = Fr(sum(xs), n)
        if (m.denominator == 1) or not mean_int:
            v = Fr(sum((x - m) ** 2 for x in xs), n)
            return xs, m, v
    return None


def v_dev(kinds=("dev", "unk", "var", "sd")):
    def mk():
        how = R.choice(kinds)
        n = R.choice([4, 5, 5, 6])
        t = data_mean(n, 2, 20)
        if not t:
            return None
        xs, m, v = t
        if how == "dev":
            i = R.randrange(n)
            return N("자료 %s의 평균이 %s일 때, %d의 편차는?" % (", ".join(map(str, xs)), neg(m), xs[i]), xs[i] - m, [m - xs[i], xs[i], abs(xs[i] - m) + 1, 0], "(변량) − (평균) = %d − %s = <b>%s</b>" % (xs[i], neg(m), neg(xs[i] - m)))
        if how == "unk":
            ds = [x - m for x in xs]
            i = R.randrange(n)
            shown = ", ".join("x" if j == i else neg(d) for j, d in enumerate(ds))
            return N("어떤 자료의 편차가 %s일 때, x의 값은?" % shown, ds[i], [-ds[i], ds[i] + 1, 0, sum(abs(d) for d in ds)], "편차의 합은 항상 0이에요. <b>%s</b>" % neg(ds[i]))
        if v.denominator != 1 and how == "sd":
            return None
        if how == "var":
            return N("자료 %s의 분산은?" % ", ".join(map(str, xs)), v, [v * n / (n - 1) if n > 1 else v + 1, sum(abs(x - m) for x in xs) / n, m, v + 1, v * v if v < 20 else v - 1],
                     "평균 %s, 편차의 제곱의 평균: (%s) ÷ %d = <b>%s</b>" % (neg(m), " + ".join(neg((x - m) ** 2) for x in xs), n, neg(v)))
        sv = math.isqrt(v.numerator) if v.denominator == 1 else None
        if sv is None:
            return None
        ok = str(sv) if sv * sv == v else rt(int(v))
        if sv * sv == v:
            return N("자료 %s의 표준편차는?" % ", ".join(map(str, xs)), sv, [v, sv + 1, Fr(v, 2) if v != 2 * sv else v + 1, m], "분산 %s → 표준편차 √%s = <b>%d</b>" % (neg(v), neg(v), sv))
        return M("자료 %s의 표준편차는?" % ", ".join(map(str, xs)), ok, [neg(v), rt(int(v) + 1), rt(int(v) * 2)], "분산 %s → 표준편차 <b>%s</b>" % (neg(v), ok))
    return mk


def v_compare(kinds=("which", "from_sd", "concept")):
    def mk():
        how = R.choice(kinds)
        if how == "which":
            cls = ["A반", "B반", "C반", "D반"]
            sds = R.sample([dec(Fr(x, 10)) for x in range(8, 60, 3)], 4)
            k = R.choice(["고르게", "흩어진"])
            vals = [float(s.replace("−", "-")) for s in sds]
            i = vals.index(min(vals)) if k == "고르게" else vals.index(max(vals))
            tb = "<div class='sn-tw'><table class='sn-table'><tr><th>반</th>%s</tr><tr><th>표준편차(점)</th>%s</tr></table></div>" % ("".join("<td>%s</td>" % c for c in cls), "".join("<td>%s</td>" % s for s in sds))
            return M("네 반의 수학 점수의 평균은 같고 표준편차는 다음과 같아요. 점수가 가장 %s 반은?%s" % ("고르게 분포된" if k == "고르게" else "넓게 흩어진", tb), cls[i], [c for j, c in enumerate(cls) if j != i],
                     "표준편차가 %s수록 자료가 %s. <b>%s</b>" % ("작을" if k == "고르게" else "클", "평균 가까이 모여 있어요" if k == "고르게" else "넓게 흩어져 있어요", cls[i]))
        if how == "from_sd":
            v = R.choice([4, 9, 16, 25, 36, 2, 3, 5])
            k = R.choice(["v2s", "s2v"])
            if k == "v2s":
                ok = str(math.isqrt(v)) if math.isqrt(v) ** 2 == v else "√%d" % v
                return M("분산이 %d인 자료의 표준편차는?" % v, ok, [str(v * v), str(v // 2) if v // 2 and str(v // 2) != ok else str(v + 1), "%d" % v], "표준편차 = √(분산) = <b>%s</b>" % ok)
            s = R.randint(2, 9)
            return N("표준편차가 %d인 자료의 분산은?" % s, s * s, [s, 2 * s, s * s * s if s < 5 else s + 10, s * s + 1], "분산 = (표준편차)² = <b>%d</b>" % (s * s))
        F_ = [("편차의 합은 항상 얼마일까요?", "0", ["1", "평균", "분산"], "<b>0</b>이에요."),
              ("분산은 무엇의 평균일까요?", "편차의 제곱", ["편차", "변량", "변량의 제곱근"], "<b>편차의 제곱</b>의 평균이에요."),
              ("표준편차는 어떻게 구할까요?", "분산의 음이 아닌 제곱근", ["분산의 2배", "편차의 합", "평균의 제곱"], "<b>√(분산)</b>이에요."),
              ("모든 변량에 같은 수 5를 더하면 표준편차는?", "변하지 않아요", ["5만큼 커져요", "5배가 돼요", "0이 돼요"], "흩어진 정도는 그대로이므로 <b>변하지 않아요</b>."),
              ("모든 변량이 같으면 표준편차는?", "0", ["1", "평균과 같아요", "알 수 없어요"], "편차가 모두 0이므로 <b>0</b>이에요."),
              ("표준편차의 단위는?", "변량의 단위와 같아요", ["단위가 없어요", "변량 단위의 제곱이에요", "항상 %예요"], "<b>변량의 단위와 같아요</b>.")]
        return M(*R.choice(F_))
    return mk


# ------------------------------------------------------------------ 상자그림
def five(xs):
    s = sorted(xs)
    n = len(s)

    def med(a):
        k = len(a)
        return Fr(a[k // 2]) if k % 2 else Fr(a[k // 2 - 1] + a[k // 2], 2)
    lo = s[: n // 2]
    hi = s[(n + 1) // 2:]
    return s[0], med(lo), med(s), med(hi), s[-1]


def box_svg(fv, lo, hi, step):
    mn, q1, q2, q3, mx = [float(v) for v in fv]
    W, H = 380, 130
    X = lambda v: 30 + (v - lo) / (hi - lo) * (W - 60)
    s = [line(X(lo), 100, X(hi), 100, INK, 1.8)]
    v = lo
    while v <= hi + 1e-9:
        s.append(line(X(v), 95, X(v), 105, INK, 1.5) + text(X(v), 122, neg(int(v)) if v == int(v) else dec(v), 13, weight=500))
        v += step
    s.append(line(X(mn), 50, X(q1), 50, INK, 2) + line(X(q3), 50, X(mx), 50, INK, 2))
    s.append(line(X(mn), 38, X(mn), 62, INK, 2) + line(X(mx), 38, X(mx), 62, INK, 2))
    s.append("<rect x='%.1f' y='30' width='%.1f' height='40' fill='#cfe3f7' stroke='%s' stroke-width='2'/>" % (X(q1), X(q3) - X(q1), BLUE))
    s.append(line(X(q2), 30, X(q2), 70, RED, 2.5))
    return svgf(W, H, "".join(s), "상자그림")


def b_five(kinds=("q1", "q3", "med", "iqr", "range")):
    def mk():
        how = R.choice(kinds)
        n = R.choice([8, 10, 12, 7, 11])
        xs = sorted(R.randint(10, 60) for _ in range(n))
        if len(set(xs)) < n - 1:
            return None
        mn, q1, q2, q3, mx = five(xs)
        d = ", ".join(map(str, xs))
        if how == "q1":
            return N("다음 자료의 <b>제1사분위수</b>는?<br>%s" % d, q1, [q3, q2, Fr(mn + q2, 2), mn], "중앙값보다 작은 쪽 자료의 중앙값이에요. <b>%s</b>" % (neg(q1) if Fr(q1).denominator == 1 else dec(q1)), f=lambda v: neg(v) if Fr(v).denominator == 1 else dec(v))
        if how == "q3":
            return N("다음 자료의 <b>제3사분위수</b>는?<br>%s" % d, q3, [q1, q2, Fr(mx + q2, 2), mx], "중앙값보다 큰 쪽 자료의 중앙값이에요. <b>%s</b>" % (neg(q3) if Fr(q3).denominator == 1 else dec(q3)), f=lambda v: neg(v) if Fr(v).denominator == 1 else dec(v))
        if how == "med":
            return N("다음 자료의 <b>중앙값(제2사분위수)</b>은?<br>%s" % d, q2, [q1, q3, Fr(sum(xs), n), Fr(mn + mx, 2)], "<b>%s</b>" % (neg(q2) if Fr(q2).denominator == 1 else dec(q2)), f=lambda v: neg(v) if Fr(v).denominator == 1 else dec(v))
        if how == "iqr":
            return N("다음 자료의 <b>사분위수범위</b>는?<br>%s" % d, q3 - q1, [mx - mn, q3 - q2, q2 - q1, q3 + q1], "(제3사분위수) − (제1사분위수) = %s − %s = <b>%s</b>" % (dec(q3), dec(q1), dec(q3 - q1)), f=lambda v: neg(v) if Fr(v).denominator == 1 else dec(v))
        return N("다음 자료의 <b>범위</b>는?<br>%s" % d, mx - mn, [q3 - q1, mx, mx - q1, mx - mn + 1], "(최댓값) − (최솟값) = <b>%d</b>" % (mx - mn))
    return mk


def b_read(kinds=("read", "iqr", "pct", "compare")):
    def mk():
        how = R.choice(kinds)
        step = R.choice([5, 10])
        lo = R.choice([0, 10, 20, 30])
        vals = sorted(R.sample(range(lo + step // 5 * 0 + 1, lo + 8 * step), 5))
        mn, q1, q2, q3, mx = [lo + step * round((v - lo) / step) if R.random() < 0.6 else v for v in vals]
        fv = sorted([mn, q1, q2, q3, mx])
        if len(set(fv)) < 5:
            return None
        mn, q1, q2, q3, mx = fv
        g = box_svg(fv, lo, lo + 8 * step, step)
        if how == "read":
            k = R.choice([("최솟값", mn), ("제1사분위수", q1), ("중앙값", q2), ("제3사분위수", q3), ("최댓값", mx)])
            if k[1] % step and k[1] % step != step // 2:
                return None
            return N("상자그림에서 <b>%s</b>은? (눈금은 %d 간격)%s" % (k[0], step, g), k[1], [x for x in fv if x != k[1]], "<b>%d</b>" % k[1])
        for v in fv:
            if v % step and v % step != step // 2:
                return None
        if how == "iqr":
            return N("상자그림에서 <b>사분위수범위</b>는? (눈금은 %d 간격)%s" % (step, g), q3 - q1, [mx - mn, q3 - q2, q2 - q1, q3], "상자의 길이예요. %d − %d = <b>%d</b>" % (q3, q1, q3 - q1))
        if how == "pct":
            k = R.choice([("제1사분위수 이하", 25), ("중앙값 이상", 50), ("제3사분위수 이상", 25), ("제1사분위수와 제3사분위수 사이", 50), ("제3사분위수 이하", 75)])
            return N("자료가 많을 때, 상자그림에서 <b>%s</b>인 자료는 전체의 약 몇 %%일까요?%s" % (k[0], g), k[1], [x for x in (25, 50, 75, 100) if x != k[1]], "사분위수는 자료를 크기순으로 4등분해요. <b>%d%%</b>" % k[1], f=lambda v: "%s%%" % neg(v))
        F_ = [("상자그림에서 상자의 길이가 나타내는 것은?", "사분위수범위", ["범위", "평균", "표준편차"], "<b>사분위수범위</b>(Q3 − Q1)예요."),
              ("상자그림에서 상자 안의 세로선이 나타내는 것은?", "중앙값", ["평균", "최빈값", "제1사분위수"], "<b>중앙값</b>이에요."),
              ("두 상자그림의 상자 길이가 다를 때, 상자가 더 긴 쪽은?", "가운데 50%의 자료가 더 넓게 퍼져 있어요", ["평균이 더 커요", "자료의 개수가 더 많아요", "최댓값이 더 커요"], "상자의 길이로 흩어진 정도를 비교해요."),
              ("상자그림으로 알 수 <b>없는</b> 것은?", "평균", ["중앙값", "최댓값", "사분위수범위"], "상자그림에는 <b>평균</b>이 나타나지 않아요.")]
        q_, a_, b_, e_ = R.choice(F_)
        return M(q_ + g, a_, b_, e_)
    return mk


# ------------------------------------------------------------------ 산점도와 상관관계
def scat_svg(pts, xl, yl, lo=0, hi=10, diag=False):
    W, H = 300, 260
    X = lambda v: 40 + (v - lo) / (hi - lo) * (W - 60)
    Y = lambda v: H - 34 - (v - lo) / (hi - lo) * (H - 60)
    s = [line(X(lo), Y(lo), X(hi), Y(lo), INK, 2) + line(X(lo), Y(lo), X(lo), Y(hi), INK, 2)]
    for v in range(lo, hi + 1, 2):
        s.append(text(X(v), Y(lo) + 18, str(v), 12, weight=500) + text(X(lo) - 8, Y(v) + 4, str(v), 12, anchor="end", weight=500))
        if v:
            s.append(line(X(v), Y(lo), X(v), Y(hi), "#e5e5e5", 1) + line(X(lo), Y(v), X(hi), Y(v), "#e5e5e5", 1))
    if diag:
        s.append(line(X(lo), Y(lo), X(hi), Y(hi), RED, 1.6, " stroke-dasharray='6 4'"))
    for x, y in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (X(x), Y(y), BLUE))
    s.append(text(W - 6, Y(lo) + 30, xl, 12, anchor="end", weight=500) + text(X(lo) + 4, 14, yl, 12, anchor="start", weight=500))
    return svgf(W, H, "".join(s), "산점도")


def corr_pts(kind, n=14):
    pts = set()
    while len(pts) < n:
        x = R.uniform(0.5, 9.5)
        if kind == "pos":
            y = x + R.uniform(-1.6, 1.6)
        elif kind == "neg":
            y = 10 - x + R.uniform(-1.6, 1.6)
        else:
            y = R.uniform(0.5, 9.5)
        if 0.3 < y < 9.7:
            pts.add((round(x, 1), round(y, 1)))
    return sorted(pts)


PAIRS = {"pos": [("키", "몸무게"), ("공부 시간", "시험 점수"), ("기온", "아이스크림 판매량"), ("통화 시간", "통화 요금"), ("운동 시간", "소모 열량")],
         "neg": [("산의 높이", "기온"), ("자동차의 주행 거리", "남은 연료의 양"), ("스마트폰 사용 시간", "수면 시간"), ("가격", "판매량"), ("결석 횟수", "출석 점수")],
         "none": [("키", "수학 점수"), ("신발 크기", "독서 시간"), ("생일의 날짜", "키"), ("이름의 글자 수", "몸무게"), ("머리카락 길이", "수학 점수")]}
KN = {"pos": "양의 상관관계", "neg": "음의 상관관계", "none": "상관관계가 없다"}


def sc_read(kinds=("type", "pair", "count")):
    def mk():
        how = R.choice(kinds)
        if how == "type":
            k = R.choice(["pos", "neg", "none"])
            pts = corr_pts(k)
            a, b = R.choice(PAIRS[k])
            ok = KN[k]
            return M("두 변량 x, y에 대한 산점도예요. 두 변량 사이의 관계는?%s" % scat_svg(pts, "x", "y"), ok, [v for kk, v in KN.items() if kk != k] + ["알 수 없다"],
                     "점들이 %s. <b>%s</b>" % ({"pos": "오른쪽 위로 향하는 직선 주위에 모여 있어요", "neg": "오른쪽 아래로 향하는 직선 주위에 모여 있어요", "none": "흩어져 있어요"}[k], ok))
        if how == "pair":
            k = R.choice(["pos", "neg", "none"])
            a, b = R.choice(PAIRS[k])
            return M("<b>%s</b>%s <b>%s</b> 사이의 상관관계로 가장 알맞은 것은?" % (a, josa(a, "과/와")[len(a):], b), KN[k], [v for kk, v in KN.items() if kk != k] + ["항상 같다"],
                     "<b>%s</b>" % KN[k])
        pts = corr_pts(R.choice(["pos", "none"]), 12)
        pts = [(round(x), round(y)) for x, y in pts]
        pts = sorted(set(pts))
        k = R.choice(["above", "below", "eq"])
        c = {"above": sum(1 for x, y in pts if y > x), "below": sum(1 for x, y in pts if y < x), "eq": sum(1 for x, y in pts if y == x)}[k]
        nm = {"above": "1차 점수보다 2차 점수가 높은", "below": "1차 점수보다 2차 점수가 낮은", "eq": "1차 점수와 2차 점수가 같은"}[k]
        return N("학생 %d명의 1차, 2차 시험 점수의 산점도예요(가로축 1차, 세로축 2차). %s 학생은 몇 명일까요?%s" % (len(pts), nm, scat_svg(pts, "1차", "2차", diag=True)), c, [len(pts) - c, c + 1, c - 1 if c else c + 2, len(pts)],
                 "점선 y = x를 기준으로 %s 점을 세요. <b>%d명</b>" % ({"above": "위쪽", "below": "아래쪽", "eq": "선 위의"}[k], c), f=lambda v: "%s명" % neg(v))
    return mk


def sc_concept():
    F_ = [("양의 상관관계가 있을 때 x의 값이 커지면 y의 값은 대체로?", "커져요", ["작아져요", "변하지 않아요", "0이 돼요"], "<b>커져요</b>."),
          ("음의 상관관계가 있을 때 x의 값이 커지면 y의 값은 대체로?", "작아져요", ["커져요", "변하지 않아요", "항상 같아요"], "<b>작아져요</b>."),
          ("산점도에서 점들이 한 직선에 가까이 모여 있을수록?", "상관관계가 강해요", ["상관관계가 약해요", "상관관계가 없어요", "자료가 적어요"], "<b>상관관계가 강해요</b>."),
          ("두 변량 사이에 상관관계가 있으면 반드시 한쪽이 다른 쪽의 원인일까요?", "아니요, 원인과 결과라고 단정할 수 없어요", ["네, 항상 원인이에요", "양의 상관관계일 때만 원인이에요", "음의 상관관계일 때만 원인이에요"],
           "상관관계는 함께 변하는 경향일 뿐 <b>원인과 결과를 뜻하지 않아요</b>."),
          ("산점도는 무엇을 나타낸 그래프일까요?", "두 변량의 순서쌍을 좌표평면에 점으로 나타낸 그래프", ["한 변량의 도수를 막대로 나타낸 그래프", "자료를 크기순으로 나열한 표", "상자와 수염으로 나타낸 그래프"],
           "<b>두 변량의 순서쌍을 점으로 나타낸 그래프</b>예요.")]
    pool = F_[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        return M(*pool.pop())
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "trig":
        return unit(G, "trigonometric-ratios", 10, "[9수03-16]", "삼각비의 뜻을 알고, 간단한 삼각비의 값을 구할 수 있다.",
                    "삼각비의 뜻과 특수한 각의 삼각비", "삼각비",
                    "중학교 3학년 수학 삼각비 문제: 직각삼각형에서 sin, cos, tan의 값, 한 삼각비로 다른 삼각비 구하기, 30°·45°·60°의 삼각비, 삼각비를 이용한 변의 길이, 삼각비의 표까지 100문제와 정답·해설.",
                    "sin A = 높이 ÷ 빗변", "cos A = 밑변 ÷ 빗변, tan A = 높이 ÷ 밑변이에요.",
                    ["∠C = 90°인 직각삼각형 ABC에서 sin A = BC/AB, cos A = AC/AB, tan A = BC/AC예요.",
                     "삼각비의 값은 삼각형의 크기와 관계없이 각의 크기에 따라 정해져요.",
                     "sin 30° = ½, sin 45° = √2/2, sin 60° = √3/2, cos 30° = √3/2, cos 45° = √2/2, cos 60° = ½, tan 30° = √3/3, tan 45° = 1, tan 60° = √3",
                     "0°에서 90°까지의 삼각비는 삼각비의 표로 어림한 값을 찾을 수 있어요."],
                    [("BC = 3, AC = 4, AB = 5에서 sin A", ["3 ÷ 5"], "3/5"), ("sin 30° + cos 60°", ["½ + ½"], "1")],
                    [("sin A를 밑변 ÷ 빗변으로 계산한다", "sin은 높이(대변) ÷ 빗변이에요."),
                     ("tan A를 높이 ÷ 빗변으로 계산한다", "tan은 높이 ÷ 밑변이에요."),
                     ("기준각을 바꾸지 않고 ∠B의 삼각비를 구한다", "∠B 기준으로 높이와 밑변이 바뀌어요.")],
                    [("sin, cos, tan은 어떻게 읽나요?", "사인, 코사인, 탄젠트라고 읽어요."),
                     ("특수한 각의 삼각비는 어떻게 기억하나요?", "한 변이 1인 정사각형의 대각선, 한 변이 2인 정삼각형의 높이로 직각삼각형을 만들면 쉽게 구할 수 있어요.")],
                    [("삼각비의 뜻", [(t_ratio(("sin", "cos", "tan")), 20)]),
                     ("삼각비로 변의 길이 구하기", [(t_ratio(("find",)), 12), (t_one(), 8)]),
                     ("특수한 각의 삼각비", [(t_special(("val", "ang")), 20)]),
                     ("특수한 각의 계산", [(t_special(("expr", "side")), 20)]),
                     ("삼각비의 표", [(t_table(), 20)])], 82910)
    if which == "trigx":
        return unit(G, "applications-of-trigonometric-ratios", 11, "[9수03-17]", "삼각비를 활용하여 여러 가지 문제를 해결할 수 있다.",
                    "삼각비의 활용: 높이, 거리, 넓이", "삼각비의 활용",
                    "중학교 3학년 수학 삼각비의 활용 문제: 올려본각으로 나무와 건물의 높이 구하기, 비탈길의 높이와 거리, 강의 폭, 두 변과 끼인각으로 삼각형과 평행사변형의 넓이 구하기까지 100문제와 정답·해설.",
                    "삼각형의 넓이 = ½ab sin C", "높이 = (수평 거리) × tan(올려본각)",
                    ["직각삼각형의 한 변과 한 예각을 알면 삼각비로 나머지 변의 길이를 구할 수 있어요.",
                     "높이 = (수평 거리) × tan(올려본각), 수직 높이 = (비탈길의 길이) × sin(경사각)",
                     "두 변 a, b와 그 끼인각 C가 예각이면 삼각형의 넓이는 ½ab sin C, 둔각이면 ½ab sin(180° − C)예요.",
                     "평행사변형의 넓이는 ab sin C예요."],
                    [("거리 10 m, 올려본각 45°", ["10 × tan 45°"], "10 m"), ("4, 6, 끼인각 30°인 삼각형", ["½ × 4 × 6 × ½"], "6 cm²")],
                    [("높이를 구할 때 sin과 tan을 바꾼다", "수평 거리와 높이의 관계는 tan이에요."),
                     ("삼각형의 넓이에서 ½을 빠뜨린다", "평행사변형은 ab sin C, 삼각형은 ½ab sin C예요."),
                     ("둔각의 사인 값을 그대로 쓴다", "중학교에서는 180°에서 뺀 예각의 사인 값을 써요.")],
                    [("눈높이는 어떻게 처리하나요?", "삼각비로 구한 높이에 눈높이를 더하면 실제 높이가 돼요."),
                     ("측량에서 실제로 쓰이나요?", "건물의 높이, 강의 폭, 산의 높이를 직접 재지 않고 계산할 때 써요.")],
                    [("높이 구하기", [(x_height(("tree", "build")), 20)]),
                     ("비탈길과 거리", [(x_height(("slope", "river")), 20)]),
                     ("삼각형의 넓이", [(x_area(("tri", "obtuse")), 20)]),
                     ("평행사변형의 넓이와 수선", [(x_area(("para", "side")), 20)]),
                     ("섞어서 연습", [(x_height(), 10), (x_area(), 10)])], 82911)
    if which == "chord":
        return unit(G, "chords-and-tangents", 12, "[9수03-18]", "원의 현에 관한 성질과 접선에 관한 성질을 이해하고 설명할 수 있다.",
                    "원의 현과 접선의 성질", "원과 직선",
                    "중학교 3학년 수학 원의 현과 접선 문제: 중심에서 현에 내린 수선과 현의 길이, 같은 거리의 현, 접선의 길이, 접선과 반지름, 원에 외접하는 사각형, 삼각형의 내접원과 둘레까지 100문제와 정답·해설.",
                    "중심에서 현에 내린 수선은 현을 이등분해요", "원 밖의 한 점에서 그은 두 접선의 길이는 같아요.",
                    ["원의 중심에서 현에 내린 수선은 그 현을 <b>이등분</b>해요. 현의 수직이등분선은 원의 중심을 지나요.",
                     "한 원에서 중심으로부터 같은 거리에 있는 두 현의 길이는 같아요.",
                     "원의 접선은 접점을 지나는 반지름에 <b>수직</b>이에요. 원 밖의 한 점에서 그은 두 접선의 길이는 같아요.",
                     "원에 외접하는 사각형 ABCD에서 AB + CD = AD + BC예요."],
                    [("반지름 5, 중심과의 거리 3인 현", ["√(25 − 9) = 4", "4 × 2"], "8"), ("반지름 3, PO = 5", ["√(25 − 9)"], "PT = 4")],
                    [("현의 길이의 반만 구하고 끝낸다", "피타고라스 정리로 구한 것은 현의 절반이에요."),
                     ("접선과 반지름이 이루는 각을 45°라고 한다", "항상 90°예요."),
                     ("외접사각형에서 이웃한 두 변의 합이 같다고 한다", "마주 보는 두 변의 합이 같아요.")],
                    [("접선은 원과 몇 점에서 만나나요?", "한 점(접점)에서만 만나요."),
                     ("왜 두 접선의 길이가 같나요?", "△PAO와 △PBO가 RHS 합동이기 때문이에요.")],
                    [("현의 길이", [(c_chord(("half", "dist")), 20)]),
                     ("현의 성질", [(c_chord(("radius", "equal")), 20)]),
                     ("접선의 길이", [(c_tan(("len", "eq")), 20)]),
                     ("접선과 각, 외접사각형", [(c_tan(("angle", "quad")), 20)]),
                     ("섞어서 연습", [(c_tan(("tri",)), 8), (c_chord(), 6), (c_tan(), 6)])], 82912)
    if which == "insc":
        return unit(G, "inscribed-angles", 13, "[9수03-19]", "원주각의 성질을 이해하고 설명할 수 있다.",
                    "원주각의 성질", "원주각",
                    "중학교 3학년 수학 원주각 문제: 원주각과 중심각의 관계, 같은 호에 대한 원주각, 지름에 대한 원주각, 원에 내접하는 사각형, 접선과 현이 이루는 각, 호의 길이와 원주각까지 100문제와 정답·해설.",
                    "원주각 = ½ × 중심각", "같은 호에 대한 원주각은 모두 같아요.",
                    ["원 위의 한 점에서 그은 두 현이 이루는 각을 <b>원주각</b>이라고 해요.",
                     "한 호에 대한 원주각의 크기는 그 호에 대한 중심각의 크기의 <b>½</b>이에요.",
                     "같은 호에 대한 원주각의 크기는 모두 같고, 반원(지름)에 대한 원주각은 <b>90°</b>예요.",
                     "원에 내접하는 사각형의 대각의 합은 180°이고, 접선과 현이 이루는 각은 그 안의 호에 대한 원주각과 같아요."],
                    [("중심각 100°", ["100° ÷ 2"], "원주각 50°"), ("내접사각형 ∠A = 75°", ["180° − 75°"], "∠C = 105°")],
                    [("원주각을 중심각과 같다고 한다", "원주각은 중심각의 ½이에요."),
                     ("지름에 대한 원주각을 180°라고 한다", "중심각이 180°이고 원주각은 90°예요."),
                     ("내접사각형에서 이웃한 두 각의 합을 180°라고 한다", "마주 보는 두 각의 합이 180°예요.")],
                    [("원주각은 왜 중심각의 반인가요?", "중심 O를 지나는 지름을 그으면 이등변삼각형 두 개로 나뉘고, 외각의 성질로 설명돼요."),
                     ("호의 길이와 원주각의 관계는?", "한 원에서 호의 길이는 원주각의 크기에 정비례해요.")],
                    [("원주각과 중심각", [(i_basic(("cen", "ins")), 20)]),
                     ("같은 호와 지름", [(i_basic(("same", "semi")), 20)]),
                     ("원에 내접하는 사각형", [(i_more(("cyc", "cycext")), 20)]),
                     ("접선과 현, 호의 길이", [(i_more(("tanchord", "arc")), 20)]),
                     ("섞어서 연습", [(i_basic(), 10), (i_more(), 10)])], 82913)
    if which == "var":
        return unit(G, "variance-and-standard-deviation", 14, "[9수04-07]", "분산과 표준편차의 의미를 이해하고, 이를 구할 수 있다.",
                    "산포도: 편차, 분산, 표준편차", "분산과 표준편차",
                    "중학교 3학년 수학 분산과 표준편차 문제: 편차 구하기, 편차의 합이 0인 성질, 분산과 표준편차 계산, 분산과 표준편차의 관계, 표준편차로 자료의 흩어진 정도 비교하기까지 100문제와 정답·해설.",
                    "분산 = 편차의 제곱의 평균", "표준편차 = √(분산), 작을수록 고르게 모여 있어요.",
                    ["(편차) = (변량) − (평균)이고, 편차의 합은 항상 <b>0</b>이에요.",
                     "<b>분산</b>은 편차의 제곱의 평균이에요.",
                     "<b>표준편차</b>는 분산의 음이 아닌 제곱근이고, 단위는 변량의 단위와 같아요.",
                     "표준편차가 작을수록 자료가 평균 가까이 모여 있고, 클수록 넓게 흩어져 있어요."],
                    [("2, 4, 6, 8의 분산", ["평균 5", "(9 + 1 + 1 + 9) ÷ 4"], "5"), ("분산 9", ["√9"], "표준편차 3")],
                    [("편차의 평균을 분산이라고 한다", "편차의 평균은 항상 0이에요. 제곱해서 평균을 내요."),
                     ("분산과 표준편차를 바꾼다", "표준편차는 분산에 √를 씌운 값이에요."),
                     ("편차를 평균 − 변량으로 계산한다", "변량 − 평균이에요.")],
                    [("왜 편차를 제곱하나요?", "그대로 더하면 양수와 음수가 지워져 0이 되기 때문이에요."),
                     ("평균이 같아도 분산이 다를 수 있나요?", "네. 자료가 흩어진 정도가 다르면 분산이 달라요.")],
                    [("편차", [(v_dev(("dev", "unk")), 20)]),
                     ("분산", [(v_dev(("var",)), 20)]),
                     ("표준편차", [(v_dev(("sd",)), 12), (v_compare(("from_sd",)), 8)]),
                     ("자료의 흩어진 정도 비교", [(v_compare(("which",)), 14), (v_compare(("concept",)), 6)]),
                     ("섞어서 연습", [(v_dev(), 14), (v_compare(("which",)), 6)])], 82914)
    if which == "box":
        return unit(G, "box-plots", 15, "[9수04-08]", "공학 도구를 이용하여 자료를 상자그림으로 나타내고 분포를 비교할 수 있다.",
                    "사분위수와 상자그림", "상자그림",
                    "중학교 3학년 수학 상자그림 문제: 최솟값·제1사분위수·중앙값·제3사분위수·최댓값 구하기, 범위와 사분위수범위, 상자그림 읽기, 사분위수가 나타내는 비율, 분포 비교까지 100문제와 정답·해설.",
                    "사분위수범위 = Q3 − Q1", "상자그림은 다섯 개의 값으로 분포를 나타내요.",
                    ["자료를 크기순으로 늘어놓고 4등분하는 값을 <b>사분위수</b>라고 해요(Q1, Q2 = 중앙값, Q3).",
                     "Q1은 중앙값보다 작은 쪽 자료의 중앙값, Q3은 중앙값보다 큰 쪽 자료의 중앙값이에요.",
                     "<b>상자그림</b>은 최솟값, Q1, 중앙값, Q3, 최댓값을 이용해 상자와 수염으로 나타내요.",
                     "(범위) = (최댓값) − (최솟값), (사분위수범위) = Q3 − Q1이에요."],
                    [("3, 5, 7, 9, 11, 13", ["Q1 = 5, Q2 = 8, Q3 = 11"], "사분위수범위 6"), ("상자의 왼쪽 끝", ["Q1"], "제1사분위수")],
                    [("사분위수범위를 범위로 쓴다", "범위는 최댓값 − 최솟값이고, 사분위수범위는 상자의 길이예요."),
                     ("중앙값을 평균으로 착각한다", "상자 안의 선은 중앙값이에요."),
                     ("크기순으로 늘어놓지 않고 사분위수를 구한다", "먼저 작은 값부터 늘어놓아요.")],
                    [("상자그림의 장점은?", "여러 집단의 분포를 한눈에 비교할 수 있고 극단적인 값의 영향을 덜 받아요."),
                     ("공학 도구는 어떻게 쓰나요?", "스프레드시트나 통계 프로그램에 자료를 넣으면 상자그림을 바로 그릴 수 있어요.")],
                    [("사분위수", [(b_five(("q1", "q3", "med")), 20)]),
                     ("범위와 사분위수범위", [(b_five(("iqr", "range")), 20)]),
                     ("상자그림 읽기", [(b_read(("read", "iqr")), 20)]),
                     ("상자그림과 비율", [(b_read(("pct", "compare")), 20)]),
                     ("섞어서 연습", [(b_five(), 10), (b_read(), 10)])], 82915)
    if which == "scat":
        return unit(G, "scatter-plots-and-correlation", 16, "[9수04-09]", "자료를 수집하여 산점도로 나타내고, 이를 이용하여 상관관계를 말할 수 있다.",
                    "산점도와 상관관계", "산점도와 상관관계",
                    "중학교 3학년 수학 산점도와 상관관계 문제: 산점도 읽기, 양의 상관관계·음의 상관관계·상관관계가 없는 경우, 실생활 두 변량의 상관관계, 기준선을 이용한 점의 개수 세기까지 100문제와 정답·해설.",
                    "오른쪽 위로 모이면 양, 오른쪽 아래로 모이면 음", "상관관계가 있어도 원인과 결과라고 단정할 수 없어요.",
                    ["두 변량 x, y의 순서쌍 (x, y)를 좌표평면 위에 점으로 나타낸 그래프를 <b>산점도</b>라고 해요.",
                     "x가 커질 때 y도 대체로 커지면 <b>양의 상관관계</b>, y가 대체로 작아지면 <b>음의 상관관계</b>예요.",
                     "점들이 흩어져 있어 증가·감소의 경향이 없으면 <b>상관관계가 없다</b>고 해요.",
                     "점들이 한 직선 가까이 모여 있을수록 상관관계가 강해요."],
                    [("공부 시간과 점수", ["함께 늘어남"], "양의 상관관계"), ("산의 높이와 기온", ["높을수록 낮아짐"], "음의 상관관계")],
                    [("오른쪽 아래로 향하는 산점도를 양의 상관관계라고 한다", "y가 감소하므로 음의 상관관계예요."),
                     ("상관관계가 있으면 원인과 결과라고 한다", "함께 변하는 경향일 뿐이에요."),
                     ("점이 적어 보이면 상관관계가 없다고 한다", "점들이 놓인 방향으로 판단해요.")],
                    [("상관관계의 강약은 어떻게 판단하나요?", "점들이 직선 주위에 좁게 모일수록 강하고, 넓게 퍼질수록 약해요."),
                     ("고등학교에서는 무엇을 배우나요?", "상관계수와 회귀 같은 내용을 더 배워요.")],
                    [("산점도 읽기", [(sc_read(("type",)), 20)]),
                     ("실생활의 상관관계", [(sc_read(("pair",)), 15), (sc_concept(), 5)]),
                     ("기준선과 점의 개수", [(sc_read(("count",)), 20)]),
                     ("상관관계의 뜻", [(sc_read(("type", "pair")), 20)]),
                     ("섞어서 연습", [(sc_read(), 20)])], 82916)
    raise ValueError(which)
