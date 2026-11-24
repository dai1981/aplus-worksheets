# -*- coding: utf-8 -*-
"""
中国 二年级 数学（课标 2022 第一学段、人教版 二上・二下 の単元の順）。
台湾版（gen_tw_math_g2_* / g3_*）の問題を adopt で简体字にして使い、竖式・混合运算は自前（cn_mid）。
"""
import random
import cn_mid as M
import cn_low as L
from cn_common import run_grade, le, no, lesson

G = 2
S_NUM = "认识万以内的数，理解数位的含义；能计算 100 以内的加减法和简单的万以内加减法；理解乘法和除法的意义，掌握表内乘除法，会算有余数的除法"
S_QTY = "能在具体情境中理解四则运算的意义，会用两步计算解决简单的实际问题；认识时、分、秒，认识克和千克"
S_SHP = "认识长度单位米、厘米，能估测和测量物体的长度；认识角和直角"
S_DATA = "能根据给定的标准或者自选的标准对数据进行分类，用简单的统计表整理数据"

UNITS = {}


def U(slug, **kw):
    UNITS[slug] = kw


U("centimeters-and-meters", sort=1, dom="G", std=S_SHP, seed=92101, tw="gen_tw_math_g2_centimeters_and_meters",
  title="长度单位：厘米和米", short="长度单位",
  meta="二年级数学“长度单位”练习题：用尺子量长度、用厘米还是米、1 米 ＝ 100 厘米、长度的加减、解决问题，100题在线练习，附可打印答案。",
  kb="1 米 ＝ 100 厘米", ks="量长度时，把尺子的 0 刻度对准物体的一端。短的用厘米，长的用米。",
  faq=[("二年级要学哪些长度单位？", "人教版二年级上册学厘米和米，三年级上册再学毫米、分米和千米。")],
  spec=lambda: [("用尺子量", [("tw", "gen_tw_math_g2_centimeters_and_meters", 0, 20)]),
                ("用厘米还是米", [("tw", "gen_tw_math_g2_centimeters_and_meters", 1, 20)]),
                ("米和厘米的换算", [("tw", "gen_tw_math_g2_centimeters_and_meters", 2, 20)]),
                ("长度的加减", [("tw", "gen_tw_math_g2_centimeters_and_meters", 3, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g2_centimeters_and_meters", 4, 20)])])

U("written-addition-and-subtraction-within-100", sort=2, dom="N", std=S_NUM, seed=92102, tw="gen_tw_math_g2_column_addition",
  title="100以内的加法和减法（二）：笔算", short="100以内的笔算",
  meta="二年级数学“100以内的加法和减法（二）”练习题：两位数加两位数（不进位、进位）、两位数减两位数（不退位、退位）、连加连减、解决问题，100题在线练习，附可打印答案。",
  kb="相同数位对齐，从个位算起", ks="个位满十向十位进 1；个位不够减，从十位退 1 当 10。",
  faq=[("笔算最容易错在哪里？", "进位时忘了加上进的 1，退位时忘了十位要减去 1。可以在竖式里写个小点或小 1 提醒自己。")],
  spec=lambda: [("不进位加法", [(M.vert("＋", 2, 2, False, mx=100), 20)]),
                ("进位加法", [(M.vert("＋", 2, 2, True, mx=100), 16), ("tw", "gen_tw_math_g2_column_addition", 1, 4, le(100))]),
                ("不退位减法", [(M.vert("－", 2, 2, False), 20)]),
                ("退位减法", [(M.vert("－", 2, 2, True), 10), ("tw", "gen_tw_math_g2_column_subtraction", 1, 10)]),
                ("连加连减和解决问题", [(M.chain("add"), 5), (M.chain("sub"), 5), (M.vert("＋", 2, 2, None, True, mx=100), 5), (M.vert("－", 2, 2, None, True), 5)])])

U("angles", sort=3, dom="G", std=S_SHP, seed=92103, tw="gen_tw_math_g3_angles",
  title="角的初步认识：直角、锐角、钝角", short="角的初步认识",
  meta="二年级数学“角的初步认识”练习题：角的顶点和边、直角、比直角大或小的角、比较角的大小、图形和钟面上的直角、生活中的角，100题在线练习，附可打印答案。",
  kb="角的大小看两条边张开的大小", ks="角有一个顶点、两条边。用三角尺的直角比一比，比直角大的是钝角，小的是锐角。",
  faq=[("角的大小和边的长短有关吗？", "没有关系。角的大小只看两条边张开得大还是小，边画得再长，角也不会变大。")],
  spec=lambda: [("角的顶点和边", [("tw", "gen_tw_math_g3_angles", 0, 20)]),
                ("直角、锐角、钝角", [("tw", "gen_tw_math_g3_angles", 1, 20)]),
                ("比较角的大小", [("tw", "gen_tw_math_g3_angles", 2, 20)]),
                ("图形和钟面上的直角", [("tw", "gen_tw_math_g3_angles", 3, 20)]),
                ("生活中的角", [("tw", "gen_tw_math_g3_angles", 4, 20)])])

U("meaning-of-multiplication", sort=4, dom="N", std=S_NUM, seed=92104, tw="gen_tw_math_g2_meaning_of_multiplication",
  title="乘法的初步认识：几个几", short="乘法的初步认识",
  meta="二年级数学“乘法的初步认识”练习题：几个几、相同加数连加改写成乘法、点子图和排列、几倍、生活中的乘法，100题在线练习，附可打印答案。",
  kb="几个相同的数相加，用乘法算", ks="3 个 4 相加：4 ＋ 4 ＋ 4 ＝ 12，写成 3 × 4 ＝ 12 或 4 × 3 ＝ 12。",
  body=lesson(["几个<b>相同的数</b>相加，可以用乘法表示。4 ＋ 4 ＋ 4 是 3 个 4，写成 <b>3 × 4 ＝ 12</b> 或 <b>4 × 3 ＝ 12</b>。",
               "“×”读作“乘”，3 × 4 读作“3 乘 4”。乘号前后的数叫<b>乘数</b>，得数叫<b>积</b>。",
               "<b>几倍</b>：5 的 3 倍就是 3 个 5，5 × 3 ＝ 15。"],
              [("每排 6 张椅子，有 5 排，一共几张？", ["5 个 6：6 × 5 ＝ 30 或 5 × 6 ＝ 30"], "30 张"),
               ("4 的 2 倍是多少？", ["2 个 4：4 × 2 ＝ 8"], "8")],
              [("3 个 4 写成 3 ＋ 4", "相同加数连加才用乘法：3 × 4 或 4 × 3。"),
               ("不同的数相加也写成乘法", "3 ＋ 4 ＋ 5 加数不同，不能直接写成乘法。"),
               ("5 的 3 倍算成 5 ＋ 3", "3 倍是 3 个 5：5 × 3 ＝ 15。")]),
  faq=[("3 × 4 和 4 × 3 一样吗？", "得数一样，都是 12。3 个 4 可以写成 3 × 4，也可以写成 4 × 3。"),
       ("什么时候用乘法？", "求几个相同加数的和时用乘法，比连加简便。")],
  spec=lambda: [("几个几", [("tw", "gen_tw_math_g2_meaning_of_multiplication", 0, 20)]),
                ("加法和乘法", [("tw", "gen_tw_math_g2_meaning_of_multiplication", 1, 20)]),
                ("排列", [("tw", "gen_tw_math_g2_meaning_of_multiplication", 2, 20)]),
                ("几倍", [("tw", "gen_tw_math_g2_meaning_of_multiplication", 3, 20)]),
                ("生活中的乘法", [("tw", "gen_tw_math_g2_meaning_of_multiplication", 4, 20)])])

U("multiplication-tables", sort=5, dom="N", std=S_NUM, seed=92105, tw="gen_tw_math_g2_multiplication_tables",
  title="表内乘法：乘法口诀", short="表内乘法",
  meta="二年级数学“表内乘法”练习题：2、5、10 的乘法口诀，3、4、6、7、8、9 的乘法口诀，口诀填空和应用，100题在线练习，附可打印答案。",
  kb="熟记乘法口诀，一句口诀算两道乘法", ks="“三七二十一”：3 × 7 ＝ 21，7 × 3 ＝ 21。",
  faq=[("乘法口诀要背到什么程度？", "能脱口而出。可以从 2、5 的口诀开始，再学 3、4、6，最后是 7、8、9。")],
  spec=lambda: [("2、5、10 的口诀", [("tw", "gen_tw_math_g2_multiplication_tables", 0, 20)]),
                ("3、4 的口诀", [("tw", "gen_tw_math_g2_multiplication_tables", 1, 20)]),
                ("6、7 的口诀", [("tw", "gen_tw_math_g2_multiplication_tables", 2, 20)]),
                ("8、9 的口诀和 □", [("tw", "gen_tw_math_g2_multiplication_tables", 3, 20)]),
                ("乘法的应用", [("tw", "gen_tw_math_g2_multiplication_tables", 4, 20)])])

U("telling-time", sort=6, dom="Q", std=S_QTY, seed=92106, tw="gen_tw_math_g2_telling_time",
  title="认识时间：几时几分", short="认识时间",
  meta="二年级数学“认识时间”练习题：时针和分针、读几时几分（5 分、1 分）、经过几小时、再过几小时，100题在线练习，附可打印答案。",
  kb="1 时 ＝ 60 分，分针走一小格是 1 分", ks="先看时针过了几，再看分针走了几个小格。",
  faq=[("二年级的时间学到哪里？", "人教版二年级上册学几时几分，三年级上册学秒和时间的计算。")],
  spec=lambda: [("时针和分针", [("tw", "gen_tw_math_g2_telling_time", 0, 17), ("tw", "gen_tw_math_g2_telling_time", 4, 3)]),
                ("几时几分（5 分）", [("tw", "gen_tw_math_g2_telling_time", 1, 20)]),
                ("几时几分（1 分）", [("tw", "gen_tw_math_g2_telling_time", 2, 20)]),
                ("经过几小时", [("tw", "gen_tw_math_g2_telling_time", 3, 20)]),
                ("再过几小时", [("tw", "gen_tw_math_g2_telling_time", 4, 17), (L.t_after(), 3)])])

U("data-collection", sort=7, dom="D", std=S_DATA, seed=92107, tw="gen_tw_math_g2_sorting_and_tables",
  title="数据收集整理", short="数据收集整理",
  meta="二年级数学“数据收集整理”练习题：按颜色和形状分类、分类后再分类、分类的标准、看统计表、用表回答问题，100题在线练习，附可打印答案。",
  kb="先分类，再数一数，填进统计表", ks="可以用画“正”字的方法记录，一个“正”字表示 5。",
  faq=[("什么是画“正”字记录？", "调查时每数到一个就画一笔，一个“正”字有 5 笔，表示 5 个，最后数一数有几个“正”字。")],
  spec=lambda: [("按颜色、形状分", [("tw", "gen_tw_math_g2_sorting_and_tables", 0, 20)]),
                ("分类中再分类", [("tw", "gen_tw_math_g2_sorting_and_tables", 1, 20)]),
                ("分类的标准", [("tw", "gen_tw_math_g2_sorting_and_tables", 2, 20)]),
                ("看统计表", [("tw", "gen_tw_math_g2_sorting_and_tables", 3, 20)]),
                ("用表回答问题", [("tw", "gen_tw_math_g2_sorting_and_tables", 4, 20)])])

U("division-within-tables", sort=8, dom="N", std=S_NUM, seed=92108, tw="gen_tw_math_g2_sharing_and_grouping",
  title="表内除法：平均分和用口诀求商", short="表内除法",
  meta="二年级数学“表内除法”练习题：平均分、每几个一份、除法的意义、用乘法口诀求商、解决问题，100题在线练习，附可打印答案。",
  kb="平均分用除法，用乘法口诀求商", ks="12 ÷ 3：想“三（四）十二”，商是 4。",
  faq=[("除法和乘法有什么关系？", "除法是乘法的逆运算。求 24 ÷ 6，就想 6 乘几等于 24，用口诀“四六二十四”，商是 4。")],
  spec=lambda: [("每几个一份", [("tw", "gen_tw_math_g2_sharing_and_grouping", 0, 20)]),
                ("平均分给几人", [("tw", "gen_tw_math_g2_sharing_and_grouping", 1, 20)]),
                ("除法的意义", [("tw", "gen_tw_math_g3_division", 0, 20)]),
                ("用口诀求商", [("tw", "gen_tw_math_g3_division", 1, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g2_sharing_and_grouping", 2, 10), ("tw", "gen_tw_math_g2_sharing_and_grouping", 4, 10, no("剩", "余"))])])

U("mixed-operations", sort=9, dom="Q", std=S_QTY, seed=92109,
  title="混合运算：先乘除后加减、小括号", short="混合运算",
  meta="二年级数学“混合运算”练习题：同级运算从左往右、先乘除后加减、带小括号的算式、合成综合算式、两步计算的解决问题，100题在线练习，附可打印答案。",
  kb="先乘除、后加减，有括号先算括号里", ks="同一级运算从左往右算：40 － 12 ＋ 8 先算 40 － 12。",
  body=lesson(["只有加减法，或只有乘除法（同一级运算），要<b>从左往右</b>按顺序算。",
               "既有乘除法又有加减法，要<b>先算乘除，后算加减</b>。",
               "有小括号的，要<b>先算小括号里面的</b>。",
               "解决两步计算的问题时，可以先分步列式，再合成一个综合算式。"],
              [("30 ＋ 5 × 4", ["先算 5 × 4 ＝ 20", "再算 30 ＋ 20 ＝ 50"], "50"),
               ("（20 － 8）× 3", ["先算括号里 20 － 8 ＝ 12", "再算 12 × 3 ＝ 36"], "36")],
              [("30 ＋ 5 × 4 先算 30 ＋ 5", "先乘后加：30 ＋ 20 ＝ 50。"),
               ("40 － 12 ＋ 8 先算 12 ＋ 8", "同级运算从左往右：28 ＋ 8 ＝ 36。"),
               ("合成算式时忘了加括号", "需要先算的加减部分要加小括号。")]),
  faq=[("为什么要先算乘除？", "这是大家共同的约定，这样同一个算式每个人算出来都一样。想改变顺序就加小括号。")],
  spec=lambda: [("同级运算", [(M.chain("mix"), 10), ("tw", "gen_tw_math_g2_two_step_problems", 3, 10)]),
                ("先乘除后加减", [(M.mixed_ops(), 20)]),
                ("小括号", [(M.mixed_ops(), 20)]),
                ("运算顺序和综合算式", [(M.order_rule(), 10), ("tw", "gen_tw_math_g2_two_step_problems", 4, 10)]),
                ("解决问题", [(M.mixed_story(), 20)])])

U("division-with-remainders", sort=10, dom="N", std=S_NUM, seed=92110, tw="gen_tw_math_g3_division",
  title="有余数的除法", short="有余数的除法",
  meta="二年级数学“有余数的除法”练习题：分不完剩下几个、有余数的除法、余数要比除数小、验算、解决问题，100题在线练习，附可打印答案。",
  kb="余数一定要比除数小", ks="23 ÷ 4 ＝ 5……3，验算：4 × 5 ＋ 3 ＝ 23。",
  faq=[("为什么余数要比除数小？", "如果余数和除数一样大或更大，就还能再分一份，说明商小了。")],
  spec=lambda: [("分不完剩下几个", [("tw", "gen_tw_math_g2_sharing_and_grouping", 3, 20)]),
                ("有余数的除法", [("tw", "gen_tw_math_g3_division", 2, 20)]),
                ("余数和验算", [("tw", "gen_tw_math_g3_division", 3, 19), ("tw", "gen_tw_math_g3_division", 1, 1)]),
                ("两位数除以一位数", [("tw", "gen_tw_math_g3_divide_by_one_digit", 1, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g3_division", 4, 20)])])

U("numbers-to-10000", sort=11, dom="N", std=S_NUM, seed=92111, tw="gen_tw_math_g3_numbers_to_10000",
  title="万以内数的认识", short="万以内数的认识",
  meta="二年级数学“万以内数的认识”练习题：千位、百位、十位、个位，读数和写数，比大小，近似数和整百整千，生活中的数，100题在线练习，附可打印答案。",
  kb="10 个一千是一万", ks="读数从高位起，中间有一个或几个 0 只读一个“零”，末尾的 0 不读。",
  faq=[("3005 怎么读？", "读作三千零五。中间有两个 0，只读一个“零”。")],
  spec=lambda: [("数位和计数单位", [("tw", "gen_tw_math_g3_numbers_to_10000", 0, 20)]),
                ("读数和写数", [("tw", "gen_tw_math_g3_numbers_to_10000", 1, 20)]),
                ("比大小", [("tw", "gen_tw_math_g3_numbers_to_10000", 2, 20)]),
                ("几个千、几个百", [("tw", "gen_tw_math_g3_numbers_to_10000", 3, 20)]),
                ("生活中的数", [("tw", "gen_tw_math_g3_numbers_to_10000", 4, 14), ("tw", "gen_tw_math_g2_estimation", 0, 6)])])

U("grams-and-kilograms", sort=12, dom="Q", std=S_QTY, seed=92112, tw="gen_tw_math_g3_kilograms_and_grams",
  title="克和千克", short="克和千克",
  meta="二年级数学“克和千克”练习题：读秤、1 千克 ＝ 1000 克、比轻重、重量的加减、估一估和解决问题，100题在线练习，附可打印答案。",
  kb="1 千克 ＝ 1000 克", ks="轻的东西用克作单位（一个鸡蛋约 50 克），重的用千克（一袋大米 10 千克）。",
  faq=[("怎么帮孩子建立“1 千克”的感觉？", "用两袋 500 克的盐或一瓶 1 升的水让孩子掂一掂，那就大约是 1 千克。")],
  spec=lambda: [("读秤", [("tw", "gen_tw_math_g3_kilograms_and_grams", 0, 19), (M.kg_cmp(), 1)]),
                ("千克和克的换算", [("tw", "gen_tw_math_g3_kilograms_and_grams", 1, 19), ("tw", "gen_tw_math_g3_kilograms_and_grams", 0, 1)]),
                ("比轻重", [("tw", "gen_tw_math_g3_kilograms_and_grams", 2, 19), ("tw", "gen_tw_math_g3_kilograms_and_grams", 1, 1)]),
                ("重量的加减", [("tw", "gen_tw_math_g3_kilograms_and_grams", 3, 19), ("tw", "gen_tw_math_g3_kilograms_and_grams", 2, 1)]),
                ("估一估和解决问题", [("tw", "gen_tw_math_g3_kilograms_and_grams", 4, 19), ("tw", "gen_tw_math_g3_kilograms_and_grams", 3, 1)])])

U("estimation", sort=13, dom="N", std=S_NUM, seed=92113, tw="gen_tw_math_g2_estimation",
  title="估算：整十、整百和够不够", short="估算",
  meta="二年级数学“估算”练习题：接近哪个整十数、大约几十几百、估算加减、钱够不够、用估算检查答案，100题在线练习，附可打印答案。",
  kb="把数看成接近的整十、整百数再算", ks="398 ＋ 205 大约是 400 ＋ 200 ＝ 600。",
  faq=[("什么时候用估算？", "只需要知道大概数目、或判断“够不够”的时候；也可以用来检查精确计算的结果对不对。")],
  spec=lambda: [("接近哪个整十数", [("tw", "gen_tw_math_g2_estimation", 0, 20)]),
                ("大约几十、几百", [("tw", "gen_tw_math_g2_estimation", 1, 20)]),
                ("估算加减", [("tw", "gen_tw_math_g2_estimation", 2, 20)]),
                ("钱够不够", [("tw", "gen_tw_math_g2_estimation", 3, 20)]),
                ("用估算检查答案", [("tw", "gen_tw_math_g2_estimation", 4, 20)])])

if __name__ == "__main__":
    import sys
    run_grade(G, UNITS, lambda r: (M.setup(r), L.setup(random.Random(r.random()))), sys.argv[1:] or None)
