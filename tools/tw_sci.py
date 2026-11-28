# -*- coding: utf-8 -*-
"""
台灣 / 自然科學（十二年國教課綱 自然科學領域）。country `tw`、subject `science`、grade `grade-3`〜`grade-12`。
中国の理科の単元（cn_s*）の問題を OpenCC（s2twp）と台灣の用語（TERMS：位能・力學能・莫耳・酵素・粒線體・族群・天擇・冷次定律…）で直して使う。
中国だけの話（我國・長江・人民幣・天宮…、LEAKS）を含む問題は落とす。単元の並びは GRADES（台灣の教科書の一般的な配分）。
  python3 tw_sci.py 8 [slug …]   seed は 96000 + 100 × 学年 + 番号
"""
import re
import sys
import importlib
import opencc
import cn_sci
import sci_common
from sci_common import Unit, item

_S2T = opencc.OpenCC("s2tw")
TERMS = [
    ("壓力感測器", "@PS@"), ("壓力傳感器", "@PS@"), ("和壓力影響", "和@P@影響"), ("位移、壓力等", "位移、@P@等"), ("承受壓力", "承受外力"), ("把壓力向", "把受力向"), ("壓強", "@P@"), ("壓力", "正向力"), ("@P@", "壓力"), ("@PS@", "壓力感測器"), ("正向力差", "壓力差"), ("向上正向力", "向上壓力"),
    ("不支持燃燒", "不助燃"), ("支持燃燒", "助燃"), ("支持力", "支撐力"), ("支持物", "支撐物"),
    ("排洩", "排泄"), ("進化", "演化"), ("內環境穩態", "體內恆定"), ("穩態", "恆定"), ("細胞器", "胞器"), ("自由組合定律", "獨立分配律"), ("分離定律", "分離律"),
    ("勻變速直線運動", "等加速度直線運動"), ("勻變速", "等加速度"), ("勻加速", "等加速"), ("勻減速", "等減速"), ("勻速直線運動", "等速度直線運動"), ("勻速", "等速"),
    ("滑動摩擦力", "動摩擦力"), ("動摩擦因數", "動摩擦係數"), ("動能定理", "功能定理"), ("交變電流", "交流電"), ("能級", "能階"), ("比結合能", "平均每核子束縛能"), ("結合能", "束縛能"),
    ("電負性", "陰電性"), ("電離能", "游離能"), ("電離", "解離"), ("雜化", "混成"), ("價層電子對互斥模型", "價殼層電子對互斥（VSEPR）模型"), ("晶胞", "單位晶格"),
    ("共價晶體", "共價網狀固體"), ("分子晶體", "分子固體"), ("離子晶體", "離子固體"), ("金屬晶體", "金屬固體"), ("烷烴", "烷類"), ("烯烴", "烯類"), ("炔烴", "炔類"), ("鹵代烴", "鹵化烴"),
    ("官能團", "官能基"), ("加聚反應", "加成聚合反應"), ("縮聚反應", "縮合聚合反應"), ("同分異構體", "同分異構物"), ("蓋斯定律", "赫斯定律"), ("勒夏特列原理", "勒沙特列原理"),
    ("金剛石", "鑽石"), ("著火點", "燃點"), ("地幔", "地函"), ("莫霍界面", "莫氏不連續面"), ("古登堡界面", "古氏不連續面"), ("準靜止鋒", "滯留鋒"), ("幼崽", "幼仔"),
    ("視頻", "影片"), ("信息", "資訊"), ("晶體管", "電晶體"), ("集成電路", "積體電路"), ("二極管", "二極體"), ("屏幕", "螢幕"), ("網絡", "網路"), ("軟件", "軟體"), ("硬件", "硬體"), ("打印", "列印"),
    ("自行車", "腳踏車"), ("公交車", "公車"), ("出租車", "計程車"), ("土豆", "馬鈴薯"), ("西紅柿", "番茄"), ("菠蘿", "鳳梨"), ("獼猴桃", "奇異果"), ("信號", "訊號"), ("等離子", "電漿"), ("光盤", "光碟"),
    ("空調", "冷氣"), ("衛生間", "廁所"), ("方便面", "泡麵"), ("圓珠筆", "原子筆"), ("短信", "簡訊"), ("電飯鍋", "電鍋"), ("冰棍", "冰棒"), ("易拉罐", "鋁罐"), ("U 盤", "隨身碟"), ("彈簧測力計", "彈簧秤"), ("測力計", "彈簧秤"),
    ("重力勢能", "重力位能"), ("彈性勢能", "彈性位能"), ("電勢能", "電位能"), ("電勢差", "電位差"), ("電勢", "電位"), ("勢能", "位能"), ("機械能", "力學能"),
    ("比熱容", "比熱"), ("熱化學方程式", "熱化學反應式"), ("離子方程式", "離子反應式"), ("化學方程式", "化學反應式"), ("溶質質量分數", "重量百分濃度"), ("質量分數", "質量百分率"),
    ("物質的量濃度", "體積莫耳濃度"), ("物質的量", "莫耳數"), ("氣體摩爾體積", "氣體莫耳體積"), ("摩爾質量", "莫耳質量"), ("阿伏加德羅常數", "亞佛加厥常數"), ("阿伏加德羅", "亞佛加厥"), ("摩爾", "莫耳"),
    ("元素週期律", "週期律"), ("元素週期表", "週期表"), ("化合價", "原子價"), ("電解池", "電解槽"), ("原電池", "化學電池"), ("電流表", "安培計"), ("電壓表", "伏特計"), ("千瓦時", "度（千瓦小時）"),
    ("洛倫茲力", "勞侖茲力"), ("楞次定律", "冷次定律"), ("開普勒", "克卜勒"), ("卡文迪什", "卡文狄西"), ("麥克斯韋", "馬克士威"), ("盧瑟福", "拉塞福"), ("玻爾", "波耳"), ("湯姆孫", "湯姆森"),
    ("密立根", "密立坎"), ("門捷列夫", "門得列夫"), ("摩爾根", "摩根"), ("沃森", "華生"), ("艾弗里", "艾佛瑞"), ("格里菲思", "格里夫茲"), ("赫爾希", "赫雪"), ("施萊登", "許來登"), ("施旺", "許旺"),
    ("多普勒", "都卜勒"), ("衍射", "繞射"), ("光導纖維", "光纖"), ("鐳射", "雷射"), ("激光", "雷射"), ("晶狀體", "水晶體"), ("核裂變", "核分裂"), ("核聚變", "核融合"), ("傳感器", "感測器"),
    ("內阻", "內電阻"), ("路端電壓", "端電壓"), ("零線", "中性線"), ("試電筆", "驗電筆"), ("空氣開關", "斷路器"), ("電動機", "馬達"), ("平拋運動", "水平拋射運動"), ("平拋", "水平拋射"),
    ("參考系", "參考座標"), ("線粒體", "粒線體"), ("高爾基體", "高基氏體"), ("溶酶體", "溶體"), ("氨基酸", "胺基酸"), ("種群", "族群"), ("生態系統", "生態系"), ("自然選擇", "天擇"),
    ("標記重捕法", "捉放法"), ("暗反應", "碳反應"), ("膠頭滴管", "滴管"), ("托盤天平", "天平"), ("化肥", "化學肥料"), ("塑料", "塑膠"), ("滌綸", "聚酯纖維"), ("可燃冰", "甲烷水合物"),
    ("金屬活動性順序", "金屬活性大小順序"), ("泥石流", "土石流"), ("滑坡", "山崩"), ("遙感", "遙測"), ("洪澇", "水災"), ("千克", "公斤"), ("厘米", "公分"), ("毫米", "公釐"), ("“", "「"), ("”", "」"), ("‘", "『"), ("’", "』"),
]
ENZ = re.compile(r"(?<![一-鿿])酶")
LEAKS = ["我國", "中國", "全國", "我們國家", "人教", "教科版", "長江", "黃河", "北京", "上海", "天宮", "神舟", "嫦娥", "南水北調", "西電東送", "西氣東輸", "三峽", "青藏", "侯德榜",
         "億畝", "碳達峰", "碳中和", "人民幣", "北斗衛星", "北斗系統", "「北斗」", "華北", "東北地區", "西北地區", "東北平原", "江淮", "華南", "珠江", "黃土", "塔里木", "新疆", "西藏", "內蒙古", "四川", "雲南", "廣西", "海南", "桂林", "石林",
         "袁隆平", "屠呦呦", "錢學森", "天問", "祝融", "玉兔", "天眼", "蛟龍", "奮鬥者", "華龍", "港珠澳", "東方紅", "兩彈", "秦嶺", "淮河", "華山", "渭河", "鄭州", "武漢", "一帶一路",
         "中歐", "抗美", "五星", "國旗", "三江源", "塞罕壩", "三北", "大熊貓", "東北虎", "長城", "故宮", "敦煌", "杭州", "廣州", "深圳", "香港", "澳門", "南京", "重慶", "天津",
         "哈爾濱", "拉薩", "昆明", "貴陽", "成都", "西安", "蘭州", "烏魯木齊", "延安", "濟南", "青島", "廈門", "福州", "南昌", "長沙", "太原", "石家莊", "呼和浩特", "銀川", "西寧",
         "神農架", "九寨溝", "黃山", "泰山", "洞庭", "鄱陽", "太湖", "青海", "漠河", "曾母", "黑龍江", "珠穆朗瑪", "喜馬拉雅山脈是", "我們的祖國", "中華民族"]


def conv(s):
    if not isinstance(s, str):
        return s
    s = _S2T.convert(s)
    for a, b in TERMS:
        s = s.replace(a, b)
    s = ENZ.sub("酵素", s)
    return s


def leak(s):
    t = re.sub(r"<[^>]+>", "", s)
    return [w for w in LEAKS if w in t]


def tw_it(q, a, wrong, e):
    q, a, e = conv(q), conv(a), conv(e)
    wrong = [conv(w) for w in wrong]
    if any(leak(x) for x in [q, a, e] + wrong):
        return None
    try:
        return item(q, a, wrong, e)
    except AssertionError:
        return None


# cn の部品を読み込む前に it を差し替える
cn_sci.it = tw_it
cn_sci._ok_text = lambda s, where: s


def _clean(xs):
    return [x for x in xs if not leak(conv(x if isinstance(x, str) else "".join(str(y) for y in (x if not isinstance(x, dict) else x.values()))))]


ADD = {      # cn の表の最初の行の見出し（简体）→ 台灣の行を足す
    "青藏高原": [("中央山脈", "山地"), ("玉山山脈", "山地"), ("嘉南平原", "平原"), ("蘭陽平原", "平原"), ("屏東平原", "平原"), ("臺北盆地", "盆地"), ("埔里盆地", "盆地"), ("臺中盆地", "盆地"),
                ("竹東丘陵", "丘陵"), ("林口台地", "台地"), ("八卦山台地", "台地")],
    "大熊猫": [("臺灣黑熊", "臺灣特有亞種，胸前有 V 字形白色斑紋"), ("櫻花鉤吻鮭", "冰河時期遺留在臺灣高山溪流的珍稀魚類，被稱為「國寶魚」"), ("臺灣藍鵲", "臺灣特有種鳥類，羽毛藍色、尾羽很長"),
               ("石虎", "臺灣僅存的原生貓科動物，數量稀少"), ("帝雉", "臺灣特有種雉類，又稱黑長尾雉"), ("臺灣杉", "臺灣高大的針葉樹，常長成巨木"), ("中華白海豚", "在臺灣西部沿海出沒的瀕危海豚"),
               ("穿山甲", "身上有鱗片、以螞蟻和白蟻為食的哺乳動物"), ("綠蠵龜", "會回到澎湖望安島沙灘產卵的海龜")],
}
ADD_G = {}    # K.G のグループ名（简体）→ {グループ: [物]}
ADD_TF = {   # K.TF の topic（简体）→ ([正しい文], [(まちがい, 正しくは)])
    "生物的分类和多样性": (["臺灣地形高低起伏大，生物多樣性很豐富。", "設立國家公園和保護區是保護生物多樣性的方法。"], [("臺灣面積小，所以特有種很少。", "臺灣有許多特有種，如臺灣黑熊、臺灣藍鵲。")]),
}
ADD_B = {    # K.B の最初の問題文（简体）→ [行]
    "威胁生物多样性的主要原因是什么？": [("臺灣第一座國家公園是哪一座？", "墾丁國家公園", ["太魯閣國家公園", "玉山國家公園", "雪霸國家公園"], "墾丁國家公園在 1984 年成立。"),
                                    ("為了保護櫻花鉤吻鮭，主要保護哪裡的溪流？", "雪霸國家公園的七家灣溪", ["墾丁的南灣", "澎湖的望安島", "臺北的淡水河口"], "櫻花鉤吻鮭生活在大甲溪上游的七家灣溪。"),
                                    ("在澎湖望安島設立保護區，主要是保護哪種動物？", "綠蠵龜", ["臺灣黑熊", "石虎", "帝雉"], "綠蠵龜會到望安島的沙灘產卵。"),
                                    ("石虎數量減少的原因不包括哪一項？", "氣候太冷", ["棲地被開發破壞", "被車輛撞死（路殺）", "誤食毒餌"], "保護石虎要保護淺山的棲地。")],
}


class TK(cn_sci.K):
    def P(self, rows, fwd, back=None, *a, **kw):
        extra = ADD.get(rows[0][0], [])
        rows = [r for r in rows if not leak(conv("".join(r[:2])))] + extra
        return cn_sci.K.P(self, rows, fwd, back, *a, **kw)

    def G(self, groups, *a, **kw):
        g = {k: [x for x in v if not leak(conv(x))] for k, v in groups.items() if not leak(conv(k))}
        for k, v in ADD_G.get(sorted(groups)[0], {}).items():
            g.setdefault(k, []).extend(v)
        return cn_sci.K.G(self, g, *a, **kw)

    def TF(self, true, false, topic):
        t2, f2 = ADD_TF.get(topic, ([], []))
        true = [x for x in true if not leak(conv(x))] + t2
        false = [x for x in false if not leak(conv(x[0] + x[1]))] + f2
        return cn_sci.K.TF(self, true, false, topic)

    def B(self, rows):
        rows = list(rows) + ADD_B.get(rows[0][0], [])
        its = [x for x in (tw_it(*r) for r in rows) if x]
        R = self
        import copy

        def mk():
            return copy.deepcopy(R.R.choice(its)) if its else None
        mk.n = len(its)
        return mk


STAGE = {3: "第二學習階段（國小三、四年級）", 4: "第二學習階段（國小三、四年級）", 5: "第三學習階段（國小五、六年級）", 6: "第三學習階段（國小五、六年級）",
         7: "第四學習階段（國中）", 8: "第四學習階段（國中）", 9: "第四學習階段（國中）", 10: "第五學習階段（高中）", 11: "第五學習階段（高中）", 12: "第五學習階段（高中）"}
GNAME = {3: "國小三年級", 4: "國小四年級", 5: "國小五年級", 6: "國小六年級", 7: "國中七年級", 8: "國中八年級", 9: "國中九年級", 10: "高中一年級", 11: "高中二年級", 12: "高中三年級"}
DOM_EL = {"M": "物質與能量", "L": "生命世界", "E": "地球與太空", "T": "科技與工程"}
STD_URL = "https://www.naer.edu.tw/upload/1/16/doc/820/十二年國民基本教育課程綱要國民中小學暨普通型高級中等校-自然科學領域.pdf"
UPDATED = "2026-11-28"

# (cn の学年, cn の slug, 台灣の領域名)   国中は 生物 / 理化 / 地球科學、高中は 物理 / 化學 / 生物 / 地球科學
P, C, B, ES = "物理", "化學", "生物", "地球科學"
GRADES = {
    3: [(3, s, None) for s in ["water", "air", "weather", "motion-of-objects", "life-cycle-of-animals", "sun-earth-and-moon"]] + [(1, "plants", None), (1, "animals", None), (2, "magnets", None)],
    4: [(4, s, None) for s in ["sound", "breathing-and-digestion", "motion-and-force", "growth-of-plants", "electric-circuits", "rocks-and-soil"]],
    5: [(5, s, None) for s in ["light", "changes-of-earths-surface", "measuring-time", "healthy-living", "living-things-and-environment", "ship-research", "heat", "environment-and-us"]],
    6: [(6, s, None) for s in ["the-tiny-world", "motion-of-the-earth", "energy", "tools-and-technology", "little-engineers", "biodiversity", "changes-of-matter", "the-universe"]],
    7: [(7, s, B) for s in ["living-things-and-the-biosphere", "the-cell", "levels-of-organization", "green-plants", "photosynthesis-and-respiration", "nutrition-and-digestion",
                            "breathing-and-circulation", "excretion-and-regulation", "human-reproduction-and-development"]]
       + [(8, s, B) for s in ["reproduction-and-development", "heredity-and-variation", "evolution-of-life", "major-groups-of-animals", "animal-movement-and-behavior",
                              "bacteria-fungi-and-viruses", "classification-and-biodiversity", "infectious-disease-and-health"]],
    8: [(8, s, "理化") for s in ["mass-and-density", "sound-phenomena", "light-phenomena", "lenses-and-their-applications", "changes-of-state"]]
       + [(9, s, "理化") for s in ["internal-energy", "heat-engines", "into-the-world-of-chemistry", "air-and-oxygen", "atoms-molecules-and-elements", "water-and-chemical-formulas",
                                 "chemical-equations", "solutions", "metals-and-metal-materials", "acids-and-bases", "salts-and-fertilizers", "carbon-and-its-oxides", "combustion-and-fuels", "chemistry-and-life"]],
    9: [(8, s, "理化") for s in ["mechanical-motion", "force", "motion-and-force-8", "pressure", "buoyancy", "work-and-mechanical-energy", "simple-machines"]]
       + [(9, s, "理化") for s in ["current-and-circuits", "voltage-and-resistance", "ohms-law", "electric-power", "household-electricity", "electricity-and-magnetism", "information-and-energy"]]
       + [(7, "land-and-ocean", ES), (11, "plate-tectonics-and-landforms", ES), (7, "weather-and-climate", ES), (11, "weather-systems", ES)],
    10: [(10, s, P) for s in ["describing-motion", "force-and-motion-relationships", "universal-gravitation-and-spaceflight", "work-energy-and-mechanical-energy"]] + [(12, "quantum-and-atomic-structure", P)]
        + [(10, s, C) for s in ["amount-of-substance", "periodic-law-and-chemical-bonds", "redox-reactions", "reaction-energy-and-rate", "organic-compounds"]]
        + [(10, s, B) for s in ["molecules-of-the-cell", "cell-structure", "transport-across-membranes", "enzymes-and-atp", "cellular-respiration-and-photosynthesis", "cell-cycle-and-differentiation"]]
        + [(10, s, ES) for s in ["earth-in-the-universe", "atmosphere-on-earth", "water-on-earth", "landforms", "natural-disasters"]],
    11: [(10, s, P) for s in ["uniformly-accelerated-motion", "forces-and-equilibrium", "projectile-and-circular-motion"]] + [(11, s, P) for s in ["momentum-and-its-conservation", "mechanical-vibrations-and-waves", "light"]]
        + [(10, s, C) for s in ["classification-and-ionic-reactions", "sodium-and-chlorine", "iron-and-metal-materials", "sulfur-nitrogen-and-silicon"]]
        + [(11, s, C) for s in ["thermochemistry", "atomic-structure-and-properties", "molecular-structure-and-properties", "crystal-structure-and-properties"]]
        + [(10, s, B) for s in ["mendelian-inheritance", "meiosis-and-sex-linked-inheritance", "dna-structure-and-replication", "gene-expression", "mutation-and-breeding", "evolution-and-speciation"]]
        + [(11, s, ES) for s in ["earth-motions", "atmospheric-circulation-and-climate", "ocean-currents"]],
    12: [(11, s, P) for s in ["electrostatic-field", "circuits-and-electrical-energy", "magnetic-forces-on-currents-and-charges", "electromagnetic-induction-and-alternating-current"]]
        + [(12, s, P) for s in ["molecular-kinetic-theory-and-gases", "laws-of-thermodynamics", "atomic-nucleus"]]
        + [(11, s, C) for s in ["reaction-rate-and-chemical-equilibrium", "ionic-equilibria-in-solution", "electrochemistry"]]
        + [(12, s, C) for s in ["organic-compounds-and-hydrocarbons", "hydrocarbon-derivatives", "biomolecules-and-polymers"]]
        + [(11, s, B) for s in ["homeostasis-and-nervous-regulation", "hormonal-regulation", "immune-regulation", "plant-life-regulation", "populations", "communities", "ecosystems", "humans-and-the-environment"]]
        + [(12, s, B) for s in ["fermentation-engineering", "cell-engineering", "genetic-engineering"]],
}
OVR = {}   # slug → {欄: 値}（cn の欄をそのまま差し替える）
FIX = {    # slug → [(台灣の文に直したあとの古い文, 新しい文)]（説明・FAQ の中国の話を台灣の話に）
    "changes-of-earths-surface": [("四川盆地是什麼地形？", "臺北盆地是什麼地形？"), ("黃河為什麼是黃色的？", "颱風過後，河水為什麼變得很混濁？"), ("流經黃土高原，帶走大量泥沙。", "大雨沖刷山坡，河水帶走大量泥沙。"),
                                  ("我國為什麼地震比較多？", "臺灣為什麼地震比較多？"), ("我國處在兩大地震帶之間，板塊運動活躍。", "臺灣位在歐亞板塊和菲律賓海板塊的交界，板塊運動活躍。"), ("中國的地形", "臺灣的地形")],
    "measuring-time": [("我國古代還用<b>圭表</b>測定節氣。", "古代還用<b>圭表</b>測定節氣。")],
    "motion-of-the-earth": [("北京時間是東八區的時間。", "臺灣使用東八區的時間。"), ("北京和烏魯木齊，誰先看到日出？", "臺灣和日本東京，誰先看到日出？"), ("東邊先迎來太陽。'], '北京')", "東邊先迎來太陽。'], '日本東京')"),
                            ("為什麼我國北方夏天白天長？", "為什麼夏天白天比較長？"), ("北京", "日本東京")],
    "biodiversity": [("我國有大熊貓、金絲猴、揚子鱷、銀杏、珙桐等珍稀動植物，建立自然保護區保護它們。", "臺灣有臺灣黑熊、櫻花鉤吻鮭、臺灣藍鵲、臺灣杉等珍稀動植物，設立國家公園和保護區保護它們。")],
    "the-universe": [("，瞭解我國航天事業的成就", "，瞭解人類探索太空的成就"), ("我國的神舟飛船、天宮空間站、嫦娥探月、天問一號探火都取得了成就。", "人類用太空船、太空站和探測器探索月球、火星和更遠的太空，臺灣也發射了福衛系列人造衛星。"),
                     ("我國的空間站叫什麼？", "國際太空站是什麼？"), ("天宮空間站。", "多個國家合作建造、在地球軌道上運行的太空站。")],
    "information-and-energy": [("我國的「北斗」系統是什麼？", "衛星導航系統（GPS）是什麼？"), ("我國自主建設的衛星導航系統。", "利用多顆人造衛星發出的訊號，確定位置和時間的系統。")],
    "land-and-ocean": [("我國為什麼多地震？", "臺灣為什麼多地震？"), ("位於亞歐板塊東南部，受太平洋板塊和印度洋板塊擠壓。", "位於歐亞板塊和菲律賓海板塊的交界，兩個板塊互相擠壓。")],
    "weather-and-climate": [("為什麼新疆降水少？", "為什麼沙漠地區降水少？"), ("深居內陸，距海遠，", "多深居內陸，距海遠，")],
    "weather-systems": [("為什麼江淮地區有「梅雨」？", "臺灣為什麼有「梅雨」？"), ("在江淮地區形成滯留鋒，帶來連續降水。", "5、6 月在臺灣附近形成滯留鋒，帶來連續降水。")],
    "universal-gravitation-and-spaceflight": [("我國有哪些航天成就？", "人類有哪些太空探索的成就？"), ("神舟載人飛船、天宮空間站、嫦娥探月、天問一號火星探測等。", "登陸月球、國際太空站、火星探測車等；臺灣也發射了福衛系列人造衛星。")],
    "earth-in-the-universe": [("為什麼我國青藏高原太陽能豐富？", "為什麼高山上太陽輻射比較強？")],
    "water-on-earth": [("為什麼長江口附近海水鹽度較低？", "為什麼大河出海口附近海水鹽度較低？")],
    "landforms": [("地上有峰林、石林，地下有溶洞。", "地上有峰林、石灰岩柱，地下有鐘乳石洞。"), ("桂林山水是什麼地貌？", "墾丁的石灰岩洞是怎樣形成的？"), ("'喀斯特地貌')", "'石灰岩被流水溶蝕（喀斯特作用）')")],
    "natural-disasters": [("我國常見的<b>氣象災害</b>", "臺灣常見的<b>氣象災害</b>"), ("有洪澇、乾旱、颱風、寒潮", "有颱風、豪雨、乾旱、寒流"), ("、北斗衛星導航系統</b>", "、衛星導航系統</b>"),
                          ("為什麼我國東部季風區旱澇頻繁？", "為什麼臺灣容易發生水災和乾旱？"), ("夏季風的強弱和進退時間每年不同，降水的季節和年際變化大。", "降水集中在梅雨和颱風季節，而且每年的雨量變化大，河川短、坡度大，水不容易留住。")],
    "earth-motions": [("北京時間 12:00 時", "臺灣時間（120°E）12:00 時"), ("為什麼我國北方樓房間距要比南方大？", "為什麼緯度高的地方樓房間距要比較大？")],
    "atmospheric-circulation-and-climate": [("，我國東部季風氣候顯著。", "，臺灣和東亞的季風氣候很明顯。")],
    "populations": [("我國為什麼實施三孩生育政策？", "臺灣為什麼要關注少子化？"), ("調整人口年齡結構，應對人口老齡化。", "出生率低會使人口年齡結構老化，需要鼓勵生育並因應高齡化。")],
    "classification-and-biodiversity": [("我國的珍稀動植物", "臺灣的珍稀動植物"), ("建立臥龍自然保護區保護大熊貓屬於什麼措施？", "設立雪霸國家公園保護櫻花鉤吻鮭屬於什麼措施？"), ("袁隆平培育雜交水稻利用了什麼？", "培育雜交水稻新品種利用了什麼？")],
    "genetic-engineering": [("我國對轉基因產品有什麼規定？", "臺灣對基因改造食品有什麼規定？"), ("實行安全評價和標識管理制度。", "要經過安全評估，並且依規定標示。")],
}


def cn_unit(cg, slug):
    for u in importlib.import_module(cn_sci.module_of(cg)).UNITS(cg):
        if u["slug"] == slug:
            return u
    raise KeyError((cg, slug))


def part_of(g, dom):
    if g <= 9:
        return dom or ""
    return ("部定必修" if g == 10 else "加深加廣選修") + dom


def build(g, cg, slug, dom, sort, check=None):
    u = dict(cn_unit(cg, slug))
    u.update(OVR.get(slug, {}))
    fx = FIX.get(slug, [])

    def cv(t):
        t = conv(t)
        for a, b in fx:
            t = t.replace(a, b)
        return t
    U_ = Unit(96000 + 100 * g + sort)
    spec = u["sets"](TK(U_.R))
    try:
        sets = U_.sets(spec)
    except AssertionError:
        # 問題が少し足りないときは、同じ単元の他のセットの部品を少しずつ足す
        U_ = Unit(96000 + 100 * g + sort)
        spec = u["sets"](TK(U_.R))
        allm = [m for _, ms in spec for m, _ in ms]
        spec = [(t, ms + [(m, 3) for m in allm if m not in [x for x, _ in ms]]) for t, ms in spec]
        sets = U_.sets(spec)
    for s in sets:
        s["title"] = cv(s["title"])
        assert not leak(s["title"]), (slug, s["title"])
    dname = dom or DOM_EL[u["dom"]]
    sub = "自然科學" if g <= 6 else dname
    u["ex"] = [(cv(q), [cv(x) for x in st], cv(an)) for q, st, an in u["ex"]]
    body = cv(cn_sci.lesson(u["think"], u["ex"], u["mist"]))
    f = {k: cv(u[k]) for k in ("title", "short", "std", "what", "kb", "ks")}
    faq = [{"q": cv(q), "a": cv(a)} for q, a in u["faq"]]
    bad = {}
    for k, v in list(f.items()) + [("body", body)] + [("faq", x["q"] + x["a"]) for x in faq]:
        if leak(v):
            bad[k] = leak(v)
    if check is not None:
        check[slug] = bad
        return
    assert not bad, (slug, bad)
    code = "%s · %s" % (STAGE[g], dname if g <= 9 else part_of(g, dom))
    cn_sci.write_unit("tw", "science", "grade-%d" % g, {
        "slug": slug, "title": f["title"], "seo_title": "%s｜%s%s練習題（附解答）" % (f["title"], GNAME[g], sub),
        "short_title": f["short"], "domain": dname, "standard_code": code, "standard_url": STD_URL,
        "standard_text": f["std"] + "（108課綱自然科學領域學習內容摘要）",
        "meta_desc": "%s%s「%s」免費學習單：%s，100題線上練習馬上對答案，附可列印解答。" % (GNAME[g], sub, f["title"], f["what"]),
        "key_big": f["kb"], "key_sub": f["ks"], "body_html": body, "faq": faq, "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


def main():
    g = int(sys.argv[1])
    only = [a for a in sys.argv[2:] if a != "--check"]
    chk = {} if "--check" in sys.argv else None
    for i, (cg, slug, dom) in enumerate(GRADES[g]):
        if only and slug not in only and str(i + 1) not in only:
            continue
        try:
            build(g, cg, slug, dom, i + 1, chk)
        except AssertionError as ex:
            if chk is None:
                raise
            chk[slug] = "ERR " + str(ex)[:120]
            continue
        if chk is None:
            print("wrote", g, slug)
    if chk is not None:
        for k, v in chk.items():
            if v:
                print(k, v)


if __name__ == "__main__":
    import tw_sci
    tw_sci.main()
