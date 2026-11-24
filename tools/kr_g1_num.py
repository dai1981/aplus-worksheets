# -*- coding: utf-8 -*-
"""
대한민국 초등 1학년 수학：수（2022 개정 [2수01-01]〜[2수01-03]）の 3 単元
  n9  : 9까지의 수           1-1
  n50 : 50까지의 수          1-1
  n100: 100까지의 수         1-2
誤答は「하나 더 세거나 빠뜨린다」「고유어와 한자어를 섞는다（삼 개）」「묶음과 낱개를 바꾼다（37 → 73）」
「몇째와 몇 개를 헷갈린다」「십의 자리를 보지 않고 일의 자리로 비교한다」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa
from kr_low import (KINDS, ORD, ONES, ONES_C, native, native_c, sino, nm, cw, cnt, row, scatter, tenframe, rods, bond,
                    crossed, cards, chart, kinds_row, ko, near)
import k_pics as K

R = random.Random(82101)
NM = Names(R)
G = "grade-1"


def seed():
    return R.randint(1, 10 ** 6)


# ------------------------------------------------------------------ 共通の問題
def count_pic(lo, hi):
    def mk():
        n, k = R.randint(lo, hi), R.choice(KINDS)
        pic = scatter(n, k, seed()) if n <= 16 and R.random() < 0.6 else row(n, k)
        return mcq("%s 몇 %s일까요?%s" % (josa(nm(k), "은/는"), cw(k), pic), "%d%s" % (n, cw(k)),
                   ["%d%s" % (w, cw(k)) for w in near(n, 1)],
                   "하나씩 빠뜨리지 않고 세어 보면 <b>%d%s</b>예요." % (n, cw(k)))
    return mk


def read_both(lo, hi):
    """수를 두 가지로 읽기：37 → 삼십칠, 서른일곱"""
    def mk():
        n = R.randint(lo, hi)
        ok = "%s, %s" % (sino(n), native(n))
        w = []
        if n >= 11 and n % 10:
            w.append("%s, %s" % (sino(n % 10 * 10 + n // 10), native(n % 10 * 10 + n // 10)) if n % 10 * 10 + n // 10 <= 99 else None)
        w += ["%s, %s" % (sino(n), native(n + 1 if n < 99 else n - 1)),
              "%s, %s" % (sino(n + 1 if n < 99 else n - 1), native(n)),
              "%s, %s" % (sino(n - 1), native(n - 1)) if n > 1 else None]
        return mcq("<b>%d</b>를 바르게 읽은 것은 무엇일까요?" % n, ok, w,
                   "%d은 <b>%s</b> 또는 <b>%s</b>라고 읽어요." % (n, sino(n), native(n)))
    return mk


def word_to_num(lo, hi):
    def mk():
        n = R.randint(lo, hi)
        wd = "'%s'" % R.choice([sino(n), native(n)])
        w = near(n, 1, 100)
        if n >= 11 and n % 10 and n % 10 * 10 + n // 10 <= 99:
            w.insert(0, n % 10 * 10 + n // 10)
        return mcq("%s 수로 쓰면 무엇일까요?" % josa(wd, "을/를"), str(n), [str(x) for x in w],
                   "%s <b>%d</b>이에요." % (josa(wd, "은/는"), n))
    return mk


def one_more_less(lo, hi, step=1):
    cap = 9 if hi <= 9 else 100

    def mk():
        n = R.randint(lo, hi)
        up = R.random() < 0.5
        a = n + step if up else n - step
        if a < 0 or a > 100:
            return None
        if step == 1:
            e = "수를 순서대로 셀 때 %d %s 수예요. <b>%d</b>" % (n, "바로 다음" if up else "바로 앞", a)
        else:
            e = "10 %s 수는 십의 자리 수가 1 %s져요. <b>%d</b>" % ("큰" if up else "작은", "커" if up else "작아", a)
        return mcq("<b>%d</b>보다 %d %s 수는 무엇일까요?" % (n, step, "큰" if up else "작은"), str(a),
                   [str(x) for x in (n - step if up else n + step, n, a + 1, a - 1, a + 10, a - 10) if 0 <= x <= cap], e)
    return mk


def seq_cards(lo, hi, step=1, length=5):
    cap = 9 if hi <= 9 else 100

    def mk():
        down = R.random() < 0.3
        st = R.randint(lo, hi - step * (length - 1))
        sq = list(range(st, st + step * length, step))
        if down:
            sq = sq[::-1]
        p = R.randint(1, length - 1)
        ans = sq[p]
        shown = ["?" if i == p else x for i, x in enumerate(sq)]
        d = -step if down else step
        return mcq("수를 순서대로 놓았어요. ?에 알맞은 수는 무엇일까요?%s" % cards(shown, 56 if hi > 9 else 50), str(ans),
                   [str(x) for x in (ans + 1, ans - 1, ans + d, sq[p - 1], ans + 10, ans - 10) if 0 <= x <= cap and x != ans],
                   "수가 %d씩 %s지고 있어요. %d 다음은 <b>%d</b>예요." % (step, "작아" if down else "커", sq[p - 1], ans))
    return mk


def between(lo, hi):
    cap = 9 if hi <= 9 else 100

    def mk():
        a = R.randint(lo, hi - 2)
        b = a + 2
        return mcq("<b>%d</b>와 <b>%d</b> 사이에 있는 수는 무엇일까요?" % (a, b), str(a + 1),
                   [str(x) for x in (a, b, b + 1, a - 1, a + 10) if 0 <= x <= cap],
                   "%d, ( ), %d 순서이므로 사이에 있는 수는 <b>%d</b>예요." % (a, b, a + 1))
    return mk


def biggest(lo, hi, close=False):
    def mk():
        big = R.random() < 0.6
        if close:
            t = R.randint(lo // 10, hi // 10)
            pool = [x for x in range(max(lo, 10), hi + 1) if abs(x // 10 - t) <= 1 and x >= lo]
        else:
            pool = list(range(lo, hi + 1))
        xs = R.sample(pool, 4)
        a = max(xs) if big else min(xs)
        rest = [x for x in xs if x != a]
        return mcq("%s 수는 무엇일까요?%s" % ("가장 큰" if big else "가장 작은", cards(xs, 56 if hi > 9 else 50)), str(a), [str(x) for x in rest],
                   ("먼저 십의 자리를 비교하고, 같으면 일의 자리를 비교해요. " if hi > 9 else "수를 순서대로 셀 때 %s 나오는 수가 %s 수예요. " % ("뒤에" if big else "앞에", "큰" if big else "작은"))
                   + "%s 수는 <b>%d</b>예요." % ("가장 큰" if big else "가장 작은", a))
    return mk


def more_than(lo, hi):
    def mk():
        n = R.randint(lo + 2, hi - 2)
        big = R.random() < 0.5
        good = list(range(n + 1, hi + 1)) if big else list(range(lo, n))
        bad = list(range(lo, n + 1)) if big else list(range(n, hi + 1))
        a = R.choice(good)
        return mcq("다음 중 <b>%d</b>보다 %s 수는 무엇일까요?" % (n, "큰" if big else "작은"), str(a), [str(x) for x in R.sample(bad, min(3, len(bad)))],
                   "%d보다 %s 수는 수를 셀 때 %d보다 %s 나와요. <b>%d</b>" % (n, "큰" if big else "작은", n, "뒤에" if big else "앞에", a))
    return mk


def most_story(lo, hi, thing="구슬"):
    def mk():
        ns = [NM.next() for _ in range(3)]
        if len(set(ns)) < 3:
            return None
        vs = R.sample(range(lo, hi + 1), 3)
        big = R.random() < 0.6
        a = ns[vs.index(max(vs) if big else min(vs))]
        txt = ", ".join("%s %d개" % (josa(n, "은/는"), v) for n, v in zip(ns, vs))
        return mcq("%s %s 가지고 있어요. %s 가진 사람은 누구일까요?" % (josa(thing, "을/를"), txt, "가장 많이" if big else "가장 적게"),
                   a, [n for n in ns if n != a] + ["세 사람이 모두 같아요"],
                   "%d, %d, %d 중에서 %s 수는 %d예요. 그래서 <b>%s</b>예요." % (vs[0], vs[1], vs[2], "가장 큰" if big else "가장 작은", max(vs) if big else min(vs), a))
    return mk


# ------------------------------------------------------------------ 9까지의 수
def count_phrase():
    def mk():
        n, k = R.randint(1, 9), R.choice(KINDS)
        ok = "%s %s %s" % (nm(k), native_c(n), cw(k))
        w = ["%s %s %s" % (nm(k), sino(n), cw(k)), "%s %s %s" % (nm(k), ONES[n], cw(k)) if ONES[n] != ONES_C[n] else None,
             "%s %s %s" % (nm(k), native_c(n + 1 if n < 9 else n - 1), cw(k)), "%s %s %s" % (nm(k), native_c(n - 1 if n > 1 else 2), cw(k))]
        return mcq("<b>%s</b>를 바르게 읽은 것은 무엇일까요?" % cnt(k, n), ok, w,
                   "개수를 셀 때는 '%s, %s…'처럼 읽어요. %s는 <b>%s</b>라고 읽어요." % (ONES_C[1] + " " + cw(k), ONES_C[2] + " " + cw(k), cnt(k, n), ok))
    return mk


def order_names():
    def mk():
        L = R.randint(5, 8)
        ns = []
        while len(ns) < L:
            x = NM.next()
            if x not in ns:
                ns.append(x)
        front = R.random() < 0.6
        p = R.randint(1, L - 1) if front else R.randint(2, L)
        idx = p - 1 if front else L - p
        a = ns[idx]
        other = ns[L - p] if front else ns[p - 1]
        w = [other, ns[idx - 1] if idx > 0 else None, ns[idx + 1] if idx + 1 < L else None]
        q = "친구들이 한 줄로 섰어요. (앞) %s (뒤)<br>%s에서 <b>%s</b>에 서 있는 친구는 누구일까요?" % (" → ".join(ns), "앞" if front else "뒤", ORD[p])
        return mcq(q, a, w, "%s에서부터 첫째, 둘째, … 하고 세면 %s는 <b>%s</b>예요." % ("앞" if front else "뒤", ORD[p], a))
    return mk


def order_objects():
    def mk():
        L = R.randint(6, 9)
        ks = R.sample(KINDS, L)
        left = R.random() < 0.6
        p = R.randint(1, L - 1)
        idx = p - 1 if left else L - p
        a = nm(ks[idx])
        w = [nm(ks[L - p]) if left else nm(ks[p - 1]), nm(ks[idx - 1]) if idx > 0 else None, nm(ks[idx + 1]) if idx + 1 < L else None, nm(ks[(idx + 2) % L])]
        return mcq("%s에서 <b>%s</b>에 있는 것은 무엇일까요?%s" % ("왼쪽" if left else "오른쪽", ORD[p], kinds_row(ks)), a, w,
                   "%s부터 첫째, 둘째, … 하고 세면 %s는 <b>%s</b>예요." % ("왼쪽" if left else "오른쪽", ORD[p], a))
    return mk


def ord_vs_count():
    def mk():
        n, k = R.randint(4, 9), R.choice(KINDS)
        p = R.randint(2, n)
        how = R.choice(["ord", "cnt"])
        if how == "ord":
            q = "%s 한 줄로 %d%s 있어요. 왼쪽에서 <b>%s</b> %s 하나에만 색칠하면 색칠한 %s는 몇 %s일까요?" % (josa(nm(k), "이/가"), n, cw(k), ORD[p], nm(k), nm(k), cw(k))
            return mcq(q, "1%s" % cw(k), ["%d%s" % (x, cw(k)) for x in (p, p - 1, n - p + 1, n)],
                       "'%s'는 순서예요. 하나만 가리키니까 <b>1%s</b>예요." % (ORD[p], cw(k)))
        q = "%s 한 줄로 %d%s 있어요. 왼쪽에서부터 <b>%d%s</b>에 색칠하면, 색칠하지 않은 %s는 몇 %s일까요?" % (josa(nm(k), "이/가"), n, cw(k), p, cw(k), nm(k), cw(k))
        return mcq(q, "%d%s" % (n - p, cw(k)), ["%d%s" % (x, cw(k)) for x in (n - p + 1, p, n, 1)],
                   "%d%s 중 %d%s에 색칠했으니 남은 것은 <b>%d%s</b>예요." % (n, cw(k), p, cw(k), n - p, cw(k)))
    return mk


def zero_q():
    def mk():
        k = R.choice(KINDS)
        n = R.randint(1, 6)
        how = R.choice(["cross", "plate"])
        if how == "cross":
            return mcq("%s %d%s를 모두 지웠어요. 남은 %s는 몇 %s일까요?%s" % (nm(k), n, cw(k), nm(k), cw(k), crossed(n, k, n)), "0%s" % cw(k),
                       ["%d%s" % (x, cw(k)) for x in (1, n, n - 1 if n > 2 else 2)],
                       "하나도 남지 않았어요. 아무것도 없는 것은 <b>0</b>(영)이에요.")
        a = R.randint(1, 5)
        return mcq("접시에 %s %d%s가 있었어요. %d%s를 먹었더니 접시에 아무것도 없어요. 처음에 있던 %s는 몇 %s일까요?" % (nm(k), a, cw(k), a, cw(k), nm(k), cw(k)),
                   "%d%s" % (a, cw(k)), ["%d%s" % (x, cw(k)) for x in (0, a + 1, a - 1 if a > 1 else 2)],
                   "먹은 만큼 있었어요. 처음에 <b>%d%s</b>가 있었어요." % (a, cw(k)))
    return mk


def match_more():
    def mk():
        ka, kb = R.sample(KINDS, 2)
        a, b = R.sample(range(2, 10), 2)
        q = "하나씩 짝을 지어 보세요. 어느 것이 몇 %s 더 많을까요?%s" % ("개", ko(K.match_svg([(a, ka, "", None), (b, kb, "", None)]), "%s와 %s" % (cnt(ka, a), cnt(kb, b))))
        big, small, d = (ka, kb, a - b) if a > b else (kb, ka, b - a)
        def say(k, x):
            return "%s %d%s 더 많아요" % (josa(nm(k), "이/가"), x, cw(k))
        return mcq(q, say(big, d), [say(small, d), say(big, d + 1), say(big, d - 1) if d > 1 else "둘이 같아요"],
                   "짝을 짓고 남는 것을 세어요. %s <b>%d%s</b> 더 많아요." % (josa(nm(big), "이/가"), d, cw(big)))
    return mk


# ------------------------------------------------------------------ 50까지의 수
def ten_make():
    def mk():
        how = R.choice(["frame", "bond", "more"])
        a = R.randint(1, 9)
        if how == "frame":
            k = R.choice(["dot", "apple", "star", "flower", "ball"])
            return mcq("10이 되려면 몇 개가 더 있어야 할까요?%s" % tenframe(a, 1, k), "%d개" % (10 - a),
                       ["%d개" % x for x in near(10 - a, 0, 10) + [a]],
                       "빈칸을 세어 보면 %d칸이에요. %d와 <b>%d</b>를 모으면 10이에요." % (10 - a, a, 10 - a))
        if how == "bond":
            return mcq("10을 두 수로 가르기 했어요. ?에 알맞은 수는 무엇일까요?%s" % bond(10, a, "?"), str(10 - a),
                       [str(x) for x in near(10 - a, 0, 10) + [a, 10]],
                       "%d와 %d를 모으면 10이에요. <b>%d</b>" % (a, 10 - a, 10 - a))
        return mcq("<b>%d</b>와 몇을 모으면 10이 될까요?" % a, str(10 - a), [str(x) for x in near(10 - a, 0, 10) + [a]],
                   "%d에서 10까지 세면 %d번 더 세요. <b>%d</b>" % (a, 10 - a, 10 - a))
    return mk


def ten_facts():
    F = [("9보다 1 큰 수는 무엇일까요?", "10", ["8", "11", "19"], "9 다음 수는 <b>10</b>이에요."),
         ("10을 바르게 읽은 것을 모두 고르면 무엇일까요?", "십, 열", ["일영, 열", "십, 하나", "일, 열"], "10은 <b>십</b> 또는 <b>열</b>이라고 읽어요."),
         ("11보다 1 작은 수는 무엇일까요?", "10", ["12", "9", "1"], "11 바로 앞의 수는 <b>10</b>이에요."),
         ("10개씩 묶음 1개는 몇일까요?", "10", ["1", "11", "100"], "10개씩 묶음 1개는 <b>10</b>이에요."),
         ("8과 몇을 모으면 10이 될까요?", "2", ["1", "3", "8"], "8, 9, 10 하고 2번 더 세요. <b>2</b>")]
    pool = F[:]

    def mk():
        if not pool:
            return None
        return mcq(*pool.pop(0))
    return mk


def teen_rods():
    def mk():
        o = R.randint(1, 9)
        n = 10 + o
        if R.random() < 0.5:
            return mcq("모두 몇 개일까요?%s" % rods(1, o), "%d개" % n, ["%d개" % x for x in (o, o * 10 + 1, n + 1, n - 1)],
                       "10개씩 묶음 1개와 낱개 %d개는 <b>%d</b>이에요." % (o, n))
        return mcq("10개씩 묶음 1개와 낱개 <b>%d개</b>는 몇일까요?" % o, str(n), [str(x) for x in (o, 10 * o + 1, n + 1, n - 1)],
                   "10과 %d을 모으면 <b>%d</b>이에요." % (o, n))
    return mk


def tens_rods(lo, hi):
    def mk():
        t = R.randint(lo, hi)
        how = R.choice(["pic", "txt", "read"])
        if how == "pic":
            return mcq("모두 몇 개일까요?%s" % rods(t, 0), "%d개" % (10 * t), ["%d개" % x for x in (t, 10 * t + 10, 10 * t - 10, 10 * t + 1) if x > 0],
                       "10개씩 묶음이 %d개이면 <b>%d</b>이에요." % (t, 10 * t))
        if how == "txt":
            return mcq("10개씩 묶음 <b>%d개</b>는 몇일까요?" % t, str(10 * t), [str(x) for x in (t, 10 * t + t, 10 * t + 10, 10 * t - 10) if x > 0],
                       "10개씩 묶음 %d개는 <b>%d</b>이에요. 낱개가 없으니 일의 자리는 0이에요." % (t, 10 * t))
        n = 10 * t
        return mcq("<b>%d</b>을 바르게 읽은 것은 무엇일까요?" % n, "%s, %s" % (sino(n), native(n)),
                   ["%s, %s" % (sino(n), native(n + 10 if n < 90 else n - 10)), "%s, %s" % (sino(n + 10 if n < 90 else n - 10), native(n)),
                    "%s, %s" % (sino(t), native(t)), "%s영, %s" % (sino(t), native(n))],
                   "%d은 <b>%s</b> 또는 <b>%s</b>이라고 읽어요." % (n, sino(n), native(n)))
    return mk


def tens_story(lo, hi):
    TH = [("연필", "자루"), ("색종이", "장"), ("사탕", "개"), ("달걀", "개"), ("구슬", "개"), ("공책", "권")]

    def mk():
        t = R.randint(lo, hi)
        th, c = R.choice(TH)
        how = R.choice(["all", "word"])
        if how == "word":
            n = 10 * t
            wd = "'%s'" % R.choice([sino(n), native(n)])
            return mcq("%s 수로 쓰면 무엇일까요?" % josa(wd, "을/를"), str(n), [str(x) for x in (t, n + 10, n - 10, 10 * t + t) if 0 < x <= 100],
                       "%s <b>%d</b>이에요." % (josa(wd, "은/는"), n))
        return mcq("%s%s 10%s씩 묶음 <b>%d개</b>가 있어요. %s 모두 몇 %s일까요?" % (josa(th, "이/가"), "", c, t, josa(th, "은/는"), c),
                   "%d%s" % (10 * t, c), ["%d%s" % (x, c) for x in (t, 10 * t + 10, 10 * t - 10, 10 + t) if x > 0],
                   "10씩 %d번 세면 10, 20, … <b>%d%s</b>예요." % (t, 10 * t, c))
    return mk


def tens_ones(tlo, thi, words=True):
    def mk():
        t, o = R.randint(tlo, thi), R.randint(1, 9)
        n = 10 * t + o
        how = R.choice(["pic", "split", "join"])
        if how == "pic":
            return mcq("모두 몇 개일까요?%s" % rods(t, o), "%d개" % n, ["%d개" % x for x in (10 * o + t, n + 1, n - 1, n + 10) if x != n and 0 < x <= 100],
                       "10개씩 묶음 %d개와 낱개 %d개이므로 <b>%d</b>이에요." % (t, o, n))
        if how == "split":
            def say(a, b):
                return "10개씩 묶음 %d개와 낱개 %d개" % (a, b)
            return mcq("<b>%d</b>은 10개씩 묶음 몇 개와 낱개 몇 개일까요?" % n, say(t, o),
                       [say(o, t), say(t, o + 1) if o < 9 else say(t, o - 1), say(t + 1, o) if t < 9 else say(t - 1, o), say(t, 0)],
                       "%d의 십의 자리 %d은 묶음, 일의 자리 %d은 낱개예요. <b>%s</b>" % (n, t, o, say(t, o)))
        return mcq("10개씩 묶음 <b>%d개</b>와 낱개 <b>%d개</b>는 몇일까요?" % (t, o), str(n),
                   [str(x) for x in (10 * o + t, n + 1, n + 10, t + o) if x != n and 0 < x <= 100],
                   "묶음 수를 십의 자리에, 낱개 수를 일의 자리에 써요. <b>%d</b>" % n)
    return mk


def loose_to_bundle():
    """낱개가 10개 넘을 때：10개씩 묶음 2개와 낱개 13개 → 33"""
    def mk():
        t, o = R.randint(1, 3), R.randint(11, 19)
        n = 10 * t + o
        if n > 50:
            return None
        return mcq("10개씩 묶음 <b>%d개</b>와 낱개 <b>%d개</b>는 모두 몇일까요?" % (t, o), str(n),
                   [str(x) for x in (10 * t + o % 10, 10 * t + 10 * o, n + 10, n - 1)],
                   "낱개 %d개는 10개씩 묶음 1개와 낱개 %d개예요. 그래서 묶음 %d개, 낱개 %d개 → <b>%d</b>" % (o, o - 10, t + 1, o - 10, n))
    return mk


# ------------------------------------------------------------------ 100까지의 수
def hundred_facts():
    F = [("99보다 1 큰 수는 무엇일까요?", "100", ["98", "101", "990"], "99 바로 다음 수는 <b>100</b>(백)이에요."),
         ("90보다 10 큰 수는 무엇일까요?", "100", ["91", "80", "190"], "90에서 10을 더 세면 <b>100</b>이에요."),
         ("10개씩 묶음 10개는 몇일까요?", "100", ["10", "1010", "90"], "10개씩 묶음 10개는 <b>100</b>이에요."),
         ("100을 바르게 읽은 것은 무엇일까요?", "백", ["십", "일영영", "열"], "100은 <b>백</b>이라고 읽어요."),
         ("100보다 1 작은 수는 무엇일까요?", "99", ["90", "101", "98"], "100 바로 앞의 수는 <b>99</b>예요.")]
    pool = F[:]

    def mk():
        if not pool:
            return None
        return mcq(*pool.pop(0))
    return mk


def chart_q():
    def mk():
        r0, c0 = R.randint(0, 7), R.randint(0, 6)
        tl = r0 * 10 + c0 + 1
        nr, nc = 3, 3 + (1 if c0 <= 5 else 0)
        tr, tc = R.randint(0, nr - 1), R.randint(0, nc - 1)
        if (tr, tc) == (0, 0):
            tr = 1
        ans = tl + 10 * tr + tc
        return mcq("수 배열표의 일부예요. ?에 알맞은 수는 무엇일까요?%s" % chart(tl, nr, nc, (tr, tc)), str(ans),
                   [str(x) for x in (ans + 1, ans - 1, ans + 10, ans - 10, tl + 10 * tc + tr) if 0 < x <= 100 and x != ans],
                   "오른쪽으로 가면 1씩, 아래로 가면 10씩 커져요. <b>%d</b>" % ans)
    return mk


def compare_say(lo, hi):
    def mk():
        a, b = R.sample(range(lo, hi + 1), 2)
        if R.random() < 0.6 and a // 10 != b // 10 and a % 10 != b % 10:
            pass
        s, g = min(a, b), max(a, b)

        lt = a < b
        ok = "%d은 %d보다 %s" % (a, b, "작아요" if lt else "커요")
        return mcq("<b>%d</b>와 <b>%d</b>의 크기를 바르게 말한 것은 무엇일까요?" % (a, b), ok,
                   ["%d은 %d보다 %s" % (a, b, "커요" if lt else "작아요"), "%d은 %d보다 %s" % (b, a, "작아요" if lt else "커요"), "%d과 %d는 크기가 같아요" % (a, b)],
                   "십의 자리 수를 먼저 비교하고, 같으면 일의 자리를 비교해요. <b>%d이 %d보다 커요.</b>" % (g, s))
    return mk


def even_odd():
    def mk():
        how = R.choice(["pick", "pic", "count"])
        if how == "pick":
            ev = R.random() < 0.5
            good = [x for x in range(1, 51) if (x % 2 == 0) == ev]
            bad = [x for x in range(1, 51) if (x % 2 == 0) != ev]
            a = R.choice(good)
            return mcq("다음 중 <b>%s</b>는 무엇일까요?" % ("짝수" if ev else "홀수"), str(a), [str(x) for x in R.sample(bad, 3)],
                       "일의 자리가 %s 수가 %s예요. <b>%d</b>" % ("0, 2, 4, 6, 8인" if ev else "1, 3, 5, 7, 9인", "짝수" if ev else "홀수", a))
        if how == "pic":
            n, k = R.randint(5, 16), R.choice(KINDS)
            sw = "짝수" if n % 2 == 0 else "홀수"
            ot = "홀수" if n % 2 == 0 else "짝수"
            pic = ko(K.groups_svg([(2, k)] * (n // 2) + ([(1, k)] if n % 2 else []), 14), cnt(k, n))
            return mcq("둘씩 짝을 지었어요. %s의 수와 짝수·홀수를 바르게 말한 것은?%s" % (nm(k), pic),
                       "%d%s, %s" % (n, cw(k), sw), ["%d%s, %s" % (n, cw(k), ot), "%d%s, %s" % (n + 1, cw(k), ot), "%d%s, %s" % (n - 1, cw(k), ot)],
                       "둘씩 짝을 지으면 %s. %d은 <b>%s</b>예요." % ("남는 것이 없어요" if n % 2 == 0 else "하나가 남아요", n, sw))
        a = R.randint(1, 40)
        b = a + R.randint(5, 9)
        ev = R.random() < 0.5
        c = sum(1 for x in range(a, b + 1) if (x % 2 == 0) == ev)
        return mcq("<b>%d</b>부터 <b>%d</b>까지의 수 중에서 %s는 몇 개일까요?" % (a, b, "짝수" if ev else "홀수"), "%d개" % c,
                   ["%d개" % x for x in (c + 1, c - 1, b - a + 1, b - a)],
                   "%s를 모두 써 보면 %s이에요. <b>%d개</b>" % ("짝수" if ev else "홀수", ", ".join(str(x) for x in range(a, b + 1) if (x % 2 == 0) == ev), c))
    return mk


# ------------------------------------------------------------------ build
def build(which):
    if which == "n9":
        return unit(G, "numbers-to-9", 1, "[2수01-01]",
                    "수의 필요성을 인식하면서 0과 100까지의 수 개념을 이해하고, 수를 세고 읽고 쓸 수 있다.",
                    "9까지의 수 세기·읽기·쓰기", "9까지의 수",
                    "초등 1학년 1학기 9까지의 수 학습지: 그림을 보고 수 세기, 두 가지로 읽기(오·다섯), 순서(첫째, 둘째), 1 큰 수와 1 작은 수, 0, 수의 크기 비교까지 100문제와 정답.",
                    "하나, 둘, 셋… 빠짐없이 세어요", "수는 두 가지로 읽어요(일·하나). 순서는 첫째, 둘째로 말해요.",
                    ["물건을 셀 때는 하나씩 짚으면서 빠뜨리지 않고 세어요. 마지막에 센 수가 물건의 수예요.",
                     "수는 두 가지로 읽어요. 5는 <b>오</b> 또는 <b>다섯</b>이에요. 개수를 말할 때는 '다섯 개', '세 마리'처럼 읽어요.",
                     "순서를 말할 때는 <b>첫째, 둘째, 셋째</b>…라고 해요. '셋째'는 하나만 가리키고, '3개'는 모두 세 개예요.",
                     "수를 순서대로 셀 때 바로 다음 수는 1 큰 수, 바로 앞의 수는 1 작은 수예요. 아무것도 없는 것은 <b>0</b>이에요."],
                    [("6보다 1 큰 수", ["6 다음에 세는 수를 찾아요."], "7"),
                     ("앞에서 넷째에 선 친구", ["앞에서부터 첫째, 둘째, 셋째, 넷째 하고 세어요."], "넷째 자리의 친구")],
                    [("사과 3개를 '사과 삼 개'라고 읽는다", "개수는 '사과 세 개'라고 읽어요."),
                     ("'셋째'와 '3개'를 같다고 생각한다", "셋째는 순서, 3개는 개수예요."),
                     ("세었던 것을 또 센다", "센 것에 표시를 하며 세어요.")],
                    [("9까지의 수는 언제 배우나요?", "초등 1학년 1학기 「9까지의 수」 단원에서 배워요."),
                     ("수를 왜 두 가지로 읽나요?", "우리말 수(하나, 둘)와 한자어 수(일, 이)가 있어요. 개수는 주로 하나, 둘로, 번호는 일, 이로 읽어요.")],
                    [("몇 개일까요", [(count_pic(1, 9), 20)]),
                     ("수 읽기", [(read_both(1, 9), 6), (word_to_num(1, 9), 7), (count_phrase(), 7)]),
                     ("순서", [(order_names(), 8), (order_objects(), 7), (ord_vs_count(), 5)]),
                     ("수의 순서와 0", [(one_more_less(0, 9), 7), (seq_cards(0, 9), 7), (between(0, 9), 3), (zero_q(), 3)]),
                     ("수의 크기 비교", [(more_than(0, 9), 6), (biggest(0, 9), 5), (match_more(), 5), (most_story(1, 9), 4)])], 82101)
    if which == "n50":
        return unit(G, "numbers-to-50", 5, "[2수01-01] [2수01-02] [2수01-03]",
                    "0과 100까지의 수 개념을 이해하고, 수를 세고 읽고 쓸 수 있다. 일, 십의 자릿값을 이해하고, 수의 계열을 이해하며 수의 크기를 비교할 수 있다.",
                    "50까지의 수: 10개씩 묶음과 낱개", "50까지의 수",
                    "초등 1학년 1학기 50까지의 수 학습지: 10 모으기와 가르기, 십몇, 몇십(이십·스물), 10개씩 묶음과 낱개, 수 읽기, 수의 순서, 크기 비교까지 100문제와 정답.",
                    "10개씩 묶음 3개와 낱개 4개는 34", "묶음은 십의 자리, 낱개는 일의 자리에 써요.",
                    ["9보다 1 큰 수는 <b>10</b>이에요. 10은 십 또는 열이라고 읽어요.",
                     "10개씩 묶음 1개와 낱개 4개는 <b>14</b>예요. 10개씩 묶음 3개는 <b>30</b>(삼십, 서른)이에요.",
                     "10개씩 묶음 수를 앞(십의 자리)에, 낱개 수를 뒤(일의 자리)에 써요. 묶음 3개, 낱개 7개 → 37",
                     "두 수의 크기는 10개씩 묶음 수를 먼저 비교하고, 같으면 낱개 수를 비교해요."],
                    [("10개씩 묶음 4개와 낱개 2개", ["묶음 4개 → 40", "낱개 2개 → 2"], "42"),
                     ("28과 31 중 더 큰 수", ["묶음 수: 2와 3", "3이 더 커요."], "31")],
                    [("묶음 3개, 낱개 7개를 73이라고 쓴다", "묶음 수를 앞에 써요: 37"),
                     ("30을 '삼영'이라고 읽는다", "30은 삼십 또는 서른이에요."),
                     ("29와 31을 일의 자리(9와 1)로 비교한다", "10개씩 묶음 수(2와 3)를 먼저 비교해요.")],
                    [("50까지의 수는 언제 배우나요?", "초등 1학년 1학기 「50까지의 수」 단원에서 배워요."),
                     ("서른, 마흔은 꼭 알아야 하나요?", "네. 나이나 개수를 말할 때 자주 써요. 스물, 서른, 마흔, 쉰을 함께 익혀요.")],
                    [("10과 십몇", [(ten_facts(), 3), (ten_make(), 9), (teen_rods(), 8)]),
                     ("몇십", [(tens_rods(2, 5), 10), (tens_story(2, 5), 10)]),
                     ("50까지의 수 세기", [(tens_ones(1, 4), 12), (read_both(11, 50), 5), (loose_to_bundle(), 3)]),
                     ("수의 순서", [(one_more_less(1, 49), 7), (seq_cards(10, 50), 7), (between(10, 50), 6)]),
                     ("수의 크기 비교", [(more_than(10, 50), 6), (biggest(10, 50, True), 7), (most_story(11, 50, "딱지"), 7)])], 82105)
    if which == "n100":
        return unit(G, "numbers-to-100", 6, "[2수01-01] [2수01-02] [2수01-03]",
                    "0과 100까지의 수 개념을 이해하고, 수를 세고 읽고 쓸 수 있다. 일, 십, 백의 자릿값을 이해하고, 수의 계열을 이해하며 수의 크기를 비교할 수 있다.",
                    "100까지의 수: 순서·크기·짝수와 홀수", "100까지의 수",
                    "초등 1학년 2학기 100까지의 수 학습지: 예순·일흔·여든·아흔, 99까지의 수, 100, 수 배열표, 수의 크기 비교, 짝수와 홀수까지 100문제와 정답.",
                    "99보다 1 큰 수는 100(백)", "십의 자리를 먼저, 같으면 일의 자리를 비교해요.",
                    ["60은 육십 또는 <b>예순</b>, 70은 칠십 또는 <b>일흔</b>, 80은 팔십 또는 <b>여든</b>, 90은 구십 또는 <b>아흔</b>이에요.",
                     "99보다 1 큰 수는 <b>100</b>이에요. 100은 백이라고 읽어요.",
                     "수 배열표에서 오른쪽으로 가면 1씩, 아래로 가면 10씩 커져요.",
                     "둘씩 짝을 지을 때 남는 것이 없는 수는 <b>짝수</b>, 하나가 남는 수는 <b>홀수</b>예요."],
                    [("67과 72의 크기 비교", ["십의 자리: 6과 7", "7이 더 커요."], "67은 72보다 작아요"),
                     ("16은 짝수일까요?", ["일의 자리가 6이에요."], "짝수")],
                    [("80을 '팔영'이나 '여덜'이라고 읽는다", "80은 팔십 또는 여든이에요."),
                     ("59와 61에서 9가 1보다 크니 59가 크다고 한다", "십의 자리(5와 6)를 먼저 비교해요."),
                     ("13은 짝수라고 생각한다", "일의 자리가 1, 3, 5, 7, 9이면 홀수예요.")],
                    [("100까지의 수는 언제 배우나요?", "초등 1학년 2학기 「100까지의 수」 단원에서 배워요."),
                     ("짝수와 홀수는 어떻게 가르치면 좋을까요?", "바둑돌이나 블록을 둘씩 짝 지어 보며 남는 것이 있는지 확인해 보세요.")],
                    [("몇십과 100", [(tens_rods(6, 9), 10), (tens_story(6, 9), 6), (hundred_facts(), 4)]),
                     ("99까지의 수", [(tens_ones(5, 9), 14), (read_both(51, 99), 6)]),
                     ("수의 순서", [(chart_q(), 8), (seq_cards(50, 100), 5), (one_more_less(50, 99), 4), (one_more_less(50, 90, 10), 3)]),
                     ("수의 크기 비교", [(compare_say(50, 99), 10), (biggest(50, 99, True), 6), (most_story(51, 99, "구슬"), 4)]),
                     ("짝수와 홀수", [(even_odd(), 20)])], 82106)
    raise ValueError(which)
