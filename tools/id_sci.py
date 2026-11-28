# -*- coding: utf-8 -*-
"""
Indonesia / IPA（Kurikulum Merdeka、Capaian Pembelajaran IPA・IPAS）。country `id`、subject `science`。
  grade: kelas-3〜kelas-6（SD、IPAS のうち IPA の章）、kelas-7〜kelas-9（SMP、IPA）、kelas-10（SMA、IPA Fase E）、
         kelas-11・kelas-12（SMA Fase F。1 つの学年ページに Fisika・Kimia・Biologi が並ぶ（domain が科目名））
  単元: id_s3（Kelas 3–4）・id_s5（5–6）・id_s7・id_s8・id_s9・id_s10・id_s11・id_s12 の UNITS(g)
  H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=, bank=, s4=)
    T は 3 つの表：(セット名, rows, fwd, back[, extra]) か (セット名, {グループ: [物]})。fwd は「{k}」、back は「{v}」を含む問題文
    TFt は正しい文、TFf は (まちがいの文, 正しくは)、topic は「Pernyataan yang benar tentang … adalah」の「…」
  python3 id_sci.py kelas-3 [slug|番号 …]   seed は 86000 + 100 × kelas + 番号
"""
import re
import sys
import copy
import importlib
from sci_common import Unit, item
from ws_common import write_unit
import id_common

UPDATED = "2026-11-28"
STD_URL = id_common.STD_URL
GRADES = {"kelas-%d" % n: n for n in range(3, 13)}
MODULE = {"kelas-3": "id_s3", "kelas-4": "id_s3", "kelas-5": "id_s5", "kelas-6": "id_s5", "kelas-7": "id_s7", "kelas-8": "id_s8",
          "kelas-9": "id_s9", "kelas-10": "id_s10", "kelas-11": "id_s11", "kelas-12": "id_s12"}
DOM = {"L": "Makhluk Hidup", "M": "Zat dan Perubahannya", "E": "Energi, Gaya, dan Gerak", "S": "Bumi dan Antariksa",
       "X": "Sains dan Lingkungan", "F": "Fisika", "K": "Kimia", "B": "Biologi"}
TOPICS = {"matter", "forces-and-motion", "energy", "waves-and-light", "living-things-and-ecosystems", "earth-and-space", "earths-systems", "working-scientifically"}
BAD = re.compile(r"[぀-ヿ㐀-鿿豈-﫿가-힯]")


def fase(n):
    return "Fase B" if n <= 4 else "Fase C" if n <= 6 else "Fase D" if n <= 9 else "Fase E" if n == 10 else "Fase F"


def school(n):
    return "SD" if n <= 6 else "SMP" if n <= 9 else "SMA"


def _txt(s):
    return re.sub(r"<[^>]+>", "", s)


def ok_text(s, where):
    t = _txt(s)
    assert not BAD.search(t), ("CJK", where, t[:80])
    assert "\\" not in s, where
    assert "  " not in t.strip(), ("spasi", where, t[:80])
    assert " ," not in t and " ." not in t.replace(" ...", ""), ("tanda baca", where, t[:80])
    return s


def esc(t):
    """< > yang bukan tag HTML → &lt; &gt;"""
    return t.replace("< ", "&lt; ").replace(" >", " &gt;").replace("...", "…")


def it(q, a, wrong, e):
    return item(q, a, list(wrong), e)


# ------------------------------------------------------------ angka（titik ribuan, koma desimal）
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _id(s):
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def sci(x, d=3):
    m, e = (("%." + str(d - 1) + "e") % x).split("e")
    m = m.rstrip("0").rstrip(".") if "." in m else m
    return ("%s × 10%s" % (_id(m), str(int(e)).translate(SUP))).replace("-", "−")


def num(x, d=3):
    """angka penting d（angka 0 di belakang dibuang）。1.000 ke atas pakai titik, desimal pakai koma。≥ 10⁶ atau < 10⁻³ ditulis × 10ⁿ"""
    if x != 0 and (abs(x) >= 1e6 or abs(x) < 1e-3):
        return sci(x, d)
    if isinstance(x, int) or float(x).is_integer():
        s = "{:,}".format(int(round(x)))
    else:
        s = ("%." + str(d) + "g") % x
        if "e" in s:
            s = (("%." + str(d) + "f") % x).rstrip("0").rstrip(".")
    return _id(s).replace("-", "−")


def nq(q, ans, wrongs, unit, e, d=3):
    """jawaban angka。wrongs = kesalahan yang sering terjadi（sama, negatif, 0 dibuang）。kurang dari 3 → None"""
    a = num(ans, d)
    out = []
    for w in wrongs:
        if w is None:
            continue
        try:
            s = num(w, d)
        except (TypeError, ValueError, OverflowError):
            continue
        if s != a and s not in out and not s.startswith("−") and s != "0":
            out.append(s)
    if len(out) < 3:
        return None
    u = ("" if unit in ("°", "%") else " ") + unit if unit else ""
    return it(q, a + u, [x + u for x in out[:3]], e)


# ------------------------------------------------------------ bagian soal
class K:
    def __init__(self, R):
        self.R = R

    def P(self, rows, fwd, back=None, fe=None, be=None, match=True, sep=" – ", extra=()):
        """rows: [(k, v)] atau [(k, v, tag)]。dengan tag, pengecoh hanya diambil dari baris dengan tag yang sama"""
        R = self
        tag = {}
        for r in rows:
            tag[(r[0], r[1])] = r[2] if len(r) > 2 else None
        rows = [(r[0], r[1]) for r in rows]
        tk = {r[0]: tag[r] for r in rows}
        tv = {r[1]: tag[r] for r in rows}
        keys = sorted({k for k, _ in rows})
        vals = sorted({v for _, v in rows})
        good = set(rows)

        def bad_pairs(n):
            out = set()
            for _ in range(80):
                k = R.R.choice(keys)
                v = R.R.choice([x for x in vals if tv[x] == tk[k]])
                if (k, v) not in good:
                    out.add((k, v))
                if len(out) >= n:
                    break
            return sorted(out)

        def dot(e):
            return e if e.endswith(".") else e + "."

        def mk():
            k, v = R.R.choice(rows)
            t = tag[(k, v)]
            same = {vv for kk, vv in rows if kk == k}
            r = R.R.random()
            if match and r < 0.25 and len(rows) >= 4:
                if R.R.random() < 0.5:
                    w = bad_pairs(3)
                    if len(w) < 3 or len({a for a, _ in w} | {k}) < 4:
                        return None
                    return it("Manakah pasangan yang benar?", k + sep + v, [a + sep + b for a, b in w], dot((fe or "{k}: {v}").format(k=k, v=v)))
                b = bad_pairs(1)
                if not b:
                    return None
                bk, bv = b[0]
                ok = [p for p in rows if p[0] != bk]
                if len(ok) < 3:
                    return None
                w = R.R.sample(ok, 3)
                right = [vv for kk, vv in rows if kk == bk]
                return it("Manakah pasangan yang salah?", bk + sep + bv, [a + sep + c for a, c in w], "Pasangan yang benar untuk ‘%s’ adalah ‘%s’." % (bk, right[0]))
            if back and r < 0.6:
                kk = {a for a, b in rows if b == v}
                w = [x for x in keys if x not in kk and tk[x] == t]
                if len(w) < 3:
                    return None
                return it(back.format(v=v), k, R.R.sample(w, 3), dot((be or fe or "{k}: {v}").format(k=k, v=v)))
            w = [x for x in vals if x not in same and tv[x] == t] + [x for x in extra if x not in same]
            if len(w) < 3:
                return None
            return it(fwd.format(k=k), v, R.R.sample(w, 3), dot((fe or "{k}: {v}").format(k=k, v=v)))
        return mk

    def G(self, groups, pos="Manakah yang termasuk {g}?", neg="Manakah yang tidak termasuk {g}?"):
        R = self
        names = sorted(groups)

        def mk():
            g = R.R.choice(names)
            mine = groups[g]
            other = [(h, x) for h in names if h != g for x in groups[h] if x not in mine]
            if neg and R.R.random() < 0.4 and len(mine) >= 3:
                h, a = R.R.choice(other)
                return it(neg.format(g=g), a, R.R.sample(mine, 3), "%s termasuk %s." % (a[0].upper() + a[1:], h))
            a = R.R.choice(mine)
            ws = sorted({x for _, x in other})
            if len(ws) < 3:
                return None
            return it(pos.format(g=g), a, R.R.sample(ws, 3), "%s termasuk %s." % (a[0].upper() + a[1:], g))
        return mk

    def TF(self, true, false, topic):
        R = self

        def mk():
            if R.R.random() < 0.5:
                a = R.R.choice(true)
                w = [f for f, _ in R.R.sample(false, 3)]
                stem = R.R.choice(["Pernyataan yang benar tentang %s adalah ...", "Manakah pernyataan yang benar tentang %s?"]) % topic
                return it(stem, a, w, a)
            f, c = R.R.choice(false)
            w = R.R.sample(true, 3)
            stem = R.R.choice(["Pernyataan yang salah tentang %s adalah ...", "Manakah pernyataan yang tidak benar tentang %s?"]) % topic
            return it(stem, f, w, "Pernyataan ‘%s’ salah. %s" % (f.rstrip("."), c))
        return mk

    def B(self, rows):
        its = [it(*r) for r in rows]
        R = self

        def mk():
            return copy.deepcopy(R.R.choice(its))
        mk.n = len(its)
        return mk

    def F(self, fn):
        R = self

        def mk():
            return fn(R.R)
        return mk


def H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=None, bank=None, s4=None):
    assert len(T) == 3 and tp in TOPICS, slug
    for s in TFt + [a for a, _ in TFf]:
        assert s.endswith("."), (slug, s)

    def part(K_, t):
        if isinstance(t[1], dict):
            return K_.G(t[1])
        name, rows, fwd, back = t[:4]
        return K_.P(rows, fwd, back, extra=t[4] if len(t) > 4 else ())

    def sets(K_):
        out = [(t[0], [(part(K_, t), 20)]) for t in T]
        if calc and bank:
            mix = [(K_.F(calc), 12), (K_.B(bank), min(8, len(bank) - 3))]
            mix.append((part(K_, T[0]), 20 - sum(n for _, n in mix)))
        elif calc:
            mix = [(K_.F(calc), 15), (part(K_, T[1]), 5)]
        elif bank:
            n = min(20, len(bank) - 3)
            mix = [(K_.B(bank), n)] + ([(part(K_, T[1]), 20 - n)] if n < 20 else [])
        else:
            mix = [(part(K_, T[0]), 7), (part(K_, T[1]), 7), (part(K_, T[2]), 6)]
        out.append((s4 or ("Hitungan dan penerapan" if calc else "Latihan campuran"), mix))
        out.append(("Benar atau salah?", [(K_.TF(TFt, TFf, topic), 20)]))
        return out
    return dict(dom=dom, slug=slug, title=title, short=short, std=std, what=what, kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets, tp=tp)


def seed_of(n, sort):
    return 86000 + 100 * n + sort


def build(grade, u, sort):
    n = GRADES[grade]
    U_ = Unit(seed_of(n, sort))
    sets = U_.sets(u["sets"](K(U_.R)))
    for s in sets:
        for x in s["items"]:
            x["q"], x["e"] = esc(x["q"]), esc(x["e"])
            x["c"] = [esc(c) for c in x["c"]]
            for t in [x["q"], x["e"]] + x["c"]:
                ok_text(t, u["slug"])
    ex = [id_common.example(esc(q), [esc(t) for t in st], esc(a)) for q, st, a in u["ex"]]
    body = id_common.lesson([esc(t) for t in u["think"]], ex, [(esc(a), esc(b)) for a, b in u["mist"]])
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["std"], u["what"], body) + tuple(a + b for a, b in u["faq"]):
        ok_text(s, u["slug"])
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["what"]):
        assert "<" not in s, s
    assert len(u["title"]) <= 60 and len(u["kb"]) <= 60 and len(u["ks"]) <= 150, (u["slug"], len(u["title"]), len(u["kb"]), len(u["ks"]))
    dom = DOM[u["dom"]]
    subj = "IPAS" if n <= 6 else ("IPA" if n <= 10 else dom)
    sch = school(n)
    seo = "%s Kelas %d %s: Latihan Soal %s dengan Kunci Jawaban" % (u["short"], n, sch, subj)
    write_unit("id", "science", grade, {
        "slug": u["slug"], "title": u["title"], "seo_title": seo,
        "short_title": u["short"], "domain": dom, "standard_code": "%s · %s" % (fase(n), dom),
        "standard_url": STD_URL,
        "standard_text": u["std"] + " (ringkasan Capaian Pembelajaran %s Kurikulum Merdeka, %s)" % ("IPAS" if n <= 6 else ("IPA" if n <= 10 else dom), fase(n)),
        "meta_desc": "Latihan soal %s Kelas %d %s tentang %s: %s. 100 soal online dengan pembahasan dan lembar kerja siap cetak dengan kunci jawaban." % (subj, n, sch, u["short"].lower() if u["short"][:2] != u["short"][:2].upper() else u["short"], u["what"]),
        "key_big": u["kb"], "key_sub": u["ks"], "body_html": body,
        "faq": [{"q": q, "a": a} for q, a in u["faq"]], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


def units(grade):
    m = importlib.import_module(MODULE[grade])
    return m.UNITS(grade)


def main():
    grade = sys.argv[1]
    only = sys.argv[2:]
    for i, u in enumerate(units(grade)):
        if only and u["slug"] not in only and str(i + 1) not in only:
            continue
        build(grade, u, i + 1)
        print("wrote", grade, u["slug"])


if __name__ == "__main__":
    import id_sci
    id_sci.main()
