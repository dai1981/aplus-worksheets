# -*- coding: utf-8 -*-
"""
中国（义务教育数学课程标准 2022年版、人教版の単元の順）の単元生成の共通部品。
・文は简体字・大陆の用語（厘米、米、千米、千克、克、吨、升、毫升、元角分、竖式、余数、条形统计图）
・数は 4 けたまでそのまま、5 けた以上もそのまま（中国の教科書は区切らない。大きい数は「万」「亿」を使う）
・多くの問題は台湾版の生成スクリプトの問題を作り直して使う：
    adopt("gen_tw_math_g3_fractions", seed) → その単元の sets・body・faq（简体字に変換済み）
  モジュールの R を新しい seed に入れ替えて main() を呼び、make_unit を横取りする（台湾版と同じ問題にならない）
・cn(s) で繁體→简体（OpenCC tw2sp）＋大陆の用語に直す。台湾の地名・新台幣などが残る問題は落とす
"""
import importlib
import random
import re
import sys

import opencc
from ws_common import fig, svg_wrap, text, line, balance, write_unit, fr, GREEN, FILL, GRAY, INK, RED, BLUE  # noqa: F401

UPDATED = "2026-11-25"
STD_URL = "http://www.moe.gov.cn/srcsite/A26/s8001/202204/t20220420_619921.html"
STD_NAME = "义务教育数学课程标准（2022年版）"
GRADE_ZH = {1: "一年级", 2: "二年级", 3: "三年级", 4: "四年级", 5: "五年级", 6: "六年级"}
STAGE = {1: "第一学段", 2: "第一学段", 3: "第二学段", 4: "第二学段", 5: "第三学段", 6: "第三学段"}
# 课标の主題（standard_code の後半と domain）
DOMAIN = {"N": "数与运算", "Q": "数量关系", "G": "图形的认识与测量", "T": "图形的位置与运动", "D": "统计与概率"}
DOMAIN_LOW = {"G": "图形的认识与测量", "D": "数据分类"}          # 第一学段の呼び方

_T2S = opencc.OpenCC("tw2sp")

# 台湾の名前 → 大陆でよく使う名前（教科書の子どもの名前）
NAMES = {"小美": "小红", "小芳": "小芳", "怡君": "丽丽", "佳穎": "佳佳", "雅婷": "婷婷", "心怡": "欣欣", "詩涵": "诗涵",
         "欣妤": "小雨", "宜蓁": "小玲", "品妍": "悦悦", "小明": "小明", "小華": "小华", "志明": "小刚", "家豪": "浩浩",
         "俊宏": "小军", "冠宇": "天天", "宇翔": "小宇", "柏翰": "明明", "承恩": "小东", "子軒": "子轩"}

# 简体字にしたあとで直す語（長いものから）
TERMS = [
    ("平方公分", "平方厘米"), ("立方公分", "立方厘米"), ("平方公尺", "平方米"), ("立方公尺", "立方米"), ("平方公里", "平方千米"),
    ("公分", "厘米"), ("公尺", "米"), ("公里", "千米"), ("公斤", "千克"), ("公克", "克"), ("公吨", "吨"), ("公升", "升"),
    ("公顷", "公顷"), ("公寸", "分米"), ("正三角形", "等边三角形"), ("线对称", "轴对称"), ("英文本母", "英文字母"), ("下面立体的前视图", "下面的物体从正面看到的形状"), ("下面立体的上视图", "下面的物体从上面看到的形状"), ("下面立体的右视图", "下面的物体从右面看到的形状"), ("前视图", "从正面看到的形状"), ("上视图", "从上面看到的形状"), ("右视图", "从右面看到的形状"), ("下面立体", "下面的物体"), ("解比例式", "解比例"), ("比例式", "比例"), ("它的从正面", "它从正面"), ("它的从上面", "它从上面"), ("它的从右面", "它从右面"), ("直式", "竖式"), ("数线", "数轴"), ("国字", "汉字"), ("长条图", "条形统计图"), ("折线图", "折线统计图"),
    ("圆形图", "扇形统计图"), ("并式", "综合算式"), ("概数", "近似数"), ("无条件进入法", "进一法"), ("无条件舍去法", "去尾法"),
    ("等值分数", "大小相等的分数"), ("百分率", "百分数"), ("学习单", "练习"), ("长针", "分针"), ("短针", "时针"), ("的在线", "的线上"), ("圆周长", "周长"), ("纪录", "记录"), ("正方体的边长", "正方体的棱长"),
    ("月历", "日历"), ("钟面面", "钟面"), ("十格板", "十格图"), ("积木塔", "小方块塔"), ("小朋友", "小朋友"), ("国语", "语文"), ("公车", "公交车"),
    ("捷运", "地铁"), ("便利商店", "便利店"), ("脚踏车", "自行车"), ("机车", "摩托车"), ("凤梨", "菠萝"), ("芭乐", "番石榴"),
    ("钮扣", "纽扣"), ("铅笔盒", "铅笔盒"), ("原子笔", "圆珠笔"), ("冰淇淋", "冰激凌"), ("影印", "复印"), ("列印", "打印"),
    ("同学们", "同学们"), ("班级", "班级"), ("颗苹果", "个苹果"), ("颗球", "个球"), ("颗纽扣", "个纽扣"),
    ("「", "“"), ("」", "”"), ("『", "‘"), ("』", "’"), ("课纲", "课标"), ("国小", "小学"), ("国中", "初中"),
    ("九九乘法表", "乘法口诀表"), ("九九乘法", "乘法口诀"), ("九九", "乘法口诀"), ("小时制", "时计时法"), ("12 时计时法", "12 时计时法"), ("撲满", "存钱罐"), ("扑满", "存钱罐"), ("里长", "社区"),
]
# これが残る問題は使わない（台湾の地名・お金・制度）
LEAKS = ["台湾", "台北", "台中", "台南", "高雄", "新竹", "基隆", "花莲", "台东", "宜兰", "嘉义", "屏东", "桃园", "新台币",
         "台币", "里民", "公亩", "500元钞", "1000元钞", "50元硬币", "10元硬币", "5元硬币", "1000 元钞", "500 元钞", "50 元硬币", "10 元硬币", "5 元硬币",
         "阿里山", "日月潭", "垦丁", "夜市", "珍珠奶茶", "全联", "悠游卡", "国历", "民国"]


# 简体字にする前に直す語（OpenCC が「線上」を「在线」にするなど）
PRE = [("方程式", "方程"), ("尾巴有 0", "末尾有 0"), ("尾巴的 0", "末尾的 0"), ("尾巴", "末尾"), ("數線", "数轴"), ("時鐘的鐘面", "钟面"), ("時鐘", "钟表"), ("鐘面", "钟面"), ("鉛筆盒", "文具盒"), ("枝鉛筆", "支铅笔"),
       ("枝筆", "支笔"), ("哪一枝", "哪一支"), ("幾枝", "几支"), ("一枝", "一支"), ("每枝", "每支"), ("兩枝", "两支")]


def cn(s):
    """繁體（台湾）→ 简体（大陆の用語）"""
    if not s:
        return s
    for a, b in NAMES.items():
        s = s.replace(a, b)
    for a, b in PRE:
        s = s.replace(a, b)
    s = re.sub(r"([\dxyn]+)( ?)枝", r"\1\2支", s)
    s = re.sub(r"(?<=\d),(?=\d{3})", "", s)       # 12,500 → 12500（中国の教科書は区切らない）
    parts = re.split(r"(<[^>]+>)", s)          # タグの中（class 名など）は変換しない。aria-label だけ変換する
    out = []
    for p in parts:
        if p.startswith("<"):
            p = re.sub(r"aria-label='([^']*)'", lambda m: "aria-label='%s'" % _terms(_T2S.convert(m.group(1))), p)
            out.append(p)
        else:
            out.append(_terms(_T2S.convert(p)))
    return "".join(out)


def _terms(s):
    for a, b in TERMS:
        s = s.replace(a, b)
    s = re.sub(r"(秒|分|时)速(是|为)? ?(\d+(?:\.\d+)?) ?(千米|米)", lambda m: "速度%s %s %s/%s" % (m.group(2) or "", m.group(3), m.group(4), m.group(1)), s)
    s = s.replace("秒速", "速度（每秒）").replace("分速", "速度（每分）").replace("时速", "速度（每时）")
    s = re.sub(r"边长( ?[\d.]+ ?(?:厘米|分米|米)?)的正方体", r"棱长\1的正方体", s)
    s = re.sub(r"正比(?!例)", "正比例", s)
    s = re.sub(r"反比(?!例)", "反比例", s)
    s = re.sub(r"([一二三四五六])年([甲乙丙丁])班", lambda m: "%s（%d）班" % (m.group(1), "甲乙丙丁".index(m.group(2)) + 1), s)
    return s


FAQ_LEAKS = ["108", "课标", "课纲", "N-", "S-", "R-", "D-", "台湾", "国小", "国中", "学习单"]


def faq_ok(f):
    return not any(w in f["q"] + f["a"] for w in FAQ_LEAKS + LEAKS)


def leak(s):
    t = re.sub(r"<[^>]+>", " ", s)
    return any(w in t for w in LEAKS)


def cn_item(it):
    it = dict(it)
    it["q"] = cn(it["q"])
    it["e"] = cn(it["e"])
    it["c"] = [cn(c) for c in it["c"]]
    return it


def _norm(c):
    c = re.sub(r"<span class='fn'>([^<]*)</span><span class='fd'>([^<]*)</span>", r"\1/\2", c)
    c = re.sub(r"<[^>]+>", "", c)
    c = re.sub(r"(\d+\.\d*?)0+(?!\d)", r"\1", c)
    return re.sub(r"(\d)\.(?!\d)", r"\1", c).strip()


def ok_item(it):
    blob = it["q"] + " " + " ".join(it["c"]) + " " + it["e"]
    return not leak(blob) and len(set(it["c"])) == 4 and len({_norm(c) for c in it["c"]}) == 4


# ------------------------------------------------------------------ 台湾版の単元を作り直して使う
_CACHE = {}


def adopt(modname, seed):
    """台湾版の生成スクリプトの main() を新しい乱数で動かし、make_unit に渡るもの（sets・body・faq など）を返す"""
    key = (modname, seed)
    if key in _CACHE:
        return _CACHE[key]
    if modname in sys.modules:
        mod = importlib.reload(sys.modules[modname])
    else:
        mod = importlib.import_module(modname)
    rnd = random.Random(seed)
    if hasattr(mod, "R"):
        mod.R = rnd
    if hasattr(mod, "NM"):
        mod.NM = mod.Names(rnd) if hasattr(mod, "Names") else mod.NM
    got = {}

    def grab(R, grade, slug, code, std_text, title, seo_title, short_title, meta_desc, key_big, key_sub, body_html, faq, sets, sort):
        got.update(sets=[(cn(t), [cn_item(it) for it in items]) for t, items in sets], body=cn(body_html),
                   faq=[{"q": cn(f["q"]), "a": cn(f["a"])} for f in faq], title=cn(title), short=cn(short_title))
    mod.make_unit = grab
    mod.main()
    _CACHE[key] = got
    return got


def items_of(got, idx, n=20, keep=None):
    """adopt した単元の idx 番目のセットから、使える問題を n 問まで"""
    out = []
    for it in got["sets"][idx][1]:
        if ok_item(it) and (keep is None or keep(it)):
            out.append(it)
    return out[:n]


# ------------------------------------------------------------------ 自前の問題
GIRLS = ["小红", "丽丽", "小芳", "婷婷", "欣欣", "小雨", "悦悦", "小玲", "笑笑", "佳佳"]
BOYS = ["小明", "小华", "小刚", "浩浩", "小军", "天天", "小宇", "明明", "乐乐", "子轩"]


class Names:
    def __init__(self, rnd):
        self.pool = GIRLS + BOYS
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        n = self.pool[self.i % len(self.pool)]
        self.i += 1
        return n


def num(n):
    return str(int(n))


def dnum(v, places=2):
    s = ("%." + str(places) + "f") % v
    return s.rstrip("0").rstrip(".") if "." in s else s


def mcq(q, correct, cands, e):
    """4 択。誤答が 3 つそろわないと None（作り直す）"""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or c.startswith("-") or c.startswith("−"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3:
        return None
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def pick(rnd, maker, n, seen, tries=6000):
    out = []
    for _ in range(tries):
        try:
            it = maker()
        except (ValueError, AssertionError, ZeroDivisionError, IndexError):
            it = None
        if it is None or it["q"] in seen or not ok_item(it):
            continue
        seen.add(it["q"])
        out.append(it)
        if len(out) == n:
            return out
    raise AssertionError("could not make %d unique questions (%d) %s" % (n, len(out), getattr(maker, "__name__", "")))


def table(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return ("<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead>"
            "<tbody>%s</tbody></table></div>" % (h, b))


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>例题</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>答：%s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist):
    """body_html：怎么想 → 例题 → 常见错误"""
    h = "<h2>怎么想</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += "".join(example(*e) for e in examples)
    h += "<h2>常见错误</h2>" + table(["常见错误", "正确的想法"], mist)
    return h


def plain(t):
    t = re.sub(r"<span class='fr'><span class='fn'>(.*?)</span><span class='fd'>([^<]*)</span></span>",
               lambda m: m.group(1) + "/" + m.group(2), t)
    assert "<" not in t, t
    return t


def unit(g, slug, sort, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, seed):
    """sets: [(セット名, [items])] × 5（各 20 問）。dom は DOMAIN のキー"""
    rnd = random.Random(seed)
    sets = [{"title": t, "items": list(items)} for t, items in sets]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (slug, s["title"], len(s["items"]))
        for it in s["items"]:
            assert it["q"] not in seen, ("duplicate", slug, it["q"][:80])
            seen.add(it["q"])
            assert ok_item(it), (slug, it["q"][:80], it["c"])
            assert not re.search(r"[們個這們為來說時對還會與無並後從應於將從學數點麼裡邊們樣條鐘幾讀寫錢買賣張隻開關]", re.sub(r"<[^>]+>", "", it["q"] + "".join(it["c"]) + it["e"])), ("traditional", slug, it["q"][:80])
    balance(sets, rnd)
    title, short, meta, key_big, key_sub = map(plain, (title, short, meta, key_big, key_sub))
    dname = (DOMAIN_LOW.get(dom) if g <= 2 else None) or DOMAIN[dom]
    write_unit("cn", "math", "grade-%d" % g, {
        "slug": slug, "title": title,
        "seo_title": "%s｜%s数学练习题（附答案）" % (title, GRADE_ZH[g]),
        "short_title": short, "domain": dname, "standard_code": "%s · %s" % (STAGE[g], dname),
        "standard_url": STD_URL, "standard_text": std + "（课标内容要求摘要）", "meta_desc": meta,
        "key_big": key_big, "key_sub": key_sub, "body_html": body,
        "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


def build_sets(spec, seed):
    """spec: [(セット名, [部品])]。部品は (maker, 数) か ("tw", 台湾版のモジュール, セット番号, 数[, keep])"""
    rnd = random.Random(seed)
    seen = set()
    out = []
    for title, parts in spec:
        items = []
        for p in parts:
            if p[0] == "tw":
                _, mod, idx, n = p[:4]
                keep = p[4] if len(p) > 4 else None
                got, qs = [], set()
                for it in items_of(adopt(mod, seed), idx, 99, keep):
                    if it["q"] not in seen and it["q"] not in qs:
                        qs.add(it["q"])
                        got.append(it)
                if n is None:                       # None：20 問になるまで
                    n = 20 - len(items)
                if n < 0:                       # 負の数：最大 |n| 問まで（足りない分は後の部品で埋める）
                    n = min(-n, len(got))
                assert len(got) >= n, ("not enough", mod, idx, len(got), n)
                got = got[:n]
                seen.update(it["q"] for it in got)
                items += got
            else:
                maker, n = p
                if n is None:                       # None：20 問になるまで埋める
                    n = 20 - len(items)
                items += pick(rnd, maker, n, seen) if n > 0 else []
        out.append((title, items))
    return out


def tw_body(mod, seed):
    b = adopt(mod, seed)["body"]
    assert not leak(b), (mod, "leak in body")
    return b


def tw_faq(mod, seed):
    return [(f["q"], f["a"]) for f in adopt(mod, seed)["faq"] if faq_ok(f)]


def le(n):
    """keep: 問題文と選択肢（図を除く）の数がすべて n 以下"""
    def f(it):
        t = re.sub(r"<svg.*?</svg>", "", it["q"] + " " + " ".join(it["c"]), flags=re.S)
        t = re.sub(r"<[^>]+>", " ", t)
        return all(int(x) <= n for x in re.findall(r"\d+", t))
    return f


def no(*words):
    """keep: 語を含まない"""
    def f(it):
        t = it["q"] + " ".join(it["c"]) + it["e"]
        return not any(w in t for w in words)
    return f


def both(*fs):
    return lambda it: all(f(it) for f in fs)


def run_grade(g, UNITS, setup=None, only=None):
    for slug in (only or list(UNITS)):
        u = UNITS[slug]
        if setup:
            setup(random.Random(u["seed"]))
        src = u.get("tw")
        body = u.get("body") or tw_body(src, u["seed"])
        faq = list(u.get("faq", [])) + (tw_faq(src, u["seed"]) if src and not u.get("body") else [])
        sets = build_sets(u["spec"](), u["seed"])
        unit(g, slug, u["sort"], u["dom"], u["std"], u["title"], u["short"], u["meta"], u["kb"], u["ks"],
             body, faq[:4], sets, u["seed"])
