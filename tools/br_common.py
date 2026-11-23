# -*- coding: utf-8 -*-
"""
Brasil (Ensino Fundamental, BNCC) の単元生成の共通部品。
・文はポルトガル語（ブラジル）。子ども向けに短い文、você で話しかける（Calcule, Escolha, Quantos …?）
・数: 1.000 以上は点で区切る（1.000、4.536、12.345）。小数はコンマ（2,5）
・記号: 3 × 4、12 ÷ 3。余りは「23 ÷ 5 = 4 e resto 3」。時刻は 8h15（デジタル時計は 08:15）、時間の長さは 1 h 25 min
・お金: R$ 3,50、50 centavos（硬貨 5・10・25・50 centavos と R$ 1、紙幣 R$ 2・5・10・20・50・100・200）
・位の名前: U, D, C, UM（unidade, dezena, centena, unidade de milhar）。位取りの積み木は material dourado
・HTML の属性はシングルクォート、バックスラッシュなし（check.py と同じルール）
"""
import math
import random
import os
import re
from ws_common import (fig, svg_wrap, text, line, balance, write_unit, fr,   # noqa: F401
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT)
import fr_common as _F
from fr_common import pick_unique, mix  # noqa: F401

UPDATED = "2026-11-23"
NB = " "
VEZES = "×"
DIV = "÷"
STD_URL = "http://basenacionalcomum.mec.gov.br/images/BNCC_EI_EF_110518_versaofinal_site.pdf"
DOMAIN = {"N": "Números", "A": "Álgebra", "G": "Geometria", "M": "Grandezas e medidas", "E": "Probabilidade e estatística"}
GRADE_NAME = {"%d-ano" % i: "%dº ano" % i for i in range(1, 10)}
GRADE_NAME.update({"%d-serie" % i: "%dª série" % i for i in range(1, 4)})   # Ensino Médio
GIRLS = ["Helena", "Alice", "Laura", "Maria", "Valentina", "Heloísa", "Sofia", "Manuela", "Júlia", "Lívia", "Cecília", "Beatriz", "Lara", "Isabela"]
BOYS = ["Miguel", "Arthur", "Gael", "Heitor", "Theo", "Davi", "Gabriel", "Bernardo", "Samuel", "João", "Pedro", "Lucas", "Rafael", "Enzo"]


# ------------------------------------------------------------ numbers
def num(n):
    """1.000, 4.536, 12.345（1.000 以上は点で区切る）"""
    n = int(n)
    s = str(abs(n))
    g = []
    while len(s) > 3:
        g.insert(0, s[-3:])
        s = s[:-3]
    g.insert(0, s)
    return ("−" if n < 0 else "") + ".".join(g)


def dec(v, places=None):
    """número decimal com vírgula: 2,5 / 1,25"""
    if places is None:
        s = ("%.3f" % v).rstrip("0").rstrip(".")
    else:
        s = ("%." + str(places) + "f") % v
    ip, _, fp_ = s.partition(".")
    return num(int(ip)) + ("," + fp_ if fp_ else "")


def dz(n, k, keep=False):
    """inteiro n × 10^−k com vírgula: dz(25, 1) → 2,5；dz(250, 2) → 2,5（keep=True で 2,50）"""
    n = int(n)
    neg = n < 0
    ip, fp_ = divmod(abs(n), 10 ** k)
    f = str(fp_).rjust(k, "0") if k else ""
    if not keep:
        f = f.rstrip("0")
    return ("−" if neg else "") + num(ip) + ("," + f if f else "")


def reais(cents, c=False):
    """dinheiro: 350 → R$ 3,50, 300 → R$ 3,00, 45 → 45 centavos（c=True のとき R$ 1 未満は centavos）"""
    cents = int(cents)
    if c and cents < 100:
        return "%d%scentavos" % (cents, NB)
    e, r = divmod(cents, 100)
    return "R$%s%s,%02d" % (NB, num(e), r)


def unit(v, u):
    return "%s%s%s" % (num(v) if isinstance(v, int) else v, NB, u)


def hora(h, m):
    """8h, 8h15, 14h30"""
    return "%dh" % h if m == 0 else "%dh%02d" % (h, m)


def dur(mins):
    """duração: 1 h 25 min, 45 min, 2 h"""
    h, m = divmod(int(mins), 60)
    if h and m:
        return "%d%sh%s%d%smin" % (h, NB, NB, m, NB)
    if h:
        return "%d%sh" % (h, NB)
    return "%d%smin" % (m, NB)


def pl(n, s, p):
    """1 lápis / 3 lápis, 1 bala / 3 balas"""
    return "%s %s" % (num(n), s if n == 1 else p)


# ------------------------------------------------------------ names
class Kids:
    """nomes com gênero: next() → (nome, 'ela'|'ele')"""

    def __init__(self, rnd):
        self.pool = [(n, "ela") for n in GIRLS] + [(n, "ele") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def two(self):
        a = self.next()
        b = self.next()
        while b[0] == a[0]:
            b = self.next()
        return a, b


def o(p):
    """o/a: « o Davi », « a Laura »（artigo antes do nome）"""
    return "a" if p[1] == "ela" else "o"


def do(p):
    return "da" if p[1] == "ela" else "do"


# ------------------------------------------------------------ questions
_NUM_RE = re.compile(r"^(.*?)(\d{1,3}(?:\.\d{3})*(?:,\d+)?)([^\d]*)$")


def mcq(q, correct, cands, e, neg=False):
    """4 択：正解＋重複しない誤答 3 つ。足りないときは答えの数を ±1、±2 … した近い数で補う。"""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or (not neg and (c.startswith("-") or c.startswith("−"))):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3 and os.environ.get("BR_WARN"):
        print("FILL:", re.sub(r"<[^>]+>", " ", q)[-90:], "|", correct)
    if len(pick) < 3 and "<" not in correct:
        m = _NUM_RE.match(correct)
        if m:
            raw = m.group(2).replace(".", "")
            places = len(raw.split(",")[1]) if "," in raw else 0
            v = int(raw.replace(",", ""))
            step = 100 if "R$" in m.group(1) and places == 2 else 1
            for d_ in (1, -1, 2, -2, 3, 10, -10):
                nv = v + d_ * step
                if nv <= 0:
                    continue
                body = num(nv) if places == 0 else "%s,%s" % (num(nv // 10 ** places), str(nv % 10 ** places).rjust(places, "0"))
                c = "%s%s%s" % (m.group(1), body, m.group(3))
                if c not in seen:
                    seen.add(c)
                    pick.append(c)
                if len(pick) == 3:
                    break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


# ------------------------------------------------------------ lesson
table = _F.table


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Exemplo</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Resposta: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist, extra=""):
    """body_html : Como pensar → Exemplos → Erros comuns（frases curtas）"""
    h = "<h2>Como pensar</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += extra
    h += "".join(example(a, b, c) for a, b, c in examples)
    h += "<h2>Erros comuns</h2>" + table(["Erro comum", "O que fazer"], mist)
    return h


def plain_text(t):
    t = re.sub(r"<span class='fr'><span class='fn'>(.*?)</span><span class='fd'>([^<]*)</span></span>", r"\1/\2", t)
    assert not re.search(r"<[a-zA-Z/]", t), t
    return t


def make_unit(rnd, slug, dom, codes, std_text, title, short_title, meta_desc,
              key_big, key_sub, body_html, faq, sets, sort, grade="3-ano"):
    """codes: códigos da BNCC, ex. ["EF03MA05", "EF03MA06"]"""
    sets = [{"title": t, "items": items} for t, items in sets]
    assert len(sets) == 5, slug
    allq = set()
    for s in sets:
        assert len(s["items"]) == 20, (slug, s["title"], len(s["items"]))
        for it in s["items"]:
            k = re.sub(r"\s+", " ", it["q"])
            assert k not in allq, ("duplicate question", slug, k)
            allq.add(k)
            for f in [it["q"], it["e"]] + it["c"]:
                assert not re.search(r"\d \d{3}\b", re.sub(r"<[^>]+>", "", f)), ("thin-space number", slug, f)
    balance(sets, rnd)
    gname = GRADE_NAME[grade]
    seo_title = "%s – %s: atividades de matemática com gabarito" % (short_title, gname)
    title, seo_title, short_title, meta_desc, key_big, key_sub = [plain_text(x) for x in (title, seo_title, short_title, meta_desc, key_big, key_sub)]
    write_unit("br", "matematica", grade, {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": DOMAIN[dom], "standard_code": ", ".join(codes), "standard_url": STD_URL,
        "standard_text": std_text + " (BNCC, Matemática, %s)" % gname,
        "meta_desc": meta_desc, "key_big": key_big, "key_sub": key_sub,
        "body_html": body_html, "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


# ------------------------------------------------------------ pictures（ラベルはポルトガル語、数は 1.000 の形）
def brn(svg):
    """fr_common の絵の数（1 000）を 1.000 に"""
    return re.sub(r"(\d) (\d{3})(?!\d)", r"\1.\2", svg)


def wrap(w, h, body, label, lg=False):
    return _F.wrap(w, h, body, label, lg)


def relabel(svg, label):
    return re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label.replace("'", "’"), svg, count=1)


def reta(lo, hi, step, marks=(), labels=None, every=None, width=460):
    """reta numérica"""
    return brn(_F.droite(lo, hi, step, marks, labels, "reta numérica", every, width))


def material_dourado(m, c, d, u):
    """cubo grande (milhar), placa (centena), barra (dezena), cubinho (unidade)"""
    return brn(_F.blocs(m, c, d, u, label="material dourado: %d milhares, %d centenas, %d dezenas, %d unidades" % (m, c, d, u)))


def quadro_valor(n, cols=4):
    """quadro de valor posicional: CM DM UM C D U（cols は 6 まで）"""
    head = ["CM", "DM", "UM", "C", "D", "U"][6 - cols:]
    ds = str(n).rjust(cols, " ")
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % ("".join("<th>%s</th>" % h for h in head),
               "".join("<td style='text-align:center;min-width:30px'>%s</td>" % (d if d != " " else "") for d in ds)))


def quadro_decimal(milesimos, places=3, ints=1):
    """quadro de valor posicional com decimais: U, d c m（milesimos = valor × 1000）"""
    head = ["C", "D", "U"][3 - ints:] + ["d", "c", "m"][:places]
    ip, fp_ = divmod(int(milesimos), 1000)
    ds = str(ip).rjust(ints, " ") + str(fp_).rjust(3, "0")[:places]
    cells = []
    for i, d in enumerate(ds):
        b = " style='text-align:center;min-width:30px%s'" % (";border-left:3px solid #333" if i == ints else "")
        cells.append("<td%s>%s</td>" % (b, d if d != " " else ""))
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % ("".join("<th>%s</th>" % h for h in head), "".join(cells)))


def reta_frac(d, units=2, marks=(), width=420):
    """reta numérica de 0 a units, cada unidade em d partes; marks = [(numerador, letra)]"""
    return relabel(_F.droite_frac(d, units, marks, width), "reta numérica dividida em partes iguais")


def grafico(data, unit_label="", step=None):
    """gráfico de colunas"""
    return brn(relabel(_F.barres(data, unit_label, "gráfico de colunas", step), "gráfico de colunas"))


def coin(cx, cy, cents):
    r = {5: 14, 10: 15, 25: 17, 50: 16, 100: 18}[cents]
    fillc = {5: "#c9733c", 10: "#e0b84c", 25: "#e0b84c", 50: "#d6d6d6", 100: "#d6d6d6"}[cents]
    ring = ""
    if cents == 100:
        fillc = "#e0b84c"
        ring = "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#d6d6d6' stroke='%s'/>" % (cx, cy, r * 0.66, INK)
    lab = "1%sreal" % NB if cents == 100 else "%d%sc" % (cents, NB)
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>%s" % (cx, cy, r, fillc, INK, ring)
            + text(cx, cy + 4, lab, 8 if cents == 100 else 10))


def note(x, y, real):
    col = {2: "#9fb7d6", 5: "#c9a6d9", 10: "#e8a0a0", 20: "#f3d27a", 50: "#e8b07a", 100: "#8fc0e8", 200: "#c8bba6"}[real]
    return ("<rect x='%.1f' y='%.1f' width='72' height='38' rx='4' fill='%s' stroke='%s' stroke-width='1.5'/>"
            % (x, y, col, INK) + text(x + 36, y + 25, "R$%s%d" % (NB, real), 14))


def dinheiro_svg(items):
    """items: valores em centavos; de 200 para cima, cédulas"""
    s, x, y = [], 6, 6
    notes = sorted([c for c in items if c >= 200], reverse=True)
    coins = sorted([c for c in items if c < 200], reverse=True)
    for c in notes:
        if x > 6 + 80 * 4:
            x, y = 6, y + 46
        s.append(note(x, y, c // 100))
        x += 80
    if notes and coins and x > 6 + 80 * 3:
        x, y = 6, y + 46
    for c in coins:
        r = 19
        if x > 360:
            x, y = 6, y + 44
        s.append(coin(x + r, y + 19, c))
        x += 2 * r + 4
    W = max(80 * min(len(notes), 5), x) + 8 if notes else x + 4
    return wrap(max(W, x + 4), y + 46, "".join(s), "moedas e cédulas: ao todo %s" % reais(sum(items)).replace(NB, " "))


def solido_svg(kind, r=34, color="#cfe6d6"):
    """cubo, bloco, esfera, cilindro, cone, piramide"""
    import de_common
    k = {"cubo": "wuerfel", "bloco": "quader", "esfera": "kugel", "cilindro": "zylinder", "cone": "kegel", "piramide": "pyramide"}[kind]
    return relabel(de_common.solid_svg(k, r, color), "uma figura geométrica espacial")


def relogio(h, m, size=170):
    from tw_common import clock as _clock
    return _clock(h, m, size, label="relógio de ponteiros")


def digital(h, m):
    """relógio digital 08:15"""
    body = ("<rect x='4' y='4' width='132' height='56' rx='10' fill='#1f2a36' stroke='%s' stroke-width='2'/>" % INK
            + text(70, 44, "%02d:%02d" % (h, m), 30, col="#7ef0a0"))
    return wrap(140, 64, body, "relógio digital marcando %02d:%02d" % (h, m))


def armada(rows, op="+", label="conta armada", result=None):
    """conta armada (algoritmo) em papel quadriculado"""
    import de_common
    rows = [r.replace(".", "") for r in rows]
    return de_common.schriftlich(rows, op, None, label, result.replace(".", "") if result else None)


def faixa(d, k, w=300):
    return relabel(_F.bande(d, k, w), "faixa dividida em %d partes iguais, %d %s" % (d, k, "pintada" if k == 1 else "pintadas"))


def disco(d, k, r=60):
    return relabel(_F.disque(d, k, r), "círculo dividido em %d partes iguais, %d %s" % (d, k, "pintada" if k == 1 else "pintadas"))


# ------------------------------------------------------------ números por extenso (até 9.999)
_U = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez",
      "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
_D = {2: "vinte", 3: "trinta", 4: "quarenta", 5: "cinquenta", 6: "sessenta", 7: "setenta", 8: "oitenta", 9: "noventa"}
_C = {1: "cento", 2: "duzentos", 3: "trezentos", 4: "quatrocentos", 5: "quinhentos", 6: "seiscentos", 7: "setecentos", 8: "oitocentos", 9: "novecentos"}


def _w99(n):
    if n < 20:
        return _U[n]
    d, u = divmod(n, 10)
    return _D[d] + ("" if u == 0 else " e " + _U[u])


def _w999(n):
    if n == 100:
        return "cem"
    c, r = divmod(n, 100)
    if not c:
        return _w99(r)
    return _C[c] + ("" if r == 0 else " e " + _w99(r))


def extenso(n):
    """número por extenso: 342 → trezentos e quarenta e dois, 1300 → mil e trezentos"""
    if n == 0:
        return "zero"
    k, r = divmod(n, 1000)
    out = ""
    if k:
        out = "mil" if k == 1 else _w999(k) + " mil"
    if r:
        if out:
            out += (" e " if r < 100 or r % 100 == 0 else " ")
        out += _w999(r)
    return out


# ------------------------------------------------------------ objetos desenhados (k_pics) com nomes em português
COISAS = {"apple": ("maçã", "maçãs", "f"), "star": ("estrela", "estrelas", "f"), "ball": ("bola", "bolas", "f"), "button": ("botão", "botões", "m"),
          "fish": ("peixe", "peixes", "m"), "flower": ("flor", "flores", "f"), "heart": ("coração", "corações", "m"), "duck": ("pato", "patos", "m"),
          "cup": ("xícara", "xícaras", "f"), "bug": ("joaninha", "joaninhas", "f")}
KINDS = sorted(COISAS)


def coisas(kind, n):
    s, p, _ = COISAS[kind]
    return "%s %s" % (num(n), s if n == 1 else p)


def _pic(svg, label, lg=False):
    svg = relabel(svg, label)
    if lg and "data-pf" not in svg:
        svg = svg.replace("<svg ", "<svg data-pf='lg' ", 1)
    return svg if svg.startswith("<div") else fig(svg)


def arranjo(rows, cols, kind):
    """disposição retangular: rows linhas com cols objetos"""
    import k_pics
    return _pic(k_pics.array_svg(rows, cols, kind), "%d linhas com %s cada" % (rows, coisas(kind, cols)))


def grupos(g, k, kind):
    """g grupos iguais com k objetos"""
    import k_pics
    return _pic(k_pics.groups_svg([(k, kind)] * g), "%d grupos com %s cada" % (g, coisas(kind, k)))


def linha(n, kind, per_row=10):
    import k_pics
    return _pic(k_pics.row_svg(n, kind, per_row), coisas(kind, n))


# ------------------------------------------------------------ reutilizar geradores de outros anos
_BRNUM = re.compile(r"(?<![\d.,])(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d+))?(?![\d])")


def nums_in(it):
    """números (inteiros e decimais) do texto visível de q, c e e"""
    txt = re.sub(r"<[^>]+>", " ", " ".join([it["q"], it["e"]] + list(it["c"])))
    txt = re.sub(r"(?:EF0\dMA\d\d|\d+º|\d+ª)", " ", txt)
    out = []
    for m in _BRNUM.finditer(txt):
        out.append((int(m.group(1).replace(".", "")), len(m.group(2)) if m.group(2) else 0))
    return out


def lim(maxn=99999, places=2):
    """predicado: nenhum número maior que maxn nem com mais de «places» casas decimais"""
    def ok(it):
        return all(v <= maxn and p <= places for v, p in nums_in(it))
    return ok


def keep(maker, *preds):
    """envolve um gerador: devolve None quando o item não passa nos filtros"""
    def mk():
        it = maker()
        if it is None:
            return None
        for p in preds:
            if not p(it):
                return None
        return it
    mk.__name__ = getattr(maker, "__name__", "mk")
    return mk


def swap(mod, seed):
    """troca o R (e o K, se houver) de um gerador importado"""
    mod.R = random.Random(seed)
    if hasattr(mod, "K"):
        mod.K = Kids(mod.R)
    return mod


def use(modname, seed, *names, preds=()):
    """importa um gerador de outro ano, troca o R e devolve os geradores pedidos (com filtros)"""
    import importlib
    m = importlib.import_module(modname)
    if getattr(m, "_br_seed", None) != seed:
        swap(m, seed)
        m._br_seed = seed
    out = [keep(getattr(m, n), *preds) for n in names]
    return out[0] if len(out) == 1 else out
