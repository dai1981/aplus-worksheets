<?php
/* Quiz together rankings: class accuracy by country and by state / province (/worksheets/ranking/)
   ?lang=de|fr|it|es|es-MX|pt-BR|zh-TW|zh-CN|ko|id|tr|sv shows the page in that language (the quiz links here in the page language).
   The page is drawn by one shared file on eigo-duke.com: /common/js/mq-rank.js (data: api/mq.php?a=rank)
   Subjects (?sub=math|science), fields (?fd=fractions, inc/fields.php) and grades (?g=uk/science/year-10) come from the catalog in the DB (ws_subject / ws_grade).
   Areas with few players show an "estimate" (inc/mq-est.json, read by api/mq.php) until real numbers are in. */
$RK = array(
    'en' => array('Quiz Rankings: Accuracy by Country and State',
        'See how players in your state, province or country score on our quizzes. Play on your own or together with your class and help your area climb the ranking.',
        'Quiz Together lets a class answer the same quiz on their phones. Tap the small QR code on any quiz, choose your country and area on the waiting screen, and your class\'s accuracy counts toward your area\'s ranking. Only each player\'s first game counts, and names are never saved. An area\'s accuracy appears after enough players join.'),
    'de' => array('Quiz-Rangliste: Trefferquote nach Land und Bundesland',
        'So gut schneiden Spieler in deinem Bundesland und Land bei unseren Quiz ab. Spiel allein oder mit deiner Klasse und bring deine Region nach oben.',
        'Mit „Gemeinsam quizzen“ löst eine Klasse dasselbe Quiz auf dem Handy. Tippe bei einem Quiz auf den kleinen QR-Code, wähle auf dem Startbildschirm Land und Region – dann zählt die Trefferquote eurer Klasse für die Rangliste eurer Region. Gezählt wird nur das erste Spiel jedes Spielers, Namen werden nie gespeichert. Die Trefferquote einer Region erscheint, sobald genug Spieler mitgemacht haben.'),
    'fr' => array('Classement des quiz : taux de réussite par pays et par région',
        'Découvre le taux de réussite des joueurs de ta région et de ton pays à nos quiz. Joue seul ou en classe et fais grimper ta région.',
        '« Quiz ensemble » permet à une classe de répondre au même quiz sur téléphone. Appuie sur le petit QR code d’un quiz, choisis le pays et la région sur l’écran d’attente : le taux de réussite de la classe compte pour le classement de ta région. Seule la première partie de chaque joueur compte et les prénoms ne sont jamais enregistrés. Le taux d’une région s’affiche quand assez de joueurs ont participé.'),
    'it' => array('Classifica dei quiz: risposte giuste per paese e regione',
        'Scopri come vanno i giocatori della tua regione e del tuo paese nei nostri quiz. Gioca da solo o con la classe e fai salire la tua regione.',
        '«Quiz insieme» permette a una classe di rispondere allo stesso quiz con il telefono. Tocca il piccolo codice QR di un quiz e scegli paese e regione nella schermata di attesa: la percentuale di risposte giuste della classe conta per la classifica della tua regione. Conta solo la prima partita di ogni partecipante e i nomi non vengono mai salvati. La percentuale di una regione compare quando hanno partecipato abbastanza persone.'),
    'es' => array('Clasificación de los quiz: aciertos por país y región',
        'Mira cómo les va a los jugadores de tu región y de tu país en nuestros quiz. Juega solo o con tu clase y haz que tu región suba.',
        '«Quiz en grupo» permite que una clase responda el mismo quiz en el teléfono. Toca el pequeño código QR de un quiz y elige el país y la región en la pantalla de espera: el porcentaje de aciertos de la clase cuenta para la clasificación de tu región. Solo cuenta la primera partida de cada jugador y los nombres nunca se guardan. El porcentaje de una región aparece cuando han jugado suficientes personas.'),
    'pt-BR' => array('Ranking dos quizzes: acertos por país e estado',
        'Veja como os jogadores do seu estado e do seu país vão nos nossos quizzes. Jogue sozinho ou com a turma e faça sua região subir no ranking.',
        'O “Quiz em grupo” deixa uma turma responder o mesmo quiz no celular. Toque no pequeno QR code de um quiz e escolha o país e a região na tela de espera: a porcentagem de acertos da turma conta para o ranking da sua região. Só conta a primeira partida de cada jogador e os nomes nunca são salvos. A porcentagem de uma região aparece quando jogadores suficientes tiverem participado.'),
    'ko' => array('퀴즈 랭킹: 나라·시도별 정답률',
        '우리 시도와 나라의 참가자들이 퀴즈를 얼마나 맞혔는지 확인해 보세요. 혼자서도, 반 친구들과 함께도 풀고 우리 지역의 순위를 올려요.',
        '‘다 함께 퀴즈’는 반 전체가 휴대폰으로 같은 퀴즈를 푸는 기능이에요. 퀴즈 오른쪽 위의 작은 QR 코드를 누르고, 대기 화면에서 나라와 시도를 고르면 반의 정답률이 우리 지역 랭킹에 들어가요. 한 사람당 첫 번째 결과만 세고, 이름은 저장하지 않아요. 참여 인원이 충분히 모이면 그 지역의 정답률이 표시돼요.'),
    'zh-CN' => array('测验排行榜：各国家和省份的答对率',
        '看看你所在的省份和国家的参加者在测验中的答对率。自己作答或全班一起作答，都能让你们省份的排名往上冲。',
        '“一起来答题”可以让全班用手机回答同一组题目。点题目右上角的小二维码，在等待页面选择国家和省份，全班的答对率就会计入所在省份的排行榜。每个人只计算第一次的成绩，不会保存名字。参加人数足够多之后，才会显示该省份的答对率。'),
    'zh-TW' => array('測驗排行榜：各國與各地區的答對率',
        '看看你所在的縣市和國家的參加者在測驗中的答對率。自己作答或全班一起作答，都能讓你們的地區排名往上衝。',
        '「一起來答題」可以讓全班用手機回答同一份題目。點題目右上角的小 QR 碼，在等待畫面選擇國家和地區，全班的答對率就會計入所在地區的排行榜。每個人只計算第一次的成績，不會保存名字。參加人數夠多之後，才會顯示該地區的答對率。'),
    'id' => array('Peringkat Kuis: Persentase Benar per Negara dan Provinsi',
        'Lihat seberapa baik para pemain di provinsi dan negaramu dalam kuis kami. Kerjakan sendiri atau bersama teman sekelas dan bantu daerahmu naik peringkat.',
        'Dengan Kuis Bersama, satu kelas menjawab kuis yang sama di ponsel. Ketuk kode QR kecil pada kuis, lalu pilih negara dan provinsi di layar tunggu. Persentase jawaban benar kelasmu akan dihitung untuk peringkat daerahmu. Hanya permainan pertama setiap pemain yang dihitung, dan nama tidak pernah disimpan. Persentase suatu daerah muncul setelah cukup banyak pemain ikut.'),
    'tr' => array('Quiz Sıralaması: Ülkelere ve İllere Göre Başarı Oranı',
        'İlindeki ve ülkendeki oyuncuların testlerimizde ne kadar başarılı olduğunu gör. Tek başına ya da sınıfınla çöz, bölgeni sıralamada yukarı taşı.',
        'Birlikte Quiz ile bütün sınıf aynı testi telefondan çözer. Bir testin küçük QR koduna dokun, bekleme ekranında ülkeni ve ilini seç. Sınıfının doğru cevap oranı bölgenin sıralamasına eklenir. Her oyuncunun yalnızca ilk oyunu sayılır ve isimler asla kaydedilmez. Bir bölgenin oranı, yeterince oyuncu katıldıktan sonra görünür.'),
    'sv' => array('Quizranking: andel rätt per land och län',
        'Se hur spelarna i ditt län och ditt land klarar sig i våra quiz. Spela själv eller med klassen och hjälp ditt område att klättra i rankingen.',
        'Med Quiz tillsammans svarar hela klassen på samma quiz i mobilen. Tryck på den lilla QR-koden på ett quiz och välj land och län på väntskärmen, så räknas klassens andel rätt med i ert områdes ranking. Bara varje spelares första omgång räknas, och namn sparas aldrig. Ett områdes andel rätt visas när tillräckligt många spelare har varit med.'),
);
$lang = isset($_GET['lang']) && is_string($_GET['lang']) ? $_GET['lang'] : 'en';
if ($lang === 'es-MX') $tx = $RK['es'];
elseif (isset($RK[$lang])) $tx = $RK[$lang];
else { $lang = 'en'; $tx = $RK['en']; }
T(array($lang === 'es-MX' ? 'es' : $lang));                 // header and footer words
page_head(array(
    'lang' => $lang,
    'title' => $tx[0] . ' | ' . SITE_NAME,
    'desc' => $tx[1],
    'canonical' => 'ranking/' . ($lang === 'en' ? '' : '?lang=' . $lang),
));
site_header(array());
// subjects for the ranking: math (every math slug) and science, with the grade names for the grade menu
$RK_SUB = array('math' => array(), 'science' => array());
$RK_GR = array();
foreach (qa('SELECT g.country, g.subject, g.slug, g.name, c.name AS cname FROM ws_grade g '
          . 'JOIN ws_country c ON c.code = g.country ORDER BY c.sort, g.subject, g.sort') as $x) {
    $grp = $x['subject'] === 'science' ? 'science' : (preg_match('/^mat/', $x['subject']) ? 'math' : '');
    if ($grp === '') continue;
    $RK_SUB[$grp][$x['subject']] = 1;
    $RK_GR[$x['country'] . '/' . $x['subject'] . '/' . $x['slug']] = $x['cname'] . ' · ' . $x['name'];
}
$rk_subs = array();
foreach ($RK_SUB as $k => $v) if ($v) $rk_subs[] = array('k' => $k, 's' => array_keys($v));
require_once __DIR__ . '/../inc/fields.php';          // fields (fractions, ratios, …) to compare countries
$rk_fu = field_ui($lang);
$rk_js = JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP;
?>
<main class="rk-wrap">
<div id="mq-rank-app"></div>
<p class="mqr-intro"><?= h($tx[2]) ?></p>
</main>
<style>.rk-wrap{padding:24px 14px}.mqr-intro{max-width:860px;margin:18px auto 0;font-size:14px;line-height:1.9;color:#5b5249}</style>
<script>window.MQR_CONF = { api: "<?= url('api/mq.php') ?>", lang: "<?= h($lang) ?>", quiz: "<?= url('') ?>",
  subjects: <?= json_encode($rk_subs, $rk_js) ?>, grades: <?= json_encode($RK_GR, $rk_js) ?>,
  fields: <?= json_encode(field_menu($lang), $rk_js) ?>, fieldL: <?= json_encode($rk_fu[0], $rk_js) ?>,
  allFields: <?= json_encode($rk_fu[1], $rk_js) ?>, fieldN: <?= json_encode($rk_fu[2], $rk_js) ?> };</script>
<script src="https://www.eigo-duke.com/common/js/mq-geo.js?v=20261127a"></script>
<script src="https://www.eigo-duke.com/common/js/mq-rank.js?v=20261127w"></script>
<?php site_footer($lang === 'es-MX' ? 'es' : $lang, false); ?>
</body>
</html>
