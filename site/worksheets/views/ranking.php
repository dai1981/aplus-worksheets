<?php
/* Quiz together rankings: class accuracy by country and by state / province (/worksheets/ranking/)
   ?lang=de|fr|it|es|es-MX|pt-BR|zh-TW shows the page in that language (the quiz links here in the page language).
   The page is drawn by one shared file on eigo-duke.com: /common/js/mq-rank.js (data: api/mq.php?a=rank) */
$RK = array(
    'en' => array('Quiz Together Rankings: Class Accuracy by Country and State',
        'See how classes in your state, province or country score on Quiz Together. Play a quiz together with your class and help your area climb the ranking.',
        'Quiz Together lets a class answer the same quiz on their phones. Tap the small QR code on any quiz, choose your country and area on the waiting screen, and your class\'s accuracy counts toward your area\'s ranking. Only each player\'s first game counts, and names are never saved. An area\'s accuracy appears after enough players join.'),
    'de' => array('Gemeinsam quizzen: Rangliste nach Land und Bundesland',
        'So gut sind Klassen in deinem Bundesland und Land beim gemeinsamen Quiz. Spielt als Klasse zusammen und bringt eure Region nach oben.',
        'Mit „Gemeinsam quizzen“ löst eine Klasse dasselbe Quiz auf dem Handy. Tippe bei einem Quiz auf den kleinen QR-Code, wähle auf dem Startbildschirm Land und Region – dann zählt die Trefferquote eurer Klasse für die Rangliste eurer Region. Gezählt wird nur das erste Spiel jedes Spielers, Namen werden nie gespeichert. Die Trefferquote einer Region erscheint, sobald genug Spieler mitgemacht haben.'),
    'fr' => array('Quiz ensemble : classement par pays et par région',
        'Découvre le taux de réussite des classes de ta région et de ton pays au quiz ensemble. Jouez en classe et faites grimper votre région.',
        '« Quiz ensemble » permet à une classe de répondre au même quiz sur téléphone. Appuie sur le petit QR code d’un quiz, choisis le pays et la région sur l’écran d’attente : le taux de réussite de la classe compte pour le classement de ta région. Seule la première partie de chaque joueur compte et les prénoms ne sont jamais enregistrés. Le taux d’une région s’affiche quand assez de joueurs ont participé.'),
    'it' => array('Quiz insieme: classifica per paese e regione',
        'Scopri come vanno le classi della tua regione e del tuo paese nel quiz insieme. Giocate in classe e fate salire la vostra regione.',
        '«Quiz insieme» permette a una classe di rispondere allo stesso quiz con il telefono. Tocca il piccolo codice QR di un quiz e scegli paese e regione nella schermata di attesa: la percentuale di risposte giuste della classe conta per la classifica della tua regione. Conta solo la prima partita di ogni partecipante e i nomi non vengono mai salvati. La percentuale di una regione compare quando hanno partecipato abbastanza persone.'),
    'es' => array('Quiz en grupo: clasificación por país y región',
        'Mira cómo les va a las clases de tu región y de tu país en el quiz en grupo. Juega con tu clase y haz que tu región suba.',
        '«Quiz en grupo» permite que una clase responda el mismo quiz en el teléfono. Toca el pequeño código QR de un quiz y elige el país y la región en la pantalla de espera: el porcentaje de aciertos de la clase cuenta para la clasificación de tu región. Solo cuenta la primera partida de cada jugador y los nombres nunca se guardan. El porcentaje de una región aparece cuando han jugado suficientes personas.'),
    'pt-BR' => array('Quiz em grupo: ranking por país e estado',
        'Veja como as turmas do seu estado e do seu país vão no quiz em grupo. Joguem juntos e façam sua região subir no ranking.',
        'O “Quiz em grupo” deixa uma turma responder o mesmo quiz no celular. Toque no pequeno QR code de um quiz e escolha o país e a região na tela de espera: a porcentagem de acertos da turma conta para o ranking da sua região. Só conta a primeira partida de cada jogador e os nomes nunca são salvos. A porcentagem de uma região aparece quando jogadores suficientes tiverem participado.'),
    'zh-TW' => array('一起來答題 排行榜：各國與各地區的班級答對率',
        '看看你所在的縣市和國家的班級在「一起來答題」中的答對率。全班一起作答，讓你們的地區排名往上衝。',
        '「一起來答題」可以讓全班用手機回答同一份題目。點題目右上角的小 QR 碼，在等待畫面選擇國家和地區，全班的答對率就會計入所在地區的排行榜。每個人只計算第一次的成績，不會保存名字。參加人數夠多之後，才會顯示該地區的答對率。'),
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
?>
<main class="rk-wrap">
<div id="mq-rank-app"></div>
<p class="mqr-intro"><?= h($tx[2]) ?></p>
</main>
<style>.rk-wrap{padding:24px 14px}.mqr-intro{max-width:860px;margin:18px auto 0;font-size:14px;line-height:1.9;color:#5b5249}</style>
<script>window.MQR_CONF = { api: "<?= url('api/mq.php') ?>", lang: "<?= h($lang) ?>", quiz: "<?= url('') ?>" };</script>
<script src="https://www.eigo-duke.com/common/js/mq-geo.js?v=20261124d"></script>
<script src="https://www.eigo-duke.com/common/js/mq-rank.js?v=20261124d"></script>
<?php site_footer($lang === 'es-MX' ? 'es' : $lang, false); ?>
</body>
</html>
