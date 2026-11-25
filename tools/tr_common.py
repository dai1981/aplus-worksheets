# -*- coding: utf-8 -*-
"""
Türkiye（Türkiye Yüzyılı Maarif Modeli, İlkokul Matematik Dersi Öğretim Programı 2024）の単元生成の共通部品。
de_common・id_common の絵の部品の上に作る。
・文はトルコ語。子ども向けに短い文、「sen」で話しかける
・数: 1.000 から点で区切る（id_common.num と同じ）。小数はコンマ
・記号: 3 × 4、12 ÷ 3、17 ÷ 5 → bölüm 3, kalan 2
・お金: 25 TL、50 kuruş
・数のあとに接尾辞を付けない（「345 sayısının」のように語を挟む）。人名にも接尾辞を付けない
・HTML の属性はシングルクォート、バックスラッシュなし
"""
import re
import de_common as D
import id_common as I
from id_common import num, dec, wrap, table, pick_unique, mix  # noqa: F401
from ws_common import (fig, svg_wrap, text, line, balance, write_unit, fr,   # noqa: F401
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT)

UPDATED = "2026-11-25"
STD_URL = "https://tymm.meb.gov.tr/upload/program/2024programmat1234Onayli.pdf"
DOMAIN = {
    "S": "Sayılar ve Nicelikler",
    "I": "İşlemlerden Cebirsel Düşünmeye",
    "G": "Nesnelerin Geometrisi",
    "V": "Veriye Dayalı Araştırma",
    "OV": "Olayların Olasılığı ve Veriye Dayalı Araştırma",
    "C5": "İşlemlerle Cebirsel Düşünme",
    "C6": "İşlemlerle Cebirsel Düşünme ve Değişimler",
    "GS": "Geometrik Şekiller",
    "GN": "Geometrik Nicelikler",
    "IA": "İstatistiksel Araştırma Süreci",
    "VO": "Veriden Olasılığa",
    "D": "Dönüşüm",
    "C8": "Cebirsel Düşünme ve Değişimler",
    "SY": "Sayılar",
    "N": "Nicelikler ve Değişimler",
    "ES": "Eşlik ve Benzerlik",
    "AB": "Algoritma ve Bilişim",
    "SAB": "Sayma, Algoritma ve Bilişim",
    "AN": "Analitik İnceleme",
    "GC": "Geometrik Cisimler",
    "DM": "Değişimin Matematiği",
    "HV": "Hazır Veriler Üzerinde Çalışma",
}
STD_URL_LISE = "https://mufredat.meb.gov.tr/Dosyalar/2026518151640408-matedöp.pdf"
STD_URL_ORTA = "https://mufredat.meb.gov.tr/Dosyalar/202681491243620-Matematik%20(5-8)%20D%C3%96P.pdf"
NAMES = ["Elif", "Yusuf", "Zeynep", "Ömer", "Defne", "Emir", "Ecrin", "Kerem", "Eylül", "Mert", "Nehir", "Aras",
         "Asel", "Can", "Duru", "Berk", "Ela", "Furkan", "Ece", "Miraç", "Azra", "Efe", "Hira", "Kuzey"]
NB = " "
D.num = num


def low(s):
    """Türkçe küçük harf: İ → i, I → ı"""
    return s.replace("İ", "i").replace("I", "ı").lower()


def tl(n):
    """25 TL"""
    return "%s%sTL" % (num(n), NB)


def kurus(n):
    return "%s%skuruş" % (num(n), NB)


def para(kr):
    """kuruş → '3 TL 25 kuruş' / '75 kuruş' / '12 TL'"""
    t, k = divmod(int(kr), 100)
    if t and k:
        return "%s %s" % (tl(t), kurus(k))
    return tl(t) if t else kurus(k)


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
        return self.next(), self.next()


# ------------------------------------------------------------ sayıların okunuşu
_B = ["sıfır", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_O = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def oku(n):
    """345 → üç yüz kırk beş"""
    n = int(n)
    if n == 0:
        return "sıfır"
    out = []
    b, n = divmod(n, 1000)
    if b:
        out.append("bin" if b == 1 else oku(b) + " bin")
    y, n = divmod(n, 100)
    if y:
        out.append("yüz" if y == 1 else _B[y] + " yüz")
    o, s = divmod(n, 10)
    if o:
        out.append(_O[o])
    if s:
        out.append(_B[s])
    return " ".join(out)


# saat: "üçü" (belirtme), "üçe" (yönelme)
_ACC = {1: "biri", 2: "ikiyi", 3: "üçü", 4: "dördü", 5: "beşi", 6: "altıyı", 7: "yediyi", 8: "sekizi", 9: "dokuzu",
        10: "onu", 11: "on biri", 12: "on ikiyi"}
_DAT = {1: "bire", 2: "ikiye", 3: "üçe", 4: "dörde", 5: "beşe", 6: "altıya", 7: "yediye", 8: "sekize", 9: "dokuza",
        10: "ona", 11: "on bire", 12: "on ikiye"}
# "saat üç buçuk", "saat dört" — yalın hâl
_NOM = {h: oku(h) for h in range(1, 13)}


def saat_oku(h, m):
    """12 saatlik okunuş: 'Saat üçü on geçiyor.' gibi (cümle başı büyük harf yok)"""
    h12 = h % 12 or 12
    nxt = h12 % 12 + 1
    if m == 0:
        return "saat %s" % _NOM[h12]
    if m == 30:
        return "saat %s buçuk" % _NOM[h12]
    if m == 15:
        return "saat %s çeyrek geçiyor" % _ACC[h12]
    if m == 45:
        return "saat %s çeyrek var" % _DAT[nxt]
    if m < 30:
        return "saat %s %s geçiyor" % (_ACC[h12], oku(m))
    return "saat %s %s var" % (_DAT[nxt], oku(60 - m))


def hm(h, m):
    """08.30（Türkçe yazımda saat ile dakika arasına nokta）"""
    return "%02d.%02d" % (h, m)


# ------------------------------------------------------------ sorular
def mcq(q, correct, cands, e):
    """4 seçenek. Yanlışlar yetmezse yakın sayılarla tamamlar (id_common.mcq)"""
    return I.mcq(q, correct, cands, e)


def M(q, correct, cands, e):
    """yanlışlar yetmezse None (yeniden üret)"""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3:
        return None
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Örnek</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Cevap: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist, extra=""):
    """body_html：Nasıl düşünürüz → Örnek → Sık yapılan hatalar"""
    h = "<h2>Nasıl düşünürüz?</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += extra
    h += "".join(examples)
    h += "<h2>Sık yapılan hatalar</h2>" + table(["Hata", "Doğrusu"], mist)
    return h


plain_text = D.plain_text
GRADE_NAME = {"%d-sinif" % g: "%d. Sınıf" % g for g in range(1, 13)}


def make_unit(rnd, slug, dom, code, std_text, title, short_title, meta_desc, key_big, key_sub,
              body_html, faq, sets, sort, grade="3-sinif"):
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
    import json as _j
    sets = _j.loads(_j.dumps(sets, ensure_ascii=False).replace("i\u0307", "i"))
    gname = GRADE_NAME[grade]
    seo_title = "%s %s Matematik: Çalışma Kâğıdı ve Cevaplı Test" % (short_title, gname)
    title, seo_title, short_title, meta_desc, key_big, key_sub = map(plain_text, (title, seo_title, short_title, meta_desc, key_big, key_sub))
    assert len(key_big) <= 40 and len(key_sub) <= 60, (slug, key_big, key_sub)
    write_unit("tr", "matematik", grade, {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": DOMAIN[dom], "standard_code": code, "standard_url": STD_URL_LISE if int(grade.split("-")[0]) >= 9 else STD_URL_ORTA if int(grade.split("-")[0]) >= 5 else STD_URL,
        "standard_text": std_text, "meta_desc": meta_desc, "key_big": key_big, "key_sub": key_sub,
        "body_html": body_html, "faq": faq, "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


# ------------------------------------------------------------ çizimler
def sayi_dogrusu(lo, hi, step, marks=(), labels=None, every=None, width=460):
    return D.zahlenstrahl(lo, hi, step, marks, labels, "sayı doğrusu", every, width)


def basamak_tablosu(n, cols=3):
    head = ["Binler", "Yüzler", "Onlar", "Birler"][-cols:]
    ds = str(n).rjust(cols, "0")[-cols:]
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead>"
            "<tbody><tr>%s</tr></tbody></table>" % ("".join("<th>%s</th>" % c for c in head),
                                                   "".join("<td style='text-align:center;min-width:44px'>%s</td>" % c for c in ds)))


def bloklar(y, o, b):
    return D.dienes(y, o, b, label="%d yüzlük, %d onluk, %d birlik" % (y, o, b))


def sutun_grafigi(data, unit_label="", step=None):
    return D.saeulen(data, unit_label, "sütun grafiği", step)


def cetele(n):
    return D.strichliste(n).replace("Strichliste mit %d Strichen" % n, "%d çizgili çetele" % n)


def alt_alta(rows, op="+", result=None):
    rows = [r.replace(".", "") for r in rows]
    return D.schriftlich(rows, op, None, "alt alta işlem", result)


def saat_svg(h, m, size=170):
    from tw_common import clock as _clock
    return _clock(h, m, size, label="analog saat")
