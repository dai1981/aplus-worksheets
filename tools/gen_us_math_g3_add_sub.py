# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Add and Subtract Within 1000 (3.NBT.A.2)
  python tools/gen_us_math_g3_add_sub.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
NAMES = ["Maya", "Leo", "Ava", "Noah", "Mia", "Eli", "Zoe", "Sam", "Lily", "Ben", "Emma", "Omar", "Kai", "Nora", "Jack", "Ruby"]
PLACE = ["ones", "tens", "hundreds", "thousands"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def digits(n, k=3):
    return [(n // 10 ** i) % 10 for i in range(k)]          # ones first


def vertical_svg(a, b, op, big=False):
    """Column (vertical) layout: a over b with the sign and a line, ready to solve."""
    fs = 34 if big else 28
    cw = fs * 0.62
    W = int(cw * 5 + 24)
    H = int(fs * 2.9 + 16)
    right = W - 14
    s = []
    for row, n in enumerate([a, b]):
        t = str(n)
        y = 12 + fs * (row + 1)
        for i, ch in enumerate(reversed(t)):
            s.append("<text x='%.0f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (right - cw * (i + 0.5), y, fs, INK, ch))
    s.append("<text x='%.0f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (right - cw * 4.3, 12 + fs * 2, fs, GREEN, "+" if op == "+" else "−"))
    ly = 12 + fs * 2 + 12
    s.append("<line x1='%.0f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (right - cw * 4.8, ly, right, ly, INK))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' "
            "aria-label='%d %s %d written in columns'>%s</svg>" % (W, H, W, H, a, "plus" if op == "+" else "minus", b, "".join(s)))


# ------------------------------------------------------------ the methods, step by step
def add_steps(a, b):
    da, db = digits(a), digits(b)
    carry, parts = 0, []
    for i in range(3):
        t = da[i] + db[i] + carry
        expr = "%d + %d" % (da[i], db[i]) + (" + 1" if carry else "")
        if t >= 10 and i == 2:
            parts.append("Hundreds: %s = %d hundreds, which is 1 thousand." % (expr, t))
            carry = 0
        elif t >= 10:
            parts.append("%s: %s = %d, write %d and regroup 1 %s." % (PLACE[i].capitalize(), expr, t, t % 10,
                                                                     PLACE[i + 1][:-1]))
            carry = 1
        else:
            if not (i == 2 and t == 0 and not carry):
                parts.append("%s: %s = %d." % (PLACE[i].capitalize(), expr, t))
            carry = 0
    return " ".join(parts) + " Answer: %d." % (a + b)


def sub_steps(a, b):
    da, db = digits(a, 4), digits(b, 4)
    d = da[:]
    parts = []
    for i in range(4):
        if d[i] < db[i]:
            cur = d[i]
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                chain = ", then ".join("1 %s as 10 %s" % (PLACE[k][:-1], PLACE[k - 1]) for k in range(j, i + 1, -1))
                parts.append("There are 0 %s, so first regroup %s." % (PLACE[i + 1], chain))
            for k in range(j, i, -1):
                d[k] -= 1
                d[k - 1] += 10
            parts.append("%s: %d − %d needs a regroup. 1 %s becomes 10 %s: %d − %d = %d."
                         % (PLACE[i].capitalize(), cur, db[i], PLACE[i + 1][:-1], PLACE[i], d[i], db[i], d[i] - db[i]))
        elif i < 3:
            parts.append("%s: %d − %d = %d." % (PLACE[i].capitalize(), d[i], db[i], d[i] - db[i]))
    return " ".join(parts) + " Answer: %d. Check: %d + %d = %d." % (a - b, a - b, b, a)


# ------------------------------------------------------------ typical mistakes
def add_no_carry(a, b):
    da, db = digits(a), digits(b)
    return sum(((da[i] + db[i]) % 10) * 10 ** i for i in range(3))


def sub_small_from_big(a, b):
    """Subtracting the smaller digit from the bigger one in every column."""
    da, db = digits(a, 4), digits(b, 4)
    return sum(abs(da[i] - db[i]) * 10 ** i for i in range(4))


def sub_forgot_reduce(a, b):
    """Regrouped but did not take 1 away from the next column."""
    da, db = digits(a, 4), digits(b, 4)
    r = a - b
    for i in range(3):
        if da[i] < db[i]:
            r += 10 ** (i + 1)
    return r


def add_cands(a, b):
    s = a + b
    return [add_no_carry(a, b), s - 10, s + 10, s - 100, s + 100, s + 1, s - 1]


def sub_cands(a, b):
    r = a - b
    return [sub_small_from_big(a, b), sub_forgot_reduce(a, b), a + b, r + 10, r - 10, r + 100, r - 100]


def regroups_add(a, b):
    da, db = digits(a), digits(b)
    c, n = 0, 0
    for i in range(3):
        t = da[i] + db[i] + c
        c = 1 if t >= 10 else 0
        n += c
    return n


def regroups_sub(a, b):
    da, db = digits(a, 4), digits(b, 4)
    d, n = da[:], 0
    for i in range(3):
        if d[i] < db[i]:
            n += 1
            d[i] += 10
            d[i + 1] -= 1
    return n


# ------------------------------------------------------------ sets
def pick_add(rnd, want, lo=100, seen=None):
    while True:
        a, b = rnd.randint(lo, 899), rnd.randint(lo, 899)
        if a + b > 1000 or (a, b) in seen or (b, a) in seen:
            continue
        if regroups_add(a, b) == want:
            seen.add((a, b))
            return a, b


def pick_sub(rnd, want, seen, zeros=False):
    while True:
        if zeros:
            a = rnd.choice([rnd.randint(1, 9) * 100, rnd.randint(1, 9) * 100 + rnd.randint(1, 9), 1000])
        else:
            a = rnd.randint(200, 999)
        b = rnd.randint(100, a - 50) if a > 160 else None
        if b is None or (a, b) in seen:
            continue
        if zeros and digits(a, 4)[1] != 0:
            continue
        if zeros or regroups_sub(a, b) == want:
            if zeros and regroups_sub(a, b) < 2:
                continue
            seen.add((a, b))
            return a, b


def item_add(a, b, rnd, col):
    q = (fig(vertical_svg(a, b, "+")) + "Add.") if col else "What is %d + %d?" % (a, b)
    return mcq(q, a + b, add_cands(a, b), add_steps(a, b), rnd)


def item_sub(a, b, rnd, col):
    q = (fig(vertical_svg(a, b, "-")) + "Subtract.") if col else "What is %d − %d?" % (a, b)
    return mcq(q, a - b, sub_cands(a, b), sub_steps(a, b), rnd)


def set_add1(rnd, seen):
    its = []
    for i in range(20):
        a, b = pick_add(rnd, 0 if i < 8 else 1, seen=seen)
        its.append(item_add(a, b, rnd, i % 2 == 1))
    return {"title": "Add 3-digit numbers", "items": its}


def set_add2(rnd, seen):
    its = []
    for i in range(16):
        a, b = pick_add(rnd, 2, seen=seen)
        its.append(item_add(a, b, rnd, i % 2 == 0))
    for a in rnd.sample([137, 245, 362, 478, 519, 683, 726, 854], 2):     # make exactly 1000
        its.append(item_add(a, 1000 - a, rnd, True))
    for _ in range(2):                                                  # 2-digit + 3-digit
        a, b = rnd.randint(46, 98), rnd.randint(305, 860)
        while regroups_add(a, b) < 2 or a + b > 1000:
            a, b = rnd.randint(46, 98), rnd.randint(305, 860)
        its.append(item_add(b, a, rnd, False))
    rnd.shuffle(its)
    return {"title": "Add with regrouping", "items": its}


def set_sub1(rnd, seen):
    its = []
    for i in range(20):
        a, b = pick_sub(rnd, 0 if i < 6 else 1, seen)
        its.append(item_sub(a, b, rnd, i % 2 == 1))
    return {"title": "Subtract 3-digit numbers", "items": its}


def set_sub2(rnd, seen):
    its = []
    for i in range(10):
        a, b = pick_sub(rnd, 2, seen)
        its.append(item_sub(a, b, rnd, i % 2 == 0))
    for i in range(10):
        a, b = pick_sub(rnd, 2, seen, zeros=True)
        its.append(item_sub(a, b, rnd, i % 2 == 1))
    rnd.shuffle(its)
    return {"title": "Subtract with regrouping and zeros", "items": its}


def set_story(rnd):
    its = []
    names = NAMES[:]
    rnd.shuffle(names)

    def nm():
        n = names.pop(0)
        names.append(n)
        return n

    # missing numbers: use the other operation
    for _ in range(3):
        x, b = rnd.randint(150, 520), rnd.randint(140, 430)
        s = x + b
        its.append(mcq("What number goes in the box?  <b>☐ + %d = %d</b>" % (b, s), x,
                       [s + b, x + 10, x - 10, x + 100, sub_small_from_big(s, b)],
                       "Use subtraction: %d − %d = %d. Check: %d + %d = %d." % (s, b, x, x, b, s), rnd))
    for _ in range(3):
        a, x = rnd.randint(520, 950), rnd.randint(130, 400)
        r = a - x
        its.append(mcq("What number goes in the box?  <b>%d − ☐ = %d</b>" % (a, r), x,
                       [a + r, x + 10, x - 10, x + 100, r],
                       "Think: %d − ? = %d. Subtract: %d − %d = %d. Check: %d − %d = %d." % (a, r, a, r, x, a, x, r), rnd))
    # estimate to check
    for a, b, op in [(487, 312, "+"), (623, 289, "+"), (812, 395, "−"), (704, 286, "−")]:
        ra, rb = round(a, -2), round(b, -2)
        est = ra + rb if op == "+" else ra - rb
        exact = a + b if op == "+" else a - b
        its.append(mcq("Round each number to the nearest hundred. Which is the best estimate for %d %s %d?" % (a, op, b),
                       "about %d" % est, ["about %d" % v for v in [est + 100, est - 100, est + 200]],
                       "%d rounds to %d and %d rounds to %d. %d %s %d = %d. The exact answer, %d, is close to %d."
                       % (a, ra, b, rb, ra, op, rb, est, exact, est), rnd))
    # word problems: (text with {n} name, {a} {b} numbers, {p} pronoun, {t} total stock), operation, unit
    stories = [
        ("{n}'s school has {a} students in the morning. {b} more students come for an afternoon event. "
         "How many students are there in all?", "+", "students"),
        ("A library had {a} books. It got {b} new books. How many books does it have now?", "+", "books"),
        ("{n} scored {a} points in the first round of a game and {b} points in the second round. "
         "What was the total score?", "+", "points"),
        ("A shop had {t} stickers. It sold {a} stickers in the morning and {b} in the afternoon. "
         "How many stickers were sold in all?", "+", "stickers"),
        ("A farm had {a} eggs. {b} eggs were sold at the market. How many eggs are left?", "-", "eggs"),
        ("{n}'s book has {a} pages. {p} has read {b} pages. How many pages are left to read?", "-", "pages"),
        ("A stadium has {a} seats. {b} seats are filled. How many seats are empty?", "-", "seats"),
        ("On Saturday, {a} people visited the zoo. On Sunday, {b} people visited. How many more people visited on "
         "Saturday than on Sunday?", "-", "people"),
    ]
    girls = ("Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby")
    for t, op, unit in stories:
        n = nm()
        if op == "+":
            a, b = rnd.randint(180, 560), rnd.randint(140, 420)
            while regroups_add(a, b) == 0 or a + b > 1000:
                a, b = rnd.randint(180, 560), rnd.randint(140, 420)
            ans, e = a + b, ("Put the two amounts together: add. " + add_steps(a, b))
            cands = add_cands(a, b) + [abs(a - b)]
        else:
            a = rnd.randint(420, 950)
            b = rnd.randint(150, a - 80)
            while regroups_sub(a, b) == 0:
                a = rnd.randint(420, 950)
                b = rnd.randint(150, a - 80)
            ans = a - b
            e = ("How many more means find the difference: subtract. " if "more" in t else "Take one part away from the whole: subtract. ") + sub_steps(a, b)
            cands = sub_cands(a, b)
        q = t.format(n=n, a=a, b=b, p="She" if n in girls else "He", t=a + b + rnd.randint(60, 200))
        its.append(mcq(q, "%d %s" % (ans, unit), ["%d %s" % (v, unit) for v in cands if v > 0], e, rnd))
    # two more with a 3-digit + 3-digit to 1000
    a = rnd.choice([365, 428, 572, 649])
    its.append(mcq("%s wants to read 1000 pages this summer. So far %s has read %d pages. How many more pages does %s need to read?"
                   % ("Leo", "he", a, "he"), "%d pages" % (1000 - a),
                   ["%d pages" % v for v in [sub_small_from_big(1000, a), 1000 - a + 100, 1000 - a + 10, 1000 + a]],
                   "Find 1000 − %d. " % a + sub_steps(1000, a), rnd))
    a, b = 268, 159
    its.append(mcq("A bakery made %d muffins and %d bagels. How many more muffins than bagels did it make?" % (a, b),
                   "%d muffins" % (a - b), ["%d muffins" % v for v in [sub_small_from_big(a, b), sub_forgot_reduce(a, b), a + b, a - b + 10]],
                   "How many more means subtract. " + sub_steps(a, b), rnd))
    rnd.shuffle(its)
    return {"title": "Missing numbers, estimates and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Line up the places</h2>"
        "<p>Every 3-digit number has <b>hundreds, tens and ones</b>. Write the numbers in columns so ones are under ones, "
        "tens under tens and hundreds under hundreds. Then work from the <b>ones</b> to the left.</p>"
        "<figure class='sn-fig'>" + vertical_svg(347, 285, "+", big=True) +
        "<figcaption>Ones: 7 + 5 = 12, write 2 and regroup 1 ten. Tens: 4 + 8 + 1 = 13, write 3 and regroup 1 hundred. "
        "Hundreds: 3 + 2 + 1 = 6. Answer: 632.</figcaption></figure>"
        "<h2>Add by place value</h2>"
        "<p>You can also break the numbers apart and add each place.</p>" +
        table(["Place", "347 + 285", "Sum"], [
            ["Hundreds", "300 + 200", "500"],
            ["Tens", "40 + 80", "120"],
            ["Ones", "7 + 5", "12"],
            ["Total", "500 + 120 + 12", "<b>632</b>"],
        ]) +
        "<h2>Subtract with regrouping</h2>"
        "<p>If the top digit is smaller, <b>regroup</b>: take 1 from the next place to the left and make 10 in this place.</p>"
        "<figure class='sn-fig'>" + vertical_svg(623, 258, "-", big=True) +
        "<figcaption>Ones: 3 − 8 needs a regroup. 1 ten becomes 10 ones: 13 − 8 = 5. Tens: now 1 − 5 needs a regroup. "
        "1 hundred becomes 10 tens: 11 − 5 = 6. Hundreds: 5 − 2 = 3. Answer: 365.</figcaption></figure>" +
        ex("Subtract across zeros", "What is 500 − 263?",
           "The tens place is 0, so regroup 1 hundred as 10 tens first. Then regroup 1 ten as 10 ones. "
           "Now it is 4 hundreds, 9 tens, 10 ones. Ones: 10 − 3 = 7. Tens: 9 − 6 = 3. Hundreds: 4 − 2 = 2.", "237") +
        "<h2>Check your answer</h2>"
        "<p><b>Addition and subtraction undo each other.</b> After subtracting, add your answer to the number you took away. "
        "You should get the number you started with: 365 + 258 = 623. You can also <b>estimate</b>: 623 − 258 is about "
        "600 − 300 = 300, so 365 makes sense.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the regrouped 1 (347 + 285 = 522)", "Write the small 1 above the next column and add it"],
            ["Taking the smaller digit from the bigger one (623 − 258 = 435)", "Always take the bottom digit from the top digit. Regroup when the top is smaller"],
            ["Regrouping but not crossing out (623 − 258 = 475)", "When you take 1 ten, the tens digit gets 1 smaller"],
            ["Lining up the numbers on the left", "Line up the ones on the right"],
        ])
    )


FAQ = [
    {"q": "How do you add 3-digit numbers with regrouping?",
     "a": "Line up the ones, tens and hundreds. Add the ones first. If the sum is 10 or more, write the ones digit and regroup 1 ten to the tens column. Do the same for the tens, then add the hundreds."},
    {"q": "How do you subtract across zeros, like 500 − 263?",
     "a": "There are no tens to regroup, so first regroup 1 hundred as 10 tens. Then regroup 1 ten as 10 ones. Now you have 4 hundreds, 9 tens and 10 ones, and you can subtract each place: 237."},
    {"q": "How can my child check a subtraction answer?",
     "a": "Add the answer to the number that was subtracted. If you get the starting number, the answer is right. For 623 − 258 = 365, check 365 + 258 = 623."},
    {"q": "What does 3.NBT.A.2 mean?",
     "a": "It is the Common Core standard for Grade 3: fluently add and subtract within 1000 using place value strategies, properties of operations and the link between addition and subtraction."},
]


def gen_add_sub():
    rnd = random.Random(38)
    seen_a, seen_s = set(), set()
    sets = [set_add1(rnd, seen_a), set_add2(rnd, seen_a), set_sub1(rnd, seen_s), set_sub2(rnd, seen_s), set_story(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "add-subtract-within-1000", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Add and Subtract Within 1000",
        "seo_title": "Grade 3 Addition and Subtraction Within 1000 Worksheets: 3-Digit Regrouping and Word Problems",
        "short_title": "Add and subtract within 1000",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "3.NBT.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/NBT/A/2/",
        "standard_text": "Fluently add and subtract within 1000 using strategies and algorithms based on place value, properties of operations, and/or the relationship between addition and subtraction.",
        "meta_desc": "Free Grade 3 worksheets for adding and subtracting 3-digit numbers: regrouping, subtracting across zeros, missing numbers, estimating to check and word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Line up the places. Start with the ones. Regroup when you need to.",
        "key_sub": "Adding: 10 ones make 1 ten, 10 tens make 1 hundred. Subtracting: if the top digit is smaller, take 1 from the next place to the left. Check by adding back.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_add_sub()
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
