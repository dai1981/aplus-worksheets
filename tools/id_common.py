# -*- coding: utf-8 -*-
"""
Indonesia (Kurikulum Merdeka, Capaian Pembelajaran Matematika, Keputusan Kepala BSKAP No. 046/H/KR/2025)
の単元生成の共通部品。de_common の上に作る。
・文はインドネシア語。子ども向けに短い文、「kamu」で話しかける
・数: 1.000 から点で区切る（4.536、10.000）。小数はコンマ（0,5）
・記号: 3 × 4、12 : 3（Buku Siswa と同じ）、17 : 5 = 3 sisa 2
・お金: Rp6.750
・HTML の属性はシングルクォート、バックスラッシュなし
"""
import re
import de_common as D
from ws_common import (fig, svg_wrap, text, line, balance, write_unit, fr,   # noqa: F401
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT)

UPDATED = "2026-11-25"
STD_URL = "https://internal-portal.kemdikbud.go.id/download/file/1933"
DOMAIN = {
    "B": "Bilangan",
    "A": "Aljabar",
    "P": "Pengukuran",
    "G": "Geometri",
    "D": "Analisis Data dan Peluang",
}
NAMES = ["Asep", "Azizah", "Slamet", "Helen", "Putu", "Karel", "Andi", "Candra", "Tono", "Tini", "Wiwin",
         "Ali", "Nazilla", "Tiara", "Dayu", "Made", "Siti", "Beni", "Lina", "Rudi", "Dewi", "Agus", "Rina", "Yosef"]
NB = " "


# ------------------------------------------------------------ numbers
def num(n):
    """1000 → 1.000、10000 → 10.000"""
    n = int(n)
    s = str(abs(n))
    g = []
    while len(s) > 3:
        g.insert(0, s[-3:])
        s = s[:-3]
    g.insert(0, s)
    return ("−" if n < 0 else "") + ".".join(g)


def dec(v, places=None):
    """0,5 / 1,25"""
    if places is None:
        s = ("%.3f" % v).rstrip("0").rstrip(".")
    else:
        s = ("%." + str(places) + "f") % v
    ip, _, fp = s.partition(".")
    return num(int(ip)) + ("," + fp if fp else "")


def rp(n):
    return "Rp" + num(n)


def u(v, unit):
    return "%s%s%s" % (num(v) if isinstance(v, int) else v, NB, unit)


# de_common の絵（数直線・棒グラフ）は D.num を使うので、インドネシア式に替える
D.num = num


class Kids:
    def __init__(self, rnd):
        self.pool = list(NAMES)
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def two(self):
        a = self.next()
        b = self.next()
        return a, b


# ------------------------------------------------------------ questions
def mcq(q, correct, cands, e):
    """4 択。誤答が足りないときは近い数で補う（数の形は num の点区切り）"""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or c.startswith("-") or c.startswith("−"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3 and "<" not in correct:
        m = re.match(r"^(.*?)(\d(?:\d|\.(?=\d{3}))*)([^\d]*)$", correct)
        if m:
            v = int(m.group(2).replace(".", ""))
            st = 1
            while v and v % (st * 10) == 0 and st < 1000:
                st *= 10
            for d in (st, -st, 2 * st, -2 * st, 10 * st, -10 * st, 3 * st):
                nv = v + d
                if nv <= 0:
                    continue
                c = "%s%s%s" % (m.group(1), num(nv), m.group(3))
                if c not in seen:
                    seen.add(c)
                    pick.append(c)
                if len(pick) == 3:
                    break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


pick_unique = D.pick_unique
mix = D.mix
table = D.table


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Contoh</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Jawaban: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist, extra=""):
    """body_html：Cara berpikir → Contoh → Kesalahan yang sering terjadi"""
    h = "<h2>Cara berpikir</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += extra
    h += "".join(examples)
    h += "<h2>Kesalahan yang sering terjadi</h2>" + table(["Kesalahan", "Yang benar"], mist)
    return h


plain_text = D.plain_text


def make_unit(rnd, slug, dom, std_text, title, short_title, meta_desc, key_big, key_sub,
              body_html, faq, sets, sort, grade="kelas-4", fase="Fase B"):
    sets = [{"title": t, "items": items} for t, items in sets]
    assert len(sets) == 5, slug
    allq = set()
    for s in sets:
        assert len(s["items"]) == 20, (slug, s["title"], len(s["items"]))
        for it in s["items"]:
            k = re.sub(r"\s+", " ", it["q"])
            assert k not in allq, ("duplicate question", slug, k)
            allq.add(k)
    balance(sets, rnd)
    gname = "Kelas " + grade.split("-")[1]
    seo_title = "%s %s SD: Latihan Soal dan Lembar Kerja dengan Kunci Jawaban" % (short_title, gname)
    title, seo_title, short_title, meta_desc, key_big, key_sub = map(plain_text, (title, seo_title, short_title, meta_desc, key_big, key_sub))
    assert len(key_big) <= 40 and len(key_sub) <= 60, (slug, key_big, key_sub)
    write_unit("id", "matematika", grade, {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": DOMAIN[dom], "standard_code": "%s · %s" % (fase, DOMAIN[dom]), "standard_url": STD_URL,
        "standard_text": std_text, "meta_desc": meta_desc, "key_big": key_big, "key_sub": key_sub,
        "body_html": body_html, "faq": faq, "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


# ------------------------------------------------------------ pictures
wrap = D.wrap


def garis_bilangan(lo, hi, step, marks=(), labels=None, every=None, width=460):
    return D.zahlenstrahl(lo, hi, step, marks, labels, "garis bilangan", every, width)


def nilai_tempat(n, cols=4):
    """tabel nilai tempat: Ribuan Ratusan Puluhan Satuan"""
    head = ["Puluh ribuan", "Ribuan", "Ratusan", "Puluhan", "Satuan"][-cols:]
    ds = str(n).rjust(cols, "0")[-cols:]
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead>"
            "<tbody><tr>%s</tr></tbody></table>" % ("".join("<th>%s</th>" % c for c in head),
                                                   "".join("<td style='text-align:center;min-width:40px'>%s</td>" % c for c in ds)))


def blok(r, p, s, ribu=0):
    """balok dienes: ribuan (kubus besar), ratusan (papan), puluhan (batang), satuan (kubus kecil)"""
    pre = []
    x = 8
    for _ in range(ribu):
        pre.append("<rect x='%d' y='10' width='44' height='44' fill='#f6d6a8' stroke='%s' stroke-width='1.5'/>"
                   "<polygon points='%d,10 %d,2 %d,2 %d,10' fill='#fbe7c8' stroke='%s' stroke-width='1.2'/>"
                   "<polygon points='%d,10 %d,2 %d,46 %d,54' fill='#e8bf86' stroke='%s' stroke-width='1.2'/>"
                   % (x, INK, x, x + 8, x + 52, x + 44, INK, x + 44, x + 52, x + 52, x + 44, INK))
        x += 62
    svg = D.dienes(r, p, s, label="%d ribuan, %d ratusan, %d puluhan, %d satuan" % (ribu, r, p, s))
    if not ribu:
        return svg
    # ribuan を左に足す
    m = re.search(r"viewBox='0 0 (\d+) (\d+)' width='(\d+)' height='(\d+)'", svg)
    w, h = int(m.group(1)), int(m.group(2))
    nw = w + x - 8
    svg = svg.replace(m.group(0), "viewBox='0 0 %d %d' width='%d' height='%d'" % (nw, h, nw, h))
    svg = svg.replace("<g font-family='%s'>" % FONT, "<g font-family='%s'>%s<g transform='translate(%d,0)'>" % (FONT, "".join(pre), x - 8), 1)
    svg = svg.replace("</g></svg>", "</g></g></svg>")
    return svg


def diagram_batang(data, unit_label="", label="diagram batang", step=1):
    return D.saeulen(data, unit_label, label, step)


def bersusun(rows, op="+", result=None):
    rows = [r.replace(".", "") for r in rows]
    return D.schriftlich(rows, op, None, "perhitungan bersusun", result)
