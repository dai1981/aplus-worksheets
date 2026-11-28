# -*- coding: utf-8 -*-
"""
México / Ciencias。country `mx`、subject `science`（name「Ciencias」）。
  preescolar・1〜6-primaria（NEM, campo formativo Saberes y Pensamiento Científico, Programas sintéticos 2024）、
  1〜3-secundaria（Fase 6: Biología, Física, Química）、
  bachillerato（MCCEMS, Ciencias Naturales, Experimentales y Tecnología: 6 UAC, una por semestre）
  単元は España の理科（es_sc*）の単元をそのまま使い、問題・本文を mx_common.mx_text でメキシコ式（小数点、1 000、$、語彙）にする。
  他国の語が残る問題は mx_item が落とす。本文などに残ると止まる（PATCH で直す）。
  python3 mx_sci.py 3-primaria [slug|番号 …]   seed は 58000 + 100 × n + 番号
"""
import re
import sys
from sci_common import Unit
from ws_common import write_unit
import es_sci
import mx_common as M

UPDATED = "2026-11-28"
MCC = "https://educacionmediasuperior.sep.gob.mx/work/models/sems/Resource/13634/1/images/Progresiones_del_MCCEMS_2024_final.pdf"

# MX grado → (n, nombre, [(grado de España, slug)])
P = "primaria"
GRADES = [
    ("preescolar", 0, "Preescolar", [("1-primaria", s) for s in ("los-seres-vivos", "los-animales", "el-cuerpo-y-los-sentidos", "empujar-y-tirar")]),
    ("1-primaria", 1, "1.er grado de primaria", [("1-primaria", "las-plantas"), ("1-primaria", "los-materiales"), ("2-primaria", "la-alimentacion-sana"), ("2-primaria", "el-agua-y-sus-estados"),
                                                  ("2-primaria", "la-luz-y-el-sonido")]),
    ("2-primaria", 2, "2.º grado de primaria", [("2-primaria", "vertebrados-e-invertebrados"), ("2-primaria", "la-vida-de-las-plantas"), ("2-primaria", "los-habitats"),
                                                 ("3-primaria", "la-materia-y-sus-propiedades"), ("3-primaria", "las-fuerzas")]),
    ("3-primaria", 3, "3.er grado de primaria", [("3-primaria", s) for s in ("los-animales-vertebrados", "los-animales-invertebrados", "la-nutricion-de-las-plantas", "el-aparato-locomotor", "el-metodo-cientifico")]),
    ("4-primaria", 4, "4.º grado de primaria", [("4-primaria", s) for s in ("los-reinos-de-los-seres-vivos", "los-sentidos-y-el-sistema-nervioso", "la-digestion-y-la-respiracion",
                                                                          "los-ecosistemas-y-las-cadenas-alimentarias", "las-mezclas", "la-energia-y-sus-fuentes", "las-maquinas")]),
    ("5-primaria", 5, "5.º grado de primaria", [("5-primaria", s) for s in ("la-celula-y-los-tejidos", "la-circulacion-y-la-excrecion", "masa-volumen-y-densidad", "cambios-fisicos-y-quimicos",
                                                                          "el-calor-y-la-temperatura", "la-luz", "la-programacion-y-los-robots")]),
    ("6-primaria", 6, "6.º grado de primaria", [("6-primaria", s) for s in ("los-microorganismos", "la-reproduccion-humana", "la-salud-y-los-habitos-saludables", "la-electricidad-y-el-magnetismo",
                                                                          "fuerzas-y-movimiento", "el-sonido", "la-energia-y-el-desarrollo-sostenible")] + [("1-eso", "el-universo-y-el-sistema-solar")]),
    ("1-secundaria", 7, "1.er grado de secundaria", [("1-eso", s) for s in ("la-celula-y-la-organizacion-de-los-seres-vivos", "la-clasificacion-de-los-seres-vivos", "las-plantas", "los-animales-invertebrados",
                                                                        "los-animales-vertebrados", "los-ecosistemas")] +
     [("3-eso", s) for s in ("alimentacion-y-nutricion", "aparatos-digestivo-y-respiratorio", "aparatos-circulatorio-y-excretor", "sistema-nervioso-y-endocrino", "la-reproduccion-humana", "salud-y-enfermedad")] +
     [("4-eso", "genetica-mendeliana"), ("4-eso", "la-evolucion")]),
    ("2-secundaria", 8, "2.º grado de secundaria", [("2-eso", s) for s in ("magnitudes-y-unidades", "el-movimiento", "las-fuerzas", "la-energia", "calor-y-temperatura", "la-luz-y-el-sonido")] +
     [("3-eso", "la-electricidad")] + [("4-eso", s) for s in ("cinematica", "las-leyes-de-newton", "presion-y-fluidos", "trabajo-energia-y-potencia")] + [("1-eso", "la-tierra-y-la-luna")]),
    ("3-secundaria", 9, "3.er grado de secundaria", [("2-eso", s) for s in ("la-materia-y-sus-propiedades", "estados-de-agregacion-y-teoria-cinetica", "sustancias-puras-y-mezclas", "los-cambios-quimicos")] +
     [("3-eso", s) for s in ("el-atomo-y-la-tabla-periodica", "enlace-quimico-y-formulacion", "el-mol-y-las-reacciones-quimicas")] + [("4-eso", "reacciones-quimicas-y-estequiometria"), ("4-eso", "quimica-del-carbono")]),
    ("la-materia-y-sus-interacciones", 10, "La materia y sus interacciones", [("1-bachillerato", "estructura-atomica-y-enlace-quimico"), ("1-bachillerato", "gases-y-disoluciones"),
                                                                             ("2-bachillerato", "modelo-cuantico-y-propiedades-periodicas"), ("2-bachillerato", "enlace-quimico-y-geometria-molecular")]),
    ("conservacion-de-la-energia", 11, "Conservación de la energía y sus interacciones con la materia", [("1-bachillerato", s) for s in ("cinematica-del-punto-material", "dinamica", "energia-mecanica-y-trabajo")] +
     [("2-bachillerato", s) for s in ("campo-gravitatorio", "campo-electrico", "campo-magnetico-e-induccion")]),
    ("ecosistemas", 12, "Ecosistemas: interacciones, energía y dinámica", [("1-bachillerato", s) for s in ("ecologia-y-sostenibilidad", "fisiologia-e-histologia-vegetal", "los-microorganismos-y-formas-acelulares",
                                                                                                     "dinamica-y-composicion-terrestre")] + [("2-bachillerato", "recursos-naturales-y-sostenibilidad")]),
    ("reacciones-quimicas", 13, "Reacciones químicas: conservación de la materia en la formación de nuevas sustancias", [("1-bachillerato", s) for s in ("estequiometria-y-termoquimica", "quimica-organica")] +
     [("2-bachillerato", s) for s in ("cinetica-quimica", "equilibrio-quimico", "acidos-y-bases", "reacciones-redox-y-electroquimica")]),
    ("la-energia-en-la-vida-diaria", 14, "La energía en los procesos de la vida diaria", [("2-bachillerato", s) for s in ("ondas-y-optica", "fisica-moderna", "las-biomoleculas", "el-metabolismo-celular")]),
    ("organismos-herencia-y-evolucion", 15, "Organismos: estructuras y procesos. Herencia y evolución biológica", [("2-bachillerato", s) for s in ("la-celula-eucariota", "genetica-molecular", "microbiologia-y-biotecnologia", "inmunologia")] +
     [("1-bachillerato", s) for s in ("fisiologia-e-histologia-animal", "historia-de-la-tierra-y-de-la-vida")]),
]
BYSLUG = {g[0]: g for g in GRADES}
SHORTN = {"conservacion-de-la-energia": "Conservación de la energía", "ecosistemas": "Ecosistemas", "reacciones-quimicas": "Reacciones químicas",
          "organismos-herencia-y-evolucion": "Organismos, herencia y evolución"}

# dominio de España → México
DOM_P = {"B": "La Tierra y el universo", "V": "Seres vivos y cuerpo humano", "M": "Materia, energía e interacciones", "A": "Pensamiento científico", "T": "Tecnología"}
DOM_S = {7: "Biología", 8: "Física", 9: "Química"}
DOM_B = {"BG": "Biología y Geología", "FQ": "Física y Química", "BI": "Biología", "Q": "Química", "FI": "Física", "GC": "Geología y ciencias ambientales"}

# textos que hay que cambiar (España → México) en el texto de la lección, la FAQ, etc.
PATCH = [("¿Qué animal ibérico está en peligro?", "¿Qué animal de México está en peligro?"), ("El lince ibérico, el oso pardo o el urogallo, entre otros.", "El ajolote, la vaquita marina o el jaguar, entre otros."),
         ("¿Qué ecosistemas hay en España?", "¿Qué ecosistemas hay en México?"), ("Bosques, dehesas, ríos, humedales como Doñana, montañas y costas.", "Selvas, bosques, desiertos, manglares como los Pantanos de Centla, montañas y costas."),
         ("¿Qué es un ecosistema protegido en España?", "¿Qué es un ecosistema protegido en México?"), ("Doñana, Picos de Europa o el Teide, entre otros parques nacionales.", "Calakmul, Sian Ka’an o la Mariposa Monarca, entre otras reservas de la biosfera."),
         ("Doñana es un parque nacional.", "Calakmul es una reserva de la biosfera."), ("los linces de Doñana", "los jaguares de Calakmul"), (", red trófica, Doñana", ", red trófica, reservas de la biosfera"),
         ("Lynx pardinus", "Lynx rufus"), ("lince ibérico", "lince rojo"), ("Aquila adalberti", "Aquila chrysaetos"), ("águila imperial ibérica", "águila real"),
         ("fauna ibérica amenazada", "fauna mexicana amenazada"), ("fauna ibérica", "fauna de México"), ("El lince rojo vive en España.", "El lince rojo vive en México."),
         ("El alumnado", "El estudiante"), ("del grifo", "de la llave"), ("Del grifo", "De la llave"), ("un grifo", "una llave"), ("el grifo", "la llave"), ("grifo", "llave"), ("el ordenador", "la computadora"), ("un ordenador", "una computadora"), ("ordenadores", "computadoras"), ("ordenador", "computadora"), ("la nevera", "el refrigerador"), ("una nevera", "un refrigerador"), ("nevera", "refrigerador"), ("el frigorífico", "el refrigerador"), ("frigorífico", "refrigerador"), ("las gafas", "los lentes"), ("unas gafas", "unos lentes"), ("gafas", "lentes"), ("el alumnado", "el estudiante"), ("en España", "en México"), ("de España", "de México"), ("España", "México"),
         ("la península", "el país"), ("peninsular", "del país"), ("Teide", "Popocatépetl"), ("Pirineos", "la Sierra Madre"), ("Sierra Nevada", "la Sierra Madre Oriental"),
         ("Cantábrico", "golfo de México"), ("Mediterráneo", "Pacífico"), ("Ebro", "Bravo"), ("Tajo", "Lerma"), ("Guadalquivir", "Usumacinta")]
EXTRA_LEAKS = ["España", "español de", "Canarias", "Pirineo", "Teide", "Doñana", "Madrid", "LOMLOE", "comunidades autónomas", "Selectividad", "PAU", "ESO", "Bachillerato", "Primaria"]
# palabras de España (con límite de palabra: «cromo» no debe tocar «cromosoma»)
SCI_LEAKS = ["€", "euro", "euros", "céntimo", "céntimos", "España", "vosotros", "habéis", "tenéis", "sabéis", "LOMLOE", "IVA", "tarta", "gominola", "chuche", "tiza", "estuche", "bocadillo",
             "gafas", "folio", "ordenador", "ordenadores", "zapatilla", "zapatillas", "cole", "nata", "judías", "tebeo", "chaqueta", "jersey", "Renfe", "colegio", "Galicia", "Andalucía", "Canarias",
             "Asturias", "Cataluña", "Teide", "Mulhacén", "Moncayo", "cucurucho", "Aneto", "Pirineo", "Pirineos", "Doñana", "Madrid", "Selectividad", "PAU", "ESO", "Bachillerato", "Primaria",
             "castellano", "ibérica", "Ibérica", "ibérico", "Doñana", "zumo", "grifo", "coche", "coches", "móvil", "patata", "patatas", "melocotón", "piscina", "mariquita", "ordenador", "nevera", "frigorífico",
             "gasoil", "gasóleo", "fontanero", "vale la pena"]
_LK = [re.compile(r"(?<![\wÁÉÍÓÚáéíóúñÑ])" + re.escape(w) + r"(?![\wáéíóúñ])") for w in SCI_LEAKS]


def _p(s):
    for a, b in PATCH:
        s = s.replace(a, b)
    return s


def div(s):
    """« : » (división en España) → « ÷ », solo fuera de las etiquetas"""
    parts = re.split(r"(<[^>]*>)", s)
    return "".join(p if p.startswith("<") else re.sub(r"([ \u00a0]):([ \u00a0])", r"\1÷\2", p) for p in parts)


def mtx(s):
    return div(M.mx_text(_p(s)))


def leaks(t):
    plain = re.sub(r"<[^>]*>", " ", t)
    for r in _LK:
        m = r.search(plain)
        if m:
            return m.group(0)
    for r in (r"\bgr[áa]ficos?\b", r"\bos\b", r"\bvuestr", r"\b(la|las) (una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce) menos\b"):
        if re.search(r, plain):
            return r
    return None


def _leak(t, where):
    w = leaks(t)
    assert not w, ("leak", where, w, re.sub(r"<[^>]*>", " ", t)[:160])


def mx_item(it):
    it = dict(it)
    it["q"], it["e"] = div(M.mx_text(it["q"])), div(M.mx_text(it["e"]))
    it["c"] = [re.sub(r"^-(?=\d)", "−", div(M.mx_text(c))) for c in it["c"]]
    it["q"], it["e"] = [re.sub(r"(?<=[=(\s])-(?=\d)", "−", t) for t in (it["q"], it["e"])]
    it["q"] = it["q"].replace("aria-label='gráfico", "aria-label='gráfica")
    if len({c.strip().lower() for c in it["c"]}) < 4 or leaks(it["q"] + " " + " ".join(it["c"]) + " " + it["e"]):
        return None
    return it


def wrap(mk):
    def f():
        x = mk()
        if x is None:
            return None
        x = dict(x)
        x["q"], x["e"] = _p(es_sci.esc(x["q"])), _p(es_sci.esc(x["e"]))
        x["c"] = [_p(es_sci.esc(c)) for c in x["c"]]
        return mx_item(x)
    return f


def es_unit(eg, slug):
    for u in es_sci.units(eg):
        if u["slug"] == slug:
            return u
    raise KeyError((eg, slug))


def seed_of(n, sort):
    return 58000 + 100 * n + sort


def build(gslug, eg, slug, sort):
    _, n, gname, _ = BYSLUG[gslug]
    u = es_unit(eg, slug)
    U_ = Unit(seed_of(n, sort))
    spec = u["sets"](es_sci.K(U_.R))
    spec = [(t, [(wrap(mk), k) for mk, k in parts]) for t, parts in spec]
    sets = U_.sets(spec)
    for s in sets:
        s["title"] = mtx(es_sci.esc(s["title"]))
        for x in s["items"]:
            for t in [x["q"], x["e"]] + x["c"]:
                es_sci.ok_text(t, slug)
    ex = [es_sci.example(mtx(es_sci.esc(q)), [mtx(es_sci.esc(t)) for t in st], mtx(es_sci.esc(a))) for q, st, a in u["ex"]]
    body = es_sci.lesson([mtx(es_sci.esc(t)) for t in u["think"]], ex, [(mtx(es_sci.esc(a)), mtx(es_sci.esc(b))) for a, b in u["mist"]])
    body = body.replace("Respuesta: ", "Respuesta: ")
    fq = [(mtx(es_sci.esc(q)), mtx(es_sci.esc(a))) for q, a in u["faq"]]
    title, short, kb, ks, std, what = [mtx(u[k]) for k in ("title", "short", "kb", "ks", "std", "what")]
    for t in (title, short, kb, ks, std, what, body) + tuple(a + b for a, b in fq):
        es_sci.ok_text(t, slug)
        _leak(t, slug)
    for t in (title, short, kb, ks, what):
        assert "<" not in t, t
    d = u["dom"]
    if n <= 6:
        dom = DOM_P[d]
        code = "Fase %d, %s · Saberes y Pensamiento Científico" % (M.FASE[n], M.GRADE_SHORT[n] if n else "preescolar")
        tail = " (resumen de los contenidos de Saberes y Pensamiento Científico, Programa sintético de la Fase %d, SEP 2024)" % M.FASE[n]
        url = M.STD_URL[n]
    elif n <= 9:
        dom = DOM_S[n]
        code = "Fase 6, %s · Saberes y Pensamiento Científico (%s)" % (M.GRADE_SHORT[n], dom)
        tail = " (resumen de los contenidos de %s, Programa sintético de la Fase 6, SEP 2024)" % dom
        url = M.STD_URL[n]
    else:
        dom = DOM_B[d]
        code = "MCCEMS · Ciencias Naturales, Experimentales y Tecnología · %s" % gname
        tail = " (resumen de las progresiones de aprendizaje de la UAC «%s», MCCEMS, SEP 2023)" % gname
        url = MCC
    gshort = SHORTN.get(gslug, gname)
    if n <= 9:
        seo = "%s – Ciencias de %s: fichas con respuestas" % (short, gname)
        meta = "%s en Ciencias (%s): %s. 100 ejercicios resueltos en línea con explicaciones y una ficha para imprimir con respuestas." % (short, gname, what)
    else:
        seo = "%s – %s (bachillerato): fichas con respuestas" % (short, gshort)
        meta = "%s en %s (bachillerato): %s. 100 ejercicios resueltos en línea con explicaciones y una ficha para imprimir con respuestas." % (short, gshort, what)
    write_unit("mx", "science", gslug, {
        "slug": slug, "title": title, "seo_title": seo, "short_title": short, "domain": dom, "standard_code": code,
        "standard_url": url, "standard_text": std + tail, "meta_desc": meta, "key_big": kb, "key_sub": ks, "body_html": body,
        "faq": [{"q": q, "a": a} for q, a in fq], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


def units(gslug):
    return [es_unit(eg, s) for eg, s in BYSLUG[gslug][3]]


def main():
    g = sys.argv[1]
    only = sys.argv[2:]
    for i, (eg, s) in enumerate(BYSLUG[g][3]):
        if only and s not in only and str(i + 1) not in only:
            continue
        build(g, eg, s, i + 1)
        print("wrote", g, s)


if __name__ == "__main__":
    import mx_sci
    mx_sci.main()
