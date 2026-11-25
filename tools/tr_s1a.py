# -*- coding: utf-8 -*-
"""Türkiye 1. sınıf (Maarif Modeli, İlkokul Matematik 2024)。20’ye kadar（ritmik sayma 100’e kadar）、とても短い文、ほぼ全問に絵。問題関数は tr_p12。"""
from tr_s3a import unit
from tr_common import mcq, num
import tr_p12 as T
from tr_p12 import *  # noqa: F401,F403


def setup(rnd):
    pass


def zar_m():
    def f():
        v = [ri(1, 6)] + ([ri(1, 6)] if rnd() < 0.5 else [])
        return mq("Zarlarda toplam kaç nokta var?" + zar(v), num(sum(v)), near(sum(v), 1, 12, (1, -1, 2)), "Noktaları sayarız: <b>%d</b>." % sum(v))
    return named(f, "zar")


def onluk_m():
    def f():
        o = ri(1, 10)
        return mq("10 + %d = ?" % o if o < 10 else "10 + 10 = ?", num(10 + o), [num(o), num(10 + o + 1), num(10 + o - 1), num(o * 10) if o > 1 else "100"],
                  "1 onluk ve %d birlik: <b>%d</b>." % (o, 10 + o))
    return named(f, "onluk")


def u1():
    sets = [("Nesneleri sayma", [(m_say(1, 20), 20)]),
            ("Okuma ve yazma", [(m_okunus(0, 20), 20)]),
            ("Zar ve onluk çerçeve", [(zar_m(), 10), (onluk_m(), 10)]),
            ("Önce ve sonra", [(m_once_sonra(0, 20), 20)]),
            ("Eksik sayılar", [(m_eksik(0, 20), 20)])]
    return unit("20ye-kadar-sayilar", "S", "MAT.1.1.1, MAT.1.1.2", 1, "20’ye Kadar Sayılar: Sayma, Okuma ve Yazma", "20’ye Kadar Sayılar",
                "Rakamları ve 20’ye kadar olan sayıları (20 dâhil) niceliklerin büyüklüklerini temsil etmek için kullanır; dağınık veya düzenli nesne gruplarını sayarken parçalar arasındaki ilişkileri çözümler.",
                "1. sınıf 20’ye kadar sayılar çalışma kâğıdı: nesne sayma, onluk çerçeve ve zar, sayıları okuma ve yazma, önce ve sonra gelen sayı, eksik sayılar. 100 soru ve cevap anahtarı.",
                "Birer birer say", "Son söylediğin sayı, nesnelerin sayısıdır.", sets,
                ["Nesneleri birer birer sayarız. Her nesneyi yalnızca bir kez sayarız.",
                 "Son söylediğimiz sayı, gruptaki nesnelerin sayısıdır.",
                 "Bir sayıdan hemen sonra gelen sayı 1 fazlasıdır; hemen önce gelen sayı 1 eksiğidir."],
                [("Resimde 7 elma var mı?", ["bir, iki, üç, dört, beş, altı, yedi"], "7 elma"), ("13 sayısından sonra gelen sayı", ["13 + 1"], "14")],
                [["Bir nesneyi iki kez saymak", "Saydığın nesneyi işaretle"], ["Önce gelen sayıyı sonraki sanmak", "Önce: 1 eksik, sonra: 1 fazla"],
                 ["6 ile 9’u karıştırmak", "6’nın yuvarlağı altta, 9’un yuvarlağı üstte"]],
                [("Dağınık nesneleri nasıl sayarız?", "Soldan sağa ya da yukarıdan aşağıya sayarız ve saydıklarımızı işaretleriz."),
                 ("Onluk çerçeve nedir?", "İki sırada beşer kutu olan 10 kutuluk bir çerçevedir. Sayıları hızlı görmeye yardım eder."),
                 ("19’dan sonra hangi sayı gelir?", "20 gelir: yirmi.")])


def u2():
    sets = [("Soldan ve sağdan sıra", [(m_sira_sayisi(), 20)]),
            ("Kaçıncı sırada?", [(m_sira_sayisi(), 20)]),
            ("Yarış ve sıra", [(m_yaris(), 20)]),
            ("Raflarda sıra", [(m_raf(), 20)]),
            ("Karışık", [(m_sira_sayisi(), 10), (m_yaris(), 10)])]
    return unit("sira-sayilari", "S", "MAT.1.1.3", 2, "Sıra Sayıları: Birinci, İkinci, Üçüncü", "Sıra Sayıları",
                "Nesnelerin sıra sayısını gösterir; bir sıradaki nesnenin yerini soldan, sağdan, baştan ve sondan belirtir.",
                "1. sınıf sıra sayıları çalışma kâğıdı: soldan ve sağdan kaçıncı, birinci, ikinci, üçüncü, yarışta sıra, baştan ve sondan sıra, raflarda sıra. 100 soru ve cevap anahtarı.",
                "Sıra sayısı: birinci, ikinci, üçüncü", "Nereden saymaya başladığına dikkat et: soldan mı, sağdan mı?", sets,
                ["Sıra sayıları bir nesnenin sıradaki yerini gösterir: birinci, ikinci, üçüncü… Kısaca 1., 2., 3. diye yazarız.",
                 "Soldan sayınca en soldaki birinci olur. Sağdan sayınca en sağdaki birinci olur.",
                 "Baştan 3. olanın önünde 2 kişi vardır."],
                [("Soldan 4. nesne", ["Soldan say: 1, 2, 3, 4"], "Dördüncü nesne"), ("6 kişilik sırada baştan 2.", ["Arkasında 6 − 2 = 4 kişi"], "Sondan 5.")],
                [["Sağdan sorulunca soldan saymak", "Hangi yönden sayılacağını oku"], ["Kendisini de saymak", "Önündekileri sayarken kendini sayma"],
                 ["3 ile 3.’yü karıştırmak", "3 bir sayı, 3. bir sıra"]],
                [("Sıra sayısı nasıl yazılır?", "Rakamdan sonra nokta konur: 1. birinci, 2. ikinci."),
                 ("Yarışta birinci kimdir?", "Yarışı ilk bitiren kişidir."),
                 ("Soldan 1. ile sağdan 1. aynı mıdır?", "Hayır, biri en soldaki, diğeri en sağdaki nesnedir.")])


def u3():
    sets = [("Çok, az, eşit", [(m_cok_az(10), 20)]),
            ("Daha çok, daha az", [(m_cok_az(15), 20)]),
            ("Sayıları karşılaştırma", [(m_karsilastir(0, 20), 20)]),
            ("En büyük ve en küçük", [(m_en(0, 20), 20)]),
            ("Sıralama", [(m_sirala(0, 20), 20)])]
    return unit("sayilari-karsilastirma", "S", "MAT.1.1.4", 3, "Çok, Az ve Eşit: Sayıları Karşılaştırma", "Karşılaştırma",
                "İki niceliğin büyüklüğünü “çok”, “daha çok”, “az”, “daha az” veya “eşit” terimleriyle karşılaştırır.",
                "1. sınıf karşılaştırma çalışma kâğıdı: çok, az ve eşit, daha çok ve daha az, büyüktür, küçüktür ve eşittir işaretleri, en büyük ve en küçük sayı, sıralama. 100 soru ve cevap anahtarı.",
                "Daha çok mu, daha az mı, eşit mi?", "Nesneleri birebir eşleyerek karşılaştır.", sets,
                ["İki grubu karşılaştırmak için nesneleri birebir eşleriz. Eşi kalmayan grupta daha çok nesne vardır.",
                 "Sayılarda sayma sırasında sonra gelen sayı daha büyüktür.",
                 "&lt; küçüktür, &gt; büyüktür, = eşittir demektir. İşaretin açık ağzı büyük sayıya bakar."],
                [("7 elma ve 5 armut", ["7 sayısı 5 sayısından büyük"], "Elma daha çok"), ("12 ○ 15", ["12, 15 sayısından küçük"], "12 &lt; 15")],
                [["Büyük resimli grubu daha çok sanmak", "Nesneleri say ya da eşle"], ["&lt; ile &gt; işaretini karıştırmak", "Açık ağız büyük sayıya bakar"],
                 ["Sıralarken bir sayıyı atlamak", "Bütün sayıları yaz ve kontrol et"]],
                [("Eşit ne demek?", "İki grupta aynı sayıda nesne var demektir."),
                 ("0 en küçük sayı mıdır?", "Evet, doğal sayıların en küçüğü 0’dır."),
                 ("Daha az ve az arasındaki fark nedir?", "“Az” tek bir grubu anlatır, “daha az” iki grubu karşılaştırır.")])


def u4():
    sets = [("Birer ve ikişer ileri", [(m_ritmik(40, (1, 2)), 20)]),
            ("Beşer ve onar ileri", [(m_ritmik(100, (5, 10)), 20)]),
            ("Geriye doğru sayma", [(m_ritmik(20, (1, 2), True), 14), (m_eksik(0, 20, (1, 2), True), 6)]),
            ("Eksik sayılar", [(m_eksik(0, 100, (2, 5, 10)), 20)]),
            ("Karışık", [(m_ritmik(100, (2, 5, 10)), 12), (m_eksik(0, 20, (1, 2), True), 8)])]
    return unit("ritmik-sayma", "S", "MAT.1.1.5", 4, "Ritmik Sayma: İkişer, Beşer, Onar", "Ritmik Sayma",
                "100’e kadar ileriye ve 20’den geriye doğru ritmik sayar.",
                "1. sınıf ritmik sayma çalışma kâğıdı: birer, ikişer, beşer ve onar ileriye sayma, 20’den geriye sayma, eksik sayıları bulma. 100 soru ve cevap anahtarı.",
                "Her adımda aynı sayı kadar ilerle", "İkişer: 2, 4, 6… Beşer: 5, 10, 15… Onar: 10, 20, 30…", sets,
                ["Ritmik saymada her adımda aynı sayı kadar ilerleriz.",
                 "İkişer sayarken 2 ekleriz, beşer sayarken 5, onar sayarken 10 ekleriz.",
                 "Geriye sayarken her adımda aynı sayı kadar azaltırız: 20, 19, 18…"],
                [("5, 10, 15, …", ["Beşer artıyor", "15 + 5"], "20"), ("20, 18, 16, …", ["İkişer azalıyor", "16 − 2"], "14")],
                [["Onar sayarken 1 eklemek", "Onar: 10 ekle"], ["Geriye sayarken eklemek", "Geriye: çıkar"], ["Bir sayıyı atlamak", "Her adımı yüksek sesle söyle"]],
                [("Ritmik sayma ne işe yarar?", "Nesneleri gruplayarak hızlı saymamızı sağlar ve çarpmaya hazırlar."),
                 ("Beşer sayınca hangi rakamlar gelir?", "Sayıların birler basamağı 5 ya da 0 olur."),
                 ("Onar sayarken birler basamağı değişir mi?", "Hayır, yalnızca onlar basamağı 1 artar.")])


def u5():
    sets = [("Şekil örüntüleri", [(m_oruntu(), 20)]),
            ("Artan sayı örüntüleri", [(m_eksik(0, 20, (1, 2), False), 20)]),
            ("Azalan sayı örüntüleri", [(m_eksik(0, 20, (1, 2), True), 20)]),
            ("Artan şekil örüntüleri", [(m_sekil_say_oruntu(), 20)]),
            ("Karışık", [(m_oruntu(), 10), (m_ritmik(20, (1, 2)), 10)])]
    return unit("oruntuler", "S", "MAT.1.1.6", 5, "Örüntüler: Şekil ve Sayı Örüntüleri", "Örüntüler",
                "Artan veya azalan sayı ve şekil örüntülerini çözümler; örüntünün kuralını bulur ve sonraki ögeyi belirler.",
                "1. sınıf örüntüler çalışma kâğıdı: tekrarlayan şekil örüntüleri, artan ve azalan sayı örüntüleri, artan şekil örüntüleri. 100 soru ve cevap anahtarı.",
                "Tekrar eden kısmı bul", "Örüntü birimi tekrar eder: kırmızı, mavi, kırmızı, mavi…", sets,
                ["Örüntü, belli bir kurala göre tekrar eden ya da değişen dizidir.",
                 "Tekrarlayan örüntüde tekrar eden kısma örüntü birimi denir.",
                 "Artan sayı örüntüsünde sayılar her adımda aynı miktar artar, azalan örüntüde azalır."],
                [("daire, üçgen, daire, üçgen, …", ["Birim: daire, üçgen"], "daire"), ("3, 5, 7, …", ["İkişer artıyor"], "9")],
                [["Örüntü birimini eksik bulmak", "Birimin tekrar ettiğini kontrol et"], ["Artanı azalan sanmak", "Sayılar büyüyor mu küçülüyor mu bak"],
                 ["Rengi unutup yalnızca şekle bakmak", "Hem şekle hem renge bak"]],
                [("Örüntü nerede görülür?", "Halılarda, kumaş desenlerinde, kaldırım taşlarında."),
                 ("Örüntü birimi kaç öge olabilir?", "İki, üç ya da daha fazla öge olabilir."),
                 ("Kendi örüntümü yapabilir miyim?", "Evet, bir birim seç ve onu tekrar et.")])


def u6():
    sets = [("Yaklaşık kaç?", [(m_tahmin(20, 5), 20)]),
            ("Bir avuçla karşılaştır", [(m_tahmin_kiyas(20), 20)]),
            ("Tahmin et ve say", [(m_tahmin(20, 5), 10), (m_say(5, 20), 10)]),
            ("Onluk çerçeveyle tahmin", [(m_tahmin_kiyas(20), 10), (m_say(11, 20), 10)]),
            ("Karışık", [(m_tahmin(20, 5), 10), (m_tahmin_kiyas(20), 10)])]
    return unit("nesne-sayisini-tahmin-etme", "S", "MAT.1.1.7", 6, "Nesne Sayısını Tahmin Etme", "Tahmin Etme",
                "Verilen bir çokluktaki ilişkilerden yararlanarak 20’ye kadar (20 dâhil) olan nesnelerin sayısını tahmin eder ve tahminini sayarak kontrol eder.",
                "1. sınıf tahmin etme çalışma kâğıdı: 20’ye kadar nesne sayısını saymadan tahmin etme, bilinen bir çoklukla karşılaştırma, tahmin edip sayarak kontrol etme. 100 soru ve cevap anahtarı.",
                "Tahmin: saymadan yaklaşık sayı", "Bilinen bir grupla karşılaştır, sonra sayarak kontrol et.", sets,
                ["Tahmin, saymadan söylenen yaklaşık sayıdır.",
                 "Bilinen bir grupla karşılaştırırız: bir avuçta 5 bilye varsa, iki avuç yaklaşık 10 bilyedir.",
                 "Tahmin ettikten sonra sayarak kontrol ederiz. Tahmin gerçek sayıya yakın olmalıdır."],
                [("Bir avuç 5 nesne, resimde iki avuç kadar", ["5 + 5"], "Yaklaşık 10"), ("Tahmin 15, sayınca 14", ["14 ile 15 çok yakın"], "İyi bir tahmin")],
                [["Tahminin tam doğru olması gerektiğini düşünmek", "Tahmin yaklaşıktır"], ["Çok uzak sayılar söylemek", "Bilinen bir grupla karşılaştır"],
                 ["Tahmin ettikten sonra saymamak", "Sayarak kontrol et"]],
                [("Neden tahmin ederiz?", "Saymak uzun sürdüğünde hızlıca bir fikir edinmek için."),
                 ("İyi bir tahmin nedir?", "Gerçek sayıya yakın olan tahmindir."),
                 ("Tahmin yanlış olur mu?", "Tahmin yaklaşıktır; sayınca biraz farklı çıkması normaldir.")])


def u7():
    sets = [("Uzun ve kısa", [(m_uzun(), 20)]),
            ("Yüksek ve alçak", [(m_kule(), 20)]),
            ("Ağır ve hafif", [(m_agir(), 20)]),
            ("Terazi dengede", [(m_denge(), 20)]),
            ("Kaç birim?", [(m_kac_birim(), 20)])]
    return unit("uzunluk-ve-kutle-olcme", "S", "MAT.1.1.8", 7, "Standart Olmayan Birimlerle Uzunluk ve Kütle", "Uzunluk ve Kütle",
                "Standart olmayan uygun ölçme araçları ile nesnelerin uzunluğunu ve tartacağı kütlenin ölçüm sonuçlarını tahmin eder ve karşılaştırır.",
                "1. sınıf uzunluk ve kütle çalışma kâğıdı: uzun ve kısa, yüksek ve alçak, ağır ve hafif, eşit kollu terazi, ataş ve küp gibi standart olmayan birimlerle ölçme. 100 soru ve cevap anahtarı.",
                "Ölçerken uçları aynı hizada tut", "Terazide ağır olan kefe aşağı iner.", sets,
                ["Uzunlukları karşılaştırırken nesnelerin bir ucunu aynı hizaya koyarız.",
                 "Ataş, küp ya da karış gibi birimlerle ölçebiliriz. Birimleri boşluk bırakmadan yan yana koyarız.",
                 "Eşit kollu terazide ağır olan kefe aşağı iner. Kefeler aynı hizadaysa kütleler eşittir."],
                [("Kalem 6 ataş, silgi 2 ataş", ["6, 2 sayısından büyük"], "Kalem daha uzun"), ("Terazi dengede: 1 elma = 4 küp", ["Kefeler eşit"], "Elma 4 küp ağırlığında")],
                [["Uçları hizalamadan karşılaştırmak", "Bir ucu aynı çizgiye koy"], ["Birimler arasında boşluk bırakmak", "Birimleri uç uca diz"],
                 ["Yukarı kalkan kefeyi ağır sanmak", "Ağır olan aşağı iner"]],
                [("Standart olmayan birim nedir?", "Karış, adım, ataş ya da küp gibi herkesin farklı olabilen ölçü birimleridir."),
                 ("Neden sonuçlar farklı çıkar?", "Herkesin karışı ve adımı farklı uzunluktadır."),
                 ("Terazi nasıl çalışır?", "Ağır taraf aşağı iner, hafif taraf yukarı kalkar.")])


def u8():
    B = [(10, 5), (5, 1), (20, 10), (10, 1), (20, 5), (50, 10), (100, 50), (200, 100), (100, 20), (50, 5)]
    sets = [("Paraları tanıma", [(m_para_tanı(), 7), (m_para_karsilastir(), 13)]),
            ("Hangisi daha değerli?", [(m_para_karsilastir(), 15), (m_para_eksik(20), 5)]),
            ("Paraları sayma", [(m_para_say((1, 5, 10), 20, (2, 3)), 12), (m_para_eksik(20), 8)]),
            ("Para bozdurma", [(m_para_bozdur(B), 20)]),
            ("Karışık", [(m_para_eksik(20), 10), (m_para_bozdur(B), 10)])]
    return unit("paralarimiz", "S", "MAT.1.1.9", 8, "Paralarımız: 1, 5, 10, 20, 50, 100 ve 200 TL", "Paralarımız",
                "Paraların (1 TL, 5 TL, 10 TL, 20 TL, 50 TL, 100 TL ve 200 TL) temsil ettiği büyüklükleri tanır ve karşılaştırır.",
                "1. sınıf paralarımız çalışma kâğıdı: 1, 5, 10, 20, 50, 100 ve 200 TL’yi tanıma, hangisi daha değerli, paraları sayma, para bozdurma. 100 soru ve cevap anahtarı.",
                "Paramızın birimi Türk lirası (TL)", "Madenî 1 TL, kâğıt 5, 10, 20, 50, 100 ve 200 TL.", sets,
                ["Paramızın birimi Türk lirasıdır ve kısaca TL yazılır.",
                 "1 TL madenî paradır. 5, 10, 20, 50, 100 ve 200 TL kâğıt paradır.",
                 "Paraların üstündeki sayı değerini gösterir. Büyük sayılı para daha değerlidir."],
                [("10 TL ve 5 TL", ["10 + 5"], "15 TL"), ("Bir 10 TL kaç tane 5 TL eder?", ["5 + 5 = 10"], "2 tane")],
                [["Para sayısını değeri sanmak", "Paraların üstündeki sayıları topla"], ["Büyük kâğıdı daha değerli sanmak", "Değer, üstündeki sayıdır"],
                 ["TL yazmayı unutmak", "Para değerinin yanına TL yaz"]],
                [("TL ne demek?", "Türk lirası demektir; paramızın birimidir."),
                 ("En değerli kâğıt para hangisidir?", "200 TL’dir."),
                 ("Para bozdurmak ne demek?", "Bir parayı aynı değerdeki daha küçük paralarla değiştirmek demektir.")])


def u9():
    sets = [("Resimle toplama", [(m_topla_resim(10), 20)]),
            ("Sayı doğrusunda toplama", [(m_atla("+", 20), 20)]),
            ("10’a kadar toplama", [(m_islem("+", 1, 10), 20)]),
            ("20’ye kadar toplama", [(m_islem("+", 10, 20, False), 20)]),
            ("Parça ve bütün", [(m_parca_butun(10), 10), (m_islem("+", 1, 20, False), 10)])]
    return unit("toplama-islemi", "I", "MAT.1.2.1, MAT.1.2.2", 9, "Toplama İşlemi: 20’ye Kadar", "Toplama İşlemi",
                "Günlük yaşamın içerdiği toplama işlemlerini çözümler; toplamı 20’yi geçmeyen eldesiz toplama yapar ve sonucu zihinden işlem yaparak muhakeme eder.",
                "1. sınıf toplama işlemi çalışma kâğıdı: resimle toplama, sayı doğrusunda ileri atlama, 10’a kadar ve 20’ye kadar eldesiz toplama, parça-bütün. 100 soru ve cevap anahtarı.",
                "Toplama = birleştirme", "Büyük sayıdan başla, üstüne say.", sets,
                ["Toplama, iki grubu birleştirmektir. + işareti “artı”, = işareti “eşittir” diye okunur.",
                 "Büyük sayıdan başlayıp küçük sayı kadar ileri sayarız: 6 + 3 → 7, 8, 9.",
                 "Toplananların yeri değişince toplam değişmez: 3 + 5 = 5 + 3."],
                [("4 + 3", ["4’ten başla: 5, 6, 7"], "7"), ("12 + 5", ["2 + 5 = 7", "10 + 7"], "17")],
                [["Baştan 1’den saymak", "Büyük sayıdan başla"], ["Başladığın sayıyı da saymak", "Önce bir adım at, sonra say"],
                 ["Toplama yerine çıkarma yapmak", "+ işaretine bak"]],
                [("Toplama ne demek?", "Grupları birleştirip hepsini bulmak demektir."),
                 ("3 + 5 ile 5 + 3 aynı mı?", "Evet, ikisi de 8 eder."),
                 ("Eldesiz toplama nedir?", "Birlerin toplamı 10’u geçmeyen toplamadır.")])


def u10():
    sets = [("Resimle çıkarma", [(m_cizik(10), 20)]),
            ("Sayı doğrusunda çıkarma", [(m_atla("-", 20), 20)]),
            ("10’a kadar çıkarma", [(m_islem("-", 2, 10), 20)]),
            ("20’ye kadar çıkarma", [(m_islem("-", 11, 20, False), 20)]),
            ("Kutudaki nesneler", [(m_kutu(20), 20)])]
    return unit("cikarma-islemi", "I", "MAT.1.2.1, MAT.1.2.2", 10, "Çıkarma İşlemi: 20’ye Kadar", "Çıkarma İşlemi",
                "Günlük yaşamın içerdiği çıkarma işlemlerini çözümler; 20’ye kadar onluk bozmadan çıkarma yapar ve sonucu zihinden işlem yaparak muhakeme eder.",
                "1. sınıf çıkarma işlemi çalışma kâğıdı: resimle çıkarma, sayı doğrusunda geri atlama, 10’a kadar ve 20’ye kadar onluk bozmadan çıkarma, kutuda kaç tane var. 100 soru ve cevap anahtarı.",
                "Çıkarma = ayırma, eksiltme", "Büyük sayıdan geri say.", sets,
                ["Çıkarma, bir gruptan bir kısmını ayırmak ya da eksiltmektir. − işareti “eksi” diye okunur.",
                 "Büyük sayıdan başlayıp küçük sayı kadar geri sayarız: 9 − 3 → 8, 7, 6.",
                 "Çıkarmada büyük sayı önce yazılır. Bir sayıdan kendisini çıkarırsak 0 kalır."],
                [("8 − 3", ["8’den geri say: 7, 6, 5"], "5"), ("17 − 4", ["7 − 4 = 3", "10 + 3"], "13")],
                [["Geri sayarken başlanan sayıyı da saymak", "Önce bir adım geri at"], ["Küçük sayıdan büyüğü çıkarmak", "Büyük sayı önce yazılır"],
                 ["Çıkarma yerine toplamak", "− işaretine bak"]],
                [("Çıkarma ne demek?", "Bir gruptan bir kısmını alıp kalanı bulmak demektir."),
                 ("Bir sayıdan 0 çıkarınca ne olur?", "Sayı değişmez: 7 − 0 = 7."),
                 ("Çıkarmayı nasıl kontrol ederim?", "Sonuçla çıkanı toplarsın; büyük sayıyı bulmalısın.")])


def u11():
    sets = [("Toplama problemleri", [(m_problem(20, "+"), 20)]),
            ("Çıkarma problemleri", [(m_problem(20, "-"), 20)]),
            ("Karşılaştırma problemleri", [(m_problem(20, "="), 20)]),
            ("Kutudaki nesneler", [(m_kutu(20), 20)]),
            ("Karışık", [(m_problem(20, "+-="), 20)])]
    return unit("toplama-ve-cikarma-problemleri", "I", "MAT.1.2.1", 11, "Toplama ve Çıkarma Problemleri", "Problemler",
                "Günlük yaşamın içerdiği toplama ve çıkarma işlemlerini çözümler; problemde hangi işlemin gerektiğine karar verir.",
                "1. sınıf toplama ve çıkarma problemleri çalışma kâğıdı: birleştirme, eksiltme ve karşılaştırma problemleri, kutudaki nesneler. 100 soru ve cevap anahtarı.",
                "Birleşiyor mu, eksiliyor mu?", "Birleşince topla, eksilince çıkar, fark sorulunca çıkar.", sets,
                ["Problemi dikkatle okuruz. Ne verildiğini ve ne sorulduğunu buluruz.",
                 "“Daha geldi, aldı, hepsi” gibi sözcükler birleştirmeyi; “gitti, yedi, kaldı” gibi sözcükler eksilmeyi anlatır.",
                 "“Kaç fazla, aralarında kaç fark” sorusunda büyük sayıdan küçük sayıyı çıkarırız."],
                [("8 kuş vardı, 5 kuş daha geldi.", ["Birleşme: 8 + 5"], "13 kuş"), ("12 balon vardı, 4 balon patladı.", ["Eksilme: 12 − 4"], "8 balon")],
                [["Her problemde toplamak", "Sözcüklere dikkat et"], ["Fark sorusunda toplamak", "Fark için çıkar"], ["Birimi yazmamak", "Cevabın yanına ne olduğunu yaz"]],
                [("Problemi nasıl çözerim?", "Oku, anla, işlemi seç, çöz ve kontrol et."),
                 ("Resim çizmek yardımcı olur mu?", "Evet, nesneleri çizip saymak problemi anlamaya yardım eder."),
                 ("Cevabımı nasıl kontrol ederim?", "Toplamayı çıkarmayla, çıkarmayı toplamayla kontrol edebilirsin.")])


def u12():
    sets = [("Eşittir işareti", [(m_esit(10), 20)]),
            ("Noktalı yer", [(m_bos(10), 20)]),
            ("Toplama ve çıkarma ilişkisi", [(m_iliski(10), 20)]),
            ("Parça ve bütün", [(m_parca_butun(10), 20)]),
            ("Terazi dengede", [(m_terazi_sayi(18), 10), (m_esit(18), 10)])]
    return unit("esitlik-ve-islemler-arasi-iliski", "I", "MAT.1.2.3, MAT.1.2.4", 12, "Eşittir İşareti, Toplama ve Çıkarma İlişkisi", "Eşitlik",
                "Eşit işaretinin anlamını toplama ve çıkarma işlemi bağlamında yorumlar; toplama ve çıkarma işlemlerinin ilişkisini yorumlar.",
                "1. sınıf eşitlik çalışma kâğıdı: eşittir işaretinin anlamı, noktalı yere gelen sayı, toplama ve çıkarma arasındaki ilişki, parça-bütün şeması, dengede terazi. 100 soru ve cevap anahtarı.",
                "= işaretinin iki yanı aynı değer", "3 + 4 = 7 ise 7 − 4 = 3.", sets,
                ["Eşittir işareti, iki yanın aynı değeri gösterdiğini anlatır: 4 + 2 = 3 + 3.",
                 "Toplama ve çıkarma birbirinin tersidir: 5 + 3 = 8 ise 8 − 3 = 5 ve 8 − 5 = 3.",
                 "Parça-bütün şemasında iki parçanın toplamı bütünü verir."],
                [("6 + 2 = 5 + …", ["6 + 2 = 8", "5 + 3 = 8"], "3"), ("4 + 5 = 9 ise", ["9 − 5 = 4"], "9 − 4 = 5")],
                [["Eşittirden sonra hemen sonucu yazmak", "Sağ taraf da bir işlem olabilir"], ["6 + 2 = 5 + 8 yazmak", "İki yanın değeri eşit olmalı"],
                 ["Çıkarmada sayıların yerini değiştirmek", "Büyük sayı önce yazılır"]],
                [("Eşittir işareti ne anlatır?", "İki yanın aynı değerde olduğunu anlatır, yalnızca “sonuç” demek değildir."),
                 ("Toplama ile çıkarma nasıl ilişkilidir?", "Biri diğerini geri alır; toplamayı çıkarmayla kontrol ederiz."),
                 ("Terazi örneği neden kullanılır?", "Dengede terazi iki yanın eşit olduğunu gösterir.")])


def u13():
    sets = [("Masanın neresinde?", [(m_masa(), 20)]),
            ("Kutunun neresinde?", [(m_kutu_konum(), 20)]),
            ("Sağ ve sol", [(m_sag_sol(), 20)]),
            ("Yönergeyi izle", [(m_yonerge(5), 20)]),
            ("Eş nesneler", [(m_es(), 20)])]
    return unit("yon-konum-ve-es-nesneler", "G", "MAT.1.3.1, MAT.1.3.2", 13, "Yön, Konum ve Eş Nesneler", "Yön ve Konum",
                "Hedefe ulaşmak için mesafeleri ve yönleri içeren yönergeleri çözümler; nesnelerin eşliğini değerlendirir.",
                "1. sınıf yön ve konum çalışma kâğıdı: üstünde, altında, önünde, arkasında, sağında ve solunda, kareli zeminde yönergeleri izleme, eş şekilleri bulma. 100 soru ve cevap anahtarı.",
                "Sağ, sol, üst, alt, ön, arka", "Yönergede kaç adım ve hangi yön olduğuna bak.", sets,
                ["Nesnelerin yerini üstünde, altında, önünde, arkasında, sağında ve solunda sözcükleriyle anlatırız.",
                 "Yönerge izlerken önce yönü, sonra adım sayısını okuruz: 2 kare sağa, 1 kare yukarı.",
                 "Biçimi ve büyüklüğü aynı olan nesneler eştir. Rengi ya da duruşu farklı olabilir."],
                [("Top masanın altında", ["Masanın aşağısında"], "Altında"), ("Yıldızdan 2 sağa, 1 yukarı", ["Önce sağa 2", "Sonra yukarı 1"], "Ulaşılan kare")],
                [["Sağ ile solu karıştırmak", "Sağ elini kaldır ve kontrol et"], ["Adım sayarken başlangıç karesini saymak", "Başlangıç karesi sayılmaz"],
                 ["Rengi farklı diye eş değil sanmak", "Eşlikte biçim ve büyüklüğe bak"]],
                [("Sağ ve solu nasıl hatırlarım?", "Yazı yazdığın el çoğu kişide sağ eldir."),
                 ("Yönerge nedir?", "Bir yere nasıl gidileceğini anlatan adımlardır."),
                 ("Eş ne demek?", "Biçimi ve büyüklüğü aynı demektir.")])


def u14():
    sets = [("Cismin adı", [(m_cisim_ad(), 20)]),
            ("Çevremizdeki cisimler", [(m_cisim_gercek(), 20)]),
            ("Yuvarlanır mı?", [(m_yuvarlanir(), 20)]),
            ("Cisim mi şekil mi?", [(m_cisim_ad(), 10), (m_sekil_ad(), 10)]),
            ("Karışık", [(m_cisim_gercek(), 12), (m_yuvarlanir(), 8)])]
    return unit("geometrik-cisimler", "G", "MAT.1.3.3", 14, "Geometrik Cisimler: Küp, Küre, Silindir, Koni", "Geometrik Cisimler",
                "Günlük yaşamdaki nesneleri biçimsel özelliklerine göre ayırt eder; küp, küre, silindir, koni ve prizma modellerini tanır.",
                "1. sınıf geometrik cisimler çalışma kâğıdı: küp, küre, silindir, koni ve dikdörtgenler prizması, çevremizdeki cisimler, yuvarlanabilen ve yuvarlanamayan cisimler. 100 soru ve cevap anahtarı.",
                "Küp, küre, silindir, koni, prizma", "Eğri yüzeyi olan cisimler yuvarlanabilir.", sets,
                ["Çevremizdeki nesneler geometrik cisimlere benzer: top küreye, zar küpe, bardak silindire benzer.",
                 "Küre her yöne yuvarlanır. Silindir ve koni bir yöne yuvarlanır.",
                 "Küp ve dikdörtgenler prizmasının bütün yüzleri düzdür; bu cisimler yuvarlanmaz, üst üste konabilir."],
                [("Futbol topu", ["Her yeri yuvarlak"], "Küre"), ("Ayakkabı kutusu", ["Yüzleri dikdörtgen"], "Dikdörtgenler prizması")],
                [["Küre ile daireyi karıştırmak", "Küre bir cisim, daire bir şekil"], ["Küp ile kareyi karıştırmak", "Küpün yüzleri karedir"],
                 ["Silindiri yuvarlanmaz sanmak", "Yan yüzü eğri; yuvarlanır"]],
                [("Cisim ile şekil arasındaki fark nedir?", "Cisim boşlukta yer kaplar ve tutulabilir; şekil kâğıt üzerinde düzdür."),
                 ("Hangi cisimler üst üste konabilir?", "Düz yüzleri olan küp ve prizma kolayca üst üste konur."),
                 ("Dondurma külahı hangi cisme benzer?", "Koniye benzer.")])


def u15():
    sets = [("Şeklin adı", [(m_sekil_ad(), 20)]),
            ("Şekli bul", [(m_sekil_bul(), 20)]),
            ("Kenar ve köşe", [(m_kenar(("triangle", "square", "rectangle")), 20)]),
            ("Şekilleri sayma", [(m_sekil_say(), 20)]),
            ("Çevremizdeki şekiller", [(m_sekil_gercek(), 14), (m_sekil_ad(), 6)])]
    return unit("geometrik-sekiller", "G", "MAT.1.3.4, MAT.1.3.5", 15, "Geometrik Şekiller: Üçgen, Kare, Dikdörtgen, Daire", "Geometrik Şekiller",
                "Günlük yaşamda karşılaşılan geometrik yapılardaki geometrik şekilleri çözümler; şekilleri kenar ve köşe sayısı gibi biçimsel özelliklerine göre sınıflandırır.",
                "1. sınıf geometrik şekiller çalışma kâğıdı: üçgen, kare, dikdörtgen ve daire, kenar ve köşe sayısı, şekilleri bulma ve sayma, çevremizdeki şekiller. 100 soru ve cevap anahtarı.",
                "Kenar ve köşe say", "Üçgen 3, kare ve dikdörtgen 4 kenarlı; dairenin köşesi yok.", sets,
                ["Üçgenin 3 kenarı ve 3 köşesi vardır.",
                 "Karenin ve dikdörtgenin 4 kenarı ve 4 köşesi vardır. Karenin bütün kenarları eşittir.",
                 "Dairenin kenarı ve köşesi yoktur; çevresi yuvarlaktır."],
                [("3 kenarlı şekil", ["Kenarları say: 3"], "Üçgen"), ("Kapı", ["Uzun ve kısa kenarları var"], "Dikdörtgen")],
                [["Döndürülmüş kareyi başka şekil sanmak", "Kenar sayısı ve eşitliği değişmez"], ["Kareyi dikdörtgenden ayıramamak", "Karenin bütün kenarları eşit"],
                 ["Daireye köşe saymak", "Dairenin köşesi yok"]],
                [("Kare bir dikdörtgen midir?", "Evet, kare bütün kenarları eşit olan bir dikdörtgendir."),
                 ("Şekil döndürülünce değişir mi?", "Hayır, adı ve özellikleri aynı kalır."),
                 ("Dairenin kaç kenarı var?", "Dairenin düz kenarı yoktur.")])


def u16():
    sets = [("Çetele okuma", [(m_cetele(20), 20)]),
            ("Nesne grafiği okuma", [(m_veri(8, "nesne", (0,)), 20)]),
            ("En çok, en az", [(m_veri(8, "nesne", (1,)), 20)]),
            ("Çetele tablosu", [(m_veri(10, "cetele", (0, 1)), 20)]),
            ("Veriye dayalı karar", [(m_karar(9), 20)])]
    return unit("veri-toplama-ve-nesne-grafigi", "V", "MAT.1.4.1", 16, "Veri Toplama: Çetele ve Nesne Grafiği", "Veri Toplama",
                "Kategorik veriye dayalı temel veri grubu ile çalışır; veriyi çetele ve nesne grafiğiyle düzenler, okur ve veriye dayalı karar verir.",
                "1. sınıf veri toplama çalışma kâğıdı: çetele okuma, nesne grafiği okuma, en çok ve en az seçilen, çetele tablosu, veriye dayalı karar verme. 100 soru ve cevap anahtarı.",
                "Çetele: her veri bir çizgi", "Beşinci çizgi diğer dördünün üstünden çizilir.", sets,
                ["Veri toplarken her cevap için bir çizgi çizeriz; buna çetele denir. Beşinci çizgi dördünün üstünden çapraz çizilir.",
                 "Nesne grafiğinde her simge bir veriyi gösterir. En uzun sıra en çok seçileni gösterir.",
                 "Veriye bakarak karar veririz: en çok seçilen meyveyi alırız."],
                [("Çetelede 2 beşli grup ve 3 çizgi", ["5 + 5 + 3"], "13"), ("Kedi 6, kuş 4", ["6, 4 sayısından büyük"], "En çok kedi")],
                [["Beşli grubu 4 saymak", "Bir beşli grup 5 eder"], ["Simgeleri yanlış sırada saymak", "Her sırayı ayrı say"],
                 ["En az seçileni en çok sanmak", "Soruyu dikkatli oku"]],
                [("Çetele neden beşli gruplanır?", "Saymayı kolaylaştırmak için; beşer beşer sayabiliriz."),
                 ("Nesne grafiği nedir?", "Verileri simgelerle gösteren grafiktir."),
                 ("Veriye dayalı karar ne demek?", "Toplanan bilgilere bakarak seçim yapmak demektir.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u16]
