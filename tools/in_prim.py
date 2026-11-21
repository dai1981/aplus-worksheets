# -*- coding: utf-8 -*-
"""
Shared parts for India Classes 1-5 (NCERT Joyful Mathematics, Maths Mela): gen_in_maths_c1_* … c5_*.
Built from ph_common: the same run / run_many / build_sets / finish machinery, so set makers from the UK, AU, SG, US,
Ontario, BC, Texas and Philippine generators can be reused.
- Indian names and places, British spelling (colour, metre, maths, anticlockwise), rupees (₹), Indian commas (1,23,456).
- Whole-number $ and £ amounts become ₹; amounts with cents or pence, and other countries' words, are refused (LEAKS).
- make(...): writes content/in/maths/class-N/{slug}.json; standard_code "Class 3, Maths Mela Chapter 7: Raksha Bandhan".
"""
import random, re
import ws_common
import in_common
from ws_common import (write_unit, fig, figure, table, comma, fr, svg_wrap, text, line, number_line, example, B,
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT, MINUS)

GIRLS = ["Priya", "Ananya", "Diya", "Meera", "Sneha", "Kavya", "Isha", "Riya", "Aditi", "Pooja", "Nisha", "Shreya", "Anika", "Tara", "Lakshmi", "Fatima", "Zoya", "Simran", "Gauri", "Neha"]
BOYS = ["Aarav", "Rohan", "Arjun", "Kabir", "Vivaan", "Ishaan", "Rahul", "Aditya", "Karan", "Siddharth", "Nikhil", "Dev", "Ayaan", "Harsh", "Manav", "Imran", "Rehan", "Varun", "Om", "Yash"]
FOREIGN_GIRLS = ['Maria', 'Ana', 'Bea', 'Andrea', 'Liza', 'Joy', 'Kristine', 'Angel', 'Trisha', 'Jasmine', 'Nicole', 'Camille', 'Rica', 'Mae', 'Aaliyah', 'Amelia', 'Amira', 'Ava', 'Camila', 'Charlotte', 'Chloe', 'Emma', 'Evie', 'Farah', 'Freya', 'Grace', 'Hana', 'Harper', 'Hui Min', 'Isabella', 'Isla', 'Ivy', 'Jia Hui', 'Leah', 'Lily', 'Lucia', 'Matilda', 'Maya', 'Mei Ling', 'Mei', 'Mia', 'Nadia', 'Nevaeh', 'Nora', 'Nurul', 'Olivia', 'Poppy', 'Rachel', 'Ruby', 'Sarah', 'Sienna', 'Siti', 'Sofia', 'Valeria', 'Wei Ling', 'Ximena', 'Xin Yi', 'Zara', 'Zoe']
FOREIGN_BOYS = ['Juan', 'Jose', 'Miguel', 'Paolo', 'Carlo', 'Mark', 'Rafael', 'Gabriel', 'Angelo', 'Christian', 'Joshua', 'Renz', 'Enzo', 'Nico', 'Ahmad', 'Aiden', 'Alfie', 'Andre', 'Ben', 'Benjamin', 'Caleb', 'Carlos', 'Charlie', 'Cooper', 'Daniel', 'Diego', 'Eli', 'Elijah', 'Ethan', 'George', 'Hafiz', 'Hamish', 'Harry', 'Isaac', 'Jack', 'Jayden', 'Ji-woo', 'Josiah', 'Jun Jie', 'Kai', 'Lachlan', 'Leo', 'Liam', 'Lucas', 'Luis', 'Marcus', 'Mateo', 'Max', 'Nathan', 'Noah', 'Oliver', 'Owen', 'Ryan', 'Sam', 'Theo', 'Tom', 'Wei Jie', 'Wei Ming', 'Wei', 'William', 'Zhi Hao']
_FOREIGN = sorted([(n, GIRLS) for n in FOREIGN_GIRLS] + [(n, BOYS) for n in FOREIGN_BOYS], key=lambda p: -len(p[0]))
PLACES = ["Delhi", "Mumbai", "Jaipur", "Chennai", "Kolkata", "Pune", "Lucknow", "Bhopal", "Kochi", "Indore", "Patna", "Nagpur"]
STD_URL = "https://ncert.nic.in/textbook.php"
GRADE = "class-3"

GB_WORDS = [(r"\bcolor", "colour"), (r"\bColor", "Colour"), (r"\b(centi|milli|kilo)?meter", r"\1metre"), (r"\b(Centi|Milli|Kilo)?Meter", r"\1Metre"),
            (r"\b(milli)?liter", r"\1litre"), (r"\b(Milli)?Liter", r"\1Litre"), (r"\bcenter", "centre"), (r"\bCenter", "Centre"),
            (r"\bfavorite", "favourite"), (r"\bFavorite", "Favourite"), (r"\bneighbor", "neighbour"), (r"\bNeighbor", "Neighbour"), (r"\bgray\b", "grey"),
            (r"\bmath\b", "maths"), (r"\bMath\b", "Maths"), (r"\bcounterclockwise", "anticlockwise"), (r"\bCounterclockwise", "Anticlockwise"),
            (r"\btrapezoid", "trapezium"), (r"\bTrapezoid", "Trapezium"), (r"\bcookie", "biscuit"), (r"\bCookie", "Biscuit"), (r"\bcandies\b", "toffees"), (r"\bcandy\b", "toffee"),
            (r"\bsoccer\b", "football"), (r"\bSoccer\b", "Football"), (r"\bmom\b", "mother"), (r"\bMom\b", "Mother"), (r"\bmum\b", "mother"), (r"\bMum\b", "Mother"),
            (r"\bpupils\b", "students"), (r"\bPupils\b", "Students"), (r"\blearners\b", "students"), (r"\bLearners\b", "Students"),
            (r"\b(Grade|Year|Primary) ([1-9])\b", r"Class \2"), (r"\borganiz", "organis"), (r"\brecogniz", "recognis"), (r"\btraveled", "travelled"), (r"\blabeled", "labelled"),
            (r"\bsari-sari store", "kirana shop"), (r"\bcanteen\b", "canteen"), (r"\bsandbox", "sandpit"), (r"\bline up\b", "line up"), (r"\bcheckers\b", "draughts"),
            (r"\brectangular prisms?\b", lambda m: "cuboids" if m.group(0).endswith("s") else "cuboid"), (r"\bRectangular prisms?\b", lambda m: "Cuboids" if m.group(0).endswith("s") else "Cuboid"),
            (r"\bPrata\b", "Paratha"), (r"\bprata\b", "paratha"), (r"\bChicken rice\b", "Pulao"), (r"\bchicken rice\b", "pulao"), (r"\bminibeasts\b", "small creatures"),
            (r"\bminibeast\b", "small creature"), (r"\bTerry Fox Run\b", "Charity Run"), (r"(\d) ?ℓ", r"\1 L"), (r"ℓ", "L"), (r"(\d) ?ml\b", r"\1 mL"), (r"(\d) l\b", r"\1 L"),
            (r"\(ml\)", "(mL)"), (r"\(l\)", "(L)"), (r"\bmixed numeral", "mixed number"), (r"\bMixed numeral", "Mixed number"), (r"\blacrosse\b", "kabaddi"), (r"\bLacrosse\b", "Kabaddi"),
            (r"\bthe food bank\b", "charity"), (r"\bfood bank\b", "charity"), (r"\bClass ([1-9]) class\b", r"Class \1"), (r"\bfood drive\b", "charity"), (r"\b(fall|Fall) (\d)", lambda m: ("autumn " if m.group(1) == "fall" else "Autumn ") + m.group(2)),
            (r"\b(A|a) Class ([1-9]) class\b", r"Class \2A"), (r"\bGr\. ([1-9])\b", r"Class \1"),
            (r"\bfrom fall to spring\b", "from autumn to spring"), (r"\bin fall\b", "in autumn"), (r"\bthan in fall\b", "than in autumn"), (r"\bkaya toast\b", "toast"), (r"\bmee\b", "noodles"), (r"\bnasi lemak\b", "rice"),
            (r"\b(?<!\.)(\d+) ?mL\b", r"\1 mL"), (r"\bsquare meters?\b", "square metres"), (r"\bsquare centimeters?\b", "square centimetres")]
LEAKS = r"(\$|¢|£|₱|°F|\b(echidnas?|platypus|wallab(?:y|ies)|kookaburras?|emus?|possums?|moose|beavers?|raccoons?|salmon|peso|pesos|centavos?|jeepney|sari-sari|pandesal|Philippines?|Filipino|Manila|Cebu|Davao|Quezon|Baguio|Iloilo|DepEd|MATATAG|Rizal|halo-halo|Jollibee|calamansi|rand|Rand|Gauteng|Durban|Johannesburg|Cape Town|braai|Texas|TEKS|STAAR|Common Core|PSLE|MOE|Ontario|Toronto|Ottawa|Canada|Canadian|loonie|toonie|EQAO|NAPLAN|Australia|Sydney|Melbourne|Brisbane|Perth|Singapore|Year [1-9]|Primary [1-6]|AUD|CAD|SGD|Tim Hortons|pucks?|Pucks?|Tobermory|Fort St|Huron|Mississauga|Collingwood|Duluth|Grouse|Smithers|Canadians|Ferries|Superior|ski|skis|skiing|Skiing|skating|Skating|sledding|Sledding|snowboarding|Snowboarding|igloo|blizzard|frostbite|Mexico|Vernon|Squamish|Prince [A-Z]\w+|Kelowna|Kamloops|Whistler|Victoria|Vancouver|Nanaimo|Surrey|Burnaby|Okanagan|Fraser|Yukon|Banff|Calgary|Edmonton|Winnipeg|Halifax|Muskoka|Sudbury|Thunder Bay|Montreal|Quebec|Alberta|Manitoba|Nunavut|Kingston|Hamilton|Niagara|Ottawa|Regina|Saskatoon|Brisbane|Adelaide|Darwin|Hobart|Canberra|Cairns|Uluru|London|Manchester|Birmingham|Leeds|Glasgow|Edinburgh|Cardiff|Bristol|Liverpool|Texas|Houston|Dallas|Austin|Chicago|Boston|Seattle|Denver|Miami|Ohio|Iowa|Utah|Orchard Road|Sentosa|Jurong|Tampines|Changi|poutine|maple syrup|maple|Loon|loons?|netball|Wattle|wattle|kangaroo|koala|footy|ute|lolly|lollies|fortnight|wombats?|ladybirds?|dollars?|cents?|penny|pennies|nickels?|dimes?|inch|inches|in\.|feet|foot|ft|yards?|yd|miles?|mi|pounds?|lb|ounces?|oz|gallons?|gal|quarts?|qt|pints?|pt|Fahrenheit|Thanksgiving|Halloween|snow|sled|mph|July 4)\b)"


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


def in_ok(it):
    """True when an item fits the Philippines (no dollars, inches, STAAR, ...)."""
    if not it.get("q", "").strip() or "_abcd" in it:
        return False
    if len(set(us_text(c) for c in it.get("c", []))) != len(it.get("c", [])):
        return False
    plain = re.sub(r"<svg.*?</svg>", " ", it["q"] + " " + it["e"] + " " + " ".join(it["c"]), flags=re.S)
    t = re.sub(r"<[^>]+>", " ", us_text(plain))
    svgs = " ".join(re.findall(r"<svg.*?</svg>", it["q"], flags=re.S))
    svg_t = " ".join(a or b for a, b in re.findall(r"aria-label='([^']*)'|>([^<>]+)</text>", svgs))
    if re.search(_leaks(), us_text(svg_t)) or re.search(r"\b(Loon|Orca|Polar bear|maple)\b", us_text(svg_t + " " + t)):
        return False
    return not re.search(_leaks(), t) and not re.search(r"\d+[cp]\b", t) and (ALLOW_IMPERIAL or not re.search(INCH, t))


def _commas_plain(t):
    t = re.sub("(\\d{1,3})\u00a0(\\d{3})(?!\\d)", "\\1,\\2", t)
    t = re.sub(r"(?<![\d.,:/#])(\d{1,3}(?:,\d{3})+)(?![\d.,:]\d|\d)", lambda m: in_common.comma(int(m.group(1).replace(",", ""))), t)
    return re.sub(r"(?<![\d.,:/#])(\d{4,9})(?![\d.,:]\d|\d)", lambda m: in_common.comma(int(m.group(1))), t)


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
    """British spelling and Indian money and commas (kept the name us_text so the ph machinery calls it)."""
    for a, b in GB_WORDS:
        s = re.sub(a, b, s)
    s = re.sub(r"[$£](\d[\d,]*)(?![.\d])", lambda m: "₹" + m.group(1), s)
    s = re.sub(r"\b(\d[\d,]*) dollars\b", lambda m: "₹" + m.group(1), s)
    s = re.sub(r"(?<![\d.,])\b1 tens\b", "1 ten", s)
    s = re.sub(r"(?<![\d.,])\b1 ones\b", "1 one", s)
    s = s.replace("ξ", "U")
    s = re.sub(r"(\d)\xa0(\d{3})(?!\d)", r"\1,\2", s)
    s = re.sub(r"(\d)\xa0(\d{3})(?!\d)", r"\1,\2", s)
    s = re.sub(r"(?<![\d.,/−-])\b1 (hour|minute|second|day|week|month|year|metre|kilometre|litre|gram|kilogram|centimetre|rupee)s\b", r"1 \1", s)
    s = re.sub(r"(?<![\d.,])\b1 were\b", "1 was", s)
    s = re.sub(r"(?<![\d.,])(?<!and )\b1 are\b", "1 is", s)
    s = re.sub(r"\b([Aa]) (₹(?:8|11(?![\d,])|18(?![\d,])|80(?![\d,])))", lambda m: m.group(1) + "n " + m.group(2), s)
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
    """Use Indian names, rupees and Indian commas in another generator's makers."""
    for name in ("GIRLS", "BOYS"):
        if hasattr(mod, name):
            setattr(mod, name, list(GIRLS if name == "GIRLS" else BOYS))
    for name in ("PLACES", "CITIES", "TOWNS"):
        if hasattr(mod, name):
            setattr(mod, name, list(PLACES))
    if hasattr(mod, "comma"):
        mod.comma = in_common.comma
    for name in ("gbp", "aud", "sgd", "usd", "cad"):
        if callable(getattr(mod, name, None)):
            setattr(mod, name, rupee)
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
    key = (lambda x: us_text(x["q"]) + "|" + "|".join(sorted(us_text(c) for c in x["c"]))) if _full else (lambda x: us_text(x["q"]))
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
            if "q" not in it or not in_ok(it) or key(it) in seen or (keep and not keep(it)):
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
    show = lambda v: in_common.comma(v) if isinstance(v, int) else str(v)
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
        if not it or not in_ok(it):
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


BOOKS = {1: "Joyful Mathematics", 2: "Joyful Mathematics", 3: "Maths Mela", 4: "Maths Mela", 5: "Maths Mela"}
DOMAINS = {"N": "Numbers and Operations", "G": "Shapes and Space", "M": "Measurement", "P": "Patterns", "D": "Data Handling"}


def make(slug, sort, strand, chapter, chapter_title, topic, title, short_title, std_text, meta, key_big, key_sub, body, faq, sets):
    """chapter_title: the NCERT story title (Raksha Bandhan); topic: what it teaches (Multiplication and Equal Groups)."""
    level = int(GRADE.split("-")[1])
    book = BOOKS[level]
    unit = {
        "slug": slug, "sort": sort, "updated": in_common.UPDATED, "pdf_url": "",
        "title": title,
        "seo_title": "%s Class %d Worksheet with Answers (%s Chapter %d)" % (topic, level, book, chapter),
        "short_title": short_title,
        "domain": DOMAINS[strand],
        "standard_code": "Class %d, %s Chapter %d: %s" % (level, book, chapter, chapter_title),
        "standard_url": STD_URL,
        "standard_text": std_text,
        "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": body, "faq": [{"q": q, "a": a} for q, a in faq],
        "sets": sets,
    }
    write_unit("in", "maths", GRADE, unit)
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


# ------------------------------------------------------------ Indian money
def rupee(v):
    """₹25, ₹1,250, ₹45.50 (paise as two decimals)."""
    c = int(round(v * 100))
    if c % 100 == 0:
        return "₹" + in_common.comma(c // 100)
    return "₹%s.%02d" % (in_common.comma(c // 100), c % 100)


peso = rupee


# ------------------------------------------------------------ one call per unit
import importlib, inspect

_MODS = {}


def mod(name, seed):
    """Import another country's generator, give it Indian names and rupees, and a fresh random seed."""
    m = importlib.import_module(name)
    if name not in _MODS:
        adopt(m)
        _MODS[name] = m
    if isinstance(getattr(m, "R", None), random.Random):
        m.R = random.Random(seed)
    return m


def rn(m, fn, n, keep=None, **fixed):
    """("run", …) part for build_sets with the set maker's arguments filled in from its parameter names."""
    f = getattr(m, fn)
    args = []
    for p in inspect.signature(f).parameters.values():
        k = p.name
        if k in fixed:
            args.append(fixed[k])
        elif k in ("rnd", "r"):
            args.append("rnd")
        elif k.startswith("seen") or k.startswith("used") or k == "uniq":
            args.append("seen")
        elif k in ("pos", "Pos"):
            args.append(m.Pos)
        elif k in ("Picker", "picker"):
            args.append(m.Picker)
        elif k in ("Names", "names"):
            args.append(m.Names)
        elif k in ("P", "people", "P_", "PK", "pk", "kids", "K", "PP", "Pe", "ppl", "Pp", "names"):
            for c in ("People2", "People", "Picker", "Names", "Kid", "Kids"):
                if hasattr(m, c):
                    args.append(getattr(m, c))
                    break
            else:
                if hasattr(m, "PEOPLE"):
                    args.append(lambda r, L=list(m.PEOPLE): (lambda x: (r.shuffle(x), iter(x * 3))[1])(L[:]))
                else:
                    raise AttributeError("%s.%s: no People for %s" % (m.__name__, fn, k))
        elif p.default is not inspect.Parameter.empty:
            break
        else:
            raise AttributeError("%s.%s: cannot fill %s" % (m.__name__, fn, k))
    return ("run", f, tuple(args), n) + ((keep,) if keep else ())


def co(maker, n):
    return ("collect", maker, n)


def le(n):
    """keep: every number in the question and choices is at most n."""
    def k(it):
        t = re.sub(r"<svg.*?</svg>", " ", it["q"] + " " + " ".join(it["c"]), flags=re.S)
        t = re.sub(r"<[^>]+>", " ", t)
        return all(int(x.replace(",", "")) <= n for x in re.findall(r"\d[\d,]*", t))
    return k


def unit(level, slug, sort, strand, chapter, chapter_title, topic, short_title, std_text, meta, key_big, key_sub,
         think, examples, mistakes, faq, specs, seed, max_num=None):
    """think: html; examples: [(question, [steps], answer)]; mistakes: [[mistake, fix]]."""
    global GRADE
    GRADE = "class-%d" % level
    if max_num is not None:
        cap = le(max_num)
        fixed = []
        for title, parts in specs:
            ps = []
            for p in parts:
                if p[0] == "run":
                    old = p[4] if len(p) > 4 else None
                    ps.append(p[:4] + ((lambda it, old=old: cap(it) and (old is None or old(it))),))
                else:
                    ps.append(("collect", (lambda mk: lambda r: (lambda it: it if it and cap(it) else None)(mk(r)))(p[1]), p[2]))
            fixed.append((title, ps))
        specs = fixed
    sets, rnd = build_sets(specs, seed)
    finish(sets, rnd)
    body = lesson(think, [example(q, st, a) for q, st, a in examples], mistakes)
    return make(slug, sort, strand, chapter, chapter_title, topic, "%s: %s" % (chapter_title, topic), short_title, std_text,
                meta, key_big, key_sub, body, faq, sets)


# ------------------------------------------------------------ own number makers for any range (place value, compare, order)
def num_maker(lo, hi, kinds=("place", "expand", "build", "cmp", "order", "near", "more", "words")):
    """Questions about whole numbers from lo to hi."""
    places = ["ones", "tens", "hundreds", "thousands", "ten thousands", "lakhs"]

    def f(r):
        kind = r.choice(kinds)
        n = r.randint(lo, hi)
        s = str(n)
        if kind == "place":
            cand = [i for i in range(len(s)) if s.count(s[i]) == 1 and s[i] != "0"]
            if not cand:
                return None
            i = r.choice(cand)
            p = len(s) - 1 - i
            v = int(s[i]) * 10 ** p
            return mcq("What is the value of the digit <b>%s</b> in <b>%s</b>?" % (s[i], in_common.comma(n)), v, [int(s[i]), v * 10, v // 10 if v >= 10 else v + 10],
                       "%s is in the %s place, so it is worth <b>%s</b>." % (s[i], places[p], in_common.comma(v)))
        if kind == "expand":
            parts = [int(c) * 10 ** (len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]
            right = " + ".join(in_common.comma(x) for x in parts)
            w1 = " + ".join(c for c in s if c != "0")
            w2 = " + ".join(in_common.comma(x * 10) for x in parts)
            w3 = " + ".join(in_common.comma(x) for x in parts[::-1][1:] + parts[-1:]) if len(parts) > 2 else in_common.comma(n + 10)
            if len({right, w1, w2, w3}) < 4:
                return None
            return mcq("Which shows <b>%s</b> in expanded form?" % in_common.comma(n), right, [w1, w2, w3], "%s = <b>%s</b>." % (in_common.comma(n), right))
        if kind == "build":
            ds = [int(c) for c in s]
            names = places[:len(ds)][::-1]
            desc = ", ".join("%d %s" % (d, nm if d != 1 else nm[:-1]) for d, nm in zip(ds, names) if d)
            alt = int(s[::-1]) if s[::-1][0] != "0" and s[::-1] != s else n + 10 ** (len(s) - 1) // 10 * 10 + 1
            return mcq("What number is <b>%s</b>?" % desc, n, [alt, int("".join(c for c in s if c != "0")) if "0" in s else n + 1, n + 10 ** (len(s) - 2) if len(s) > 2 else n + 10],
                       "<b>%s</b>." % in_common.comma(n))
        if kind == "cmp":
            m2 = n + r.choice([-1, 1]) * r.choice([1, 9, 10, 90, 100, 1000][:len(s)])
            if m2 < lo or m2 > hi or m2 == n:
                return None
            sg = "&gt;" if n > m2 else "&lt;"
            return mcq("Which sign goes in the box? <b>%s ☐ %s</b>" % (in_common.comma(n), in_common.comma(m2)), sg, ["&lt;" if sg == "&gt;" else "&gt;", "=", "+"],
                       "Compare from the biggest place: %s is %s, so <b>%s</b>." % (in_common.comma(n), "greater" if n > m2 else "smaller", sg))
        if kind == "order":
            xs = sorted(set(r.randint(lo, hi) for _ in range(4)))
            if len(xs) < 4:
                return None
            big = r.random() < 0.5
            ans = xs[-1] if big else xs[0]
            return mcq("Which is the %s: %s?" % ("greatest" if big else "smallest", ", ".join(in_common.comma(x) for x in r.sample(xs, 4))), in_common.comma(ans),
                       [in_common.comma(x) for x in xs if x != ans], "<b>%s</b>." % in_common.comma(ans))
        if kind == "near":
            if n <= lo or n >= hi:
                return None
            k = r.choice(["after", "before"])
            v = n + 1 if k == "after" else n - 1
            return mcq("Which number comes just %s <b>%s</b>?" % (k, in_common.comma(n)), v, [n - 1 if k == "after" else n + 1, v + 10, v - 10 if v > 10 else v + 2],
                       "<b>%s</b>." % in_common.comma(v))
        if kind == "more":
            step = r.choice([x for x in (10, 100, 1000) if x * 10 <= hi])
            up = r.random() < 0.5
            v = n + step if up else n - step
            if v < 0 or v > hi:
                return None
            return mcq("What is %s %s than <b>%s</b>?" % (in_common.comma(step), "more" if up else "less", in_common.comma(n)), v,
                       [n + (step // 10 if step > 10 else 1) * (1 if up else -1), n - step if up else n + step, v + 1], "<b>%s</b>." % in_common.comma(v))
        if n > 99999:
            return None
        w = re.sub(r"hundred (?!and)(?=\w)", "hundred and ", words(n))
        alt = [n + 10 ** (len(s) - 2) if len(s) > 1 else n + 1, int(s[::-1]) if s[::-1][0] != "0" and s[::-1] != s else n + 2, n + 1]
        return mcq("Write <b>%s</b> in numbers." % w, n, alt, "<b>%s</b>." % in_common.comma(n))
    f.__name__ = "num_maker"
    return f
