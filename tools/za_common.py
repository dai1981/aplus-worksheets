# -*- coding: utf-8 -*-
"""
Shared parts for the South Africa (CAPS) maths generators: gen_za_maths_gN_*.py.
- South African names and places, British spelling (as in CAPS), metric units, rand (R) and cents (c).
- South African number writing: spaces between thousands (4 536, 10 000) and a decimal comma (2,5; R12,50).
- adopt(mod): reuse question makers from other generators with South African names.
- Items with things that do not fit South Africa (dollars, pesos, inches, °F, STAAR, jeepney, ...) are skipped.
- finish(sets, rnd): British spelling, SA numbers, no repeated questions, answers spread over A to D.
standard_code looks like "Grade 4: 1.1 Whole numbers" (the CAPS topic); standard_text is the CAPS content.
"""
import random, re
import ws_common
from ws_common import (write_unit, fig, figure, table, comma, fr, svg_wrap, text, line, number_line, example, B,
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT, MINUS)

GIRLS = ["Lerato", "Thandi", "Naledi", "Ayanda", "Zanele", "Lindiwe", "Palesa", "Nomsa", "Amahle", "Kgomotso", "Refilwe", "Busisiwe", "Anika", "Chloe", "Megan", "Aisha", "Fatima", "Priya", "Lwazi", "Mbali", "Karabo", "Tumi", "Sarah", "Nadia", "Elna", "Zinhle", "Precious", "Ofentse"]
BOYS = ["Thabo", "Sipho", "Themba", "Kagiso", "Mpho", "Lungile", "Bongani", "Tshepo", "Sibusiso", "Kabelo", "Neo", "Lethabo", "Johan", "Pieter", "Ruan", "Liam", "Yusuf", "Ravi", "Daniel", "Tebogo", "Andile", "Siyabonga", "Musa", "Jabu", "Kyle", "Ethan", "Dumisani", "Vusi"]
FOREIGN_GIRLS = ['Aaliyah', 'Amelia', 'Amira', 'Ana', 'Andrea', 'Angel', 'Ava', 'Bea', 'Bianca', 'Camila', 'Camille', 'Carla', 'Carmela', 'Charlotte', 'Devi', 'Diane', 'Ella', 'Emma', 'Evie', 'Farah', 'Freya', 'Grace', 'Hana', 'Harper', 'Hazel', 'Hui Min', 'Isabel', 'Isabella', 'Isla', 'Ivy', 'Janelle', 'Jasleen', 'Jasmine', 'Jenny', 'Jia Hui', 'Joy', 'Kavya', 'Kristine', 'Kyla', 'Leah', 'Lily', 'Liza', 'Lorna', 'Lucia', 'Mae', 'Maria', 'Matilda', 'Maya', 'Mei', 'Mei Ling', 'Mia', 'Nevaeh', 'Nicole', 'Nora', 'Nurul', 'Olivia', 'Patricia', 'Poppy', 'Rachel', 'Rica', 'Rose', 'Ruby', 'Sheila', 'Sienna', 'Simran', 'Siti', 'Sofia', 'Trisha', 'Valeria', 'Wei Ling', 'Ximena', 'Xin Yi', 'Zara', 'Zoe']
FOREIGN_BOYS = ['Aarav', 'Ahmad', 'Aiden', 'Alfie', 'Ali', 'Andre', 'Angelo', 'Arjun', 'Arnel', 'Ben', 'Benjamin', 'Bryan', 'Caleb', 'Carlo', 'Carlos', 'Charlie', 'Christian', 'Cooper', 'Dennis', 'Diego', 'Eli', 'Elijah', 'Emmanuel', 'Enzo', 'Francis', 'Gabriel', 'George', 'Hafiz', 'Hamish', 'Harjot', 'Harry', 'Imran', 'Isaac', 'Ivan', 'Jack', 'Jayden', 'Jericho', 'Ji-woo', 'Jomar', 'Jose', 'Joshua', 'Josiah', 'Juan', 'Jun Jie', 'Kai', 'Kenneth', 'Kevin', 'Kumar', 'Lachlan', 'Lance', 'Leo', 'Lucas', 'Luis', 'Marcus', 'Mark', 'Mateo', 'Max', 'Miguel', 'Mohammed', 'Nathan', 'Nico', 'Noah', 'Oliver', 'Omar', 'Owen', 'Paolo', 'Rafael', 'Raju', 'Ramon', 'Renz', 'Rodel', 'Ryan', 'Sam', 'Theo', 'Tom', 'Vincent', 'Wei', 'Wei Jie', 'Wei Ming', 'William', 'Zhi Hao']
_FOREIGN = sorted([(n, GIRLS) for n in FOREIGN_GIRLS] + [(n, BOYS) for n in FOREIGN_BOYS], key=lambda p: -len(p[0]))
PLACES = ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Soweto", "Bloemfontein", "Gqeberha", "Polokwane", "Mbombela", "Kimberley"]
STD_URL_IP = "https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20IP%20%20MATHEMATICS%20GR%204-6%20web.pdf"
STD_URLS = {"grade-4": STD_URL_IP, "grade-5": STD_URL_IP, "grade-6": STD_URL_IP}
GRADE = "grade-4"

GB_WORDS = [("centimeter", "centimetre"), ("millimeter", "millimetre"), ("kilometer", "kilometre"), ("Kilometer", "Kilometre"), ("Centimeter", "Centimetre"), ("milliliter", "millilitre"), ("Milliliter", "Millilitre"), ("colorful", "colourful"), ("color", "colour"), ("Color", "Colour"), ("meter", "metre"), ("Meter", "Metre"), ("liter", "litre"), ("Liter", "Litre"),
            ("center", "centre"), ("Center", "Centre"), ("favorite", "favourite"), ("Favorite", "Favourite"), ("neighbor", "neighbour"),
            ("gray", "grey"), ("organize", "organise"), ("Organize", "Organise"), ("recognize", "recognise"), ("Recognize", "Recognise"),
            ("traveled", "travelled"), ("traveling", "travelling"), ("labeled", "labelled"), ("analog ", "analogue "), ("analog,", "analogue,"),
            ("cookies", "biscuits"), ("cookie", "biscuit"), ("candies", "sweets"), ("candy", "sweets"), ("Candies", "Sweets"),
            ("cafeteria", "tuck shop"), ("canteen", "tuck shop"), ("sandbox", "sandpit"), ("trapezoids", "trapeziums"), ("Trapezoids", "Trapeziums"),
            ("trapezoid", "trapezium"), ("Trapezoid", "Trapezium"), ("counterclockwise", "anti-clockwise"), ("Counterclockwise", "Anti-clockwise"),
            ("counter-clockwise", "anti-clockwise"), ("parking lot", "parking area"), ("vacation", "holiday"), ("apartment", "flat"),
            ("cell phone", "cellphone"), ("Cell phone", "Cellphone"), ("gasoline", "petrol"), ("gas station", "petrol station"), ("recess", "break"),
            ("Recess", "Break"), ("pupils", "learners"), ("students", "learners"), ("Students", "Learners"), ("student", "learner"), ("pupil", "learner"), ("ladybug", "ladybird"), ("Ladybug", "Ladybird"),
            ("subitizing", "subitising"), ("Subitizing", "Subitising"), ("piggy bank", "money box"), ("eraser", "rubber"), ("Eraser", "Rubber"),
            ("Year 4 ", "Grade 4 "), ("Year 3 ", "Grade 3 "), ("Year 5 ", "Grade 5 "), ("Year 6 ", "Grade 6 "), ("Primary 4 ", "Grade 4 "),
            ("Wattle Street", "Long Street"), ("baseball", "cricket"), ("Baseball", "Cricket"), ("football", "soccer"), ("Football", "Soccer"),
            ("sari-sari store", "spaza shop"), ("sausage sizzle", "fundraiser"), ("ice blocks", "ice lollies"), ("ice block", "ice lolly"), ("athletics carnival", "athletics day"), ("swimming carnival", "swimming gala"), ("column graph", "bar graph"), ("Column graph", "Bar graph"), ("column graphs", "bar graphs"), ("convenience store", "spaza shop"), ("corner store", "spaza shop")]
LEAKS = r"(\$|¢|£|₱|°F|\b(Cornwall|Devon|Europe|Scotland|Wales|England|Yorkshire|Kent|Brighton|Oxford|Cambridge|Nevis|Snowdon|Scafell|Thames|Severn|Lake District|Big Ben|Tower Bridge|Philippines|Filipino|Manila|Cebu|Davao|Baguio|Quezon|jeepneys?|sari-sari|pandesal|peso|pesos|centavos?|barangay|lola|lolo|adobo|Carabao|MATATAG|DepEd|tricycle|halo-halo|bibingka|puto|Texas|TEKS|STAAR|Common Core|PSLE|MOE|Ontario|Toronto|Ottawa|Canada|Canadian|loonie|toonie|EQAO|NAPLAN|Australia|Sydney|Melbourne|Brisbane|Perth|Singapore|Year [1-9]|Primary [1-6]|AUD|CAD|SGD|Tim Hortons|pucks?|Pucks?|Tobermory|Fort St|Huron|Mississauga|Collingwood|Duluth|Grouse|Smithers|Canadians|Ferries|Superior|ski|skis|skiing|Skiing|skating|Skating|sledding|Sledding|snowboarding|Snowboarding|igloo|blizzard|frostbite|Mexico|Vernon|Squamish|Prince [A-Z]\w+|Kelowna|Kamloops|Whistler|Victoria|Vancouver|Nanaimo|Surrey|Burnaby|Okanagan|Fraser|Yukon|Banff|Calgary|Edmonton|Winnipeg|Halifax|Muskoka|Sudbury|Thunder Bay|Montreal|Quebec|Alberta|Manitoba|Nunavut|Kingston|Hamilton|Niagara|Ottawa|Regina|Saskatoon|Brisbane|Adelaide|Darwin|Hobart|Canberra|Cairns|Uluru|London|Manchester|Birmingham|Leeds|Glasgow|Edinburgh|Cardiff|Bristol|Liverpool|Texas|Houston|Dallas|Austin|Chicago|Boston|Seattle|Denver|Miami|Ohio|Iowa|Utah|Orchard Road|Sentosa|Jurong|Tampines|Changi|poutine|maple syrup|hockey|netball|Wattle|wattle|kangaroo|koala|footy|ute|lolly|lollies|biscuits?|trolley|fortnight|mum|wombats?|ladybirds?|dollars?|penny|pennies|nickels?|dimes?|inch|inches|in\.|feet|foot|ft|yards?|yd|miles?|mi|pounds?|lb|ounces?|oz|gallons?|gal|quarts?|qt|pints?|pt|Fahrenheit|Thanksgiving|Halloween|snow|sled|mph|July 4)\b)"


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


def za_ok(it):
    """True when an item fits South Africa (no dollars, pesos, inches, STAAR, ...)."""
    if not it.get("q", "").strip() or "_abcd" in it:
        return False
    plain = re.sub(r"<svg.*?</svg>", " ", it["q"] + " " + it["e"] + " " + " ".join(it["c"]), flags=re.S)
    t = re.sub(r"<[^>]+>", " ", gb_text(plain))
    return not re.search(_leaks(), t) and not re.search(r"\d+p\b", t) and (ALLOW_IMPERIAL or not re.search(INCH, t))


NBSP = "\u00a0"


def _za_plain(t):
    """4,536 -> 4 536; 10000 -> 10 000; 2.5 -> 2,5 (text only)."""
    t = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", NBSP, t)
    t = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", NBSP, t)
    t = re.sub(r"(?<=\d)\.(?=\d)", ",", t)
    t = re.sub(r"(\d,\d+), (?=[−-]?\d)", r"\1; ", t)
    t = re.sub(r"(\d), (?=[−-]?\d+,\d)", r"\1; ", t)
    t = re.sub(r"(?<![\d,:/#" + NBSP + r"])(\d{4,9})(?![,:]\d|\d)", lambda m: "{:,}".format(int(m.group(1))).replace(",", NBSP), t)
    return t


def za_numbers(s):
    """South African number writing in text and in SVG labels, never inside tags."""
    out = []
    prev = ""
    for part in re.split(r"(<[^>]+>)", s):
        if part.startswith("<"):
            out.append(part)
        elif re.search(r"\d[.,]$", prev) and out and out[-1].startswith("<"):
            out.append(part.replace(".", ","))
        else:
            out.append(_za_plain(part))
        if not part.startswith("<"):
            prev = part
    return "".join(out)


def gb_text(s):
    for a, b in GB_WORDS:
        s = re.sub(r"(?<![A-Za-z])" + re.escape(a), b, s) if a[0].isalpha() else s.replace(a, b)
    s = re.sub(r"(?<=[☐?] )(l|L)\b", "ℓ", s)
    s = re.sub(r"(?<=[☐?] )(ml|mL)\b", "mℓ", s)
    s = s.replace(">L<", ">ℓ<").replace(">mL<", ">mℓ<").replace(">ml<", ">mℓ<")
    s = re.sub(r"\bmath\b", "maths", s)
    s = re.sub(r"\bMath\b", "Maths", s)
    s = re.sub(r"(?<=\d)( ?)(mL|ml)\b", r"\1 mℓ".replace(" mℓ", "mℓ"), s)
    s = re.sub(r"(?<=\d)( ?)L\b", r"\1ℓ", s)
    s = re.sub(r"(?<=\d)( ?)l\b", r"\1ℓ", s)
    s = re.sub(r"(?<![A-Za-z])(mL|ml)(?![A-Za-z])", "mℓ", s)
    s = re.sub(r"\b([ap])\.m\.\.(?!\.)", r"\1.m.", s)
    s = re.sub(r"(?<![\d.,])\b1 tens\b", "1 ten", s)
    s = re.sub(r"(?<![\d.,])\b1 ones\b", "1 one", s)
    s = re.sub(r"\b(\d)th graders\b", r"Grade \1 learners", s)
    s = re.sub(r"(?<![\d.,/−-])\b1 (hour|minute|second|day|week|month|year|metre|kilometre|litre|gram|kilogram|centimetre)s\b", r"1 \1", s)
    s = re.sub(r"(?<![\d.,])\b1 were\b", "1 was", s)
    s = re.sub(r"(?<![\d.,])(?<!and )\b1 are\b", "1 is", s)
    return za_numbers(s)


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
    """Use South African names and rand in another generator's makers."""
    for name in ("GIRLS", "BOYS"):
        if hasattr(mod, name):
            setattr(mod, name, list(GIRLS if name == "GIRLS" else BOYS))
    for name in ("PLACES", "CITIES", "TOWNS"):
        if hasattr(mod, name):
            setattr(mod, name, list(PLACES))
    if hasattr(mod, "comma"):
        mod.comma = comma
    for name in ("gbp", "aud", "sgd", "usd", "cad", "peso"):
        if callable(getattr(mod, name, None)):
            setattr(mod, name, rand)
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
    key = (lambda x: gb_text(x["q"]) + "|" + "|".join(sorted(gb_text(c) for c in x["c"]))) if _full else (lambda x: gb_text(x["q"]))
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
            if "q" not in it or not za_ok(it) or key(it) in seen or (keep and not keep(it)):
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
            bad.add(re.sub(r"\s+", " ", gb_text(x["q"])))
    for _ in range(tries):
        try:
            it = maker(rnd)
        except AssertionError:
            continue
        if not it or not za_ok(it):
            continue
        k = (re.sub(r"\s+", " ", gb_text(it["q"])), tuple(sorted(gb_text(c) for c in it["c"])))
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
        s["title"] = gb_text(s["title"])
        for it in s["items"]:
            localize(it)
            for k in ("q", "e"):
                it[k] = gb_text(it[k])
            it["c"] = [gb_text(c) for c in it["c"]]
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
                    for n in re.findall(r"\d[\d\u00a0]*", re.sub(r"<[^>]+>", "", c)):
                        assert int(n.replace("\u00a0", "")) <= max_num, (c, it["q"][:120])
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
        "seo_title": seo_title or "Grade %s %s Worksheets with Answers (CAPS Maths)" % (GRADE.split("-")[1], short_title),
        "short_title": short_title,
        "domain": domain,
        "standard_code": code,
        "standard_url": STD_URLS.get(GRADE, "https://www.education.gov.za/Curriculum/CurriculumAssessmentPolicyStatements(CAPS).aspx"),
        "standard_text": std_text,
        "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": body, "faq": [{"q": q, "a": a} for q, a in faq],
        "sets": sets,
    }
    write_unit("za", "maths", GRADE, unit)
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
    if th and rest and rest < 100:
        return parts[0] + " and " + parts[1]
    return " ".join(parts)


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


# ------------------------------------------------------------ South African money
def rand(v):
    """R25, R1 250, R45,50 (cents as two decimals with a comma)."""
    c = int(round(v * 100))
    if c % 100 == 0:
        return "R" + comma(c // 100).replace(",", NBSP)
    return "R%s,%02d" % (comma(c // 100).replace(",", NBSP), c % 100)


def cents(v):
    return "%dc" % v
