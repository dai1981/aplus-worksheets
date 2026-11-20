# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Numeric Patterns, Flow Diagrams and Input-Output Tables (Grade 4: 2.1 Numeric patterns)
  python3 tools/gen_za_maths_g4_numeric_patterns.py
Extending number sequences with a constant difference or ratio, finding the rule (US Grade 4 and BC Grade 4
makers), flow diagrams (own maker) and input-output tables (BC Grade 4 maker).
Wrong answers come from real mistakes: using only the first two numbers to find the rule, adding when the pattern
multiplies, and applying the rule to the output instead of the input.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g4_patterns as usp
adopt(usp)
if hasattr(usp, 'R'): usp.R = random.Random(804120)
import gen_cabc_math_g4_patterns as cbp
adopt(cbp)
if hasattr(cbp, 'R'): cbp.R = random.Random(804121)
za_common.GRADE = "grade-4"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"]
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", t) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def le10000(it):
    return all(n <= 10000 for n in _nums(it))


def nodec(it):
    t = _re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]))
    return not _re.search(r"\d\.\d", t)


from ws_common import svg_wrap, text, GREEN, FILL, INK


def flow_svg(rule, ins, outs):
    """flow diagram: inputs -> [rule] -> outputs"""
    n = len(ins)
    H = 40 + 34 * n
    b = "<rect x='150' y='%d' width='110' height='44' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (H / 2 - 22, FILL, GREEN) + text(205, H / 2 + 6, rule, 18)
    for i, (a, c) in enumerate(zip(ins, outs)):
        y = 30 + 34 * i
        b += text(60, y + 6, a, 17) + text(350, y + 6, c, 17, col="#c0392b" if c == "?" else INK)
        b += "<line x1='85' y1='%d' x2='148' y2='%.0f' stroke='%s' stroke-width='1.5'/>" % (y, H / 2, INK)
        b += "<line x1='262' y1='%.0f' x2='325' y2='%d' stroke='%s' stroke-width='1.5'/>" % (H / 2, y, INK)
    b += text(60, 14, "Input", 13) + text(350, 14, "Output", 13)
    return svg_wrap(410, H, b, "flow diagram with the rule %s" % rule)


def one_flow(r):
    op = r.choice(["+", "−", "×", "÷"])
    k = {"+": r.randint(5, 99), "−": r.randint(3, 49), "×": r.randint(2, 10), "÷": r.randint(2, 10)}[op]
    if op == "÷":
        ins = [k * x for x in r.sample(range(2, 13), 4)]
    else:
        ins = r.sample(range(k + 1 if op == "−" else 1, 100), 4)
    f = {"+": lambda x: x + k, "−": lambda x: x - k, "×": lambda x: x * k, "÷": lambda x: x // k}[op]
    outs = [f(x) for x in ins]
    i = r.randrange(4)
    if r.random() < 0.6:
        shown = [str(o) if j != i else "?" for j, o in enumerate(outs)]
        right = outs[i]
        wr = [{"+": ins[i] - k, "−": ins[i] + k, "×": ins[i] + k, "÷": ins[i] * k}[op], right + 1, outs[(i + 1) % 4]]
        return mcq(fig(flow_svg("%s %d" % (op, k), [str(x) for x in ins], shown)) + "What is the missing output?", right, [x for x in wr if x != right and x >= 0] + [right + 10],
                   "The rule is %s %d: %d %s %d = <b>%d</b>." % (op, k, ins[i], op, k, right))
    rules = ["%s %d" % (op, k)]
    for o2, k2 in (("+", outs[0] - ins[0]), ("×", k), ("+", k), ("−", k)):
        cand = "%s %d" % (o2, abs(k2))
        if cand not in rules and k2 != 0:
            rules.append(cand)
    right = rules[0]
    return mcq(fig(flow_svg("?", [str(x) for x in ins], [str(o) for o in outs])) + "What is the rule in the flow diagram?", right, rules[1:4] + ["÷ 2", "+ 1"],
               "Check every input: %s. The rule is <b>%s</b>." % ("; ".join("%d %s %d = %d" % (x, op, k, f(x)) for x in ins[:3]), right))


def build():
    sets, R = build_sets([
        ("Extend the pattern", [("run", usp.set_extend, ("rnd",), 10, le10000), ("run", cbp.set_increasing, (), 10, le10000)]),
        ("Decreasing patterns", [("run", cbp.set_decreasing, (), 20, le10000)]),
        ("Find the rule", [("run", usp.set_find_rule, ("rnd",), 20, le10000)]),
        ("Flow diagrams", [("collect", uniq(one_flow), 20)]),
        ("Input and output tables", [("run", cbp.set_io, (), 10, le10000), ("run", cbp.set_predict, (), 10, le10000)]),
    ], 80412)
    finish(sets, R)
    body = lesson('<ul><li>A numeric pattern follows a <b>rule</b>. Look at how each number changes: add, subtract, multiply or divide by the same number.</li><li>Check the rule on <b>every</b> pair of numbers.</li><li>A <b>flow diagram</b> shows input values, a rule and output values: 6 → × 4 → 24.</li><li>A table shows the same: input in the top row, output in the bottom row.</li></ul>',
        [example("4, 12, 36, 108, …", ["4 × 3 = 12, 12 × 3 = 36"], "rule × 3; next 324")],
        [['Only two numbers', '4, 12 could be + 8 or × 3. Check the next pair.'], ['Adding instead of multiplying', 'Fast-growing patterns often multiply.'], ['Rule on the output', 'Apply the rule to the input.']])
    faq = [('What does CAPS Grade 4 say about numeric patterns?', 'Investigate and extend numeric patterns looking for relationships or rules of patterns: sequences with a constant difference or ratio, and patterns represented in flow diagrams and tables.'), ('What is a constant difference?', 'The same number is added or subtracted each time.'), ('What is a constant ratio?', 'Each number is multiplied by the same number.'), ('What is a flow diagram?', 'A picture of input numbers, a rule and output numbers.')]
    make('numeric-patterns', 12, 'Patterns, Functions and Algebra', 'Grade 4: 2.1 Numeric patterns',
         "Investigate and extend numeric patterns looking for relationships or rules of patterns: sequences involving a constant difference or ratio, of learner's own creation; describe the general rules for the observed relationships; determine input values, output values and rules for patterns and relationships using flow diagrams and tables.",
         'Numeric Patterns, Flow Diagrams and Input-Output Tables', 'Numeric Patterns',
         'Free CAPS Grade 4 numeric patterns worksheets: extending sequences, finding the rule, flow diagrams and input-output tables. 100 questions with memos.',
         'Find the rule, then check it on every number.', 'Flow diagram: input → rule → output.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
