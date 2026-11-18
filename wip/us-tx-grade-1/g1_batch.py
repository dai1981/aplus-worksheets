import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
T = open(os.path.join(here, "g1tmpl.txt")).read()
OUT = "/home/claude/aplus-worksheets/tools"
U = []

NO = "Number and Operations"
AR = "Algebraic Reasoning"
GM = "Geometry and Measurement"
DA = "Data Analysis"
P = "Proportionality"
EER = "Expressions, Equations and Relationships"
MD = "Measurement and Data"
PFL = "Personal Financial Literacy"


def unit(**k):
    k.setdefault("extra", "")
    U.append(k)


def imp(seed, *mods, extra=""):
    """Import US modules that use a module-level R and reseed them for Texas."""
    lines = ["import random"]
    for i, (m, a) in enumerate(mods):
        lines.append("import %s as %s" % (m, a))
        lines.append("adopt(%s)" % a)
        lines.append("%s.R = random.Random(%d)" % (a, seed * 10 + i))
    if extra:
        lines.append(extra)
    return "\n".join(lines)


def mods(*pairs):
    lines = []
    for m, a in pairs:
        lines.append("import %s as %s" % (m, a))
        lines.append("adopt(%s)" % a)
    return "\n".join(lines)


UNIQ = '''def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f

'''


ABCD = '''import random as _random


def abcd(mod, fn, seed):
    """Build A-D picture items (_abcd) now, with the right picture at a random position."""
    rr = _random.Random(seed)
    def f(*a):
        st = fn(*a)
        for it in (st["items"] if isinstance(st, dict) else st):
            if "_abcd" in it:
                parts = it.pop("_abcd")
                prompt, right, wrong = parts[0], parts[1], list(parts[2])
                t = rr.randrange(4)
                rr.shuffle(wrong)
                it["q"] = mod.fig(mod.abcd_svg(wrong[:t] + [right] + wrong[t:], *parts[3:])) + prompt
                it["a"] = t
                it["e"] = it["e"].replace("{L}", "ABCD"[t])
        return st
    f.__name__ = fn.__name__
    return f

'''


files = sys.argv[1:] or ["g1_u_a.py", "g1_u_b.py", "g1_u_c.py"]
for f in files:
    exec(open(os.path.join(here, f)).read())

for u in U:
    open(os.path.join(OUT, "gen_ustx_math_g1_%s.py" % u["fname"]), "w").write(T % u)
print("wrote", len(U), [u["fname"] for u in U])
