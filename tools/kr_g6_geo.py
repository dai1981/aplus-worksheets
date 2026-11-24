# -*- coding: utf-8 -*-
"""
대한민국 초등 6학년 수학：도형과 측정
  prism   : 각기둥과 각뿔 [6수03-05] [6수03-06]
  volume  : 직육면체의 겉넓이와 부피 [6수03-17] [6수03-18] [6수03-19]
  cubes   : 쌓기나무(공간과 입체) [6수03-09] [6수03-10]
  circum  : 원주와 원주율 [6수03-15] [6수03-16]
  carea   : 원의 넓이 [6수03-16]
  solids  : 원기둥, 원뿔, 구 [6수03-07] [6수03-08]
원주율은 3.14. 誤答は「n각기둥의 꼭짓점을 n+2로」「겉넓이에서 2배를 빠뜨린다」「1 m³ = 100 cm³」「반지름과 지름을 헷갈린다」「원의 넓이에 지름을 두 번 곱한다」から作る。
"""
import random
from decimal import Decimal as D
from kr_common import mcq, unit, Names, josa, num
from kr_pics56 import iso_cubes, views_panel, box_svg, circle_svg

R = random.Random(82602)
NM = Names(R)
PI = D("3.14")
POLY = {3: "삼각", 4: "사각", 5: "오각", 6: "육각", 7: "칠각", 8: "팔각", 9: "구각", 10: "십각"}


def dd(v):
    v = D(v)
    s = format(v.quantize(D("0.01")) if v != v.to_integral() else v.to_integral(), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    i, _, f = s.partition(".")
    i = num(int(i))
    return i + ("." + f if f else "")


# ---------------------------------------------------------------- 각기둥과 각뿔
def prism_count():
    n = R.randint(3, 10)
    kind = R.choice(["기둥", "뿔"])
    part = R.choice(["면", "모서리", "꼭짓점"])
    if kind == "기둥":
        v = {"면": n + 2, "모서리": 3 * n, "꼭짓점": 2 * n}[part]
        wr = {"면": [n + 1, n, 2 * n], "모서리": [2 * n, 3 * n + 2, n + 2], "꼭짓점": [n + 2, n + 1, 3 * n]}[part]
        rule = {"면": "(한 밑면의 변의 수) + 2", "모서리": "(한 밑면의 변의 수) × 3", "꼭짓점": "(한 밑면의 변의 수) × 2"}[part]
    else:
        v = {"면": n + 1, "모서리": 2 * n, "꼭짓점": n + 1}[part]
        wr = {"면": [n + 2, n, 2 * n], "모서리": [3 * n, n + 1, 2 * n + 1], "꼭짓점": [n, 2 * n, n + 2]}[part]
        rule = {"면": "(밑면의 변의 수) + 1", "모서리": "(밑면의 변의 수) × 2", "꼭짓점": "(밑면의 변의 수) + 1"}[part]
    return mcq("%s%s의 %s 몇 개인가요?" % (POLY[n], kind, josa(part, "은/는")), "%d개" % v, ["%d개" % x for x in wr],
               "%s%s의 %s 수는 %s = <b>%d개</b>예요." % (POLY[n], kind, part, rule, v))


def prism_name():
    n = R.randint(3, 9)
    kind = R.choice(["기둥", "뿔"])
    k = R.choice(["edge", "vert", "face", "base"])
    if k == "base":
        q = "밑면의 모양이 %s형인 %s의 이름은?" % (POLY[n], "각" + kind)
        a = POLY[n] + kind
        others = [POLY[n] + ("뿔" if kind == "기둥" else "기둥"), POLY[n + 1] + kind, POLY[n - 1] + kind if n > 3 else POLY[n + 2] + kind]
        return mcq(q, a, others, "각%s의 이름은 밑면의 모양에 따라 정해요. <b>%s</b>" % (kind, a))
    v = {"기둥": {"edge": 3 * n, "vert": 2 * n, "face": n + 2}, "뿔": {"edge": 2 * n, "vert": n + 1, "face": n + 1}}[kind][k]
    nm = {"edge": "모서리", "vert": "꼭짓점", "face": "면"}[k]
    a = POLY[n] + kind
    alts = [POLY[m] + kind for m in POLY if m != n and ({"기둥": {"edge": 3 * m, "vert": 2 * m, "face": m + 2}, "뿔": {"edge": 2 * m, "vert": m + 1, "face": m + 1}}[kind][k] != v)]
    return mcq("%s이 %d개인 각%s의 이름은?" % (nm, v, kind), a, R.sample(alts, 3), "%s의 %s 수를 거꾸로 생각해요. <b>%s</b>" % ("각" + kind, nm, a))


PF = [("각기둥의 두 밑면은 서로 평행하고 합동이에요.", "○"), ("각기둥의 옆면은 모두 직사각형이에요.", "○"), ("각뿔의 옆면은 모두 삼각형이에요.", "○"),
      ("각뿔의 밑면은 2개예요.", "×"), ("각기둥의 밑면과 옆면은 서로 수직이에요.", "○"), ("각뿔에서 모든 옆면이 만나는 점을 각뿔의 꼭짓점이라고 해요.", "○"),
      ("각기둥의 높이는 두 밑면 사이의 거리예요.", "○"), ("각뿔의 옆면은 직사각형이에요.", "×"), ("직육면체도 각기둥이에요.", "○")]


def prism_fact():
    t, a = R.choice(PF)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "모양에 따라 달라요"],
               "각기둥: 평행하고 합동인 두 밑면, 직사각형 옆면. 각뿔: 밑면 1개, 삼각형 옆면, 각뿔의 꼭짓점 1개.")


def prism_net():
    n = R.randint(3, 8)
    k = R.choice(["side", "w", "all"])
    if k == "side":
        return mcq("%s기둥의 전개도에서 옆면은 몇 개인가요?" % POLY[n], "%d개" % n, ["%d개" % x for x in (n + 2, 2, n - 1)],
                   "옆면의 수는 밑면의 변의 수와 같아요. <b>%d개</b>" % n)
    a, h = R.randint(2, 9), R.randint(3, 12)
    if k == "w":
        return mcq("밑면이 한 변 %d cm인 정%s형이고 높이가 %d cm인 %s기둥의 전개도에서 옆면 전체(직사각형)의 가로는 몇 cm인가요?" % (a, POLY[n], h, POLY[n]), "%d cm" % (a * n),
                   ["%d cm" % x for x in (a * (n + 2), h * n, a + h)], "옆면 전체의 가로는 밑면의 둘레와 같아요. %d × %d = <b>%d cm</b>" % (a, n, a * n))
    return mcq("밑면이 한 변 %d cm인 정%s형이고 높이가 %d cm인 %s기둥의 모든 모서리의 길이의 합은?" % (a, POLY[n], h, POLY[n]), "%d cm" % (2 * a * n + h * n),
               ["%d cm" % x for x in (a * n + h * n, 2 * a * n + h, 3 * n * a)], "밑면의 모서리 %d × %d × 2 + 옆 모서리 %d × %d = <b>%d cm</b>" % (a, n, h, n, 2 * a * n + h * n))


# ---------------------------------------------------------------- 겉넓이와 부피
def sa_q():
    a, b, c = R.randint(2, 15), R.randint(2, 12), R.randint(2, 12)
    cube = R.random() < 0.3
    if cube:
        return mcq("한 모서리가 %d cm인 정육면체의 겉넓이는 몇 cm²인가요?" % a, "%d cm²" % (6 * a * a), ["%d cm²" % x for x in (a * a * a, 4 * a * a, 12 * a)],
                   "(한 면의 넓이) × 6 = %d × %d × 6 = <b>%d cm²</b>" % (a, a, 6 * a * a))
    s = 2 * (a * b + b * c + a * c)
    return mcq(box_svg(a, b, c) + "직육면체의 겉넓이는 몇 cm²인가요?", "%s cm²" % num(s), ["%s cm²" % num(x) for x in (a * b + b * c + a * c, a * b * c, 4 * (a + b + c))],
               "(세 면의 넓이의 합) × 2 = (%d + %d + %d) × 2 = <b>%s cm²</b>" % (a * b, b * c, a * c, num(s)))


def vol_q():
    a, b, c = R.randint(2, 15), R.randint(2, 12), R.randint(2, 12)
    if R.random() < 0.3:
        return mcq("한 모서리가 %d cm인 정육면체의 부피는 몇 cm³인가요?" % a, "%s cm³" % num(a ** 3), ["%s cm³" % num(x) for x in (a * a, 6 * a * a, 3 * a)],
                   "(한 모서리) × (한 모서리) × (한 모서리) = <b>%s cm³</b>" % num(a ** 3))
    return mcq(box_svg(a, b, c) + "직육면체의 부피는 몇 cm³인가요?", "%s cm³" % num(a * b * c), ["%s cm³" % num(x) for x in (2 * (a * b + b * c + a * c), a + b + c, a * b * c // a + a)],
               "(가로) × (세로) × (높이) = %d × %d × %d = <b>%s cm³</b>" % (a, b, c, num(a * b * c)))


def vol_unit():
    k = R.choice(["m2c", "c2m", "mix"])
    n = R.randint(2, 15)
    if k == "m2c":
        return mcq("%d m³는 몇 cm³인가요?" % n, "%s cm³" % num(n * 1000000), ["%s cm³" % num(n * x) for x in (1000, 10000, 100)],
                   "1 m³ = 100 cm × 100 cm × 100 cm = 1,000,000 cm³예요. <b>%s cm³</b>" % num(n * 1000000))
    if k == "c2m":
        return mcq("%s cm³는 몇 m³인가요?" % num(n * 1000000), "%d m³" % n, ["%s m³" % num(x) for x in (n * 1000, n * 100, n * 10)],
                   "1,000,000 cm³ = 1 m³예요. <b>%d m³</b>" % n)
    a, b, c = R.choice([100, 200, 300, 400, 500]), R.choice([100, 200, 300]), R.randint(1, 5)
    v = a // 100 * (b // 100) * c
    return mcq("가로 %d cm, 세로 %d cm, 높이 %d m인 직육면체의 부피는 몇 m³인가요?" % (a, b, c), "%d m³" % v, ["%s m³" % num(x) for x in (a * b * c, v * 100, a * b * c // 100)],
               "단위를 m로 맞추면 %d × %d × %d = <b>%d m³</b>" % (a // 100, b // 100, c, v))


def vol_back():
    k = R.choice(["h", "cube_sa", "cube_v"])
    if k == "h":
        a, b, c = R.randint(2, 12), R.randint(2, 10), R.randint(2, 10)
        return mcq("부피가 %d cm³이고 가로가 %d cm, 세로가 %d cm인 직육면체의 높이는 몇 cm인가요?" % (a * b * c, a, b), "%d cm" % c,
                   ["%d cm" % x for x in (a * b * c - a - b, a * b * c // a, c + 1)], "%d ÷ (%d × %d) = <b>%d cm</b>" % (a * b * c, a, b, c))
    a = R.randint(2, 12)
    if k == "cube_sa":
        return mcq("겉넓이가 %d cm²인 정육면체의 한 모서리는 몇 cm인가요?" % (6 * a * a), "%d cm" % a, ["%d cm" % x for x in (a * a, 6 * a, a + 1)],
                   "한 면의 넓이는 %d ÷ 6 = %d cm², %d × %d = %d이므로 <b>%d cm</b>" % (6 * a * a, a * a, a, a, a * a, a))
    return mcq("부피가 %s cm³인 정육면체의 한 모서리는 몇 cm인가요?" % num(a ** 3), "%d cm" % a, ["%d cm" % x for x in (a * a, a + 2, 3 * a)],
               "%d × %d × %d = %s이므로 <b>%d cm</b>" % (a, a, a, num(a ** 3), a))


def vol_story():
    k = R.choice(["box", "water", "cubes"])
    if k == "box":
        a, b, c = R.randint(10, 40), R.randint(10, 30), R.randint(5, 20)
        return mcq("가로 %d cm, 세로 %d cm, 높이 %d cm인 상자의 겉면을 모두 포장지로 싸려고 해요. 필요한 포장지의 넓이는 적어도 몇 cm²인가요?" % (a, b, c),
                   "%s cm²" % num(2 * (a * b + b * c + a * c)), ["%s cm²" % num(x) for x in (a * b + b * c + a * c, a * b * c, 2 * a * b + b * c)],
                   "겉넓이를 구해요. (%d + %d + %d) × 2 = <b>%s cm²</b>" % (a * b, b * c, a * c, num(2 * (a * b + b * c + a * c))))
    if k == "water":
        a, b, h = R.randint(10, 40), R.randint(10, 30), R.randint(2, 10)
        return mcq("가로 %d cm, 세로 %d cm인 직육면체 모양 수조에 돌을 넣었더니 물의 높이가 %d cm 올라갔어요. 돌의 부피는 몇 cm³인가요?" % (a, b, h), "%s cm³" % num(a * b * h),
                   ["%s cm³" % num(x) for x in (a * b, (a + b) * h, a * b * h * 2)], "올라간 물의 부피와 같아요. %d × %d × %d = <b>%s cm³</b>" % (a, b, h, num(a * b * h)))
    a, b, c = R.randint(2, 6), R.randint(2, 6), R.randint(2, 6)
    return mcq("부피가 1 cm³인 쌓기나무로 가로 %d개, 세로 %d개, 높이 %d층인 직육면체를 만들었어요. 직육면체의 부피는 몇 cm³인가요?" % (a, b, c), "%d cm³" % (a * b * c),
               ["%d cm³" % x for x in (a + b + c, a * b, 2 * (a * b + b * c + a * c))], "%d × %d × %d = <b>%d cm³</b>" % (a, b, c, a * b * c))


# ---------------------------------------------------------------- 쌓기나무
def heights(n, m, lo=4, hi=12):
    while True:
        h = [[R.choice([0, 1, 1, 2, 2, 3]) for _ in range(m)] for _ in range(n)]
        tot = sum(map(sum, h))
        if lo <= tot <= hi and all(any(r) for r in h) and all(any(h[x][y] for x in range(n)) for y in range(m)):
            return h


def cells_of(h):
    return [(x, y, z) for x in range(len(h)) for y in range(len(h[0])) for z in range(h[x][y])]


def top_num_svg(h):
    """위에서 본 모양에 쌓은 개수를 적은 그림"""
    from ws_common import fig, svg_wrap, text, INK
    n, m = len(h), len(h[0])
    c = 36
    s = []
    for x in range(n):
        for y in range(m):
            if h[x][y]:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#e6f4ea' stroke='%s' stroke-width='1.6'/>" % (10 + x * c, 10 + y * c, c, c, INK))
                s.append(text(10 + x * c + c / 2, 10 + y * c + c / 2 + 7, str(h[x][y]), 19))
    s.append(text(10 + n * c / 2, 10 + m * c + 24, "앞", 16))
    return fig(svg_wrap(20 + n * c, m * c + 42, "".join(s), "위에서 본 모양").replace("<svg ", "<svg data-pf='lg' ", 1))


def cube_count():
    h = heights(R.choice([2, 3]), R.choice([2, 3]))
    t = sum(map(sum, h))
    if R.random() < 0.5:
        return mcq(top_num_svg(h) + "위에서 본 모양의 각 칸에 쌓은 쌓기나무의 개수를 썼어요. 쌓기나무는 모두 몇 개인가요?", "%d개" % t,
                   ["%d개" % x for x in (sum(1 for r in h for v in r if v), t + 1, t - 1)], "칸에 적힌 수를 모두 더해요. <b>%d개</b>" % t)
    return mcq(iso_cubes(cells_of(h)) + top_num_svg(h) + "쌓기나무로 쌓은 모양과 위에서 본 모양이에요. 쌓기나무는 모두 몇 개인가요?", "%d개" % t,
               ["%d개" % x for x in (t - 1, t + 2, sum(1 for r in h for v in r if v))], "위에서 본 모양의 칸마다 쌓은 개수를 더해요. <b>%d개</b>" % t)


def front_view(h):
    return [max(h[x][y] for y in range(len(h[0]))) for x in range(len(h))]


def side_view(h):
    return [max(h[x][y] for x in range(len(h))) for y in range(len(h[0]))][::-1]


def top_cells(h):
    return [(x, y) for x in range(len(h)) for y in range(len(h[0])) if h[x][y]]


def col_cells(cols, H=3):
    return ([(c, H - 1 - z) for c, hh in enumerate(cols) for z in range(hh)], len(cols), H)


def view_q():
    h = heights(R.choice([2, 3]), R.choice([2, 3]))
    k = R.choice(["앞", "옆", "위"])
    fv, sv = front_view(h), side_view(h)
    if k == "앞":
        ans = col_cells(fv)
    elif k == "옆":
        ans = col_cells(sv)
    else:
        n, m = len(h), len(h[0])
        ans = (top_cells(h), n, m)
    cands = []
    for cols in (fv, sv, fv[::-1], [max(1, c - 1) if i == 0 else c for i, c in enumerate(fv)], [c + 1 if c < 3 and i == len(sv) - 1 else c for i, c in enumerate(sv)]):
        v = col_cells(cols)
        if sorted(v[0]) != sorted(ans[0]) and v not in cands:
            cands.append(v)
    if k == "위":
        n, m = len(h), len(h[0])
        tc = top_cells(h)
        alts = []
        for _ in range(20):
            t2 = set(tc)
            c = (R.randrange(n), R.randrange(m))
            t2 ^= {c}
            v = (sorted(t2), n, m)
            if t2 and sorted(t2) != sorted(tc) and v not in alts:
                alts.append(v)
        cands = alts
    if len(cands) < 3:
        return None
    opts = [ans] + cands[:3]
    R.shuffle(opts)
    letter = "가나다라"[opts.index(ans)]
    who = {"앞": "앞에서", "옆": "오른쪽 옆에서", "위": "위에서"}[k]
    return mcq(iso_cubes(cells_of(h)) + views_panel(opts) + "쌓기나무로 쌓은 모양을 %s 본 모양은? (뒤에 보이지 않는 쌓기나무는 없어요)" % who, letter, [x for x in "가나다라" if x != letter],
               ("위에서 보면 쌓기나무가 놓인 칸이 모두 보여요. <b>%s</b>" % letter) if k == "위" else
               "%s 볼 때 각 줄에서 가장 높이 쌓은 개수만큼 보여요. <b>%s</b>" % (who, letter))


def layer_q():
    h = heights(3, 3, 6, 14)
    k = R.randint(1, 3)
    cnt = sum(1 for r in h for v in r if v >= k)
    if cnt == 0:
        return None
    return mcq(top_num_svg(h) + "위에서 본 모양에 쌓은 개수를 썼어요. %d층에 쌓은 쌓기나무는 몇 개인가요?" % k, "%d개" % cnt,
               ["%d개" % x for x in (sum(map(sum, h)), cnt + 1, cnt - 1 if cnt > 1 else cnt + 2)], "%d 이상인 칸의 수를 세요. <b>%d개</b>" % (k, cnt))


def cube_need():
    a, b, c = R.randint(2, 4), R.randint(2, 4), R.randint(2, 4)
    h = heights(R.choice([2, 3]), R.choice([2, 3]))
    t = sum(map(sum, h))
    full = len(h) * len(h[0]) * 3
    return mcq(top_num_svg(h) + "이 모양에 쌓기나무를 더 쌓아서 위에서 본 모양 그대로 모든 칸이 3층인 직육면체를 만들려고 해요. 쌓기나무가 몇 개 더 필요한가요?", "%d개" % (full - t),
               ["%d개" % x for x in (full, t, full - t + 1)], "%d × %d × 3 = %d개에서 %d개를 빼요. <b>%d개</b>" % (len(h), len(h[0]), full, t, full - t))


# ---------------------------------------------------------------- 원주와 원주율
def circum_q():
    k = R.choice(["d", "r"])
    v = R.randint(2, 30)
    d = v if k == "d" else 2 * v
    c = D(d) * PI
    pic = circle_svg("%d cm" % v, kind=k)
    return mcq(pic + "원주는 몇 cm인가요? (원주율: 3.14)", "%s cm" % dd(c),
               ["%s cm" % dd(x) for x in (D(v) * PI if k == "r" else D(d) * 2 * PI, D(d) * D(d) * PI / 4 if k == "d" else D(v) * D(v) * PI, D(d) * 3)],
               "(원주) = (지름) × (원주율) = %d × 3.14 = <b>%s cm</b>" % (d, dd(c)))


def circum_back():
    d = R.randint(2, 30)
    c = D(d) * PI
    k = R.choice(["d", "r"])
    if k == "d":
        return mcq("원주가 %s cm인 원의 지름은 몇 cm인가요? (원주율: 3.14)" % dd(c), "%d cm" % d, ["%s cm" % dd(x) for x in (D(d) / 2, D(d) * 2, c / 3)] if d % 2 == 0 else ["%s cm" % dd(x) for x in (D(d) * 2, D(d) + 1, c / 3)],
                   "(지름) = (원주) ÷ 3.14 = <b>%d cm</b>" % d)
    if d % 2:
        return None
    return mcq("원주가 %s cm인 원의 반지름은 몇 cm인가요? (원주율: 3.14)" % dd(c), "%d cm" % (d // 2), ["%d cm" % x for x in (d, d * 2, d // 2 + 1)],
               "지름은 %s ÷ 3.14 = %d cm, 반지름은 %d ÷ 2 = <b>%d cm</b>" % (dd(c), d, d, d // 2))


def ratio_pi():
    d = R.randint(5, 40)
    c = D(d) * D("3.14") + D(R.choice([-2, -1, 0, 1, 2])) / 100
    q = (c / d).quantize(D("0.01"))
    return mcq("지름이 %d cm인 원 모양 접시의 원주를 재었더니 %s cm였어요. (원주) ÷ (지름)을 반올림하여 소수 둘째 자리까지 나타내면?" % (d, dd(c)), format(q, "f"),
               [format((D(d) / c).quantize(D("0.01")), "f"), format((c / d).quantize(D("0.1")), "f"), format(q + D("0.1"), "f")],
               "(원주) ÷ (지름) = %s ÷ %d ≈ <b>%s</b>. 원의 크기와 상관없이 약 3.14로 일정해요. 이 값이 원주율이에요." % (dd(c), d, format(q, "f")))


PIF = [("원주율은 원의 크기와 상관없이 일정해요.", "○"), ("원이 클수록 원주율도 커져요.", "×"), ("원주율은 (원주) ÷ (지름)이에요.", "○"),
       ("원주는 지름의 약 3배예요.", "○"), ("원주율은 (원주) ÷ (반지름)이에요.", "×"), ("원주율은 3.14로 끝나는 수예요.", "×")]


def pi_fact():
    t, a = R.choice(PIF)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "원에 따라 달라요"],
               "원주율 = (원주) ÷ (지름) = 3.1415926…으로 끝없이 이어지는 일정한 값이고, 보통 3.14를 써요.")


def circum_story():
    k = R.choice(["wheel", "track", "half"])
    if k == "wheel":
        d = R.choice([40, 50, 60, 70, 80])
        n = R.randint(5, 30)
        dist = D(d) * PI * n
        return mcq("지름이 %d cm인 바퀴가 %d바퀴 굴러간 거리는 몇 cm인가요? (원주율: 3.14)" % (d, n), "%s cm" % dd(dist),
                   ["%s cm" % dd(x) for x in (D(d) * n, D(d) * PI, dist / 2)], "%d × 3.14 × %d = <b>%s cm</b>" % (d, n, dd(dist)))
    if k == "track":
        r = R.randint(3, 20)
        c = D(2 * r) * PI
        return mcq("반지름이 %d m인 원 모양 연못의 둘레를 한 바퀴 돌았어요. 몇 m를 걸었나요? (원주율: 3.14)" % r, "%s m" % dd(c),
                   ["%s m" % dd(x) for x in (D(r) * PI, D(r) * D(r) * PI, c * 2)], "%d × 2 × 3.14 = <b>%s m</b>" % (r, dd(c)))
    d = R.randint(4, 20) * 2
    c = D(d) * PI / 2 + d
    return mcq("지름이 %d cm인 반원의 둘레는 몇 cm인가요? (원주율: 3.14)" % d, "%s cm" % dd(c), ["%s cm" % dd(x) for x in (D(d) * PI / 2, D(d) * PI, D(d) * PI + d)],
               "곡선 부분 %d × 3.14 ÷ 2 = %s cm에 지름 %d cm를 더해요. <b>%s cm</b>" % (d, dd(D(d) * PI / 2), d, dd(c)))


# ---------------------------------------------------------------- 원의 넓이
def carea_q():
    k = R.choice(["r", "d"])
    v = R.randint(2, 20)
    r = v if k == "r" else v
    if k == "d" and v % 2:
        return None
    r = v if k == "r" else v // 2
    a = D(r * r) * PI
    u = R.choice(["cm", "m"])
    pic = circle_svg("%d %s" % (v, u), kind=k)
    return mcq(pic + "원의 넓이는 몇 %s²인가요? (원주율: 3.14)" % u, "%s %s²" % (dd(a), u),
               ["%s %s²" % (dd(x), u) for x in (D(2 * r) * PI, D(4 * r * r) * PI if k == "d" else D(r) * PI, D(2 * r * r) * PI)],
               "(원의 넓이) = (반지름) × (반지름) × (원주율) = %d × %d × 3.14 = <b>%s %s²</b>" % (r, r, dd(a), u))


def carea_back():
    r = R.randint(2, 15)
    a = D(r * r) * PI
    u = R.choice(["cm", "m"])
    if R.random() < 0.5:
        return mcq("넓이가 %s %s²인 원의 반지름은 몇 %s인가요? (원주율: 3.14)" % (dd(a), u, u), "%d %s" % (r, u), ["%d %s" % (x, u) for x in (2 * r, r * r, r + 1)],
                   "%s ÷ 3.14 = %d = %d × %d이므로 <b>%d %s</b>" % (dd(a), r * r, r, r, r, u))
    c = D(2 * r) * PI
    return mcq("원주가 %s %s인 원의 넓이는 몇 %s²인가요? (원주율: 3.14)" % (dd(c), u, u), "%s %s²" % (dd(a), u), ["%s %s²" % (dd(x), u) for x in (D(4 * r * r) * PI, c, D(r) * PI)],
               "지름 %s ÷ 3.14 = %d %s, 반지름 %d %s. %d × %d × 3.14 = <b>%s %s²</b>" % (dd(c), 2 * r, u, r, u, r, r, dd(a), u))


def carea_shape():
    k = R.choice(["half", "quarter", "ring", "sq"])
    r = R.randint(2, 12) * 2
    if k == "half":
        a = D(r * r) * PI / 2
        return mcq("반지름이 %d cm인 반원의 넓이는 몇 cm²인가요? (원주율: 3.14)" % r, "%s cm²" % dd(a), ["%s cm²" % dd(x) for x in (D(r * r) * PI, D(r) * PI, a / 2)],
                   "%d × %d × 3.14 ÷ 2 = <b>%s cm²</b>" % (r, r, dd(a)))
    if k == "quarter":
        a = D(r * r) * PI / 4
        return mcq("반지름이 %d cm인 원을 똑같이 4로 나눈 한 조각(사분원)의 넓이는 몇 cm²인가요? (원주율: 3.14)" % r, "%s cm²" % dd(a), ["%s cm²" % dd(x) for x in (D(r * r) * PI / 2, D(r * r) * PI, D(r) * PI / 4)],
                   "%d × %d × 3.14 ÷ 4 = <b>%s cm²</b>" % (r, r, dd(a)))
    if k == "ring":
        r2 = r // 2
        a = D(r * r - r2 * r2) * PI
        return mcq("반지름이 %d cm인 원 안에 중심이 같고 반지름이 %d cm인 원을 뺀 고리 모양의 넓이는 몇 cm²인가요? (원주율: 3.14)" % (r, r2), "%s cm²" % dd(a),
                   ["%s cm²" % dd(x) for x in (D((r - r2) ** 2) * PI, D(r * r) * PI, D(r * r + r2 * r2) * PI)],
                   "(%d × %d − %d × %d) × 3.14 = <b>%s cm²</b>" % (r, r, r2, r2, dd(a)))
    a = D(r * r) - D((r // 2) ** 2) * PI
    return mcq("한 변이 %d cm인 정사각형 안에 꼭 맞게 그린 원을 뺀 나머지 부분의 넓이는 몇 cm²인가요? (원주율: 3.14)" % r, "%s cm²" % dd(a),
               ["%s cm²" % dd(x) for x in (D(r * r) - D(r * r) * PI, D((r // 2) ** 2) * PI, D(r * r) - D(r) * PI)],
               "원의 반지름은 %d cm. %d × %d − %d × %d × 3.14 = <b>%s cm²</b>" % (r // 2, r, r, r // 2, r // 2, dd(a)))


def carea_est():
    r = R.randint(3, 15)
    lo, hi = 2 * r * r, 4 * r * r
    return mcq("반지름이 %d cm인 원의 넓이를 어림했어요. 원 밖의 정사각형 넓이와 원 안의 정사각형 넓이로 나타낸 범위로 알맞은 것은?" % r,
               "%d cm²보다 크고 %d cm²보다 작아요" % (lo, hi), ["%d cm²보다 크고 %d cm²보다 작아요" % (r * r, lo), "%d cm²보다 크고 %d cm²보다 작아요" % (hi, 2 * hi), "%d cm²와 같아요" % hi],
               "원 안의 정사각형은 대각선이 %d cm이므로 %d cm², 원 밖의 정사각형은 한 변이 %d cm이므로 %d cm²예요." % (2 * r, lo, 2 * r, hi))


# ---------------------------------------------------------------- 원기둥, 원뿔, 구
SF = [("원기둥의 두 밑면은 서로 평행하고 합동인 원이에요.", "○"), ("원기둥의 옆면은 굽은 면이에요.", "○"), ("원뿔의 밑면은 2개예요.", "×"),
      ("구는 어느 방향에서 보아도 원 모양이에요.", "○"), ("원뿔에는 꼭짓점이 있어요.", "○"), ("원기둥에는 꼭짓점이 있어요.", "×"),
      ("구의 반지름은 모두 길이가 같아요.", "○"), ("원뿔의 모선은 1개뿐이에요.", "×"), ("원기둥의 전개도에서 옆면은 직사각형이에요.", "○"),
      ("원뿔의 높이는 모선의 길이와 같아요.", "×")]


def solid_fact():
    t, a = R.choice(SF)
    return mcq("다음 문장이 맞으면 ○, 틀리면 ×를 고르세요.<br>「%s」" % t, a, ["×" if a == "○" else "○", "알 수 없어요", "크기에 따라 달라요"],
               "원기둥: 평행하고 합동인 원 2개, 굽은 옆면. 원뿔: 원 밑면 1개, 꼭짓점 1개, 모선은 셀 수 없이 많아요. 구: 중심에서 겉면까지 거리가 모두 같아요.")


def cyl_net():
    r = R.randint(2, 10)
    h = R.randint(3, 15)
    k = R.choice(["w", "h", "area"])
    w = D(2 * r) * PI
    if k == "w":
        return mcq("밑면의 반지름이 %d cm, 높이가 %d cm인 원기둥의 전개도에서 옆면(직사각형)의 가로는 몇 cm인가요? (원주율: 3.14)" % (r, h), "%s cm" % dd(w),
                   ["%s cm" % dd(x) for x in (D(r) * PI, D(h), D(r * r) * PI)], "옆면의 가로는 밑면의 둘레(원주)와 같아요. %d × 2 × 3.14 = <b>%s cm</b>" % (r, dd(w)))
    if k == "h":
        return mcq("밑면의 반지름이 %d cm, 높이가 %d cm인 원기둥의 전개도에서 옆면(직사각형)의 세로는 몇 cm인가요?" % (r, h), "%d cm" % h,
                   ["%d cm" % x for x in (2 * r, r, h + 2 * r)], "옆면의 세로는 원기둥의 높이와 같아요. <b>%d cm</b>" % h)
    a = w * h
    return mcq("밑면의 반지름이 %d cm, 높이가 %d cm인 원기둥의 전개도에서 옆면의 넓이는 몇 cm²인가요? (원주율: 3.14)" % (r, h), "%s cm²" % dd(a),
               ["%s cm²" % dd(x) for x in (D(r) * PI * h, D(r * r) * PI * h, a + D(2 * r * r) * PI)], "(원주) × (높이) = %s × %d = <b>%s cm²</b>" % (dd(w), h, dd(a)))


def solid_compare():
    k = R.choice(["cyl_prism", "cone_pyr", "count"])
    if k == "count":
        nm, part = R.choice([("원기둥", "밑면"), ("원뿔", "밑면"), ("원뿔", "꼭짓점"), ("원기둥", "꼭짓점"), ("구", "중심")])
        v = {("원기둥", "밑면"): "2개", ("원뿔", "밑면"): "1개", ("원뿔", "꼭짓점"): "1개", ("원기둥", "꼭짓점"): "없어요", ("구", "중심"): "1개"}[(nm, part)]
        return mcq("%s의 %s 몇 개인가요?" % (nm, josa(part, "은/는")), v, [x for x in ("1개", "2개", "없어요", "셀 수 없이 많아요") if x != v],
                   "원기둥: 밑면 2개, 꼭짓점 없음. 원뿔: 밑면 1개, 꼭짓점 1개. 구: 중심 1개. <b>%s</b>" % v)
    if k == "cyl_prism":
        return mcq("원기둥과 각기둥의 같은 점은?", "두 밑면이 평행하고 합동이에요", ["옆면이 직사각형이에요", "꼭짓점이 있어요", "밑면이 다각형이에요"],
                   "원기둥과 각기둥은 모두 <b>두 밑면이 평행하고 합동</b>이에요. 원기둥은 꼭짓점이 없고 옆면이 굽은 면이에요.")
    return mcq("원뿔과 각뿔의 같은 점은?", "밑면이 1개이고 뿔의 꼭짓점이 있어요", ["밑면이 다각형이에요", "옆면이 삼각형이에요", "모서리가 있어요"],
               "원뿔과 각뿔은 모두 <b>밑면이 1개이고 뿔의 꼭짓점이 있어요</b>.")


def cone_q():
    k = R.choice(["rot", "dims", "sphere"])
    if k == "rot":
        a, b = R.randint(3, 12), R.randint(3, 12)
        nm = R.choice(["직사각형", "직각삼각형", "반원"])
        res = {"직사각형": "원기둥", "직각삼각형": "원뿔", "반원": "구"}[nm]
        return mcq("%s 모양의 종이를 한 변(지름)을 기준으로 한 바퀴 돌리면 어떤 입체도형이 되나요?" % nm, res, [x for x in ("원기둥", "원뿔", "구", "각기둥") if x != res],
                   "직사각형 → 원기둥, 직각삼각형 → 원뿔, 반원 → 구. <b>%s</b>" % res)
    if k == "dims":
        r, h = R.randint(3, 12), R.randint(4, 16)
        return mcq("가로 %d cm, 세로 %d cm인 직사각형의 세로를 기준으로 한 바퀴 돌려 원기둥을 만들었어요. 원기둥의 밑면의 지름은 몇 cm인가요?" % (r, h), "%d cm" % (2 * r),
                   ["%d cm" % x for x in (r, 2 * h, h)], "가로가 밑면의 반지름이 돼요. %d × 2 = <b>%d cm</b>" % (r, 2 * r))
    r = R.randint(3, 15)
    return mcq("지름이 %d cm인 반원을 지름을 기준으로 한 바퀴 돌려 구를 만들었어요. 구의 반지름은 몇 cm인가요?" % (2 * r), "%d cm" % r,
               ["%d cm" % x for x in (2 * r, 4 * r, r + 1)], "반원의 반지름이 구의 반지름이 돼요. <b>%d cm</b>" % r)


def build(which):
    G = "grade-6"
    if which == "prism":
        return unit(G, "prisms-and-pyramids", 2, "[6수03-05] [6수03-06]",
                    "각기둥과 각뿔을 이해하고, 구성 요소와 성질을 탐구하고 설명할 수 있다. 각기둥의 전개도를 그릴 수 있다.",
                    "각기둥과 각뿔", "각기둥과 각뿔",
                    "초등 6학년 1학기 각기둥과 각뿔 학습지: 면・모서리・꼭짓점의 수, 밑면의 모양으로 이름 짓기, 각기둥과 각뿔의 성질, 각기둥의 전개도까지 100문제와 정답.",
                    "각기둥은 밑면 2개, 각뿔은 밑면 1개", "이름은 밑면의 모양으로 정해요.",
                    ["서로 평행하고 합동인 두 다각형이 있는 입체도형을 <b>각기둥</b>이라고 해요. 옆면은 직사각형이에요.",
                     "밑면이 다각형이고 옆면이 모두 삼각형인 입체도형을 <b>각뿔</b>이라고 해요.",
                     "n각기둥: 면 n + 2, 모서리 n × 3, 꼭짓점 n × 2",
                     "n각뿔: 면 n + 1, 모서리 n × 2, 꼭짓점 n + 1"],
                    [("오각기둥의 모서리의 수", ["밑면의 변 5개 × 3"], "15개")],
                    [("각뿔의 밑면을 2개라고 한다", "각뿔의 밑면은 1개예요."),
                     ("각기둥의 꼭짓점을 n + 2라고 한다", "꼭짓점은 n × 2, 면이 n + 2예요."),
                     ("옆면의 모양으로 이름을 짓는다", "밑면의 모양으로 이름을 지어요.")],
                    [("각기둥과 각뿔은 언제 배우나요?", "초등 6학년 1학기 「각기둥과 각뿔」 단원에서 배워요."),
                     ("직육면체도 각기둥인가요?", "네. 직육면체는 사각기둥이에요.")],
                    [("면, 모서리, 꼭짓점", [(prism_count, 20)]),
                     ("이름 알아보기", [(prism_name, 20)]),
                     ("각기둥과 각뿔의 성질", [(prism_fact, 8), (prism_count, 12)]),
                     ("각기둥의 전개도", [(prism_net, 20)]),
                     ("섞어서 연습", [(prism_name, 10), (prism_net, 10)])], 82602)
    if which == "volume":
        return unit(G, "surface-area-and-volume-of-cuboids", 7, "[6수03-17] [6수03-18] [6수03-19]",
                    "직육면체와 정육면체의 겉넓이를 구하는 방법을 이해하고, 이를 구할 수 있다. 부피 단위 1 cm³, 1 m³를 알며, 그 관계를 이해한다. 직육면체와 정육면체의 부피를 구하는 방법을 이해하고, 이를 구할 수 있다.",
                    "직육면체의 겉넓이와 부피", "겉넓이와 부피",
                    "초등 6학년 1학기 학습지: 직육면체와 정육면체의 겉넓이, 부피, 1 cm³와 1 m³의 관계, 부피로 높이 구하기, 포장지와 수조 문장제까지 100문제와 정답.",
                    "부피 = 가로 × 세로 × 높이", "겉넓이 = (세 면의 넓이의 합) × 2",
                    ["입체도형의 겉면 전체의 넓이를 <b>겉넓이</b>라고 해요. 직육면체는 합동인 면이 2개씩 3쌍이에요.",
                     "한 모서리가 1 cm인 정육면체의 부피가 <b>1 cm³</b>예요.",
                     "직육면체의 부피 = (가로) × (세로) × (높이), 정육면체의 부피 = (한 모서리)³",
                     "1 m³ = 100 cm × 100 cm × 100 cm = 1,000,000 cm³"],
                    [("가로 5 cm, 세로 4 cm, 높이 3 cm인 직육면체", ["겉넓이 (20 + 12 + 15) × 2 = 94", "부피 5 × 4 × 3 = 60"], "94 cm², 60 cm³")],
                    [("겉넓이에서 × 2를 빠뜨린다", "마주 보는 면까지 6개의 면을 모두 더해요."),
                     ("1 m³ = 100 cm³라고 한다", "세 방향 모두 100배라서 1000000배예요."),
                     ("단위를 맞추지 않고 곱한다", "cm와 m를 섞어 쓰지 않아요.")],
                    [("겉넓이와 부피는 언제 배우나요?", "2022 개정 교육과정에서는 초등 6학년에서 배워요."),
                     ("들이와 부피의 관계는?", "1 L = 1000 cm³, 1 mL = 1 cm³예요.")],
                    [("직육면체의 겉넓이", [(sa_q, 20)]),
                     ("직육면체의 부피", [(vol_q, 20)]),
                     ("부피의 단위", [(vol_unit, 20)]),
                     ("모르는 길이 구하기", [(vol_back, 20)]),
                     ("문장제", [(vol_story, 20)])], 82607)
    if which == "cubes":
        return unit(G, "stacking-cubes-and-views", 10, "[6수03-09] [6수03-10]",
                    "쌓기나무로 만든 입체도형을 보고 사용된 쌓기나무의 개수를 구할 수 있다. 쌓기나무로 만든 입체도형의 위, 앞, 옆에서 본 모양을 표현할 수 있고, 이러한 표현을 보고 입체도형의 모양을 추측할 수 있다.",
                    "쌓기나무와 위, 앞, 옆에서 본 모양", "공간과 입체",
                    "초등 6학년 2학기 공간과 입체 학습지: 위에서 본 모양에 수를 써서 쌓기나무의 개수 구하기, 앞・옆・위에서 본 모양 고르기, 층별 개수, 직육면체 만들기까지 100문제와 정답.",
                    "위에서 본 모양에 수를 쓰면 개수가 보여요", "앞・옆에서는 각 줄에서 가장 높은 층만큼 보여요.",
                    ["위에서 본 모양의 각 칸에 쌓은 쌓기나무의 개수를 쓰면 전체 개수를 정확하게 알 수 있어요.",
                     "앞에서 본 모양은 왼쪽부터 각 줄에서 <b>가장 높이 쌓은 개수</b>만큼 그려요. 옆에서 본 모양도 같아요.",
                     "층별로 나누어 그리면 각 층의 개수를 알 수 있어요."],
                    [("위에서 본 모양 3, 1, 2, 1인 쌓기나무", ["3 + 1 + 2 + 1"], "7개")],
                    [("보이는 면의 수를 센다", "쌓기나무의 개수를 세요."),
                     ("앞에서 본 모양을 위에서 본 모양으로 착각한다", "앞에서 보면 높이(층)가 보여요."),
                     ("뒤에 숨은 쌓기나무를 빼먹는다", "위에서 본 모양에 수를 써서 확인해요.")],
                    [("이 단원은 언제 배우나요?", "초등 6학년 2학기 「공간과 입체」 단원에서 배워요."),
                     ("중학교에서는 어떻게 이어지나요?", "입체도형의 겨냥도와 투영도로 이어져요.")],
                    [("쌓기나무의 개수", [(cube_count, 20)]),
                     ("앞, 옆, 위에서 본 모양", [(view_q, 20)]),
                     ("층별로 알아보기", [(layer_q, 20)]),
                     ("더 필요한 쌓기나무", [(cube_need, 10), (cube_count, 10)]),
                     ("섞어서 연습", [(view_q, 10), (layer_q, 10)])], 82610)
    if which == "circum":
        return unit(G, "circumference-and-pi", 13, "[6수03-15] [6수03-16]",
                    "여러 가지 원 모양 물체의 원주와 지름을 측정하는 활동을 통하여, 원주율이 일정한 값임을 알고 그 근삿값을 사용할 수 있다. 원주와 원의 넓이를 구하는 방법을 이해하고, 이를 구할 수 있다.",
                    "원주와 원주율", "원주와 원주율",
                    "초등 6학년 2학기 원주 학습지: 원주율의 뜻, 지름과 반지름으로 원주 구하기, 원주로 지름과 반지름 구하기, 바퀴와 반원의 둘레 문장제까지 100문제와 정답.",
                    "원주 = 지름 × 원주율", "원주율은 약 3.14로 일정해요.",
                    ["원의 둘레를 <b>원주</b>라고 해요.",
                     "원의 크기와 상관없이 (원주) ÷ (지름)은 일정해요. 이 값을 <b>원주율</b>이라고 하고, 3.14를 많이 써요.",
                     "(원주) = (지름) × (원주율) = (반지름) × 2 × (원주율)",
                     "(지름) = (원주) ÷ (원주율)"],
                    [("반지름이 5 cm인 원의 원주", ["5 × 2 × 3.14"], "31.4 cm")],
                    [("반지름에 원주율을 바로 곱한다", "지름(반지름 × 2)에 곱해요."),
                     ("원이 크면 원주율도 크다고 생각한다", "원주율은 항상 같아요."),
                     ("반원의 둘레에 지름을 빼먹는다", "곡선 부분 + 지름이에요.")],
                    [("원주율은 왜 3.14인가요?", "원주율은 3.1415926…로 끝없이 이어지는 수라서 근삿값 3.14를 써요."),
                     ("원주는 언제 배우나요?", "초등 6학년 2학기 「원의 넓이」 단원에서 배워요.")],
                    [("원주율", [(ratio_pi, 15), (pi_fact, 5)]),
                     ("원주 구하기", [(circum_q, 20)]),
                     ("지름과 반지름 구하기", [(circum_back, 20)]),
                     ("섞어서 연습", [(circum_q, 10), (circum_back, 10)]),
                     ("문장제", [(circum_story, 20)])], 82613)
    if which == "carea":
        return unit(G, "area-of-circles", 14, "[6수03-16]",
                    "원주와 원의 넓이를 구하는 방법을 이해하고, 이를 구할 수 있다.",
                    "원의 넓이", "원의 넓이",
                    "초등 6학년 2학기 원의 넓이 학습지: 원의 넓이 어림하기, 반지름과 지름으로 넓이 구하기, 넓이와 원주로 반지름 구하기, 반원・고리・색칠한 부분의 넓이까지 100문제와 정답.",
                    "원의 넓이 = 반지름 × 반지름 × 원주율", "원을 잘라 붙이면 직사각형에 가까워져요.",
                    ["원을 잘게 잘라 이어 붙이면 가로가 (원주) ÷ 2, 세로가 반지름인 직사각형에 가까워져요.",
                     "그래서 (원의 넓이) = (반지름) × (반지름) × (원주율)이에요.",
                     "지름이 주어지면 먼저 반지름을 구해요.",
                     "색칠한 부분은 큰 도형에서 작은 도형을 빼서 구해요."],
                    [("지름이 10 cm인 원의 넓이", ["반지름 5 cm", "5 × 5 × 3.14 = 78.5"], "78.5 cm²")],
                    [("지름 × 지름 × 원주율로 계산한다", "반지름 × 반지름이에요."),
                     ("반지름 × 2 × 원주율을 넓이라고 한다", "그것은 원주예요."),
                     ("반원의 넓이를 원의 넓이로 답한다", "반원은 원의 넓이 ÷ 2예요.")],
                    [("원의 넓이는 언제 배우나요?", "초등 6학년 2학기 「원의 넓이」 단원에서 배워요."),
                     ("원주와 원의 넓이를 헷갈리지 않으려면?", "원주는 길이(cm), 넓이는 cm²예요. 넓이는 반지름을 두 번 곱해요.")],
                    [("원의 넓이 어림하기", [(carea_est, 10), (carea_q, 10)]),
                     ("원의 넓이 구하기", [(carea_q, 16), (carea_back, 4)]),
                     ("반지름 구하기", [(carea_back, 20)]),
                     ("여러 가지 모양의 넓이", [(carea_shape, 20)]),
                     ("섞어서 연습", [(carea_shape, 10), (carea_back, 10)])], 82614)
    return unit(G, "cylinders-cones-and-spheres", 15, "[6수03-07] [6수03-08]",
                "원기둥, 원뿔, 구를 이해하고, 구성 요소와 성질을 탐구하고 설명할 수 있다. 원기둥의 전개도를 그릴 수 있다.",
                "원기둥, 원뿔, 구", "원기둥, 원뿔, 구",
                "초등 6학년 2학기 학습지: 원기둥・원뿔・구의 구성 요소와 성질, 원기둥의 전개도에서 옆면의 가로와 세로, 평면도형을 돌려 만든 입체도형까지 100문제와 정답.",
                "원기둥 옆면의 가로 = 밑면의 둘레", "직사각형・직각삼각형・반원을 돌리면 원기둥・원뿔・구",
                ["<b>원기둥</b>: 평행하고 합동인 두 원(밑면)과 굽은 옆면. 두 밑면 사이의 거리가 높이예요.",
                 "<b>원뿔</b>: 원 모양 밑면 1개와 굽은 옆면, 원뿔의 꼭짓점. 꼭짓점과 밑면의 둘레를 이은 선분이 모선이에요.",
                 "<b>구</b>: 공 모양. 중심에서 겉면까지의 거리(반지름)가 모두 같아요.",
                 "원기둥의 전개도에서 옆면은 직사각형이고, 가로는 밑면의 둘레, 세로는 높이와 같아요."],
                [("반지름 3 cm, 높이 10 cm인 원기둥의 전개도에서 옆면의 가로", ["밑면의 둘레 3 × 2 × 3.14"], "18.84 cm")],
                [("원기둥에 꼭짓점이 있다고 한다", "원기둥에는 꼭짓점이 없어요."),
                 ("원뿔의 높이와 모선을 같다고 한다", "높이는 꼭짓점에서 밑면에 수직인 선분이에요. 모선이 더 길어요."),
                 ("옆면의 가로를 밑면의 지름으로 쓴다", "밑면의 둘레(원주)와 같아요.")],
                [("원기둥, 원뿔, 구는 언제 배우나요?", "초등 6학년 2학기 「원기둥, 원뿔, 구」 단원에서 배워요."),
                 ("원기둥의 부피도 배우나요?", "원기둥의 겉넓이와 부피는 중학교에서 배워요.")],
                [("원기둥, 원뿔, 구의 성질", [(solid_fact, 7), (solid_compare, 6), (cone_q, 7)]),
                 ("원기둥의 전개도", [(cyl_net, 20)]),
                 ("돌려서 만든 입체도형", [(cone_q, 20)]),
                 ("섞어서 연습", [(cyl_net, 10), (cone_q, 10)]),
                 ("성질 비교하기", [(solid_fact, 3), (cyl_net, 12), (cone_q, 5)])], 82615)
