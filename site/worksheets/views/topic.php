<?php
/* /worksheets/{country}/{subject}/topics/{topic}/ : every skill on one topic, lowest grade first */
require_once __DIR__ . '/../inc/topics.php';
$country = get_country($seg[0]);
$subject = $country ? get_subject($seg[0], $seg[1]) : null;
if (!$subject) not_found();
T(array($country['lang']));
$defs = topic_defs($seg[0]);
$all = topics_for($seg[0], $seg[1]);
if (!isset($all[$seg[3]])) not_found();
$tk = $seg[3];
$units = $all[$tk];
$name = topic_name($defs[$tk], $seg[0]);
$lc = topic_lc($name);
$range = topic_range($units);
$sbase = $seg[0] . '/' . $seg[1] . '/';
$path = $sbase . 'topics/' . $tk . '/';
$paper = $country['paper'] === 'letter' ? ($country['lang'] === 'es-MX' ? 'tamaño carta' : 'Letter') : 'A4';
$crumbs = array(array(T('worksheets'), ''), array($country['name'], $seg[0] . '/'),
                array($subject['name'], $sbase), array($name, $path));

$groups = array();
foreach ($units as $u) $groups[$u['grade']][] = $u;
$gnames = array();
foreach ($units as $u) $gnames[$u['grade']] = $u['grade_name'];
$titles = array();
foreach ($units as $u) $titles[] = $u['short_title'];
$first = $units[0]; $last = $units[count($units) - 1];

$zh = $country['lang'] === 'zh-TW';
$de = $country['lang'] === 'de';
$fr = $country['lang'] === 'fr';
$it = $country['lang'] === 'it';
$pt = $country['lang'] === 'pt-BR';
$es = strpos($country['lang'], 'es') === 0;
if ($es) {
    $faq = array(
        array('q' => '¿Qué fichas sobre «' . $name . '» hay aquí?',
              'a' => 'Hay ' . count($units) . ' temas, ' . $range . ': '
                   . implode(', ', array_slice($titles, 0, 6)) . (count($titles) > 6 ? ', etc.' : '.')),
        array('q' => '¿En qué curso se estudia este tema?',
              'a' => 'El tema empieza en ' . $first['grade_name'] . ' con «' . $first['short_title'] . '»'
                   . ($first['grade'] === $last['grade'] ? '.' : ' y llega hasta ' . $last['grade_name'] . ' con «' . $last['short_title'] . '».')),
        array('q' => '¿Cómo puede practicar mi hijo con estas fichas?',
              'a' => 'Elige el tema de su curso, lee la lección breve y haz las 5 series de 20 ejercicios. '
                   . 'Cada respuesta se corrige al momento. Para practicar más, imprime la ficha en ' . $paper . ': las soluciones están en la última página.'),
        array('q' => '¿Las fichas son gratis?',
              'a' => 'Sí. Las lecciones, los ejercicios en línea y las fichas con soluciones son gratis para usar en casa y en el aula. No hace falta registrarse.'),
    );
} elseif ($pt) {
    $faq = array(
        array('q' => 'Quais atividades sobre « ' . $name . ' » há aqui?',
              'a' => 'Há ' . count($units) . ' conteúdos, ' . $range . ': '
                   . implode(', ', array_slice($titles, 0, 6)) . (count($titles) > 6 ? ' etc.' : '.')),
        array('q' => 'Em que ano esse tema é estudado?',
              'a' => 'O tema começa no ' . $first['grade_name'] . ' com « ' . $first['short_title'] . ' »'
                   . ($first['grade'] === $last['grade'] ? '.' : ' e vai até o ' . $last['grade_name'] . ' com « ' . $last['short_title'] . ' ».')),
        array('q' => 'Como meu filho pode praticar com estas atividades?',
              'a' => 'Escolha o conteúdo do ano dele, leia a aula curta e faça as 5 séries de 20 exercícios. '
                   . 'Cada resposta é corrigida na hora. Para praticar mais, imprima a atividade em ' . $paper . ': o gabarito está na última página.'),
        array('q' => 'As atividades são grátis?',
              'a' => 'Sim. As aulas, os exercícios on-line e as atividades com gabarito são grátis para usar em casa e na escola. Não precisa de cadastro.'),
    );
} elseif ($it) {
    $faq = array(
        array('q' => 'Quali schede sull’argomento « ' . $name . ' » ci sono qui?',
              'a' => 'Ci sono ' . count($units) . ' argomenti, ' . $range . ': '
                   . implode(', ', array_slice($titles, 0, 6)) . (count($titles) > 6 ? ', ecc.' : '.')),
        array('q' => 'In quale classe si studia questo argomento?',
              'a' => 'L’argomento comincia in ' . strtolower($first['grade_name']) . ' con « ' . $first['short_title'] . ' »'
                   . ($first['grade'] === $last['grade'] ? '.' : ' e arriva fino alla ' . strtolower($last['grade_name']) . ' con « ' . $last['short_title'] . ' ».')),
        array('q' => 'Come può esercitarsi mio figlio con queste schede?',
              'a' => 'Scegli l’argomento della sua classe, leggi la lezione breve, poi fai le 5 serie da 20 esercizi. '
                   . 'Ogni risposta viene corretta subito. Per esercitarsi ancora, stampa la scheda in formato ' . $paper . ': le soluzioni sono nell’ultima pagina.'),
        array('q' => 'Le schede sono gratis?',
              'a' => 'Sì. Le lezioni, gli esercizi online e le schede con le soluzioni sono gratis per la casa e la classe. Non serve registrarsi.'),
    );
} elseif ($fr) {
    $faq = array(
        array('q' => 'Quelles fiches sur le thème « ' . $name . ' » trouve-t-on ici ?',
              'a' => 'Il y a ' . count($units) . ' notions sur ce thème, ' . $range . ' : '
                   . implode(', ', array_slice($titles, 0, 6)) . (count($titles) > 6 ? ', etc.' : '.')),
        array('q' => 'En quelle classe travaille-t-on ce thème ?',
              'a' => 'Le thème commence en ' . $first['grade_name'] . ' avec « ' . $first['short_title'] . ' »'
                   . ($first['grade'] === $last['grade'] ? '.' : ' et va jusqu’au ' . $last['grade_name'] . ' avec « ' . $last['short_title'] . ' ».')),
        array('q' => 'Comment mon enfant peut-il s’entraîner avec ces fiches ?',
              'a' => 'Choisis la notion de sa classe, lis la leçon courte, puis fais les 5 séries de 20 exercices. '
                   . 'Chaque réponse est corrigée tout de suite. Pour s’entraîner encore, imprime la fiche au format ' . $paper . ' : le corrigé est sur la dernière page.'),
        array('q' => 'Les fiches sont-elles gratuites ?',
              'a' => 'Oui. Les leçons, les exercices en ligne et les fiches avec corrigé sont gratuits pour la maison et la classe. Aucune inscription n’est nécessaire.'),
    );
} elseif ($de) {
    $faq = array(
        array('q' => 'Welche Arbeitsblätter zum Thema ' . $name . ' gibt es hier?',
              'a' => 'Hier findest du ' . count($units) . ' Themen zu ' . $name . ' von ' . $range . ': '
                   . implode(', ', array_slice($titles, 0, 6)) . (count($titles) > 6 ? ' und weitere' : '') . '.'),
        array('q' => 'In welcher Klasse lernen Kinder ' . $name . '?',
              'a' => 'Das Thema beginnt in ' . $first['grade_name'] . ' mit „' . $first['short_title'] . '“'
                   . ($first['grade'] === $last['grade'] ? '.' : ' und geht bis ' . $last['grade_name'] . ' mit „' . $last['short_title'] . '“.')),
        array('q' => 'Wie übt mein Kind am besten mit diesen Arbeitsblättern?',
              'a' => 'Wähle das Thema für die Klasse deines Kindes, lies die kurze Erklärung und löse dann die 5 Runden mit je 20 Aufgaben. '
                   . 'Jede Antwort wird sofort geprüft. Für zusätzliche Übung kannst du das Arbeitsblatt im Format ' . $paper . ' ausdrucken; die Lösungen stehen auf der letzten Seite.'),
        array('q' => 'Sind die Arbeitsblätter kostenlos?',
              'a' => 'Ja. Die Erklärungen, die Online-Übungen und die Arbeitsblätter mit Lösungen sind kostenlos für zu Hause und den Unterricht. Eine Anmeldung ist nicht nötig.'),
    );
} elseif ($zh) {
    $faq = array(
        array('q' => '這一頁有哪些' . $name . '學習單？',
              'a' => '共有 ' . count($units) . ' 個' . $name . '單元，從' . $range . '：'
                   . implode('、', array_slice($titles, 0, 6)) . (count($titles) > 6 ? '等' : '') . '。'),
        array('q' => $name . '在' . $country['standard'] . '中從幾年級開始學？',
              'a' => $name . '從' . $first['grade_name'] . '的「' . $first['short_title'] . '」開始'
                   . ($first['grade'] === $last['grade'] ? '。' : '，一直學到' . $last['grade_name'] . '的「' . $last['short_title'] . '」。')),
        array('q' => '孩子要怎麼使用這些' . $name . '學習單？',
              'a' => '選擇孩子所在年級的單元，先讀簡短的說明，再做 5 組、每組 20 題的練習，每題作答後立刻知道對錯。'
                   . '也可以列印 ' . $paper . ' 學習單多練習，最後一頁是解答。'),
        array('q' => '這些' . $name . '學習單免費嗎？',
              'a' => '免費。說明、線上練習和附解答的列印學習單，在家裡和教室都可以免費使用，不需要註冊。'),
    );
} else {
    $faq = array(
        array('q' => 'What ' . $lc . ' worksheets are on this page?',
              'a' => 'There are ' . count($units) . ' ' . $lc . ' skills from ' . $range . ': '
                   . implode(', ', array_slice($titles, 0, 6)) . (count($titles) > 6 ? ', and more' : '') . '.'),
        array('q' => 'When do students learn ' . $lc . ' in the ' . $country['standard'] . '?',
              'a' => $name . ' starts in ' . $first['grade_name'] . ' with ' . $first['short_title']
                   . ($first['grade'] === $last['grade'] ? '.' : ' and goes up to ' . $last['grade_name'] . ' with ' . $last['short_title'] . '.')),
        array('q' => 'How should my child use these ' . $lc . ' worksheets?',
              'a' => 'Pick the skill for their ' . strtolower(rtrim(T('grades'), 's')) . ', read the short lesson, then do the 5 practice sets of 20 questions. '
                   . 'Each answer is checked right away. Print the ' . $paper . ' worksheet for extra practice; the answer key is on the last page.'),
        array('q' => 'Are these ' . $lc . ' worksheets free?',
              'a' => 'Yes. The lessons, the online practice and the printable worksheets with answer keys are free for home and classroom use. No sign-up is needed.'),
    );
}

page_head(array(
    'lang' => $country['lang'], 'hreflang' => $country['hreflang'],
    'title' => $es ? $name . ': fichas ' . $range . ' gratis con soluciones | ' . SITE_NAME : ($pt ? $name . ': atividades ' . $range . ' grátis com gabarito | ' . SITE_NAME : ($it ? $name . ': schede ' . $range . ' gratis con soluzioni | ' . SITE_NAME : ($fr ? $name . ' : fiches ' . $range . ' gratuites avec corrigé | ' . SITE_NAME : ($de ? $name . ' Arbeitsblätter ' . $range . ': kostenlos üben mit Lösungen | ' . SITE_NAME
             : ($zh ? $name . '學習單｜' . $range . '免費練習（附解答）| ' . SITE_NAME
                   : $name . ' Worksheets: Free ' . $range . ' ' . $subject['name'] . ' Practice with Answers | ' . SITE_NAME))))),
    'desc' => $es ? 'Fichas gratis sobre «' . $name . '», ' . $range . ', según la ' . $country['standard'] . ': '
                    . count($units) . ' temas, cada uno con una lección, 100 ejercicios y soluciones para imprimir.' : ($pt ? 'Atividades grátis sobre « ' . $name . ' », ' . $range . ', de acordo com a ' . $country['standard'] . ': '
                    . count($units) . ' conteúdos, cada um com aula, 100 exercícios e gabarito para imprimir.' : ($it ? 'Schede gratis sull’argomento « ' . $name . ' », ' . $range . ', secondo le ' . $country['standard'] . ': '
                    . count($units) . ' argomenti, ognuno con una lezione, 100 esercizi e le soluzioni da stampare.' : ($fr ? 'Fiches gratuites sur le thème « ' . $name . ' », ' . $range . ', conformes aux ' . $country['standard'] . ' : '
                    . count($units) . ' notions, chacune avec une leçon, 100 exercices et un corrigé à imprimer.' : ($de ? 'Kostenlose Arbeitsblätter zum Thema ' . $name . ' für ' . $range . ' nach den ' . $country['standard'] . ': '
                    . count($units) . ' Themen, jeweils mit Erklärung, 100 Übungsaufgaben und Lösungen zum Ausdrucken.'
            : ($zh ? '免費' . $name . '學習單，依照' . $country['standard'] . '，從' . $range . '共 ' . count($units)
                    . ' 個單元，每個單元都有說明、100 題練習和可列印的解答。'
                  : 'Free ' . $lc . ' worksheets for ' . $range . ', aligned to the ' . $country['standard'] . ': '
                    . count($units) . ' skills, each with a lesson, 100 practice questions and a printable answer key.'))))),
    'canonical' => $path, 'image' => preview_path($path),
));
site_header($crumbs);
?>
<main class="sn-wrap">
<span class="sn-grade"><?= h($range . ' · ' . $country['standard']) ?></span>
<h1><?= h(sprintf(T('topic_h1'), $name)) ?></h1>
<div class="sx-hero"><p><?= h(topic_blurb($defs[$tk], $seg[0])) ?><?= $es ? h(' Cada tema tiene una lección breve, 100 ejercicios corregidos al momento y una ficha (' . $paper . ') para imprimir con soluciones. Gratis, sin registro.') : ($pt ? h(' Cada conteúdo tem uma aula curta, 100 exercícios corrigidos na hora e uma atividade (' . $paper . ') para imprimir com gabarito. Grátis, sem cadastro.') : ($it ? h(' Ogni argomento ha una lezione breve, 100 esercizi corretti subito e una scheda (' . $paper . ') da stampare con le soluzioni. Gratis, senza registrazione.') : ($fr ? h(' Chaque notion a une leçon courte, 100 exercices corrigés tout de suite et une fiche (' . $paper . ') à imprimer avec corrigé. Gratuit, sans inscription.') : ($de ? h(' Zu jedem Thema gibt es eine kurze Erklärung, 100 Übungsaufgaben mit sofortiger Rückmeldung und ein Arbeitsblatt (' . $paper . ') mit Lösungen zum Ausdrucken. Kostenlos, ohne Anmeldung.') : ($zh ? h('每個單元都有簡短的說明、100 題立即對答的練習，以及附解答的 ' . $paper . ' 列印學習單。免費，不需要註冊。')
  : ' Every skill below has a short lesson, 100 practice questions with instant feedback and a printable ' . h($paper) . ' worksheet with an answer key. Free, no sign-up.'))))) ?></p></div>

<?php if (count($groups) > 1): ?>
<ul class="tp-grades" aria-label="<?= h(T('grades')) ?>">
<?php foreach ($groups as $g => $list): ?>
  <li><a href="#<?= h($g) ?>"><?= h($gnames[$g]) ?></a></li>
<?php endforeach; ?>
</ul>
<?php endif; ?>

<?php foreach ($groups as $g => $list): $gbase = $sbase . $g . '/'; ?>
<h2 id="<?= h($g) ?>"><?= h($es ? $name . ' en ' . $gnames[$g] : ($pt ? $name . ' – ' . $gnames[$g] : ($it ? $name . ' in ' . strtolower($gnames[$g]) : ($fr ? $name . ' en ' . $gnames[$g] : $gnames[$g] . ($zh ? '' : ($de ? ': ' : ' ')) . $name)))) ?></h2>
<ul class="sx-list">
<?php foreach ($list as $u): $up = $gbase . $u['slug'] . '/'; ?>
<li><div class="m"><span class="t"><?= h($u['title']) ?></span>
  <span class="d"><?= h($u['standard_code']) ?> · 100 <?= h(T('questions')) ?></span>
  <?php if ($u['key_big']): ?><span class="k"><?= h($u['key_big']) ?></span><?php endif; ?>
  <span class="sp-bar" data-prog="<?= h(prog_key($seg[0], $seg[1], $g, $u['slug'])) ?>" data-sets="5"></span></div>
  <p class="act"><a class="q" href="<?= url($up) ?>"><?= h(T('learn_quiz')) ?></a><a href="<?= url($up . 'print/') ?>"><?= h(T('print')) ?></a><a href="<?= url($gbase) ?>"><?= h($gnames[$g]) ?></a></p></li>
<?php endforeach; ?>
</ul>
<?php endforeach; ?>

<section class="sn-faq">
<h2><?= h(T('faq')) ?></h2>
<?php foreach ($faq as $f): ?>
  <details><summary><?= h($f['q']) ?></summary><div class="sn-a"><?= h($f['a']) ?></div></details>
<?php endforeach; ?>
</section>

<h2><?= h($es ? 'Otros temas de ' . mb_strtolower($subject['name']) : ($pt ? 'Outros temas de ' . mb_strtolower($subject['name']) : ($it ? 'Altri argomenti di ' . strtolower($subject['name']) : ($fr ? 'Autres thèmes de ' . strtolower($subject['name']) : ($de ? 'Weitere Themen in ' . $subject['name'] : ($zh ? '其他' . $subject['name'] . '主題' : 'More ' . strtolower($subject['name']) . ' topics')))))) ?></h2>
<ul class="tp-chips">
<?php foreach ($all as $ok => $ou): if ($ok === $tk) continue; ?>
  <li><a href="<?= url($sbase . 'topics/' . $ok . '/') ?>"><?= h(topic_name($defs[$ok], $seg[0])) ?><span class="n"><?= count($ou) ?></span></a></li>
<?php endforeach; ?>
</ul>
</main>
<?php
echo breadcrumb_ld($crumbs);
$items = array();
foreach ($units as $i => $u) {
    $items[] = array('@type' => 'ListItem', 'position' => $i + 1, 'name' => $u['grade_name'] . ': ' . $u['title'],
                     'url' => abs_url($sbase . $u['grade'] . '/' . $u['slug'] . '/'));
}
$cp = array('@context' => 'https://schema.org', '@type' => 'CollectionPage',
    'name' => sprintf(T('topic_h1'), $name), 'description' => topic_blurb($defs[$tk], $seg[0]), 'url' => abs_url($path),
    'inLanguage' => $country['hreflang'], 'isAccessibleForFree' => true,
    'about' => array('@type' => 'Thing', 'name' => $name),
    'mainEntity' => array('@type' => 'ItemList', 'numberOfItems' => count($items), 'itemListElement' => $items));
if (preview_path($path)) $cp['image'] = abs_url(preview_path($path));
echo jsonld($cp);
$qs = array();
foreach ($faq as $f) $qs[] = array('@type' => 'Question', 'name' => $f['q'], 'acceptedAnswer' => array('@type' => 'Answer', 'text' => $f['a']));
echo jsonld(array('@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $qs));
site_footer($country['lang']);
?>
</body>
</html>
