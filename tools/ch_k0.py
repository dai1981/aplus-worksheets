# -*- coding: utf-8 -*-
"""Schweiz Kindergarten (Lehrplan 21, Zyklus 1, 4–6 Jahre): Zahlen bis 10 (zählen bis 20), Mengen, Formen, Lage, Muster, Grössen vergleichen, Tagesablauf, Daten.
Aus Deutschland Klasse 1 (gen_de_mathe_k1_*): Aufgaben mit Zahlen über 10 werden weggelassen (LIMIT), Texte auf den Kindergarten umgestellt (FIX)."""
import re

UNITS = [
    ("zahlen-bis-10", 1, ["MA.1.A.1", "MA.1.A.2"], "Z", "gen_de_mathe_k1_zahlen_bis_10"),
    ("zaehlen-bis-20", 2, ["MA.1.A.1", "MA.1.C.2"], "Z", "gen_de_mathe_k1_zahlen_bis_20"),
    ("mengen-vergleichen", 3, ["MA.1.A.2"], "Z", "gen_de_mathe_k1_zahlen_vergleichen"),
    ("zahlen-zerlegen", 4, ["MA.1.A.3", "MA.1.C.2"], "Z", "gen_de_mathe_k1_zerlegen_und_ergaenzen"),
    ("dazuzaehlen-bis-10", 5, ["MA.1.A.3"], "Z", "gen_de_mathe_k1_plus_bis_10"),
    ("wegnehmen-bis-10", 6, ["MA.1.A.3"], "Z", "gen_de_mathe_k1_minus_bis_10"),
    ("formen-und-koerper", 7, ["MA.2.A.1"], "F", "gen_de_mathe_k1_formen_und_koerper"),
    ("lage-und-richtung", 8, ["MA.2.C.3"], "F", "gen_de_mathe_k1_lage_und_richtung"),
    ("muster", 9, ["MA.1.B.1", "MA.1.C.2"], "Z", "gen_de_mathe_k1_muster_und_zahlenfolgen"),
    ("laengen-vergleichen", 10, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k1_laengen_vergleichen_und_messen"),
    ("tagesablauf-und-uhr", 11, ["MA.3.A.1"], "G", "gen_de_mathe_k1_uhrzeit_und_tagesablauf"),
    ("sortieren-und-zaehlen", 12, ["MA.3.C.1"], "G", "gen_de_mathe_k1_strichlisten_und_tabellen"),
]

_TAG = re.compile(r"<[^>]*>")
_NUM = re.compile(r"(?<![\d.’])\d+(?![\d’])")


def upto(n):
    """sichtbare Zahlen (Frage, Antworten, Lösung) höchstens n"""
    def ok(it):
        txt = _TAG.sub(" ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
        txt = re.sub(r"\d+:\d+", " ", txt)          # Uhrzeiten
        return all(int(x) <= n for x in _NUM.findall(txt))
    return ok


LIMIT = {u[0]: [upto(10)] for u in UNITS if u[0] not in ("zaehlen-bis-20", "tagesablauf-und-uhr", "laengen-vergleichen")}
LIMIT["zaehlen-bis-20"] = []
LIMIT["laengen-vergleichen"] = [upto(20)]
LIMIT["tagesablauf-und-uhr"] = [upto(12)]

_REP = [
    (r"\bfür (die )?Klasse 1\b", "für den Kindergarten"), (r"\bIn (der )?Klasse 1\b", "Im Kindergarten"),
    (r"\bin (der )?Klasse 1\b", "im Kindergarten"), (r"\bKlasse 1\b", "Kindergarten"),
    (r"\bfür die 1\. Klasse\b", "für den Kindergarten"), (r"\bIn der 1\. Klasse\b", "Im Kindergarten"),
    (r"\bin der 1\. Klasse\b", "im Kindergarten"), (r"\b1\. Klasse\b", "Kindergarten"),
    (r"\bbis 20\b(?! zählen)", "bis 10"),
]


def _kg(got, keep20=False):
    def f(s):
        for a, b in _REP:
            if keep20 and "bis 20" in a:
                continue
            s = re.sub(a, b, s)
        return s
    for k in ("title", "short", "meta", "kb", "ks", "body"):
        got[k] = f(got[k])
    got["faq"] = [{"q": f(x["q"]), "a": f(x["a"])} for x in got["faq"]]
    for x in got["faq"]:
        if x["q"].startswith("Bis zu welcher Zahl vergleicht"):
            x["a"] = "Meist bis 10, manchmal schon bis 20. In der 1. und 2. Klasse geht es weiter bis 100."
    for st in got["sets"]:
        for it in (st["items"] if isinstance(st, dict) else st[1]):
            for k in ("q", "e"):
                it[k] = _items(it[k])
            it["c"] = [_items(c) for c in it["c"]]


_ITEMS = [("Die Kinder der Klasse 1a", "Die Kinder im Kindergarten"), ("Umfrage in der Klasse 1b", "Umfrage im Kindergarten"),
          ("Klasse 1a", "Kindergartengruppe"), ("Klasse 1b", "Kindergartengruppe"),
          ("zur Schule gehen", "in den Kindergarten gehen"), ("Zeit für die Schule", "Zeit für den Kindergarten"),
          ("in der Schule", "im Kindergarten"), ("keine Schule", "kein Kindergarten"), ("Schultag", "Kindergartentag"),
          ("Schulweg", "Weg zum Kindergarten")]


def _items(s):
    for a, b in _ITEMS:
        s = s.replace(a, b)
    return s


FIX = {u[0]: _kg for u in UNITS}
FIX["zaehlen-bis-20"] = lambda g: _kg(g, True)
FIX["laengen-vergleichen"] = lambda g: _kg(g, True)
def _soft_mix(mod):
    """Wenn eine Aufgabenart wegen LIMIT zu wenige Aufgaben ergibt, mit den anderen Arten des Blattes auffüllen."""
    import de_common as D
    used = []

    def mix(rnd, seen, parts):
        out = []
        for mk, n in parts:
            used.append(mk)
            try:
                out += D.pick_unique(rnd, mk, n, seen, tries=3000)
            except AssertionError:
                got = []
                for _ in range(3000):
                    try:
                        it = mk()
                    except (ValueError, IndexError, ZeroDivisionError):
                        continue
                    if it is None:
                        continue
                    k = re.sub(r"\s+", " ", it["q"])
                    if k not in seen:
                        seen.add(k)
                        got.append(it)
                        if len(got) == n:
                            break
                out += got
        need = sum(n for _, n in parts) - len(out)
        for mk in [p[0] for p in parts] + used[::-1]:
            if need <= 0:
                break
            for _ in range(3000):
                if need <= 0:
                    break
                try:
                    it = mk()
                except (ValueError, IndexError, ZeroDivisionError):
                    continue
                if it is None:
                    continue
                k = re.sub(r"\s+", " ", it["q"])
                if k not in seen:
                    seen.add(k)
                    out.append(it)
                    need -= 1
        rnd.shuffle(out)
        return out
    mod.mix = mix


PRE = {u[0]: _soft_mix for u in UNITS}
