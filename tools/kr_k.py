# -*- coding: utf-8 -*-
"""
대한민국 유치원（만 5세、2019 개정 누리과정 자연탐구「생활 속에서 탐구하기」）の 12 単元。
・10까지（数えるのは 20까지）。とても短い文、ほぼ全問に絵
・初等 1・2학년の問題関数（kr_g1_num・kr_g1_calc・kr_g1_geo・kr_g2_data）は、モジュールの R を
  新しい seed に入れ替えて再利用する（同じ問題にならない）
・위치와 방향・똑같이 나누기・모양/몸짓의 규칙・두 줄 비교は自前
誤答は「하나 더 세거나 빠뜨린다」「왼쪽과 오른쪽을 바꾼다」「위에서와 아래에서를 헷갈린다」
「똑같지 않게 나눈다」「반복되는 부분을 짧게 본다」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa
from kr_low import KINDS, LET, ORD, nm, cw, cnt, ko, row, tenframe, near, kinds_row
import k_pics as K
from f_common import pattern_svg
from ws_common import svg_wrap, text, GREEN, INK

import kr_g1_num as N1
import kr_g1_calc as C1
import kr_g1_geo as G1
import kr_g2_data as D2

G = "kindergarten"
STD = "누리과정 자연탐구: 생활 속에서 탐구하기"
R = random.Random(82001)
NM = Names(R)
TH = [("사탕", "개"), ("구슬", "개"), ("연필", "자루"), ("색종이", "장"), ("풍선", "개"), ("딸기", "개"),
      ("쿠키", "개"), ("귤", "개"), ("딱지", "장"), ("블록", "개"), ("스티커", "장"), ("떡", "개")]


def reseed(s):
    """他学年のモジュールの乱数を入れ替える"""
    global R, NM
    R = random.Random(s)
    NM = Names(R)
    for m, k in ((N1, 1), (C1, 2), (G1, 3), (D2, 4)):
        m.R = random.Random(s * 10 + k)
        m.NM = Names(m.R)
        m.NM.pool = [x for x in m.NM.pool if x != "하나"]      # 수 '하나'와 헷갈리지 않게
    NM.pool = [x for x in NM.pool if x != "하나"]


def le(mk, n):
    """答え・選択肢に n より大きい数があれば捨てる"""
    import re

    def f():
        it = mk()
        if it is None:
            return None
        txt = " ".join(it["c"]) + " " + re.sub(r"<svg.*?</svg>", "", it["q"])
        if any(int(x) > n for x in re.findall(r"\d+", txt)):
            return None
        return it
    return f


# ------------------------------------------------------------------ 수 세기
TF = ["dot", "apple", "star", "flower", "ball"]


def tf_count():
    def mk():
        n, k = R.randint(1, 10), R.choice(TF)
        u = "개" if k != "flower" else "송이"
        return mcq("10칸 상자에 몇 %s 있을까요?%s" % (u, tenframe(n, 1, k)), "%d%s" % (n, u),
                   ["%d%s" % x for x in [(v, u) for v in near(n, 0, 10) + [10 - n]]],
                   "한 줄에 5칸씩 있어요. %s <b>%d%s</b>예요." % ("5칸과 %d칸을 더하면" % (n - 5) if n > 5 else "하나씩 세면", n, u))
    return mk


# ------------------------------------------------------------------ 많고 적음
def cmp_rows():
    def mk():
        vs = R.sample(range(1, 11), 3)
        same = R.random() < 0.5
        ks = [R.choice(KINDS)] * 3 if same else R.sample(KINDS, 3)
        big = R.random() < 0.6
        i = vs.index(max(vs) if big else min(vs))
        pic = ko(K.match_svg([(v, k, "ABC"[j], 30) for j, (v, k) in enumerate(zip(vs, ks))], 34), "세 줄의 물건")
        return mcq("가장 %s 줄은 어느 것일까요?%s" % ("많은" if big else "적은", pic), "%s 줄" % LET[i],
                   ["%s 줄" % LET[j] for j in range(3) if j != i] + ["모두 같아요"],
                   "하나씩 세면 가 %d, 나 %d, 다 %d예요. 가장 %s 것은 <b>%s 줄</b>이에요." % (vs[0], vs[1], vs[2], "많은" if big else "적은", LET[i]))
    return mk


def cmp_equal():
    def mk():
        a = R.randint(3, 9)
        others = R.sample([x for x in range(2, 11) if x != a], 2)
        vs = [a, a] + others
        R.shuffle(vs)
        ks = R.sample(KINDS, 4)
        pic = ko(K.lettered_groups_svg(list(zip(vs, ks))), "네 묶음의 물건")
        pr = [i for i in range(4) if vs[i] == a]
        ok = "%s와 %s" % (LET[pr[0]], LET[pr[1]])
        bad = ["%s와 %s" % (LET[i], LET[j]) for i in range(4) for j in range(i + 1, 4) if [i, j] != pr]
        R.shuffle(bad)
        return mcq("수가 같은 두 묶음은 어느 것일까요?%s" % pic, ok, bad,
                   "세어 보면 가 %d, 나 %d, 다 %d, 라 %d예요. 수가 같은 것은 <b>%s</b>예요." % (vs[0], vs[1], vs[2], vs[3], ok))
    return mk


# ------------------------------------------------------------------ 순서
def ord_word():
    pool = [(p, d) for p in range(1, 10) for d in (1,)] + [(p, -1) for p in range(2, 11)]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        p, d = pool.pop()
        a = p + d
        return mcq("<b>%s</b> 바로 %s 순서는 무엇일까요?" % (ORD[p], "다음" if d > 0 else "앞"), ORD[a],
                   [ORD[x] for x in (p - d, p, a + d, a + 2 * d) if 1 <= x <= 10 and x != a],
                   "첫째, 둘째, 셋째… 순서대로 말해 보면 %s 바로 %s은 <b>%s</b>예요." % (ORD[p], "다음" if d > 0 else "앞", ORD[a]))
    return mk


def ord_race():
    def mk():
        n = NM.next()
        p = R.randint(2, 10)
        how = R.choice(["before", "place"])
        if how == "before":
            return mcq("달리기에서 %s %s로 들어왔어요. %s보다 먼저 들어온 친구는 몇 명일까요?" % (josa(n, "이/가"), ORD[p], n), "%d명" % (p - 1),
                       ["%d명" % x for x in (p, p + 1, p - 2 if p > 2 else 10 - p)],
                       "%s 앞에 첫째부터 %s까지 들어왔어요. <b>%d명</b>이에요." % (ORD[p], ORD[p - 1], p - 1))
        return mcq("달리기에서 %s보다 먼저 들어온 친구가 %d명이에요. %s 몇째로 들어왔을까요?" % (n, p - 1, josa(n, "은/는")), ORD[p],
                   [ORD[x] for x in (p - 1, p + 1, p + 2 if p < 9 else p - 2) if 1 <= x <= 10],
                   "먼저 들어온 친구 %d명 다음이니까 <b>%s</b>예요." % (p - 1, ORD[p]))
    return mk


# ------------------------------------------------------------------ 위치와 방향
def pos_table():
    W = {"above": "위", "below": "아래", "beside": "옆", "beside-left": "옆"}

    def mk():
        k = R.choice(KINDS)
        rel = R.choice(list(W))
        pic = ko(K.table_scene_svg(k, rel), "책상과 %s" % nm(k))
        ok = "책상 %s" % W[rel]
        return mcq("%s 어디에 있을까요?%s" % (josa(nm(k), "은/는"), pic), ok,
                   ["책상 %s" % w for w in ("위", "아래", "옆", "안") if w != W[rel]],
                   "%s 책상의 <b>%s</b>에 있어요." % (josa(nm(k), "은/는"), W[rel]))
    return mk


def pos_box():
    W = {"front": "앞", "behind": "뒤", "beside": "옆", "above": "위"}

    def mk():
        k = R.choice(KINDS)
        rel = R.choice(list(W))
        pic = ko(K.box_scene_svg(k, rel), "상자와 %s" % nm(k))
        ok = "상자 %s" % W[rel]
        tip = {"front": "상자보다 가까이 있고 다 보여요.", "behind": "상자에 가려서 조금만 보여요.",
               "beside": "상자와 나란히 바닥에 있어요.", "above": "상자보다 높은 곳에 있어요."}[rel]
        return mcq("%s 상자의 어디에 있을까요?%s" % (josa(nm(k), "은/는"), pic), ok,
                   ["상자 %s" % w for w in ("앞", "뒤", "옆", "위") if w != W[rel]],
                   "%s <b>상자 %s</b>에 있어요." % (tip, W[rel]))
    return mk


def pos_shelf(kinds=("top", "bottom", "ord", "near")):
    def mk():
        L = R.randint(4, 5)
        ks = R.sample(KINDS, L)
        pic = ko(K.shelf_svg(ks), "%d칸 선반" % L)
        how = R.choice(kinds)
        if how == "top":
            up = R.random() < 0.5
            a = ks[0] if up else ks[-1]
            q = "선반의 맨 %s 칸에 있는 것은 무엇일까요?" % ("위" if up else "아래")
            e = "맨 %s 칸을 보면 <b>%s</b>예요." % ("위" if up else "아래", nm(a))
            w = [nm(ks[-1] if up else ks[0]), nm(ks[1] if up else ks[-2]), nm(ks[2])]
        elif how == "ord":
            up = R.random() < 0.5
            p = R.randint(2, L - 1)
            a = ks[p - 1] if up else ks[L - p]
            q = "%s에서 <b>%s</b> 칸에 있는 것은 무엇일까요?" % ("위" if up else "아래", ORD[p])
            e = "%s에서부터 첫째, 둘째… 하고 세면 %s 칸은 <b>%s</b>예요." % ("위" if up else "아래", ORD[p], nm(a))
            w = [nm(ks[L - p] if up else ks[p - 1]), nm(ks[p] if up else ks[L - p - 1]), nm(ks[p - 2] if up else ks[L - p + 1])]
        else:
            i = R.randint(1, L - 2)
            up = R.random() < 0.5
            a = ks[i - 1] if up else ks[i + 1]
            q = "%s의 바로 %s 칸에 있는 것은 무엇일까요?" % (nm(ks[i]), "위" if up else "아래")
            e = "%s 칸에서 한 칸 %s 올라가면 <b>%s</b>예요." % (nm(ks[i]), "위로" if up else "아래로", nm(a))
            e = e.replace("아래로 올라가면", "아래로 내려가면")
            w = [nm(ks[i + 1] if up else ks[i - 1]), nm(ks[i]), nm(ks[(i + 2) % L])]
        return mcq(q + pic, nm(a), w + [nm(k) for k in ks], e)
    return mk


def pos_lr():
    def mk():
        ks = R.sample(KINDS, 5)
        pic = kinds_row(ks)
        how = R.choice(["right", "left", "between", "end"])
        if how in ("right", "left"):
            i = R.randint(1, 3)
            j = i + 1 if how == "right" else i - 1
            a = ks[j]
            q = "%s 바로 %s에 있는 것은 무엇일까요?" % (nm(ks[i]) + "의", "오른쪽" if how == "right" else "왼쪽")
            w = [nm(ks[i - 1] if how == "right" else ks[i + 1]), nm(ks[i])]
            e = "%s에서 %s 손 쪽으로 하나 가면 <b>%s</b>예요." % (nm(ks[i]), "오른" if how == "right" else "왼", nm(a))
        elif how == "between":
            i = R.randint(0, 2)
            a = ks[i + 1]
            q = "%s %s 사이에 있는 것은 무엇일까요?" % (josa(nm(ks[i]), "과/와"), nm(ks[i + 2]))
            w = [nm(ks[i]), nm(ks[i + 2]), nm(ks[(i + 3) % 5])]
            e = "%s %s 가운데에 <b>%s</b>가 있어요." % (josa(nm(ks[i]), "과/와"), nm(ks[i + 2]), nm(a))
            e = e.replace("<b>%s</b>가" % nm(a), josa("<b>%s</b>" % nm(a), "이/가"))
        else:
            left = R.random() < 0.5
            a = ks[0] if left else ks[-1]
            q = "맨 %s에 있는 것은 무엇일까요?" % ("왼쪽" if left else "오른쪽")
            w = [nm(ks[-1] if left else ks[0]), nm(ks[1] if left else ks[-2]), nm(ks[2])]
            e = "%s 손 쪽 끝에 있는 것은 <b>%s</b>예요." % ("왼" if left else "오른", nm(a))
        return mcq(q + pic, nm(a), w + [nm(k) for k in ks], e)
    return mk


def grid_svg(ks):
    sp = 62
    s = []
    for r in range(4):
        s.append("<line x1='8' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (8 + r * sp, 8 + 3 * sp, 8 + r * sp, GREEN))
        s.append("<line x1='%d' y1='8' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (8 + r * sp, 8 + r * sp, 8 + 3 * sp, GREEN))
    for i, k in enumerate(ks):
        s.append(K.obj(k, 8 + sp / 2 + (i % 3) * sp, 8 + sp / 2 + (i // 3) * sp, 18))
    return ko(svg_wrap(16 + 3 * sp, 16 + 3 * sp, "".join(s), "x"), "9칸에 놓인 물건")


def pos_grid():
    D = {"위": (-1, 0), "아래": (1, 0), "왼쪽": (0, -1), "오른쪽": (0, 1)}

    def mk():
        ks = R.sample(KINDS, 9)
        r, c = R.randint(0, 2), R.randint(0, 2)
        dirs = [d for d, (dr, dc) in D.items() if 0 <= r + dr <= 2 and 0 <= c + dc <= 2]
        d = R.choice(dirs)
        dr, dc = D[d]
        a = ks[(r + dr) * 3 + c + dc]
        w = [nm(ks[(r + D[x][0]) * 3 + c + D[x][1]]) for x in dirs if x != d] + [nm(ks[r * 3 + c])]
        return mcq("%s 바로 %s에 있는 것은 무엇일까요?%s" % (nm(ks[r * 3 + c]) + "의", d, grid_svg(ks)), nm(a), w + [nm(k) for k in ks],
                   "%s 칸에서 %s 한 칸 가면 <b>%s</b>예요." % (nm(ks[r * 3 + c]), josa(d, "으로/로"), nm(a)))
    return mk


def pos_words():
    P = [("위", "아래"), ("아래", "위"), ("앞", "뒤"), ("뒤", "앞"), ("왼쪽", "오른쪽"), ("오른쪽", "왼쪽"), ("안", "밖"), ("밖", "안")]
    pool = P[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        a, b = pool.pop()
        return mcq("%s 반대되는 쪽은 어디일까요?" % josa("<b>%s</b>" % a, "과/와"), b,
                   [x for x in ("위", "아래", "앞", "뒤", "왼쪽", "오른쪽", "안", "밖") if x not in (a, b)][:5],
                   "%s의 반대는 <b>%s</b>예요." % (a, b))
    return mk


# ------------------------------------------------------------------ 똑같이 나누기
def th():
    return R.choice(TH)


def share_fair():
    def mk():
        t, c = th()
        g = R.choice([2, 2, 3])
        n = R.choice([x for x in range(2 * g, 11) if x % g == 0])
        q = n // g
        if g == 2:
            ok = "%d%s와 %d%s" % (q, c, q, c)
            w = ["%d%s와 %d%s" % (q - d, c, q + d, c) for d in (1, 2, 3) if q - d >= 0]
            w.append("%d%s와 %d%s" % (q + 1, c, q + 1, c))
        else:
            ok = "%d%s, %d%s, %d%s" % (q, c, q, c, q, c)
            w = ["%d%s, %d%s, %d%s" % (q - 1, c, q, c, q + 1, c), "%d%s, %d%s, %d%s" % (q + 1, c, q + 1, c, q - 2, c) if q >= 2 else None,
                 "%d%s, %d%s, %d%s" % (q, c, q, c, q + 1, c), "%d%s, %d%s, %d%s" % (q - 1, c, q - 1, c, q + 2, c)]
        names = [NM.next() for _ in range(g)]
        return mcq("%s %d%s를 %s 똑같이 나누었어요. 바르게 나눈 것은 무엇일까요?" % (t, n, c, josa(josa(names[0], "과/와") + " " + names[1], "이/가") if g == 2 else ", ".join(names) + " 세 명이"),
                   ok, w, "똑같이 나누면 한 명이 가진 수가 모두 같아요. <b>%s</b>" % ok)
    return mk


def share_eq():
    def mk():
        t, c = th()
        k = R.choice(KINDS)
        g = R.choice([2, 2, 3, 4, 5])
        n = R.choice([x for x in range(2 * g, 11) if x % g == 0])
        q = n // g
        return mcq("%s %d%s를 친구 %d명이 똑같이 나누어 가지면, 한 명이 몇 %s씩 가질까요?%s" % (nm(k), n, cw(k), g, cw(k), row(n, k)),
                   "%d%s" % (q, cw(k)), ["%d%s" % (x, cw(k)) for x in (q + 1, q - 1, g, n - g, n) if x > 0 and x != q],
                   "한 명에게 하나씩 차례로 나누어 주면 %d%s씩 돌아가요. <b>%d%s</b>" % (q, cw(k), q, cw(k)))
    return mk


def share_group():
    def mk():
        k = R.choice(KINDS)
        g = R.choice([2, 2, 3, 5])
        n = R.choice([x for x in range(2 * g, 11) if x % g == 0])
        q = n // g
        return mcq("%s %d%s를 %d%s씩 묶으면 몇 묶음이 될까요?%s" % (nm(k), n, cw(k), g, cw(k), row(n, k)), "%d묶음" % q,
                   ["%d묶음" % x for x in (q + 1, q - 1, g, n) if x > 0 and x != q],
                   "%d%s씩 동그라미로 묶어 보면 <b>%d묶음</b>이에요." % (g, cw(k), q))
    return mk


def share_plate():
    def mk():
        k = R.choice(KINDS)
        g = R.randint(2, 4)
        q = R.randint(1, 10 // g)
        if q * g < 4:
            return None
        pic = ko(K.groups_svg([(q, k)] * g, 26), "%d묶음에 똑같이 나눈 %s" % (g, nm(k)))
        if R.random() < 0.5:
            return mcq("%s 접시 %d개에 똑같이 나누었어요. 한 접시에 몇 %s씩 있을까요?%s" % (josa(nm(k), "을/를"), g, cw(k), pic), "%d%s" % (q, cw(k)),
                       ["%d%s" % (x, cw(k)) for x in (q * g, g, q + 1, q - 1) if x > 0 and x != q],
                       "한 묶음만 세면 <b>%d%s</b>예요." % (q, cw(k)))
        return mcq("똑같이 %d%s씩 %d묶음이 있어요. 모두 몇 %s일까요?%s" % (q, cw(k), g, cw(k), pic), "%d%s" % (q * g, cw(k)),
                   ["%d%s" % (x, cw(k)) for x in (q * g + 1, q * g - 1, q + g, q) if x > 0 and x != q * g],
                   "%s 모두 세면 <b>%d%s</b>예요." % (" + ".join([str(q)] * g) + "처럼", q * g, cw(k)))
    return mk


def share_story():
    def mk():
        t, c = th()
        n = NM.next()
        g = R.randint(2, 5)
        q = R.randint(1, 10 // g)
        if q * g < 4:
            return None
        if R.random() < 0.5:
            return mcq("%s 친구 %d명에게 %s %d%s씩 주려고 해요. %s 모두 몇 %s 있어야 할까요?" % (josa(n, "은/는"), g, t, q, c, josa(t, "이/가"), c),
                       "%d%s" % (q * g, c), ["%d%s" % (x, c) for x in (q + g, q * g + 1, q * g - 1, g) if x > 0 and x != q * g],
                       "%d명에게 %d%s씩: %s = <b>%d%s</b>" % (g, q, c, " + ".join([str(q)] * g), q * g, c))
        return mcq("%s %s %d%s를 친구 %d명에게 똑같이 나누어 주었어요. 한 명이 몇 %s씩 받았을까요?" % (josa(n, "은/는"), t, q * g, c, g, c),
                   "%d%s" % (q, c), ["%d%s" % (x, c) for x in (g, q + 1, q - 1, q * g - g) if x > 0 and x != q],
                   "하나씩 차례로 나누어 주면 한 명이 <b>%d%s</b>씩 받아요." % (q, c))
    return mk


# ------------------------------------------------------------------ 규칙
PATS = ["AB", "AAB", "ABB", "ABC", "AABB"]
SH = {"circle": "동그라미", "triangle": "세모", "square": "네모"}


def pat_shape():
    def mk():
        p = R.choice(PATS)
        ss = R.sample(list(SH), len(set(p)))
        mp = {ch: ss[i] for i, ch in enumerate(sorted(set(p)))}
        col = R.choice(["red", "blue", "yellow", "green"])
        L = len(p) * 2 + R.randint(0, len(p) - 1)
        seq = [mp[p[i % len(p)]] for i in range(L + 1)]
        ans = seq[-1]
        pic = ko(pattern_svg([("shape", s, col) for s in seq[:-1]], 1), "규칙에 따라 놓은 모양")
        return mcq("규칙에 따라 모양을 놓았어요. ?에 알맞은 모양은 무엇일까요?%s" % pic, SH[ans], [SH[s] for s in SH if s != ans] + ["별"],
                   "%s 반복돼요. <b>%s</b>" % (josa(", ".join(SH[mp[ch]] for ch in p), "이/가"), SH[ans]))
    return mk


def pat_mid():
    def mk():
        p = R.choice(PATS)
        ks = R.sample(KINDS, len(set(p)))
        mp = {ch: ks[i] for i, ch in enumerate(sorted(set(p)))}
        L = len(p) * 3
        seq = [mp[p[i % len(p)]] for i in range(L)]
        b = R.randint(len(p), L - 2)
        ans = seq[b]
        items = [("obj", k) if i != b else ("blank",) for i, k in enumerate(seq)]
        pic = ko(pattern_svg(items, 0), "규칙에 따라 놓은 물건, 가운데가 비어 있어요")
        return mcq("규칙에 따라 놓았어요. 빈칸 ?에 알맞은 것은 무엇일까요?%s" % pic, nm(ans), [nm(k) for k in ks if k != ans] + [nm(k) for k in KINDS if k not in ks][:2],
                   "%s 되풀이돼요. 빈칸에는 <b>%s</b>가 들어가요." % (josa(", ".join(nm(mp[c]) for c in p), "이/가"), nm(ans)))
    return mk


BODY = [("짝", "손뼉"), ("쿵", "발 구르기"), ("야호", "만세")]


def pat_body():
    def mk():
        p = R.choice(["AB", "AAB", "ABB", "ABC", "AABB", "ABCC"])
        ws = R.sample(["짝", "쿵", "야호", "콩", "똑"], len(set(p)))
        mp = {ch: ws[i] for i, ch in enumerate(sorted(set(p)))}
        L = len(p) * 2 + R.randint(0, len(p) - 1)
        seq = [mp[p[i % len(p)]] for i in range(L + 1)]
        ans = seq[-1]
        return mcq("규칙에 따라 소리를 내요. 다음에 올 소리는 무엇일까요?<br><b>%s, ?</b>" % ", ".join(seq[:-1]), ans,
                   [w for w in ["짝", "쿵", "야호", "콩", "똑"] if w != ans],
                   "%s 되풀이돼요. 다음은 <b>%s</b>예요." % (josa("'" + ", ".join(mp[c] for c in p) + "'", "이/가"), ans))
    return mk


# ------------------------------------------------------------------ 단원
def L(lo, hi):
    return lambda mk: le(mk, hi)


def build(which):
    U = UNITS[which]
    reseed(U["seed"])
    return unit(G, which, U["sort"], STD, U["std"], U["title"], U["short"], U["meta"], U["kb"], U["ks"],
                U["think"], U["ex"], U["mist"], U["faq"], U["spec"](), U["seed"], domain=U["dom"])


UNITS = {}


def defunit(slug, **kw):
    UNITS[slug] = kw


NUM = "수 세기와 셈"
GEO = "위치와 모양"
CMP = "길이와 무게 비교"
PAT = "규칙 찾기"
SORT = "분류하기"
S_CNT = "물체를 세어 수량을 알아본다."

defunit("counting-to-10", sort=1, seed=82001, dom=NUM, std=S_CNT,
        title="10까지의 수 세기", short="10까지 세기",
        meta="유치원(만 5세) 10까지의 수 학습지: 그림을 보고 수 세기, 10칸 상자, 수 읽기(다섯·오), 하나 큰 수와 하나 작은 수, 0, 많고 적음까지 그림이 있는 100문제와 정답.",
        kb="하나씩 짚으며 빠짐없이 세요", ks="마지막에 센 수가 모두의 수예요. 아무것도 없으면 0이에요.",
        think=["물건을 셀 때는 하나씩 손가락으로 짚으면서 세요. 센 것에는 표시를 하면 두 번 세지 않아요.",
               "마지막에 말한 수가 물건의 수예요. 하나, 둘, 셋, 넷, 다섯 → 모두 <b>5개</b>",
               "수는 두 가지로 읽어요. 5는 <b>다섯</b> 또는 <b>오</b>예요. 개수를 말할 때는 '다섯 개'라고 해요.",
               "아무것도 없을 때는 <b>0</b>(영)이라고 해요."],
        ex=[("별이 몇 개일까요? ★★★★★★", ["하나, 둘, 셋, 넷, 다섯, 여섯 하고 세요."], "6개"),
            ("7보다 하나 큰 수", ["7 다음에 세는 수를 찾아요."], "8")],
        mist=[("같은 것을 두 번 센다", "센 것에 표시를 하며 세요."),
              ("사과 3개를 '사과 삼 개'라고 읽는다", "'사과 세 개'라고 읽어요."),
              ("아무것도 없을 때 1이라고 한다", "하나도 없으면 0이에요.")],
        faq=[("만 5세는 어디까지 세면 되나요?", "누리과정에서는 생활 속 물건을 세어 수량을 알아봐요. 먼저 10까지 정확하게 세고, 익숙해지면 20까지 세어 보세요."),
             ("집에서 어떻게 연습하나요?", "간식, 신발, 계단처럼 눈에 보이는 것을 함께 세어 보세요. 손가락으로 짚으며 세는 습관이 중요해요.")],
        spec=lambda: [("몇 개일까요", [(N1.count_pic(1, 10), 20)]),
                      ("10칸 상자", [(tf_count(), 20)]),
                      ("수 읽기", [(N1.read_both(1, 10), 7), (N1.word_to_num(1, 10), 7), (N1.count_phrase(), 6)]),
                      ("하나 큰 수, 하나 작은 수", [(N1.one_more_less(0, 9), 8), (N1.seq_cards(0, 9), 8), (N1.between(0, 9), 4)]),
                      ("0과 크기 비교", [(N1.zero_q(), 4), (N1.more_than(0, 9), 8), (N1.biggest(0, 9), 8)])])

defunit("numbers-to-20", sort=2, seed=82002, dom=NUM, std=S_CNT,
        title="20까지의 수 세기", short="20까지 세기",
        meta="유치원(만 5세) 20까지의 수 학습지: 10 만들기, 10과 몇(십몇), 11부터 20까지 세기와 읽기(열하나·십일), 수의 순서, 많고 적음까지 그림이 있는 100문제와 정답.",
        kb="10과 몇이면 십몇", ks="10과 3이면 13(열셋)이에요. 10씩 묶으면 세기 쉬워요.",
        think=["9 다음 수는 <b>10</b>이에요. 10은 열 또는 십이라고 읽어요.",
               "10개를 한 묶음으로 만들고 남은 것을 세면 쉬워요. 10과 3이면 <b>13</b>이에요.",
               "11은 열하나(십일), 15는 열다섯(십오), 20은 <b>스물</b>(이십)이에요.",
               "수를 순서대로 셀 때 뒤에 나오는 수가 더 커요."],
        ex=[("10개씩 묶음 1개와 낱개 4개", ["10과 4를 모아요."], "14"),
            ("16과 19 중 더 큰 수", ["16, 17, 18, 19 순서로 세요."], "19")],
        mist=[("10과 4를 104라고 쓴다", "10과 4는 14예요."),
              ("20을 '열열'이라고 읽는다", "20은 스물 또는 이십이에요."),
              ("10을 만들지 않고 하나씩 세다가 빠뜨린다", "10개를 먼저 묶고 남은 것을 세요.")],
        faq=[("20까지는 꼭 알아야 하나요?", "초등 1학년 1학기에 50까지의 수를 배워요. 유치원에서 20까지 셀 수 있으면 큰 도움이 돼요."),
             ("10 묶음은 어떻게 연습하나요?", "블록이나 빨대 10개를 고무줄로 묶어 '10과 몇'을 만들어 보세요.")],
        spec=lambda: [("11부터 20까지 세기", [(N1.count_pic(11, 20), 20)]),
                      ("10 만들기", [(N1.ten_make(), 15), (N1.ten_facts(), 5)]),
                      ("10과 몇", [(N1.teen_rods(), 16), (N1.word_to_num(11, 19), 4)]),
                      ("수 읽기와 순서", [(N1.read_both(11, 20), 8), (N1.word_to_num(11, 20), 4), (le(N1.one_more_less(10, 19), 20), 8)]),
                      ("수의 순서와 크기", [(le(N1.seq_cards(5, 20), 20), 7), (le(N1.between(10, 20), 21), 5), (le(N1.more_than(10, 20), 20), 8)])])

defunit("comparing-quantities", sort=3, seed=82003, dom=NUM, std=S_CNT,
        title="많고 적음 비교하기", short="많고 적음",
        meta="유치원(만 5세) 많고 적음 비교 학습지: 가장 많은 줄과 가장 적은 줄, 수가 같은 묶음, 하나씩 짝 지어 몇 개 더 많은지 알기, 이야기 문제까지 그림이 있는 100문제와 정답.",
        kb="하나씩 짝을 지어 비교해요", ks="짝이 없이 남는 쪽이 더 많아요. 남는 것이 없으면 같아요.",
        think=["두 가지를 비교할 때는 <b>하나씩 짝</b>을 지어 보세요. 짝이 없이 남는 쪽이 더 많아요.",
               "남는 것이 하나도 없으면 두 수는 <b>같아요</b>.",
               "세어서 비교할 수도 있어요. 수를 셀 때 뒤에 나오는 수가 더 많아요.",
               "물건의 크기가 달라도 수는 같을 수 있어요. 크기가 아니라 <b>개수</b>를 비교해요."],
        ex=[("사과 5개와 별 3개", ["하나씩 짝을 지으면 사과 2개가 남아요."], "사과가 2개 더 많아요"),
            ("가 4개, 나 4개", ["짝을 지으면 남는 것이 없어요."], "같아요")],
        mist=[("크게 그려진 쪽이 더 많다고 한다", "크기가 아니라 개수를 세어 비교해요."),
              ("길게 늘어선 줄이 더 많다고 한다", "간격이 넓으면 길어 보여요. 하나씩 짝을 지어 봐요."),
              ("몇 개 더 많은지를 큰 수로 답한다", "짝 짓고 남은 것만 세요.")],
        faq=[("많고 적음은 어떻게 가르치나요?", "그릇에 담긴 간식을 하나씩 짝 지어 보며 어느 쪽이 남는지 이야기해 보세요."),
             ("왜 짝 짓기부터 하나요?", "수를 세지 않아도 비교할 수 있어서, 수의 크기를 처음 익히는 데 좋아요. 초등 1학년 뺄셈(더 많은 것 구하기)으로 이어져요.")],
        spec=lambda: [("가장 많은 줄, 가장 적은 줄", [(cmp_rows(), 20)]),
                      ("수가 같은 묶음", [(cmp_equal(), 20)]),
                      ("더 큰 수, 더 작은 수", [(le(N1.more_than(0, 10), 10), 10), (N1.biggest(0, 9), 10)]),
                      ("몇 개 더 많을까요", [(N1.match_more(), 20)]),
                      ("이야기 문제", [(N1.most_story(1, 10, "구슬"), 10), (N1.most_story(1, 10, "스티커"), 10)])])

defunit("ordinal-numbers", sort=4, seed=82004, dom=NUM, std=S_CNT,
        title="첫째, 둘째… 순서 알기", short="순서(몇째)",
        meta="유치원(만 5세) 순서 학습지: 첫째부터 열째까지, 왼쪽·오른쪽에서 몇째, 앞·뒤에서 몇째, 선반의 위·아래에서 몇째, 몇째와 몇 개의 차이까지 그림이 있는 100문제와 정답.",
        kb="어디에서부터 세는지 먼저 봐요", ks="왼쪽에서 셋째와 오른쪽에서 셋째는 달라요. 셋째는 하나, 세 개는 셋이에요.",
        think=["순서를 말할 때는 <b>첫째, 둘째, 셋째, 넷째, 다섯째…열째</b>라고 해요.",
               "먼저 어디에서부터 세는지 봐요. 왼쪽에서 셋째와 오른쪽에서 셋째는 다른 것일 수 있어요.",
               "'셋째'는 <b>하나</b>만 가리켜요. '세 개'는 모두 셋이에요."],
        ex=[("앞에서 둘째에 선 친구", ["앞에서부터 첫째, 둘째 하고 세요."], "둘째 자리의 친구"),
            ("넷째 바로 다음", ["넷째, 다섯째 순서예요."], "다섯째")],
        mist=[("오른쪽에서 세라고 했는데 왼쪽에서 센다", "어디에서부터 세는지 먼저 확인해요."),
              ("'셋째'에 색칠하라고 했는데 세 개를 칠한다", "셋째는 하나만 칠해요."),
              ("'첫째'를 '하나째'라고 한다", "순서는 첫째, 둘째, 셋째예요.")],
        faq=[("몇째는 언제 배우나요?", "초등 1학년 1학기 「9까지의 수」에서 다시 배워요. 줄서기, 달리기처럼 생활에서 자주 쓰면 금방 익혀요."),
             ("집에서 어떻게 연습하나요?", "인형을 한 줄로 세우고 '왼쪽에서 둘째는?'처럼 번갈아 물어보세요.")],
        spec=lambda: [("왼쪽·오른쪽에서 몇째", [(N1.order_objects(), 20)]),
                      ("앞·뒤에서 몇째", [(N1.order_names(), 20)]),
                      ("위·아래에서 몇째", [(pos_shelf(("ord", "top")), 20)]),
                      ("몇째와 몇 개", [(N1.ord_vs_count(), 20)]),
                      ("순서 말하기", [(ord_word(), 12), (ord_race(), 8)])])

defunit("putting-together-and-taking-apart", sort=5, seed=82005, dom=NUM, std=S_CNT,
        title="모으기와 가르기 (10까지)", short="모으기와 가르기",
        meta="유치원(만 5세) 모으기와 가르기 학습지: 두 수를 모으기, 한 수를 두 수로 가르기, 주사위 눈 모으기, 10이 되는 두 수(10칸 상자)까지 그림이 있는 100문제와 정답.",
        kb="3과 2를 모으면 5", ks="5는 3과 2, 4와 1로 가를 수 있어요. 10은 7과 3이에요.",
        think=["두 수를 하나로 합치는 것을 <b>모으기</b>라고 해요. 3과 2를 모으면 5예요.",
               "하나의 수를 두 수로 나누는 것을 <b>가르기</b>라고 해요. 5는 4와 1, 3과 2로 가를 수 있어요.",
               "10칸 상자에서 빈칸을 세면 10이 되려면 몇이 더 필요한지 알 수 있어요."],
        ex=[("4와 3을 모으면?", ["4 다음부터 5, 6, 7 하고 이어 세요."], "7"),
            ("8은 6과 몇?", ["6에서 8까지 7, 8 하고 두 번 세요."], "2")],
        mist=[("4와 3을 모을 때 4, 5, 6으로 세어 6이라고 한다", "4 다음부터 세 번: 5, 6, 7"),
              ("가르기를 할 때 두 수를 더하지 않고 하나만 쓴다", "가른 두 수를 다시 모으면 처음 수가 돼요."),
              ("10이 되려면 채운 칸을 센다", "빈칸을 세요.")],
        faq=[("모으기와 가르기가 왜 중요한가요?", "초등 1학년 덧셈과 뺄셈의 바탕이에요. 특히 10이 되는 두 수를 알면 받아올림 계산이 쉬워져요."),
             ("집에서 어떻게 연습하나요?", "사탕 5개를 두 손에 나누어 쥐고 '한 손에 2개면 다른 손에는?' 하고 놀이처럼 물어보세요.")],
        spec=lambda: [("6까지 모으기와 가르기", [(C1.bond9(6), 14), (C1.dice_sum(), 6)]),
                      ("10까지 모으기와 가르기", [(C1.bond9(10), 20)]),
                      ("여러 가지로 가르기", [(C1.split_ways(), 6), (C1.bond9(9), 14)]),
                      ("10이 되는 두 수", [(N1.ten_make(), 20)]),
                      ("섞어서 연습", [(C1.bond9(10), 12), (C1.dice_sum(), 8)])])

defunit("adding-and-taking-away", sort=6, seed=82006, dom=NUM, std=S_CNT,
        title="더하기와 빼기 (10까지)", short="더하기와 빼기",
        meta="유치원(만 5세) 더하기와 빼기 학습지: 그림을 보고 모두 몇 개, 지우고 남은 것, 몇 개 더 많은지, 간단한 식, 이야기 문제까지 9까지의 수로 된 그림 100문제와 정답.",
        kb="더 생기면 많아지고, 덜어 내면 적어져요", ks="3개에 2개가 더 오면 5개, 5개에서 2개를 먹으면 3개예요.",
        think=["물건이 <b>더 생기면</b> 수가 많아져요. 3개에 2개를 더하면 5개예요. 3 + 2 = 5",
               "물건을 <b>덜어 내면</b> 수가 적어져요. 5개에서 2개를 먹으면 3개가 남아요. 5 − 2 = 3",
               "그림을 보고 처음에 몇 개였는지, 몇 개가 오고 갔는지 먼저 말해 보세요."],
        ex=[("오리 4마리에 2마리가 더 왔어요.", ["4 다음부터 5, 6 하고 세요."], "6마리"),
            ("사탕 7개 중 3개를 먹었어요.", ["7에서 거꾸로 6, 5, 4"], "4개")],
        mist=[("더 왔는데 빼서 답한다", "더 오면 많아져요. 더하기예요."),
              ("남은 것을 묻는데 먹은 것을 답한다", "지우지 않은 것을 세요."),
              ("이어 셀 때 처음 수를 한 번 더 센다", "처음 수 다음부터 세요.")],
        faq=[("유치원에서 +, − 기호를 써도 되나요?", "그림과 이야기로 충분히 익힌 다음이면 괜찮아요. 기호는 초등 1학년 1학기에 정식으로 배워요."),
             ("손가락으로 세어도 되나요?", "네, 처음에는 손가락이나 바둑돌로 세어도 좋아요.")],
        spec=lambda: [("모두 몇 개일까요", [(C1.add_pic(), 20)]),
                      ("남은 것은 몇 개일까요", [(C1.sub_pic(), 20)]),
                      ("그림과 식", [(C1.calc9("+"), 10), (C1.calc9("−"), 10)]),
                      ("더하기 이야기", [(C1.story9(("join", "add")), 20)]),
                      ("빼기 이야기", [(C1.story9(("take", "comp")), 20)])])

defunit("sharing-and-grouping", sort=7, seed=82007, dom=NUM, std=S_CNT,
        title="똑같이 나누기와 묶어 세기", short="똑같이 나누기",
        meta="유치원(만 5세) 똑같이 나누기 학습지: 친구와 똑같이 나누기, 한 명이 받는 수, 2개씩·3개씩 묶기, 접시에 나눈 수, 이야기 문제까지 10까지의 수로 된 그림 100문제와 정답.",
        kb="한 명에게 하나씩 차례로 나눠요", ks="6개를 2명이 똑같이 나누면 3개씩이에요. 모두 같으면 똑같이 나눈 거예요.",
        think=["똑같이 나눌 때는 한 명에게 <b>하나씩 차례로</b> 나누어 주세요. 다 나누면 한 명이 받은 수를 세어요.",
               "똑같이 나누면 모든 사람이 받은 수가 <b>같아요</b>.",
               "2개씩, 3개씩 동그라미로 묶으면 몇 묶음인지 셀 수 있어요."],
        ex=[("딸기 8개를 2명이 똑같이", ["한 명씩 번갈아 하나씩 주면 4개씩이에요."], "4개씩"),
            ("공 6개를 2개씩 묶으면", ["2개씩 묶으면 3묶음이에요."], "3묶음")],
        mist=[("2개와 4개로 나누고 똑같다고 한다", "두 사람의 수가 같아야 해요."),
              ("몇 묶음을 묻는데 한 묶음 안의 수를 답한다", "묶음의 수를 세요."),
              ("나누어 준 사람 수를 답한다", "한 명이 받은 물건의 수를 세요.")],
        faq=[("나눗셈을 배우는 건가요?", "아니에요. 놀이처럼 똑같이 나누어 보는 경험이에요. 초등 2·3학년 곱셈과 나눗셈의 바탕이 돼요."),
             ("집에서 어떻게 연습하나요?", "간식을 가족 수만큼 접시에 똑같이 나누어 담아 보세요.")],
        spec=lambda: [("똑같이 나눈 것 찾기", [(share_fair(), 20)]),
                      ("한 명이 몇 개씩", [(share_eq(), 20)]),
                      ("몇 묶음일까요", [(share_group(), 20)]),
                      ("접시에 나누기", [(share_plate(), 20)]),
                      ("이야기 문제", [(share_story(), 20)])])

defunit("position-and-direction", sort=8, seed=82008, dom=GEO, std="물체의 위치와 방향, 모양을 알고 구별한다.",
        title="위치와 방향 (위·아래·앞·뒤·옆)", short="위치와 방향",
        meta="유치원(만 5세) 위치와 방향 학습지: 위·아래·옆, 앞·뒤, 선반의 맨 위와 맨 아래, 왼쪽·오른쪽·사이, 9칸 그림에서 위치 찾기까지 그림이 있는 100문제와 정답.",
        kb="무엇을 기준으로 보는지 먼저 찾아요", ks="책상 위, 상자 뒤처럼 기준이 되는 물건과 함께 말해요.",
        think=["위치를 말할 때는 <b>기준</b>이 되는 물건을 먼저 찾아요. '책상 <b>위</b>', '상자 <b>뒤</b>'처럼 말해요.",
               "<b>위·아래</b>는 높고 낮은 곳, <b>앞·뒤</b>는 가깝고 가려진 곳, <b>옆</b>은 나란히 있는 곳이에요.",
               "<b>왼쪽·오른쪽</b>은 그림을 보는 내 쪽에서 생각해요. 숟가락을 드는 손이 오른쪽이에요(사람마다 달라요).",
               "두 물건 가운데 있는 것은 '<b>사이</b>'에 있다고 해요."],
        ex=[("공이 상자에 가려 조금만 보여요.", ["가려진 것은 뒤에 있어요."], "상자 뒤"),
            ("사과, 별, 컵이 한 줄로 있어요. 별의 바로 오른쪽은?", ["별에서 오른쪽으로 하나 가요."], "컵")],
        mist=[("왼쪽과 오른쪽을 바꾸어 말한다", "그림을 보는 나를 기준으로 생각해요."),
              ("'위에서 둘째'를 아래에서 센다", "어디에서부터 세는지 먼저 봐요."),
              ("가려진 물건을 앞에 있다고 한다", "가려진 것은 뒤에 있어요.")],
        faq=[("왼쪽·오른쪽을 헷갈려요.", "만 5세에게는 자연스러운 일이에요. 오른손에 스티커를 붙이고 '스티커 쪽이 오른쪽' 하고 놀이로 익혀 보세요."),
             ("초등학교에서는 언제 배우나요?", "초등 1학년 「여러 가지 모양」과 4학년 「위치와 방향」으로 이어져요.")],
        spec=lambda: [("위·아래·옆", [(pos_table(), 14), (pos_words(), 6)]),
                      ("앞·뒤·옆·위", [(pos_box(), 20)]),
                      ("선반의 위와 아래", [(pos_shelf(("top", "near")), 20)]),
                      ("왼쪽·오른쪽·사이", [(pos_lr(), 20)]),
                      ("9칸 그림에서 찾기", [(pos_grid(), 20)])])

defunit("shapes", sort=9, seed=82009, dom=GEO, std="물체의 위치와 방향, 모양을 알고 구별한다.",
        title="여러 가지 모양 알기", short="여러 가지 모양",
        meta="유치원(만 5세) 모양 학습지: 상자·둥근 기둥·공 모양, □(네모)·△(세모)·○(동그라미) 모양, 생활 속 물건의 모양, 같은 모양 세기까지 그림이 있는 100문제와 정답.",
        kb="평평한지, 둥근지, 뾰족한지 봐요", ks="공은 잘 굴러가고 상자는 잘 쌓여요. 세모는 뾰족한 곳이 3군데예요.",
        think=["물건의 모양은 <b>상자 모양, 둥근 기둥 모양, 공 모양</b>으로 나눌 수 있어요.",
               "상자 모양은 평평해서 잘 쌓여요. 공 모양은 둥글어서 잘 굴러가요. 둥근 기둥 모양은 눕히면 굴러가고 세우면 쌓여요.",
               "종이에 대고 그리면 <b>네모(□), 세모(△), 동그라미(○)</b> 모양이 나와요.",
               "색이나 크기가 달라도 생김새가 같으면 같은 모양이에요."],
        ex=[("두루마리 휴지는 어떤 모양?", ["위아래는 평평하고 옆은 둥글어요."], "둥근 기둥 모양"),
            ("뾰족한 곳이 없는 모양", ["둥근 선만 있어요."], "○ 모양")],
        mist=[("색이 다르면 다른 모양이라고 한다", "생김새로 나누어요."),
              ("거꾸로 놓인 △을 다른 모양이라고 한다", "돌려도 △ 모양이에요."),
              ("상자 모양도 잘 굴러간다고 한다", "평평한 부분만 있어서 굴러가지 않아요.")],
        faq=[("도형 이름(원기둥, 삼각형)을 알려 줘야 하나요?", "유치원에서는 상자 모양, 공 모양, 세모, 네모처럼 생활 속 말로 충분해요."),
             ("집에서 어떻게 연습하나요?", "집 안의 물건을 모아 굴려 보고 쌓아 보며 모양끼리 나누어 보세요.")],
        spec=lambda: [("상자·둥근 기둥·공 모양", [(G1.sol_name(), 12), (G1.sol_feature(), 8)]),
                      ("생활 속 물건의 모양", [(G1.sol_obj(), 20)]),
                      ("□·△·○ 모양", [(G1.flat_name(), 20)]),
                      ("생활 속 □·△·○", [(G1.flat_obj(), 14), (G1.flat_trace(), 6)]),
                      ("같은 모양 세기", [(le(G1.sol_count(), 10), 10), (le(G1.flat_count(), 10), 10)])])

defunit("comparing-length-weight-and-capacity", sort=10, seed=82010, dom=CMP, std="일상에서 길이, 무게 등의 속성을 비교한다.",
        title="길이·높이·무게·넓이·들이 비교", short="길이와 무게 비교",
        meta="유치원(만 5세) 비교하기 학습지: 더 긴 것과 더 짧은 것, 더 높은 것, 저울로 더 무거운 것, 더 넓은 것, 물이 더 많이 들어가는 그릇까지 그림이 있는 100문제와 정답.",
        kb="한쪽 끝을 맞추고 비교해요", ks="저울은 내려간 쪽이 더 무거워요. 그릇은 크기와 물 높이를 함께 봐요.",
        think=["길이를 비교할 때는 <b>한쪽 끝을 맞추고</b> 다른 쪽 끝을 봐요. 더 많이 나온 것이 더 길어요.",
               "높이는 바닥을 맞추고 위쪽을 봐요. 더 높이 올라간 것이 더 높아요.",
               "양팔저울은 <b>내려간 쪽이 더 무거워요</b>.",
               "넓이는 겹쳐 보고, 들이는 물을 옮겨 담아 비교해요."],
        ex=[("연필과 크레파스 중 더 긴 것", ["왼쪽 끝을 맞추어 놓아요."], "오른쪽 끝이 더 나온 것"),
            ("양팔저울에서 사과 쪽이 내려갔어요.", ["내려간 쪽이 무거워요."], "사과가 더 무거워요")],
        mist=[("끝을 맞추지 않고 길이를 비교한다", "한쪽 끝을 맞추어요."),
              ("저울에서 올라간 쪽이 무겁다고 한다", "내려간 쪽이 무거워요."),
              ("큰 것은 항상 무겁다고 생각한다", "풍선처럼 커도 가벼운 것이 있어요.")],
        faq=[("cm, kg 같은 단위를 알려 줘야 하나요?", "유치원에서는 직접 비교하는 경험이 중요해요. 단위는 초등 2학년(cm), 3학년(kg, L)에서 배워요."),
             ("집에서 어떻게 연습하나요?", "가족의 신발 길이를 나란히 놓고 비교하거나, 컵에 물을 옮겨 담아 보세요.")],
        spec=lambda: [("길이 비교", [(G1.cmp_len(), 12), (G1.cmp_len_offset(), 8)]),
                      ("높이 비교", [(G1.cmp_tower(), 14), (G1.cmp_words(("높이", "길이")), 6)]),
                      ("무게 비교", [(G1.cmp_weight(), 10), (G1.cmp_weight3(), 6), (G1.cmp_words(("무게",)), 4)]),
                      ("넓이 비교", [(G1.cmp_area(), 15), (G1.cmp_words(("넓이",)), 5)]),
                      ("들이 비교", [(G1.cmp_water(), 15), (G1.cmp_words(("들이",)), 5)])])

defunit("patterns", sort=11, seed=82011, dom=PAT, std="주변에서 반복되는 규칙을 찾는다.",
        title="반복되는 규칙 찾기", short="규칙 찾기",
        meta="유치원(만 5세) 규칙 찾기 학습지: 물건의 규칙, 색깔의 규칙, 모양의 규칙, 가운데 빈칸 채우기, 소리의 규칙(짝 쿵 짝 쿵)까지 그림이 있는 100문제와 정답.",
        kb="되풀이되는 부분을 찾아요", ks="빨강, 파랑, 빨강, 파랑… 빨강과 파랑이 되풀이돼요.",
        think=["같은 것이 <b>되풀이되는 부분</b>을 찾으면 규칙을 알 수 있어요.",
               "처음 두세 개만 보지 말고 끝까지 보며 되풀이되는 부분을 찾아요. '사과, 사과, 별'이 되풀이될 수도 있어요.",
               "되풀이되는 부분을 손가락으로 묶어 보면 다음에 올 것을 알 수 있어요."],
        ex=[("○ △ ○ △ ○ ?", ["○, △가 되풀이돼요."], "△"),
            ("짝 짝 쿵, 짝 짝 쿵, 짝 ?", ["짝 짝 쿵이 되풀이돼요."], "짝")],
        mist=[("처음 두 개만 보고 규칙을 정한다", "끝까지 보고 되풀이되는 부분을 찾아요."),
              ("빈칸 앞의 것을 그대로 쓴다", "규칙에서 빈칸의 자리를 찾아요."),
              ("색깔 규칙인데 모양만 본다", "무엇이 바뀌는지 먼저 봐요.")],
        faq=[("규칙 찾기는 왜 중요한가요?", "규칙을 찾는 힘은 수 세기, 곱셈구구, 나중의 함수 공부까지 이어져요."),
             ("집에서 어떻게 연습하나요?", "구슬 꿰기, 블록 늘어놓기, 손뼉 놀이로 아이가 규칙을 만들고 말로 설명하게 해 보세요.")],
        spec=lambda: [("물건의 규칙", [(G1.pat_obj(), 20)]),
                      ("색깔의 규칙", [(G1.pat_color(), 20)]),
                      ("모양의 규칙", [(pat_shape(), 20)]),
                      ("빈칸 채우기", [(pat_mid(), 20)]),
                      ("소리의 규칙", [(pat_body(), 20)])])

defunit("sorting-and-classifying", sort=12, seed=82012, dom=SORT, std="일상에서 모은 자료를 기준에 따라 분류한다.",
        title="기준에 따라 분류하기", short="분류하기",
        meta="유치원(만 5세) 분류하기 학습지: 분류 기준 정하기, 종류별로 세기, 색깔과 모양으로 나누기, 분리배출·동물·탈것 분류, 표를 보고 말하기까지 그림이 있는 100문제와 정답.",
        kb="누가 해도 같은 기준으로 나눠요", ks="'예쁜 것'은 사람마다 달라요. 색깔, 모양, 종류처럼 분명한 기준을 써요.",
        think=["분류할 때는 <b>누가 해도 결과가 같은 기준</b>을 써요. 색깔, 모양, 종류, 다리 수 같은 기준이에요.",
               "'예쁜 것, 좋아하는 것'은 사람마다 달라서 분류 기준이 될 수 없어요.",
               "기준을 정하면 같은 것끼리 모으고, 몇 개인지 세어 봐요."],
        ex=[("빨간 공, 파란 공, 빨간 블록", ["색깔로 나누면 빨간색 2개, 파란색 1개"], "빨간색이 더 많아요"),
            ("우유갑은 어디에 버릴까요?", ["종이로 만들었어요."], "종이류")],
        mist=[("'예쁜 것'으로 나눈다", "누가 해도 같은 기준을 써요."),
              ("세면서 같은 것을 두 번 센다", "센 것에 표시를 해요."),
              ("색깔로 나누라고 했는데 모양으로 나눈다", "어떤 기준인지 먼저 확인해요.")],
        faq=[("분류는 왜 배우나요?", "분류하고 세어 보는 경험은 초등 2학년 「분류하기」, 「표와 그래프」로 이어져요."),
             ("집에서 어떻게 연습하나요?", "빨래 개기, 장난감 정리, 분리배출을 함께 하며 '무엇끼리 모을까?' 하고 기준을 말해 보세요.")],
        spec=lambda: [("분류 기준", [(D2.s_crit(), 8), (D2.s_life(), 12)]),
                      ("종류별로 세기", [(le(D2.s_kind_count(), 18), 20)]),
                      ("색깔과 모양으로 나누기", [(D2.s_shape_count(), 20)]),
                      ("생활 속 분류", [(D2.s_life(), 20)]),
                      ("두 가지 기준과 표", [(D2.s_two(), 10), (le(D2.s_result(), 10), 10)])])
