# -*- coding: utf-8 -*-
"""
中国 四年级 数学（课标 2022 第二学段、人教版 四上・四下 の単元の順）。
台湾版の問題を adopt で简体字にして使い、公顷・鸡兔同笼・小数的加减は自前も足す（cn_mid）。
"""
import random
import cn_mid as M
import cn_low as L
from cn_common import run_grade, le, no, lesson

G = 4
S_NUM = "认识亿以内和亿以上的数，会用“万”“亿”为单位表示大数和求近似数；理解小数的意义和性质，会计算小数的加减法；掌握三位数乘两位数、除数是两位数的除法和四则混合运算，理解运算律"
S_QTY = "能用速度、时间、路程，单价、数量、总价等数量关系解决问题；体会鸡兔同笼等问题中的假设和列表的方法"
S_SHP = "会用量角器量角，认识直角、锐角、钝角、平角、周角；认识平行与垂直、平行四边形和梯形、三角形的特性和分类，知道三角形的内角和是 180°；认识公顷和平方千米"
S_MOV = "认识轴对称图形，能找出轴对称图形的对称轴，能在方格纸上补全轴对称图形，认识平移"
S_DATA = "能用条形统计图表示数据，理解平均数的意义，能求简单的平均数"

UNITS = {}


def U(slug, **kw):
    UNITS[slug] = kw


def same(mod, titles):
    return [(t, [("tw", mod, i, 20)]) for i, t in enumerate(titles)]


U("large-numbers", sort=1, dom="N", std=S_NUM, seed=94101, tw="gen_tw_math_g4_numbers_to_100_million",
  title="大数的认识：万、十万、百万、千万、亿", short="大数的认识",
  meta="四年级数学“大数的认识”练习题：计数单位万、十万、百万、千万、亿，读大数和写大数，比大小，用“万”作单位，生活中的大数，100题在线练习，附可打印答案。",
  kb="四位一级：个级、万级、亿级", ks="读数从高位读起，先读亿级，再读万级，最后读个级。",
  faq=[("怎么读 30502000？", "先分级：3050｜2000。读作三千零五十万二千。万级末尾的 0 不读。")],
  spec=lambda: [("计数单位和数位", [("tw", "gen_tw_math_g4_numbers_to_100_million", 0, 20)]),
                ("读数和写数", [("tw", "gen_tw_math_g4_numbers_to_100_million", 1, 20)]),
                ("比大小", [("tw", "gen_tw_math_g4_numbers_to_100_million", 2, 20)]),
                ("用“万”作单位", [("tw", "gen_tw_math_g4_numbers_to_100_million", 3, 20)]),
                ("生活中的大数", [("tw", "gen_tw_math_g4_numbers_to_100_million", 4, 13), ("tw", "gen_tw_math_g5_place_value", 3, 7)])])

U("hectares-and-square-kilometers", sort=2, dom="G", std=S_SHP, seed=94102, tw="gen_tw_math_g5_area_units",
  title="公顷和平方千米", short="公顷和平方千米",
  meta="四年级数学“公顷和平方千米”练习题：1 公顷 ＝ 10000 平方米、1 平方千米 ＝ 100 公顷、单位换算、比大小、选合适的面积单位、解决问题，100题在线练习，附可打印答案。",
  kb="1 公顷 ＝ 10000 平方米，1 平方千米 ＝ 100 公顷", ks="边长 100 米的正方形面积是 1 公顷，边长 1 千米的正方形面积是 1 平方千米。",
  body=lesson(["测量土地面积常用<b>公顷</b>：边长 100 米的正方形，面积是 1 公顷。<b>1 公顷 ＝ 10000 平方米</b>。",
               "测量更大的土地（城市、湖泊）用<b>平方千米</b>：边长 1 千米的正方形，面积是 1 平方千米。<b>1 平方千米 ＝ 100 公顷</b>。",
               "大单位换成小单位乘进率，小单位换成大单位除以进率。"],
              [("5 公顷 ＝ ___ 平方米", ["1 公顷 ＝ 10000 平方米", "5 × 10000 ＝ 50000"], "50000"),
               ("长 400 米、宽 250 米的果园有几公顷？", ["400 × 250 ＝ 100000（平方米）", "100000 ÷ 10000 ＝ 10"], "10 公顷")],
              [("1 公顷 ＝ 1000 平方米", "1 公顷 ＝ 10000 平方米（边长 100 米）。"),
               ("1 平方千米 ＝ 1000 公顷", "1 平方千米 ＝ 100 公顷。"),
               ("算出平方米后忘了换算", "题目问公顷时，最后要除以 10000。")]),
  faq=[("1 公顷大概有多大？", "边长 100 米的正方形，大约是两个标准足球场那么大。")],
  spec=lambda: [("面积单位的换算", [("tw", "gen_tw_math_g5_area_units", 0, -12), (M.ha_conv(), None)]),
                ("复名数和换算", [("tw", "gen_tw_math_g5_area_units", 1, -11), (M.ha_conv(), None)]),
                ("比大小和选单位", [("tw", "gen_tw_math_g5_area_units", 2, -7), (M.ha_conv(), None)]),
                ("算面积", [("tw", "gen_tw_math_g5_area_units", 3, -13), (M.ha_story(), None)]),
                ("解决问题", [("tw", "gen_tw_math_g5_area_units", 4, -11), (M.ha_story(), None)])])

U("measuring-angles", sort=3, dom="G", std=S_SHP, seed=94103, tw="gen_tw_math_g4_angles",
  title="角的度量：量角器、锐角、钝角、平角、周角", short="角的度量",
  meta="四年级数学“角的度量”练习题：用量角器量角，锐角、直角、钝角、平角、周角，角的和与差，比平角大的角，用三角尺画角和估测，100题在线练习，附可打印答案。",
  kb="量角时，中心对顶点，0 刻度线对一条边", ks="直角 90°，平角 180°，周角 360°；锐角小于 90°，钝角大于 90° 小于 180°。",
  faq=[("量角器的内圈和外圈看哪一圈？", "看角的一条边对着哪一圈的 0 刻度，就读那一圈上的数。")],
  spec=lambda: same("gen_tw_math_g4_angles", ["用量角器量角", "锐角、直角、钝角、平角、周角", "角的和与差", "比平角大的角", "三角尺和估测"]))

U("three-digit-by-two-digit", sort=4, dom="N", std=S_NUM, seed=94104, tw="gen_tw_math_g4_multi_digit_multiplication",
  title="三位数乘两位数和速度、时间、路程", short="三位数乘两位数",
  meta="四年级数学“三位数乘两位数”练习题：三位数乘两位数的笔算、末尾有 0 的乘法、速度 × 时间 ＝ 路程、求时间和速度、解决问题，100题在线练习，附可打印答案。",
  kb="速度 × 时间 ＝ 路程，单价 × 数量 ＝ 总价", ks="因数末尾有 0 的，先把 0 前面的数相乘，再在积的末尾添上 0。",
  faq=[("速度的单位怎么写？", "每小时行 60 千米写作 60 千米/时，每分钟走 70 米写作 70 米/分。")],
  spec=lambda: [("三位数乘两位数", [("tw", "gen_tw_math_g4_multi_digit_multiplication", 1, 20)]),
                ("末尾有0的乘法", [("tw", "gen_tw_math_g4_multi_digit_multiplication", 2, 20)]),
                ("求速度", [("tw", "gen_tw_math_g6_speed", 0, 20)]),
                ("求路程和时间", [("tw", "gen_tw_math_g6_speed", 1, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g4_multi_digit_multiplication", 4, 20)])])

U("parallel-perpendicular-and-quadrilaterals", sort=5, dom="G", std=S_SHP, seed=94105, tw="gen_tw_math_g4_perpendicular_and_parallel",
  title="平行与垂直、平行四边形和梯形", short="平行四边形和梯形",
  meta="四年级数学“平行四边形和梯形”练习题：找出互相垂直和互相平行的线、图形中的平行和垂直、认识平行四边形和梯形、四边形之间的关系，100题在线练习，附可打印答案。",
  kb="同一平面内不相交的两条直线互相平行", ks="两条直线相交成直角，就互相垂直。平行四边形两组对边平行，梯形只有一组对边平行。",
  faq=[("正方形是平行四边形吗？", "是。正方形和长方形的两组对边都分别平行，所以都是特殊的平行四边形。")],
  spec=lambda: [("互相垂直", [("tw", "gen_tw_math_g4_perpendicular_and_parallel", 0, 20)]),
                ("互相平行", [("tw", "gen_tw_math_g4_perpendicular_and_parallel", 1, 20)]),
                ("图形中的平行和垂直", [("tw", "gen_tw_math_g4_perpendicular_and_parallel", 2, 20)]),
                ("认识平行四边形和梯形", [("tw", "gen_tw_math_g4_quadrilaterals", 0, 20)]),
                ("四边形之间的关系", [("tw", "gen_tw_math_g4_quadrilaterals", 3, 20)])])

U("divide-by-two-digit", sort=6, dom="N", std=S_NUM, seed=94106, tw="gen_tw_math_g4_multi_digit_division",
  title="除数是两位数的除法", short="除数是两位数的除法",
  meta="四年级数学“除数是两位数的除法”练习题：口算除法、商是一位数的笔算、商是两位数的笔算、四位数除以两位数、试商和解决问题，100题在线练习，附可打印答案。",
  kb="把除数看作整十数来试商", ks="商偏大要调小，商偏小（余数比除数大）要调大。",
  faq=[("试商总是不对怎么办？", "把除数“四舍五入”看成整十数试商，再用除数乘商检查：积比被除数大就把商改小，余数比除数大就把商改大。")],
  spec=lambda: same("gen_tw_math_g4_multi_digit_division", ["口算除法", "商是一位数", "三位数除以两位数", "四位数除以两位数", "解决问题"]))

U("bar-graphs-and-averages", sort=7, dom="D", std=S_DATA, seed=94107, tw="gen_tw_math_g4_bar_and_line_graphs",
  title="条形统计图和平均数", short="条形统计图和平均数",
  meta="四年级数学“条形统计图和平均数”练习题：读条形统计图、用条形统计图比较、选合适的统计图、求平均数、用平均数求总数和缺少的数，100题在线练习，附可打印答案。",
  kb="平均数 ＝ 总数 ÷ 份数", ks="条形统计图用直条的长短表示数量的多少，一眼就能比较。",
  faq=[("平均数一定是数据里的某一个数吗？", "不一定。平均数表示一组数据的整体水平，可能和每一个数据都不同，也可能是小数。")],
  spec=lambda: [("读条形统计图", [("tw", "gen_tw_math_g4_bar_and_line_graphs", 0, 20)]),
                ("用条形统计图比较", [("tw", "gen_tw_math_g4_bar_and_line_graphs", 1, 20)]),
                ("选合适的统计图", [("tw", "gen_tw_math_g4_bar_and_line_graphs", 4, 20)]),
                ("求平均数", [("tw", "gen_tw_math_g5_three_step_problems_and_averages", 2, 20)]),
                ("用平均数解决问题", [("tw", "gen_tw_math_g5_three_step_problems_and_averages", 3, 20)])])

U("order-of-operations", sort=8, dom="N", std=S_NUM, seed=94108, tw="gen_tw_math_g4_order_of_operations",
  title="四则运算：运算顺序和综合算式", short="四则运算",
  meta="四年级数学“四则运算”练习题：同级运算从左往右、先乘除后加减、带括号的算式、列综合算式、用综合算式解决问题，100题在线练习，附可打印答案。",
  kb="先乘除后加减，有括号先算括号里", ks="小括号里面的先算，再算中括号里面的。",
  faq=[("什么时候要加小括号？", "需要先算的加减法放在乘除法后面时，要用小括号，例如（48 ＋ 12）÷ 6。")],
  spec=lambda: same("gen_tw_math_g4_order_of_operations", ["同级运算从左往右", "先乘除后加减", "括号先算", "列综合算式", "解决问题"]))

U("laws-of-operations", sort=9, dom="N", std=S_NUM, seed=94109, tw="gen_tw_math_g4_calculation_rules",
  title="运算定律和简便计算", short="运算定律",
  meta="四年级数学“运算定律”练习题：加法交换律和结合律、减法的性质、乘法交换律和结合律、乘法分配律、简便计算和解决问题，100题在线练习，附可打印答案。",
  kb="凑整十、整百，计算更简便", ks="乘法分配律：（a ＋ b）× c ＝ a × c ＋ b × c。25 × 4 ＝ 100，125 × 8 ＝ 1000。",
  faq=[("怎样看出能不能简便计算？", "看看有没有能凑成整十、整百、整千的数，例如 25 和 4、125 和 8、相加得 100 的两个数。")],
  spec=lambda: [("交换律和结合律", [("tw", "gen_tw_math_g4_calculation_rules", 0, 20)]),
                ("减法的性质", [("tw", "gen_tw_math_g4_calculation_rules", 1, 20)]),
                ("乘法分配律", [("tw", "gen_tw_math_g5_distributive_property", 0, 20)]),
                ("简便计算", [("tw", "gen_tw_math_g4_calculation_rules", 3, 10), ("tw", "gen_tw_math_g5_distributive_property", 2, 10)]),
                ("解决问题", [("tw", "gen_tw_math_g4_calculation_rules", 4, 20)])])

U("meaning-and-properties-of-decimals", sort=10, dom="N", std=S_NUM, seed=94110, tw="gen_tw_math_g4_decimals",
  title="小数的意义和性质", short="小数的意义和性质",
  meta="四年级数学“小数的意义和性质”练习题：百分位和 0.01、小数的性质、小数比大小、小数点移动引起的大小变化、求小数的近似数、单位换算，100题在线练习，附可打印答案。",
  kb="小数的末尾添上 0 或去掉 0，大小不变", ks="小数点向右移动一位，小数就扩大到原来的 10 倍；向左移动一位，缩小到原来的 1/10。",
  faq=[("0.30 和 0.3 一样吗？", "大小相等，但表示的精确度不同：0.30 精确到百分位，0.3 精确到十分位。")],
  spec=lambda: [("小数的意义", [("tw", "gen_tw_math_g4_decimals", 0, 20)]),
                ("小数的性质和比大小", [(M.dec_simplify(), 10), ("tw", "gen_tw_math_g4_decimals", 1, 10)]),
                ("小数点移动", [("tw", "gen_tw_math_g5_place_value", 2, 20)]),
                ("求小数的近似数", [("tw", "gen_tw_math_g5_rounding_decimals", 1, 10), ("tw", "gen_tw_math_g5_rounding_decimals", 2, 10)]),
                ("小数和单位换算", [("tw", "gen_tw_math_g4_decimals", 3, -20, no("×", "÷")), (M.dec_simplify(), None)])])

U("triangles", sort=11, dom="G", std=S_SHP, seed=94111, tw="gen_tw_math_g4_triangles",
  title="三角形：分类、内角和、三边关系", short="三角形",
  meta="四年级数学“三角形”练习题：按边分类、按角分类、等腰三角形和等边三角形、三角形的内角和是 180°、两边之和大于第三边，100题在线练习，附可打印答案。",
  kb="三角形的内角和是 180°", ks="任意两边之和大于第三边；三角形具有稳定性。",
  faq=[("怎么判断三条线段能不能围成三角形？", "看较短的两条线段之和是否大于最长的那条，大于才能围成。")],
  spec=lambda: [("按边分类", [("tw", "gen_tw_math_g4_triangles", 0, 20)]),
                ("按角分类", [("tw", "gen_tw_math_g4_triangles", 1, 20)]),
                ("三角形的内角和", [("tw", "gen_tw_math_g5_triangle_and_quadrilateral_properties", 0, 20)]),
                ("三边关系", [("tw", "gen_tw_math_g5_triangle_and_quadrilateral_properties", 2, 20)]),
                ("三角形的性质", [("tw", "gen_tw_math_g4_triangles", 4, 20)])])

U("adding-and-subtracting-decimals", sort=12, dom="N", std=S_NUM, seed=94112, tw="gen_tw_math_g4_decimals",
  title="小数的加法和减法", short="小数的加减法",
  meta="四年级数学“小数的加法和减法”练习题：两位小数的加减、位数不同的小数加减、小数加减混合运算、简便计算、解决问题，100题在线练习，附可打印答案。",
  kb="小数点对齐，也就是相同数位对齐", ks="位数不同时，可以在末尾添 0 再算：3.5 － 1.27 ＝ 3.50 － 1.27 ＝ 2.23。",
  faq=[("小数加减和整数加减有什么一样？", "都是相同数位对齐再算。整数是末位对齐，小数是小数点对齐。")],
  spec=lambda: [("两位小数的加减", [("tw", "gen_tw_math_g4_decimals", 2, 20)]),
                ("小数加法", [(M.dec_op("+"), 20)]),
                ("小数减法", [(M.dec_op("-"), 20)]),
                ("加减混合和简便计算", [(M.dec_op("+", 1), 10), (M.dec_op("-", 1), 10)]),
                ("解决问题", [("tw", "gen_tw_math_g4_decimals", 4, 10), (M.dec_op("+", 2, True), 5), (M.dec_op("-", 2, True), 5)])])

U("axial-symmetry", sort=13, dom="T", std=S_MOV, seed=94113, tw="gen_tw_math_g5_line_symmetry",
  title="图形的运动：轴对称", short="轴对称",
  meta="四年级数学“轴对称”练习题：对称轴有几条、找对称点、对称边和对称角、字母和汉字中的轴对称、推理和应用，100题在线练习，附可打印答案。",
  kb="沿对称轴对折，两边完全重合", ks="对称点到对称轴的距离相等。正方形有 4 条对称轴，圆有无数条。",
  faq=[("平行四边形是轴对称图形吗？", "一般的平行四边形不是：找不到一条直线把它对折后完全重合。长方形、菱形和正方形是。")],
  spec=lambda: same("gen_tw_math_g5_line_symmetry", ["对称轴有几条", "找对称点", "对称边和对称角", "字母和汉字", "推理和应用"]))

U("rounding-and-approximate-numbers", sort=14, dom="N", std=S_NUM, seed=94114, tw="gen_tw_math_g4_rounding",
  title="近似数：四舍五入法、进一法、去尾法", short="近似数",
  meta="四年级数学“近似数”练习题：四舍五入法、进一法和去尾法、生活中用哪一种、用近似数估算、近似数原来可能是多少，100题在线练习，附可打印答案。",
  kb="看省略部分的最高位：满 5 进 1，不满 5 舍去", ks="装东西要用“进一法”，做衣服、装满的盒数要用“去尾法”。",
  faq=[("近似数后面的 0 能去掉吗？", "用“万”作单位时可以：123456 ≈ 12 万。直接写数时不能随便去掉，否则大小就变了。")],
  spec=lambda: [("四舍五入法", [("tw", "gen_tw_math_g4_rounding", 0, 20)]),
                ("进一法和去尾法", [("tw", "gen_tw_math_g4_rounding", 1, 20)]),
                ("生活中用哪一种", [("tw", "gen_tw_math_g4_rounding", 2, -20), ("tw", "gen_tw_math_g5_rounding_decimals", 4, None)]),
                ("用近似数估算", [("tw", "gen_tw_math_g4_rounding", 3, 20)]),
                ("原来的数可能是多少", [("tw", "gen_tw_math_g4_rounding", 4, 20)])])

U("chickens-and-rabbits", sort=15, dom="Q", std=S_QTY, seed=94115, tw="gen_tw_math_g6_classic_word_problems",
  title="鸡兔同笼", short="鸡兔同笼",
  meta="四年级数学“鸡兔同笼”练习题：列表法、假设法、求兔有几只、求鸡有几只、龟鹤和车轮等变式问题，100题在线练习，附可打印答案。",
  kb="先假设全是鸡，多出来的腿是兔的", ks="兔的只数 ＝（总腿数 － 总只数 × 2）÷（4 － 2）。",
  body=lesson(["<b>列表法</b>：从“全是鸡”开始，一只一只把鸡换成兔，看腿数什么时候正好。",
               "<b>假设法</b>：假设全是鸡，腿数会比实际少。每把 1 只鸡换成 1 只兔，腿多 2 条。少了几条，就有几个 2，就是兔的只数。",
               "求出兔的只数后，用总只数减去兔，就是鸡的只数。"],
              [("鸡兔共 10 只，腿 28 条。兔几只？", ["假设全是鸡：10 × 2 ＝ 20（条）", "少了 28 － 20 ＝ 8（条），8 ÷ 2 ＝ 4"], "兔 4 只，鸡 6 只"),
               ("自行车和三轮车共 8 辆，轮子 19 个。三轮车几辆？", ["假设全是自行车：8 × 2 ＝ 16", "19 － 16 ＝ 3，3 ÷（3 － 2）＝ 3"], "3 辆")],
              [("把少的腿数直接当成兔的只数", "每只兔比鸡多 2 条腿，要再除以 2。"),
               ("假设全是兔时求成了兔", "假设全是兔，求出来的是鸡的只数。"),
               ("忘了检验", "把答案代回去，腿数和只数都要对。")]),
  faq=[("鸡兔同笼在哪个年级学？", "人教版四年级下册“数学广角”。五年级学了方程后，也可以用方程来解。"),
       ("除了假设法还有什么方法？", "还有列表法、画图法，以及五年级学的方程法：设兔有 x 只，列 4x ＋ 2(10 － x) ＝ 28。")],
  spec=lambda: [("列表法", [(M.cr_list(), 20)]),
                ("求兔有几只", [(M.cr("big"), 20)]),
                ("求鸡有几只", [(M.cr("small"), 20)]),
                ("变式问题", [(M.cr("car"), 20)]),
                ("综合练习", [("tw", "gen_tw_math_g6_classic_word_problems", 1, 13), (M.cr("big"), 7)])])

U("observing-objects", sort=16, dom="G", std=S_SHP, seed=94116, tw="gen_tw_math_g7_three_views",
  title="观察物体：从正面、上面、左面看", short="观察物体",
  meta="四年级数学“观察物体”练习题：从正面看、从上面看、从右面看小正方体搭成的物体，根据看到的图形判断，100题在线练习，附可打印答案。",
  kb="从不同方向看同一个物体，看到的形状可能不同", ks="从正面看，前后挡住的方块只算一个；从上面看，看到的是每一列的顶。",
  faq=[("怎么帮孩子练习观察物体？", "用积木或小方块搭一搭，让孩子蹲下从正面看、站起来从上面看，再把看到的画在方格纸上。")],
  spec=lambda: same("gen_tw_math_g7_three_views", ["从正面看", "从上面看", "综合判断", "从右面看", "看上面的数字"]))

if __name__ == "__main__":
    import sys
    run_grade(G, UNITS, lambda r: (M.setup(r), L.setup(random.Random(r.random()))), sys.argv[1:] or None)
