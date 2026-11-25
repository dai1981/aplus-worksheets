# -*- coding: utf-8 -*-
"""Türkiye okul öncesi (60–72 ay, Maarif Modeli Okul Öncesi Eğitim Programı 2024, Matematik alanı MAB)。
10’a kadar（ritmik sayma 20’ye kadar）、とても短い文、ほぼ全問に絵。問題関数は tr_p12（1. sınıf と共有）＋自前。"""
from tr_s3a import unit
from tr_common import num
import tr_p12 as T
from tr_p12 import *  # noqa: F401,F403


def setup(rnd):
    pass


def lim(mk, mx=10):
    """数の答え・選択肢が mx を超える問題を落とす"""
    import re

    def f():
        it = mk()
        if not it:
            return None
        q = re.sub(r"<svg.*?</svg>", "", it["q"], flags=re.S)
        for c in it["c"] + [q]:
            for n in re.findall(r"\d+", re.sub(r"<[^>]+>", "", c)):
                if int(n) > mx:
                    return None
        return it
    f.__name__ = mk.__name__
    return f


def bakista():
    def f():
        k = ri(0, 2)
        n = ri(1, 5)
        if k == 0:
            v = [n] if rnd() < 0.6 or n < 2 else [ri(1, n - 1)]
            if len(v) == 1 and rnd() < 0.4 and n >= 2:
                a = ri(1, n - 1)
                v = [a, n - a]
            s = sum(v)
            return mq("Zara bir bak. Saymadan söyle: kaç nokta var?%s" % zar(v), num(s), near(s, 1, 10, (1, -1, 2)), "Bir bakışta görürüz: <b>%d</b> nokta." % s)
        kind = ch(KINDS)
        if k == 1:
            return mq("Resme bir bak. Kaç %s var?%s" % (b(kind), dagin(n, kind)), num(n), near(n, 1, 10, (1, -1, 2)), "Bir bakışta görürüz: <b>%d</b> %s." % (n, b(kind)))
        return mq("Onluk çerçevede kaç nokta var?%s" % cerceve(n + ri(0, 5)), None, [], "") if False else (lambda m: mq("Onluk çerçevede kaç nokta var?%s" % cerceve(m), num(m), near(m, 1, 10, (1, -1, 5)), "Üst sıra 5 nokta alır. <b>%d</b> nokta var." % m))(ri(1, 10))
    return named(f, "bakista")


ACC = {"apple": "elmayı", "star": "yıldızı", "ball": "topu", "button": "düğmeyi", "fish": "balığı", "flower": "çiçeği",
       "duck": "ördeği", "cup": "bardağı", "bug": "uğur böceğini"}


def paylastir():
    def f():
        n = ri(1, 5) * 2
        kind = ch(KINDS)
        x = nm()
        k = ri(0, 2)
        if k == 0:
            q = "%s, %d %s iki arkadaşına eşit paylaştırıyor. Her biri kaç %s alır?%s" % (x, n, ACC[kind], b(kind), sira(n, kind))
        elif k == 1:
            q = "%d %s iki kutuya eşit olarak konuluyor. Her kutuda kaç %s olur?%s" % (n, b(kind), b(kind), sira(n, kind))
        else:
            q = "%d %s iki tabağa eşit olarak dağıtılıyor. Bir tabakta kaç %s olur?%s" % (n, b(kind), b(kind), sira(n, kind))
        return mq(q, num(n // 2), [num(v) for v in (n // 2 + 1, n // 2 - 1, n, n // 2 + 2) if 0 < v != n // 2], "İkiye eşit ayırırız: <b>%d</b> ve %d." % (n // 2, n // 2))
    return named(f, "paylastir")


def esit_mi():
    def f():
        a, c = ri(1, 10), ri(1, 10)
        if a + c > 10 or a == c and rnd() < 0.5:
            return None
        k1, k2 = ch(KINDS), ch(KINDS)
        g = "Eşit paylaştırılmış" if a == c else "Eşit paylaştırılmamış"
        return mq("Ali’nin tabağında %d %s, Ece’nin tabağında %d %s var. Paylaşım eşit mi?%s" % (a, b(k1), c, b(k1), iki(a, k1, c, k1, "+")), g,
                  ["Eşit paylaştırılmamış" if a == c else "Eşit paylaştırılmış", "Bilmiyorum", "İkisi de boş"], "%d ve %d: <b>%s</b>." % (a, c, g.lower()))
    return named(f, "esit_mi")


def rakam_eslestir():
    def f():
        n = ri(0, 10)
        kind = ch(KINDS)
        k = ri(0, 1)
        if k == 0:
            return mq("Resimdeki %s sayısını hangi rakam gösterir?%s" % (b(kind), sira(n, kind) if n else "<br>(Tabakta hiç %s yok.)" % b(kind)), num(n), near(n, 0, 10, (1, -1, 2)) + ["6" if n == 9 else "9" if n == 6 else str(10 - n) if 10 - n != n else "3"],
                      "Sayarız: <b>%d</b>." % n)
        if n == 0:
            return None
        ws = [m for m in range(1, 11) if m != n]
        sh_ = sh(ws)[:3]
        return mq("%s tane %s olan resim hangisidir?<br>A) %d %s &nbsp; B) %d %s &nbsp; C) %d %s &nbsp; D) %d %s" % (cap(oku_(n)), b(kind), *[x for m in sorted(sh_ + [n]) for x in (m, b(kind))]),
                  "%s)" % "ABCD"[sorted(sh_ + [n]).index(n)], ["%s)" % L for i, L in enumerate("ABCD") if i != sorted(sh_ + [n]).index(n)], "%s = <b>%d</b>." % (cap(oku_(n)), n)) if False else None
    return named(f, "rakam")


def karsi():
    def f():
        a, c = ri(0, 10), ri(0, 10)
        if a == c:
            return None
        k = ch(["büyük", "küçük"])
        g = max(a, c) if k == "büyük" else min(a, c)
        return mq("%d ve %d sayılarından hangisi daha %stür?" % (a, c, k) if k == "büyük" else "%d ve %d sayılarından hangisi daha küçüktür?" % (a, c), num(g),
                  [num(min(a, c) if k == "büyük" else max(a, c)), "İkisi eşit", "Bilinemez"], "Sayarken %s sayı %s söylenir: <b>%d</b>." % ("büyük", "sonra", g) if k == "büyük" else "Sayarken küçük sayı önce söylenir: <b>%d</b>." % g)
    return named(f, "karsi")


def oku_(n):
    from tr_common import oku
    return oku(n)


def u1():
    sets = [("İleriye sayma", [(m_ritmik(20, (1,)), 15), (m_once_sonra(0, 20), 5)]), ("Geriye sayma", [(m_ritmik(20, (1,), down=True), 15), (m_eksik(0, 20), 5)]),
            ("Önce ve sonra", [(m_once_sonra(0, 20), 20)]), ("Eksik sayı", [(m_eksik(0, 20), 20)]), ("Karışık", [(m_once_sonra(0, 20), 10), (m_eksik(0, 20), 10)])]
    return unit("ritmik-sayma", "SAY", "MAB.1", 1, "Ritmik Sayma: 1’den 20’ye Birer Birer", "Ritmik Sayma",
                "Ritmik ve algısal sayabilme: 1 ile 20 arasında birer ritmik sayar.",
                "Okul öncesi ritmik sayma etkinliği: 1’den 20’ye ileriye ve geriye birer sayma, önce ve sonra gelen sayı, eksik sayıyı bulma. 100 soru ve cevap anahtarı.",
                "Birer birer say", "Her adımda 1 artar ya da 1 azalır.", sets,
                ["Sayıları sırayla söyleriz: bir, iki, üç…",
                 "İleriye sayarken her sayı 1 artar. Geriye sayarken her sayı 1 azalır.",
                 "Bir sayıdan hemen sonra gelen sayı 1 fazlasıdır."],
                [("5, 6, 7, …", ["Bir sonraki sayı"], "8"), ("10, 9, 8, …", ["Geriye sayıyoruz"], "7")],
                [["Bir sayıyı atlamak", "Parmakla göstererek say"], ["Geriye sayarken ileri gitmek", "Her adımda 1 azalır"], ["12 ile 21’i karıştırmak", "On iki: 1 onluk 2 birlik"]],
                [("Çocuğum nasıl çalışabilir?", "Merdiven çıkarken, oyuncak toplarken birlikte sayabilirsiniz."), ("Geriye sayma neden önemli?", "Çıkarma için hazırlıktır."),
                 ("20’ye kadar saymak yeterli mi?", "Okul öncesinde 20’ye kadar ritmik sayma hedeflenir.")])


def u2():
    sets = [("Sıralı nesneleri sayma", [(lim(m_say(1, 10)), 20)]), ("Dağınık nesneleri sayma", [(lim(m_say(1, 10)), 20)]), ("20’ye kadar sayma", [(m_say(11, 20), 20)]),
            ("Rakamla eşleştirme", [(rakam_eslestir(), 20)]), ("Sayının adı", [(lim(m_okunus(0, 10)), 20)])]
    return unit("nesne-sayma", "SAY", "MAB.1, MAB.9", 2, "Nesne Sayma: Kaç Tane Var?", "Nesne Sayma",
                "1 ile 20 arasında nesne/varlık sayısını söyler; ismi söylenen rakamı gösterir.",
                "Okul öncesi nesne sayma etkinliği: sıralı ve dağınık nesneleri sayma, 20’ye kadar sayma, sayıyı rakamla eşleştirme, sayıların adları. 100 soru ve cevap anahtarı.",
                "Son sayı kaç tane olduğunu söyler", "Her nesneyi bir kez say.", sets,
                ["Her nesneye dokunarak ya da göstererek bir kez sayarız.",
                 "Son söylediğimiz sayı, kaç tane nesne olduğunu gösterir.",
                 "Sayıyı rakamla yazabiliriz: beş → 5."],
                [("Resimde 6 top var mı?", ["bir, iki, üç, dört, beş, altı"], "6 top"), ("Yedi", ["Rakamı"], "7")],
                [["Bir nesneyi iki kez saymak", "Saydığını işaretle"], ["Dağınık nesnelerde atlamak", "Soldan sağa say"], ["6 ile 9’u karıştırmak", "Yuvarlağın yerine bak"]],
                [("Dağınık nesneler nasıl sayılır?", "Sayılanları kenara alarak ya da işaretleyerek."), ("Parmakla saymak doğru mu?", "Evet, bu yaşta çok yararlıdır."),
                 ("Evde nasıl çalışılır?", "Sofrayı kurarken tabak ve kaşık saymak iyi bir etkinliktir.")])


def u3():
    sets = [("Zar ve resimler", [(bakista(), 20)]), ("Bir bakışta söyle", [(bakista(), 20)]), ("Onluk çerçeve", [(bakista(), 10), (lim(m_say(1, 10)), 10)]),
            ("Tahmin et", [(lim(m_tahmin(10, 1)), 10), (lim(m_say(1, 10)), 10)]), ("Karışık", [(bakista(), 5), (lim(m_say(1, 10)), 15)])]
    return unit("bir-bakista-sayma", "SAY", "MAB.1", 3, "Bir Bakışta Sayma: Zar ve Onluk Çerçeve", "Bir Bakışta Sayma",
                "1 ile 5 arasında nesnelerin/varlıkların miktarını bir bakışta söyler.",
                "Okul öncesi bir bakışta sayma etkinliği: zar noktaları, az sayıda nesneyi saymadan söyleme, onluk çerçeve, tahmin etme. 100 soru ve cevap anahtarı.",
                "5’e kadar olan miktarı bir bakışta gör", "Zar ve onluk çerçeve hızlı görmeyi sağlar.", sets,
                ["Az sayıda nesneyi (5’e kadar) tek tek saymadan bir bakışta görebiliriz.",
                 "Zardaki noktaların dizilişi sayıyı hatırlamamızı kolaylaştırır.",
                 "Onluk çerçevenin üst sırası 5 noktadır; 5 ve birkaç nokta daha diye görebiliriz."],
                [("Zarda dört nokta", ["Köşelerde 4 nokta"], "4"), ("Çerçevede üst sıra dolu, altta 2", ["5 ve 2"], "7")],
                [["Zarda her noktayı tek tek saymak", "Dizilişi tanı"], ["Onluk çerçevede boşları saymak", "Dolu kutuları say"], ["Tahmini sayı sanmak", "Tahmin yaklaşık değerdir"]],
                [("Bir bakışta sayma neden önemli?", "Sayı duygusunu ve hızlı toplamayı geliştirir."), ("Hangi oyunlar yararlı?", "Zarla oynanan kutu oyunları."),
                 ("Kaça kadar bir bakışta görülür?", "Çoğu çocuk 4–5 nesneyi bir bakışta görebilir.")])


def u4():
    sets = [("Parça ve bütün", [(lim(m_parca_butun(10)), 20)]), ("Eş parçalar", [(T.m_yarim((0,)), 6), (esit_mi(), 14)]), ("Eş olanı bul", [(m_es(), 20)]),
            ("Eşit paylaşım", [(esit_mi(), 10), (paylastir(), 10)]), ("Karışık", [(lim(m_parca_butun(10)), 10), (m_es(), 10)])]
    return unit("butun-ve-parca", "MM", "MAB.2", 4, "Bütün ve Parça: Eş Parçalar", "Bütün ve Parça",
                "Bir bütünü oluşturan parçaları gösterir; eş/eşit olan ve olmayan parçaları gösterir.",
                "Okul öncesi bütün ve parça etkinliği: bir sayıyı iki parçaya ayırma, yarım ve çeyrek, eş şekilleri bulma, eşit paylaşımı fark etme. 100 soru ve cevap anahtarı.",
                "Parçalar birleşince bütün olur", "Eş parçalar aynı büyüklüktedir.", sets,
                ["Bir bütün parçalara ayrılabilir; parçaları birleştirince yine bütün elde ederiz: 5 = 2 ve 3.",
                 "Eş parçaların büyüklüğü aynıdır. İki eş parçanın her birine yarım deriz.",
                 "Eşit paylaşımda herkes aynı sayıda nesne alır."],
                [("5’i iki parçaya ayır", ["2 ve 3", "1 ve 4"], "5 = 2 + 3"), ("Elma iki eş parçaya bölündü", ["Her biri"], "Yarım")],
                [["Eş olmayan parçalara yarım demek", "Yarımlar eşit olmalı"], ["Parçaları toplamayı unutmak", "Bütün = parçaların toplamı"], ["Biçimi aynı ama büyüklüğü farklı şekli eş sanmak", "Eşler aynı büyüklükte"]],
                [("Evde nasıl çalışılır?", "Ekmeği, meyveyi ikiye bölerken “yarım” kelimesini kullanın."), ("Parça-bütün neden önemli?", "Toplama ve çıkarmanın temelidir."),
                 ("Eş ne demek?", "Biçimi ve büyüklüğü aynı demektir.")])


def u5():
    sets = [("Şekillerin adı", [(m_sekil_ad(), 20)]), ("Şekli bul", [(m_sekil_bul(), 20)]), ("Kenar ve köşe", [(m_kenar(("triangle", "square", "rectangle")), 10), (m_sekil_gercek(), 10)]),
            ("Cisimler", [(m_cisim_ad(), 10), (m_cisim_gercek(), 10)]), ("Kaç tane?", [(lim(m_sekil_say()), 10), (m_yuvarlanir(), 10)])]
    return unit("geometrik-sekiller", "MT", "MAB.3, MAB.9", 5, "Geometrik Şekiller: Daire, Üçgen, Kare, Dikdörtgen", "Geometrik Şekiller",
                "Geometrik şekillerin farklı biçimsel özelliklere sahip örneklerini oluşturur; ismi söylenen şekli gösterir.",
                "Okul öncesi geometrik şekiller etkinliği: daire, üçgen, kare, dikdörtgen, kenar ve köşe sayısı, günlük hayattaki şekiller, küp, küre, silindir. 100 soru ve cevap anahtarı.",
                "Üçgenin 3, karenin 4 kenarı var", "Dairenin köşesi yoktur.", sets,
                ["Üçgenin 3 kenarı ve 3 köşesi vardır. Karenin 4 eşit kenarı vardır.",
                 "Dikdörtgenin 4 kenarı vardır; karşılıklı kenarları eşittir. Dairenin kenarı ve köşesi yoktur.",
                 "Top küre, zar küp, bardak silindir biçimindedir."],
                [("Üç kenarlı şekil", ["Kenarları say"], "Üçgen"), ("Saat", ["Yuvarlak"], "Daire")],
                [["Kareyle dikdörtgeni karıştırmak", "Karenin bütün kenarları eşit"], ["Ters duran üçgeni üçgen saymamak", "Döndürsen de üçgen"], ["Daireyle küreyi karıştırmak", "Küre top gibi"]],
                [("Şekilleri nerede görürüz?", "Pencere dikdörtgen, saat daire, yol işareti üçgen olabilir."), ("Hangi cisim yuvarlanır?", "Küre ve silindir."),
                 ("Nasıl oynanır?", "Evde şekil avı yapın: “Kare olan bir şey bul!”")])


def u6():
    sets = [("Masada nerede?", [(m_masa(), 20)]), ("Kutuya göre konum", [(m_kutu_konum(), 20)]), ("Sağ ve sol", [(m_sag_sol(), 20)]),
            ("Rafta nerede?", [(m_raf(), 20)]), ("Yön bulma", [(m_yonerge(5), 10), (m_yon_bul(5), 10)])]
    return unit("konum-ve-yon", "MT", "MAB.3", 6, "Konum ve Yön: Üstünde, Altında, Sağında, Solunda", "Konum ve Yön",
                "Nesne/varlıkların konum, şekil gibi matematiksel özelliklerini farklı yollarla ifade eder.",
                "Okul öncesi konum ve yön etkinliği: üstünde, altında, içinde, dışında, önünde, arkasında, sağında, solunda, rafta yer, kareli zeminde yön bulma. 100 soru ve cevap anahtarı.",
                "Konumu bir nesneye göre söyleriz", "Sağ ve sol, bakan kişiye göredir.", sets,
                ["Bir nesnenin yerini başka bir nesneye göre söyleriz: kedi masanın altında.",
                 "Üstünde-altında, içinde-dışında, önünde-arkasında, sağında-solunda konum sözcükleridir.",
                 "Yön bulurken adımları sırayla izleriz: 2 kare sağa, 1 kare yukarı."],
                [("Top masanın altında", ["Masa üstte, top aşağıda"], "Altında"), ("Kalem kutunun içinde", ["Kutunun içi"], "İçinde")],
                [["Sağ ile solu karıştırmak", "Sağ el ile yemek yeriz"], ["Önünde ile arkasında karıştırmak", "Yüzünün baktığı taraf önü"], ["Adım sayısını karıştırmak", "Her kareyi tek tek say"]],
                [("Sağ ve sol nasıl öğretilir?", "Sağ ele bir bilezik takarak oyunlar oynayabilirsiniz."), ("Yön oyunları?", "Saklanan oyuncağı “iki adım ileri, bir adım sağa” diye buldurun."),
                 ("Neden önemli?", "Harita okumanın ve geometrinin ilk adımıdır.")])


def u7():
    sets = [("Uzun ve kısa", [(m_uzun(), 20)]), ("Uzun ve kısa kule", [(lim(m_kule()), 20)]), ("Ağır ve hafif", [(m_agir(), 10), (m_denge(), 10)]),
            ("Dolu ve boş", [(m_kap(), 20)]), ("Ölçme", [(lim(m_standart_olmayan()), 10), (lim(m_kac_birim()), 10)])]
    return unit("olcme-ve-karsilastirma", "MM", "MAB.4", 7, "Ölçme: Uzun–Kısa, Ağır–Hafif, Dolu–Boş", "Ölçme",
                "Nesnelerin ölçülebilir özelliklerine ilişkin çıkarımda bulunur; nesneleri karşılaştırır.",
                "Okul öncesi ölçme etkinliği: uzun ve kısa, yüksek ve alçak kuleler, ağır ve hafif, terazi, dolu ve boş kaplar, ataşla ölçme. 100 soru ve cevap anahtarı.",
                "Karşılaştırırken aynı yerden başlat", "Terazide ağır olan taraf aşağı iner.", sets,
                ["Uzunlukları karşılaştırırken nesneleri aynı çizgiden başlatırız.",
                 "Terazide ağır olan taraf aşağı iner, hafif olan yukarı çıkar.",
                 "Bir uzunluğu ataş, adım ya da karış gibi birimlerle ölçebiliriz."],
                [("Kırmızı kalem maviden uzun", ["Aynı yerden başlat"], "Kırmızı daha uzun"), ("Terazinin sol kefesi aşağıda", ["Aşağı inen ağır"], "Sol taraf ağır")],
                [["Büyük görünen nesneyi ağır sanmak", "Teraziye bak"], ["Uçları aynı hizada olmayan nesneleri karşılaştırmak", "Başlangıcı eşitle"], ["Birimleri boşluklu dizmek", "Birimler bitişik olmalı"]],
                [("Evde nasıl çalışılır?", "Ayakkabıları, kalemleri boylarına göre dizin."), ("Terazi yoksa?", "İki elde tutup hangisinin ağır olduğunu tahmin edin."),
                 ("Neden standart birim yok?", "Okul öncesinde önce ataş, karış gibi birimlerle ölçme deneyimi kazanılır.")])


def u8():
    sets = [("Örüntüyü devam ettir", [(m_oruntu(), 20)]), ("Renk ve şekil örüntüleri", [(m_oruntu(), 20)]), ("Sayı örüntüleri", [(m_ritmik(20, (1,)), 10), (m_oruntu(), 10)]),
            ("Eksik olanı bul", [(m_oruntu(), 20)]), ("Karışık", [(m_oruntu(), 10), (m_ritmik(20, (1,), down=True), 10)])]
    return unit("oruntuler", "MM", "MAB.4", 8, "Örüntüler: Sıradaki Hangisi?", "Örüntüler",
                "Kendisine sunulan örüntüyü kopyalar, kuralına uygun olarak devam ettirir ve örüntü oluşturur.",
                "Okul öncesi örüntü etkinliği: renk ve şekil örüntüleri, örüntüyü devam ettirme, eksik olanı bulma, basit sayı örüntüleri. 100 soru ve cevap anahtarı.",
                "Tekrar eden kısmı bul", "Kural bulununca sıradaki tahmin edilir.", sets,
                ["Örüntüde bir kısım tekrar eder: kırmızı, mavi, kırmızı, mavi…",
                 "Önce tekrar eden kısmı buluruz, sonra kurala göre devam ederiz.",
                 "Örüntüler renkle, şekille, sesle ya da hareketle yapılabilir."],
                [("●▲●▲●…", ["Tekrar eden: ●▲"], "▲"), ("Kırmızı, kırmızı, mavi, kırmızı, kırmızı…", ["Tekrar: kırmızı, kırmızı, mavi"], "Mavi")],
                [["Yalnızca son nesneye bakmak", "Bütün örüntüye bak"], ["Tekrar eden kısmı kısa almak", "Bir kez daha kontrol et"], ["Sırayı ters okumak", "Soldan sağa oku"]],
                [("Evde örüntü nasıl yapılır?", "Boncuk dizerek, el çırpıp ayak vurarak."), ("Örüntü neden önemli?", "Matematiksel düşünmenin ve cebirin temelidir."),
                 ("Çocuk kendi örüntüsünü yapabilir mi?", "Evet; bu programın hedeflerinden biridir.")])


def u9():
    sets = [("Çok mu az mı?", [(lim(m_cok_az(10)), 20)]), ("Büyük ve küçük sayı", [(karsi(), 20)]), ("En çok, en az", [(lim(m_en(0, 10)), 20)]),
            ("Sıra sayıları", [(m_sira_sayisi(), 20)]), ("Yarış", [(m_yaris(), 20)])]
    return unit("karsilastirma-ve-siralama", "MM", "MAB.4", 9, "Karşılaştırma ve Sıralama: Çok, Az, Birinci", "Karşılaştırma ve Sıralama",
                "Nesne, olgu ve olayları karşılaştırır; nesne gruplarındaki miktarları karşılaştırarak çıkarımlarını söyler.",
                "Okul öncesi karşılaştırma etkinliği: çok ve az, büyük ve küçük sayı, en çok ve en az, birinci, ikinci, üçüncü, yarışta sıra. 100 soru ve cevap anahtarı.",
                "Eşleştir: fazla kalan grup çoktur", "Sıra sayısı: birinci, ikinci, üçüncü.", sets,
                ["İki grubu birebir eşleştiririz; artan nesneleri olan grup daha çoktur.",
                 "Sayılardan büyük olanı sayarken daha sonra söyleriz.",
                 "Sıradaki yeri birinci, ikinci, üçüncü diye söyleriz."],
                [("5 elma ve 3 armut", ["Eşleştir", "2 elma arttı"], "Elma çok"), ("Yarışta önde olan", ["İlk gelen"], "Birinci")],
                [["Büyük resimli grubu çok sanmak", "Sayıya bak, boyuta değil"], ["Sırayı ters taraftan saymak", "Baştan say"], ["Eşit grupları farklı sanmak", "Sayıları aynıysa eşittir"]],
                [("Evde nasıl çalışılır?", "Kimin tabağında daha çok çilek var diye sorun."), ("Sıra sayıları nerede?", "Kuyrukta, yarışta, merdivenin basamaklarında."),
                 ("Eşleştirme neden önemli?", "Sayma bilmeden de çok ve az olanı bulmayı sağlar.")])


def u10():
    sets = [("Resimle toplama", [(lim(m_topla_resim(10)), 20)]), ("Eksilen nesneler", [(lim(m_cizik(10)), 20)]), ("Kutuda kaç tane?", [(lim(m_kutu(10)), 20)]),
            ("Hikâyeli problemler", [(lim(m_problem(10, "+-")), 20)]), ("Karışık", [(lim(m_topla_resim(10)), 10), (lim(m_cizik(10)), 10)])]
    return unit("artma-ve-azalma", "PC", "MAB.5", 10, "Artma ve Azalma: Kaç Tane Oldu?", "Artma ve Azalma",
                "Artma/azalma sonucunda oluşan yeni nesne sayısını söyler; matematiksel durumlara ilişkin eksik/fazla parçaları söyler.",
                "Okul öncesi artma ve azalma etkinliği: resimlerle ekleme, eksilen nesneler, kutudaki nesneleri bulma, 10’a kadar kısa hikâyeli problemler. 100 soru ve cevap anahtarı.",
                "Eklenince artar, alınınca azalır", "Önce say, sonra ekle ya da çıkar.", sets,
                ["Bir gruba nesne eklenince sayı artar: 3 elmaya 2 elma gelirse 5 elma olur.",
                 "Bir gruptan nesne alınınca sayı azalır: 6 balondan 2’si uçarsa 4 balon kalır.",
                 "Hikâyeyi dinler, nesneleri sayar ya da parmaklarla gösteririz."],
                [("3 kuş ve 2 kuş daha geldi", ["3, 4, 5"], "5 kuş"), ("6 balon, 2 tanesi uçtu", ["6, 5, 4"], "4 balon")],
                [["Uçan balonları da saymak", "Çizili olanları sayma"], ["Eklenenleri ayrı söylemek", "Hepsini birlikte say"], ["Hikâyede “kaldı” ile “oldu”yu karıştırmak", "Kaldı: azalır"]],
                [("Toplama işareti kullanılır mı?", "Okul öncesinde işaret şart değildir; nesnelerle düşünmek önemlidir."), ("Evde nasıl çalışılır?", "Oyuncakları sepete koyup çıkararak."),
                 ("Parmakla hesaplamak doğru mu?", "Evet, bu yaşta çok uygundur.")])


def u11():
    sets = [("İkiye paylaştır", [(paylastir(), 20)]), ("Eşit mi?", [(esit_mi(), 20)]), ("Yarısını ver", [(lim(T.m_yarim((1,))), 20)]),
            ("Parça ve bütün", [(lim(m_parca_butun(10)), 20)]), ("Karışık", [(paylastir(), 10), (esit_mi(), 10)])]
    return unit("paylastirma", "PC", "MAB.5", 11, "Paylaştırma: İki Kişiye Eşit Dağıt", "Paylaştırma",
                "Sayısı 10’a kadar olan nesneleri iki kişiye/kutuya paylaştırır; matematiksel problemlerin parçaları arasındaki ilişkileri açıklar.",
                "Okul öncesi paylaştırma etkinliği: 10’a kadar nesneleri iki kişiye ya da iki kutuya eşit paylaştırma, paylaşım eşit mi, yarısını verme. 100 soru ve cevap anahtarı.",
                "Birer birer dağıt, eşit olsun", "İki kişiye eşit paylaşırsak ikisi de aynı sayıda alır.", sets,
                ["Nesneleri sırayla birer birer dağıtırız: bir sana, bir bana.",
                 "Eşit paylaşımda herkes aynı sayıda nesne alır.",
                 "Bir grubun yarısı, onu iki eşit gruba ayırınca bir grupta kalan sayıdır."],
                [("6 kurabiye, 2 çocuk", ["Birer birer dağıt"], "3’er kurabiye"), ("Ali 4, Ece 2 elma", ["Sayılar farklı"], "Eşit değil")],
                [["Birine fazla vermek", "Sayıları karşılaştır"], ["Toplam sayıyı söylemek", "Bir kişinin payını söyle"], ["Tek sayıda nesneyi eşit paylaşmaya çalışmak", "Bir tane artar"]],
                [("Evde nasıl çalışılır?", "Meyve ve oyuncakları kardeşler arasında birlikte paylaştırın."), ("Neden birer birer dağıtmak?", "Eşitliği görmeyi kolaylaştırır."),
                 ("Paylaştırma neye hazırlar?", "İlkokulda bölmeye hazırlar.")])


def u12():
    sets = [("Nesne grafiği", [(lim(m_veri(5, "nesne")), 20)]), ("Çetele", [(m_cetele(20), 20)]), ("Çetele tablosu", [(lim(m_veri(5, "cetele")), 20)]),
            ("Karar verme", [(lim(m_karar(5)), 20)]), ("Karışık", [(lim(m_veri(5, "nesne")), 10), (m_cetele(20), 10)])]
    return unit("veri-toplama-ve-grafik", "VK", "MAB.11, MAB.12, MAB.13, MAB.14", 12, "Veri Toplama, Çetele ve Nesne Grafiği", "Veri ve Grafik",
                "Araştırılabilecek problemler belirler, veri toplar, verilerin somut modelini oluşturur, analiz eder ve sonuçları çeşitli yollarla ifade eder.",
                "Okul öncesi veri etkinliği: nesne grafiği okuma, çetele ile sayma, çetele tablosu, en çok ve en az seçilen, veriye göre karar verme. 100 soru ve cevap anahtarı.",
                "Topla, say, göster, karar ver", "En uzun sütun en çok seçilendir.", sets,
                ["Bir soru sorup cevapları toplarız: “Hangi meyveyi seversin?”",
                 "Cevapları çetele ya da nesne grafiğiyle gösteririz.",
                 "Grafiğe bakarak en çok ve en az seçileni bulur, karar veririz."],
                [("Elma 4, muz 2, çilek 5", ["En uzun sıra"], "Çilek en çok"), ("Çetelede ||||", ["Çizgileri say"], "4")],
                [["Simge yerine satırı saymak", "Her simge 1 kişi"], ["Çetelede beşli grubu yanlış saymak", "Çapraz çizgi 5’inci"], ["En az ile en çoku karıştırmak", "Kısa sıra: en az"]],
                [("Okul öncesinde grafik mi?", "Evet; somut nesnelerle ve resimlerle yapılan grafikler kullanılır."), ("Evde nasıl çalışılır?", "Aile üyelerinin sevdiği renkleri sorup çizgi çekin."),
                 ("Neden önemli?", "Veriye dayalı karar vermeyi öğretir.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12]
