# -*- coding: utf-8 -*-
"""
대한민국 초등 1학년 수학：도형・측정・규칙（2022 개정）の 5 単元
  solid  : 여러 가지 모양（상자・둥근 기둥・공 모양）[2수03-01]      1-1
  compare: 비교하기（길이・높이・무게・넓이・들이）[2수03-06]          1-1
  flat   : 여러 가지 모양（□・△・○ 모양）[2수03-03]                1-2
  time   : 몇 시, 몇 시 30분 [2수03-07]                             1-2
  pattern: 규칙 찾기 [2수02-01] [2수02-02]                          1-2
誤答は「긴바늘을 시로 읽는다」「짧은바늘이 지난 수가 아니라 다음 수를 읽는다」「방향이 바뀌면 다른 모양이라고 생각한다」
「길이를 잴 때 한쪽 끝을 맞추지 않는다」「물의 높이만 보고 그릇 크기를 보지 않는다」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa, clock
from kr_low import KINDS, LET, nm, cw, ko, lg, pencils, towers, scale, glasses, near, cards, chart, fig
import k_pics as K
from f_common import pattern_svg
from ws_common import svg_wrap, text, INK, GREEN, RED

R = random.Random(82102)
NM = Names(R)
G = "grade-1"

SOL = {"cube": "상자 모양", "cylinder": "둥근 기둥 모양", "sphere": "공 모양"}
FLAT = {"square": "□ 모양", "rectangle": "□ 모양", "triangle": "△ 모양", "circle": "○ 모양"}
FLATS = ["□ 모양", "△ 모양", "○ 모양"]
COL = {"red": "빨간색", "blue": "파란색", "yellow": "노란색", "green": "초록색"}


def solid_pic(kind, color):
    return ko(K.one_solid_svg(kind, color, 34), SOL[kind])


def flat_pic(kind, color, rot=0, r=36):
    return ko(K.one_shape_svg(kind, color, r, rot), FLAT[kind])


# ------------------------------------------------------------------ 상자・둥근 기둥・공 모양
OBJ3 = {"상자 모양": ["주사위", "휴지 상자", "선물 상자", "벽돌", "냉장고", "필통", "과자 상자", "책"],
        "둥근 기둥 모양": ["음료수 캔", "딱풀", "두루마리 휴지", "북", "통조림", "양초", "페인트 통", "저금통(원통)"],
        "공 모양": ["축구공", "구슬", "수박", "지구본", "야구공", "볼링공", "탁구공", "농구공"]}


def sol_name():
    def mk():
        k = R.choice(list(SOL))
        c = R.choice(list(COL))
        return mcq("이 물건은 어떤 모양일까요? (%s)%s" % (COL[c], solid_pic(k, c)), SOL[k], [v for v in SOL.values() if v != SOL[k]] + ["□ 모양"],
                   {"cube": "평평한 부분과 뾰족한 부분이 있어요. <b>상자 모양</b>이에요.",
                    "cylinder": "평평한 부분과 둥근 부분이 있어요. <b>둥근 기둥 모양</b>이에요.",
                    "sphere": "어느 쪽도 둥글어요. <b>공 모양</b>이에요."}[k])
    return mk


def sol_obj():
    pool = [(o, k) for k, os in OBJ3.items() for o in os]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        o, k = pool.pop()
        return mcq("<b>%s</b> 어떤 모양일까요?" % josa(o, "은/는"), k, [v for v in SOL.values() if v != k] + ["모양이 없어요"],
                   "%s %s이에요." % (josa(o, "은/는"), k))
    return mk


def sol_odd():
    def mk():
        k = R.choice(list(OBJ3))
        others = [x for x in OBJ3 if x != k]
        same = R.sample(OBJ3[k], 3)
        odd = R.choice(OBJ3[R.choice(others)])
        return mcq("모양이 <b>다른</b> 하나는 무엇일까요?<br>%s" % ", ".join(R.sample(same + [odd], 4)), odd, same,
                   "%s %s이고, %s %s이 아니에요." % (josa(", ".join(same), "은/는"), k, josa(odd, "은/는"), k))
    return mk


SOL_FACT = [("어느 쪽으로 굴려도 잘 굴러가는 모양은 무엇일까요?", "공 모양", "모든 부분이 둥글어서 어느 쪽으로도 잘 굴러가요."),
            ("뾰족한 부분이 있는 모양은 무엇일까요?", "상자 모양", "상자 모양에는 뾰족한 부분이 있어요."),
            ("평평한 부분만 있는 모양은 무엇일까요?", "상자 모양", "상자 모양은 평평한 부분만 있어요."),
            ("둥근 부분만 있는 모양은 무엇일까요?", "공 모양", "공 모양은 둥근 부분만 있어요."),
            ("위에 다른 물건을 쌓기 가장 어려운 모양은 무엇일까요?", "공 모양", "평평한 부분이 없어서 쌓기 어려워요."),
            ("눕히면 잘 굴러가고, 세우면 쌓을 수 있는 모양은 무엇일까요?", "둥근 기둥 모양", "둥근 부분과 평평한 부분이 모두 있어요."),
            ("어느 방향으로 놓아도 잘 쌓을 수 있는 모양은 무엇일까요?", "상자 모양", "모든 부분이 평평해서 잘 쌓여요."),
            ("평평한 부분과 둥근 부분이 모두 있는 모양은 무엇일까요?", "둥근 기둥 모양", "위아래는 평평하고 옆은 둥글어요."),
            ("굴리면 한쪽으로만 굴러가는 모양은 무엇일까요?", "둥근 기둥 모양", "눕혀서 굴리면 둥근 옆면으로 굴러가요."),
            ("어느 쪽으로도 굴러가지 않는 모양은 무엇일까요?", "상자 모양", "평평한 부분만 있어서 굴러가지 않아요.")]


def sol_fact():
    pool = SOL_FACT[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        q, a, e = pool.pop()
        return mcq(q, a, [v for v in SOL.values() if v != a] + ["세 모양 모두"], e + " <b>%s</b>" % a)
    return mk


def sol_feature():
    FE = {"cube": ("평평한 부분과 뾰족한 부분이 있어요", ["둥근 부분만 있어요", "어느 쪽으로도 잘 굴러가요", "평평한 부분이 없어요"]),
          "cylinder": ("눕히면 굴러가고, 세우면 쌓을 수 있어요", ["뾰족한 부분이 있어요", "둥근 부분만 있어요", "평평한 부분만 있어요"]),
          "sphere": ("어느 쪽으로 굴려도 잘 굴러가요", ["평평한 부분이 있어요", "뾰족한 부분이 있어요", "쌓기 쉬워요"])}

    def mk():
        k = R.choice(list(SOL))
        c = R.choice(list(COL))
        ok, bad = FE[k]
        return mcq("이 모양(%s)에 대해 바르게 말한 것은 무엇일까요?%s" % (COL[c], solid_pic(k, c)), ok, bad, "%s이에요. %s." % (SOL[k], ok))
    return mk


def solids_row(items):
    sp = 100
    s = [K.solid(k, 52 + i * sp, 64, 34, c) for i, (k, c) in enumerate(items)]
    return ko(svg_wrap(len(items) * sp + 10, 128, "".join(s), "여러 가지 모양"), "여러 가지 모양")


def sol_count():
    def mk():
        n = R.randint(5, 7)
        items = [(R.choice(list(SOL)), R.choice(list(COL))) for _ in range(n)]
        k = R.choice(list(SOL))
        c = sum(1 for x, _ in items if x == k)
        if c == 0:
            return None
        return mcq("<b>%s</b> 몇 개일까요?%s" % (SOL[k] + "은", solids_row(items)), "%d개" % c, ["%d개" % x for x in near(c, 0, n) + [n]],
                   "%s만 하나씩 세어 보면 <b>%d개</b>예요." % (SOL[k], c))
    return mk


def built(cols):
    """쌓아 만든 모양：cols = [[아래→위 kind]]"""
    sp = 70
    W = len(cols) * sp + 20
    H = 40 + max(len(c) for c in cols) * 60
    s = ["<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (H - 6, W - 4, H - 6, INK)]
    COLS = ["yellow", "blue", "red", "green"]
    for i, col in enumerate(cols):
        y = H - 6
        for j, k in enumerate(col):
            h = 56 if k == "cube" else 58 if k == "cylinder" else 50
            cy = y - h / 2
            s.append(K.solid(k, 18 + sp / 2 + i * sp, cy, 24, COLS[(i + j) % 4]))
            y -= h
    return ko(svg_wrap(W, H, "".join(s), "모양을 쌓아 만든 것"), "모양을 쌓아 만든 것")


def sol_built():
    def mk():
        cols = []
        for _ in range(R.randint(3, 4)):
            h = R.randint(1, 3)
            col = [R.choice(["cube", "cube", "cylinder"]) for _ in range(h - 1)]
            col.append(R.choice(["cube", "cylinder", "sphere"]))
            cols.append(col)
        allk = [k for c in cols for k in c]
        how = R.choice(["count", "most", "total"])
        if how == "total":
            n = len(allk)
            return mcq("모양을 쌓아 만들었어요. 모두 몇 개를 사용했을까요?%s" % built(cols), "%d개" % n, ["%d개" % x for x in near(n, 1)],
                       "모양을 하나씩 세면 <b>%d개</b>예요." % n)
        if how == "count":
            k = R.choice(list(SOL))
            c = allk.count(k)
            return mcq("모양을 쌓아 만들었어요. %s 몇 개를 사용했을까요?%s" % (SOL[k] + "은", built(cols)), "%d개" % c, ["%d개" % x for x in near(c, 0, 12)],
                       "%s만 세면 <b>%d개</b>예요." % (SOL[k], c))
        cnt = {k: allk.count(k) for k in SOL}
        best = max(cnt.values())
        if list(cnt.values()).count(best) > 1:
            return None
        a = [SOL[k] for k in SOL if cnt[k] == best][0]
        return mcq("모양을 쌓아 만들었어요. 가장 많이 사용한 모양은 무엇일까요?%s" % built(cols), a, [v for v in SOL.values() if v != a] + ["모두 같아요"],
                   "상자 %d개, 둥근 기둥 %d개, 공 %d개를 사용했어요. <b>%s</b>" % (cnt["cube"], cnt["cylinder"], cnt["sphere"], a))
    return mk


# ------------------------------------------------------------------ □・△・○ 모양
OBJF = {"□ 모양": ["액자", "공책", "창문", "칠판", "달력", "손수건", "스케치북", "현관문"],
        "△ 모양": ["삼각자", "트라이앵글", "삼각김밥", "옷걸이", "양보 표지판", "샌드위치 반쪽", "삼각 깃발", "텐트의 앞면"],
        "○ 모양": ["동전", "시계", "접시", "단추", "CD", "훌라후프", "바퀴", "도넛"]}


def flat_name():
    def mk():
        k = R.choice(["square", "rectangle", "triangle", "circle"])
        c = R.choice(list(COL))
        rot = R.choice([0, 0, 20, 45, 180]) if k != "circle" else 0
        return mcq("어떤 모양일까요? (%s)%s" % (COL[c], flat_pic(k, c, rot)), FLAT[k], [x for x in FLATS if x != FLAT[k]] + ["공 모양"],
                   {"□ 모양": "곧은 선 4개와 뾰족한 곳 4군데가 있어요.", "△ 모양": "곧은 선 3개와 뾰족한 곳 3군데가 있어요.",
                    "○ 모양": "곧은 선과 뾰족한 곳이 없어요."}[FLAT[k]] + " 방향이 바뀌어도 모양은 같아요. <b>%s</b>" % FLAT[k])
    return mk


def flat_obj():
    pool = [(o, k) for k, os in OBJF.items() for o in os]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        o, k = pool.pop()
        return mcq("<b>%s</b> 어떤 모양일까요?" % josa(o, "은/는"), k, [x for x in FLATS if x != k] + ["공 모양"], "%s %s이에요." % (josa(o, "은/는"), k))
    return mk


TRACE = [("상자 모양을 종이에 대고 본뜨면 어떤 모양이 나올까요?", "□ 모양"),
         ("둥근 기둥 모양의 평평한 부분을 본뜨면 어떤 모양이 나올까요?", "○ 모양"),
         ("동전을 종이에 대고 본뜨면 어떤 모양이 나올까요?", "○ 모양"),
         ("주사위를 종이에 대고 본뜨면 어떤 모양이 나올까요?", "□ 모양"),
         ("음료수 캔의 밑면을 찍으면 어떤 모양이 나올까요?", "○ 모양"),
         ("휴지 상자를 찰흙 위에 찍으면 어떤 모양이 나올까요?", "□ 모양"),
         ("□ 모양 색종이를 반으로 접어 뾰족한 두 곳을 맞대어 잘랐어요. 잘린 한 조각은 어떤 모양일까요?", "△ 모양")]


def flat_trace():
    pool = TRACE[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        q, a = pool.pop()
        return mcq(q, a, [x for x in FLATS if x != a] + ["공 모양"], "<b>%s</b>이 나와요." % a)
    return mk


def flat_feature():
    def mk():
        how = R.choice(["corners", "lines", "which"])
        if how == "which":
            F = [("뾰족한 곳이 3군데 있는 모양은 무엇일까요?", "△ 모양"), ("뾰족한 곳이 4군데 있는 모양은 무엇일까요?", "□ 모양"),
                 ("뾰족한 곳이 없는 모양은 무엇일까요?", "○ 모양"), ("곧은 선 없이 둥근 선만 있는 모양은 무엇일까요?", "○ 모양"),
                 ("곧은 선이 3개 있는 모양은 무엇일까요?", "△ 모양"), ("곧은 선이 4개 있는 모양은 무엇일까요?", "□ 모양"),
                 ("굴리면 잘 굴러가는 모양은 무엇일까요?", "○ 모양")]
            q, a = R.choice(F)
            return mcq(q, a, [x for x in FLATS if x != a] + ["모두 아니에요"], "<b>%s</b>이에요." % a)
        k = R.choice(["square", "rectangle", "triangle", "circle"])
        c = R.choice(list(COL))
        rot = R.choice([0, 15, 30, 180]) if k != "circle" else 0
        v = {"square": 4, "rectangle": 4, "triangle": 3, "circle": 0}[k]
        if how == "corners":
            q = "이 모양에서 뾰족한 곳은 몇 군데일까요? (%s, %d도 돌림)%s" % (COL[c], rot, flat_pic(k, c, rot)) if rot else \
                "이 모양에서 뾰족한 곳은 몇 군데일까요? (%s)%s" % (COL[c], flat_pic(k, c, rot))
            a = "%d군데" % v if v else "없어요"
            return mcq(q.replace(", %d도 돌림" % rot, ""), a, [x for x in ("3군데", "4군데", "없어요", "1군데", "2군데") if x != a],
                       "뾰족한 곳을 하나씩 세면 <b>%s</b>." % ("%d군데예요" % v if v else "없어요"))
        a = "%d개" % v if v else "없어요"
        return mcq("이 모양에서 곧은 선은 몇 개일까요? (%s)%s" % (COL[c], flat_pic(k, c, rot)), a, [x for x in ("3개", "4개", "없어요", "2개", "1개") if x != a],
                   "곧은 선은 <b>%s</b>." % ("%d개예요" % v if v else "없어요(둥근 선만 있어요)"))
    return mk


def flat_count():
    def mk():
        n = R.randint(7, 11)
        items = [(R.choice(["square", "rectangle", "triangle", "circle"]), R.choice(list(COL))) for _ in range(n)]
        t = R.choice(FLATS)
        c = sum(1 for k, _ in items if FLAT[k] == t)
        pic = ko(K.shapes_mix_svg(items, R.randint(1, 10 ** 6), 5, 3), "여러 가지 모양")
        return mcq("<b>%s</b> 몇 개일까요?%s" % (t + "은", pic), "%d개" % c, ["%d개" % x for x in near(c, 0, n)],
                   "%s만 하나씩 세면 <b>%d개</b>예요.%s" % (t, c, " 길쭉한 □도 □ 모양이에요." if t == "□ 모양" else ""))
    return mk


def flat_scene():
    def mk():
        cells = R.sample([(c, r) for c in range(3) for r in range(3)], R.randint(6, 9))
        placed = [(R.choice(["square", "triangle", "circle", "rectangle"]), R.choice(list(COL)), c, r) for c, r in cells]
        pic = ko(K.shapes_scene_svg(placed), "모양으로 꾸민 그림")
        cntf = {t: sum(1 for k, _, _, _ in placed if FLAT[k] == t) for t in FLATS}
        if R.random() < 0.5:
            t = R.choice(FLATS)
            v = cntf[t]
            return mcq("모양으로 그림을 꾸몄어요. %s 몇 개 사용했을까요?%s" % (t + "은", pic), "%d개" % v, ["%d개" % x for x in near(v, 0, 9)],
                       "%s만 세면 <b>%d개</b>예요." % (t, v))
        best = max(cntf.values())
        if list(cntf.values()).count(best) > 1:
            return None
        a = [t for t in FLATS if cntf[t] == best][0]
        return mcq("모양으로 그림을 꾸몄어요. 가장 많이 사용한 모양은 무엇일까요?%s" % pic, a, [t for t in FLATS if t != a] + ["모두 같아요"],
                   "□ %d개, △ %d개, ○ %d개예요. <b>%s</b>" % (cntf["□ 모양"], cntf["△ 모양"], cntf["○ 모양"], a))
    return mk


# ------------------------------------------------------------------ 비교하기
def cmp_len():
    def mk():
        n = R.choice([3, 4])
        ls = R.sample(range(3, 10), n)
        long_ = R.random() < 0.5
        tgt = ls.index(max(ls) if long_ else min(ls))
        pic = pencils(ls, None, 30)
        return mcq("%s 연필은 어느 것일까요? (왼쪽 끝을 맞추었어요)%s" % ("가장 긴" if long_ else "가장 짧은", pic), LET[tgt], [LET[i] for i in range(n) if i != tgt] + ["모두 같아요"],
                   "왼쪽 끝이 맞추어져 있으니 오른쪽 끝이 %s 나온 것이 %s. <b>%s</b>" % ("가장 많이" if long_ else "가장 적게", "가장 길어요" if long_ else "가장 짧아요", LET[tgt]))
    return mk


def grid_pencils(specs, u=30):
    """모눈 위의 연필 2자루：specs = [(시작 칸, 길이 칸)]"""
    lw = 34
    W = lw + 12 * u + 16
    H = 20 + len(specs) * 44 + 10
    s = []
    for i in range(13):
        x = lw + i * u
        s.append("<line x1='%d' y1='8' x2='%d' y2='%d' stroke='#c8d8cc' stroke-width='1.2'/>" % (x, x, H - 6))
    for j in range(len(specs) + 1):
        y = 8 + j * 44
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#c8d8cc' stroke-width='1.2'/>" % (lw, y, lw + 12 * u, y))
    cols = ["#e74c3c", "#3498db"]
    for i, (st, L) in enumerate(specs):
        y = 8 + i * 44 + 11
        x0 = lw + st * u
        body = L * u - 18
        s.append(text(16, y + 17, LET[i], 18, col=GREEN))
        s.append("<rect x='%d' y='%d' width='8' height='22' fill='#f2b8c6' stroke='%s' stroke-width='1.5'/>" % (x0, y, INK))
        s.append("<rect x='%d' y='%d' width='%d' height='22' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x0 + 8, y, body - 8, cols[i], INK))
        tip = x0 + body
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='#f5deb3' stroke='%s' stroke-width='1.5'/>" % (tip, y, tip + 18, y + 11, tip, y + 22, INK))
    return ko(svg_wrap(W, H, "".join(s), "모눈 위의 연필 두 자루"), "모눈 위의 연필 두 자루")


def cmp_len_offset():
    """한쪽 끝이 맞지 않은 연필：칸을 세어 비교해요"""
    def mk():
        a, b = R.sample(range(3, 9), 2)
        oa = R.randint(0, 12 - a)
        ob = R.randint(0, 12 - b)
        if (oa + a > ob + b) == (a > b) or oa + a == ob + b:     # 오른쪽 끝만 보면 틀리도록
            return None
        big = LET[0] if a > b else LET[1]
        return mcq("두 연필 중 더 긴 것은 어느 것일까요? (연필이 몇 칸인지 세어 보세요)%s" % grid_pencils([(oa, a), (ob, b)]), big,
                   [LET[1] if big == LET[0] else LET[0], "길이가 같아요", "알 수 없어요"],
                   "왼쪽 끝이 맞지 않으니 오른쪽 끝만 보면 안 돼요. 가는 %d칸, 나는 %d칸이에요. <b>%s</b>" % (a, b, big))
    return mk


def cmp_tower():
    def mk():
        n = R.choice([3, 4])
        hs = R.sample(range(1, 8), n)
        hi = R.random() < 0.5
        tgt = hs.index(max(hs) if hi else min(hs))
        return mcq("상자를 쌓았어요. %s 것은 어느 것일까요?%s" % ("가장 높은" if hi else "가장 낮은", towers(hs)), LET[tgt], [LET[i] for i in range(n) if i != tgt] + ["모두 같아요"],
                   "아래쪽 끝이 맞추어져 있어요. 위쪽 끝이 %s 것은 <b>%s</b>예요." % ("가장 높은" if hi else "가장 낮은", LET[tgt]))
    return mk


def cmp_weight():
    def mk():
        a, b = R.sample(KINDS, 2)
        tilt = R.choice(["left", "right"])
        heavy, light = (a, b) if tilt == "left" else (b, a)
        pic = scale((a, 1), (b, 1), tilt)
        ok = "%s 더 무거워요" % josa(nm(heavy), "이/가")
        return mcq("양팔저울에 %s %s 올렸어요. 바르게 말한 것은 무엇일까요?%s" % (josa(nm(a), "과/와"), josa(nm(b), "을/를"), pic), ok,
                   ["%s 더 무거워요" % josa(nm(light), "이/가"), "%s 더 가벼워요" % josa(nm(heavy), "이/가"), "무게가 같아요"],
                   "무거운 쪽이 아래로 내려가요. <b>%s</b>" % ok)
    return mk


def cmp_weight3():
    def mk():
        ks = R.sample(KINDS, 3)
        heavy = R.random() < 0.5
        q = "%s %s보다 무겁고, %s %s보다 무거워요. 가장 %s 것은 무엇일까요?" % (josa(nm(ks[0]), "은/는"), nm(ks[1]), josa(nm(ks[1]), "은/는"), nm(ks[2]), "무거운" if heavy else "가벼운")
        a = nm(ks[0]) if heavy else nm(ks[2])
        return mcq(q, a, [nm(ks[1]), nm(ks[2]) if heavy else nm(ks[0]), "모두 같아요"],
                   "무거운 순서는 %s, %s, %s예요. <b>%s</b>" % (nm(ks[0]), nm(ks[1]), nm(ks[2]), a))
    return mk


def areas_pic(sizes):
    sp = 16
    x = 12
    H = max(h for _, h in sizes) * sp + 50
    s = []
    COLS = ["#f4c430", "#7fb3e6", "#f4a3a3", "#9fd3a7"]
    for i, (w, h) in enumerate(sizes):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, H - 34 - h * sp, w * sp, h * sp, COLS[i], INK))
        s.append(text(x + w * sp / 2, H - 10, LET[i], 18, col=GREEN))
        x += w * sp + 22
    return ko(svg_wrap(x, H, "".join(s), "넓이 비교"), "넓이 비교")


def cmp_area():
    def mk():
        n = R.choice([3, 4])
        sizes = []
        while len(sizes) < n:
            w, h = R.randint(2, 6), R.randint(2, 6)
            if any(abs(w * h - a * b) < 3 for a, b in sizes):
                continue
            sizes.append((w, h))
        big = R.random() < 0.5
        ar = [w * h for w, h in sizes]
        tgt = ar.index(max(ar) if big else min(ar))
        return mcq("%s 것은 어느 것일까요?%s" % ("가장 넓은" if big else "가장 좁은", areas_pic(sizes)), LET[tgt], [LET[i] for i in range(n) if i != tgt] + ["모두 같아요"],
                   "겹쳐 보았을 때 %s 쪽이 더 넓어요. <b>%s</b>" % ("남는", LET[tgt]) if big else "겹쳐 보았을 때 모자라는 쪽이 더 좁아요. <b>%s</b>" % LET[tgt])
    return mk


PAIRS = [("길이", "길어요", "짧아요", [("기차", "자동차"), ("지팡이", "연필"), ("줄넘기 줄", "운동화 끈"), ("기린의 목", "토끼의 귀"), ("빨대", "이쑤시개"), ("버스", "자전거")]),
         ("높이", "높아요", "낮아요", [("아파트", "우리 집 강아지 집"), ("산", "언덕"), ("가로등", "의자"), ("나무", "꽃")]),
         ("무게", "무거워요", "가벼워요", [("수박", "귤"), ("코끼리", "강아지"), ("책가방", "지우개"), ("의자", "연필"), ("볼링공", "탁구공"), ("냉장고", "컵")]),
         ("넓이", "넓어요", "좁아요", [("운동장", "교실 바닥"), ("이불", "손수건"), ("달력", "우표"), ("칠판", "공책"), ("책상", "필통")]),
         ("들이", "많이 담을 수 있어요", "적게 담을 수 있어요", [("양동이", "컵"), ("욕조", "세숫대야"), ("물병", "숟가락"), ("냄비", "밥그릇"), ("주전자", "요구르트병")])]


def cmp_words(cat):
    pool = [(w, big, small, a, b) for w, big, small, ps in PAIRS for a, b in ps if w in cat]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        w, big, small, a, b = pool.pop()
        ask_big = R.random() < 0.5
        x, y = (a, b) if R.random() < 0.5 else (b, a)
        ans = a if ask_big else b
        word = big if ask_big else small
        ok = "%s 더 %s" % (josa(ans, "이/가"), word)
        other = b if ans == a else a
        return mcq("%s %s의 %s를 비교해요. 바르게 말한 것은 무엇일까요?" % (josa(x, "과/와"), y, w), ok,
                   ["%s 더 %s" % (josa(other, "이/가"), word), "%s 더 %s" % (josa(ans, "이/가"), small if ask_big else big), "%s %s의 %s 같아요" % (josa(a, "과/와"), b, josa(w, "이/가"))],
                   "<b>%s</b>" % ok)
    return mk


def cmp_water():
    def mk():
        if R.random() < 0.5:     # 같은 그릇、물의 높이
            n = R.choice([3, 4])
            lv = R.sample([0.2, 0.35, 0.5, 0.65, 0.8, 0.95], n)
            items = [(56, 90, v) for v in lv]
            more = R.random() < 0.5
            tgt = lv.index(max(lv) if more else min(lv))
            return mcq("모양과 크기가 같은 그릇에 물을 담았어요. 물이 가장 %s 담긴 것은 어느 것일까요?%s" % ("많이" if more else "적게", glasses(items)), LET[tgt],
                       [LET[i] for i in range(n) if i != tgt] + ["모두 같아요"],
                       "그릇이 같으면 물의 높이가 %s 물이 %s. <b>%s</b>" % ("높을수록" if more else "낮을수록", "많아요" if more else "적어요", LET[tgt]))
        n = 3
        ws = R.sample([40, 56, 72, 88], n)
        hs = [R.choice([70, 80, 90]) for _ in range(n)]
        vol = [w * h for w, h in zip(ws, hs)]
        if len(set(vol)) < n:
            return None
        items = [(w, h, 1.0) for w, h in zip(ws, hs)]
        tgt = vol.index(max(vol))
        return mcq("물을 가득 채웠어요. 가장 많이 담을 수 있는 그릇은 어느 것일까요?%s" % glasses(items), LET[tgt], [LET[i] for i in range(n) if i != tgt] + ["모두 같아요"],
                   "그릇이 클수록 많이 담을 수 있어요. <b>%s</b>" % LET[tgt])
    return mk


# ------------------------------------------------------------------ 몇 시, 몇 시 30분
def t_hour():
    def mk():
        h = R.randint(1, 12)
        return mcq("시계가 나타내는 시각은 몇 시일까요?%s" % clock(h, 0, 170), "%d시" % h,
                   ["%d시" % x for x in (12 if h != 12 else 6, h % 12 + 1, (h - 2) % 12 + 1)] + ["%d시 30분" % h],
                   "짧은바늘이 %d, 긴바늘이 12를 가리켜요. <b>%d시</b>" % (h, h))
    return mk


def t_half():
    def mk():
        h = R.randint(1, 12)
        nx = h % 12 + 1
        return mcq("시계가 나타내는 시각은 몇 시 몇 분일까요?%s" % clock(h, 30, 170), "%d시 30분" % h,
                   ["%d시 30분" % nx, "6시" if h != 6 else "12시 30분", "%d시" % h, "%d시 6분" % h],
                   "짧은바늘이 %d과 %d 사이, 긴바늘이 6을 가리켜요. <b>%d시 30분</b>" % (h, nx, h))
    return mk


def t_hands():
    def mk():
        h = R.randint(1, 12)
        nx = h % 12 + 1
        how = R.choice(["short30", "long30", "long0", "short0"])
        if how == "short30":
            return mcq("<b>%d시 30분</b>일 때 짧은바늘은 어디를 가리킬까요?" % h, "%d과 %d 사이" % (h, nx),
                       ["%d" % h, "%d" % nx, "%d과 %d 사이" % ((h - 2) % 12 + 1, h)],
                       "30분이면 짧은바늘은 %d을 지나 %d 쪽으로 반쯤 가요. <b>%d과 %d 사이</b>" % (h, nx, h, nx))
        if how == "long30":
            return mcq("<b>%d시 30분</b>일 때 긴바늘은 어디를 가리킬까요?" % h, "6", ["12", "%d" % h if h != 6 else "3", "30"],
                       "30분일 때 긴바늘은 <b>6</b>을 가리켜요.")
        if how == "long0":
            return mcq("<b>%d시</b>일 때 긴바늘은 어디를 가리킬까요?" % h, "12", ["%d" % h if h not in (12, 6) else "3", "6", "9" if h != 9 else "1"],
                       "'몇 시'일 때 긴바늘은 <b>12</b>를 가리켜요.")
        return mcq("<b>%d시</b>일 때 짧은바늘은 어디를 가리킬까요?" % h, "%d" % h, ["12" if h != 12 else "6", "%d" % nx, "%d과 %d 사이" % (h, nx)],
                   "'몇 시'일 때 짧은바늘은 <b>%d</b>을 가리켜요." % h)
    return mk


def t_desc(kind=None):
    def mk():
        h = R.randint(1, 12)
        nx = h % 12 + 1
        if (kind or R.choice(["h", "m"])) == "h":
            return mcq("짧은바늘이 <b>%d</b>, 긴바늘이 <b>12</b>를 가리켜요. 몇 시일까요?" % h, "%d시" % h, ["12시" if h != 12 else "6시", "%d시 30분" % h, "%d시" % nx],
                       "짧은바늘은 '시', 긴바늘이 12면 '정각'이에요. <b>%d시</b>" % h)
        return mcq("짧은바늘이 <b>%d과 %d 사이</b>, 긴바늘이 <b>6</b>을 가리켜요. 몇 시 몇 분일까요?" % (h, nx), "%d시 30분" % h,
                   ["%d시 30분" % nx, "6시 %d분" % h, "%d시" % h], "지나온 수 %d을 읽고 30분을 붙여요. <b>%d시 30분</b>" % (h, h))
    return mk


DAY = [("아침을 먹어요", 7, 8), ("학교에 도착해요", 8, 9), ("점심을 먹어요", 12, 1), ("학교가 끝나요", 1, 2), ("태권도장에 가요", 3, 4),
       ("저녁을 먹어요", 6, 7), ("잠을 자요", 9, 10), ("숙제를 해요", 4, 5), ("놀이터에서 놀아요", 2, 3)]


def t_life():
    def mk():
        how = R.choice(["first", "order", "half"])
        if how == "first":
            n1, n2 = NM.next(), NM.next()
            if n1 == n2:
                return None
            h1 = R.randint(6, 8)
            m1, m2 = R.choice([0, 30]), R.choice([0, 30])
            h2 = h1 + R.choice([0, 1])
            if (h1, m1) == (h2, m2):
                return None
            t1, t2 = "%d시%s" % (h1, " 30분" if m1 else ""), "%d시%s" % (h2, " 30분" if m2 else "")
            first = n1 if (h1, m1) < (h2, m2) else n2
            other = n2 if first == n1 else n1
            return mcq("아침에 %s %s에, %s %s에 일어났어요. 누가 더 먼저 일어났을까요?" % (josa(n1, "은/는"), t1, josa(n2, "은/는"), t2), first,
                       [other, "똑같이 일어났어요", "알 수 없어요"],
                       "%s %s보다 이른 시각이에요. <b>%s</b>" % (josa(t1 if first == n1 else t2, "이/가"), t2 if first == n1 else t1, first))
        if how == "order":
            ts = R.sample([(h, m) for h in range(1, 12) for m in (0, 30)], 4)
            early = min(ts)
            fmt = lambda t: "%d시%s" % (t[0], " 30분" if t[1] else "")
            return mcq("다음 시각 중 가장 이른 시각은 무엇일까요? (모두 오후)<br>%s" % ", ".join(fmt(t) for t in ts), fmt(early), [fmt(t) for t in ts if t != early],
                    "'시'를 먼저 비교하고, 같으면 '분'을 비교해요. <b>%s</b>" % fmt(early))
        act, h, nx = R.choice(DAY)
        m = R.choice([0, 30])
        tt = "%d시%s" % (h, " 30분" if m else "")
        return mcq("시우는 %s에 %s. 이 시각에 시계의 긴바늘은 어디를 가리킬까요?" % (tt, act), "6" if m else "12", ["12" if m else "6", str(h), str(nx)],
                   "%s이면 긴바늘은 <b>%s</b>를 가리켜요." % (tt, "6" if m else "12"))
    return mk


# ------------------------------------------------------------------ 규칙 찾기
PATS = ["AB", "AAB", "ABB", "ABC", "AABB", "ABCC"]


def pat_obj():
    def mk():
        p = R.choice(PATS)
        ks = R.sample(KINDS, len(set(p)))
        mp = {ch: ks[i] for i, ch in enumerate(sorted(set(p)))}
        L = len(p) * 2 + R.randint(0, len(p) - 1)
        seq = [mp[p[i % len(p)]] for i in range(L + 1)]
        ans = seq[-1]
        pic = ko(pattern_svg([("obj", k) for k in seq[:-1]], 1), "규칙에 따라 놓은 물건")
        return mcq("규칙에 따라 놓았어요. ?에 알맞은 것은 무엇일까요?%s" % pic, nm(ans), [nm(k) for k in ks if k != ans] + [nm(k) for k in KINDS if k not in ks][:2],
                   "%s 반복되는 규칙이에요. <b>%s</b>" % (josa(", ".join(nm(mp[c]) for c in p), "이/가"), nm(ans)))
    return mk


def pat_color():
    def mk():
        p = R.choice(PATS)
        cs = R.sample(list(COL), len(set(p)))
        mp = {ch: cs[i] for i, ch in enumerate(sorted(set(p)))}
        shp = R.choice(["circle", "triangle", "square"])
        L = len(p) * 2 + R.randint(0, len(p) - 1)
        seq = [mp[p[i % len(p)]] for i in range(L + 1)]
        ans = seq[-1]
        pic = ko(pattern_svg([("shape", shp, c) for c in seq[:-1]], 1), "규칙에 따라 색칠한 모양")
        return mcq("규칙에 따라 색칠했어요. ?에는 어떤 색을 칠해야 할까요?%s" % pic, COL[ans], [COL[c] for c in COL if c != ans],
                   "%s 반복돼요. <b>%s</b>" % (josa(", ".join(COL[mp[c]] for c in p), "이/가"), COL[ans]))
    return mk


def pat_num():
    def mk():
        how = R.choice(["step", "step", "rep"])
        if how == "step":
            st = R.choice([1, 2, 5, 10, 3])
            down = R.random() < 0.3
            a = R.randint(1, 100 - st * 5)
            sq = [a + st * i for i in range(6)]
            if down:
                sq = sq[::-1]
            p = R.randint(3, 5)
            ans = sq[p]
            shown = [x if i != p else "?" for i, x in enumerate(sq[:p + 1])]
            return mcq("규칙에 따라 수를 늘어놓았어요. ?에 알맞은 수는 무엇일까요?%s" % cards(shown, 56), str(ans),
                       [str(x) for x in (ans + 1, ans - 1, ans + st, ans - st, ans + 10) if 0 < x <= 100 and x != ans],
                       "%d씩 %s지는 규칙이에요. <b>%d</b>" % (st, "작아" if down else "커", ans))
        p = R.choice(["AB", "ABC", "AAB", "ABB"])
        ns = R.sample(range(1, 10), len(set(p)))
        mp = {ch: ns[i] for i, ch in enumerate(sorted(set(p)))}
        L = len(p) * 2 + R.randint(0, len(p) - 1)
        seq = [mp[p[i % len(p)]] for i in range(L + 1)]
        ans = seq[-1]
        return mcq("규칙에 따라 수를 늘어놓았어요. ?에 알맞은 수는 무엇일까요?%s" % cards(seq[:-1] + ["?"], 46), str(ans), [str(x) for x in ns if x != ans] + [str(ans + 1)],
                   "%s 반복돼요. <b>%d</b>" % (josa(", ".join(str(mp[c]) for c in p), "이/가"), ans))
    return mk


def pat_rule():
    def mk():
        st = R.choice([2, 5, 10, 3, 4])
        a = R.randint(1, 30)
        down = R.random() < 0.3
        sq = [a + st * i for i in range(5)]
        if down:
            sq = sq[::-1]
        ok = "%d씩 %s져요" % (st, "작아" if down else "커")
        return mcq("수의 규칙을 바르게 말한 것은 무엇일까요?<br><b>%s</b>" % ", ".join(map(str, sq)), ok,
                   ["%d씩 %s져요" % (st, "커" if down else "작아"), "%d씩 %s져요" % (st + 1, "작아" if down else "커"), "%d씩 %s져요" % (st - 1 if st > 2 else st + 2, "작아" if down else "커")],
                   "%d, %d처럼 %d씩 %s져요." % (sq[0], sq[1], st, "작아" if down else "커"))
    return mk


def pat_chart():
    def mk():
        how = R.choice(["down", "right", "diag", "q"])
        if how == "q":
            r0, c0 = R.randint(0, 6), R.randint(0, 6)
            tl = r0 * 10 + c0 + 1
            tr, tc = R.randint(1, 2), R.randint(0, 3)
            ans = tl + 10 * tr + tc
            return mcq("수 배열표의 일부예요. ?에 알맞은 수는 무엇일까요?%s" % chart(tl, 3, 4, (tr, tc)), str(ans),
                       [str(x) for x in (ans + 1, ans - 1, ans + 10, ans - 10) if 0 < x <= 100], "→ 방향은 1씩, ↓ 방향은 10씩 커져요. <b>%d</b>" % ans)
        a = R.randint(1, 50)
        d = {"down": 10, "right": 1, "diag": 11}[how]
        sq = [a + d * i for i in range(4)]
        if sq[-1] > 100 or (how in ("right", "diag") and (a - 1) % 10 + 3 >= 10):
            return None
        word = {"down": "↓ 방향(아래로)", "right": "→ 방향(오른쪽으로)", "diag": "↘ 방향(오른쪽 아래로)"}[how]
        return mcq("수 배열표에서 %s 수를 읽었어요: %s<br>몇씩 커지는 규칙일까요?" % (word, ", ".join(map(str, sq))), "%d씩" % d,
                   ["%d씩" % x for x in (1, 10, 11, 9, 2) if x != d], "%d, %d, …는 <b>%d씩</b> 커져요." % (sq[0], sq[1], d))
    return mk


def pat_code():
    """규칙을 수로・모양으로 나타내기"""
    SYM = {"circle": "○", "triangle": "△", "square": "□"}

    def mk():
        how = R.choice(["code", "nth"])
        p = R.choice(["AB", "AAB", "ABB", "ABC"])
        shp = R.sample(list(SYM), len(set(p)))
        mp = {ch: shp[i] for i, ch in enumerate(sorted(set(p)))}
        seq = [mp[p[i % len(p)]] for i in range(len(p) * 2)]
        if how == "code":
            nums = {s: i + 1 for i, s in enumerate(shp)}
            ok = ", ".join(str(nums[s]) for s in seq)
            q = "%s<br>%s 1, %s 2%s로 나타내면 어떻게 될까요?" % (" ".join(SYM[s] for s in seq), josa(SYM[shp[0]], "은/는"), josa(SYM[shp[1]], "은/는") if len(shp) > 1 else "",
                                                       (", %s 3" % josa(SYM[shp[2]], "은/는")) if len(shp) > 2 else "")
            q = q.replace("○은", "○는").replace("△은", "△는").replace("□은", "□는")
            bad = []
            for _ in range(10):
                b = list(ok.split(", "))
                i = R.randrange(len(b))
                b[i] = str((int(b[i]) % len(shp)) + 1)
                b = ", ".join(b)
                if b != ok and b not in bad:
                    bad.append(b)
            return mcq(q, ok, bad, "모양을 하나씩 수로 바꾸어요. <b>%s</b>" % ok)
        k = R.choice([8, 9, 10])
        ans = SYM[mp[p[(k - 1) % len(p)]]]
        return mcq("%s …<br>같은 규칙으로 계속 놓을 때 %s 모양은 무엇일까요?" % (" ".join(SYM[s] for s in seq), "<b>%s</b>" % ["", "", "", "", "", "", "", "", "여덟째", "아홉째", "열째"][k]),
                   ans + " 모양", [SYM[s] + " 모양" for s in SYM if SYM[s] != ans] + ["공 모양"],
                   "%s 반복돼요. 이어서 놓아 보면 %s는 <b>%s 모양</b>이에요." % (josa(" ".join(SYM[mp[c]] for c in p), "이/가"), ["", "", "", "", "", "", "", "", "여덟째", "아홉째", "열째"][k], ans))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "solid":
        return unit(G, "solid-shapes", 2, "[2수03-01]",
                    "교실 및 생활 주변에서 여러 가지 물건을 관찰하여 직육면체, 원기둥, 구의 모양을 찾고, 이를 이용하여 여러 가지 모양을 만들 수 있다.",
                    "상자 모양, 둥근 기둥 모양, 공 모양", "여러 가지 모양(입체)",
                    "초등 1학년 1학기 여러 가지 모양 학습지: 상자 모양·둥근 기둥 모양·공 모양 찾기, 생활 속 물건, 굴러가는 모양과 쌓을 수 있는 모양, 모양을 쌓아 만들기까지 100문제와 정답.",
                    "상자·둥근 기둥·공 모양", "평평한 부분, 둥근 부분, 뾰족한 부분을 살펴봐요.",
                    ["주사위나 휴지 상자처럼 평평한 부분과 뾰족한 부분이 있는 모양은 <b>상자 모양</b>이에요.",
                     "음료수 캔처럼 위아래는 평평하고 옆은 둥근 모양은 <b>둥근 기둥 모양</b>이에요.",
                     "축구공처럼 모든 부분이 둥근 모양은 <b>공 모양</b>이에요.",
                     "공 모양은 어느 쪽으로도 잘 굴러가고, 상자 모양은 잘 쌓을 수 있어요. 둥근 기둥 모양은 눕히면 굴러가고 세우면 쌓을 수 있어요."],
                    [("두루마리 휴지는 어떤 모양?", ["위아래는 평평하고 옆은 둥글어요."], "둥근 기둥 모양"),
                     ("가장 잘 굴러가는 모양", ["둥근 부분만 있는 모양을 찾아요."], "공 모양")],
                    [("색이나 크기가 다르면 다른 모양이라고 생각한다", "색, 크기와 상관없이 생김새로 나누어요."),
                     ("둥근 기둥 모양은 쌓을 수 없다고 생각한다", "세우면 평평한 부분끼리 쌓을 수 있어요."),
                     ("상자 모양도 잘 굴러간다고 생각한다", "평평한 부분만 있어서 굴러가지 않아요.")],
                    [("직육면체, 원기둥이라는 말을 써야 하나요?", "1학년에서는 상자 모양, 둥근 기둥 모양, 공 모양처럼 생활 속 말로 익혀요."),
                     ("집에서 어떻게 연습하나요?", "집 안의 물건을 모아 세 가지 모양으로 나누고, 굴리거나 쌓아 보세요.")],
                    [("모양 알아보기", [(sol_name(), 12), (sol_feature(), 8)]),
                     ("생활 속 물건", [(sol_obj(), 20)]),
                     ("모양의 특징", [(sol_fact(), 10), (sol_odd(), 10)]),
                     ("같은 모양 세기", [(sol_count(), 20)]),
                     ("모양으로 만들기", [(sol_built(), 20)])], 82102)
    if which == "compare":
        return unit(G, "comparing-length-weight-area-and-capacity", 4, "[2수03-06]",
                    "구체물의 길이, 들이, 무게, 넓이를 비교하여 각각 ‘길다, 짧다’, ‘많다, 적다’, ‘무겁다, 가볍다’, ‘넓다, 좁다’ 등을 구별하여 말할 수 있다.",
                    "길이·높이·무게·넓이·들이 비교하기", "비교하기",
                    "초등 1학년 1학기 비교하기 학습지: 길다·짧다, 높다·낮다, 무겁다·가볍다, 넓다·좁다, 많다·적다를 그림과 생활 장면으로 비교하는 100문제와 정답.",
                    "한쪽 끝을 맞추어 비교해요", "길다·짧다, 무겁다·가볍다, 넓다·좁다, 많다·적다",
                    ["길이를 비교할 때는 <b>한쪽 끝을 맞추고</b> 다른 쪽 끝을 봐요. 더 많이 나온 쪽이 더 <b>길어요</b>.",
                     "높이는 아래쪽 끝을 맞추고 위쪽을 비교해요. 더 위에 있으면 더 <b>높아요</b>.",
                     "양팔저울에서는 아래로 내려간 쪽이 더 <b>무거워요</b>.",
                     "넓이는 겹쳐 보아 남는 쪽이 더 <b>넓어요</b>. 들이는 그릇에 담긴 물의 양으로 비교해요. 같은 그릇이면 물의 높이가 높은 쪽이 더 <b>많아요</b>."],
                    [("연필과 크레파스 중 더 긴 것", ["왼쪽 끝을 맞추어 놓아요.", "오른쪽 끝이 더 나온 것을 찾아요."], "더 많이 나온 것"),
                     ("수박과 귤 중 더 무거운 것", ["손에 들어 보거나 저울에 올려요."], "수박")],
                    [("끝을 맞추지 않고 길이를 비교한다", "한쪽 끝을 맞추고 비교해요."),
                     ("저울에서 올라간 쪽이 무겁다고 한다", "내려간 쪽이 무거워요."),
                     ("물 높이만 보고 크기가 다른 그릇을 비교한다", "그릇의 크기도 함께 봐요.")],
                    [("비교하기는 언제 배우나요?", "초등 1학년 1학기 「비교하기」 단원에서 배워요."),
                     ("단위(cm)도 배우나요?", "1학년에서는 직접 비교해요. cm, m는 2학년에서 배워요.")],
                    [("길이 비교", [(cmp_len(), 12), (cmp_len_offset(), 8)]),
                     ("높이 비교", [(cmp_tower(), 14), (cmp_words(("높이", "길이")), 6)]),
                     ("무게 비교", [(cmp_weight(), 10), (cmp_weight3(), 6), (cmp_words(("무게",)), 4)]),
                     ("넓이 비교", [(cmp_area(), 15), (cmp_words(("넓이",)), 5)]),
                     ("들이 비교", [(cmp_water(), 15), (cmp_words(("들이",)), 5)])], 82104)
    if which == "flat":
        return unit(G, "flat-shapes", 10, "[2수03-03]",
                    "교실 및 생활 주변에서 여러 가지 물건을 관찰하여 삼각형, 사각형, 원의 모양을 찾고, 이를 이용하여 여러 가지 모양을 만들 수 있다.",
                    "□ 모양, △ 모양, ○ 모양", "여러 가지 모양(평면)",
                    "초등 1학년 2학기 여러 가지 모양 학습지: □·△·○ 모양 찾기, 생활 속 물건, 본뜬 모양, 뾰족한 곳과 곧은 선, 모양 세기, 모양으로 꾸미기까지 100문제와 정답.",
                    "□ 4군데, △ 3군데, ○ 0군데", "뾰족한 곳과 곧은 선의 수로 모양을 구별해요.",
                    ["액자처럼 곧은 선 4개와 뾰족한 곳 4군데가 있는 모양은 <b>□ 모양</b>이에요. 길쭉해도 □ 모양이에요.",
                     "삼각자처럼 곧은 선 3개와 뾰족한 곳 3군데가 있는 모양은 <b>△ 모양</b>이에요.",
                     "동전처럼 둥근 선만 있고 뾰족한 곳이 없는 모양은 <b>○ 모양</b>이에요.",
                     "모양을 돌려 놓아도 모양은 바뀌지 않아요."],
                    [("시계는 어떤 모양?", ["뾰족한 곳이 없고 둥글어요."], "○ 모양"),
                     ("△ 모양의 뾰족한 곳", ["하나씩 세어요."], "3군데")],
                    [("거꾸로 놓인 △을 다른 모양이라고 한다", "돌려도 △ 모양이에요."),
                     ("길쭉한 □는 □ 모양이 아니라고 한다", "곧은 선 4개, 뾰족한 곳 4군데면 □ 모양이에요."),
                     ("○ 모양에도 뾰족한 곳이 있다고 한다", "○ 모양은 둥근 선만 있어요.")],
                    [("삼각형, 사각형이라는 말은 언제 배우나요?", "2학년 1학기 「여러 가지 도형」에서 삼각형, 사각형, 원을 배워요."),
                     ("집에서 어떻게 연습하나요?", "물건을 종이에 대고 본떠 보거나, 색종이를 잘라 모양을 만들어 보세요.")],
                    [("모양 알아보기", [(flat_name(), 20)]),
                     ("생활 속 모양", [(flat_obj(), 14), (flat_trace(), 6)]),
                     ("모양의 특징", [(flat_feature(), 20)]),
                     ("모양 세기", [(flat_count(), 20)]),
                     ("모양으로 꾸미기", [(flat_scene(), 20)])], 82110)
    if which == "time":
        return unit(G, "telling-time-hours-and-half-hours", 11, "[2수03-07]",
                    "시계를 보고 시각을 ‘몇 시 몇 분’까지 읽을 수 있다. (1학년: 몇 시, 몇 시 30분)",
                    "시계 보기: 몇 시, 몇 시 30분", "몇 시, 몇 시 30분",
                    "초등 1학년 2학기 시계 보기 학습지: 몇 시 읽기, 몇 시 30분 읽기, 짧은바늘과 긴바늘의 위치, 바늘 설명으로 시각 찾기, 생활 속 시각까지 100문제와 정답.",
                    "긴바늘 12는 몇 시, 6은 30분", "짧은바늘은 '시', 긴바늘은 '분'을 나타내요.",
                    ["짧은바늘이 3, 긴바늘이 12를 가리키면 <b>3시</b>예요.",
                     "긴바늘이 6을 가리키면 <b>30분</b>이에요. 짧은바늘이 3과 4 사이에 있으면 <b>3시 30분</b>이에요.",
                     "30분일 때 짧은바늘은 두 수 사이에 있어요. 이미 지난 수(작은 수)를 '시'로 읽어요."],
                    [("짧은바늘 8, 긴바늘 12", ["긴바늘이 12 → 정각"], "8시"),
                     ("짧은바늘이 5와 6 사이, 긴바늘 6", ["지난 수 5를 읽어요.", "긴바늘 6 → 30분"], "5시 30분")],
                    [("긴바늘이 가리키는 수를 '시'로 읽는다", "'시'는 짧은바늘로 읽어요."),
                     ("5시 30분을 6시 30분이라고 읽는다", "짧은바늘이 지나온 수 5를 읽어요."),
                     ("긴바늘이 6이면 6분이라고 읽는다", "긴바늘이 6이면 30분이에요.")],
                    [("몇 시 몇 분은 언제 배우나요?", "2학년 2학기 「시각과 시간」에서 몇 시 몇 분까지 읽어요."),
                     ("집에서 어떻게 연습하나요?", "바늘이 있는 시계를 걸어 두고 밥 먹는 시각, 자는 시각을 함께 읽어 보세요.")],
                    [("몇 시", [(t_hour(), 12), (t_desc("h"), 8)]),
                     ("몇 시 30분", [(t_half(), 12), (t_desc("m"), 8)]),
                     ("바늘의 위치", [(t_hands(), 20)]),
                     ("생활 속 시각", [(t_life(), 20)]),
                     ("섞어서 연습", [(t_hands(), 10), (t_life(), 10)])], 82111)
    if which == "pattern":
        return unit(G, "patterns", 12, "[2수02-01] [2수02-02]",
                    "물체, 무늬, 수 등의 배열에서 규칙을 찾아 여러 가지 방법으로 표현할 수 있다. 자신이 정한 규칙에 따라 물체, 무늬, 수 등을 배열할 수 있다.",
                    "규칙 찾기: 모양·색·수의 규칙", "규칙 찾기",
                    "초등 1학년 2학기 규칙 찾기 학습지: 물건과 색깔의 반복 규칙, 수의 규칙(2씩, 5씩, 10씩), 수 배열표의 규칙, 규칙을 수로 나타내기까지 100문제와 정답.",
                    "반복되는 부분을 찾아요", "모양·색·수에서 되풀이되는 부분이 규칙이에요.",
                    ["사과, 별, 사과, 별처럼 <b>되풀이되는 부분</b>을 찾으면 다음에 올 것을 알 수 있어요.",
                     "수는 몇씩 커지거나 작아지는지 살펴봐요. 2, 4, 6, 8은 <b>2씩 커지는</b> 규칙이에요.",
                     "수 배열표에서 → 방향은 1씩, ↓ 방향은 10씩 커져요.",
                     "규칙은 ○를 1, △를 2처럼 수로 바꾸어 나타낼 수도 있어요."],
                    [("빨강, 파랑, 파랑, 빨강, 파랑, 파랑, 다음은?", ["빨강, 파랑, 파랑이 반복돼요."], "빨강"),
                     ("5, 10, 15, 20, 다음 수", ["5씩 커져요."], "25")],
                    [("처음 두 개만 보고 규칙을 정한다", "끝까지 보고 되풀이되는 부분을 찾아요."),
                     ("10씩 커지는 수를 1씩 커진다고 한다", "앞뒤 수의 차이를 계산해 봐요."),
                     ("↓ 방향으로 1씩 커진다고 한다", "수 배열표의 아래쪽 수는 10 커요.")],
                    [("규칙 찾기는 왜 배우나요?", "규칙을 찾고 표현하는 힘은 곱셈구구와 나중의 함수 공부로 이어져요."),
                     ("집에서 어떻게 연습하나요?", "구슬 꿰기, 블록 늘어놓기로 아이가 규칙을 직접 만들고 설명하게 해 보세요.")],
                    [("물건의 규칙", [(pat_obj(), 20)]),
                     ("색깔의 규칙", [(pat_color(), 20)]),
                     ("수의 규칙", [(pat_num(), 14), (pat_rule(), 6)]),
                     ("수 배열표의 규칙", [(pat_chart(), 20)]),
                     ("규칙을 나타내기", [(pat_code(), 20)])], 82112)
    raise ValueError(which)
