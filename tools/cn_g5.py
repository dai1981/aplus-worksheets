# -*- coding: utf-8 -*-
"""
中国 五年级 数学（课标 2022 第三学段、人教版 五上・五下 の単元の順）。
台湾版の問題を adopt で简体字にして使い、数对・解方程（正の数）は自前（cn_high）。
"""
import random
import cn_mid as M
import cn_high as H
from cn_common import run_grade, le, no, both, lesson

G = 5
S_NUM = "会计算小数乘法和小数除法，能用“四舍五入”法求积和商的近似数，认识循环小数；理解因数和倍数、质数和合数，知道 2、3、5 的倍数的特征；理解分数的意义和基本性质，会约分和通分，会计算异分母分数的加减法"
S_QTY = "能用字母表示数和数量关系，会解简单的方程，能列方程解决问题"
S_SHP = "掌握平行四边形、三角形、梯形的面积公式，会计算组合图形的面积；认识长方体和正方体的特征和展开图，会计算它们的表面积和体积，认识体积单位和容积单位"
S_MOV = "能在方格纸上用数对确定位置；认识图形的旋转，能在方格纸上把简单图形旋转 90°"
S_DATA = "能用折线统计图表示数据并分析变化的趋势；能用“一定”“可能”“不可能”描述事件发生的可能性，能判断可能性的大小"

UNITS = {}


def U(slug, **kw):
    UNITS[slug] = kw


def same(mod, titles, keep=None):
    return [(t, [("tw", mod, i, 20, keep) if keep else ("tw", mod, i, 20)]) for i, t in enumerate(titles)]


U("multiplying-decimals", sort=1, dom="N", std=S_NUM, seed=95101, tw="gen_tw_math_g5_multiplying_decimals",
  title="小数乘法：小数乘整数、小数乘小数、积的大小", short="小数乘法",
  meta="五年级数学“小数乘法”练习题：小数乘整数、小数乘小数、积的小数位数、积和因数的大小关系、积末尾的 0、解决问题，100题在线练习，附可打印答案。",
  kb="因数中一共有几位小数，积就有几位小数", ks="先按整数乘法算出积，再数因数的小数位数，从积的右边起点上小数点。",
  faq=[("积的末尾有 0 怎么办？", "先点小数点，再把末尾的 0 去掉。例如 2.5 × 0.4 ＝ 1.00 ＝ 1。")],
  spec=lambda: same("gen_tw_math_g5_multiplying_decimals", ["小数乘整数", "小数乘小数（一）", "小数乘小数（二）", "积的大小和末尾的 0", "解决问题"]))

U("position-ordered-pairs", sort=2, dom="T", std=S_MOV, seed=95102, tw=None,
  title="位置：用数对确定位置", short="用数对确定位置",
  meta="五年级数学“位置”练习题：用数对表示位置、根据数对找点、同一行和同一列、图形的平移和数对、长方形的第四个顶点，100题在线练习，附可打印答案。",
  kb="数对 (列, 行)：先写列，再写行", ks="竖排叫列，从左往右数；横排叫行，从前往后（从下往上）数。",
  body=lesson(["竖排叫<b>列</b>，横排叫<b>行</b>。确定第几列一般从左往右数，确定第几行一般从前往后（方格图从下往上）数。",
               "用<b>数对</b>表示位置：先写列，再写行，中间用逗号隔开，外面加小括号。例如第 3 列第 2 行写作 (3, 2)。",
               "第一个数相同，在同一列；第二个数相同，在同一行。"],
              [("小明坐在第 4 列第 3 行，用数对表示", ["先写列 4，再写行 3"], "(4, 3)"),
               ("点 (2, 5) 向右平移 3 格", ["向右平移改变列：2 ＋ 3 ＝ 5，行不变"], "(5, 5)")],
              [("把列和行写反", "(3, 2) 是第 3 列第 2 行，和 (2, 3) 不是同一个位置。"),
               ("上下平移时改了第一个数", "上下平移改变的是行，也就是第二个数。"),
               ("忘了加括号和逗号", "数对要写成 (3, 2) 的形式。")]),
  faq=[("数对为什么先写列再写行？", "这是数学上的约定，和以后学的坐标 (x, y) 一样：先横向（列），再纵向（行）。"),
       ("生活中哪里用到数对？", "电影票上的“几排几座”、地图上的网格、国际象棋的棋盘，都是用两个数确定位置。")],
  spec=lambda: [("用数对表示位置", [(H.pair_read(), 20)]),
                ("根据数对找位置", [(H.pair_find(), 20)]),
                ("座位和数对", [(H.pair_seat(), 20)]),
                ("平移和同行同列", [(H.pair_seat(), 20)]),
                ("综合练习", [(H.pair_shape(), 10), (H.pair_read(), 10)])])

U("dividing-decimals", sort=3, dom="N", std=S_NUM, seed=95103, tw="gen_tw_math_g5_dividing_decimals",
  title="小数除法：除数是整数、除数是小数、循环小数", short="小数除法",
  meta="五年级数学“小数除法”练习题：除数是整数的小数除法、除数是小数的除法、商的近似数、商和被除数的大小关系、解决问题，100题在线练习，附可打印答案。",
  kb="除数是小数，先把除数变成整数", ks="除数扩大到原来的几倍，被除数也扩大到原来的几倍，商不变。商的小数点和被除数的小数点对齐。",
  faq=[("什么是循环小数？", "一个小数从小数部分的某一位起，一个或几个数字依次不断重复出现，就是循环小数。例如 1 ÷ 3 ＝ 0.333……")],
  spec=lambda: [("除数是整数", [("tw", "gen_tw_math_g5_dividing_decimals", 1, 20)]),
                ("除数是小数", [("tw", "gen_tw_math_g6_dividing_decimals", 0, 10), ("tw", "gen_tw_math_g6_dividing_decimals", 1, 10)]),
                ("商的近似数", [("tw", "gen_tw_math_g5_dividing_decimals", 2, 20)]),
                ("商和被除数的大小", [("tw", "gen_tw_math_g6_dividing_decimals", 3, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g5_dividing_decimals", 4, 10), ("tw", "gen_tw_math_g6_dividing_decimals", 2, 10)])])

U("likelihood", sort=4, dom="D", std=S_DATA, seed=95104, tw="gen_tw_math_g6_likelihood",
  title="可能性：一定、可能、不可能和可能性的大小", short="可能性",
  meta="五年级数学“可能性”练习题：用一定、可能、不可能描述事件，判断可能性的大小，摸球和转盘，设计游戏规则，100题在线练习，附可打印答案。",
  kb="数量越多，摸到的可能性越大", ks="只有一种颜色的球时“一定”摸到它；没有这种颜色时“不可能”摸到；都有时“可能”摸到。",
  faq=[("“可能性大”就一定会发生吗？", "不一定。可能性大只是更容易发生，摸一次仍然可能摸到数量少的那种。")],
  spec=lambda: [("一定、可能、不可能", [("tw", "gen_tw_math_g6_likelihood", 0, -20), ("tw", "gen_tw_math_g6_likelihood", 4, None)]),
                ("摸球的可能性", [("tw", "gen_tw_math_g6_likelihood", 1, 20)]),
                ("转盘：哪一个可能性大", [("tw", "gen_tw_math_g6_likelihood", 2, 20)]),
                ("从统计数据判断", [("tw", "gen_tw_math_g6_likelihood", 3, 20)]),
                ("骰子、硬币和数字卡", [("tw", "gen_tw_math_g6_likelihood", 4, -20), ("tw", "gen_tw_math_g6_likelihood", 1, None)])])

U("simple-equations", sort=5, dom="Q", std=S_QTY, seed=95105, tw=None,
  title="简易方程：用字母表示数、解方程、列方程解决问题", short="简易方程",
  meta="五年级数学“简易方程”练习题：用字母表示数和数量关系，等式的性质，解形如 x ＋ a ＝ b、ax ＝ b、ax ＋ b ＝ c 的方程，列方程解决问题，100题在线练习，附可打印答案。",
  kb="等式两边同时加、减、乘、除以同一个数（0 除外），等式仍然成立", ks="含有未知数的等式叫方程。求出的未知数的值要代回原方程检验。",
  body=lesson(["用<b>字母</b>可以表示数和数量关系，例如每本书 a 元，买 3 本是 3a 元。数和字母相乘，乘号可以省略。",
               "含有未知数的等式叫<b>方程</b>。解方程用<b>等式的性质</b>：两边同时加上或减去同一个数，同时乘或除以同一个不为 0 的数，等式仍然成立。",
               "列方程解决问题：先找出等量关系，再设未知数为 x，列方程、解方程、检验。"],
              [("x ＋ 18 ＝ 45", ["两边同时减去 18", "x ＝ 45 － 18 ＝ 27"], "x ＝ 27"),
               ("3x ＋ 5 ＝ 32", ["两边同时减去 5：3x ＝ 27", "两边同时除以 3：x ＝ 9"], "x ＝ 9")],
              [("x － 12 ＝ 30，算成 x ＝ 18", "两边应该同时加上 12：x ＝ 42。"),
               ("把 3x 当成 3 ＋ x", "3x 是 3 × x。"),
               ("解完不检验", "把 x 的值代回原方程，左右两边相等才对。")]),
  faq=[("方程和等式有什么区别？", "方程一定是等式，但等式不一定是方程。只有含有未知数的等式才是方程，例如 3 ＋ 5 ＝ 8 是等式，不是方程。"),
       ("五年级解方程需要移项吗？", "人教版五年级用等式的性质解方程，不讲移项。移项在七年级学。")],
  spec=lambda: [("用字母和符号表示数", [("tw", "gen_tw_math_g5_formulas_with_symbols", 1, -14, H.nonneg), (H.eqn_story(), None)]),
                ("方程的解", [("tw", "gen_tw_math_g7_solving_linear_equations", 0, -20, H.nonneg), (H.eqn("mul"), None)]),
                ("解方程（一步）", [(H.eqn("add"), 7), (H.eqn("sub"), 7), (H.eqn("mul"), 6)]),
                ("解方程（两步）", [(H.eqn("two"), 12), (H.eqn("par"), 8)]),
                ("列方程解决问题", [(H.eqn_story(), 10), ("tw", "gen_tw_math_g5_formulas_with_symbols", 2, -10, H.nonneg), (H.eqn("two"), None)])])

U("area-of-polygons", sort=6, dom="G", std=S_SHP, seed=95106, tw="gen_tw_math_g5_area_of_triangles_and_quadrilaterals",
  title="多边形的面积：平行四边形、三角形、梯形", short="多边形的面积",
  meta="五年级数学“多边形的面积”练习题：平行四边形的面积、三角形的面积、梯形的面积、已知面积求高、解决问题，100题在线练习，附可打印答案。",
  kb="平行四边形 S ＝ ah，三角形 S ＝ ah ÷ 2，梯形 S ＝（a ＋ b）h ÷ 2", ks="三角形和梯形的面积公式都是拼成平行四边形推出来的，所以要除以 2。",
  faq=[("为什么三角形面积要除以 2？", "两个完全一样的三角形能拼成一个平行四边形，三角形的面积是这个平行四边形的一半。")],
  spec=lambda: same("gen_tw_math_g5_area_of_triangles_and_quadrilaterals", ["平行四边形的面积", "三角形的面积", "梯形的面积", "已知面积求高", "解决问题"]))

U("factors-and-multiples", sort=7, dom="N", std=S_NUM, seed=95107, tw="gen_tw_math_g5_factors_and_multiples",
  title="因数与倍数：2、3、5 的倍数，质数和合数", short="因数与倍数",
  meta="五年级数学“因数与倍数”练习题：找因数和倍数，2、5、3 的倍数的特征，奇数和偶数，质数和合数，分解质因数，100题在线练习，附可打印答案。",
  kb="只有 1 和它本身两个因数的数是质数", ks="个位是 0、2、4、6、8 的数是 2 的倍数；个位是 0 或 5 的是 5 的倍数；各位数字之和是 3 的倍数，这个数就是 3 的倍数。",
  faq=[("1 是质数还是合数？", "1 既不是质数也不是合数，因为它只有一个因数。"),
       ("最小的质数是几？", "2。2 也是唯一的偶数质数。")],
  spec=lambda: [("因数和倍数", [("tw", "gen_tw_math_g5_factors_and_multiples", 0, 20)]),
                ("2、3、5 的倍数的特征", [("tw", "gen_tw_math_g6_prime_factorization", 1, 20)]),
                ("质数和合数", [("tw", "gen_tw_math_g6_prime_factorization", 0, 20)]),
                ("质因数", [("tw", "gen_tw_math_g6_prime_factorization", 2, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g5_factors_and_multiples", 4, 20)])])

U("cuboids-and-cubes", sort=8, dom="G", std=S_SHP, seed=95108, tw="gen_tw_math_g5_volume_and_surface_area",
  title="长方体和正方体：特征、表面积、体积和容积", short="长方体和正方体",
  meta="五年级数学“长方体和正方体”练习题：长方体中互相平行和垂直的面，表面积，体积，体积单位和容积单位的换算，解决问题，100题在线练习，附可打印答案。",
  kb="长方体的体积 ＝ 长 × 宽 × 高", ks="长方体的表面积 ＝（长 × 宽 ＋ 长 × 高 ＋ 宽 × 高）× 2。1 立方分米 ＝ 1 升，1 立方厘米 ＝ 1 毫升。",
  faq=[("表面积和体积有什么不同？", "表面积是 6 个面的面积之和，单位是平方厘米；体积是物体所占空间的大小，单位是立方厘米。")],
  spec=lambda: [("面与面的关系", [("tw", "gen_tw_math_g5_faces_parallel_and_perpendicular", 0, -20), ("tw", "gen_tw_math_g5_faces_parallel_and_perpendicular", 1, None)]),
                ("表面积", [("tw", "gen_tw_math_g5_volume_and_surface_area", 1, 20)]),
                ("体积", [("tw", "gen_tw_math_g5_volume_and_surface_area", 0, 20)]),
                ("体积单位和容积", [("tw", "gen_tw_math_g5_volume_and_capacity", 1, 20)]),
                ("解决问题", [("tw", "gen_tw_math_g5_volume_and_surface_area", 4, 10), ("tw", "gen_tw_math_g5_volume_and_capacity", 4, 10)])])

U("meaning-and-properties-of-fractions", sort=9, dom="N", std=S_NUM, seed=95109, tw="gen_tw_math_g5_simplifying_fractions",
  title="分数的意义和性质：约分、通分、分数和小数", short="分数的意义和性质",
  meta="五年级数学“分数的意义和性质”练习题：分数与除法、真分数和假分数、分数的基本性质、最大公因数和约分、最小公倍数和通分、分数和小数的互化，100题在线练习，附可打印答案。",
  kb="分子和分母同时乘或除以相同的数（0 除外），分数的大小不变", ks="约分用分子和分母的最大公因数去除；通分用分母的最小公倍数作公分母。",
  faq=[("什么是最简分数？", "分子和分母只有公因数 1 的分数叫最简分数，例如 2/3。")],
  spec=lambda: [("分数与除法", [("tw", "gen_tw_math_g5_fractions_as_division", 0, -20), ("tw", "gen_tw_math_g5_fractions_as_division", 1, None)]),
                ("真分数和假分数", [("tw", "gen_tw_math_g4_fractions", 0, 20)]),
                ("最大公因数和约分", [("tw", "gen_tw_math_g6_gcf_and_lcm", 0, -10), ("tw", "gen_tw_math_g5_simplifying_fractions", 1, None)]),
                ("最小公倍数和通分", [("tw", "gen_tw_math_g6_gcf_and_lcm", 1, -10), ("tw", "gen_tw_math_g5_simplifying_fractions", 2, None)]),
                ("分数和小数的互化", [("tw", "gen_tw_math_g5_dividing_decimals", 3, 20)])])

U("rotation", sort=10, dom="T", std=S_MOV, seed=95110, tw="gen_tw_math_g4_rotation",
  title="图形的运动：旋转", short="旋转",
  meta="五年级数学“图形的运动（三）”练习题：顺时针和逆时针旋转，旋转的中心、方向和角度，分针和时针转过的角度，转身和方向，100题在线练习，附可打印答案。",
  kb="旋转要说清：绕哪一点、按什么方向、转多少度", ks="顺时针和钟表指针转的方向相同，逆时针相反。旋转后图形的形状和大小不变。",
  faq=[("钟表的分针转一圈是多少度？", "360°。分针每走 1 分钟转 6°，走 15 分钟转 90°。")],
  spec=lambda: same("gen_tw_math_g4_rotation", ["分针转了几度", "分针和时间", "时针转了几度", "顺时针和逆时针", "转身和方向"]))

U("adding-and-subtracting-fractions", sort=11, dom="N", std=S_NUM, seed=95111, tw="gen_tw_math_g5_adding_and_subtracting_fractions",
  title="分数的加法和减法：同分母和异分母", short="分数的加法和减法",
  meta="五年级数学“分数的加法和减法”练习题：同分母分数加减法、异分母分数的加法和减法、通分、解决问题，100题在线练习，附可打印答案。",
  kb="异分母分数相加减，先通分，再按同分母分数加减", ks="同分母分数相加减，分母不变，分子相加减；计算结果要化成最简分数。",
  faq=[("结果是假分数要化成带分数吗？", "人教版一般化成最简分数即可，假分数可以保留，也可以化成带分数。")],
  spec=lambda: [("同分母分数加减法", [("tw", "gen_tw_math_g4_fractions", 2, -20), ("tw", "gen_tw_math_g4_fractions", 3, None)]),
                ("简单的异分母加减", [("tw", "gen_tw_math_g4_equivalent_fractions", 3, 20)]),
                ("异分母分数的加法", [("tw", "gen_tw_math_g5_adding_and_subtracting_fractions", 0, -20), ("tw", "gen_tw_math_g5_adding_and_subtracting_fractions", 2, None)]),
                ("异分母分数的减法", [("tw", "gen_tw_math_g5_adding_and_subtracting_fractions", 1, -20), ("tw", "gen_tw_math_g5_adding_and_subtracting_fractions", 3, None)]),
                ("解决问题", [("tw", "gen_tw_math_g5_adding_and_subtracting_fractions", 4, -20), ("tw", "gen_tw_math_g5_adding_and_subtracting_fractions", 2, None)])])

U("line-graphs", sort=12, dom="D", std=S_DATA, seed=95112, tw="gen_tw_math_g5_making_line_graphs",
  title="折线统计图：读图、画图和复式折线统计图", short="折线统计图",
  meta="五年级数学“折线统计图”练习题：描点画折线统计图，确定刻度，读折线统计图，看变化的趋势，选条形统计图还是折线统计图，100题在线练习，附可打印答案。",
  kb="折线统计图能清楚地看出数量增减变化的情况", ks="线往上就是增加，往下就是减少；线越陡，变化越大。",
  faq=[("什么时候用折线统计图？", "要看数量随时间怎样变化（气温、身高、销量）时用折线统计图；只比较多少时用条形统计图。")],
  spec=lambda: same("gen_tw_math_g5_making_line_graphs", ["描点", "找出画错的点", "确定刻度和省略", "读折线统计图", "看变化和选统计图"]))

if __name__ == "__main__":
    import sys
    run_grade(G, UNITS, lambda r: (M.setup(r), H.setup(random.Random(r.random()))), sys.argv[1:] or None)
