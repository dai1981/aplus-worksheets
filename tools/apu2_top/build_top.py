# -*- coding: utf-8 -*-
"""apu2.com の トップ（index.html）と About（about.html）を 英語と 6 言語で 作る → out/"""
import json, os, re, html
from top_data import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SRC_I = open(os.path.join(HERE, "en_index.html"), encoding="utf-8").read()
SRC_A = open(os.path.join(HERE, "en_about.html"), encoding="utf-8").read()
LINE = "https://line.me/ti/g2/bNMNEcyFfTX1-QEg9Jv48UjSb-_U2iFtuk_90g?utm_source=invitation&amp;utm_medium=link_copy&amp;utm_campaign=default"
DISCORD = "https://discord.gg/6sNvy7xpDw"
SITE = "https://www.apu2.com"

# 英語の ページから そのまま 使う 部分
CSS_I = re.search(r"<style>.*?</style>\s*<style id=\"ts-css\">.*?</style>", SRC_I, re.S).group(0)
TS_JS = re.search(r"<script id=\"ts-js\">.*?</script>", SRC_I, re.S).group(0)
CSS_A = re.search(r"<style>.*?</style>", SRC_A, re.S).group(0)
LOGO = re.search(r"<a class=\"brand\".*?</a>", SRC_I, re.S).group(0)
ICO = dict(re.findall(r"<section class=\"lang\" id=\"(\w+)\">.*?<div class=\"ico\" aria-hidden=\"true\">(<svg.*?</svg>)", SRC_I, re.S))
FEAT_SVG = re.findall(r"<div class=\"feat\">(<svg.*?</svg>)", SRC_I, re.S)
DC_SVG = re.search(r"<a class=\"btn-dc\"[^>]*>(<svg.*?</svg>)", SRC_I, re.S).group(1)
LN_SVG = re.search(r"<a class=\"btn-line\"[^>]*>(<svg.*?</svg>)", SRC_I, re.S).group(1)
ARR = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
assert len(FEAT_SVG) == 4 and set(ICO) == {"japanese", "english", "maths"}
CSS_X = "<style>.mh{font-size:13.5px;color:var(--sub);margin:16px 0 8px;font-weight:800}.mh:first-of-type{margin-top:4px}</style>"
MATH_D = {m[0]: m for m in MATH}


def fr_fix(s):
    """フランス語の : ; ? ! の 前は ノーブレークスペース"""
    return re.sub(r" ([:;?!])", " \\1", s)


def tx(L, d):
    out = {}
    for k, v in d.items():
        if isinstance(v, str):
            v = v.replace("{jw}", n(JW, L)).replace("{ew}", n(EW, L)).replace("{line}", LINE)
            v = v.replace("{nk}", str(NK)).replace("{nc}", str(NC)).replace("{nk1}", str(NK - 1)).replace("{nk2}", str(NK - 2))
            out[k] = fr_fix(v) if L == "fr" else v
        else:
            out[k] = json.loads(json.dumps(v)) if not isinstance(v, (list, tuple)) else tx_list(L, v)
    return out


def tx_list(L, v):
    r = []
    for x in v:
        if isinstance(x, (list, tuple)):
            r.append(tuple(tx(L, {"a": y})["a"] if isinstance(y, str) else y for y in x))
        else:
            r.append(tx(L, {"a": x})["a"])
    return r


def pre(L):
    return "/" if L == "en" else "/%s/" % L


def head(L, title, desc, path, ld, css, extra=""):
    canon = SITE + pre(L) + path
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s%s%s">\n' % (HREFLANG[k], SITE, pre(k), path) for k in LANGS)
    alts += '<link rel="alternate" hreflang="x-default" href="%s/%s">\n' % (SITE, path)
    e = html.escape
    return ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n<meta charset="UTF-8">\n' % HREFLANG[L] + extra +
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<link rel="canonical" href="%s">\n' % (e(title, False), e(desc), canon) + alts +
            '<meta property="og:type" content="website">\n<meta property="og:url" content="%s">\n<meta property="og:title" content="%s">\n'
            '<meta property="og:description" content="%s">\n<meta property="og:site_name" content="aplus">\n<meta property="og:locale" content="%s">\n'
            '<meta property="og:image" content="https://www.apu2.com/logo.svg">\n'
            '<meta name="google-adsense-account" content="ca-pub-3234684892462480">\n<link rel="icon" type="image/svg+xml" href="/logo.svg">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;800&family=Noto+Sans+JP:wght@500;700&display=swap" rel="stylesheet">\n'
            '<script async src="https://www.googletagmanager.com/gtag/js?id=G-JXYPVC45WC"></script>\n'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-JXYPVC45WC');</script>\n"
            % (canon, e(title), e(desc), LOCALE[L]) +
            '<script type="application/ld+json">%s</script>\n' % json.dumps(ld, ensure_ascii=False) + css + "\n</head>\n")


def header(L, page, t):
    opts = ""
    for k, lab in SEL:
        v = ("/" if k == "en" else "/%s/" % k) + ("" if page == "index.html" else page)
        opts += '<option value="%s" data-l="%s"%s>%s</option>' % (v, k, " selected" if k == L else "", lab)
    sel = ('<select id="langSel" aria-label="%s" onchange="try{localStorage.setItem(\'aplus_lang\',this.options[this.selectedIndex].getAttribute(\'data-l\'))}catch(e){}location.href=this.value">%s</select>'
           % (t["lang"], opts))
    return ('<body>\n<header class="top">\n  <div class="wrap">\n    %s\n    <span class="tr">%s<a class="small" href="%sabout.html">%s</a></span>\n  </div>\n</header>\n'
            % (LOGO, sel, pre(L), t["about"]))


def footer(L, t, games):
    nav = '<a href="/japanese/">%s</a><a href="/english/">%s</a>' % (t["f_j"], t["f_e"])
    if games:
        nav += '<a href="/game/">%s</a>' % t["f_g"]
    nav += ('<a href="/worksheets/">%s</a><a href="%sabout.html">%s</a><a href="/privacypolicy.html%s">%s</a><a href="/mailform/">%s</a>'
            % (t["f_m"], pre(L), t["f_a"], "" if L == "en" else "?lang=" + L, t["f_p"], t["f_c"]))
    langs = "".join('<a href="%s%s" lang="%s">%s</a>' % (pre(k), "" if games is False else "about.html", HREFLANG[k], lab)
                    for k, lab in SEL if k in LANGS and k != L)
    return ('<footer>\n  <div class="wrap">\n    <div>&copy; Aplus Inc.</div>\n    <nav>%s</nav>\n    <div class="langs">%s</div>\n  </div>\n</footer>\n'
            % (nav, langs))


def choice(href, b, s, lang=None, c=None, r=None):
    a = ' lang="%s"' % lang if lang else ""
    a += ' data-c="%s"' % c if c else ""
    a += ' data-r="%s"' % html.escape(r) if r else ""
    sl = ""
    return '<a class="choice" href="%s"%s><div><b>%s</b><span>%s</span></div>%s</a>' % (href, a, b, s, ARR)


def math_href(L, c):
    if L == "en" and c in ("us", "uk", "au"):
        return "/%s/" % c
    return MATH_D[c][1]


def math_cards(L, codes):
    r = ""
    for c in codes:
        m = MATH_D[c]
        la = "" if m[2] == L or (L == "en" and m[2] == "en") else ' lang="%s"' % m[2]
        r += '<a class="choice" href="%s" data-c="%s"%s><div><b>%s</b><span%s>%s</span></div>%s</a>' % (
            math_href(L, c), c, ' data-r="%s"' % SHORT[c] if L == "en" and c in SHORT else "", CC[L][c], la, m[3], ARR)
    return r


def others(L):
    own = OWN[L]
    return [m[0] for m in MATH if m[0] not in own]


FOR_YOU = """<script>
/* その人の 国の 算数を 先に（ブラウザの ことばの 地域 en-US・de-CH など で えらぶ） */
(function(){try{
  var R={us:'us',gb:'uk',uk:'uk',au:'au',ca:'ca-on',sg:'sg','in':'in',za:'za',ph:'ph',de:'de',at:'de',ch:'ch',fr:'fr',be:'fr',it:'it',es:'es',mx:'mx',br:'br',kr:'kr',cn:'cn',tw:'tw',id:'id',tr:'tr',se:'se',ng:'ng'};
  var L=(navigator.languages||[navigator.language||'']).map(function(x){return String(x).toLowerCase()});
  var c=null;for(var i=0;i<L.length&&!c;i++){var m=/^[a-z]{2,3}-([a-z]{2})(?:-|$)/.exec(L[i]);if(m&&R[m[1]])c=R[m[1]];}
  if(!c)return;
  var a=document.querySelector('#maths .choice[data-c="'+c+'"]');if(!a)return;
  a.classList.add('is-mine');var t=document.createElement('span');t.className='tag mine';t.textContent=%(mine)s;a.appendChild(t);
  var box=a.parentNode;box.insertBefore(a,box.firstChild);%(en)s
}catch(e){}})();
</script>"""
FOR_YOU_EN = """
  if(box!==document.querySelector('#maths .choices'))return;
  var sec=document.getElementById('maths'),jp=document.getElementById('japanese');if(sec&&jp)jp.parentNode.insertBefore(sec,jp);
  var p=document.querySelector('#pick a[data-k="ma"]');
  if(p){p.href=a.getAttribute('href');p.classList.add('me');p.querySelector('span').textContent=a.getAttribute('data-r')||'';p.parentNode.insertBefore(p,p.parentNode.firstChild);}"""
REDIRECT = """<script>
/* 初めて来た人は、ブラウザの言語のトップへ。英語を選んだ人・サイト内から来た人はそのまま */
(function(){try{
  var P={sv:'/sv/',ja:'/ja/',vi:'/vi/',id:'/id/',zh:'/zh/',tw:'/tw/',ko:'/ko/',de:'/de/',fr:'/fr/',it:'/it/',es:'/es/',pt:'/pt/',tr:'/tr/',us:'/us/',uk:'/uk/',au:'/au/',ca:'/ca/',sg:'/sg/'},k=null,saved=null;
  try{saved=localStorage.getItem('aplus_lang')}catch(e){}
  if(saved){if(P[saved])k=saved}
  else if(!document.referrer||document.referrer.indexOf(location.host)<0){
    var n=(navigator.languages||[navigator.language||'']).map(function(x){return String(x).toLowerCase()});
    for(var i=0;i<n.length;i++){var a=n[i];if(/^zh-(tw|hk|mo|hant)/.test(a)){k='tw';break}var c=a.slice(0,2);if(c==='in')c='id';if(c==='en'){var r=/^en-(us|gb|au|ca|sg)/.exec(a);if(r)k={us:'us',gb:'uk',au:'au',ca:'ca',sg:'sg'}[r[1]];break}if(P[c]){k=c;break}}
  }
  if(k)location.replace(P[k]+location.search+location.hash);
}catch(e){}})();
</script>
"""


def org():
    return {"@type": "Organization", "@id": SITE + "/#org", "name": "Aplus Inc.", "alternateName": ["えいぷら Aplus", "aplus"],
            "url": SITE + "/", "logo": SITE + "/logo.svg", "sameAs": ["https://www.eigo-duke.com/", "https://www.eigo-duke.com/aplus/"],
            "award": "Japan e-Learning Award 2024, English Education Special Prize"}


def jdict(L):
    if L in ("vi", "zh", "tw", "ko", "id"):
        return "/japanese/%s/word/" % L
    return "/japanese/%s/word/" % L if L in DICT_J else ("/japanese/en/word/" if L in ("it", "tr", "sv") else "/japanese/")


def edict(L):
    if L in ("vi", "zh", "tw", "ko", "id"):
        return "/english/%s/word/" % L
    return "/english/%s/word/" % L if L in DICT_E else "/english/"


def build_index(L):
    t = tx(L, T[L])
    # ---- ld+json
    items = [(t["ld_j"], SITE + ("/japanese/" if L == "en" else jdict(L))), (t["ld_e"], SITE + ("/english/" if L == "en" else edict(L)))]
    mitems = [("%s · %s" % (t["ld_m"], CC[L][c]), SITE + MATH_D[c][1]) for c in OWN[L]]
    items = (mitems + items) if L != "en" else (items + mitems)
    graph = []
    if L == "en":
        graph.append({"@type": "WebSite", "name": "aplus", "url": SITE + "/", "inLanguage": "en", "publisher": {"@id": SITE + "/#org"}})
    graph += [{"@type": "WebPage", "name": t["title"], "url": SITE + pre(L), "inLanguage": L, "description": t["desc"], "publisher": {"@id": SITE + "/#org"}},
              org(),
              {"@type": "ItemList", "name": t["ld_list"], "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": a, "url": b} for i, (a, b) in enumerate(items)]},
              {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}]
    ld = {"@context": "https://schema.org", "@graph": graph}
    extra = '<meta name="p:domain_verify" content="e37548685e3ef4a809ffe9ee5c966e11"/>\n' + REDIRECT if L == "en" else ""
    h = head(L, t["title"], t["desc"], "", ld, CSS_I + "\n" + CSS_X, extra)
    h += header(L, "index.html", t)
    # ---- hero
    h += '\n<div class="hero"><div class="wrap">\n  <h1>%s</h1>\n  <p>%s</p>\n' % (t["h1"], t["hp"])
    if L in DICT_J:
        tabs = ('<button type="button" role="tab" class="on" aria-selected="true" data-d="j" data-v="20261109a" data-ph="%s" data-all="%s">%s<small>%s</small></button>'
                % (html.escape(t["s_jph"]), html.escape(t["s_all"].replace("›", "&rsaquo;")), t["s_j"], t["s_words"].replace("{n}", n(JW, L))))
        if L in DICT_E:
            tabs += ('<button type="button" role="tab" data-d="e" data-v="20261016b" data-ph="%s" data-all="%s">%s<small>%s</small></button>'
                     % (html.escape(t["s_eph"]), html.escape(t["s_all"].replace("›", "&rsaquo;")), t["s_e"], t["s_words"].replace("{n}", n(EW, L))))
        h += ('  <form class="ts" data-lang="%s" data-empty="%s" role="search"><div class="ts-tabs" role="tablist">%s</div><div class="ts-box"><input type="search" name="q" placeholder="%s" aria-label="%s"><button type="submit">%s</button></div><a class="ts-all" href="%s">%s</a></form>\n'
              % (L, html.escape(t["s_empty"]), tabs, html.escape(t["s_jph"]), html.escape(t["s_jph"]), t["s_btn"], jdict(L), t["s_all"].replace("›", "&rsaquo;")))
    pj = '<a href="#japanese" data-k="ja"><small>%s</small><b>%s</b><span>JLPT N5–N1</span></a>' % (t["p_learn"], t["p_j"])
    pe = '<a href="#english" data-k="en"><small>%s</small><b>%s</b><span>IELTS · TOEFL</span></a>' % (t["p_learn"], t["p_e"])
    pm = '<a href="#maths" data-k="ma"><small>%s</small><b>%s</b><span>%s</span></a>' % (t["p_prac"], t["p_m"], t["p_my"])
    order = t.get("order", "jem" if L == "en" else "mje")
    h += '  <div class="pick" id="pick">%s</div>\n</div></div>\n<main class="wrap">\n' % "".join({"j": pj, "e": pe, "m": pm}[k] for k in order)
    # ---- sections
    sj = '<section class="lang" id="japanese"><div class="card">\n  <div class="head"><div class="ico" aria-hidden="true">%s</div><h2>%s</h2></div>\n  <p class="lead">%s</p><div class="choices">' % (ICO["japanese"], t["j_h"], t["j_lead"])
    if L == "en":
        sj += (choice("/japanese/vi/", "Tiếng Việt", "Học tiếng Nhật", "vi") + choice("/japanese/id/", "Bahasa Indonesia", "Belajar bahasa Jepang", "id")
               + choice("/japanese/zh/", "简体中文", "学日语", "zh-Hans") + choice("/japanese/ko/", "한국어", "일본어 공부", "ko"))
    if t.get("j_c"):
        sj += choice("/japanese/%s/" % L, t["j_c"], t["j_c_s"])
    sj += choice(jdict(L) if L != "en" else "/japanese/en/word/", t["j_dict"], t["j_dict_s"]) + choice("/japanese/", t["j_all"], t["j_all_s"]) + "</div>\n</div></section>\n"
    se = '<section class="lang" id="english"><div class="card">\n  <div class="head"><div class="ico" aria-hidden="true">%s</div><h2>%s</h2></div>\n  <p class="lead">%s</p><div class="choices">' % (ICO["english"], t["e_h"], t["e_lead"])
    if L == "en":
        se += (choice("https://www.eigo-duke.com/", "日本語", "英語漬け.com で英語を学ぶ", "ja") + choice("/english/vi/", "Tiếng Việt", "Học tiếng Anh · IELTS, TOEFL", "vi")
               + choice("/english/zh/", "简体中文", "学英语 · IELTS、TOEFL", "zh-Hans") + choice("/english/tw/", "繁體中文", "學英語 · IELTS、TOEFL", "zh-Hant")
               + choice("/english/ko/", "한국어", "영어 공부 · IELTS, TOEFL", "ko"))
    for href, b, sub in t.get("e_more", []):
        se += choice(href, b, sub)
    if t.get("e_c"):
        se += choice("/english/%s/" % L, t["e_c"], t["e_c_s"])
    if t["e_dict"]:
        se += choice(edict(L), t["e_dict"], t["e_dict_s"])
    se += choice("/english/", t["e_all"], t["e_all_s"]) + "</div>\n</div></section>\n"
    sm = ('<section class="lang" id="maths"><div class="card">\n  <div class="head"><div class="ico" aria-hidden="true">%s</div><h2>%s<small>%s</small></h2></div>\n  <p class="lead">%s</p>'
          '%s<h3 class="mh">%s</h3><div class="choices">%s</div>\n</div></section>\n'
          % (ICO["maths"], t["m_h"], t["m_sub"], t["m_lead"],
             '<h3 class="mh">%s</h3><div class="choices">%s</div>' % (t["m_own"], math_cards(L, OWN[L])) if OWN[L] and t["m_own"] else "",
             t["m_oth"], math_cards(L, others(L))))
    h += "".join({"j": sj, "e": se, "m": sm}[k] for k in order)
    # ---- feats, faq, community
    h += '\n  <div class="feats">' + "".join('<div class="feat">%s<b>%s</b><span>%s</span></div>' % (FEAT_SVG[i], b, s) for i, (b, s) in enumerate(t["feats"])) + "</div>\n"
    h += '  <section class="faq"><h2>%s</h2>%s</section>\n' % (t["faq_h"], "".join("<details><summary>%s</summary><p>%s</p></details>" % qa for qa in t["faq"]))
    h += ('<div class="dc"><div><span class="k">%s</span><h2>%s</h2><p>%s</p></div>\n    <a class="btn-dc" href="%s" target="_blank" rel="noopener">%s%s</a></div>\n'
          % (t["dc_k"], t["dc_h"], t["dc_p"], DISCORD, DC_SVG, t["dc_b"]))
    h += ('<div class="line"><div><span class="k">%s</span><h2>%s</h2><p>%s</p></div>\n    <a class="btn-line" href="%s" target="_blank" rel="noopener">%s%s</a></div>\n'
          % (t["ln_k"], t["ln_h"], t["ln_p"], LINE, LN_SVG, t["ln_b"]))
    h += '  <p class="more">%s</p>\n</main>\n' % t["more"]
    h += footer(L, t, False)
    h += FOR_YOU % {"mine": json.dumps(t["mine"], ensure_ascii=False), "en": FOR_YOU_EN if L == "en" else ""} + "\n"
    if L in DICT_J:
        h += TS_JS + "\n"
    return h + "</body>\n</html>\n"


def build_about(L):
    t = tx(L, T[L])
    a = tx(L, A[L])
    cjk = L in ("ja", "zh", "tw")
    sep = "\u00a0: " if L == "fr" else "：" if cjk else ": "
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "AboutPage", "name": a["title"].split(" | ")[0], "url": SITE + pre(L) + "about.html", "inLanguage": HREFLANG[L], "description": a["desc"], "about": {"@id": SITE + "/#org"}},
        dict(org(), contactPoint={"@type": "ContactPoint", "contactType": "customer support", "url": SITE + "/mailform/",
                                   "availableLanguage": ["en", "ja", "vi", "id", "zh", "ko", "th", "es", "pt", "fr", "de", "ru", "ar", "it", "tr"]})]}
    h = head(L, a["title"], a["desc"], "about.html", ld, CSS_A)
    h += header(L, "about.html", t)
    jd, ed, co, mw, gm = a["jd"], a["ed"], a["co"], a["mw"], a["gm"]
    links = ("、" if cjk else ", ").join('<a href="%s">%s</a>' % (MATH_D[c][1], CC[L][c]) for c in OWN[L] + others(L))
    li = ['<li><b><a href="%s">%s</a></b>%s%s</li>' % (jdict(L) if L not in ("en", "ja") else "/japanese/", jd[0], sep, jd[1]),
          '<li><b><a href="%s">%s</a></b>%s%s</li>' % (edict(L) if L != "en" else "/english/", ed[0], sep, ed[1]),
          '<li><b>%s</b>%s%s</li>' % (co[0], sep, co[1]),
          ('<li><b><a href="/worksheets/">%s</a></b>%s%s（%s）。%s</li>' % (mw[0], sep, mw[1], links, mw[2])) if cjk else
          '<li><b><a href="/worksheets/">%s</a></b>%s%s %s. %s</li>' % (mw[0], sep, mw[1], links, mw[2]),
          '<li><b><a href="/game/">%s</a></b>%s%s</li>' % (gm[0], sep, gm[1])]
    if L in NEW:
        li = [li[3], li[0], li[1], li[2], li[4]]
    body = '<h1>%s</h1><p class="lead2">%s</p>\n' % (a["h1"], a["lead"])
    body += '<div class="stats3">' + "".join('<div class="s3"><b>%s</b><span>%s</span></div>' % x for x in a["stats"]) + "</div>\n"
    body += "<h2>%s</h2><ul>%s</ul>\n" % (a["h_what"], "".join(li))
    body += "<h2>%s</h2><ul>%s</ul>\n" % (a["h_you"], "".join(("<li><b>%s</b>%s</li>" if cjk else "<li><b>%s</b> %s</li>") % x for x in a["you"]))
    body += "<h2>%s</h2><p>%s</p>\n<h2>%s</h2><p>%s</p>\n" % (a["h_exp"], a["exp"], a["h_mis"], a["mis"])
    body += '<h2>%s</h2>\n<p><a class="btn2" href="%s">%s</a></p>\n' % (a["h_start"], pre(L), a["start"].replace("›", "&rsaquo;"))
    body += "<h2>%s</h2><table>%s</table>\n" % (a["h_op"], "".join("<tr><th>%s</th><td>%s</td></tr>" % x for x in a["op"]))
    body += ('<p style="margin-top:16px;font-size:13px"><a href="/privacypolicy.html%s">%s</a> · <a href="https://www.eigo-duke.com/aplus/" target="_blank" rel="noopener">%s</a></p>\n'
             % ("" if L == "en" else "?lang=" + L, a["pp"], a["corp"]))
    h += '\n<main class="ab"><article>\n' + body + "</article></main>\n"
    h += footer(L, t, True)
    return h + "</body>\n</html>\n"


if __name__ == "__main__":
    for L in LANGS:
        d = OUT if L == "en" else os.path.join(OUT, L)
        os.makedirs(d, exist_ok=True)
        if True:
            open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(build_index(L))
        open(os.path.join(d, "about.html"), "w", encoding="utf-8").write(build_about(L))
    print("ok")
