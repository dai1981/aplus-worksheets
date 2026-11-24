# -*- coding: utf-8 -*-
"""
대한민국 고등학교 확률과 통계（2022 개정）の 10 単元。build(key)：
  rperm 중복순열과 같은 것이 있는 순열 / rcomb 중복조합 / binom 이항정리 / prob 확률의 뜻과 덧셈정리 / cond 조건부확률
  indep 독립과 곱셈정리 / drv 이산확률변수 / bdist 이항분포 / norm 정규분포 / samp 표본평균과 추정
誤答は「중복순열을 ₙPᵣ로 센다」「같은 것을 나누지 않는다」「ₙHᵣ = ₙCᵣ로 쓴다」「이항계수에서 a, b의 거듭제곱을 빠뜨린다」
「P(A ∪ B)에서 P(A ∩ B)를 빼지 않는다」「P(B|A)를 P(A ∩ B) ÷ P(B)로 쓴다」「독립과 배반을 같게 본다」「V(aX + b) = aV(X) + b」
「표준화에서 σ 대신 σ²으로 나눈다」「σ(X̄) = σ/n으로 쓴다」から作る。
"""
import math
import random
from fractions import Fraction as Fr
from kr_hs import M, N, neg, par, px, surd, W, num, fr, unit
from fr_common import table

R = random.Random(83401)
G = "probability-and-statistics"
C = math.comb
P_ = math.perm


def sub(n, L, r):
    return "<sub>%s</sub>%s<sub>%s</sub>" % (n, L, r)


def nz(lo=-6, hi=6):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


# ------------------------------------------------------------------ 중복순열·같은 것이 있는 순열
def rp_main(kinds=("pi", "num", "func", "same", "word", "path")):
    def mk():
        how = R.choice(kinds)
        if how == "pi":
            n, r = R.randint(2, 9), R.randint(2, 5)
            v = n ** r
            if v > 10 ** 5:
                return None
            return N("<b>%s</b>의 값은?" % sub(n, "Π", r), v, [P_(n, r) if r <= n else r ** n, r ** n, C(n + r - 1, r), n * r], "%s = %d<sup>%d</sup> = <b>%s</b>" % (sub(n, "Π", r), n, r, num(v)))
        if how == "num":
            n = R.randint(2, 5)
            r = R.randint(2, 4)
            k = R.choice(["any", "zero"])
            if k == "any":
                v = n ** r
                return N("숫자 %s를 중복하여 사용할 수 있을 때, 만들 수 있는 %d자리 자연수의 개수는?" % (", ".join(str(i) for i in range(1, n + 1)), r), v, [P_(n, r) if r <= n else n * r, r ** n, n * r, v - 1], "각 자리에 %d가지씩: %d<sup>%d</sup> = <b>%s</b>" % (n, n, r, num(v)), f=lambda t: "%s개" % num(t))
            v = (n - 1) * n ** (r - 1)
            return N("숫자 %s를 중복하여 사용할 수 있을 때, 만들 수 있는 %d자리 자연수의 개수는?" % (", ".join(str(i) for i in range(n)), r), v, [n ** r, (n - 1) ** r, n ** (r - 1), v + 1], "맨 앞자리는 0이 아닌 %d가지, 나머지는 %d가지씩. <b>%s</b>" % (n - 1, n, num(v)), f=lambda t: "%s개" % num(t))
        if how == "func":
            m, n = R.randint(2, 5), R.randint(2, 4)
            k = R.choice(["func", "post", "vote"])
            if k == "func":
                v = n ** m
                return N("집합 X = {%s}에서 집합 Y = {%s}로의 함수의 개수는?" % (", ".join(str(i) for i in range(1, m + 1)), ", ".join("abcd"[:n])), v, [m ** n, m * n, P_(n, m) if m <= n else v - 1, v + 1], "X의 각 원소마다 %d가지: %s = <b>%s</b>" % (n, sub(n, "Π", m), num(v)), f=lambda t: "%s개" % num(t))
            if k == "post":
                v = n ** m
                return N("서로 다른 편지 %d통을 서로 다른 우체통 %d개에 넣는 방법의 수는? (빈 우체통이 있어도 돼요)" % (m, n), v, [m ** n, P_(max(m, n), min(m, n)), m * n, C(m + n - 1, m)], "편지 한 통마다 %d가지: %d<sup>%d</sup> = <b>%s</b>" % (n, n, m, num(v)), f=lambda t: "%s가지" % num(t))
            v = n ** m
            return N("학생 %d명이 후보 %d명 중 한 명에게 각각 투표할 때, 기명으로 투표하는 방법의 수는?" % (m, n), v, [m ** n, C(m + n - 1, m), m * n, P_(max(m, n), min(m, n))], "학생마다 %d가지: <b>%s</b>" % (n, num(v)), f=lambda t: "%s가지" % num(t))
        if how == "same":
            a, b = R.randint(1, 4), R.randint(1, 4)
            c = R.randint(0, 3)
            n = a + b + c
            v = math.factorial(n) // (math.factorial(a) * math.factorial(b) * math.factorial(c))
            items = ["빨간 공 %d개" % a, "파란 공 %d개" % b] + (["노란 공 %d개" % c] if c else [])
            return N("%s를 일렬로 나열하는 방법의 수는?" % ", ".join(items), v, [math.factorial(n), math.factorial(n) // math.factorial(a), n ** 2, v * 2 if v * 2 != math.factorial(n) else v + 1],
                     "%d! ÷ (%d!%d!%s) = <b>%s</b>" % (n, a, b, " %d!" % c if c else "", num(v)), f=lambda t: "%s가지" % num(t))
        if how == "word":
            W_ = R.choice(["banana", "apple", "letter", "school", "coffee", "seesaw", "tomato", "pepper", "assess", "puzzle", "google", "balloon", "success", "address", "bubble", "cocoon", "kayak", "level", "radar", "yellow", "dinner", "happy", "committee", "teeth", "sheep", "little"])
            n = len(W_)
            cnt = {ch: W_.count(ch) for ch in set(W_)}
            den = 1
            for v_ in cnt.values():
                den *= math.factorial(v_)
            v = math.factorial(n) // den
            return N("<b>%s</b>의 %d개 문자를 모두 일렬로 나열하는 방법의 수는?" % (W_, n), v, [math.factorial(n), v * 2, math.factorial(n) // max(cnt.values()), v + 1], "같은 문자: %s. %d! ÷ (%s) = <b>%s</b>" % (", ".join("%s %d개" % (k, v_) for k, v_ in sorted(cnt.items()) if v_ > 1), n, " × ".join("%d!" % v_ for v_ in sorted(cnt.values()) if v_ > 1), num(v)),
                     f=lambda t: "%s가지" % num(t))
        a, b = R.randint(2, 5), R.randint(2, 5)
        v = C(a + b, a)
        if R.random() < 0.5:
            a1, b1 = R.randint(1, a - 1), R.randint(1, b - 1)
            v2 = C(a1 + b1, a1) * C(a - a1 + b - b1, a - a1)
            return N("가로로 %d칸, 세로로 %d칸인 바둑판 모양의 길에서 A(왼쪽 아래)에서 출발하여 A에서 오른쪽으로 %d칸, 위로 %d칸 떨어진 지점 P를 거쳐 B(오른쪽 위)까지 최단 거리로 가는 방법의 수는?" % (a, b, a1, b1), v2, [C(a1 + b1, a1) + C(a - a1 + b - b1, a - a1), v, v - v2 if v - v2 != v2 else v2 + 1, v2 * 2],
                     "A → P: %s가지, P → B: %s가지이므로 곱해요. <b>%s</b>" % (num(C(a1 + b1, a1)), num(C(a - a1 + b - b1, a - a1)), num(v2)), f=lambda t: "%s가지" % num(t))
        return N("가로로 %d칸, 세로로 %d칸인 바둑판 모양의 길에서 A(왼쪽 아래)에서 B(오른쪽 위)까지 최단 거리로 가는 방법의 수는?" % (a, b), v, [math.factorial(a + b), a * b, 2 ** (a + b), v + 1], "→ %d개, ↑ %d개를 나열해요. %d! ÷ (%d!%d!) = <b>%s</b>" % (a, b, a + b, a, b, num(v)), f=lambda t: "%s가지" % num(t))
    return mk


# ------------------------------------------------------------------ 중복조합
def rc_main(kinds=("h", "buy", "eq", "pos", "ball")):
    def mk():
        how = R.choice(kinds)
        if how == "h":
            n, r = R.randint(2, 6), R.randint(2, 6)
            v = C(n + r - 1, r)
            return N("<b>%s</b>의 값은?" % sub(n, "H", r), v, [C(n, r) if r <= n else n ** r, n ** r, C(n + r, r), C(n + r - 1, r - 1) if C(n + r - 1, r - 1) != v else v + 1], "%s = %s = <b>%s</b>" % (sub(n, "H", r), sub(n + r - 1, "C", r), num(v)))
        if how == "buy":
            n, r = R.randint(3, 5), R.randint(2, 10)
            kinds_ = ["사과", "배", "귤", "감", "복숭아"][:n]
            v = C(n + r - 1, r)
            return N("%s 중에서 %d개를 사는 방법의 수는? (같은 종류를 여러 개 사도 되고, 각 종류는 충분히 많아요)" % (", ".join(kinds_), r), v, [n ** r, C(n, r) if r <= n else C(r, n), C(n + r, r), v + 1], "%d종류에서 중복을 허락하여 %d개: %s = <b>%s</b>" % (n, r, sub(n, "H", r), num(v)), f=lambda t: "%s가지" % num(t))
        if how == "eq":
            k, n = R.randint(2, 4), R.randint(3, 12)
            vars_ = ["x", "y", "z", "w"][:k]
            v = C(n + k - 1, n)
            return N("방정식 %s = %d를 만족하는 음이 아닌 정수 해의 순서쌍의 개수는?" % (" + ".join(vars_), n), v, [C(n - 1, k - 1), C(n + k, n), k ** n if k ** n < 10 ** 5 else v * 2, v + 1], "%s = %s = <b>%s</b>" % (sub(k, "H", n), sub(n + k - 1, "C", n), num(v)), f=lambda t: "%s개" % num(t))
        if how == "pos":
            k, n = R.randint(2, 4), R.randint(5, 12)
            vars_ = ["x", "y", "z", "w"][:k]
            v = C(n - 1, k - 1)
            return N("방정식 %s = %d를 만족하는 자연수 해의 순서쌍의 개수는?" % (" + ".join(vars_), n), v, [C(n + k - 1, n), C(n, k), C(n - 1, k) if C(n - 1, k) != v else v + 2, v + 1], "x = x′ + 1 꼴로 바꾸면 합이 %d인 음이 아닌 정수 해: %s = <b>%s</b>" % (n - k, sub(k, "H", n - k), num(v)), f=lambda t: "%s개" % num(t))
        n, r = R.randint(2, 4), R.randint(3, 8)
        k = R.choice(["any", "each"])
        if k == "any":
            v = C(n + r - 1, r)
            return N("같은 공 %d개를 서로 다른 상자 %d개에 넣는 방법의 수는? (빈 상자가 있어도 돼요)" % (r, n), v, [n ** r, C(r - 1, n - 1) if r >= n else v + 1, C(n + r, r), v + 2], "%s = <b>%s</b>" % (sub(n, "H", r), num(v)), f=lambda t: "%s가지" % num(t))
        if r < n:
            return None
        v = C(r - 1, n - 1)
        return N("같은 공 %d개를 서로 다른 상자 %d개에 넣을 때, 빈 상자가 없도록 넣는 방법의 수는?" % (r, n), v, [C(n + r - 1, r), n ** r, C(r, n), v + 1], "먼저 한 개씩 넣고 남은 %d개를 나누어요: %s = <b>%s</b>" % (r - n, sub(n, "H", r - n), num(v)), f=lambda t: "%s가지" % num(t))
    return mk


# ------------------------------------------------------------------ 이항정리
def bn_main(kinds=("coef", "term", "sum", "pascal", "const")):
    def mk():
        how = R.choice(kinds)
        if how == "coef":
            n = R.randint(3, 7)
            a, b = R.choice([1, 2, 3]), R.choice([1, 2, -1, -2, 3])
            k = R.randint(1, n - 1)
            v = C(n, k) * a ** k * b ** (n - k)
            return N("<b>(%s)<sup>%d</sup></b>의 전개식에서 x<sup>%d</sup>의 계수는?" % (px([a, b]), n, k), v, [C(n, k), C(n, k) * a ** k, C(n, k) * b ** (n - k) if b ** (n - k) != a ** k * b ** (n - k) else v + 1, -v],
                     "일반항 %s(%sx)<sup>%d</sup>(%s)<sup>%d</sup>에서 %s × %s × %s. <b>%s</b>" % (sub(n, "C", k), "" if a == 1 else a, k, neg(b), n - k, C(n, k), par(a ** k), par(b ** (n - k)), neg(v)))
        if how == "term":
            n = R.randint(4, 8)
            k = R.randint(1, n - 1)
            ok = "%s<sub></sub>x<sup>%d</sup>y<sup>%d</sup>" % (sub(n, "C", k), k, n - k)
            ok = "%sx<sup>%d</sup>y<sup>%d</sup>" % (neg(C(n, k)), k, n - k)
            return M("<b>(x + y)<sup>%d</sup></b>의 전개식에서 x<sup>%d</sup>y<sup>%d</sup>항은?" % (n, k, n - k), ok, ["%sx<sup>%d</sup>y<sup>%d</sup>" % (neg(P_(n, k)), k, n - k), "%sx<sup>%d</sup>y<sup>%d</sup>" % (neg(n), k, n - k), "%sx<sup>%d</sup>y<sup>%d</sup>" % (neg(C(n, k) + 1), k, n - k), "x<sup>%d</sup>y<sup>%d</sup>" % (k, n - k)],
                     "일반항 %sx<sup>r</sup>y<sup>n−r</sup>. <b>%s</b>" % (sub(n, "C", "r"), ok))
        if how == "sum":
            n = R.randint(4, 12)
            k = R.choice(["all", "even", "nz"])
            if k == "all":
                return N("<b>%s + %s + … + %s</b>의 값은?" % (sub(n, "C", 0), sub(n, "C", 1), sub(n, "C", n)), 2 ** n, [2 ** (n - 1), n * n, 2 * n, 2 ** n - 1], "(1 + 1)<sup>%d</sup> = <b>%s</b>" % (n, num(2 ** n)))
            if k == "even":
                return N("<b>%s + %s + %s + …</b>의 값은? (n = %d)" % (sub(n, "C", 0), sub(n, "C", 2), sub(n, "C", 4), n), 2 ** (n - 1), [2 ** n, 2 ** (n - 2), n * (n - 1) // 2, 2 ** (n - 1) - 1], "짝수 번째 이항계수의 합 = 홀수 번째의 합 = 2<sup>n−1</sup>. <b>%s</b>" % num(2 ** (n - 1)))
            return N("<b>%s + %s + … + %s</b>의 값은?" % (sub(n, "C", 1), sub(n, "C", 2), sub(n, "C", n)), 2 ** n - 1, [2 ** n, 2 ** (n - 1), 2 ** n - 2, n * n], "전체 2<sup>%d</sup>에서 %s = 1을 빼요. <b>%s</b>" % (n, sub(n, "C", 0), num(2 ** n - 1)))
        if how == "pascal":
            n = R.randint(4, 10)
            r = R.randint(1, n - 1)
            k = R.choice(["add", "sym"])
            if k == "add":
                v = C(n + 1, r + 1)
                ok = sub(n + 1, "C", r + 1)
                return M("<b>%s + %s</b>의 값과 같은 것은?" % (sub(n, "C", r), sub(n, "C", r + 1)), ok, [sub(n, "C", r + 2), sub(2 * n, "C", 2 * r + 1), sub(n + 1, "C", r), sub(n + 2, "C", r + 1)], "파스칼의 삼각형: <sub>n</sub>C<sub>r</sub> + <sub>n</sub>C<sub>r+1</sub> = <sub>n+1</sub>C<sub>r+1</sub>. <b>%s</b>" % ok)
            if 2 * r == n:
                return None
            ok = sub(n, "C", n - r)
            return M("<b>%s</b>의 값과 같은 것은?" % sub(n, "C", r), ok, [sub(n, "C", r + 1), sub(n - 1, "C", r), sub(n, "P", r), sub(n, "C", n - r - 1) if n - r - 1 != r else sub(n, "C", r - 1)], "<sub>n</sub>C<sub>r</sub> = <sub>n</sub>C<sub>n−r</sub>. <b>%s</b>" % ok)
        # const: (x + a/x)^n 상수항
        n = R.choice([2, 4, 6, 8])
        a = R.choice([1, 2, -1, -2, 3])
        k = n // 2
        v = C(n, k) * a ** k
        return N("<b>(x + %s)<sup>%d</sup></b>의 전개식에서 상수항은?" % (fr(neg(a), "x") if a > 0 else "(" + "−" + fr(abs(a), "x") + ")", n) if a > 0 else "<b>(x − %s)<sup>%d</sup></b>의 전개식에서 상수항은?" % (fr(abs(a), "x"), n), v, [C(n, k), a ** k, -v, v * 2],
                 "일반항 %sx<sup>%d−r</sup>(%s/x)<sup>r</sup>에서 %d − 2r = 0, r = %d. <b>%s</b>" % (sub(n, "C", "r"), n, neg(a), n, k, neg(v)))
    return mk


# ------------------------------------------------------------------ 확률과 덧셈정리
def p_main(kinds=("dice", "ball", "add", "comp", "card", "concept")):
    def mk():
        how = R.choice(kinds)
        if how == "dice":
            k = R.choice(["sum", "sum_le", "diff", "prod"])
            if k == "sum":
                s = R.randint(3, 11)
                c = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s)
                v = Fr(c, 36)
                return N("서로 다른 두 개의 주사위를 동시에 던질 때, 나오는 눈의 수의 합이 %d일 확률은?" % s, v, [Fr(c, 12), Fr(1, 6), Fr(c + 1, 36), Fr(c, 21)], "36가지 중 %d가지. <b>%s</b>" % (c, neg(v)))
            if k == "sum_le":
                s = R.randint(3, 10)
                c = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j <= s)
                v = Fr(c, 36)
                return N("서로 다른 두 개의 주사위를 동시에 던질 때, 나오는 눈의 수의 합이 %d 이하일 확률은?" % s, v, [Fr(36 - c, 36), Fr(s, 12), Fr(c, 21) if Fr(c, 21) != v else v + Fr(1, 36), v + Fr(1, 36)], "36가지 중 %d가지. <b>%s</b>" % (c, neg(v)))
            if k == "diff":
                d = R.randint(0, 4)
                c = sum(1 for i in range(1, 7) for j in range(1, 7) if abs(i - j) == d)
                v = Fr(c, 36)
                return N("서로 다른 두 개의 주사위를 동시에 던질 때, 나오는 눈의 수의 차가 %d일 확률은?" % d, v, [Fr(c, 18) if Fr(c, 18) != v else v * 3, Fr(6 - d, 36) if Fr(6 - d, 36) != v else v / 2, v + Fr(1, 36), Fr(1, 6) if v != Fr(1, 6) else Fr(1, 3)], "36가지 중 %d가지. <b>%s</b>" % (c, neg(v)))
            m = R.choice([2, 3, 4, 6])
            c = sum(1 for i in range(1, 7) for j in range(1, 7) if (i * j) % m == 0)
            v = Fr(c, 36)
            return N("서로 다른 두 개의 주사위를 동시에 던질 때, 나오는 눈의 수의 곱이 %d의 배수일 확률은?" % m, v, [Fr(36 - c, 36), Fr(1, m), v + Fr(1, 36), Fr(c, 21)], "36가지 중 %d가지. <b>%s</b>" % (c, neg(v)))
        if how == "ball":
            r, b = R.randint(2, 6), R.randint(2, 6)
            n = r + b
            k = R.choice([2, 3])
            j = R.randint(1, min(k, r))
            if k - j > b:
                return None
            v = Fr(C(r, j) * C(b, k - j), C(n, k))
            return N("빨간 공 %d개, 파란 공 %d개가 든 주머니에서 공 %d개를 동시에 꺼낼 때, 빨간 공이 %d개일 확률은?" % (r, b, k, j), v, [Fr(r, n) ** j if (Fr(r, n) ** j) != v else v / 2, Fr(C(r, j), C(n, k)), Fr(j, k), 1 - v], "%s × %s ÷ %s = <b>%s</b>" % (sub(r, "C", j), sub(b, "C", k - j), sub(n, "C", k), neg(v)))
        if how == "add":
            n = R.randint(20, 50)
            a, b = R.randint(2, 6), R.randint(2, 7)
            if a == b or a % b == 0 or b % a == 0:
                return None
            A_ = n // a
            B_ = n // b
            AB = n // (a * b // math.gcd(a, b))
            v = Fr(A_ + B_ - AB, n)
            return N("1부터 %d까지의 자연수가 하나씩 적힌 %d장의 카드에서 한 장을 뽑을 때, %d의 배수 또는 %d의 배수가 적힌 카드일 확률은?" % (n, n, a, b), v, [Fr(A_ + B_, n), Fr(AB, n), Fr(A_ + B_ - 2 * AB, n) if AB else v + Fr(1, n), 1 - v], "P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = (%d + %d − %d) ÷ %d. <b>%s</b>" % (A_, B_, AB, n, neg(v)))
        if how == "comp":
            k = R.choice(["coin", "ball"])
            if k == "coin":
                n = R.randint(2, 6)
                v = 1 - Fr(1, 2 ** n)
                return N("동전 %d개를 동시에 던질 때, 적어도 한 개는 앞면이 나올 확률은?" % n, v, [Fr(1, 2 ** n), Fr(n, 2 ** n), Fr(1, 2), 1 - Fr(n, 2 ** n)], "여사건(모두 뒷면)의 확률 1/%d을 1에서 빼요. <b>%s</b>" % (2 ** n, neg(v)))
            r, b = R.randint(3, 7), R.randint(2, 5)
            k2 = R.randint(2, 3)
            if k2 > r:
                return None
            v = 1 - Fr(C(r, k2), C(r + b, k2))
            return N("흰 공 %d개, 검은 공 %d개가 든 주머니에서 공 %d개를 동시에 꺼낼 때, 검은 공이 적어도 한 개 나올 확률은?" % (r, b, k2), v, [Fr(C(r, k2), C(r + b, k2)), Fr(b, r + b), Fr(b * k2, r + b) if Fr(b * k2, r + b) < 1 else v / 2, v - Fr(1, C(r + b, k2))], "1 − (흰 공만 나올 확률 %s ÷ %s). <b>%s</b>" % (sub(r, "C", k2), sub(r + b, "C", k2), neg(v)))
        if how == "card":
            pa, pb = Fr(R.randint(1, 6), 10), Fr(R.randint(1, 6), 10)
            pab = Fr(R.randint(0, int(min(pa, pb) * 10)), 10)
            k = R.choice(["cup", "ab"])
            if k == "cup":
                v = pa + pb - pab
                if v > 1:
                    return None
                return N("두 사건 A, B에 대하여 P(A) = %s, P(B) = %s, P(A ∩ B) = %s일 때, P(A ∪ B)의 값은?" % (neg(pa), neg(pb), neg(pab)), v, [pa + pb if pa + pb <= 1 else v / 2, pa * pb, pa + pb - 2 * pab if pab else v + Fr(1, 10), 1 - v], "P(A) + P(B) − P(A ∩ B) = <b>%s</b>" % neg(v))
            v = pa + pb - pab
            if v > 1:
                return None
            return N("두 사건 A, B에 대하여 P(A) = %s, P(B) = %s, P(A ∪ B) = %s일 때, P(A ∩ B)의 값은?" % (neg(pa), neg(pb), neg(v)), pab, [pa + pb + v - 1 if 0 <= pa + pb + v - 1 <= 1 and pa + pb + v - 1 != pab else pab + Fr(1, 10), pa * pb if pa * pb != pab else pab + Fr(2, 10), v - pa, 1 - pab], "P(A) + P(B) − P(A ∪ B) = <b>%s</b>" % neg(pab))
        C_ = [("두 사건 A, B가 서로 배반사건일 때, P(A ∩ B)의 값은?", "0", ["1", "P(A)P(B)", "P(A) + P(B)"]),
              ("사건 A의 여사건 A<sup>C</sup>의 확률은?", "1 − P(A)", ["P(A)", "−P(A)", "1 + P(A)"]),
              ("어떤 사건 A에 대하여 P(A)의 값의 범위는?", "0 ≤ P(A) ≤ 1", ["0 &lt; P(A) &lt; 1", "P(A) ≥ 1", "−1 ≤ P(A) ≤ 1"]),
              ("반드시 일어나는 사건의 확률은?", "1", ["0", "½", "∞"]),
              ("절대로 일어나지 않는 사건의 확률은?", "0", ["1", "−1", "½"]),
              ("두 사건 A, B가 서로 배반사건일 때, P(A ∪ B)는?", "P(A) + P(B)", ["P(A)P(B)", "P(A) + P(B) − 1", "1"]),
              ("'적어도 하나'가 들어간 확률을 구할 때 편리한 방법은?", "여사건의 확률을 1에서 빼요", ["모든 경우를 곱해요", "확률을 모두 더해요", "1을 더해요"]),
              ("같은 시행을 매우 많이 반복할 때 상대도수가 가까워지는 값은?", "수학적 확률", ["0", "1", "평균"])]
        q, ok, w = R.choice(C_)
        return M(q, ok, w, "<b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ 조건부확률
def cd_main(kinds=("formula", "table", "draw", "total", "bayes")):
    def mk():
        how = R.choice(kinds)
        if how == "formula":
            pa = Fr(R.randint(2, 9), 10)
            pab = Fr(R.randint(1, int(pa * 10) - 1), 10)
            k = R.choice(["BA", "AB"])
            if k == "BA":
                v = pab / pa
                return N("두 사건 A, B에 대하여 P(A) = %s, P(A ∩ B) = %s일 때, P(B|A)의 값은?" % (neg(pa), neg(pab)), v, [pab, pa * pab, pa / pab if pa / pab <= 1 else 1 - v, pa - pab], "P(B|A) = P(A ∩ B) ÷ P(A). <b>%s</b>" % neg(v))
            pba = Fr(R.randint(1, 9), 10)
            v = pa * pba
            return N("P(A) = %s, P(B|A) = %s일 때, P(A ∩ B)의 값은?" % (neg(pa), neg(pba)), v, [pba / pa if pba / pa <= 1 else pa + pba - 1 if pa + pba > 1 else v / 2, pa + pba if pa + pba <= 1 else 1 - v, pba, pa - pba if pa > pba else v + Fr(1, 100)], "P(A ∩ B) = P(A)P(B|A). <b>%s</b>" % neg(v))
        if how == "table":
            a, b, c, d = (R.randint(5, 30) for _ in range(4))
            T = a + b + c + d
            # 행: 남/여, 열: 찬성/반대
            k = R.choice(["m_yes", "yes_m", "f_no", "no_f"])
            tbl = table(["", "찬성", "반대", "합계"], [["남학생", a, b, a + b], ["여학생", c, d, c + d], ["합계", a + c, b + d, T]])
            if k == "m_yes":
                v, q = Fr(a, a + b), "뽑은 학생이 남학생일 때, 이 학생이 찬성했을 확률은?"
                w = [Fr(a, a + c), Fr(a, T), Fr(a + c, T), Fr(b, a + b)]
            elif k == "yes_m":
                v, q = Fr(a, a + c), "뽑은 학생이 찬성했을 때, 이 학생이 남학생일 확률은?"
                w = [Fr(a, a + b), Fr(a, T), Fr(a + b, T), Fr(c, a + c)]
            elif k == "f_no":
                v, q = Fr(d, c + d), "뽑은 학생이 여학생일 때, 이 학생이 반대했을 확률은?"
                w = [Fr(d, b + d), Fr(d, T), Fr(c + d, T), Fr(c, c + d)]
            else:
                v, q = Fr(d, b + d), "뽑은 학생이 반대했을 때, 이 학생이 여학생일 확률은?"
                w = [Fr(d, c + d), Fr(d, T), Fr(b + d, T), Fr(b, b + d)]
            return N("어느 학교 학생 %d명을 대상으로 조사한 결과예요.%s 한 학생을 임의로 뽑을 때, %s" % (T, tbl, q), v, w, "조건에 해당하는 학생 수를 분모로 해요. <b>%s</b>" % neg(v))
        if how == "draw":
            r, b = R.randint(2, 6), R.randint(2, 6)
            n = r + b
            k = R.choice(["rr", "rb", "second"])
            if k == "rr":
                v = Fr(r - 1, n - 1)
                return N("빨간 공 %d개, 파란 공 %d개가 든 주머니에서 공을 한 개씩 두 번 꺼낼 때(꺼낸 공은 넣지 않아요), 첫 번째가 빨간 공이었을 때 두 번째도 빨간 공일 확률은?" % (r, b), v, [Fr(r, n), Fr(r * (r - 1), n * (n - 1)), Fr(r - 1, n), Fr(r, n - 1)], "남은 %d개 중 빨간 공 %d개. <b>%s</b>" % (n - 1, r - 1, neg(v)))
            if k == "rb":
                v = Fr(r, n) * Fr(b, n - 1)
                return N("빨간 공 %d개, 파란 공 %d개가 든 주머니에서 공을 한 개씩 두 번 꺼낼 때(꺼낸 공은 넣지 않아요), 첫 번째는 빨간 공, 두 번째는 파란 공일 확률은?" % (r, b), v, [Fr(r, n) * Fr(b, n), Fr(b, n - 1), Fr(r * b, C(n, 2)) if Fr(r * b, C(n, 2)) != v else v * 2, v + Fr(1, n * (n - 1))], "%s × %s = <b>%s</b>" % (fr(r, n), fr(b, n - 1), neg(v)))
            v = Fr(r, n)
            return N("빨간 공 %d개, 파란 공 %d개가 든 주머니에서 공을 한 개씩 두 번 꺼낼 때(꺼낸 공은 넣지 않아요), 두 번째에 빨간 공이 나올 확률은?" % (r, b), v, [Fr(r - 1, n - 1), Fr(r, n - 1), Fr(r * (r - 1), n * (n - 1)), Fr(b, n)], "(빨, 빨) + (파, 빨) = %s × %s + %s × %s = <b>%s</b>" % (fr(r, n), fr(r - 1, n - 1), fr(b, n), fr(r, n - 1), neg(v)))
        pa = Fr(R.randint(2, 8), 10)
        pba = Fr(R.randint(1, 9), 100)
        pbna = Fr(R.randint(1, 9), 100)
        if pba == pbna:
            return None
        pb = pa * pba + (1 - pa) * pbna
        if how == "total":
            return N("어느 공장에서 기계 A가 전체 제품의 %s%%, 기계 B가 나머지를 만들어요. A 제품의 불량률은 %s%%, B 제품의 불량률은 %s%%예요. 제품 하나를 임의로 골랐을 때 불량품일 확률은?" % (neg(pa * 100), neg(pba * 100), neg(pbna * 100)), pb, [pba + pbna if pba + pbna <= 1 else (pba + pbna) / 2 + Fr(1, 100), (pba + pbna) / 2 if (pba + pbna) / 2 != pb else pb + Fr(1, 100), pa * pba, (1 - pa) * pbna],
                     "%s × %s + %s × %s = <b>%s</b>" % (neg(pa), neg(pba), neg(1 - pa), neg(pbna), neg(pb)))
        v = pa * pba / pb
        return N("어느 공장에서 기계 A가 전체 제품의 %s%%, 기계 B가 나머지를 만들어요. A 제품의 불량률은 %s%%, B 제품의 불량률은 %s%%예요. 임의로 고른 제품이 불량품이었을 때, 이 제품이 A에서 만들어졌을 확률은?" % (neg(pa * 100), neg(pba * 100), neg(pbna * 100)), v, [pa * pba, pba, pa, 1 - v], "P(A ∩ 불량) ÷ P(불량) = %s ÷ %s. <b>%s</b>" % (neg(pa * pba), neg(pb), neg(v)))
    return mk


# ------------------------------------------------------------------ 독립과 곱셈정리
def id_main(kinds=("mul", "check", "rep", "atleast", "concept", "game")):
    def mk():
        how = R.choice(kinds)
        if how == "mul":
            pa, pb = Fr(R.randint(1, 9), 10), Fr(R.randint(1, 9), 10)
            k = R.choice(["ab", "cup", "neither"])
            if k == "ab":
                v = pa * pb
                return N("두 사건 A, B가 서로 독립이고 P(A) = %s, P(B) = %s일 때, P(A ∩ B)의 값은?" % (neg(pa), neg(pb)), v, [pa + pb if pa + pb <= 1 else v + Fr(1, 10), 0, abs(pa - pb) if pa != pb else v + Fr(2, 10), 1 - v], "독립이면 P(A ∩ B) = P(A)P(B). <b>%s</b>" % neg(v))
            if k == "cup":
                v = pa + pb - pa * pb
                return N("두 사건 A, B가 서로 독립이고 P(A) = %s, P(B) = %s일 때, P(A ∪ B)의 값은?" % (neg(pa), neg(pb)), v, [pa + pb if pa + pb <= 1 else v - Fr(1, 100), pa * pb, 1 - pa * pb, v + Fr(1, 100)], "P(A) + P(B) − P(A)P(B). <b>%s</b>" % neg(v))
            v = (1 - pa) * (1 - pb)
            return N("두 사건 A, B가 서로 독립이고 P(A) = %s, P(B) = %s일 때, A와 B가 모두 일어나지 않을 확률은?" % (neg(pa), neg(pb)), v, [1 - pa * pb, 1 - pa - pb if pa + pb < 1 else v + Fr(1, 100), pa * pb, (1 - pa) + (1 - pb) if (1 - pa) + (1 - pb) <= 1 else v / 2], "(1 − %s)(1 − %s) = <b>%s</b>" % (neg(pa), neg(pb), neg(v)))
        if how == "check":
            n = R.choice([6, 8, 10, 12])
            S_ = set(range(1, n + 1))
            A_ = set(x for x in S_ if x % 2 == 0)
            m = R.choice([3, 4, 5])
            B_ = set(x for x in S_ if x <= m) if R.random() < 0.5 else set(x for x in S_ if x % 3 == 0)
            pa, pb, pab = Fr(len(A_), n), Fr(len(B_), n), Fr(len(A_ & B_), n)
            ind = pab == pa * pb
            ok = "독립이에요" if ind else "종속이에요"
            bdesc = "%d 이하의 수" % m if all(x <= m for x in B_) and len(B_) == m else "3의 배수"
            return M("1부터 %d까지의 자연수 중 하나를 뽑을 때, A: 짝수가 나오는 사건, B: %s가 나오는 사건이에요. A와 B는?" % (n, bdesc), ok, ["독립이에요" if not ind else "종속이에요", "배반사건이에요", "알 수 없어요"],
                     "P(A) = %s, P(B) = %s, P(A ∩ B) = %s. P(A)P(B) = %s이므로 <b>%s</b>" % (neg(pa), neg(pb), neg(pab), neg(pa * pb), ok))
        if how == "rep":
            n = R.randint(3, 6)
            k = R.randint(1, n - 1)
            p = R.choice([Fr(1, 2), Fr(1, 3), Fr(1, 6), Fr(2, 3), Fr(1, 4)])
            v = C(n, k) * p ** k * (1 - p) ** (n - k)
            ev = {Fr(1, 2): "동전 한 개를 던져 앞면이 나오는", Fr(1, 6): "주사위 한 개를 던져 1의 눈이 나오는", Fr(1, 3): "주사위 한 개를 던져 3의 배수의 눈이 나오는", Fr(2, 3): "주사위 한 개를 던져 2 이상 5 이하의 눈이 나오는", Fr(1, 4): "확률이 1/4인"}[p]
            return N("%s 시행을 %d번 반복할 때, 그 사건이 정확히 %d번 일어날 확률은?" % (ev, n, k), v, [p ** k * (1 - p) ** (n - k), C(n, k) * p ** k, p ** k, 1 - v], "%s(%s)<sup>%d</sup>(%s)<sup>%d</sup> = <b>%s</b>" % (sub(n, "C", k), neg(p), k, neg(1 - p), n - k, neg(v)))
        if how == "atleast":
            n = R.randint(2, 6)
            p = R.choice([Fr(1, 2), Fr(1, 3), Fr(1, 6), Fr(1, 4), Fr(2, 5), Fr(1, 5), Fr(3, 10)])
            v = 1 - (1 - p) ** n
            return N("한 번의 시도에서 성공할 확률이 %s인 시도를 독립적으로 %d번 할 때, 적어도 한 번 성공할 확률은?" % (neg(p), n), v, [n * p if n * p < 1 else v / 2, p ** n, (1 - p) ** n, 1 - p ** n], "1 − (한 번도 성공하지 못할 확률 (%s)<sup>%d</sup>). <b>%s</b>" % (neg(1 - p), n, neg(v)))
        if how == "game":
            p, q = Fr(R.randint(1, 9), 10), Fr(R.randint(1, 9), 10)
            v = p * (1 - q) + (1 - p) * q
            return N("A, B 두 사람이 각각 과녁을 맞힐 확률이 %s, %s이고 서로 독립이에요. 두 사람이 한 번씩 쏠 때, 한 사람만 맞힐 확률은?" % (neg(p), neg(q)), v, [p * q, 1 - p * q, p + q if p + q <= 1 else v / 2, (1 - p) * (1 - q)], "%s × %s + %s × %s = <b>%s</b>" % (neg(p), neg(1 - q), neg(1 - p), neg(q), neg(v)))
        C_ = [("두 사건 A, B가 서로 독립일 조건은?", "P(A ∩ B) = P(A)P(B)", ["P(A ∩ B) = 0", "P(A ∪ B) = 1", "P(A) = P(B)"]),
              ("P(A) &gt; 0, P(B) &gt; 0인 두 사건 A, B가 서로 배반사건이면?", "A와 B는 종속이에요", ["A와 B는 독립이에요", "P(A ∩ B) = P(A)P(B)", "P(A) = P(B)"]),
              ("A와 B가 서로 독립이면 A와 B<sup>C</sup>는?", "서로 독립이에요", ["서로 종속이에요", "배반사건이에요", "알 수 없어요"]),
              ("A와 B가 서로 독립일 때 P(B|A)는?", "P(B)", ["P(A)", "P(A)P(B)", "1"]),
              ("확률의 곱셈정리로 옳은 것은?", "P(A ∩ B) = P(A)P(B|A)", ["P(A ∩ B) = P(A) + P(B|A)", "P(A ∩ B) = P(B|A) ÷ P(A)", "P(A ∩ B) = P(A|B)P(A)"]),
              ("주사위를 두 번 던질 때 첫 번째와 두 번째 결과는?", "서로 독립이에요", ["서로 종속이에요", "배반사건이에요", "같은 사건이에요"])]
        q, ok, w = R.choice(C_)
        return M(q, ok, w, "<b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ 이산확률변수
def tbl(xs, ps, var="X"):
    return table([var] + [neg(x) for x in xs] + ["합계"], [["P(%s = x)" % var] + [p if isinstance(p, str) else neg(p) for p in ps] + ["1"]])


def dv_main(kinds=("a", "E", "V", "lin", "prob", "sd")):
    def mk():
        how = R.choice(kinds)
        n = R.choice([3, 4])
        xs = sorted(R.sample(range(0, 6), n))
        den = R.choice([6, 8, 10, 12])
        while True:
            parts = [R.randint(1, den - n + 1) for _ in range(n)]
            if sum(parts) == den:
                break
        ps = [Fr(p, den) for p in parts]
        E = sum(x * p for x, p in zip(xs, ps))
        E2 = sum(x * x * p for x, p in zip(xs, ps))
        V = E2 - E * E
        if how == "a":
            i = R.randrange(n)
            shown = [("a" if j == i else ps[j]) for j in range(n)]
            return N("확률변수 X의 확률분포가 다음과 같을 때, 상수 a의 값은?%s" % tbl(xs, shown), ps[i], [1 - ps[i], Fr(1, n), ps[i] * 2, sum(ps[:i] + ps[i + 1:])], "확률의 합이 1이에요. <b>a = %s</b>" % neg(ps[i]))
        if how == "E":
            return N("확률변수 X의 확률분포가 다음과 같을 때, E(X)의 값은?%s" % tbl(xs, ps), E, [Fr(sum(xs), n), E2, E + Fr(1, den), sum(ps) * max(xs) / 2 if sum(ps) * max(xs) / 2 != E else E * 2], "E(X) = Σ x P(X = x) = <b>%s</b>" % neg(E))
        if how == "V":
            return N("확률변수 X의 확률분포가 다음과 같을 때, V(X)의 값은?%s" % tbl(xs, ps), V, [E2, E2 + E * E, E * E, V + Fr(1, den)], "E(X) = %s, E(X²) = %s이므로 V(X) = E(X²) − {E(X)}² = <b>%s</b>" % (neg(E), neg(E2), neg(V)))
        if how == "lin":
            a, b = R.choice([2, 3, -2, 4, 5]), R.randint(-5, 5)
            m, v = R.randint(1, 10), R.randint(1, 9)
            k = R.choice(["E", "V", "s"])
            if k == "E":
                return N("E(X) = %d, V(X) = %d일 때, E(%s)의 값은?" % (m, v, px([a, b], "X")), a * m + b, [a * m, m + b, a * (m + b), a * m - b if b else a * m + 1], "E(aX + b) = aE(X) + b. <b>%s</b>" % neg(a * m + b))
            if k == "V":
                return N("E(X) = %d, V(X) = %d일 때, V(%s)의 값은?" % (m, v, px([a, b], "X")), a * a * v, [a * v + b, a * v, a * a * v + b, abs(a) * v if abs(a) * v != a * a * v else v], "V(aX + b) = a²V(X). <b>%s</b>" % neg(a * a * v))
            sd = R.randint(1, 6)
            return N("σ(X) = %d일 때, σ(%s)의 값은?" % (sd, px([a, b], "X")), abs(a) * sd, [a * a * sd, abs(a) * sd + b if b else abs(a) * sd + 1, sd, a * sd if a < 0 else sd + abs(a)], "σ(aX + b) = |a|σ(X). <b>%s</b>" % neg(abs(a) * sd))
        if how == "prob":
            t = R.choice(xs[1:])
            v = sum(p for x, p in zip(xs, ps) if x >= t)
            return N("확률변수 X의 확률분포가 다음과 같을 때, P(X ≥ %d)의 값은?%s" % (t, tbl(xs, ps)), v, [1 - v if 1 - v != v else v / 2, ps[xs.index(t)], v - ps[xs.index(t)] if v != ps[xs.index(t)] else v + Fr(1, den), sum(p for x, p in zip(xs, ps) if x > t) + Fr(1, den)], "X = %d 이상인 확률을 더해요. <b>%s</b>" % (t, neg(v)))
        # sd: V 가 제곱수일 때
        a2 = R.randint(1, 6)
        Vv = a2 * a2
        Ex = R.randint(1, 8)
        k = R.choice(["sd", "E2"])
        if k == "sd":
            return N("E(X) = %d, E(X²) = %d일 때, σ(X)의 값은?" % (Ex, Vv + Ex * Ex), a2, [Vv, Vv + Ex * Ex, a2 + 1, Ex], "V(X) = %d − %d = %d, σ(X) = √%d. <b>%d</b>" % (Vv + Ex * Ex, Ex * Ex, Vv, Vv, a2))
        return N("E(X) = %d, σ(X) = %d일 때, E(X²)의 값은?" % (Ex, a2), Vv + Ex * Ex, [Vv, Ex * Ex, Vv - Ex * Ex if Vv > Ex * Ex else Vv + Ex, a2 + Ex * Ex], "E(X²) = V(X) + {E(X)}² = %d + %d. <b>%d</b>" % (Vv, Ex * Ex, Vv + Ex * Ex))
    return mk


# ------------------------------------------------------------------ 이항분포
def bd_main(kinds=("ev", "pk", "lin", "find", "word")):
    def mk():
        how = R.choice(kinds)
        n = R.choice([10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 50, 60, 72, 80, 90, 100])
        p = R.choice([Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(1, 5), Fr(1, 6), Fr(2, 3), Fr(3, 4), Fr(2, 5)])
        E, V = n * p, n * p * (1 - p)
        if how == "ev":
            k = R.choice(["E", "V"])
            if k == "E":
                return N("확률변수 X가 이항분포 B(%d, %s)를 따를 때, E(X)의 값은?" % (n, neg(p)), E, [V, n * (1 - p), E + 1, p], "E(X) = np = %d × %s. <b>%s</b>" % (n, neg(p), neg(E)))
            return N("확률변수 X가 이항분포 B(%d, %s)를 따를 때, V(X)의 값은?" % (n, neg(p)), V, [E, n * p * p, V + 1, E * (1 - E) if E * (1 - E) != V else V * 2], "V(X) = np(1 − p) = %d × %s × %s. <b>%s</b>" % (n, neg(p), neg(1 - p), neg(V)))
        if how == "pk":
            n2 = R.randint(3, 6)
            k = R.randint(0, n2)
            p2 = R.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3)])
            v = C(n2, k) * p2 ** k * (1 - p2) ** (n2 - k)
            return N("확률변수 X가 이항분포 B(%d, %s)를 따를 때, P(X = %d)의 값은?" % (n2, neg(p2), k), v, [p2 ** k * (1 - p2) ** (n2 - k) if C(n2, k) != 1 else v * 2, C(n2, k) * p2 ** k, Fr(k, n2), 1 - v], "%s(%s)<sup>%d</sup>(%s)<sup>%d</sup> = <b>%s</b>" % (sub(n2, "C", k), neg(p2), k, neg(1 - p2), n2 - k, neg(v)))
        if how == "lin":
            a, b = R.choice([2, 3, -1, 4]), R.randint(-5, 5)
            k = R.choice(["E", "V"])
            if k == "E":
                return N("확률변수 X가 이항분포 B(%d, %s)를 따를 때, E(%s)의 값은?" % (n, neg(p), px([a, b], "X")), a * E + b, [a * E, E + b, a * V + b, a * (E + b)], "E(X) = %s이므로 %s × %s %s %d. <b>%s</b>" % (neg(E), neg(a), par(E), "+" if b >= 0 else "−", abs(b), neg(a * E + b)))
            return N("확률변수 X가 이항분포 B(%d, %s)를 따를 때, V(%s)의 값은?" % (n, neg(p), px([a, b], "X")), a * a * V, [a * V + b, a * V, a * a * V + b if b else a * a * V + 1, a * a * E], "V(X) = %s이므로 %d × %s. <b>%s</b>" % (neg(V), a * a, par(V), neg(a * a * V)))
        if how == "find":
            k = R.choice(["n", "p"])
            if k == "n":
                return N("확률변수 X가 이항분포 B(n, %s)를 따르고 E(X) = %s일 때, n의 값은?" % (neg(p), neg(E)), n, [E, E / (1 - p), n + 1, V], "np = %s → <b>n = %d</b>" % (neg(E), n))
            return N("확률변수 X가 이항분포 B(%d, p)를 따르고 E(X) = %s일 때, p의 값은? (0 &lt; p &lt; 1)" % (n, neg(E)), p, [1 - p if 1 - p != p else p / 2, E / 100 if E / 100 != p else p * 2, Fr(1, n), p + Fr(1, 10)], "np = %s → <b>p = %s</b>" % (neg(E), neg(p)))
        k = R.choice(["dice", "coin", "seed"])
        if k == "dice":
            n2 = R.choice([30, 36, 60, 72, 90, 120, 180])
            E2, V2 = Fr(n2, 6), Fr(n2 * 5, 36)
            kk = R.choice(["E", "V"])
            return N("주사위 한 개를 %d번 던질 때, 1의 눈이 나오는 횟수를 X라 하면 %s의 값은?" % (n2, "E(X)" if kk == "E" else "V(X)"), E2 if kk == "E" else V2, [V2 if kk == "E" else E2, Fr(n2, 2), Fr(n2, 36), (E2 if kk == "E" else V2) + 1],
                     "X는 B(%d, 1/6)을 따르므로 <b>%s</b>" % (n2, neg(E2 if kk == "E" else V2)))
        if k == "coin":
            n2 = R.choice([16, 36, 64, 100, 144, 196, 256, 400])
            sd = Fr(math.isqrt(n2), 2)
            return N("동전 한 개를 %d번 던질 때, 앞면이 나오는 횟수를 X라 하면 σ(X)의 값은?" % n2, sd, [Fr(n2, 4), Fr(n2, 2), sd * 2, sd + 1], "V(X) = %d × ½ × ½ = %s이므로 <b>σ(X) = %s</b>" % (n2, neg(Fr(n2, 4)), neg(sd)))
        n2 = R.choice([100, 200, 300, 400, 500])
        pp = R.choice([Fr(4, 5), Fr(9, 10), Fr(3, 4), Fr(7, 10)])
        return N("발아율이 %s%%인 씨앗 %d개를 심을 때, 싹이 트는 씨앗의 개수 X의 평균은?" % (neg(pp * 100), n2), n2 * pp, [n2 * (1 - pp), n2 * pp * (1 - pp), pp * 100, n2 * pp + 1], "E(X) = np = %d × %s. <b>%s</b>" % (n2, neg(pp), neg(n2 * pp)), f=lambda t: "%s개" % neg(t))
    return mk


# ------------------------------------------------------------------ 정규분포
ZT = [(Fr(1, 2), "0.1915"), (Fr(1), "0.3413"), (Fr(3, 2), "0.4332"), (Fr(2), "0.4772"), (Fr(5, 2), "0.4938"), (Fr(3), "0.4987")]
ZD = {z: Fr(p) for z, p in [(Fr(1, 2), "0.1915"), (Fr(1), "0.3413"), (Fr(3, 2), "0.4332"), (Fr(2), "0.4772"), (Fr(5, 2), "0.4938"), (Fr(3), "0.4987")]}


def ztable():
    return table(["z"] + ["%.1f" % float(z) for z, _ in ZT], [["P(0 ≤ Z ≤ z)"] + [p for _, p in ZT]])


def d4(x):
    s = "%.4f" % float(x)
    return s.replace("-", "−")


def nm_main(kinds=("std", "prob", "between", "word", "approx", "concept")):
    def mk():
        how = R.choice(kinds)
        m = R.choice([50, 60, 65, 70, 100, 150, 170])
        s = R.choice([2, 4, 5, 8, 10, 12])
        if how == "std":
            z = R.choice([Fr(1, 2), Fr(1), Fr(3, 2), Fr(2), Fr(-1), Fr(-2), Fr(5, 2)])
            x = m + z * s
            if x.denominator != 1:
                return None
            return N("확률변수 X가 정규분포 N(%d, %d²)을 따를 때, X = %s를 표준화한 값 z는?" % (m, s, neg(x)), z, [-z, z * 2, z + Fr(1, 2), z - Fr(1, 2) if z != Fr(1, 2) else z + 1], "z = (X − m) ÷ σ = (%s − %d) ÷ %d. <b>%s</b>" % (neg(x), m, s, ("%.1f" % float(z)).replace("-", "−")),
                     f=lambda v: ("%.1f" % float(v)).replace("-", "−"))
        z, pz = R.choice(list(ZD.items()))
        if how == "prob":
            k = R.choice(["ge", "le", "le_neg"])
            if k == "ge":
                x = m + z * s
                v = Fr(1, 2) - pz
                return M("확률변수 X가 정규분포 N(%d, %d²)을 따를 때, <b>P(X ≥ %s)</b>의 값은? (아래 표준정규분포표를 이용하세요)%s" % (m, s, neg(x), ztable()), d4(v), [d4(pz), d4(Fr(1, 2) + pz), d4(1 - pz), d4(2 * pz)],
                         "z = %s. P(Z ≥ %s) = 0.5 − %s = <b>%s</b>" % (("%.1f" % float(z)), ("%.1f" % float(z)), d4(pz), d4(v)))
            if k == "le":
                x = m + z * s
                v = Fr(1, 2) + pz
                return M("확률변수 X가 정규분포 N(%d, %d²)을 따를 때, <b>P(X ≤ %s)</b>의 값은? (아래 표준정규분포표를 이용하세요)%s" % (m, s, neg(x), ztable()), d4(v), [d4(pz), d4(Fr(1, 2) - pz), d4(1 - pz), d4(2 * pz)],
                         "z = %s. P(Z ≤ %s) = 0.5 + %s = <b>%s</b>" % (("%.1f" % float(z)), ("%.1f" % float(z)), d4(pz), d4(v)))
            x = m - z * s
            v = Fr(1, 2) - pz
            return M("확률변수 X가 정규분포 N(%d, %d²)을 따를 때, <b>P(X ≤ %s)</b>의 값은? (아래 표준정규분포표를 이용하세요)%s" % (m, s, neg(x), ztable()), d4(v), [d4(Fr(1, 2) + pz), d4(pz), d4(1 - pz), d4(2 * pz)],
                     "z = −%s. 대칭이므로 P(Z ≥ %s) = 0.5 − %s = <b>%s</b>" % (("%.1f" % float(z)), ("%.1f" % float(z)), d4(pz), d4(v)))
        if how == "between":
            z2, pz2 = R.choice([(k_, v_) for k_, v_ in ZD.items() if k_ != z])
            k = R.choice(["both", "same"])
            if k == "both":
                v = pz + pz2
                return M("확률변수 X가 정규분포 N(%d, %d²)을 따를 때, <b>P(%s ≤ X ≤ %s)</b>의 값은? (아래 표준정규분포표를 이용하세요)%s" % (m, s, neg(m - z * s), neg(m + z2 * s), ztable()), d4(v), [d4(abs(pz - pz2)), d4(1 - v), d4(pz * 2), d4(pz2 * 2)],
                         "P(−%s ≤ Z ≤ %s) = %s + %s = <b>%s</b>" % (("%.1f" % float(z)), ("%.1f" % float(z2)), d4(pz), d4(pz2), d4(v)))
            lo, hi = min(z, z2), max(z, z2)
            v = ZD[hi] - ZD[lo]
            if (m + lo * s).denominator != 1 or (m + hi * s).denominator != 1:
                return None
            return M("확률변수 X가 정규분포 N(%d, %d²)을 따를 때, <b>P(%s ≤ X ≤ %s)</b>의 값은? (아래 표준정규분포표를 이용하세요)%s" % (m, s, neg(m + lo * s), neg(m + hi * s), ztable()), d4(v), [d4(ZD[hi] + ZD[lo]), d4(ZD[hi]), d4(1 - v), d4(Fr(1, 2) - v)],
                     "P(%s ≤ Z ≤ %s) = %s − %s = <b>%s</b>" % (("%.1f" % float(lo)), ("%.1f" % float(hi)), d4(ZD[hi]), d4(ZD[lo]), d4(v)))
        if how == "word":
            m = R.choice([155, 160, 165, 170, 175])
            s = R.choice([4, 5, 6, 8, 10])
            N_ = R.choice([200, 400, 500, 1000])
            x = m + z * s
            if (x).denominator != 1:
                return None
            v = (Fr(1, 2) - pz) * N_
            ws = [(Fr(1, 2) + pz) * N_, pz * N_, (1 - pz) * N_]
            fm = lambda t: ("%.1f" % float(t)).rstrip("0").rstrip(".") + "명"
            return M("어느 학교 학생 %d명의 키는 평균 %d cm, 표준편차 %d cm인 정규분포를 따른다고 해요. 키가 %s cm 이상인 학생은 약 몇 명일까요? (아래 표준정규분포표를 이용하세요)%s" % (N_, m, s, neg(x), ztable()), fm(v), [fm(t) for t in ws] + [fm(v + 10)],
                     "P(Z ≥ %s) = 0.5 − %s = %s, %d × %s. <b>%s</b>" % (("%.1f" % float(z)), d4(pz), d4(Fr(1, 2) - pz), N_, d4(Fr(1, 2) - pz), fm(v)))
        if how == "approx":
            pairs = [(n_, p_) for n_ in (100, 144, 400, 900, 1600, 2500, 3600) for p_ in (Fr(1, 2), Fr(1, 5), Fr(1, 10), Fr(4, 5), Fr(9, 10)) if (n_ * p_ * (1 - p_)).denominator == 1 and math.isqrt(int(n_ * p_ * (1 - p_))) ** 2 == n_ * p_ * (1 - p_)]
            n, p = R.choice(pairs)
            mu, sd = n * p, Fr(math.isqrt(int(n * p * (1 - p))))
            k = R.choice(["m", "s"])
            if k == "m":
                return N("확률변수 X가 이항분포 B(%d, %s)를 따를 때, n이 충분히 크면 X는 근사적으로 정규분포 N(m, σ²)을 따라요. m의 값은?" % (n, neg(p)), mu, [sd, sd * sd, mu + 1, n], "m = np = <b>%s</b>" % neg(mu))
            return N("확률변수 X가 이항분포 B(%d, %s)를 따를 때, n이 충분히 크면 X는 근사적으로 정규분포 N(m, σ²)을 따라요. σ의 값은?" % (n, neg(p)), sd, [sd * sd, mu, sd * 2, sd + 1], "σ² = np(1 − p) = %s. <b>σ = %s</b>" % (neg(sd * sd), neg(sd)))
        C_ = [("정규분포 N(m, σ²)의 그래프는 어떤 직선에 대하여 대칭일까요?", "x = m", ["x = σ", "x = 0", "y = m"]),
              ("정규분포에서 σ가 커지면 그래프는?", "낮아지고 옆으로 퍼져요", ["높아지고 뾰족해져요", "오른쪽으로 이동해요", "변하지 않아요"]),
              ("정규분포에서 m이 커지면 그래프는?", "오른쪽으로 평행이동해요", ["왼쪽으로 이동해요", "낮아져요", "뾰족해져요"]),
              ("표준정규분포는?", "N(0, 1)", ["N(1, 0)", "N(1, 1)", "N(0, 0)"]),
              ("X가 N(m, σ²)을 따를 때 Z = (X − m)/σ가 따르는 분포는?", "N(0, 1)", ["N(m, σ)", "N(0, σ²)", "N(m, 1)"]),
              ("정규분포의 그래프와 x축 사이의 전체 넓이는?", "1", ["0.5", "m", "σ"]),
              ("P(Z ≥ 0)의 값은?", "0.5", ["0", "1", "0.3413"])]
        q, ok, w = R.choice(C_)
        return M(q, ok, w, "<b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ 표본평균과 추정
def sm_main(kinds=("mean", "var", "sd", "ci95", "ci99", "prop", "concept")):
    def mk():
        how = R.choice(kinds)
        m = R.choice([20, 50, 60, 100, 150, 170, 250])
        s = R.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
        n = R.choice([4, 9, 16, 25, 36, 49, 64, 100, 144])
        rn = math.isqrt(n)
        if how == "mean":
            return N("모평균이 %d, 모표준편차가 %d인 모집단에서 크기가 %d인 표본을 임의추출할 때, 표본평균 X̄의 평균 E(X̄)는?" % (m, s, n), m, [Fr(m, n), Fr(m, rn), m * n, s], "E(X̄) = m = <b>%d</b>" % m)
        if how == "var":
            return N("모평균이 %d, 모표준편차가 %d인 모집단에서 크기가 %d인 표본을 임의추출할 때, 표본평균 X̄의 분산 V(X̄)는?" % (m, s, n), Fr(s * s, n), [Fr(s * s, rn), Fr(s, n), s * s, Fr(s, rn)], "V(X̄) = σ² ÷ n = %d ÷ %d. <b>%s</b>" % (s * s, n, neg(Fr(s * s, n))))
        if how == "sd":
            return N("모표준편차가 %d인 모집단에서 크기가 %d인 표본을 임의추출할 때, 표본평균 X̄의 표준편차 σ(X̄)는?" % (s, n), Fr(s, rn), [Fr(s, n), Fr(s * s, n), s, Fr(s * rn, 1) if s * rn < 1000 else Fr(s, rn) + 1], "σ(X̄) = σ ÷ √n = %d ÷ %d. <b>%s</b>" % (s, rn, neg(Fr(s, rn))))
        if how in ("ci95", "ci99"):
            z = Fr(196, 100) if how == "ci95" else Fr(258, 100)
            xbar = m + R.randint(-5, 5)
            e = z * s / rn
            lo, hi = xbar - e, xbar + e
            f2 = lambda t: ("%.2f" % float(t)).rstrip("0").rstrip(".").replace("-", "−")
            if lo <= 0:
                return None
            ok = "%s ≤ m ≤ %s" % (f2(lo), f2(hi))
            z2 = Fr(258, 100) if how == "ci95" else Fr(196, 100)
            e2 = z2 * s / rn
            e3 = z * s / n
            return M("모표준편차가 %d인 정규분포를 따르는 모집단에서 크기가 %d인 표본을 임의추출하여 표본평균 %d를 얻었어요. 모평균 m의 신뢰도 %d%% 신뢰구간은? (P(|Z| ≤ %s) = 0.%s)" % (s, n, xbar, 95 if how == "ci95" else 99, "1.96" if how == "ci95" else "2.58", "95" if how == "ci95" else "99"), ok,
                     ["%s ≤ m ≤ %s" % (f2(xbar - e2), f2(xbar + e2)), "%s ≤ m ≤ %s" % (f2(xbar - e3), f2(xbar + e3)), "%s ≤ m ≤ %s" % (f2(xbar - z * s), f2(xbar + z * s))],
                     "x̄ ± %s × σ/√n = %d ± %s × %d/%d. <b>%s</b>" % ("1.96" if how == "ci95" else "2.58", xbar, "1.96" if how == "ci95" else "2.58", s, rn, ok))
        if how == "prop":
            n2 = R.choice([100, 400, 900, 1600, 2500])
            p = R.choice([Fr(1, 2), Fr(1, 5), Fr(2, 5), Fr(1, 10), Fr(3, 10)])
            k = R.choice(["E", "V"])
            if k == "E":
                return N("모비율이 %s인 모집단에서 크기가 %d인 표본을 임의추출할 때, 표본비율 p̂의 평균 E(p̂)는?" % (neg(p), n2), p, [p * n2, 1 - p, p / n2, p * (1 - p)], "E(p̂) = p = <b>%s</b>" % neg(p))
            v = p * (1 - p) / n2
            return N("모비율이 %s인 모집단에서 크기가 %d인 표본을 임의추출할 때, 표본비율 p̂의 분산 V(p̂)는?" % (neg(p), n2), v, [p * (1 - p), p / n2, v * n2 / math.isqrt(n2), 1 - v], "V(p̂) = p(1 − p) ÷ n. <b>%s</b>" % neg(v))
        C_ = [("조사 대상 전체를 무엇이라고 할까요?", "모집단", ["표본", "모수", "통계량"]),
              ("모집단의 일부를 뽑아 조사하는 것을 무엇이라고 할까요?", "표본조사", ["전수조사", "모집단", "추정"]),
              ("모집단의 각 대상이 같은 확률로 뽑히도록 추출하는 방법은?", "임의추출", ["편의 추출", "전수조사", "계통 오차"]),
              ("표본의 크기 n이 커지면 표본평균의 표준편차는?", "작아져요", ["커져요", "변하지 않아요", "모표준편차와 같아요"]),
              ("신뢰도를 95%에서 99%로 높이면 신뢰구간의 길이는?", "길어져요", ["짧아져요", "같아요", "0이 돼요"]),
              ("표본의 크기를 4배로 하면 신뢰구간의 길이는?", "½배가 돼요", ["4배가 돼요", "2배가 돼요", "¼배가 돼요"]),
              ("전수조사가 어려운 경우의 예는?", "통조림의 품질 검사", ["학급 학생의 키 조사", "가족의 생일 조사", "반 학생 출석 확인"]),
              ("모평균 m의 신뢰도 95% 신뢰구간의 뜻으로 옳은 것은?", "이런 구간을 많이 만들면 약 95%가 m을 포함해요", ["m이 이 구간에 있을 확률이 정확히 95%예요", "표본의 95%가 이 구간에 있어요", "모집단의 95%가 이 구간에 있어요"])]
        q, ok, w = R.choice(C_)
        return M(q, ok, w, "<b>%s</b>" % ok)
    return mk


# ------------------------------------------------------------------ build
def build(which):
    U = {}
    U["rperm"] = ("permutations-with-repetition", 1, "[12확통01-01]", "중복순열, 같은 것이 있는 순열을 이해하고, 그 순열의 수를 구하는 방법을 설명할 수 있다.",
                  "중복순열과 같은 것이 있는 순열", "중복순열",
                  "고등학교 확률과 통계 중복순열 문제: ₙΠᵣ = nʳ, 중복을 허락하여 자연수 만들기, 함수·우체통·투표의 수, 같은 것이 있는 순열 n!/(p!q!r!), 문자 나열, 최단 경로의 수까지 100문제와 정답·해설.",
                  "ₙΠᵣ = nʳ", "같은 것이 있으면 n!을 같은 것의 개수의 계승으로 나눠요.",
                  ["서로 다른 n개에서 중복을 허락하여 r개를 택해 일렬로 나열하는 것을 <b>중복순열</b>이라 하고 <sub>n</sub>Π<sub>r</sub> = n<sup>r</sup>이에요.",
                   "r은 n보다 커도 돼요. 자리(또는 대상)마다 n가지씩 고르기 때문이에요.",
                   "n개 중 같은 것이 각각 p개, q개, r개 있을 때 일렬로 나열하는 방법의 수는 n! ÷ (p!q!r!)예요.",
                   "바둑판 길의 최단 경로는 →와 ↑를 나열하는 같은 것이 있는 순열이에요."],
                  [("1, 2, 3으로 만드는 네 자리 수(중복 허락)", ["3<sup>4</sup>"], "81개"), ("aabbb를 나열", ["5! ÷ (2!3!)"], "10가지")],
                  [("중복순열을 ₙPᵣ로 센다", "중복을 허락하면 nʳ이에요."), ("nʳ과 rⁿ을 바꾼다", "택하는 대상의 수(n)가 밑, 자리의 수(r)가 지수예요."), ("같은 것이 있는데 n!로 센다", "같은 것끼리 바꾸어도 같으므로 나눠야 해요.")],
                  [("ₙΠᵣ에서 r &gt; n이어도 되나요?", "네, 중복을 허락하므로 가능해요."), ("최단 경로에서 지나면 안 되는 점이 있으면?", "전체에서 그 점을 지나는 경로를 빼요.")],
                  [("중복순열의 수", [(rp_main(("pi",)), 20)]), ("자연수 만들기", [(rp_main(("num",)), 20)]), ("함수·분배의 수", [(rp_main(("func",)), 20)]),
                   ("같은 것이 있는 순열", [(rp_main(("same", "word")), 20)]), ("최단 경로", [(rp_main(("path",)), 14), (rp_main(("word",)), 6)])], 83401)
    U["rcomb"] = ("combinations-with-repetition", 2, "[12확통01-02]", "중복조합을 이해하고, 중복조합의 수를 구하는 방법을 설명할 수 있다.",
                  "중복조합", "중복조합",
                  "고등학교 확률과 통계 중복조합 문제: ₙHᵣ = ₙ₊ᵣ₋₁Cᵣ, 여러 종류에서 중복을 허락하여 고르기, 방정식의 음이 아닌 정수해와 자연수해의 개수, 같은 공을 상자에 넣는 방법까지 100문제와 정답·해설.",
                  "ₙHᵣ = ₙ₊ᵣ₋₁Cᵣ", "x + y + z = n의 음이 아닌 정수해는 ₃Hₙ개",
                  ["서로 다른 n개에서 중복을 허락하여 r개를 택하는 조합을 <b>중복조합</b>이라 하고 <sub>n</sub>H<sub>r</sub> = <sub>n+r−1</sub>C<sub>r</sub>이에요.",
                   "x + y + z = n을 만족하는 음이 아닌 정수 해의 순서쌍은 <sub>3</sub>H<sub>n</sub>개예요.",
                   "자연수 해는 각 변수에서 1씩 빼서 음이 아닌 정수 해로 바꾸어 세요.",
                   "같은 공을 서로 다른 상자에 넣는 방법도 중복조합이에요."],
                  [("₃H₄", ["₆C₄"], "15"), ("x + y + z = 5의 음이 아닌 정수 해", ["₃H₅ = ₇C₅"], "21개")],
                  [("ₙHᵣ = ₙCᵣ로 계산한다", "ₙ₊ᵣ₋₁Cᵣ예요."), ("자연수 해를 음이 아닌 정수 해로 센다", "각 변수에 1씩 먼저 주고 남은 것을 나눠요."), ("같은 공을 nʳ로 센다", "공이 같으면 중복조합이에요.")],
                  [("중복순열과 중복조합의 차이는?", "순서가 있으면 중복순열, 순서가 없으면 중복조합이에요."), ("ₙHᵣ에서 n은?", "고를 수 있는 종류의 수예요.")],
                  [("중복조합의 수", [(rc_main(("h",)), 20)]), ("여러 종류에서 고르기", [(rc_main(("buy",)), 20)]), ("음이 아닌 정수해", [(rc_main(("eq",)), 20)]),
                   ("자연수해", [(rc_main(("pos",)), 20)]), ("공을 상자에 넣기", [(rc_main(("ball",)), 20)])], 83402)
    U["binom"] = ("binomial-theorem", 3, "[12확통01-03]", "이항정리를 이해하고, 이를 활용하여 문제를 해결할 수 있다.",
                  "이항정리와 이항계수의 성질", "이항정리",
                  "고등학교 확률과 통계 이항정리 문제: (a + b)ⁿ의 일반항, 전개식에서 특정한 항의 계수, 상수항, 이항계수의 합 2ⁿ, 파스칼의 삼각형과 ₙCᵣ = ₙCₙ₋ᵣ까지 100문제와 정답·해설.",
                  "(a + b)ⁿ의 일반항 ₙCᵣaⁿ⁻ʳbʳ", "ₙC₀ + ₙC₁ + … + ₙCₙ = 2ⁿ",
                  ["(a + b)<sup>n</sup> = <sub>n</sub>C<sub>0</sub>a<sup>n</sup> + <sub>n</sub>C<sub>1</sub>a<sup>n−1</sup>b + … + <sub>n</sub>C<sub>n</sub>b<sup>n</sup>이에요.",
                   "일반항 <sub>n</sub>C<sub>r</sub>a<sup>n−r</sup>b<sup>r</sup>에서 원하는 차수가 되는 r을 찾아요.",
                   "이항계수의 합은 2<sup>n</sup>, 짝수 번째(홀수 번째) 이항계수의 합은 2<sup>n−1</sup>이에요.",
                   "파스칼의 삼각형: <sub>n</sub>C<sub>r</sub> + <sub>n</sub>C<sub>r+1</sub> = <sub>n+1</sub>C<sub>r+1</sub>"],
                  [("(x + 2)⁵에서 x³의 계수", ["₅C₃ × 2²"], "40"), ("(x + 1/x)⁴의 상수항", ["4 − 2r = 0, r = 2", "₄C₂"], "6")],
                  [("계수에서 b의 거듭제곱을 빠뜨린다", "₅C₃ × 2²처럼 상수도 거듭제곱해요."), ("음수 b의 부호를 놓친다", "(−2)³ = −8처럼 부호까지 계산해요."), ("이항계수의 합을 2n으로 쓴다", "2ⁿ이에요.")],
                  [("이항정리는 어디에 쓰이나요?", "이항분포의 확률 계산과 근삿값 계산에 써요."), ("파스칼의 삼각형의 각 행의 합은?", "2ⁿ이에요.")],
                  [("특정한 항의 계수", [(bn_main(("coef",)), 20)]), ("일반항", [(bn_main(("term",)), 20)]), ("상수항", [(bn_main(("const",)), 12), (bn_main(("coef",)), 8)]),
                   ("이항계수의 합", [(bn_main(("sum",)), 20)]), ("파스칼의 삼각형", [(bn_main(("pascal",)), 20)])], 83403)
    U["prob"] = ("probability-and-addition-rule", 4, "[12확통02-01] [12확통02-02] [12확통02-03]", "확률의 개념을 이해하고 기본 성질을 설명할 수 있다. 확률의 덧셈정리를 이해하고, 이를 활용하여 문제를 해결할 수 있다. 여사건의 확률을 이해하고, 이를 활용하여 문제를 해결할 수 있다.",
                 "확률의 뜻과 덧셈정리, 여사건", "확률의 덧셈정리",
                 "고등학교 확률과 통계 확률 문제: 주사위·공·카드를 이용한 수학적 확률, 확률의 기본 성질, 덧셈정리 P(A ∪ B) = P(A) + P(B) − P(A ∩ B), 배반사건, 여사건을 이용한 '적어도' 확률까지 100문제와 정답·해설.",
                 "합사건은 겹친 부분을 한 번 빼요", "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)",
                 ["표본공간의 각 근원사건이 일어날 가능성이 같을 때 P(A) = n(A) ÷ n(S)예요.",
                  "0 ≤ P(A) ≤ 1, P(S) = 1, P(∅) = 0이에요.",
                  "<b>덧셈정리</b>: P(A ∪ B) = P(A) + P(B) − P(A ∩ B). 배반사건이면 P(A ∪ B) = P(A) + P(B)예요.",
                  "<b>여사건</b>: P(A<sup>C</sup>) = 1 − P(A)"],
                 [("두 주사위의 합이 7", ["6가지 ÷ 36"], "1/6"), ("동전 3개, 적어도 한 개 앞면", ["1 − 1/8"], "7/8")],
                 [("P(A ∪ B)에서 P(A ∩ B)를 빼지 않는다", "겹친 부분을 두 번 세지 않도록 빼요."), ("서로 다른 두 주사위의 경우를 21가지로 센다", "36가지예요."), ("'적어도'를 직접 나누어 세다 빠뜨린다", "여사건을 이용해요.")],
                 [("통계적 확률이란?", "많이 반복한 실험의 상대도수로 정한 확률이에요."), ("배반사건과 여사건의 차이는?", "여사건은 배반사건이면서 합하면 전체가 되는 사건이에요.")],
                 [("주사위와 확률", [(p_main(("dice",)), 20)]), ("공을 꺼내는 확률", [(p_main(("ball",)), 20)]), ("확률의 덧셈정리", [(p_main(("add", "card")), 20)]),
                  ("여사건의 확률", [(p_main(("comp",)), 20)]), ("확률의 기본 성질", [(p_main(("concept",)), 8), (p_main(("card", "add")), 12)])], 83404)
    U["cond"] = ("conditional-probability", 5, "[12확통02-04]", "조건부확률을 이해하고, 이를 실생활과 연결하여 문제를 해결할 수 있다.",
                 "조건부확률", "조건부확률",
                 "고등학교 확률과 통계 조건부확률 문제: P(B|A) = P(A ∩ B)/P(A), 표를 이용한 조건부확률, 꺼낸 공을 넣지 않는 시행, 전확률, 불량품이 특정 기계에서 나왔을 확률까지 100문제와 정답·해설.",
                 "P(B|A) = P(A ∩ B) ÷ P(A)", "조건에 해당하는 것을 새로운 전체(분모)로 봐요.",
                 ["사건 A가 일어났을 때 B가 일어날 확률을 <b>조건부확률</b> P(B|A)라 하고 P(B|A) = P(A ∩ B) ÷ P(A)예요.",
                  "표에서는 조건에 해당하는 행(또는 열)의 합계를 분모로 써요.",
                  "꺼낸 공을 넣지 않으면 두 번째 시행의 확률이 달라져요.",
                  "P(B) = P(A)P(B|A) + P(A<sup>C</sup>)P(B|A<sup>C</sup>)처럼 경우를 나누어 더해요."],
                 [("P(A) = 0.5, P(A ∩ B) = 0.2", ["0.2 ÷ 0.5"], "P(B|A) = 0.4"), ("빨 3, 파 2에서 첫 번째 빨간 공일 때 두 번째도 빨간 공", ["남은 4개 중 빨 2"], "1/2")],
                 [("P(B|A)를 P(A ∩ B) ÷ P(B)로 쓴다", "조건이 되는 A로 나눠요."), ("표에서 전체 인원을 분모로 쓴다", "조건에 맞는 인원이 분모예요."), ("꺼낸 공을 다시 넣은 것처럼 계산한다", "개수가 하나씩 줄어요.")],
                 [("P(B|A)와 P(A|B)는 같나요?", "일반적으로 달라요."), ("조건부확률은 어디에 쓰이나요?", "검사 결과가 양성일 때 실제 병이 있을 확률처럼 정보가 주어진 뒤의 확률을 구할 때 써요.")],
                 [("조건부확률의 계산", [(cd_main(("formula",)), 20)]), ("표를 이용한 조건부확률", [(cd_main(("table",)), 20)]), ("꺼내는 시행", [(cd_main(("draw",)), 20)]),
                  ("전확률", [(cd_main(("total",)), 20)]), ("원인의 확률", [(cd_main(("bayes",)), 20)])], 83405)
    U["indep"] = ("independence-and-multiplication-rule", 6, "[12확통02-05] [12확통02-06]", "사건의 독립과 종속을 이해하고, 이를 판단할 수 있다. 확률의 곱셈정리를 이해하고, 이를 활용하여 문제를 해결할 수 있다.",
                  "사건의 독립과 종속, 곱셈정리", "독립과 곱셈정리",
                  "고등학교 확률과 통계 사건의 독립과 확률의 곱셈정리 문제: 독립의 판정 P(A ∩ B) = P(A)P(B), 독립인 사건의 확률, 독립시행의 확률 ₙCᵣpʳ(1 − p)ⁿ⁻ʳ, 적어도 한 번 성공할 확률까지 100문제와 정답·해설.",
                  "독립: P(A ∩ B) = P(A)P(B)", "독립시행: ₙCᵣpʳ(1 − p)ⁿ⁻ʳ",
                  ["<b>곱셈정리</b>: P(A ∩ B) = P(A)P(B|A)예요.",
                   "P(B|A) = P(B)이면 A와 B는 서로 <b>독립</b>이고, 이때 P(A ∩ B) = P(A)P(B)예요.",
                   "A, B가 독립이면 A와 B<sup>C</sup>, A<sup>C</sup>와 B<sup>C</sup>도 독립이에요.",
                   "확률이 p인 시행을 n번 독립적으로 할 때 r번 일어날 확률은 <sub>n</sub>C<sub>r</sub>p<sup>r</sup>(1 − p)<sup>n−r</sup>이에요."],
                  [("P(A) = 0.4, P(B) = 0.5, 독립", ["0.4 × 0.5"], "P(A ∩ B) = 0.2"), ("동전 4번, 앞면 2번", ["₄C₂(1/2)²(1/2)²"], "3/8")],
                  [("배반사건이면 독립이라고 생각한다", "P(A), P(B) &gt; 0이면 배반사건은 종속이에요."), ("독립시행에서 ₙCᵣ를 빠뜨린다", "어느 회에 일어나는지 고르는 경우를 곱해요."), ("P(A ∪ B)를 P(A)P(B)로 쓴다", "곱은 A ∩ B의 확률이에요.")],
                  [("독립과 배반은 어떻게 다른가요?", "배반은 동시에 일어나지 않는 것, 독립은 서로의 확률에 영향을 주지 않는 것이에요."), ("독립시행의 예는?", "주사위나 동전을 반복해서 던지는 시행이에요.")],
                  [("독립인 사건의 확률", [(id_main(("mul",)), 20)]), ("독립과 종속의 판정", [(id_main(("check",)), 10), (id_main(("concept",)), 6), (id_main(("mul",)), 4)]), ("독립시행의 확률", [(id_main(("rep",)), 20)]),
                   ("적어도 한 번", [(id_main(("atleast",)), 20)]), ("곱셈정리의 활용", [(id_main(("game",)), 14), (id_main(("rep",)), 6)])], 83406)
    U["drv"] = ("discrete-random-variables", 7, "[12확통03-01] [12확통03-02]", "확률변수와 확률분포의 뜻을 설명할 수 있다. 이산확률변수의 기댓값(평균)과 표준편차를 구할 수 있다.",
                "이산확률변수의 평균, 분산, 표준편차", "이산확률변수",
                "고등학교 확률과 통계 이산확률변수 문제: 확률분포표와 확률의 합, 기댓값 E(X), 분산 V(X) = E(X²) − {E(X)}², 표준편차, E(aX + b), V(aX + b), σ(aX + b)까지 100문제와 정답·해설.",
                "V(X) = E(X²) − {E(X)}²", "E(aX + b) = aE(X) + b, V(aX + b) = a²V(X)",
                ["확률변수 X가 가질 수 있는 값이 셀 수 있을 때 <b>이산확률변수</b>라 하고, 확률의 합은 1이에요.",
                 "E(X) = Σx P(X = x), V(X) = E(X²) − {E(X)}², σ(X) = √V(X)",
                 "E(aX + b) = aE(X) + b, V(aX + b) = a²V(X), σ(aX + b) = |a|σ(X)",
                 "b는 퍼진 정도에 영향을 주지 않으므로 분산·표준편차에서 사라져요."],
                [("X: 0, 1, 2 / P: 1/4, 1/2, 1/4", ["E = 1", "E(X²) = 3/2"], "V(X) = 1/2"), ("V(X) = 4, V(3X − 1)", ["3² × 4"], "36")],
                [("V(aX + b) = aV(X) + b", "a²V(X)예요."), ("분산을 E(X²)로 답한다", "{E(X)}²을 빼요."), ("σ(−2X) = −2σ(X)", "표준편차는 |a|를 곱해요.")],
                [("기댓값은 실제로 나오는 값인가요?", "많이 반복했을 때의 평균값이에요. 실제로 나오지 않는 값일 수도 있어요."), ("연속확률변수는?", "키, 시간처럼 구간의 모든 값을 갖는 확률변수예요.")],
                [("확률분포", [(dv_main(("a", "prob")), 20)]), ("기댓값", [(dv_main(("E",)), 20)]), ("분산", [(dv_main(("V",)), 20)]),
                 ("표준편차", [(dv_main(("sd",)), 20)]), ("E(aX + b)와 V(aX + b)", [(dv_main(("lin",)), 20)])], 83407)
    U["bdist"] = ("binomial-distribution", 8, "[12확통03-03]", "이항분포의 뜻과 성질을 이해하고, 평균과 표준편차를 구할 수 있다.",
                  "이항분포의 평균과 분산", "이항분포",
                  "고등학교 확률과 통계 이항분포 문제: B(n, p)의 확률 P(X = r), 평균 np, 분산 np(1 − p), 표준편차, 주사위·동전·발아율 문제, 평균으로 n이나 p 구하기까지 100문제와 정답·해설.",
                  "B(n, p)의 평균은 np", "분산은 np(1 − p), P(X = r) = ₙCᵣpʳ(1 − p)ⁿ⁻ʳ",
                  ["확률이 p인 시행을 n번 독립적으로 할 때 그 사건이 일어나는 횟수 X는 <b>이항분포</b> B(n, p)를 따라요.",
                   "P(X = r) = <sub>n</sub>C<sub>r</sub>p<sup>r</sup>(1 − p)<sup>n−r</sup> (r = 0, 1, …, n)",
                   "E(X) = np, V(X) = np(1 − p), σ(X) = √(np(1 − p))",
                   "E(aX + b), V(aX + b)는 이산확률변수의 성질을 그대로 써요."],
                  [("B(30, 1/3)", ["E = 10", "V = 30 × 1/3 × 2/3"], "E(X) = 10, V(X) = 20/3"), ("주사위 60번, 6의 눈 횟수", ["B(60, 1/6)"], "평균 10")],
                  [("V(X) = np로 쓴다", "(1 − p)를 곱해요."), ("p와 1 − p를 바꾼다", "구하는 사건의 확률이 p예요."), ("σ(X)를 np(1 − p)로 답한다", "√를 씌워요.")],
                  [("이항분포의 그래프는?", "n이 크면 평균 np 근처에서 가장 높은 종 모양이에요."), ("n이 크면 어떤 분포에 가까워지나요?", "정규분포 N(np, np(1 − p))에 가까워져요.")],
                  [("평균과 분산", [(bd_main(("ev",)), 20)]), ("P(X = r)", [(bd_main(("pk",)), 20)]), ("E(aX + b)와 V(aX + b)", [(bd_main(("lin",)), 20)]),
                   ("n과 p 구하기", [(bd_main(("find",)), 20)]), ("실생활 문제", [(bd_main(("word",)), 20)])], 83408)
    U["norm"] = ("normal-distribution", 9, "[12확통03-04]", "정규분포의 뜻과 성질을 이해하고, 이항분포와의 관계를 설명할 수 있다.",
                 "정규분포와 표준정규분포", "정규분포",
                 "고등학교 확률과 통계 정규분포 문제: 정규분포 곡선의 성질, 표준화 Z = (X − m)/σ, 표준정규분포표를 이용한 확률, 실생활 문제, 이항분포의 정규분포 근사까지 100문제와 정답·해설.",
                 "Z = (X − m) ÷ σ는 N(0, 1)", "그래프는 x = m에 대하여 대칭이에요.",
                 ["정규분포 N(m, σ²)의 그래프는 x = m에 대하여 대칭인 종 모양이고, 곡선과 x축 사이의 넓이는 1이에요.",
                  "Z = (X − m) ÷ σ로 표준화하면 Z는 표준정규분포 N(0, 1)을 따라요.",
                  "표준정규분포표의 P(0 ≤ Z ≤ z)와 대칭성, P(Z ≥ 0) = 0.5를 이용해 확률을 구해요.",
                  "n이 충분히 크면 B(n, p)는 N(np, np(1 − p))에 가까워져요."],
                 [("N(50, 4²), P(X ≥ 58)", ["z = 2", "0.5 − 0.4772"], "0.0228"), ("N(70, 5²), P(65 ≤ X ≤ 80)", ["P(−1 ≤ Z ≤ 2) = 0.3413 + 0.4772"], "0.8185")],
                 [("표준화할 때 σ²으로 나눈다", "표준편차 σ로 나눠요."), ("P(Z ≥ z)를 표의 값 그대로 쓴다", "0.5에서 표의 값을 빼요."), ("음수 z의 확률을 음수로 쓴다", "대칭을 이용해 양수 z로 바꿔요.")],
                 [("정규분포는 어디에 쓰이나요?", "키, 시험 점수, 제품의 무게처럼 평균 근처에 많이 모이는 자료에 써요."), ("표에 없는 z는?", "더 자세한 표나 공학 도구를 이용해요.")],
                 [("표준화", [(nm_main(("std",)), 20)]), ("표준정규분포표 읽기", [(nm_main(("prob",)), 20)]), ("구간의 확률", [(nm_main(("between",)), 20)]),
                  ("실생활 문제", [(nm_main(("word",)), 20)]), ("정규분포의 성질과 근사", [(nm_main(("concept",)), 7), (nm_main(("approx",)), 13)])], 83409)
    U["samp"] = ("sampling-and-estimation", 10, "[12확통03-05] [12확통03-06] [12확통03-07]", "모집단과 표본의 뜻을 알고, 표본추출의 방법을 설명할 수 있다. 표본평균과 모평균, 표본비율과 모비율의 관계를 이해하고 설명할 수 있다. 공학 도구를 이용하여 모평균 및 모비율을 추정하고 그 결과를 해석할 수 있다.",
                 "표본평균의 분포와 모평균의 추정", "표본평균과 추정",
                 "고등학교 확률과 통계 통계적 추정 문제: 모집단과 표본, 임의추출, 표본평균의 평균·분산·표준편차, 표본비율의 평균과 분산, 모평균의 신뢰도 95%·99% 신뢰구간까지 100문제와 정답·해설.",
                 "E(X̄) = m, σ(X̄) = σ ÷ √n", "95% 신뢰구간: x̄ ± 1.96 × σ/√n",
                 ["조사 대상 전체를 <b>모집단</b>, 그 일부를 <b>표본</b>이라 하고, 같은 확률로 뽑는 것을 임의추출이라고 해요.",
                  "모평균 m, 모표준편차 σ인 모집단에서 크기 n인 표본의 표본평균 X̄는 E(X̄) = m, V(X̄) = σ²/n, σ(X̄) = σ/√n이에요.",
                  "모비율 p에 대하여 표본비율 p̂은 E(p̂) = p, V(p̂) = p(1 − p)/n이에요.",
                  "모평균의 신뢰구간: 신뢰도 95%는 x̄ ± 1.96σ/√n, 99%는 x̄ ± 2.58σ/√n이에요."],
                 [("σ = 10, n = 25", ["σ(X̄) = 10 ÷ 5"], "2"), ("x̄ = 50, σ = 6, n = 36, 95%", ["50 ± 1.96 × 1"], "48.04 ≤ m ≤ 51.96")],
                 [("σ(X̄) = σ ÷ n으로 쓴다", "√n으로 나눠요."), ("신뢰도 95%에 2.58을 쓴다", "95%는 1.96, 99%는 2.58이에요."), ("E(X̄)를 m ÷ n으로 쓴다", "표본평균의 평균은 모평균 m과 같아요.")],
                 [("표본의 크기를 키우면?", "표본평균이 모평균 근처에 더 모이고 신뢰구간이 짧아져요."), ("공학 도구는 왜 쓰나요?", "큰 자료의 평균·표준편차와 신뢰구간을 빠르고 정확하게 계산할 수 있어요.")],
                 [("표본평균의 평균과 분산", [(sm_main(("mean", "var")), 20)]), ("표본평균의 표준편차", [(sm_main(("sd",)), 20)]), ("신뢰도 95% 신뢰구간", [(sm_main(("ci95",)), 20)]),
                  ("신뢰도 99% 신뢰구간", [(sm_main(("ci99",)), 20)]), ("표본비율과 표본조사", [(sm_main(("prop",)), 12), (sm_main(("concept",)), 8)])], 83410)
    t = U[which]
    slug, sort, code, std, title, short, meta, kb, ks, think, ex_, mist, faq, spec, seed = t
    return unit(G, slug, sort, code, std, title, short, meta, kb, ks, think, ex_, mist, faq, spec, seed)
