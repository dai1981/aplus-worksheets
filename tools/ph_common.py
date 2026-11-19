# -*- coding: utf-8 -*-
"""
Shared parts for the Philippines (DepEd MATATAG) math generators: gen_ph_math_g4_*.py.
- Filipino names and places, US spelling (as in Philippine schools), metric units, pesos (₱) and centavos, commas from 1,000.
- adopt(mod): reuse question makers from other generators (US Common Core, Texas, Singapore) with Filipino names.
- Every item is checked for things that do not fit the Philippines (dollars, cents, inches, pounds, °F, STAAR, ...):
  run_many and collect skip them, and finish refuses them.
- run(fn, *args): call a set maker with a fresh seed until it succeeds (some makers assert on rare draws).
- finish(sets, rnd): US spelling, no repeated questions, answers spread over A to D (lettered choices keep order).
- make(...): writes content/ph/math/grade-4/{slug}.json.
standard_code looks like "Grade 4: Number and Algebra" (the MATATAG strand); standard_text is the learning competency.
"""
import random, re
import ws_common
from ws_common import (write_unit, fig, figure, table, comma, fr, svg_wrap, text, line, number_line, example, B,
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT, MINUS)

GIRLS = ["Maria", "Ana", "Bea", "Andrea", "Liza", "Joy", "Kristine", "Angel", "Trisha", "Jasmine", "Nicole", "Camille", "Rica", "Mae",
         "Carmela", "Isabel", "Jenny", "Patricia", "Bianca", "Ella", "Kyla", "Janelle", "Hazel", "Diane", "Rose", "Carla", "Sheila", "Lorna"]
BOYS = ["Juan", "Jose", "Miguel", "Paolo", "Carlo", "Mark", "Rafael", "Gabriel", "Angelo", "Christian", "Joshua", "Renz", "Enzo", "Nico",
        "Jericho", "Kevin", "Bryan", "Emmanuel", "Dennis", "Ramon", "Arnel", "Francis", "Vincent", "Kenneth", "Lance", "Ivan", "Jomar", "Rodel"]
FOREIGN_GIRLS = ['Aaliyah', 'Aisha', 'Amelia', 'Amira', 'Ava', 'Camila', 'Charlotte', 'Chloe', 'Devi', 'Emma', 'Evie', 'Farah', 'Freya', 'Grace', 'Hana', 'Harper', 'Hui Min', 'Isabella', 'Isla', 'Ivy', 'Jasleen', 'Jia Hui', 'Kavya', 'Leah', 'Lily', 'Lucia', 'Matilda', 'Maya', 'Mei Ling', 'Mei', 'Mia', 'Nadia', 'Nevaeh', 'Nora', 'Nurul', 'Olivia', 'Poppy', 'Priya', 'Rachel', 'Ruby', 'Sarah', 'Sienna', 'Simran', 'Siti', 'Sofia', 'Valeria', 'Wei Ling', 'Ximena', 'Xin Yi', 'Zara', 'Zoe']
FOREIGN_BOYS = ['Aarav', 'Ahmad', 'Aiden', 'Alfie', 'Ali', 'Andre', 'Arjun', 'Ben', 'Benjamin', 'Caleb', 'Carlos', 'Charlie', 'Cooper', 'Daniel', 'Diego', 'Eli', 'Elijah', 'Ethan', 'George', 'Hafiz', 'Hamish', 'Harjot', 'Harry', 'Imran', 'Isaac', 'Jack', 'Jayden', 'Ji-woo', 'Josiah', 'Jun Jie', 'Kai', 'Kumar', 'Lachlan', 'Leo', 'Liam', 'Lucas', 'Luis', 'Marcus', 'Mateo', 'Max', 'Mohammed', 'Nathan', 'Noah', 'Oliver', 'Omar', 'Owen', 'Raju', 'Ravi', 'Ryan', 'Sam', 'Theo', 'Tom', 'Wei Jie', 'Wei Ming', 'Wei', 'William', 'Zhi Hao']
_FOREIGN = sorted([(n, GIRLS) for n in FOREIGN_GIRLS] + [(n, BOYS) for n in FOREIGN_BOYS], key=lambda p: -len(p[0]))
PLACES = ["Manila", "Quezon City", "Cebu City", "Davao City", "Baguio", "Iloilo City", "Bacolod", "Cagayan de Oro", "Zamboanga City", "Tacloban"]
STD_URLS = {"grade-1": "https://www.deped.gov.ph/wp-content/uploads/MATATAG-Mathematics-CG-Grades1-4-and-7.pdf",
            "grade-4": "https://www.deped.gov.ph/wp-content/uploads/MATATAG-Mathematics-CG-Grades1-4-and-7.pdf",
            "grade-7": "https://www.deped.gov.ph/wp-content/uploads/MATATAG-Mathematics-CG-Grades1-4-and-7.pdf"}
GRADE = "grade-4"

US_WORDS = [("colour", "color"), ("Colour", "Color"), ("centimetre", "centimeter"), ("millimetre", "millimeter"),
            ("kilometre", "kilometer"), ("metre", "meter"), ("Metre", "Meter"), ("litre", "liter"), ("Litre", "Liter"),
            ("millilitre", "milliliter"), ("centre", "center"), ("Centre", "Center"), ("favourite", "favorite"),
            ("Favourite", "Favorite"), ("neighbour", "neighbor"), ("grey", "gray"), ("practise", "practice"),
            ("Practise", "Practice"), ("organise", "organize"), ("recognise", "recognize"), ("travelled", "traveled"),
            ("labelled", "labeled"), ("maths", "math"), ("Maths", "Math"), ("analogue", "analog"), ("cm²", "square centimeters"),
            ("m²", "square meters"), ("biscuit", "cookie"), ("lollies", "candies"), ("footy", "football"),
            ("tuck shop", "canteen"), ("cafeteria", "canteen"), ("Year 4 ", "Grade 4 "), ("Year 3 ", "Grade 3 "), ("Year 1 ", "Grade 1 "), ("Year 2 ", "Grade 2 "), ("Year 5 ", "Grade 5 "), ("Year 6 ", "Grade 6 "), ("Primary 4 ", "Grade 4 "), ("P4 ", "Grade 4 "), ("Wattle Street", "Rizal Street"), ("baseball", "basketball"), ("Baseball", "Basketball"), ("pupils", "learners"), ("students", "learners"), ("Students", "Learners"), ("all the way round", "all the way around"), (" round the ", " around the "), ("right-angled", "right"), ("Right-angled", "Right"), ("renamed", "regrouped"), ("renaming", "regrouping"), ("anticlockwise", "counterclockwise"), ("Anticlockwise", "Counterclockwise"), ("clockwise or counterclockwise", "clockwise or counterclockwise"), ("netball team has", "kickball team has"), ("on the court", "on the field"), ("$2 coins", "$2 bills"), ("$2 coin", "$2 bill"), ("money box", "piggy bank"), ("mobile phone", "cell phone"), ("petrol", "gas"), ("holidays", "vacation"), ("Hockey", "Volleyball"), ("hockey", "volleyball"), ("Canada geese", "wild geese"), ("Canada goose", "wild goose"), ("Ringette", "Snowboarding"), ("ringette", "snowboarding"), ("curling", "bowling"), ("Curling", "Bowling"), ("kookaburras", "robins"), ("Kookaburras", "Robins"), ("kookaburra", "robin"), ("Kookaburra", "Robin"), ("trapeziums", "trapezoids"), ("Trapeziums", "Trapezoids"), ("trapezium", "trapezoid"), ("Trapezium", "Trapezoid"), ("ladybird", "ladybug"), ("Ladybird", "Ladybug"), ("subitising", "subitizing"), ("Subitising", "Subitizing")]
LEAKS = r"(\$|¢|£|°F|\b(Texas|TEKS|STAAR|Common Core|PSLE|MOE|Ontario|Toronto|Ottawa|Canada|Canadian|loonie|toonie|EQAO|NAPLAN|Australia|Sydney|Melbourne|Brisbane|Perth|Singapore|Year [1-9]|Primary [1-6]|AUD|CAD|SGD|Tim Hortons|poutine|maple syrup|hockey|netball|Wattle|wattle|kangaroo|koala|footy|ute|lolly|lollies|biscuits?|trolley|fortnight|mum|wombats?|ladybirds?|dollars?|cents?|penny|pennies|nickels?|dimes?|inch|inches|in\.|feet|foot|ft|yards?|yd|miles?|mi|pounds?|lb|ounces?|oz|gallons?|gal|quarts?|qt|pints?|pt|Fahrenheit|Thanksgiving|Halloween|snow|sled|mph|July 4)\b)"


INCH = r"\d (in|ft|yd|lb|oz|mi|gal|qt|pt)\b(?! (all|the|a|an|each|his|her|their|every|order|total|front|which|this|that|one|its|it|them|row|line|place|between))"


def localize(it):
    """Give people from other countries' generators Filipino names (different names stay different, gender kept)."""
    whole = it["q"] + " " + it["e"] + " " + " ".join(it["c"])
    found = []
    for n, pool in _FOREIGN:
        m = re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(n), whole)
        if m and not any(n in f[0] for f in found):
            found.append((n, pool, m.start()))
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


def ph_ok(it):
    """True when an item fits the Philippines (no dollars, inches, STAAR, ...)."""
    plain = re.sub(r"<svg.*?</svg>", " ", it["q"] + " " + it["e"] + " " + " ".join(it["c"]), flags=re.S)
    t = re.sub(r"<[^>]+>", " ", us_text(plain))
    return not re.search(LEAKS, t) and not re.search(INCH, t)


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


def us_text(s):
    for a, b in US_WORDS:
        s = s.replace(a, b)
    s = re.sub(r"\b(puts?|putting|goes|go|going|walks?|walking|runs?|running|ran|went|fence|fencing|border|ribbon|trim|tape|rope|path|wall) round\b", r"\1 around", s)
    s = re.sub(r"(?<=\d)( ?)ml\b", r"\1mL", s)
    s = re.sub(r"(?<=\d)( ?)l\b", r"\1L", s)
    s = re.sub(r"(?<![A-Za-z])ml(?![A-Za-z])", "mL", s)
    s = re.sub(r"\b([ap])\.m\.\.(?!\.)", r"\1.m.", s)
    s = s.replace("sandpit", "sandbox").replace("Sandpit", "Sandbox")
    s = re.sub(r"(?<![\d.,])\b1 were\b", "1 was", s)
    sing = {"dimes": "dime", "pennies": "penny", "nickels": "nickel", "quarters": "quarter", "tenths": "tenth", "hundredths": "hundredth"}
    s = re.sub(r"(?<![\d.,/])\b1 (dimes|pennies|nickels|quarters|tenths|hundredths)\b", lambda m: "1 " + sing[m.group(1)], s)
    s = re.sub(r"(?<![\d.,])\b1 square (centimeter|meter|inch|foot|unit)(e?s)\b", lambda m: "1 square " + m.group(1), s)
    s = re.sub(r"(?<![\d.,])(?<!and )\b1 are\b", "1 is", s)
    # "an" before amounts said with a vowel sound: an $8 snack, an $11 book, an $18 ticket
    s = re.sub(r"\b([Aa]) (\$(?:8|11(?![\d,])|18(?![\d,])))", lambda m: m.group(1) + "n " + m.group(2), s)
    return add_commas(s)


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
    """Use Texas names and US commas in another generator's makers."""
    for name in ("GIRLS", "BOYS"):
        if hasattr(mod, name):
            setattr(mod, name, list(GIRLS if name == "GIRLS" else BOYS))
    for name in ("PLACES", "CITIES", "TOWNS"):
        if hasattr(mod, name):
            setattr(mod, name, list(PLACES))
    if hasattr(mod, "comma"):
        mod.comma = comma
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
            if key(it) in seen or (keep and not keep(it)) or not ph_ok(it):
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
        if not it or not ph_ok(it):
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
            m = re.search(LEAKS, re.sub(r"<[^>]+>", " ", plain + " " + it["e"] + " " + " ".join(it["c"])))
            assert not m, (m.group(0), it["q"][:200])
            m = re.search(INCH, re.sub(r"<[^>]+>", " ", plain + " " + it["e"] + " " + " ".join(it["c"])))
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
        "slug": slug, "sort": sort, "updated": "2026-11-20", "pdf_url": "",
        "title": title,
        "seo_title": seo_title or "Grade %s %s Worksheets with Answers (MATATAG Math %s)" % (GRADE.split("-")[1], short_title, GRADE.split("-")[1]),
        "short_title": short_title,
        "domain": domain,
        "standard_code": code,
        "standard_url": STD_URLS.get(GRADE, "https://www.deped.gov.ph/matatagcurriculumk147/"),
        "standard_text": std_text,
        "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": body, "faq": [{"q": q, "a": a} for q, a in faq],
        "sets": sets,
    }
    write_unit("ph", "math", GRADE, unit)
    return unit


# ------------------------------------------------------------ numbers in words and place value charts
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
PLACES_PV = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"]
PLACE_VAL = [1, 10, 100, 1000, 10000, 100000]


def words(n):
    """45,206 -> forty-five thousand, two hundred six."""
    assert 0 <= n <= 1000000
    if n == 1000000:
        return "one million"
    if n == 0:
        return "zero"

    def under1000(m):
        out = []
        if m >= 100:
            out.append(ONES[m // 100] + " hundred")
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


# ------------------------------------------------------------ Philippine money
def peso(v):
    """₱25, ₱1,250, ₱45.50 (centavos as two decimals)."""
    c = int(round(v * 100))
    if c % 100 == 0:
        return "₱" + comma(c // 100)
    return "₱%s.%02d" % (comma(c // 100), c % 100)
