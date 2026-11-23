# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: partes comuns (números até 1.000, padrões com figuras, calendário).
Os geradores gen_br_matematica_2_*.py usam estas funções junto com br_common.
"""
import calendar as _cal
from br_common import num, pl, brn, relabel, fig, text, INK, NB, material_dourado as _md
import k_pics
import f_common

FORMAS = {"circle": ("círculo", "círculos", "m"), "square": ("quadrado", "quadrados", "m"),
          "rectangle": ("retângulo", "retângulos", "m"), "triangle": ("triângulo", "triângulos", "m")}
CORES = {"red": ("vermelho", "vermelha"), "blue": ("azul", "azul"), "yellow": ("amarelo", "amarela"), "green": ("verde", "verde")}
DIAS = ["domingo", "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado"]
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
DIAS_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def parts(n):
    return n // 100, n // 10 % 10, n % 10


def wrong(n, top=1000):
    """误答: troca de ordens, esquecer o zero, ±100, ±10, ±1"""
    c, d, u = parts(n)
    out = []
    z = int("".join(str(x) for x in (c, d, u) if x) or "0")
    if z != n:
        out.append(z)
    out += [c * 100 + u * 10 + d if d != u else None, d * 100 + c * 10 + u if c != d and d else None,
            n + 100 if n < 900 else n - 100, n + 10 if n % 100 < 90 else n - 10, n + 1, n - 1, u * 100 + d * 10 + c if u and u != c else None]
    return [num(x) for x in out if x and 0 < x <= top and x != n]


def md(c, d, u):
    """material dourado sem o cubo grande"""
    return relabel(_md(0, c, d, u), "material dourado: %s, %s e %s" % (pl(c, "placa", "placas"), pl(d, "barra", "barras"), pl(u, "cubinho", "cubinhos")))


def cdu(c, d, u):
    words = [pl(v, a, b) for v, a, b in ((c, "centena", "centenas"), (d, "dezena", "dezenas"), (u, "unidade", "unidades")) if v]
    return words[0] if len(words) == 1 else ", ".join(words[:-1]) + " e " + words[-1]


# ------------------------------------------------------------ padrões com figuras
def forma(kind, color):
    """«quadrado azul», «bola»"""
    if kind in FORMAS:
        return "%s %s" % (FORMAS[kind][0], CORES[color][0])
    return k_pics.name(kind, 1)


def item_nome(it):
    if it[0] == "shape":
        return forma(it[1], it[2])
    from br_common import COISAS
    return COISAS[it[1]][0]


def padrao(items, blanks=0):
    """sequência de figuras em fila; ('blank',) mostra um ?"""
    svg = f_common.pattern_svg(items, blanks)
    return fig(relabel(svg, "sequência: " + ", ".join("?" if it[0] == "blank" else item_nome(it) for it in items)))


def opcoes(cands):
    """respostas A a D com figuras"""
    return fig(relabel(f_common.choice_row_svg(cands), "respostas A, B, C e D"))


# ------------------------------------------------------------ calendário
def mes_svg(ano, mes, marks=(), title=True):
    """folha de calendário de um mês (domingo primeiro); marks: dias circulados"""
    first = (_cal.weekday(ano, mes, 1) + 1) % 7  # domingo = 0
    nd = _cal.monthrange(ano, mes)[1]
    cw, ch, top = 44, 30, 58
    s = []
    if title:
        s.append(text(7 * cw / 2 + 8, 22, "%s de %d" % (MESES[mes - 1].capitalize(), ano), 16))
    for i, d in enumerate(["D", "S", "T", "Q", "Q", "S", "S"]):
        s.append("<rect x='%d' y='32' width='%d' height='22' fill='%s' stroke='%s' stroke-width='0.8'/>" % (8 + i * cw, cw, "#f6d6d6" if i == 0 else "#e8eef6", INK))
        s.append(text(8 + i * cw + cw / 2, 48, d, 13))
    for day in range(1, nd + 1):
        k = first + day - 1
        r, c = divmod(k, 7)
        x, y = 8 + c * cw, top + r * ch
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='0.8'/>" % (x, y, cw, ch, INK))
        if day in marks:
            s.append("<circle cx='%d' cy='%d' r='12' fill='none' stroke='#e53935' stroke-width='2'/>" % (x + cw / 2, y + ch / 2))
        s.append(text(x + cw / 2, y + 20, str(day), 13, col="#c62828" if c == 0 else INK))
    rows = (first + nd + 6) // 7
    W, H = 16 + 7 * cw, top + rows * ch + 8
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' data-pf='lg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' aria-label='calendário de %s de %d'>"
           "<g font-family='Arial, Helvetica, sans-serif'>%s</g></svg>" % (W, H, W, H, MESES[mes - 1], ano, "".join(s)))
    return fig(svg)


def dia_semana(ano, mes, dia):
    return DIAS[(_cal.weekday(ano, mes, dia) + 1) % 7]
