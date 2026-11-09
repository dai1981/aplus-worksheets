# -*- coding: utf-8 -*-
"""
Pinterest bulk-upload CSV files for worksheet units (Pinterest > Create > Bulk create Pins).
  python3 tools/make_pinterest_csv.py us math grade-1,grade-2,grade-3,grade-4,grade-5,grade-6,grade-7 2026-11-10 OUT_DIR
Columns: Title, Media URL, Pinterest board, Thumbnail, Description, Link, Publish date, Keywords
Rules from Pinterest: at most 100 rows per file, titles unique and <= 100 characters,
descriptions <= 500 characters, publish dates at most 14 days ahead.
Board names must match boards that already exist, e.g. "Grade 7 Math Worksheets".
Pins are spread over the days (PER_DAY a day) and grades are mixed so each day covers several grades.
"""
import csv, json, os, re, sys, datetime

BASE = "https://www.apu2.com/worksheets"
HERE = os.path.dirname(os.path.abspath(__file__))
PER_DAY = 10
HOURS = [8, 9, 11, 12, 14, 16, 17, 19, 20, 21]


def grade_name(g):
    return g.replace("grade-", "Grade ").replace("year-", "Year ").replace("primary-", "Primary ")


def main():
    country, subject, grades, start, out = sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4], sys.argv[5]
    per_grade = []
    for g in grades:
        d = os.path.join(HERE, "..", "content", country, subject, g)
        units = [json.load(open(os.path.join(d, f), encoding="utf-8")) for f in os.listdir(d) if f.endswith(".json")]
        units.sort(key=lambda u: (u["sort"], u["slug"]))
        per_grade.append(units)
    order = []                                  # round robin over the grades
    while any(per_grade):
        for lst in per_grade:
            if lst:
                order.append(lst.pop(0))
    day0 = datetime.date.fromisoformat(start)
    rows = []
    for i, u in enumerate(order):
        gn = grade_name(u["grade"])
        subj = "Math" if subject == "math" else "Maths"
        name = u["title"] if len(u["title"]) <= 55 else u["short_title"]
        name = re.sub(r"^(Grade|Year|Primary) \d+:? ", "", name)
        title = "%s Worksheet: %s %s (Free, Answer Key)" % (name, gn, subj)
        if len(title) > 100:
            title = "%s Worksheet: %s %s" % (name, gn, subj)
        title = title[:100]
        desc = ("%s Free printable %s %s worksheet with a short lesson, 100 practice questions and an answer key."
                % (u["key_big"], gn, u["short_title"].lower()))
        if len(desc) > 500:
            desc = desc[:497] + "..."
        link = "%s/%s/%s/%s/%s/" % (BASE, country, subject, u["grade"], u["slug"])
        day = day0 + datetime.timedelta(days=i // PER_DAY)
        when = datetime.datetime.combine(day, datetime.time(HOURS[i % PER_DAY], 0)).strftime("%Y-%m-%dT%H:%M:%S")
        kw = ", ".join([u["short_title"].lower(), "%s %s worksheets" % (gn.lower(), subj.lower()),
                        "free printable %s worksheets" % subj.lower(), u["standard_code"]])
        rows.append([title, link + "pin.png", "%s %s Worksheets" % (gn, subj), "", desc, link, when, kw])
    titles = [r[0] for r in rows]
    assert len(titles) == len(set(titles)), "duplicate titles"
    last = (day0 + datetime.timedelta(days=(len(rows) - 1) // PER_DAY))
    assert (last - day0).days <= 13, "publish dates go past 14 days: lower the number of grades or raise PER_DAY"
    os.makedirs(out, exist_ok=True)
    head = ["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]
    for k in range(0, len(rows), 100):
        path = os.path.join(out, "pinterest_%s_%s_%d.csv" % (country, subject, k // 100 + 1))
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, quoting=csv.QUOTE_ALL)
            w.writerow(head)
            w.writerows(rows[k:k + 100])
        print("wrote", path, len(rows[k:k + 100]), "pins")
    print("days:", day0, "to", last)


if __name__ == "__main__":
    main()
