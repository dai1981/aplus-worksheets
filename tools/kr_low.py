# -*- coding: utf-8 -*-
"""
대한민국 초등 1・2학년（2022 개정）の共通部品。
・k_pics の絵を韓国語の aria-label で使う（A〜D の文字は 가 나 다 라 に）
・고유어（하나・둘…아흔아홉）と 한자어（일・이…）の読み、순서（첫째…）
・とても短い文。答えも誤答もすべてコードで計算する
"""
import re
import random
import k_pics as K
from ws_common import fig, svg_wrap, text, line, INK, GREEN, RED, FILL, BLUE
from kr_common import mcq, num, josa, read_num, Names, clock   # noqa: F401

KO = {"apple": ("사과", "개"), "star": ("별", "개"), "ball": ("공", "개"), "button": ("단추", "개"), "fish": ("물고기", "마리"),
      "flower": ("꽃", "송이"), "heart": ("하트", "개"), "duck": ("오리", "마리"), "cup": ("컵", "개"), "bug": ("무당벌레", "마리")}
KINDS = list(KO)
LET = "가나다라마"

ONES = ["", "하나", "둘", "셋", "넷", "다섯", "여섯", "일곱", "여덟", "아홉"]
TENS = ["", "열", "스물", "서른", "마흔", "쉰", "예순", "일흔", "여든", "아흔"]
ORD = ["", "첫째", "둘째", "셋째", "넷째", "다섯째", "여섯째", "일곱째", "여덟째", "아홉째", "열째"]
# 数え方（개・마리 の前）：한 개、두 개、세 개、네 개、스무 개
ONES_C = ["", "한", "두", "세", "네", "다섯", "여섯", "일곱", "여덟", "아홉"]


def native(n):
    """1〜99 の고유어：37 → 서른일곱"""
    assert 1 <= n <= 99
    return TENS[n // 10] + ONES[n % 10]


def native_c(n):
    """数える時の形：1 한, 20 스무, 21 스물한"""
    if n == 20:
        return "스무"
    return TENS[n // 10] + ONES_C[n % 10]


def sino(n):
    return read_num(n)


def nm(kind):
    return KO[kind][0]


def cw(kind):
    return KO[kind][1]


def cnt(kind, n):
    """사과 5개、오리 3마리"""
    return "%s %d%s" % (nm(kind), n, cw(kind))


def ko(svg, label):
    """aria-label を韓国語に、図の中の A B C D を 가 나 다 라 に"""
    svg = re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1)
    for a, b in zip("ABCD", LET):
        svg = svg.replace(">%s</text>" % a, ">%s</text>" % b)
    return fig(svg)


def lg(f):
    return f.replace("<svg ", "<svg data-pf='lg' ", 1)


# ------------------------------------------------------------------ 絵
def row(n, kind, per_row=10):
    return ko(K.row_svg(n, kind, per_row), cnt(kind, n))


def scatter(n, kind, seed):
    return ko(K.scatter_svg(n, kind, seed), "%s 여러 %s" % (nm(kind), cw(kind)))


def tenframe(n, frames=None, kind="dot"):
    return ko(K.tenframe_svg(n, frames, kind), "10칸 상자")


def rods(t, o):
    return ko(K.rods_svg(t, o), "10개씩 묶음 %d개와 낱개 %d개" % (t, o))


def dice(vals):
    return ko(K.dice_svg(vals), "주사위")


def bond(whole, a, b):
    return ko(K.bond_svg(whole, a, b), "모으기와 가르기")


def two(a, ka, b, kb=None, word="+"):
    return ko(K.two_groups_svg(a, ka, b, kb, word), "%s와 %s" % (cnt(ka, a), cnt(kb or ka, b)))


def crossed(n, kind, k):
    return ko(K.crossed_row_svg(n, kind, k), "%s 중 %d%s를 지운 그림" % (cnt(kind, n), k, cw(kind)))


def boxed(n, kind):
    return ko(K.box_svg(n, kind), "%s와 상자" % cnt(kind, n))


def hops(start, h, lo=0, hi=10, sp=40):
    return ko(K.hop_line_svg(start, h, lo, hi, sp), "수직선 뛰어 세기")


def cards(items, w=50, h=56):
    return ko(K.cards_svg([str(x) for x in items], w, h), "수 카드")


def chart(tl, nr, nc, target=None, hide=()):
    return ko(K.chart_svg(tl, nr, nc, target, hide), "수 배열표")


def pencils(lengths, labels=None, unit=34, offsets=None):
    return ko(K.pencils_svg(lengths, labels or list(LET[:len(lengths)]), unit, None, offsets), "연필의 길이 비교")


def towers(hs, labels=None):
    return ko(K.towers_svg(hs, labels or list(LET[:len(hs)])), "쌓은 상자의 높이 비교")


def scale(left, right, tilt):
    return ko(K.balance_svg(left, right, tilt), "양팔저울")


def glasses(items):
    from f_common import glasses_svg
    return ko(glasses_svg(items), "그릇에 담긴 물")


def kinds_row(kinds):
    return ko(K.kinds_row_svg(kinds), "여러 가지 물건이 한 줄로")


def mixed(counts, seed, cols=6, rows=4):
    return ko(K.mixed_svg(counts, seed, cols, rows), "여러 가지 물건이 섞인 그림")


def towers_plain(hs):
    return ko(K.towers_svg(hs, list(LET[:len(hs)])), "쌓기나무")


# ------------------------------------------------------------------ 選択肢の部品
def near(v, lo=0, hi=None, ds=(1, -1, 2, -2, 10, -10, 3)):
    out = []
    for d in ds:
        w = v + d
        if w >= lo and (hi is None or w <= hi) and w != v:
            out.append(w)
    return out


def unitn(n, u="개"):
    return "%d%s" % (n, u)


def rnd_kinds(R, k=4):
    ks = KINDS[:]
    R.shuffle(ks)
    return ks[:k]


# ------------------------------------------------------------------ 名詞の後の助詞を直す（꽃는 → 꽃은）
import kr_common as _KC
_NOUNS = "사과|별|공|단추|물고기|꽃|하트|오리|컵|무당벌레|구슬|딱지|사탕|연필|색종이|풍선|공책|귤|딸기|쿠키|책|우유"
_PAIR = {"은": "은/는", "는": "은/는", "이": "이/가", "가": "이/가", "을": "을/를", "를": "을/를", "과": "과/와", "와": "과/와"}


def fix_noun_josa(s):
    return re.sub(r"(?<![가-힣])(%s)(은|는|이|가|을|를|과|와)(?=[\s,.?!<]|$)" % _NOUNS,
                  lambda m: josa(m.group(1), _PAIR[m.group(2)]), s)


_old_tidy = _KC.tidy


def _bat(c):
    o = ord(c)
    return 0xAC00 <= o <= 0xD7A3 and (o - 0xAC00) % 28 != 0


def fix_copula(s):
    """받침 뒤의 예요 → 이에요、라고 → 이라고（컵예요 → 컵이에요）"""
    s = re.sub(r"([가-힣])(</b>)?(예요|라고)", lambda m: m.group(1) + (m.group(2) or "") +
               ({"예요": "이에요", "라고": "이라고"}[m.group(3)] if _bat(m.group(1)) else m.group(3)), s)
    s = re.sub(r"([가-힣])(</b>)?이(에요|라고)", lambda m: m.group(0) if _bat(m.group(1)) or m.group(1) in "아" else
               m.group(1) + (m.group(2) or "") + ("예요" if m.group(3) == "에요" else "라고"), s)
    return s


def fix_counter_josa(s):
    """3장를 → 3장을、7권를 → 7권을（数＋助数詞の後）"""
    return re.sub(r"(\d(?:</b>)?\s?|몇 )(장|권|명|개|마리|자루|송이|살|번|칸|층|군데|묶음|배|씩|원|분|시간|일|주일|개월|년|시|cm|m)(</b>)?(을|를|이|가|은|는|과|와|으로|로)(?=[\s,.?!<)]|$)",
                  lambda m: m.group(1) + m.group(2) + (m.group(3) or "") + josa(m.group(2), _PAIR.get(m.group(4), "으로/로"))[len(m.group(2)):]
                  if m.group(2) not in ("cm", "m") else m.group(0), s)


def _tidy(s):
    return fix_copula(fix_counter_josa(fix_noun_josa(_old_tidy(s))))


_KC.tidy = _tidy


# ------------------------------------------------------------------ 2학년：수 모형・돈
def blocks(th, h, t, o, u=6):
    """수 모형：천 모형（큰 정육면체）th、백 모형 h、십 모형 t、일 모형 o"""
    s = []
    x = 8
    H = 10 * u + 16
    for _ in range(th):
        a = 10 * u
        d = 4 * u
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#f7d774' stroke='%s' stroke-width='1.4'/>" % (x, 8 + d, a, a, INK))
        s.append("<polygon points='%d,%d %d,%d %d,%d %d,%d' fill='#fbe7a1' stroke='%s' stroke-width='1.4'/>" % (x, 8 + d, x + d, 8, x + a + d, 8, x + a, 8 + d, INK))
        s.append("<polygon points='%d,%d %d,%d %d,%d %d,%d' fill='#e9c24f' stroke='%s' stroke-width='1.4'/>" % (x + a, 8 + d, x + a + d, 8, x + a + d, 8 + a, x + a, 8 + a + d, INK))
        x += a + d + 10
        H = max(H, a + d + 16)
    for _ in range(h):
        s.append("<rect x='%d' y='8' width='%d' height='%d' fill='#f7d774' stroke='%s' stroke-width='1.2'/>" % (x, 10 * u, 10 * u, INK))
        for i in range(1, 10):
            s.append("<line x1='%d' y1='8' x2='%d' y2='%d' stroke='#c9a93a' stroke-width='0.6'/>" % (x + i * u, x + i * u, 8 + 10 * u))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#c9a93a' stroke-width='0.6'/>" % (x, 8 + i * u, x + 10 * u, 8 + i * u))
        x += 10 * u + 8
    for _ in range(t):
        s.append("<rect x='%d' y='8' width='%d' height='%d' fill='#7fb3e6' stroke='%s' stroke-width='1.2'/>" % (x, u, 10 * u, INK))
        for i in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#4f86bd' stroke-width='0.6'/>" % (x, 8 + i * u, x + u, 8 + i * u))
        x += u + 5
    x += 4
    for i in range(o):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#f4a3a3' stroke='%s' stroke-width='1.2'/>" % (x + (i % 3) * (u + 3), 8 + 10 * u - u - (i // 3) * (u + 3), u, u, INK))
    if o:
        x += 3 * (u + 3)
    return fig(svg_wrap(x + 8, H, "".join(s), "수 모형: 천 %d개, 백 %d개, 십 %d개, 일 %d개" % (th, h, t, o)))


COIN = {10: (17, "#e3b27a", "#8a5a1a"), 50: (19, "#d9dde0", "#6c7378"), 100: (21, "#d9dde0", "#6c7378"), 500: (24, "#e9e3d0", "#7a7460")}


def money(vals):
    """10원・50원・100원・500원 동전、1000원 지폐"""
    s = []
    x = 8
    for v in vals:
        if v in COIN:
            r, f, st = COIN[v]
            s.append("<circle cx='%.1f' cy='33' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x + r, r, f, st))
            s.append(text(x + r, 38, str(v), 13 if v < 100 else 12))
            x += 2 * r + 7
        else:
            s.append("<rect x='%d' y='8' width='92' height='50' rx='4' fill='#bcd9a8' stroke='%s' stroke-width='1.6'/>" % (x, INK))
            s.append(text(x + 46, 39, "%d원" % v, 16))
            x += 100
    return fig(svg_wrap(x, 66, "".join(s), "돈"))
