# -*- coding: utf-8 -*-
"""各国・各言語のトップに出す「教科 → 学年」の一覧（content/catalog.json と単元 JSON から作る）"""
import json, os, glob, html

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CAT = json.load(open(os.path.join(ROOT, "content", "catalog.json"), encoding="utf-8"))

CSS_G = ("<style>.grades{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}"
         ".gcard{display:flex;flex-direction:column;gap:4px;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;transition:border-color .15s,box-shadow .15s}"
         ".gcard:hover{border-color:var(--green);box-shadow:0 6px 16px rgba(0,102,51,.12)}"
         ".gcard h3{margin:0;font-size:17px;color:var(--green-d);display:flex;align-items:baseline;justify-content:space-between;gap:8px}"
         ".gcard h3 span{font-size:12px;font-weight:700;color:var(--green);white-space:nowrap}"
         ".gcard p{margin:0;font-size:13px;color:var(--sub);line-height:1.5}"
         ".gsub{font-size:15px;color:var(--green-d);margin:20px 0 8px;font-weight:800}.gsub:first-of-type{margin-top:6px}"
         ".gsub small{font-weight:600;color:var(--sub);font-size:13px;margin-left:6px}"
         ".sgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin-top:4px}"
         ".scard{display:flex;flex-direction:column;gap:2px;padding:14px 14px;border:1px solid var(--line);border-radius:14px;background:#fff}"
         ".scard:hover{border-color:var(--green);box-shadow:0 6px 16px rgba(0,102,51,.12)}"
         ".scard b{font-size:18px;color:var(--green-d)}.scard span{font-size:12.5px;color:var(--sub)}</style>")

TOPICS = {"en": "{n} topics", "ja": "{n}単元", "vi": "{n} chủ đề", "id": "{n} topik", "zh": "{n} 个单元", "tw": "{n} 個單元",
          "ko": "{n}개 단원", "de": "{n} Themen", "fr": "{n} thèmes", "it": "{n} argomenti", "es": "{n} temas",
          "pt": "{n} temas", "tr": "{n} konu", "sv": "{n} områden"}


def subjects(cc):
    return sorted([s for s in CAT["subjects"] if s["country"] == cc], key=lambda s: s["sort"])


def grades(cc, subj):
    gs = sorted([g for g in CAT["grades"] if g["country"] == cc and g["subject"] == subj], key=lambda g: g["sort"])
    out = []
    for g in gs:
        us = []
        for f in glob.glob(os.path.join(ROOT, "content", cc, subj, g["slug"], "*.json")):
            d = json.load(open(f, encoding="utf-8"))
            t = d.get("short_title") or d.get("title")
            us.append((d.get("sort", 0), t[:1].upper() + t[1:]))
        if us:
            us.sort()
            out.append((g["slug"], g["name"], [u[1] for u in us]))
    return out


def count(cc, subj):
    return sum(len(x[2]) for x in grades(cc, subj))


def gcards(cc, subj, L, label=None, sep=", "):
    r = ""
    for slug, name, us in grades(cc, subj):
        sample = sep.join(html.escape(u) for u in us[:3]) + (" …" if len(us) > 3 else "")
        r += ('<a class="gcard" href="/worksheets/%s/%s/%s/"><h3>%s<span>%s</span></h3><p>%s</p></a>'
              % (cc, subj, slug, html.escape(label(name) if label else name), TOPICS[L].replace("{n}", str(len(us))), sample))
    return '<div class="grades">%s</div>' % r


def span(cc, subj, dash="–"):
    g = grades(cc, subj)
    return "%s %s %s" % (g[0][1], dash, g[-1][1]) if len(g) > 1 else g[0][1]
