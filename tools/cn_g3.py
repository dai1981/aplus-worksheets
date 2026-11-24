# -*- coding: utf-8 -*-
"""
中国 三年级 数学（课标 2022 第二学段、人教版 三上・三下 の単元の順）。
台湾版の問題を adopt で简体字にして使い、倍的认识・位置与方向は自前（cn_mid）。
"""
import random
import cn_mid as M
import cn_low as L
from cn_common import run_grade, le, no, lesson

G = 3
S_NUM = "认识万以内的数和简单的小数、分数；掌握万以内的加减法、多位数乘一位数、两位数乘两位数、除数是一位数的除法，能进行估算"
S_QTY = "认识时、分、秒和年、月、日；认识长度单位毫米、分米、千米和质量单位吨；能用两步计算解决实际问题，理解“倍”的含义"
S_SHP = "认识长方形和正方形的特征，会计算它们的周长和面积；认识面积单位平方厘米、平方分米、平方米"
S_POS = "能根据给定的一个方向（东、南、西、北）辨认其余三个方向，能用东、南、西、北、东北、西北、东南、西南描述物体所在的方向"
S_DATA = "能用复式统计表整理数据，能根据统计表回答简单的问题"

UNITS = {}


def U(slug, **kw):
    UNITS[slug] = kw


def tw5(mod, n=(20, 20, 20, 20, 20)):
    return [("tw", mod, i, k) for i, k in enumerate(n)]


U("hours-minutes-seconds", sort=1, dom="Q", std=S_QTY, seed=93101, tw="gen_tw_math_g3_time",
  title="时、分、秒：时间单位和经过的时间", short="时、分、秒",
  meta="三年级数学“时、分、秒”练习题：时间单位的换算（1 时 ＝ 60 分，1 分 ＝ 60 秒）、时间的加减、再过多久是几时几分、经过多长时间、选合适的时间单位，100题在线练习，附可打印答案。",
  kb="1 时 ＝ 60 分，1 分 ＝ 60 秒", ks="算经过的时间：结束时刻 － 开始时刻；分不够减时，从时借 1 当 60 分。",
  faq=[("三年级的时间学什么？", "人教版三年级上册第一单元学秒和时间的简单计算；三年级下册学年、月、日和 24 时计时法。")],
  spec=lambda: [("时间单位的换算", [("tw", "gen_tw_math_g3_time", 0, 20)]),
                ("时间的加减", [("tw", "gen_tw_math_g3_time", 1, 20)]),
                ("再过多久是几时几分", [("tw", "gen_tw_math_g3_time", 2, 20)]),
                ("经过多长时间", [("tw", "gen_tw_math_g3_time", 3, 20)]),
                ("选合适的单位和解决问题", [("tw", "gen_tw_math_g3_time", 4, 20)])])

U("add-subtract-within-10000", sort=2, dom="N", std=S_NUM, seed=93102, tw="gen_tw_math_g3_add_subtract_within_10000",
  title="万以内的加法和减法", short="万以内的加减法",
  meta="三年级数学“万以内的加法和减法”练习题：三位数加三位数（进位）、四位数加法（多次进位）、退位减法、连续退位和中间有 0 的减法、解决问题，100题在线练习，附可打印答案。",
  kb="相同数位对齐，满十进一，不够减退一", ks="中间有 0 的减法：从百位退 1，十位变 9，个位得 10。",
  faq=[("503 － 278 怎么算？", "个位 3 不够减 8，十位是 0，要从百位退 1：百位变 4，十位变 9，个位变 13。13 － 8 ＝ 5，9 － 7 ＝ 2，4 － 2 ＝ 2，得 225。")],
  spec=lambda: [("三位数加法（进位）", [("tw", "gen_tw_math_g3_add_subtract_within_10000", 0, 20)]),
                ("四位数加法", [("tw", "gen_tw_math_g3_add_subtract_within_10000", 1, 20)]),
                ("退位减法", [("tw", "gen_tw_math_g3_add_subtract_within_10000", 2, 20)]),
                ("连续退位和中间有0", [("tw", "gen_tw_math_g3_add_subtract_within_10000", 3, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g3_add_subtract_within_10000", 4, 20)])])

U("measurement-units", sort=3, dom="Q", std=S_QTY, seed=93103, tw="gen_tw_math_g3_millimeters",
  title="测量：毫米、分米、千米和吨", short="测量",
  meta="三年级数学“测量”练习题：用毫米量长度、厘米和毫米的换算、千米和米的换算、吨和千克的换算、选合适的单位和解决问题，100题在线练习，附可打印答案。",
  kb="1 厘米 ＝ 10 毫米，1 千米 ＝ 1000 米，1 吨 ＝ 1000 千克", ks="1 分米 ＝ 10 厘米，1 米 ＝ 10 分米。很重的东西用吨作单位。",
  faq=[("长度单位之间是多少进率？", "1 千米 ＝ 1000 米，1 米 ＝ 10 分米，1 分米 ＝ 10 厘米，1 厘米 ＝ 10 毫米。")],
  spec=lambda: [("毫米", [("tw", "gen_tw_math_g3_millimeters", 0, 20)]),
                ("厘米和毫米的换算", [("tw", "gen_tw_math_g3_millimeters", 1, 10), ("tw", "gen_tw_math_g3_millimeters", 2, 10)]),
                ("千米和米", [("tw", "gen_tw_math_g4_kilometers", 1, 10), ("tw", "gen_tw_math_g4_kilometers", 3, 10)]),
                ("吨和千克", [("tw", "gen_tw_math_g5_metric_tons", 0, 10, no(".")), ("tw", "gen_tw_math_g5_metric_tons", 3, 10)]),
                ("选单位和解决问题", [("tw", "gen_tw_math_g3_millimeters", 4, 7), ("tw", "gen_tw_math_g4_kilometers", 0, 6), ("tw", "gen_tw_math_g5_metric_tons", 2, 7)])])

U("meaning-of-times", sort=4, dom="Q", std=S_QTY, seed=93104,
  title="倍的认识：几倍和求一个数的几倍", short="倍的认识",
  meta="三年级数学“倍的认识”练习题：看图说几倍、求一个数是另一个数的几倍、求一个数的几倍是多少、已知几倍求一份，100题在线练习，附可打印答案。",
  kb="把一个数看作 1 份，另一个数有这样的几份就是几倍", ks="求几倍用除法：12 ÷ 3 ＝ 4（倍）；求一个数的几倍用乘法：3 × 4 ＝ 12。",
  body=lesson(["比较两个数时，把较小的数看作 <b>1 份</b>，较大的数里有这样的几份，就是它的<b>几倍</b>。",
               "求一个数是另一个数的几倍，用<b>除法</b>：12 里面有几个 3？12 ÷ 3 ＝ 4，是 4 倍。",
               "求一个数的几倍是多少，用<b>乘法</b>：3 的 4 倍是 3 × 4 ＝ 12。"],
              [("红花 6 朵，黄花 18 朵。黄花是红花的几倍？", ["18 ÷ 6 ＝ 3"], "3 倍"),
               ("白兔 5 只，灰兔是白兔的 4 倍，灰兔几只？", ["5 × 4 ＝ 20"], "20 只")],
              [("求几倍用减法：18 － 6 ＝ 12", "几倍要看有几个 6：18 ÷ 6 ＝ 3。"),
               ("把“3 的 4 倍”算成 3 ＋ 4", "4 倍是 4 个 3：3 × 4 ＝ 12。"),
               ("单位写成“倍”和“只”混用", "求几倍时答案写“倍”，求数量时写“只、个”。")]),
  faq=[("“多几”和“几倍”有什么不同？", "“多几”是相差多少，用减法；“几倍”是一个数里有几个另一个数，用除法。"),
       ("倍的认识在哪个年级学？", "人教版三年级上册第五单元。")],
  spec=lambda: [("看图说几倍", [(M.times_pic(), 20)]),
                ("求几倍", [(M.times_find("howmany"), 20)]),
                ("求一个数的几倍", [(M.times_find("times"), 20)]),
                ("已知几倍求一份", [(M.times_find("part"), 20)]),
                ("综合练习", [(M.times_find("howmany"), 7), (M.times_find("times"), 7), (M.times_find("part"), 6)])])

U("multiply-by-one-digit", sort=5, dom="N", std=S_NUM, seed=93105, tw="gen_tw_math_g3_multiply_by_one_digit",
  title="多位数乘一位数", short="多位数乘一位数",
  meta="三年级数学“多位数乘一位数”练习题：整十整百数乘一位数、两位数乘一位数（进位）、三位数乘一位数、中间和末尾有 0 的乘法、解决问题，100题在线练习，附可打印答案。",
  kb="从个位乘起，哪一位满几十就向前一位进几", ks="进位的数要加在前一位的积上：38 × 4，8 × 4 ＝ 32 写 2 进 3。",
  faq=[("乘法竖式最常错在哪里？", "忘了加进位的数，或者把进位的数先加后乘。要先乘，再加上进位的数。")],
  spec=lambda: tw5("gen_tw_math_g3_multiply_by_one_digit") and [
      ("整十、整百数乘一位数", [("tw", "gen_tw_math_g3_multiply_by_one_digit", 0, 20)]),
      ("两位数乘一位数（一次进位）", [("tw", "gen_tw_math_g3_multiply_by_one_digit", 1, 20)]),
      ("两位数乘一位数（连续进位）", [("tw", "gen_tw_math_g3_multiply_by_one_digit", 2, 20)]),
      ("三位数乘一位数", [("tw", "gen_tw_math_g3_multiply_by_one_digit", 3, 20)]),
      ("解决问题", [("tw", "gen_tw_math_g3_multiply_by_one_digit", 4, 20)])])

U("rectangles-and-squares", sort=6, dom="G", std=S_SHP, seed=93106, tw="gen_tw_math_g3_squares_and_rectangles",
  title="长方形和正方形：特征和周长", short="长方形和正方形",
  meta="三年级数学“长方形和正方形”练习题：认识长方形和正方形、它们的特征、边长、周长、剪一剪拼一拼，100题在线练习，附可打印答案。",
  kb="长方形周长 ＝（长 ＋ 宽）× 2，正方形周长 ＝ 边长 × 4", ks="长方形对边相等、四个角都是直角；正方形四条边都相等。",
  faq=[("周长是什么？", "封闭图形一周的长度叫周长。长方形的周长是四条边的和：长 ＋ 宽 ＋ 长 ＋ 宽，也就是（长 ＋ 宽）× 2。")],
  spec=lambda: [("认识长方形和正方形", [("tw", "gen_tw_math_g3_squares_and_rectangles", 0, 20)]),
                ("长方形和正方形的特征", [("tw", "gen_tw_math_g3_squares_and_rectangles", 1, 20)]),
                ("边长", [("tw", "gen_tw_math_g3_squares_and_rectangles", 2, 20)]),
                ("周长", [("tw", "gen_tw_math_g3_squares_and_rectangles", 3, 20)]),
                ("剪一剪、拼一拼", [("tw", "gen_tw_math_g3_squares_and_rectangles", 4, 20)])])

U("fractions", sort=7, dom="N", std=S_NUM, seed=93107, tw="gen_tw_math_g3_fractions",
  title="分数的初步认识", short="分数的初步认识",
  meta="三年级数学“分数的初步认识”练习题：涂色部分是几分之几、几个几分之一、分数比大小、同分母分数的加减、解决问题，100题在线练习，附可打印答案。",
  kb="平均分成几份，取其中的几份，就是几分之几", ks="分母相同，分子大的分数大；同分母分数相加减，分母不变，分子相加减。",
  faq=[("为什么一定要“平均分”？", "只有每一份一样大，才能用分数表示。没有平均分的，不能说是几分之一。")],
  spec=lambda: [("涂色部分是几分之几", [("tw", "gen_tw_math_g3_fractions", 0, 20)]),
                ("几个几分之一", [("tw", "gen_tw_math_g3_fractions", 1, 20)]),
                ("分数比大小", [("tw", "gen_tw_math_g3_fractions", 2, 20)]),
                ("同分母分数的加减", [("tw", "gen_tw_math_g3_fractions", 3, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g3_fractions", 4, 20)])])

U("directions", sort=8, dom="T", std=S_POS, seed=93108,
  title="位置与方向：东、南、西、北", short="位置与方向",
  meta="三年级数学“位置与方向（一）”练习题：认识东南西北、看地图辨方向（上北下南、左西右东）、东北西北东南西南、方向的相对性、按路线走，100题在线练习，附可打印答案。",
  kb="地图上通常是上北下南、左西右东", ks="早上面对太阳是东，背后是西，左手是北，右手是南。",
  body=lesson(["早晨太阳从<b>东方</b>升起。面对太阳，背后是<b>西</b>，左手是<b>北</b>，右手是<b>南</b>。",
               "地图上通常按“<b>上北下南，左西右东</b>”来绘制。",
               "东和北之间是<b>东北</b>，西和北之间是<b>西北</b>，东和南之间是<b>东南</b>，西和南之间是<b>西南</b>。",
               "方向是相对的：A 在 B 的东面，B 就在 A 的西面。"],
              [("图书馆在学校的东北方向，学校在图书馆的哪个方向？", ["东北的相对方向是西南。"], "西南"),
               ("面向北，向右转后面向哪里？", ["北 → 东 → 南 → 西，按顺时针转一次。"], "东")],
              [("地图上把左边当成东", "地图通常左西右东。"),
               ("把“东北”说成“北东”", "中国习惯先说东、西，再说南、北：东北、西南。"),
               ("忘了方向是相对的", "A 在 B 的东面，B 在 A 的西面。")]),
  faq=[("孩子总记不住东南西北怎么办？", "在家里找出东方（早上太阳的方向），在墙上贴上“东南西北”，每天说一说哪个房间在哪个方向。"),
       ("三年级学几个方向？", "人教版三年级下册学东、南、西、北四个方向和东北、西北、东南、西南四个方向。")],
  spec=lambda: [("认识东南西北", [(M.dir_turn(), 20)]),
                ("看地图辨方向", [(M.dir_map(False), 20)]),
                ("八个方向", [(M.dir_map(True), 20)]),
                ("方向的相对性", [(M.dir_opp(), 20)]),
                ("路线和解决问题", [(M.dir_route(), 10), (M.dir_map(True), 10)])])

U("divide-by-one-digit", sort=9, dom="N", std=S_NUM, seed=93109, tw="gen_tw_math_g3_divide_by_one_digit",
  title="除数是一位数的除法", short="除数是一位数的除法",
  meta="三年级数学“除数是一位数的除法”练习题：口算除法、两位数除以一位数、三位数除以一位数、商中间和末尾有 0、有余数的除法和验算、解决问题，100题在线练习，附可打印答案。",
  kb="从高位除起，除到哪一位商就写在哪一位上", ks="哪一位不够商 1，就在那一位上写 0 占位。",
  faq=[("商中间什么时候写 0？", "除到某一位时，被除数这一位不够除，商这一位就写 0。例如 618 ÷ 6 ＝ 103，十位上 1 不够除 6，商写 0。")],
  spec=lambda: [("口算除法和两位数除以一位数", [("tw", "gen_tw_math_g3_divide_by_one_digit", 0, 20)]),
                ("有余数的除法", [("tw", "gen_tw_math_g3_divide_by_one_digit", 1, 20)]),
                ("三位数除以一位数", [("tw", "gen_tw_math_g3_divide_by_one_digit", 2, 20)]),
                ("商中间有 0 和余数", [("tw", "gen_tw_math_g3_divide_by_one_digit", 3, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g3_divide_by_one_digit", 4, 20)])])

U("tables", sort=10, dom="D", std=S_DATA, seed=93110, tw="gen_tw_math_g3_tables",
  title="复式统计表", short="复式统计表",
  meta="三年级数学“复式统计表”练习题：读单式统计表、单式表的计算、读复式统计表、复式表的合计、画“正”字记录，100题在线练习，附可打印答案。",
  kb="复式统计表把几个单式表合在一起", ks="先看表头：横着是哪一类，竖着是哪一类，再找交叉的格子。",
  faq=[("单式统计表和复式统计表有什么不同？", "单式表只统计一组数据；复式表把两组以上的数据放在一张表里，方便比较。")],
  spec=lambda: [("读单式统计表", [("tw", "gen_tw_math_g3_tables", 0, 20)]),
                ("单式表的计算", [("tw", "gen_tw_math_g3_tables", 1, 20)]),
                ("读复式统计表", [("tw", "gen_tw_math_g3_tables", 2, 20)]),
                ("复式表的合计", [("tw", "gen_tw_math_g3_tables", 3, 20)]),
                ("画“正”字和做表格", [("tw", "gen_tw_math_g3_tables", 4, 20)])])

U("two-digit-by-two-digit-multiplication", sort=11, dom="N", std=S_NUM, seed=93111, tw="gen_tw_math_g4_multi_digit_multiplication",
  title="两位数乘两位数", short="两位数乘两位数",
  meta="三年级数学“两位数乘两位数”练习题：口算乘法（整十数）、两位数乘两位数的笔算、末尾有 0 的乘法、估算和解决问题，100题在线练习，附可打印答案。",
  kb="先用个位乘，再用十位乘，最后相加", ks="24 × 13：24 × 3 ＝ 72，24 × 10 ＝ 240，72 ＋ 240 ＝ 312。",
  faq=[("用十位上的数去乘时，积的末位写在哪里？", "写在十位上，因为它表示几个十。个位上可以不写 0。")],
  spec=lambda: [("口算乘法", [(M.tens_mult(), 20)]),
                ("两位数乘两位数的笔算", [(M.two_by_two(None), 20)]),
                ("两位数乘两位数（进位）", [("tw", "gen_tw_math_g4_multi_digit_multiplication", 0, 20)]),
                ("估算", [(M.two_by_two_est(), 20)]),
                ("解决问题", [(M.two_by_two_story(), 20)])])

U("area", sort=12, dom="G", std=S_SHP, seed=93112, tw="gen_tw_math_g3_area",
  title="面积：平方厘米、长方形和正方形的面积", short="面积",
  meta="三年级数学“面积”练习题：数方格求面积、比较面积、面积单位、长方形和正方形的面积公式、面积和周长的区别、解决问题，100题在线练习，附可打印答案。",
  kb="长方形面积 ＝ 长 × 宽，正方形面积 ＝ 边长 × 边长", ks="1 平方米 ＝ 100 平方分米，1 平方分米 ＝ 100 平方厘米。",
  faq=[("面积和周长有什么不同？", "周长是一周的长度，单位是厘米、米；面积是平面的大小，单位是平方厘米、平方米。")],
  spec=lambda: [("数方格", [("tw", "gen_tw_math_g3_area", 0, 20)]),
                ("比较面积", [("tw", "gen_tw_math_g3_area", 1, 10), ("tw", "gen_tw_math_g3_area", 2, 10)]),
                ("长方形和正方形的面积", [("tw", "gen_tw_math_g3_area", 3, 10), ("tw", "gen_tw_math_g4_area_and_perimeter", 0, 10)]),
                ("面积单位", [("tw", "gen_tw_math_g4_area_and_perimeter", 3, 19), ("tw", "gen_tw_math_g3_area", 2, 1)]),
                ("解决问题", [("tw", "gen_tw_math_g3_area", 4, 10), ("tw", "gen_tw_math_g4_area_and_perimeter", 4, 10)])])

U("years-months-days", sort=13, dom="Q", std=S_QTY, seed=93113, tw="gen_tw_math_g2_years_months_and_days",
  title="年、月、日和24时计时法", short="年、月、日",
  meta="三年级数学“年、月、日”练习题：大月和小月、平年和闰年、年月日的换算、看日历、经过几天、24 时计时法，100题在线练习，附可打印答案。",
  kb="大月 31 天，小月 30 天，2 月平年 28 天、闰年 29 天", ks="24 时计时法：下午 3 时就是 15 时（3 ＋ 12）。",
  faq=[("怎么记大月和小月？", "可以用拳头记：凸起的指关节是大月（31 天），凹下去的是小月；或者背口诀“一三五七八十腊，三十一天永不差”。")],
  spec=lambda: [("大月和小月", [("tw", "gen_tw_math_g2_years_months_and_days", 0, 20)]),
                ("年、月、星期、日的换算", [("tw", "gen_tw_math_g2_years_months_and_days", 1, 20)]),
                ("看日历", [("tw", "gen_tw_math_g2_years_months_and_days", 2, 20)]),
                ("经过几天", [("tw", "gen_tw_math_g2_years_months_and_days", 3, 10), ("tw", "gen_tw_math_g2_years_months_and_days", 4, 10)]),
                ("24时计时法", [("tw", "gen_tw_math_g4_time", 0, 12), ("tw", "gen_tw_math_g4_time", 2, 8)])])

U("decimals", sort=14, dom="N", std=S_NUM, seed=93114, tw="gen_tw_math_g3_decimals",
  title="小数的初步认识", short="小数的初步认识",
  meta="三年级数学“小数的初步认识”练习题：认识 0.1 和一位小数、个位和十分位、小数比大小、一位小数的加减、解决问题，100题在线练习，附可打印答案。",
  kb="把 1 平均分成 10 份，1 份是 0.1", ks="小数相加减，小数点要对齐：4.2 ＋ 3.6 ＝ 7.8。",
  faq=[("小数和分数有什么关系？", "0.1 就是 1/10，0.3 就是 3/10。十分之几可以写成一位小数。")],
  spec=lambda: [("认识一位小数", [("tw", "gen_tw_math_g3_decimals", 0, 20)]),
                ("个位和十分位", [("tw", "gen_tw_math_g3_decimals", 1, 20)]),
                ("比大小", [("tw", "gen_tw_math_g3_decimals", 2, 20)]),
                ("一位小数的加减", [("tw", "gen_tw_math_g3_decimals", 3, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g3_decimals", 4, 15), (M.dec1_story(), 5)])])

U("estimation", sort=15, dom="N", std=S_NUM, seed=93115, tw="gen_tw_math_g3_estimation",
  title="估算：加减乘除的估算", short="估算",
  meta="三年级数学“估算”练习题：最接近的整十整百、估算加法和减法、估算乘法、生活中的估算（钱够不够），100题在线练习，附可打印答案。",
  kb="先把数看成接近的整十、整百数，再算", ks="36 × 9 大约是 40 × 9 ＝ 360；估算时说“大约”。",
  faq=[("估算的结果是唯一的吗？", "不一定。可以估成整十，也可以估成整百，只要合理就行。判断“够不够”时，要想一想估大了还是估小了。")],
  spec=lambda: [("最接近的整十、整百", [("tw", "gen_tw_math_g3_estimation", 0, 20)]),
                ("估算加法", [("tw", "gen_tw_math_g3_estimation", 1, 20)]),
                ("估算减法", [("tw", "gen_tw_math_g3_estimation", 2, 20)]),
                ("估算乘法", [("tw", "gen_tw_math_g3_estimation", 3, 20)]),
                ("生活中的估算", [("tw", "gen_tw_math_g3_estimation", 4, 18), ("tw", "gen_tw_math_g3_estimation", 3, 0), (M.two_by_two_est(), 2)])])

U("two-step-problems", sort=16, dom="Q", std=S_QTY, seed=93116, tw="gen_tw_math_g3_two_step_word_problems",
  title="解决问题：两步计算", short="两步计算的解决问题",
  meta="三年级数学“两步计算的解决问题”练习题：连乘、先加再除、先减再除、先除再加、想好第一步算什么，100题在线练习，附可打印答案。",
  kb="先想要求的问题需要知道什么，再找第一步", ks="可以分步列式，也可以列综合算式；有需要先算的加减要加小括号。",
  faq=[("两步计算的问题怎么想？", "从问题往回想：要求“每组几颗”，就要先知道“一共有几颗”。先算出这个中间问题，再算最后的答案。")],
  spec=lambda: [("连乘", [("tw", "gen_tw_math_g3_two_step_word_problems", 0, 20)]),
                ("先加再除", [("tw", "gen_tw_math_g3_two_step_word_problems", 1, 20)]),
                ("先减再除", [("tw", "gen_tw_math_g3_two_step_word_problems", 2, 20)]),
                ("先除再加和买东西", [("tw", "gen_tw_math_g3_two_step_word_problems", 3, 20)]),
                ("想好第一步", [("tw", "gen_tw_math_g3_two_step_word_problems", 4, 20)])])

if __name__ == "__main__":
    import sys
    run_grade(G, UNITS, lambda r: (M.setup(r), L.setup(random.Random(r.random()))), sys.argv[1:] or None)
