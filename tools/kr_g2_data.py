# -*- coding: utf-8 -*-
"""
대한민국 초등 2학년 수학：자료와 가능성（2022 개정）の 2 単元
  sort : 분류하기（분류 기준、기준에 따라 세기、두 가지 기준、결과 말하기）[2수04-01]  2-1
  graph: 표와 그래프（자료를 표로、표 읽기、○ 그래프、그래프 그리기、편리한 점）[2수04-02] [2수04-03]  2-2
誤答は「사람마다 다른 기준（예쁜 것）으로 분류한다」「같은 것을 두 번 센다」「합계를 뺀 수와 헷갈린다」
「그래프의 칸 수와 ○의 수를 헷갈린다」「표와 그래프의 편리한 점을 바꾸어 말한다」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa
from kr_low import KINDS, nm, cw, ko, fig, near
import k_pics as K
from ws_common import svg_wrap, text, INK, GREEN, RED, FILL

R = random.Random(82209)
NM = Names(R)
G = "grade-2"
COLN = {"red": "빨간색", "blue": "파란색", "yellow": "노란색", "green": "초록색"}
SHN = {"circle": "○ 모양", "triangle": "△ 모양", "square": "□ 모양"}


# ------------------------------------------------------------------ 분류하기
CRIT = [("여러 가지 공을 분류하려고 해요. 분류 기준으로 알맞은 것은 무엇일까요?", "색깔", ["예쁜 것과 예쁘지 않은 것", "좋아하는 것과 싫어하는 것", "멋진 것과 멋지지 않은 것"]),
        ("동물 카드를 분류하려고 해요. 분류 기준으로 알맞은 것은 무엇일까요?", "다리의 수", ["귀여운 것", "무서운 것", "좋아하는 동물"]),
        ("블록을 분류하려고 해요. 분류 기준으로 알맞은 것은 무엇일까요?", "모양", ["갖고 싶은 것", "예쁜 것", "비싸 보이는 것"]),
        ("탈것 그림을 분류하려고 해요. 분류 기준으로 알맞은 것은 무엇일까요?", "바퀴의 수", ["빠르게 보이는 것", "멋있는 것", "타 보고 싶은 것"]),
        ("시장에서 산 것을 분류하려고 해요. 분류 기준으로 알맞지 <b>않은</b> 것은 무엇일까요?", "맛있는 것과 맛없는 것", ["과일과 채소", "색깔", "모양"]),
        ("옷장의 옷을 분류하려고 해요. 분류 기준으로 알맞지 <b>않은</b> 것은 무엇일까요?", "예쁜 옷과 예쁘지 않은 옷", ["옷의 종류", "옷의 색깔", "긴소매와 반소매"]),
        ("단추를 분류하려고 해요. 분류 기준으로 알맞지 <b>않은</b> 것은 무엇일까요?", "마음에 드는 것과 안 드는 것", ["구멍이 2개인 것과 4개인 것", "색깔", "모양"]),
        ("곤충과 새 카드를 분류할 때 누가 해도 결과가 같은 기준은 무엇일까요?", "날개가 있는 것과 없는 것", ["무서운 것과 무섭지 않은 것", "좋아하는 것과 싫어하는 것", "귀여운 것과 귀엽지 않은 것"])]


def s_crit():
    pool = CRIT[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        q, a, b = pool.pop()
        return mcq(q, a, b, "분류는 <b>누가 해도 결과가 같은 분명한 기준</b>으로 해야 해요. <b>%s</b>" % a)
    return mk


def s_kind_count():
    def mk():
        ks = R.sample(KINDS, 3)
        cnts = [(k, R.randint(1, 6)) for k in ks]
        pic = ko(K.mixed_svg(cnts, R.randint(1, 10 ** 6), 6, 4), "여러 가지 물건이 섞인 그림")
        k, v = R.choice(cnts)
        return mcq("종류에 따라 분류했어요. <b>%s</b> 몇 %s일까요?%s" % (josa(nm(k), "은/는"), cw(k), pic), "%d%s" % (v, cw(k)),
                   ["%d%s" % (x, cw(k)) for x in near(v, 0, 12) + [sum(c for _, c in cnts)]],
                   "%s만 표시하며 세면 <b>%d%s</b>예요." % (nm(k), v, cw(k)))
    return mk


def shape_items(n):
    return [(R.choice(list(SHN)), R.choice(list(COLN))) for _ in range(n)]


def s_shape_count():
    def mk():
        items = shape_items(R.randint(8, 12))
        pic = ko(K.shapes_mix_svg(items, R.randint(1, 10 ** 6), 5, 3), "여러 가지 색과 모양")
        if R.random() < 0.5:
            c = R.choice(list(COLN))
            v = sum(1 for _, x in items if x == c)
            return mcq("색깔에 따라 분류하면 <b>%s</b>은 몇 개일까요?%s" % (COLN[c], pic), "%d개" % v, ["%d개" % x for x in near(v, 0, 12)],
                       "%s만 세면 <b>%d개</b>예요." % (COLN[c], v))
        sh = R.choice(list(SHN))
        v = sum(1 for x, _ in items if x == sh)
        return mcq("모양에 따라 분류하면 <b>%s</b>은 몇 개일까요?%s" % (SHN[sh], pic), "%d개" % v, ["%d개" % x for x in near(v, 0, 12)],
                   "색깔과 상관없이 %s만 세면 <b>%d개</b>예요." % (SHN[sh], v))
    return mk


def s_two():
    def mk():
        items = shape_items(R.randint(9, 12))
        pic = ko(K.shapes_mix_svg(items, R.randint(1, 10 ** 6), 5, 3), "여러 가지 색과 모양")
        c = R.choice(list(COLN))
        sh = R.choice(list(SHN))
        v = sum(1 for x, y in items if x == sh and y == c)
        a = sum(1 for _, y in items if y == c)
        b = sum(1 for x, _ in items if x == sh)
        return mcq("<b>%s</b>이면서 <b>%s</b>인 것은 몇 개일까요?%s" % (COLN[c], SHN[sh], pic), "%d개" % v,
                   ["%d개" % x for x in (a, b, a + b, v + 1, v + 2) if x != v],
                   "%s 중에서 %s만 세면 <b>%d개</b>예요." % (COLN[c], SHN[sh], v))
    return mk


def s_result():
    def mk():
        ks = R.sample(["사과", "포도", "딸기", "귤", "수박", "바나나", "복숭아"], 4)
        vs = R.sample(range(2, 10), 4)
        tb = "<div class='sn-tw'><table class='sn-table'><tr><th>과일</th>%s</tr><tr><th>수(개)</th>%s</tr></table></div>" % (
            "".join("<td>%s</td>" % k for k in ks), "".join("<td>%d</td>" % v for v in vs))
        how = R.choice(["most", "least", "diff", "total"])
        if how in ("most", "least"):
            i = vs.index(max(vs) if how == "most" else min(vs))
            return mcq("과일을 종류에 따라 분류하여 세었어요. 가장 %s 과일은 무엇일까요?%s" % ("많은" if how == "most" else "적은", tb), ks[i], [k for k in ks if k != ks[i]],
                       "수가 가장 %s 것은 <b>%s</b>예요." % ("큰" if how == "most" else "작은", ks[i]))
        if how == "diff":
            i, j = R.sample(range(4), 2)
            if vs[i] < vs[j]:
                i, j = j, i
            d = vs[i] - vs[j]
            return mcq("분류하여 세었어요. %s %s보다 몇 개 더 많을까요?%s" % (josa(ks[i], "은/는"), ks[j], tb), "%d개" % d,
                       ["%d개" % x for x in (vs[i] + vs[j], d + 1, d - 1 if d > 1 else d + 2, vs[i])], "%d − %d = <b>%d개</b>" % (vs[i], vs[j], d))
        t = sum(vs)
        return mcq("분류한 과일은 모두 몇 개일까요?%s" % tb, "%d개" % t, ["%d개" % x for x in (t + 1, t - 1, max(vs), t + 10)],
                   "%s = <b>%d개</b>" % (" + ".join(map(str, vs)), t))
    return mk


LIFE = [("우유갑", "종이류"), ("신문지", "종이류"), ("공책", "종이류"), ("택배 상자", "종이류"), ("페트병", "플라스틱류"), ("요구르트병", "플라스틱류"),
        ("샴푸 통", "플라스틱류"), ("음료수 캔", "캔류"), ("참치 캔", "캔류"), ("통조림 캔", "캔류"), ("유리병", "유리병류"), ("잼 병", "유리병류"),
        ("주스 유리병", "유리병류"), ("과자 상자", "종이류"), ("플라스틱 컵", "플라스틱류")]
ANIM = [("닭", "다리 2개"), ("오리", "다리 2개"), ("참새", "다리 2개"), ("타조", "다리 2개"), ("강아지", "다리 4개"), ("고양이", "다리 4개"),
        ("소", "다리 4개"), ("토끼", "다리 4개"), ("뱀", "다리 없음"), ("물고기", "다리 없음"), ("지렁이", "다리 없음"), ("개구리", "다리 4개")]
RIDE = [("비행기", "하늘"), ("헬리콥터", "하늘"), ("열기구", "하늘"), ("배", "물"), ("잠수함", "물"), ("요트", "물"), ("버스", "땅"), ("기차", "땅"),
        ("자전거", "땅"), ("자동차", "땅")]


def s_life():
    pool = [(o, c, ["종이류", "플라스틱류", "캔류", "유리병류"], "분리배출할 때 %s 어느 곳에 넣어야 할까요?") for o, c in LIFE] + \
           [(o, c, ["다리 2개", "다리 4개", "다리 없음", "다리 6개"], "%s 다리의 수에 따라 분류하면 어디에 들어갈까요?") for o, c in ANIM] + \
           [(o, c, ["하늘", "물", "땅", "우주"], "%s 다니는 곳에 따라 분류하면 어디에 들어갈까요?") for o, c in RIDE]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        o, c, opts, q = pool.pop()
        return mcq(q % josa("<b>%s</b>" % o, "은/는"), c, [x for x in opts if x != c], "%s <b>%s</b>에 들어가요." % (josa(o, "은/는"), c))
    return mk


# ------------------------------------------------------------------ 표와 그래프
TOPIC = [("좋아하는 과일", ["사과", "포도", "딸기", "귤", "수박"]), ("좋아하는 계절", ["봄", "여름", "가을", "겨울"]),
         ("좋아하는 동물", ["강아지", "고양이", "토끼", "햄스터"]), ("좋아하는 색깔", ["빨강", "파랑", "노랑", "초록"]),
         ("좋아하는 운동", ["축구", "줄넘기", "수영", "피구"]), ("받고 싶은 선물", ["책", "인형", "게임기", "자전거"])]


def survey():
    tp, opts = R.choice(TOPIC)
    opts = opts[:4] if len(opts) > 4 else opts
    vs = [R.randint(1, 7) for _ in opts]
    return tp, opts, vs


def tab_html(tp, opts, vs, total=True, hide=None):
    head = "<tr><th>%s</th>%s%s</tr>" % (tp, "".join("<td>%s</td>" % o for o in opts), "<td>합계</td>" if total else "")
    row = "<tr><th>학생 수(명)</th>%s%s</tr>" % ("".join("<td>%s</td>" % ("□" if i == hide else v) for i, v in enumerate(vs)), "<td>%d</td>" % sum(vs) if total else "")
    return "<div class='sn-tw'><table class='sn-table'>%s%s</table></div>" % (head, row)


def graph_svg(opts, vs, rows=None, mark="○"):
    rows = rows or max(vs)
    cw_, ch = 70, 30
    lw = 30
    W = lw + cw_ * len(opts) + 12
    H = rows * ch + 60
    s = []
    for r in range(rows + 1):
        y = 10 + r * ch
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (lw, y, W - 12, y, "#9e9e9e"))
    for c in range(len(opts) + 1):
        x = lw + c * cw_
        s.append("<line x1='%d' y1='10' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, x, 10 + rows * ch, "#9e9e9e"))
    for r in range(rows):
        s.append(text(lw - 10, 10 + (rows - r) * ch - 9, str(r + 1), 13, weight=400))
    for c, (o, v) in enumerate(zip(opts, vs)):
        cx = lw + c * cw_ + cw_ / 2
        for k in range(v):
            cy = 10 + (rows - k) * ch - ch / 2
            s.append(text(cx, cy + 7, mark, 20, col=RED if mark != "○" else "#1f5fa8"))
        s.append(text(cx, 10 + rows * ch + 22, o, 15))
    return fig(svg_wrap(W, H, "".join(s), "○를 이용한 그래프").replace("<svg ", "<svg data-pf='lg' ", 1))


def g_make_table():
    def mk():
        tp, opts, vs = survey()
        names = []
        while len(names) < sum(vs):
            names.append(NM.next())
        ans = [o for o, v in zip(opts, vs) for _ in range(v)]
        R.shuffle(ans)
        lst = ", ".join(ans)
        i = R.randrange(len(opts))
        if R.random() < 0.6:
            return mcq("반 친구들의 %s 조사했어요.<br>%s<br>표로 나타낼 때 <b>%s</b>에 쓸 수는 무엇일까요?" % (josa(tp, "을/를"), lst, opts[i]), str(vs[i]),
                       [str(x) for x in near(vs[i], 0, 15) + [sum(vs)]], "%s만 표시하며 세면 <b>%d</b>이에요." % (opts[i], vs[i]))
        t = sum(vs)
        return mcq("반 친구들의 %s 조사했어요.<br>%s<br>조사한 학생은 모두 몇 명일까요?" % (josa(tp, "을/를"), lst), "%d명" % t, ["%d명" % x for x in near(t, 1) + [len(opts)]],
                   "하나씩 세면 <b>%d명</b>이에요. 표의 합계와 같아요." % t)
    return mk


def g_read_table():
    def mk():
        tp, opts, vs = survey()
        how = R.choice(["most", "least", "diff", "hide", "total"])
        if how == "hide":
            i = R.randrange(len(opts))
            return mcq("%s 조사하여 표로 나타냈어요. □에 알맞은 수는 무엇일까요?%s" % (josa(tp, "을/를"), tab_html(tp, opts, vs, True, i)), str(vs[i]),
                       [str(x) for x in (sum(vs) - vs[i], vs[i] + 1, vs[i] - 1 if vs[i] > 1 else vs[i] + 2, sum(vs))],
                       "합계에서 나머지를 빼요. %d − (%s) = <b>%d</b>" % (sum(vs), " + ".join(str(v) for j, v in enumerate(vs) if j != i), vs[i]))
        tb = tab_html(tp, opts, vs)
        if how in ("most", "least"):
            m = max(vs) if how == "most" else min(vs)
            if vs.count(m) > 1:
                return None
            i = vs.index(m)
            return mcq("표를 보고 답해요. 가장 %s 학생이 좋아하는 것은 무엇일까요?%s" % ("많은" if how == "most" else "적은", tb), opts[i], [o for o in opts if o != opts[i]],
                       "학생 수가 가장 %s 것: <b>%s</b>(%d명)" % ("많은" if how == "most" else "적은", opts[i], m))
        if how == "diff":
            i, j = R.sample(range(len(opts)), 2)
            if vs[i] == vs[j]:
                return None
            if vs[i] < vs[j]:
                i, j = j, i
            d = vs[i] - vs[j]
            return mcq("%s 좋아하는 학생은 %s 좋아하는 학생보다 몇 명 더 많을까요?%s" % (josa(opts[i], "을/를"), josa(opts[j], "을/를"), tb), "%d명" % d,
                       ["%d명" % x for x in (vs[i] + vs[j], d + 1, d - 1 if d > 1 else d + 2, vs[i])], "%d − %d = <b>%d명</b>" % (vs[i], vs[j], d))
        t = sum(vs)
        return mcq("조사한 학생은 모두 몇 명일까요?%s" % tab_html(tp, opts, vs, False), "%d명" % t, ["%d명" % x for x in (t + 1, t - 1, max(vs), len(opts))],
                   "%s = <b>%d명</b>" % (" + ".join(map(str, vs)), t))
    return mk


def g_read_graph():
    def mk():
        tp, opts, vs = survey()
        how = R.choice(["val", "most", "diff", "more_than"])
        pic = graph_svg(opts, vs)
        if how == "val":
            i = R.randrange(len(opts))
            return mcq("%s 조사하여 ○ 그래프로 나타냈어요. %s 좋아하는 학생은 몇 명일까요?%s" % (josa(tp, "을/를"), josa(opts[i], "을/를"), pic), "%d명" % vs[i],
                       ["%d명" % x for x in near(vs[i], 0, 10) + [sum(vs)]], "%s 칸의 ○를 세면 <b>%d명</b>이에요." % (opts[i], vs[i]))
        if how == "most":
            m = max(vs)
            if vs.count(m) > 1:
                return None
            i = vs.index(m)
            return mcq("그래프를 보고 답해요. 가장 많은 학생이 좋아하는 것은 무엇일까요?%s" % pic, opts[i], [o for o in opts if o != opts[i]],
                       "○가 가장 높이 올라간 것은 <b>%s</b>예요." % opts[i])
        if how == "diff":
            i, j = R.sample(range(len(opts)), 2)
            if vs[i] <= vs[j]:
                return None
            d = vs[i] - vs[j]
            return mcq("그래프에서 %s %s보다 몇 명 더 많이 좋아할까요?%s" % (josa(opts[i], "을/를"), opts[j], pic), "%d명" % d,
                       ["%d명" % x for x in (vs[i] + vs[j], d + 1, d - 1 if d > 1 else d + 2, vs[i])], "○의 수를 비교해요. %d − %d = <b>%d명</b>" % (vs[i], vs[j], d))
        k = R.randint(2, 5)
        c = sum(1 for v in vs if v > k)
        return mcq("그래프에서 좋아하는 학생이 <b>%d명보다 많은</b> 것은 모두 몇 가지일까요?%s" % (k, pic), "%d가지" % c,
                   ["%d가지" % x for x in (0, 1, 2, 3, 4) if x != c], "○가 %d개보다 많은 것을 세면 <b>%d가지</b>예요." % (k, c))
    return mk


def g_draw():
    def mk():
        tp, opts, vs = survey()
        how = R.choice(["rows", "marks", "fix", "rows"])
        tb = tab_html(tp, opts, vs)
        if how == "rows":
            m = max(vs)
            return mcq("표를 ○ 그래프로 나타내려고 해요. 세로 칸은 적어도 몇 칸이어야 할까요?%s" % tb, "%d칸" % m, ["%d칸" % x for x in (sum(vs), len(opts), m - 1, m + 2) if x != m],
                   "가장 많은 수 %d명까지 나타낼 수 있어야 해요. <b>%d칸</b>" % (m, m))
        if how == "marks":
            i = R.randrange(len(opts))
            return mcq("표를 ○ 그래프로 나타낼 때 <b>%s</b> 칸에는 ○를 몇 개 그려야 할까요?%s" % (opts[i], tb), "%d개" % vs[i], ["%d개" % x for x in near(vs[i], 0, 10) + [sum(vs)]],
                       "학생 수만큼 ○를 그려요. <b>%d개</b>" % vs[i])
        F = [("○ 그래프를 그릴 때 ○는 어떻게 그려야 할까요?", "아래에서 위로 빈칸 없이 그려요", ["위에서 아래로 그려요", "띄엄띄엄 그려요", "아무 칸에나 그려요"]),
             ("○ 그래프에서 ○ 한 개는 무엇을 나타낼까요? (학생 수를 조사했을 때)", "학생 1명", ["학생 2명", "과일 1개", "합계"]),
             ("그래프를 그리기 전에 먼저 해야 할 일은 무엇일까요?", "자료를 조사하여 표로 정리해요", ["○를 아무렇게나 그려요", "제목만 써요", "가장 많은 것을 지워요"]),
             ("그래프의 가로에 과일 이름을 쓰면 세로에는 무엇을 쓸까요?", "학생 수", ["과일 이름", "합계만", "날짜"])]
        q, a, b = R.choice(F)
        return mcq(q, a, b, "<b>%s</b>" % a)
    return mk


def g_good():
    F = [("조사한 학생이 <b>모두 몇 명</b>인지 알아보기 편리한 것은 무엇일까요?", "표", ["그래프", "조사한 자료", "그림"], "표에는 합계가 있어서 전체 수를 알기 편리해요. <b>표</b>"),
         ("<b>가장 많은 것</b>을 한눈에 알아보기 편리한 것은 무엇일까요?", "그래프", ["표", "조사한 자료", "글"], "○의 높이를 비교하면 한눈에 알 수 있어요. <b>그래프</b>"),
         ("<b>누가 무엇을 좋아하는지</b> 알 수 있는 것은 무엇일까요?", "조사한 자료", ["표", "그래프", "합계"], "이름과 답이 함께 있는 <b>조사한 자료</b>에서 알 수 있어요."),
         ("각각의 수를 정확한 수로 바로 알기 편리한 것은 무엇일까요?", "표", ["그래프", "조사한 자료", "그림"], "표에는 수가 적혀 있어요. <b>표</b>"),
         ("많고 적음을 비교하기 편리한 것은 무엇일까요?", "그래프", ["표", "조사한 자료", "합계"], "그래프는 ○의 높이로 비교할 수 있어요. <b>그래프</b>")]
    pool = F[:]

    def mk():
        if pool:
            return mcq(*pool.pop(0))
        tp, opts, vs = survey()
        srt = sorted(zip(vs, opts), reverse=True)
        if len(set(vs)) < len(vs):
            return None
        ok = ", ".join(o for _, o in srt)
        bad = [", ".join(o for _, o in srt[::-1]), ", ".join(opts), ", ".join(o for _, o in srt[1:] + srt[:1])]
        return mcq("그래프를 보고 많이 좋아하는 것부터 차례로 쓴 것은 무엇일까요?%s" % graph_svg(opts, vs), ok, [b for b in bad if b != ok],
                   "○가 많은 것부터 쓰면 <b>%s</b>예요." % ok)
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "sort":
        return unit(G, "sorting", 9, "[2수04-01]",
                    "여러 가지 사물을 정해진 기준 또는 자신이 정한 기준으로 분류하여 개수를 세어 보고, 기준에 따른 결과를 말할 수 있다.",
                    "분류하기: 기준을 정해 나누고 세기", "분류하기",
                    "초등 2학년 1학기 분류하기 학습지: 분명한 분류 기준, 종류·색깔·모양에 따라 분류하고 세기, 두 가지 기준, 분류한 결과 말하기, 분리배출까지 100문제와 정답.",
                    "누가 해도 같은 기준으로 나눠요", "분류한 다음 세어 보면 많고 적음을 알 수 있어요.",
                    ["'예쁜 것'처럼 사람마다 생각이 다른 기준은 알맞지 않아요. <b>색깔, 모양, 종류</b>처럼 누가 해도 같은 기준으로 분류해요.",
                     "분류한 것은 하나씩 표시하며 세어야 빠뜨리거나 두 번 세지 않아요.",
                     "두 가지 기준(색깔과 모양)으로 나누면 '빨간색이면서 △ 모양'처럼 더 자세히 분류할 수 있어요.",
                     "분류한 결과를 보면 어느 것이 가장 많은지, 몇 개 더 많은지 알 수 있어요."],
                    [("단추를 구멍 수로 분류", ["구멍 2개, 4개로 나누어요."], "누가 해도 같은 결과"),
                     ("빨간색 △ 찾기", ["빨간색만 고른 뒤 그중 △를 세요."], "두 가지 기준")],
                    [("'좋아하는 것'으로 분류한다", "분명한 기준(색깔, 모양, 종류)으로 분류해요."),
                     ("같은 것을 두 번 센다", "센 것에 ○나 ✓ 표시를 해요."),
                     ("빨간색 □를 셀 때 빨간색 전체를 센다", "두 기준에 모두 맞는 것만 세요.")],
                    [("분류하기는 왜 배우나요?", "자료를 정리하는 첫 단계예요. 2학기에 배우는 표와 그래프로 이어져요."),
                     ("집에서 어떻게 연습하나요?", "장난감 정리, 빨래 개기, 분리배출을 함께 하며 기준을 정해 나누어 보세요.")],
                    [("분류 기준", [(s_crit(), 8), (s_life(), 12)]),
                     ("종류에 따라 분류하기", [(s_kind_count(), 20)]),
                     ("색깔과 모양으로 분류하기", [(s_shape_count(), 20)]),
                     ("두 가지 기준", [(s_two(), 20)]),
                     ("분류한 결과 말하기", [(s_result(), 14), (s_life(), 6)])], 82209)
    if which == "graph":
        return unit(G, "tables-and-graphs", 16, "[2수04-02] [2수04-03]",
                    "자료를 분류하여 표로 나타내고, 자료를 표로 나타내면 편리한 점을 말할 수 있다. 자료를 분류하여 ○, ×, / 등을 이용한 그래프로 나타내고, 자료를 그래프로 나타내면 편리한 점을 말할 수 있다.",
                    "표와 그래프: 자료를 정리하고 읽기", "표와 그래프",
                    "초등 2학년 2학기 표와 그래프 학습지: 조사한 자료를 표로 나타내기, 표 읽기, ○ 그래프 읽기, 그래프 그리기, 표와 그래프의 편리한 점까지 100문제와 정답.",
                    "표는 수와 합계, 그래프는 한눈에", "○는 아래에서 위로 빈칸 없이 그려요.",
                    ["조사한 자료를 종류별로 세어 <b>표</b>로 나타내면 각각의 수와 <b>합계</b>를 알기 쉬워요.",
                     "표를 ○, ×, / 등으로 나타낸 것을 <b>그래프</b>라고 해요. ○는 아래에서 위로 한 칸에 하나씩 빈칸 없이 그려요.",
                     "그래프는 가장 많은 것과 가장 적은 것을 <b>한눈에</b> 비교할 수 있어요.",
                     "그래프의 세로 칸은 가장 큰 수만큼은 있어야 해요."],
                    [("사과 5명, 포도 3명, 딸기 4명의 합계", ["5 + 3 + 4"], "12명"),
                     ("○가 가장 높은 것", ["○의 수가 가장 많아요."], "가장 많이 좋아하는 것")],
                    [("합계에 종류의 수를 쓴다", "합계는 학생 수를 모두 더한 수예요."),
                     ("○를 위에서부터 그린다", "아래에서 위로 빈칸 없이 그려요."),
                     ("표와 그래프의 편리한 점을 바꾸어 말한다", "전체 수는 표, 많고 적음은 그래프가 편해요.")],
                    [("막대그래프는 언제 배우나요?", "3학년에서 그림그래프, 4학년에서 막대그래프와 꺾은선그래프를 배워요."),
                     ("집에서 어떻게 연습하나요?", "가족이 좋아하는 음식을 조사해 표와 ○ 그래프로 함께 그려 보세요.")],
                    [("자료를 표로 나타내기", [(g_make_table(), 20)]),
                     ("표 읽기", [(g_read_table(), 20)]),
                     ("그래프 읽기", [(g_read_graph(), 20)]),
                     ("그래프 그리기", [(g_draw(), 20)]),
                     ("표와 그래프의 편리한 점", [(g_good(), 12), (g_read_graph(), 8)])], 82216)
    raise ValueError(which)
