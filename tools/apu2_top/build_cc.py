# -*- coding: utf-8 -*-
"""英語圏の国別トップ（/us/ /uk/ /au/ /ca/ /sg/）：その国の全教科を学年の一覧で。
もとのページ（cc_src/）の head・header・footer はそのまま、中身だけ作り直す → out/{国}/index.html"""
import os, re, json, html
import cards

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.apu2.com"
ICO_M = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 7h3M9.5 5.5v3M13 7h3M8 12.5l3 3M11 12.5l-3 3M13 14h3"/></svg>'
ICO_S = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 2h6M10 2v6.5L4.5 18.5A2 2 0 0 0 6.3 21.5h11.4a2 2 0 0 0 1.8-3L14 8.5V2"/><path d="M7 15h10"/></svg>'
FREE = ("A short lesson with worked examples and common mistakes, 100 practice questions in 5 sets from easy to hard, "
        "instant answers with explanations, and a 4-page printable PDF with an answer key.")

# 国ごと：教科（id, 見出し, 説明, [(サブ見出し, 国コード, 教科, 基準)]）
C = {
 "us": dict(
  title="Free Math and Science Worksheets, Kindergarten to High School (Common Core, NGSS) | aplus",
  desc="Free math and science worksheets from Kindergarten to high school, matched to Common Core, TEKS and NGSS: Algebra 1, Geometry, Algebra 2, Precalculus, Biology, Chemistry and Physics. Each topic has a short lesson, 100 questions with answers and a printable PDF. No sign-up.",
  h1="Free math and science worksheets<br><em>for every grade.</em>",
  hp="Matched to Common Core, TEKS and NGSS. A short lesson, 100 practice questions and a printable PDF for every topic.",
  locale="en-US", subj=[
   ("math", "Math worksheets by grade", "Pick a grade, then a topic. Read the lesson, practice online and print the worksheet.",
    [("Common Core", "us", "math", "Common Core State Standards"), ("Texas", "us-tx", "math", "TEKS")]),
   ("science", "Science worksheets by grade", "Short lessons with diagrams, 100 practice questions and a printable worksheet for every topic.",
    [("NGSS", "us", "science", "Next Generation Science Standards")])],
  faq=[("Are these worksheets free?", "Yes. Every lesson, quiz and printable PDF is free. No sign-up or email is needed."),
       ("Which standards do they follow?", "Math follows the Common Core State Standards, with a separate set for Texas (TEKS). Science follows the Next Generation Science Standards (NGSS). The standard is shown on every topic page."),
       ("Do you have high school courses?", "Yes. Math has Algebra 1, Geometry, Algebra 2 and Precalculus. Science has Biology, Chemistry, Physics and Earth and Space Science."),
       ("What does each topic include?", FREE),
       ("Which grade should my child start with?", "Start with your child's current grade. If it feels hard, go back one grade for a quick review."),
       ("Can teachers use them in class?", "Yes. You can print and copy the worksheets for home and classroom use.")]),
 "uk": dict(
  title="Free Maths and Science Worksheets, Year 1 to Year 13 (National Curriculum, GCSE, A Level) | aplus",
  desc="Free maths and science worksheets for Year 1 to Year 13, matched to the National Curriculum in England, with KS2 SATs, GCSE and A level practice. Each topic has a short lesson, 100 questions with answers and a printable A4 PDF. No sign-up.",
  h1="Free maths and science worksheets<br><em>for every year.</em>",
  hp="Matched to the National Curriculum, GCSE and A level. A short lesson, 100 practice questions and a printable A4 PDF for every topic.",
  locale="en-GB", subj=[
   ("maths", "Maths worksheets by year", "Pick a year, then a topic. Read the lesson, practise online and print the worksheet.",
    [("", "uk", "maths", "National Curriculum, GCSE and A level")]),
   ("science", "Science worksheets by year", "Short lessons with diagrams, 100 practice questions and a printable worksheet for every topic.",
    [("", "uk", "science", "National Curriculum, GCSE and A level")])],
  faq=[("Are these worksheets free?", "Yes. Every lesson, quiz and printable PDF is free. No sign-up or email is needed."),
       ("Do they match the National Curriculum in England?", "Yes. Years 1–9 follow the National Curriculum, Years 10–11 the GCSE subject content and Years 12–13 the A level subject content."),
       ("Do they help with SATs, GCSE and A level?", "Yes. Year 6 covers the KS2 SATs skills, Years 10–11 cover GCSE Maths and Combined Science, and Years 12–13 cover A level Maths, Biology, Chemistry and Physics."),
       ("What does each topic include?", FREE),
       ("Which year should my child start with?", "Start with your child's current year. If it feels hard, go back one year for a quick review."),
       ("Can teachers use them in class?", "Yes. You can print and copy the worksheets for home and classroom use.")]),
 "au": dict(
  title="Free Maths and Science Worksheets, Foundation to Year 12 (Australian Curriculum) | aplus",
  desc="Free maths and science worksheets matched to the Australian Curriculum v9.0: maths from Foundation to Year 8 and science from Foundation to Year 12, with NAPLAN practice. Each topic has a short lesson, 100 questions with answers and a printable A4 PDF. No sign-up.",
  h1="Free maths and science worksheets<br><em>for every year.</em>",
  hp="Matched to the Australian Curriculum v9.0. A short lesson, 100 practice questions and a printable A4 PDF for every topic.",
  locale="en-AU", subj=[
   ("maths", "Maths worksheets by year", "Pick a year, then a topic. Read the lesson, practise online and print the worksheet.",
    [("", "au", "maths", "Australian Curriculum v9.0")]),
   ("science", "Science worksheets by year", "Short lessons with diagrams, 100 practice questions and a printable worksheet for every topic.",
    [("", "au", "science", "Australian Curriculum v9.0")])],
  faq=[("Are these worksheets free?", "Yes. Every lesson, quiz and printable PDF is free. No sign-up or email is needed."),
       ("Do they match the Australian Curriculum?", "Yes. Each topic follows one part of the Australian Curriculum v9.0, and the content description code is shown on the page. Years 11–12 science follows the senior secondary Biology, Chemistry, Physics and Earth and Environmental Science."),
       ("Do they help with NAPLAN?", "Yes. Year 3 and Year 5 are NAPLAN years, and every maths topic ends with word problems like the ones in the numeracy test."),
       ("What does each topic include?", FREE),
       ("Which year should my child start with?", "Start with your child's current year. If it feels hard, go back one year for a quick review."),
       ("Can teachers use them in class?", "Yes. You can print and copy the worksheets for home and classroom use.")]),
 "ca": dict(
  title="Free Math and Science Worksheets for Canada: Ontario and BC, Kindergarten to Grade 12 | aplus",
  desc="Free math and science worksheets matched to the Ontario and British Columbia curricula, from Kindergarten to Grade 12. Each topic has a short lesson, 100 questions with answers and a printable PDF. No sign-up.",
  h1="Free math and science worksheets<br><em>for your province and grade.</em>",
  hp="Matched to the Ontario and BC curricula. A short lesson, 100 practice questions and a printable PDF for every topic.",
  locale="en-CA", subj=[
   ("math", "Math worksheets by grade", "Pick your province and grade, then a topic. Read the lesson, practise online and print the worksheet.",
    [("Ontario", "ca-on", "math", "Ontario Curriculum"), ("British Columbia", "ca-bc", "math", "BC Curriculum")]),
   ("science", "Science worksheets by grade", "Short lessons with diagrams, 100 practice questions and a printable worksheet for every topic.",
    [("Ontario", "ca-on", "science", "Ontario Curriculum"), ("British Columbia", "ca-bc", "science", "BC Curriculum")])],
  faq=[("Are these worksheets free?", "Yes. Every lesson, quiz and printable PDF is free. No sign-up or email is needed."),
       ("Do they match the Ontario and BC curricula?", "Yes. Ontario topics follow the Ontario Curriculum, and BC topics follow BC's Curriculum. The expectation or learning standard is shown on each page."),
       ("My province is not Ontario or BC. Can I still use them?", "Yes. Most topics are taught in the same grade across Canada. Pick the grade your child is in, or the topic name you need."),
       ("What does each topic include?", FREE),
       ("Which grade should my child start with?", "Start with your child's current grade. If it feels hard, go back one grade for a quick review."),
       ("Can teachers use them in class?", "Yes. You can print and copy the worksheets for home and classroom use.")]),
 "sg": dict(
  title="Free Maths and Science Worksheets, Primary 1 to Secondary 4 (MOE Syllabus, PSLE, O-Level) | aplus",
  desc="Free maths and science worksheets for Primary 1 to Secondary 4, matched to the Singapore MOE syllabus, with PSLE and O-Level practice. Each topic has a short lesson, 100 questions with answers and a printable PDF. No sign-up.",
  h1="Free maths and science worksheets<br><em>for your level.</em>",
  hp="Matched to the MOE syllabus. A short lesson, 100 practice questions and a printable PDF for every topic.",
  locale="en-SG", subj=[
   ("maths", "Maths worksheets by level", "Pick a level, then a topic. Read the lesson, practise online and print the worksheet.",
    [("", "sg", "maths", "MOE syllabus")]),
   ("science", "Science worksheets by level", "Short lessons with diagrams, 100 practice questions and a printable worksheet for every topic.",
    [("", "sg", "science", "MOE syllabus")])],
  faq=[("Are these worksheets free?", "Yes. Every lesson, quiz and printable PDF is free. No sign-up or email is needed."),
       ("Do they match the MOE syllabus?", "Yes. Maths follows the MOE primary and O-Level mathematics syllabuses, and science follows the primary science, lower secondary science and O-Level Physics, Chemistry and Biology syllabuses."),
       ("Do they help with PSLE and O-Level?", "Yes. Primary 5 and 6 cover the skills tested in the PSLE, and Secondary 3 and 4 cover the O-Level syllabuses. Every topic ends with word problems."),
       ("What does each topic include?", FREE),
       ("Which level should my child start with?", "Start with your child's current level. If it feels hard, go back one level for a quick review."),
       ("Can teachers use them in class?", "Yes. You can print and copy the worksheets for home and classroom use.")]),
}
NAME = {"math": "Math", "maths": "Maths", "science": "Science"}


def build(c):
    d = C[c]
    s = open(os.path.join(HERE, "cc_src", c + ".html"), encoding="utf-8").read()
    e = html.escape
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % e(d["title"], False), s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(d["desc"]), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e(d["title"]), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(d["desc"]), s, count=1)
    # 本文
    secs, items, picks = "", [], ""
    for sid, h2, lead, parts in d["subj"]:
        body, tot, rng = "", 0, []
        for sub, cc, subj, std in parts:
            n = cards.count(cc, subj)
            tot += n
            rng.append(cards.span(cc, subj))
            if sub or len(parts) > 1:
                body += '<h3 class="gsub">%s<small>%s · %d topics · %s</small></h3>' % (sub, cards.span(cc, subj), n, std)
            body += cards.gcards(cc, subj, "en")
            for slug, name, us in cards.grades(cc, subj):
                items.append(("%s%s %s worksheets" % (sub + " " if sub and len(parts) > 1 else "", name, NAME[subj].lower()),
                              "%s/worksheets/%s/%s/%s/" % (SITE, cc, subj, slug)))
        std0 = parts[0][3] if len(parts) == 1 else " and ".join(p[0] for p in parts)
        secs += ('<section class="lang" id="%s"><div class="card">\n  <div class="head"><div class="ico" aria-hidden="true">%s</div><h2>%s<small>%d topics · %s</small></h2></div>\n'
                 '  <p class="lead">%s</p>%s\n</div></section>\n' % (sid, ICO_S if sid == "science" else ICO_M, h2, tot, std0, lead, body))
        picks += '<a href="#%s"><small>%s</small><b>%s</b><span>%s</span></a>' % (sid, "%d topics" % tot, NAME[sid if sid in NAME else "math"], " · ".join(rng) if len(rng) == 1 else ", ".join(p[0] for p in parts))
    hero = ('<div class="hero"><div class="wrap">\n  <h1>%s</h1>\n  <p>%s</p>\n  <div class="pick">%s</div>\n</div></div>\n'
            % (d["h1"], d["hp"], picks))
    s = re.sub(r'<div class="hero">.*?</div></div>\n', lambda m: hero, s, count=1, flags=re.S)
    i, j = s.index('<main class="wrap">') + len('<main class="wrap">\n'), s.index('  <div class="feats">')
    s = s[:i] + secs + s[j:]
    faq = '<section class="faq"><h2>FAQ</h2>%s</section>' % "".join("<details><summary>%s</summary><p>%s</p></details>" % qa for qa in d["faq"])
    s = re.sub(r'<section class="faq">.*?</section>', lambda m: faq, s, count=1, flags=re.S)
    # ほかの国へのリンクは出さない（日本語辞書だけ）
    s = re.sub(r'(<section class="oth"><h2>[^<]*</h2><div class="also">)(<a class="choice" href="/japanese/en/word/">.*?</a>).*?(</div></section>)',
               lambda m: m.group(1) + m.group(2) + m.group(3), s, count=1, flags=re.S)
    s = s.replace("More grades and topics are added every month.", "New topics are added every month.")
    # 構造化データ
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    ld = json.loads(m.group(1))
    for g in ld["@graph"]:
        if g["@type"] == "CollectionPage":
            g["name"], g["description"] = d["title"], d["desc"]
            g["about"] = ["Mathematics", "Science"]
            g.pop("educationalAlignment", None)
        if g["@type"] == "ItemList":
            g["name"] = "Worksheets by grade"
            g["itemListElement"] = [{"@type": "ListItem", "position": k + 1, "name": a, "url": b} for k, (a, b) in enumerate(items)]
        if g["@type"] == "FAQPage":
            g["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]
    s = s[:m.start(1)] + json.dumps(ld, ensure_ascii=False) + s[m.end(1):]
    s = s.replace("</head>", cards.CSS_G + "\n</head>", 1)
    # フッターに理科
    sci = [p for x in d["subj"] if x[0] == "science" for p in x[3]]
    if sci and "Science worksheets</a>" not in s:
        s = re.sub(r'(<nav><a href="/worksheets/[^"]*">[^<]*</a>)', lambda m: m.group(1) + '<a href="/worksheets/%s/science/">Science worksheets</a>' % sci[0][1], s, count=1)
    return s


if __name__ == "__main__":
    for c in C:
        os.makedirs(os.path.join(HERE, "out", c), exist_ok=True)
        open(os.path.join(HERE, "out", c, "index.html"), "w", encoding="utf-8").write(build(c))
    print("ok")


# ------------------------------------------------------------------ About（国別）
AB = {  # (もとの基準の言い方, 新しい言い方)
 "us": [("the Common Core State Standards", "Common Core, TEKS (Texas) and the NGSS")],
 "uk": [("the National Curriculum in England", "the National Curriculum in England, GCSE and A level")],
 "au": [],
 "ca": [],
 "sg": [("the Singapore MOE primary mathematics syllabus", "the Singapore MOE syllabus"), ("the MOE primary mathematics syllabus", "the MOE syllabus")],
}


def build_about(c):
    d = C[c]
    s = open(os.path.join(HERE, "cc_src", c + "_about.html"), encoding="utf-8").read()
    i, j = s.index("<main"), s.index("</main>")
    head, body, tail = s[:i], s[i:j], s[j:]
    def fix(t):
        t = re.sub(r"\b(Free |free )(maths?) (worksheets|practice)", lambda m: "%s%s and science %s" % m.groups(), t)
        for a, b in AB[c]:
            t = t.replace(a, b)
        return t
    head = re.sub(r"<title>.*?</title>", lambda m: fix(m.group(0)), head, count=1)
    head = re.sub(r'content="[^"]*"', lambda m: fix(m.group(0)), head)
    head = re.sub(r'"(name|description)": "[^"]*"', lambda m: fix(m.group(0)), head)
    body = re.sub(r"<h1>.*?</p>", lambda m: fix(m.group(0)), body, count=1, flags=re.S)
    tot = sum(cards.count(cc, subj) for _, _, _, parts in d["subj"] for _, cc, subj, _ in parts)
    body = re.sub(r'<div class="s3"><b>[^<]*</b><span>(Maths?) topics', lambda m: '<div class="s3"><b>%s</b><span>%s and science topics' % ("{:,}".format(tot), m.group(1)), body, count=1)
    lists = ""
    for sid, h2, lead, parts in d["subj"]:
        for sub, cc, subj, std in parts:
            lists += "<h3>%s%s</h3><ul>" % (NAME[subj], " · " + sub if sub and len(parts) > 1 else "")
            for slug, name, us in cards.grades(cc, subj):
                lists += '<li><a href="/worksheets/%s/%s/%s/">%s</a>: %d topics, including %s.</li>' % (cc, subj, slug, html.escape(name), len(us), html.escape(", ".join(us[:3])))
            lists += "</ul>"
    body = re.sub(r"(<h2>(?:Grades|Years|Levels) and topics</h2>)(?:<h3>[^<]*</h3>)?<ul>.*</ul>(?=<p>)", lambda m: m.group(1) + lists, body, count=1, flags=re.S)
    body = body.replace("Choose a grade &rsaquo;", "Choose a subject and grade &rsaquo;").replace("Choose a year &rsaquo;", "Choose a subject and year &rsaquo;").replace("Choose a level &rsaquo;", "Choose a subject and level &rsaquo;")
    body = body.replace("Every topic ends with word problems", ("Every maths topic" if C[c]["subj"][0][0] == "maths" else "Every math topic") + " ends with word problems")
    css = "<style>.ab h3{font-size:16px;color:var(--green-d);margin:18px 0 6px}</style>\n"
    return head.replace("</head>", css + "</head>", 1) + body + tail


for _c in C:
    open(os.path.join(HERE, "out", _c, "about.html"), "w", encoding="utf-8").write(build_about(_c))
