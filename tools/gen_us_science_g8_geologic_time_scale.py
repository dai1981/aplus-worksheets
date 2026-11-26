# -*- coding: utf-8 -*-
"""
US Grade 8 Science: The Geologic Time Scale (MS-ESS1-4)
  python tools/gen_us_science_g8_geologic_time_scale.py
Construct a scientific explanation based on evidence from rock strata for how the geologic time scale is used to
organize Earth's 4.6-billion-year-old history. Eons and eras (Precambrian, Paleozoic, Mesozoic, Cenozoic) with
boundaries marked by mass extinctions; relative dating (superposition, cross-cutting, index fossils); absolute dating
(half-lives); scaling Earth history to a clock or calendar.
Wrong answers come from real mistakes: "humans appeared early in Earth's history", "an intrusion is older than the rock
it cuts", "eras are equal lengths", "half-life means half of the time has passed".
"""
from sci_common import Unit, item, bank, lesson, make, table, People, comma

U = Unit(80121)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# event, millions of years ago, era
EV = [("Earth forms", 4600, "Precambrian"), ("first single-celled life appears", 3500, "Precambrian"), ("oxygen builds up in the atmosphere", 2400, "Precambrian"),
      ("first animals with hard shells (Cambrian explosion)", 540, "Paleozoic"), ("first land plants", 470, "Paleozoic"), ("first fish with jaws", 430, "Paleozoic"),
      ("coal swamp forests grow", 330, "Paleozoic"), ("the largest mass extinction (end of the Permian)", 252, "Paleozoic"), ("first dinosaurs", 233, "Mesozoic"),
      ("first mammals", 210, "Mesozoic"), ("first birds", 150, "Mesozoic"), ("first flowering plants", 130, "Mesozoic"), ("an asteroid impact ends the dinosaurs", 66, "Mesozoic"),
      ("first grasslands spread", 25, "Cenozoic"), ("first members of the human family", 6, "Cenozoic"), ("modern humans (Homo sapiens) appear", 0.3, "Cenozoic")]


def mya(x):
    return ("%s million years ago" % comma(x)) if x >= 1 else "about 300,000 years ago"


def g_order():
    who = P.next()[0]
    evs = R.sample(EV, 3)
    k = R.choice(["first", "last"])
    if not once((tuple(sorted(e[0] for e in evs)), k)):
        return None
    if k == "first":
        a = max(evs, key=lambda e: e[1])[0]
        q = "happened first"
    else:
        a = min(evs, key=lambda e: e[1])[0]
        q = "happened most recently"
    return item("%s is building a timeline. Which of these events %s?" % (who, q), a, [e[0] for e in evs if e[0] != a] + ["They all happened at the same time."],
                "; ".join("%s: %s" % (e[0], mya(e[1])) for e in sorted(evs, key=lambda e: -e[1])) + ".")


def g_era():
    e, t, era = R.choice(EV)
    who = P.next()[0]
    if not once(("era", e)):
        return None
    return item("%s's timeline lists this event: %s (%s). In which part of the time scale did it happen? (Paleozoic: 541–252, Mesozoic: 252–66, Cenozoic: 66–now, in millions of years ago)" % (who, e, mya(t)), era,
                [x for x in ["Precambrian", "Paleozoic", "Mesozoic", "Cenozoic"] if x != era], "%s %s falls in the %s." % (e[0].upper() + e[1:], mya(t), era))


def g_clock():
    who = P.next()[0]
    k = R.choice(["hours", "day"])
    e, t, _ = R.choice(EV[1:])
    if not once((k, e)):
        return None
    if k == "hours":
        # 4,600 million years -> 24 hours; time left before midnight
        mins = t / 4600 * 24 * 60
        if mins >= 180:
            h = round(mins / 60, 1)
            a = "about %g hours before midnight" % h
            w = ["about %g hours before midnight" % round(h / 2, 1), "about %g hours before midnight" % min(24, round(h * 2, 1)) if h * 2 <= 24 else "about 1 minute before midnight", "about %g hours after midnight" % h]
        elif mins >= 1:
            a = "about %d minutes before midnight" % round(mins)
            w = ["about %d hours before midnight" % round(mins), "about %d seconds before midnight" % round(mins), "about %d minutes after midnight" % round(mins)]
        else:
            secs = mins * 60
            a = "about %d seconds before midnight" % max(1, round(secs))
            w = ["about %d minutes before midnight" % max(1, round(secs)), "about %d hours before midnight" % max(1, round(secs)), "right at noon"]
        if a in w:
            return None
        return item("%s squeezes Earth's 4.6-billion-year history into one 24-hour day, with Earth forming at midnight and today at the next midnight. On this clock, when did this happen: %s (%s)?" % (who, e, mya(t)),
                    a, w, "%s ÷ 4,600 × 24 hours." % comma(t) if t >= 1 else "Modern humans are a tiny fraction of Earth's history.")
    frac = 1 - t / 4600
    a = "%d%%" % round(frac * 100) if round(frac * 100) < 100 else "more than 99%"
    w = ["%d%%" % round(t / 4600 * 100) if round(t / 4600 * 100) != round(frac * 100) else "50%", "50%", "10%"]
    w = [x for x in dict.fromkeys(w) if x != a]
    while len(w) < 3:
        w.append(["25%", "75%", "5%"][len(w)])
    return item("%s reads about this event: %s (%s). About what percent of Earth's 4.6-billion-year history had already passed?" % (who, e, mya(t)), a, w[:3],
                "(4,600 − %s) ÷ 4,600 ≈ %s." % (comma(t) if t >= 1 else "0.3", a))


def g_half():
    who = P.next()[0]
    n = R.choice([1, 2, 3, 4])
    hl = R.choice([("carbon-14", 5730, "years"), ("potassium-40", 1300, "million years"), ("uranium-235", 704, "million years")])
    k = R.choice(["left", "age"])
    if not once((hl[0], n, k)):
        return None
    left = {1: "1/2", 2: "1/4", 3: "1/8", 4: "1/16"}[n]
    if k == "left":
        return item("%s's sample is %d half-li%s old for %s (half-life %s %s). What fraction of the original %s is left?" % (who, n, "fe" if n == 1 else "ves", hl[0], comma(hl[1]), hl[2], hl[0]), left,
                    [x for x in ["1/2", "1/4", "1/8", "1/16", "1/3"] if x != left][:3], "Each half-life cuts the amount in half %d time%s." % (n, "" if n == 1 else "s"))
    return item("A sample has %s of its original %s left. The half-life is %s %s. About how old is %s's sample?" % (left, hl[0], comma(hl[1]), hl[2], who), "%s %s" % (comma(hl[1] * n), hl[2]),
                ["%s %s" % (comma(hl[1] * (n + 1)), hl[2]), "%s %s" % (comma(round(hl[1] / 2)), hl[2]), "%s %s" % (comma(hl[1] * n * 2), hl[2])],
                "%s left means %d half-li%s: %d × %s." % (left, n, "fe" if n == 1 else "ves", n, comma(hl[1])))


REL = [("A layer of volcanic rock (an intrusion) cuts through three sedimentary layers.", "The intrusion is younger than the layers it cuts."),
       ("A fault breaks layers A, B and C but not layer D on top.", "The fault happened after A, B and C formed but before D."),
       ("A worn, uneven surface (an unconformity) lies between two sets of layers.", "Some rock was eroded away, so part of the record is missing."),
       ("The same trilobite species is found in layers in Wales and in New York.", "The two layers formed at about the same time (an index fossil)."),
       ("Tilted layers are covered by flat layers.", "The tilted layers formed and were tilted before the flat layers were deposited."),
       ("Pebbles of granite are found inside a sandstone layer.", "The granite is older than the sandstone.")]


def g_rel():
    s, a = R.choice(REL)
    who = P.next()[0]
    if not once(("r", s)):
        return None
    w = [x[1] for x in REL if x[1] != a]
    return item("%s observes in a cliff: “%s” What can be concluded?" % (who, s), a, R.sample(w, 3), "Relative dating uses superposition, cross-cutting features, unconformities, inclusions and index fossils.")


B1 = bank([
    ("How old is Earth?", "about 4.6 billion years", ["about 6,000 years", "about 66 million years", "about 100 billion years"], "From radiometric dating."),
    ("What is the geologic time scale?", "a timeline that divides Earth's history into eons, eras, periods and epochs", ["a scale for weighing rocks", "a calendar for one year", "a map of rock layers in one place"],
     "Based on rock and fossil evidence."),
    ("What often marks the boundary between two eras?", "a mass extinction and big change in fossils", ["a full moon", "the start of a year", "a change of season"], "For example, 252 and 66 million years ago."),
    ("Which era is called the Age of Reptiles (dinosaurs)?", "Mesozoic", ["Paleozoic", "Cenozoic", "Precambrian"], "252 to 66 million years ago."),
    ("In which era do we live?", "Cenozoic", ["Mesozoic", "Paleozoic", "Precambrian"], "The last 66 million years."),
    ("What part of Earth's history is the Precambrian?", "about the first 88% of Earth's history", ["the last few thousand years", "only the age of dinosaurs", "about 10%"], "4,600 to 541 million years ago."),
    ("What is an index fossil?", "a fossil of a species that lived for a short time over a wide area, used to date layers", ["any fossil", "a fossil found only once", "a fossil in an index book"], "It matches layers in different places."),
    ("What is relative dating?", "putting rocks and events in order from oldest to youngest without exact ages", ["giving an exact age in years", "measuring rock weight", "counting tree rings"], "Superposition is one rule."),
])
B5 = bank([
    ("Ava says humans have been around for most of Earth's history. How should you respond?", "Modern humans appeared about 300,000 years ago, a tiny fraction of 4.6 billion years.", ["She is right.", "Humans appeared 4 billion years ago.", "Humans and Earth formed together."],
     "Humans are very recent."),
    ("Leo sees a dark layer full of iridium in rocks 66 million years old around the world. What does this evidence support?", "an asteroid impact at the end of the Mesozoic", ["a very cold winter", "the first plants", "the start of the Precambrian"],
     "The impact layer marks the boundary."),
    ("Mia finds that the eras are not equal lengths. Why?", "Era boundaries are based on major changes in life, not on equal amounts of time.", ["Scientists made a mistake.", "Each era is exactly 100 million years.", "Eras are based on seasons."],
     "Events define boundaries."),
    ("A rock layer has fossils of both trilobites and the first land plants. About when did it form?", "in the Paleozoic Era", ["in the Cenozoic Era", "in the Mesozoic Era", "last century"], "Both lived in the Paleozoic."),
    ("Why do scientists use both relative and absolute dating?", "Relative dating orders events; radiometric dating gives ages in years.", ["Only one is ever needed.", "They measure the same thing.", "Absolute dating is a guess."],
     "Together they build the time scale."),
])


def body():
    think = ("<p>Earth is about <b>4.6 billion years</b> old. The <b>geologic time scale</b> organizes this history using evidence from <b>rock layers</b> and <b>fossils</b>.</p>"
             "<ul><li><b>Precambrian</b> (4,600–541 million years ago): early life, mostly single-celled. <b>Paleozoic</b> (541–252): shells, fish, land plants. "
             "<b>Mesozoic</b> (252–66): dinosaurs. <b>Cenozoic</b> (66–now): mammals and humans.</li>"
             "<li>Era boundaries are marked by <b>mass extinctions</b>, so eras are not equal in length.</li>"
             "<li><b>Relative dating</b> orders events (lower layers are older; a feature that cuts layers is younger). <b>Radiometric dating</b> uses <b>half-lives</b> to give ages in years.</li></ul>")
    ex = [("Dinosaurs died out 66 million years ago. Which era ended?", ["66 = Mesozoic/Cenozoic boundary."], "the Mesozoic"),
          ("2 half-lives have passed. Fraction left?", ["½ × ½"], "1/4")]
    mist = ["Thinking humans appeared early in Earth's history.",
            "Thinking an intrusion is older than the rock it cuts.",
            "Thinking all eras are the same length."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Earth's long history", B1 + [(g_order, 12)]),
        ("Eras and events", [(g_era, 13), (g_order, 7)]),
        ("Reading rock layers", [(g_rel, 6), (g_half, 8), (g_order, 6)]),
        ("Time on a human scale", [(g_clock, 14), (g_half, 4), (g_era, 2)]),
        ("Explaining with evidence", B5 + [g_clock, g_order, g_half]),
    ])
    make("grade-8", "geologic-time-scale", 21, "MS-ESS1-4",
         "Construct a scientific explanation based on evidence from rock strata for how the geologic time scale is used to organize Earth's 4.6-billion-year-old history.",
         "The Geologic Time Scale",
         "Grade 8 Geologic Time Scale Worksheets: Eras, Relative Dating and Half-Lives",
         "Geologic Time Scale",
         "Free middle school science worksheets on the geologic time scale (NGSS MS-ESS1-4): Earth's 4.6-billion-year history, eras and mass extinctions, relative dating from rock layers, half-lives and scaling time to a clock. 100 practice questions with answers.",
         "Earth's 4.6-billion-year history is read from rock layers.",
         "Eras are marked by big changes in fossils. Relative dating orders events; half-lives give ages in years.",
         body(),
         [("How is the geologic time scale organized?", "Into eons, eras, periods and epochs, with boundaries at major changes in the fossil record such as mass extinctions."),
          ("How do scientists know the order of rock layers?", "In undisturbed rock, lower layers are older; features that cut across layers are younger; index fossils match layers from different places."),
          ("How long have humans been around compared with Earth?", "Modern humans appeared about 300,000 years ago, less than 0.01% of Earth's 4.6-billion-year history.")],
         sets)


if __name__ == "__main__":
    main()
