# -*- coding: utf-8 -*-
"""
Shared runner for Nigeria / Mathematics (NERDC 9-Year Basic Education Curriculum).
Each grade file (ng_p1.py … ng_p6.py, ng_j1.py … ng_j3.py) defines units() and calls main().
  python3 tools/ng_p5.py [number …]      seed = BASE + number
Parts of a set:
  co(fn, n)            n items from an own maker fn(r) (Nigerian money allowed)
  cx(fn, n)            n items from another country's one_x(r) maker (items with money dropped)
  rs(m, "set_x", n)    n items from another country's set maker; its arguments are filled in from their names
"""
import importlib
import inspect
import random
import re
import sys
import ng_common as C
from ng_common import finish, make, lesson, adopt, build_sets, example

TH_P = {"N": "Number and Numeration", "O": "Basic Operations", "A": "Algebraic Processes", "M": "Measurement", "G": "Geometry", "S": "Everyday Statistics"}
TH_J = {"N": "Number and Numeration", "O": "Basic Operations", "A": "Algebraic Processes", "G": "Mensuration and Geometry", "M": "Mensuration and Geometry", "S": "Everyday Statistics"}
MONEY = re.compile(r"₦|\bnaira\b|\bkobo\b|£|\$|\bpence\b")


def mod(name, seed):
    m = importlib.import_module(name)
    adopt(m)
    if isinstance(getattr(m, "R", None), random.Random):
        m.R = random.Random(seed)
    return m


def _plain(it):
    return re.sub(r"<svg.*?</svg>", " ", it["q"] + " " + it.get("e", "") + " " + " ".join(it["c"]), flags=re.S)


def nomoney(it):
    return not MONEY.search(_plain(it))


def both(*fs):
    return lambda it: all(f(it) for f in fs if f)


def le(n):
    """keep: every number in the question and in the answer is at most n."""
    def k(it):
        t = re.sub(r"<[^>]+>", " ", re.sub(r"<svg.*?</svg>", " ", it["q"] + " " + it["c"][it["a"]], flags=re.S))
        return all(int(x.replace(",", "")) <= n for x in re.findall(r"\d[\d,]*", t))
    return k


def uniq(fn, keep=None):
    seen = set()

    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen or (keep and not keep(it)):
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = getattr(fn, "__name__", "maker")
    return f


def co(fn, n, keep=None):
    return ("collect", uniq(fn, keep), n)


def cx(fn, n, keep=None, money=False):
    return ("collect", uniq(fn, keep if money else both(nomoney, keep)), n)


ARG = {"P": ("People", "People2"), "Pp": ("People", "Pp", "People2"), "pk": ("Picker", "Pk"), "pos": ("Pos", "Spots", "Place"),
       "people": ("People",), "P2": ("People2", "People"), "spots": ("Spots",), "PK": ("Picker",), "P_": ("People",), "PP": ("People", "Pos")}


def rs(m, name, n, keep=None, money=False, **over):
    fn = getattr(m, name)
    args = []
    for p in inspect.signature(fn).parameters.values():
        if p.name in over:
            args.append(over[p.name])
        elif p.default is not inspect._empty:
            break
        elif p.name in ("rnd", "r", "R"):
            args.append("rnd")
        elif p.name in ("seen", "used", "used_blobs"):
            args.append("seen")
        elif p.name == "people" and isinstance(getattr(m, "PEOPLE", None), list):
            def mk(r, L=m.PEOPLE):
                l = list(L)
                r.shuffle(l)
                return iter(l * 3)
            args.append(mk)
        elif p.name in ARG:
            for cl in ARG[p.name]:
                if hasattr(m, cl):
                    args.append(getattr(m, cl))
                    break
            else:
                raise KeyError("%s.%s: no class for %s" % (m.__name__, name, p.name))
        elif callable(getattr(m, p.name, None)):
            args.append(getattr(m, p.name))
        else:
            raise KeyError("%s.%s: unknown argument %s" % (m.__name__, name, p.name))
    return ("run", fn, tuple(args), n) + ((keep if money else both(nomoney, keep),))


def ru(fn, args, n, keep=None):
    return ("run", fn, args, n) + ((keep,) if keep else ())


def ul(items):
    return "<ul>" + "".join("<li>%s</li>" % x for x in items) + "</ul>"


def U(slug, th, std, title, short, meta, kb, ks, sets, think, ex, mist, faq):
    return dict(slug=slug, th=th, std=std, title=title, short=short, meta=meta, kb=kb, ks=ks, sets=sets, think=think, ex=ex, mist=mist, faq=faq)


def main(grade, label, units, base, th=None, max_num=None):
    C.GRADE = grade
    C.LABEL = label
    th = th or (TH_J if grade.startswith("jss") else TH_P)
    want = sys.argv[1:]
    us = units()
    for i, u in enumerate(us, 1):
        if want and str(i) not in want:
            continue
        sets, rnd = build_sets2(u["sets"], base + i)
        finish(sets, rnd, max_num)
        body = lesson(u["think"], u["ex"], u["mist"])
        make(u["slug"], i, th[u["th"]], label + ": " + th[u["th"]], u["std"] + " (summary of the NERDC %s Mathematics curriculum)" % label,
             u["title"], u["short"], u["meta"], u["kb"], u["ks"], body, u["faq"], sets)
        print(i, u["slug"], flush=True)


# ------------------------------------------------------------ sets that tolerate a short part
import signal


def _alarm(*a):
    raise TimeoutError("set maker took too long")


def _run_part(p, seed, k, avoid):
    """Up to k items from one part (fewer if the maker runs dry)."""
    if k <= 0:
        return []
    if p[0] == "run":
        fn, args = p[1], p[2]
        keep = p[4] if len(p) > 4 else None
        for full in (False, True):
            out, seen = [], set()
            key = (lambda x: C.ng_text(x["q"]) + "|" + "|".join(sorted(C.ng_text(c) for c in x["c"]))) if full else (lambda x: C.ng_text(x["q"]))
            for a in avoid:
                for x in a:
                    seen.add(key(x))
            for j in range(40):
                signal.signal(signal.SIGALRM, _alarm)
                signal.alarm(4)
                try:
                    its = C.run(fn, *args, seed=seed * 100 + j)["items"]
                except (AssertionError, TimeoutError):
                    continue
                finally:
                    signal.alarm(0)
                for it in its:
                    if "build" in it:
                        it = it["build"](random.Random(seed * 1000 + j * 50 + len(out)).randrange(4))
                    if "q" not in it or not C.ng_ok(it) or key(it) in seen or (keep and not keep(it)):
                        continue
                    seen.add(key(it))
                    out.append(it)
                    if len(out) == k:
                        return out
            if len(out) >= k * 0.75 or full:
                return out
        return out
    maker = p[1]
    rnd = random.Random(seed)
    out, seen, bad = [], set(), set()
    for a in avoid:
        for x in a:
            bad.add(re.sub(r"\s+", " ", C.ng_text(x["q"])))
    for _ in range(4000):
        try:
            it = maker(rnd)
        except (AssertionError, TypeError, ValueError, KeyError, IndexError, ZeroDivisionError, AttributeError):
            continue
        if not it or not C.ng_ok(it):
            continue
        kk = (re.sub(r"\s+", " ", C.ng_text(it["q"])), tuple(sorted(it["c"])))
        if kk in seen or kk[0] in bad:
            continue
        seen.add(kk)
        out.append(it)
        if len(out) == k:
            break
    return out


def build_sets2(specs, seed):
    rnd = random.Random(seed)
    sets = []
    for si, (title, parts) in enumerate(specs):
        got = [[] for _ in parts]
        for pi, p in enumerate(parts):
            prev = [it for s in sets for it in s["items"]] + [it for g in got for it in g]
            got[pi] = _run_part(p, seed % 10000 * 7 + si * 10 + pi, p[3] if p[0] == "run" else p[2], [prev])
        short = 20 - sum(len(g) for g in got)
        tries = 0
        while short > 0 and tries < 3:
            for pi, p in enumerate(parts):
                if short <= 0:
                    break
                prev = [it for s in sets for it in s["items"]] + [it for g in got for it in g]
                more = _run_part(p, seed % 10000 * 7 + si * 10 + pi + 500 * (tries + 1), short, [prev])
                got[pi] += more
                short -= len(more)
            tries += 1
        items = [it for g in got for it in g]
        assert len(items) == 20, (title, len(items))
        sets.append(C.S(title, items))
    return sets, rnd
