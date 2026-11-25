# -*- coding: utf-8 -*-
"""
Shared parts for the Nigeria (NERDC 9-Year Basic Education Curriculum) maths generators: tools/ng_p4.py and others.
- Nigerian names and places, British spelling (as in Nigerian schools), metric units, naira (₦) and kobo, commas from 1,000.
- adopt(mod): reuse question makers from other generators (US, UK, Singapore, Philippines) with Nigerian names.
- ng_text(): US spelling -> British spelling, pesos -> naira, Grade N -> Primary N.
- Every item is checked for things that do not fit Nigeria (dollars, pounds, inches, pesos, °F, STAAR, ...).
- make(...): writes content/ng/maths/{GRADE}/{slug}.json.
standard_code looks like "Primary 4: Number and Numeration" (the NERDC theme).
"""
import random, re
import ws_common
from ws_common import (write_unit, fig, figure, table, comma, fr, svg_wrap, text, line, number_line, example, B,
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT, MINUS)

GIRLS = ["Ngozi", "Amaka", "Fatima", "Bola", "Funke", "Chioma", "Zainab", "Kemi", "Tolu", "Ada", "Halima", "Ife", "Nneka", "Hauwa",
         "Yetunde", "Blessing", "Esther", "Ruth", "Chiamaka", "Aminat", "Simi", "Ifeoma", "Bisi", "Nkechi", "Hadiza", "Temi", "Joy", "Uju"]
BOYS = ["Chinedu", "Emeka", "Tunde", "Musa", "Ibrahim", "Femi", "Obinna", "Segun", "Yusuf", "Kelechi", "Uche", "Bayo", "Sani", "Dayo",
        "Ikenna", "Tobi", "Kunle", "Chidi", "Usman", "Samuel", "Gbenga", "Ifeanyi", "Babatunde", "Nonso", "Abdullahi", "Kayode", "Victor", "Peter"]
PH_GIRLS = ["Maria", "Ana", "Bea", "Andrea", "Liza", "Kristine", "Angel", "Trisha", "Jasmine", "Nicole", "Camille", "Rica", "Mae",
            "Carmela", "Isabel", "Jenny", "Patricia", "Bianca", "Ella", "Kyla", "Janelle", "Hazel", "Diane", "Rose", "Carla", "Sheila", "Lorna"]
PH_BOYS = ["Juan", "Jose", "Miguel", "Paolo", "Carlo", "Mark", "Rafael", "Gabriel", "Angelo", "Christian", "Joshua", "Renz", "Enzo", "Nico",
           "Jericho", "Kevin", "Bryan", "Emmanuel", "Dennis", "Ramon", "Arnel", "Francis", "Vincent", "Kenneth", "Lance", "Ivan", "Jomar", "Rodel"]
FOREIGN_GIRLS = ['Aaliyah', 'Amelia', 'Amira', 'Ava', 'Camila', 'Charlotte', 'Chloe', 'Devi', 'Emma', 'Evie', 'Farah', 'Freya', 'Grace', 'Hana', 'Harper', 'Hui Min', 'Isabella', 'Isla', 'Ivy', 'Jasleen', 'Jia Hui', 'Kavya', 'Leah', 'Lily', 'Lucia', 'Matilda', 'Maya', 'Mei Ling', 'Mei', 'Mia', 'Nadia', 'Nevaeh', 'Nora', 'Nurul', 'Olivia', 'Poppy', 'Priya', 'Rachel', 'Ruby', 'Sarah', 'Sienna', 'Simran', 'Siti', 'Sofia', 'Valeria', 'Wei Ling', 'Ximena', 'Xin Yi', 'Zara', 'Zoe'] + PH_GIRLS
FOREIGN_BOYS = ['Aarav', 'Aiden', 'Alfie', 'Andre', 'Arjun', 'Ben', 'Benjamin', 'Caleb', 'Carlos', 'Charlie', 'Cooper', 'Daniel', 'Diego', 'Eli', 'Elijah', 'Ethan', 'George', 'Hafiz', 'Hamish', 'Harjot', 'Harry', 'Imran', 'Isaac', 'Jack', 'Jayden', 'Ji-woo', 'Josiah', 'Jun Jie', 'Kai', 'Kumar', 'Lachlan', 'Leo', 'Liam', 'Lucas', 'Luis', 'Marcus', 'Mateo', 'Max', 'Nathan', 'Noah', 'Oliver', 'Owen', 'Raju', 'Ravi', 'Ryan', 'Sam', 'Theo', 'Tom', 'Wei Jie', 'Wei Ming', 'Wei', 'William', 'Zhi Hao'] + PH_BOYS
_FOREIGN = sorted([(n, GIRLS) for n in FOREIGN_GIRLS] + [(n, BOYS) for n in FOREIGN_BOYS], key=lambda p: -len(p[0]))
PLACES = ["Lagos", "Abuja", "Kano", "Ibadan", "Enugu", "Port Harcourt", "Kaduna", "Benin City", "Jos", "Abeokuta", "Owerri", "Calabar"]
PH_PLACES = ["Quezon City", "Cebu City", "Davao City", "Iloilo City", "Cagayan de Oro", "Zamboanga City", "Manila", "Baguio", "Bacolod", "Tacloban"]
STD_URL = "https://nerdc.gov.ng/"
GRADE = "primary-4"

LEAKS = r"(\$|¢|£|₱|°F|\b(Texas|TEKS|STAAR|Common Core|PSLE|MOE|MATATAG|DepEd|Ontario|Toronto|Canada|Canadian|loonie|toonie|EQAO|NAPLAN|Australia|Sydney|Melbourne|Singapore|Philippines?|Filipino|pesos?|centavos?|jeepney|sari-sari|pandesal|barangay|Manila|Cebu|Davao|Quezon|Rizal|Luzon|Grade [1-9]|Year [1-9]|AUD|CAD|SGD|Tim Hortons|pucks?|ski|skis|skiing|Skiing|skating|Skating|sledding|snowboarding|Snowboarding|igloo|blizzard|frostbite|Mexico|Vancouver|Calgary|London|Manchester|Birmingham|Glasgow|Edinburgh|Houston|Dallas|Chicago|Boston|Orchard Road|Sentosa|poutine|maple syrup|hockey|kangaroo|koala|footy|ute|wombats?|dollars?|cents?|penny|pennies|nickels?|dimes?|inch|inches|in\.|feet|foot|ft|yards?|yd|miles?|mi|pounds?|lb|ounces?|oz|gallons?|gal|quarts?|qt|pints?|pt|Fahrenheit|Thanksgiving|Halloween|snow|sled|mph|July 4|rand|kickball|Canberra|Perth|Batangas|Calapan|Victoria|Elizabeth|Waterloo|Europe|Adelaide|Brisbane|Darwin|Hobart|Toronto)\b)"


IMPERIAL = "inch|inches|in\\.|feet|foot|ft|yards?|yd|miles?|mi|pounds?|lb|ounces?|oz|gallons?|gal|quarts?|qt|pints?|pt|mph"
ALLOW_IMPERIAL = False   # True only in a unit that converts between metric and customary units (Grade 7)


def _leaks():
    if not ALLOW_IMPERIAL:
        return LEAKS
    out = LEAKS
    for t in IMPERIAL.split("|"):
        out = out.replace("|" + t + "|", "|")
    return out


INCH = r"\d (in|ft|yd|lb|oz|mi|gal|qt|pt)\b(?! (all|the|a|an|each|his|her|their|every|order|total|front|which|this|that|one|its|it|them|row|line|place|between))"


def localize(it):
    """Give people from other countries' generators Nigerian names (different names stay different, gender kept)."""
    whole = it["q"] + " " + it["e"] + " " + " ".join(it["c"])
    found = []
    for n, pool in _FOREIGN:
        m = re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(n), whole)
        if m and not any(n in f[0] for f in found):
            found.append((n, pool, m.start()))
    for p in PH_PLACES:
        if p in whole:
            q = PLACES[sum(ord(ch) for ch in p) % len(PLACES)]
            it["q"], it["e"], it["c"] = it["q"].replace(p, q), it["e"].replace(p, q), [c.replace(p, q) for c in it["c"]]
    if not found:
        return it
    found.sort(key=lambda f: f[2])
    used = {p for p in GIRLS + BOYS if re.search(r"\b%s\b" % p, whole)}
    rep = {}
    for n, pool, _ in found:
        k = sum(ord(ch) for ch in n) % len(pool)
        for j in range(len(pool)):
            cand = pool[(k + j) % len(pool)]
            if cand not in used:
                break
        used.add(cand)
        rep[n] = cand
    rx = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(n) for n in sorted(rep, key=len, reverse=True)))
    sub = lambda t: rx.sub(lambda m: rep[m.group(1)], t)
    it["q"], it["e"], it["c"] = sub(it["q"]), sub(it["e"]), [sub(c) for c in it["c"]]
    return it


def ng_ok(it):
    """True when an item fits Nigeria (no dollars, pesos, inches, STAAR, ...)."""
    if not it.get("q", "").strip() or "_abcd" in it:
        return False
    plain = re.sub(r"<svg.*?</svg>", " ", it["q"] + " " + it["e"] + " " + " ".join(it["c"]), flags=re.S)
    t = re.sub(r"<[^>]+>", " ", ng_text(plain))
    return not re.search(_leaks(), t) and not re.search(r"\d+[cp]\b", t) and (ALLOW_IMPERIAL or not re.search(INCH, t))


def _commas_plain(t):
    t = re.sub("(\\d{1,3})\u00a0(\\d{3})(?!\\d)", "\\1,\\2", t)
    return re.sub(r"(?<![\d.,:/#])(\d{4,6})(?![\d.,:]\d|\d)", lambda m: "{:,}".format(int(m.group(1))), t)


def add_commas(s):
    """1000 -> 1,000 in text, but not inside SVG pictures or HTML tags."""
    out = []
    prev = ""
    for part in re.split(r"(<svg.*?</svg>|<[^>]+>)", s, flags=re.S):
        if part.startswith("<"):
            out.append(part)
        elif re.search(r"\d\.$", prev) and out and out[-1].startswith("<"):
            # digits right after "1.<span ...>" are decimal places (repeating-decimal bars): no commas
            out.append(part)
        else:
            out.append(_commas_plain(part))
        if not part.startswith("<"):
            prev = part
    return "".join(out)


GB = [(r"\b([Cc])olor(s|ed|ful|ing)?\b", r"\1olour\2"), (r"\b([Ff])avorite(s?)\b", r"\1avourite\2"), (r"\b([Nn])eighbor", r"\1eighbour"),
      (r"\bgray\b", "grey"), (r"\b([Cc])enter(s|d)?\b", r"\1entre\2"), (r"\b(kilo|centi|milli|deci)?meter(s?)\b", r"\1metre\2"),
      (r"\b(Kilo|Centi|Milli|Deci)?meter(s?)\b", r"\1metre\2"), (r"\b(milli|centi)?liter(s?)\b", r"\1litre\2"), (r"\b(Milli|Centi)?liter(s?)\b", r"\1litre\2"),
      (r"\b([Oo])rganiz", r"\1rganis"), (r"\b([Rr])ecogniz", r"\1ecognis"), (r"\b([Tt])raveled\b", r"\1ravelled"), (r"\b([Tt])raveling\b", r"\1ravelling"),
      (r"\b([Ll])abeled\b", r"\1abelled"), (r"\banalog\b", "analogue"), (r"\bcandies\b", "sweets"), (r"\bCandies\b", "Sweets"), (r"\bcandy\b", "sweet"),
      (r"\bcookies\b", "biscuits"), (r"\bcookie\b", "biscuit"), (r"\b([Cc])ounterclockwise\b", lambda m: ("A" if m.group(1) == "C" else "a") + "nticlockwise"),
      (r"\btrapezoids\b", "trapeziums"), (r"\bTrapezoids\b", "Trapeziums"), (r"\btrapezoid\b", "trapezium"), (r"\bTrapezoid\b", "Trapezium"),
      (r"\bmath\b", "maths"), (r"\bMath\b", "Maths"), (r"\blearners\b", "pupils"), (r"\bLearners\b", "Pupils"), (r"\blearner\b", "pupil"), (r"\bLearner\b", "Pupil"),
      (r"\bstudents\b", "pupils"), (r"\bStudents\b", "Pupils"), (r"\bGrade ([1-6])\b", r"Primary \1"), (r"\bYear ([1-6])\b", r"Primary \1"), (r"\bP([1-6]) ", r"Primary \1 "),
      (r"\bladybugs?\b", lambda m: "ladybird" + ("s" if m.group(0).endswith("s") else "")), (r"\bvacation\b", "holiday"), (r"\bcell phone\b", "mobile phone"),
      (r"\bpiggy bank\b", "money box"), (r"\bkickball\b", "football"), (r"\bsquare (centi|kilo|milli)?meters\b", r"square \1metres"),
      (r"\bjeepneys?\b", lambda m: "bus" + ("es" if m.group(0).endswith("s") else "")), (r"\bsari-sari store\b", "provision shop"), (r"\bpandesal\b", "bread rolls"),
      (r"\bCarabao mangoes\b", "mangoes"), (r"\bcanteen\b", "tuck shop"), (r"\bregrouping\b", "regrouping"), (r"\bfavor\b", "favour"),
      (r"\bpractice (it|them|this|these)\b", r"practise \1"),
      (r"\bmeters\b", "metres"), (r"\bApartment\b", "Flat"), (r"\bapartment\b", "flat"), (r"\btyphoon\b", "storm"), (r"\bin standard form\b", "in figures"),
      (r"\bhundred (?=(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)\b)", "hundred and ")]


def ng_text(s):
    """US/Filipino text -> Nigerian (British spelling, naira and kobo, Primary N)."""
    s = s.replace("₱", "₦").replace("pesos", "naira").replace("Pesos", "Naira").replace("peso", "naira").replace("centavos", "kobo").replace("centavo", "kobo")
    for a, b in GB:
        s = re.sub(a, b, s)
    s = re.sub(r"\b([ap])\.m\.\.(?!\.)", r"\1.m.", s)
    s = re.sub(r"(?<![\d.,])\b1 tens\b", "1 ten", s)
    s = re.sub(r"(?<![\d.,])\b1 ones\b", "1 one", s)
    s = re.sub(r"(\d)\xa0(\d{3})(?!\d)", r"\1,\2", s)
    s = re.sub(r"(\d)\xa0(\d{3})(?!\d)", r"\1,\2", s)
    s = re.sub(r"(?<![\d.,/−-])\b1 (hour|minute|second|day|week|month|year|metre|kilometre|litre|gram|kilogram|centimetre|naira)s\b", r"1 \1", s)
    s = re.sub(r"(?<![\d.,])\b1 were\b", "1 was", s)
    s = re.sub(r"(?<![\d.,])(?<!and )\b1 are\b", "1 is", s)
    s = re.sub(r"(?<![\d.,])\b1 square (centimetre|metre|unit)s\b", r"1 square \1", s)
    return add_commas(s)


us_text = ng_text


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


class Kid:
    """Dict-style person for new makers: k['n'], k['he'], k['He'], k['his'], k['His'], k['him']."""
    def __init__(self, rnd):
        self.P = People(rnd)

    def next(self):
        n, he, his = self.P.next()
        return {"n": n, "he": he, "He": he.capitalize(), "his": his, "His": his.capitalize(), "him": "her" if he == "she" else "him"}


def adopt(mod):
    """Use Nigerian names and commas in another generator's makers."""
    for name in ("GIRLS", "BOYS"):
        if hasattr(mod, name):
            setattr(mod, name, list(GIRLS if name == "GIRLS" else BOYS))
    for name in ("PLACES", "CITIES", "TOWNS"):
        if hasattr(mod, name):
            setattr(mod, name, list(PLACES))
    if hasattr(mod, "comma"):
        mod.comma = comma
    for name in ("gbp", "aud", "sgd", "usd", "cad"):
        if callable(getattr(mod, name, None)):
            setattr(mod, name, naira)
    return mod


def run(fn, *args, seed=1, tries=60):
    """Call a set maker with seeds seed, seed+1, … until it returns 20 items."""
    last = None
    for k in range(tries):
        r = random.Random(seed * 1000 + k)
        a = []
        for x in args:
            if x == "rnd":
                a.append(r)
            elif x == "seen":
                a.append(set())
            elif callable(x):
                a.append(x(r))
            else:
                a.append(x)
        try:
            s = fn(*a)
        except (AssertionError, IndexError, ValueError, RuntimeError, KeyError, ZeroDivisionError) as e:
            last = e
            continue
        its = s["items"] if isinstance(s, dict) else s
        if len(its) >= 20:
            return {"title": s["title"] if isinstance(s, dict) else "", "items": its[:20]}
    raise AssertionError("set maker failed: %s %r" % (fn.__name__, last))


def run_many(fn, *args, seed=1, n=20, keep=None, avoid=(), _full=False):
    """Like run, but gathers n different items over several seeds, keeping only items where keep(item) is true.
    Questions are kept different by their text; if that gives too few, the choices count too."""
    out, seen = [], set()
    key = (lambda x: x["q"] + "|" + "|".join(sorted(x["c"]))) if _full else (lambda x: x["q"])
    for a in avoid:
        for x in (a["items"] if isinstance(a, dict) else a):
            seen.add(key(x))
    for k in range(40):
        try:
            its = run(fn, *args, seed=seed * 100 + k)["items"]
        except AssertionError:
            continue
        for it in its:
            if "build" in it:          # letter questions (A–D pictures) built for a chosen answer position
                it = it["build"](random.Random(seed * 1000 + k * 50 + len(out)).randrange(4))
            if "q" not in it or not ng_ok(it) or key(it) in seen or (keep and not keep(it)):
                continue
            seen.add(key(it))
            out.append(it)
            if len(out) == n:
                return out
    if not _full:
        return run_many(fn, *args, seed=seed, n=n, keep=keep, avoid=avoid, _full=True)
    raise AssertionError("run_many: only %d items from %s" % (len(out), fn.__name__))


def S(title, items):
    return {"title": title, "items": items}


def mcq(q, correct, cands, e, allow_zero=False):
    """correct and cands are values (numbers or text). Duplicates and negatives are dropped; 0 only with allow_zero."""
    def key(v):
        return str(v)
    seen = {key(correct)}
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, (int, float)) and (c < 0 or (c == 0 and not allow_zero)):
            continue
        if key(c) in seen:
            continue
        seen.add(key(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    show = lambda v: comma(v) if isinstance(v, int) else str(v)
    return {"q": q, "c": [show(correct)] + [show(c) for c in pick], "a": 0, "e": e}


def collect(maker, n, rnd, tries=4000, avoid=()):
    """n different items from maker(rnd). avoid: items (or sets of items) whose questions must not repeat."""
    out, seen = [], set()
    bad = set()
    for a in avoid:
        for x in (a["items"] if isinstance(a, dict) else a if isinstance(a, list) else [a]):
            bad.add(re.sub(r"\s+", " ", x["q"]))
    for _ in range(tries):
        try:
            it = maker(rnd)
        except AssertionError:
            continue
        if not it or not ng_ok(it):
            continue
        k = (re.sub(r"\s+", " ", it["q"]), tuple(sorted(it["c"])))
        if k in seen or k[0] in bad:
            continue
        seen.add(k)
        out.append(it)
        if len(out) == n:
            return out
    raise AssertionError("only %d items from %s" % (len(out), maker.__name__))


def letters(it, labels="ABCD"):
    """Keep the choice order A, B, C, D (choices name parts of one picture)."""
    ans = it["c"][it["a"]]
    lab = list(labels)
    it["c"] = lab + [c for c in it["c"] if c not in lab]
    it["c"] = it["c"][:4]
    it["a"] = it["c"].index(ans)
    it["_fixed"] = True
    return it


ORDERED = [{"A", "B", "C", "D"}, {"Always", "Sometimes", "Never"}]


def _ordered(it):
    cs = set(it["c"])
    if cs <= {"A", "B", "C", "D"} or cs <= {"Shape A", "Shape B", "Shape C", "Shape D"}:
        return True
    return False


def balance(sets, rnd):
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            if _ordered(it) and not it.get("_fixed"):
                ans = it["c"][it["a"]]
                it["c"] = sorted(it["c"])
                it["a"] = it["c"].index(ans)
                it["_fixed"] = True
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("_fixed") and it["a"] in targets:
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("_fixed", False):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [c[it["a"]]] + wrong[t:]
            it["a"] = t


def finish(sets, rnd, max_num=None):
    seen = set()
    for s in sets:
        s["title"] = us_text(s["title"])
        for it in s["items"]:
            localize(it)
            for k in ("q", "e"):
                it[k] = us_text(it[k])
            it["c"] = [us_text(c) for c in it["c"]]
            assert len(set(it["c"])) == 4, it["c"]
            plain = re.sub(r"<svg.*?</svg>", "", it["q"], flags=re.S)
            m = re.search(_leaks(), re.sub(r"<[^>]+>", " ", plain + " " + it["e"] + " " + " ".join(it["c"])))
            assert not m, (m.group(0), it["q"][:200])
            m = None if ALLOW_IMPERIAL else re.search(INCH, re.sub(r"<[^>]+>", " ", plain + " " + it["e"] + " " + " ".join(it["c"])))
            assert not m, (m.group(0), it["q"][:200])
            key = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"][:200]
            seen.add(key)
            if max_num is not None:
                for c in it["c"]:
                    for n in re.findall(r"\d[\d,]*", re.sub(r"<[^>]+>", "", c)):
                        assert int(n.replace(",", "")) <= max_num, (c, it["q"][:120])
    balance(sets, rnd)
    rx = re.compile(r"<svg (?!data-pf)")
    return sets


def lesson(think, examples, mistakes):
    """think: html list; examples: list of html blocks; mistakes: [[mistake, fix], ...]."""
    h = "<h2>How to think about it</h2>" + think
    h += "<h2>Examples</h2>" + "".join(examples)
    h += "<h2>Common mistakes</h2>" + table(["Mistake", "What to do instead"], mistakes)
    return h


def make(slug, sort, domain, code, std_text, title, short_title, meta, key_big, key_sub, body, faq, sets, seo_title=None):
    unit = {
        "slug": slug, "sort": sort, "updated": "2026-11-26", "pdf_url": "",
        "title": title,
        "seo_title": seo_title or "%s – Primary %s Mathematics Worksheets with Answers (NERDC)" % (short_title, GRADE.split("-")[1]),
        "short_title": short_title,
        "domain": domain,
        "standard_code": code,
        "standard_url": STD_URL,
        "standard_text": std_text,
        "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": body, "faq": [{"q": q, "a": a} for q, a in faq],
        "sets": sets,
    }
    write_unit("ng", "maths", GRADE, unit)
    return unit


# ------------------------------------------------------------ numbers in words and place value charts
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
PLACES_PV = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"]
PLACE_VAL = [1, 10, 100, 1000, 10000, 100000]


def words(n):
    """45,206 -> forty-five thousand, two hundred and six (British)."""
    assert 0 <= n <= 1000000
    if n == 1000000:
        return "one million"
    if n == 0:
        return "zero"

    def under1000(m):
        out = []
        if m >= 100:
            out.append(ONES[m // 100] + " hundred" + (" and" if m % 100 else ""))
            m %= 100
        if m >= 20:
            out.append(TENS[m // 10] + ("-" + ONES[m % 10] if m % 10 else ""))
        elif m:
            out.append(ONES[m])
        return " ".join(out)
    th, rest = divmod(n, 1000)
    parts = []
    if th:
        parts.append(under1000(th) + " thousand")
    if rest:
        parts.append(under1000(rest))
    return ", ".join(parts)


def pv_chart_svg(n, red=None, places=5):
    """Place value chart: Ten Thousands | Thousands | Hundreds | Tens | Ones. red: place index to color red."""
    heads = ["Hundred Thousands", "Ten Thousands", "Thousands", "Hundreds", "Tens", "Ones"][6 - places:]
    w = 92
    W = w * places + 8
    digits = str(n).rjust(places, " ")
    b = ""
    for i, hd in enumerate(heads):
        x = 4 + i * w
        b += "<rect x='%d' y='4' width='%d' height='40' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, w, FILL, GREEN)
        ws = hd.split(" ")
        if len(ws) == 2:
            b += text(x + w / 2, 21, ws[0], 12) + text(x + w / 2, 36, ws[1], 12)
        else:
            b += text(x + w / 2, 29, hd, 13)
        b += "<rect x='%d' y='44' width='%d' height='46' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (x, w, GREEN)
        d = digits[i]
        if d != " ":
            place = places - 1 - i
            b += text(x + w / 2, 77, d, 26, col=RED if red == place else INK)
    return svg_wrap(W, 94, b, "place value chart showing %s" % comma(n))


# ------------------------------------------------------------ strip diagrams (TEKS: strip diagram = tape diagram)
def strip_svg(parts, total=None, compare=None, label="strip diagram"):
    """parts: [(text, width_units, fill)] drawn in one bar; total: text over a brace above the bar.
    compare: [(text, units), ...] second bar under the first (for comparison problems), drawn left-aligned."""
    unit = 360.0 / max(sum(p[1] for p in parts), sum(c[1] for c in compare) if compare else 0)
    x0, y0, h = 20, 40 if total else 12, 38
    s = []
    x = x0
    for t, w, col in parts:
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, y0, w * unit, h, col, GREEN))
        s.append(text(x + w * unit / 2, y0 + 25, t, 16))
        x += w * unit
    if total:
        x1 = x
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, x0, y0 - 14, x1, y0 - 14, x1, y0 - 6, INK))
        s.append(text((x0 + x1) / 2, y0 - 20, total, 16))
    H = y0 + h + 8
    if compare:
        y1 = y0 + h + 14
        x = x0
        for t, w in compare:
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>" % (x, y1, w * unit, h, GREEN))
            s.append(text(x + w * unit / 2, y1 + 25, t, 16))
            x += w * unit
        H = y1 + h + 8
    return svg_wrap(int(x0 * 2 + 360), H, "".join(s), label)


# ------------------------------------------------------------ sets from several makers
def build_sets(specs, seed):
    """specs: [(title, [part, ...]), ...]; part is ("run", fn, args, n[, keep]) for another generator's set maker
    (several seeds, no question repeated in the unit) or ("collect", maker, n) for an item maker of this file."""
    rnd = random.Random(seed)
    sets = []
    for si, (title, parts) in enumerate(specs):
        items = []
        for pi, p in enumerate(parts):
            if p[0] == "run":
                fn, args, n = p[1], p[2], p[3]
                keep = p[4] if len(p) > 4 else None
                items += run_many(fn, *args, seed=seed % 10000 + si * 10 + pi, n=n, keep=keep, avoid=sets + [items])
            else:
                items += collect(p[1], p[2], rnd, avoid=sets + [items])
        sets.append(S(title, items))
    return sets, rnd


# ------------------------------------------------------------ Nigerian money
def naira(v):
    """₦25, ₦1,250, ₦45.50 (kobo as two decimals)."""
    c = int(round(v * 100))
    if c % 100 == 0:
        return "₦" + comma(c // 100)
    return "₦%s.%02d" % (comma(c // 100), c % 100)


peso = naira
