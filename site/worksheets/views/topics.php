<?php
/* /worksheets/{country}/{subject}/topics/ : list of topic hubs */
require_once __DIR__ . '/../inc/topics.php';
$country = get_country($seg[0]);
$subject = $country ? get_subject($seg[0], $seg[1]) : null;
if (!$subject) not_found();
T(array($country['lang']));
$defs = topic_defs($seg[0]);
$all = topics_for($seg[0], $seg[1]);
if (!$all) not_found();
$zh = strpos($country['lang'], 'zh') === 0;   // zh-TW and zh-CN (zt() converts the text for zh-CN)
$ko = $country['lang'] === 'ko';
$idn = $country['lang'] === 'id';
$trk = $country['lang'] === 'tr';
$sv = $country['lang'] === 'sv';
$de = $country['lang'] === 'de';
$fr = $country['lang'] === 'fr';
$it = $country['lang'] === 'it';
$pt = $country['lang'] === 'pt-BR';
$es = strpos($country['lang'], 'es') === 0;
$sbase = $seg[0] . '/' . $seg[1] . '/';
$path = $sbase . 'topics/';
$crumbs = array(array(T('worksheets'), ''), array($country['name'], $seg[0] . '/'),
                array($subject['name'], $sbase), array($sv ? 'Teman' : ($trk ? 'Konular' : ($idn ? 'Topik' : ($ko ? '주제' : (($pt || $es) ? 'Temas' : ($it ? 'Argomenti' : ($fr ? 'Thèmes' : ($de ? 'Themen' : ($zh ? zt('主題') : 'Topics')))))))), $path));

$tnames = array_map(function ($k) use ($defs, $seg) { return topic_name($defs[$k], $seg[0]); }, array_slice(array_keys($all), 0, 6));
page_head(array(
    'lang' => $country['lang'], 'hreflang' => $country['hreflang'],
    'title' => $sv ? $subject['name'] . ' – arbetsblad efter tema (' . $country['standard'] . ') | ' . SITE_NAME : ($trk ? 'Konulara Göre ' . $subject['name'] . ' Çalışma Kâğıtları (' . $country['standard'] . ') | ' . SITE_NAME : ($idn ? 'Lembar Kerja ' . $subject['name'] . ' per Topik (' . $country['standard'] . ') | ' . SITE_NAME : ($ko ? $subject['name'] . ' 학습지: 주제별로 찾기 | ' . $country['standard'] . ' | ' . SITE_NAME : ($es ? 'Fichas de ' . mb_strtolower($subject['name']) . ' por temas (' . $country['standard'] . ') | ' . SITE_NAME : ($pt ? 'Atividades de ' . mb_strtolower($subject['name']) . ' por tema (' . $country['standard'] . ') | ' . SITE_NAME : ($it ? 'Schede di ' . strtolower($subject['name']) . ' per argomento (' . $country['standard'] . ') | ' . SITE_NAME : ($fr ? 'Fiches de ' . strtolower($subject['name']) . ' par thème (' . $country['standard'] . ') | ' . SITE_NAME : ($de ? $subject['name'] . '-Arbeitsblätter nach Themen (' . $country['standard'] . ') | ' . SITE_NAME
             : ($zh ? $subject['name'] . zt('學習單：依主題找｜') . $country['standard'] . ' | ' . SITE_NAME
                   : $subject['name'] . ' Worksheets by Topic (' . $country['standard'] . ') | ' . SITE_NAME))))))))),
    'desc' => $sv ? 'Gratis arbetsblad i ' . mb_strtolower($subject['name']) . ' ordnade efter tema enligt ' . $country['standard'] . ': ' . implode(', ', $tnames) . ' med flera, med genomgångar, övningar och facit.' : ($trk ? $country['standard'] . ' ile uyumlu, konulara göre düzenlenmiş ücretsiz ' . $subject['name'] . ' çalışma kâğıtları: ' . implode(', ', $tnames) . ' ve diğerleri. Her konuda anlatım, alıştırma ve cevap anahtarı var.' : ($idn ? 'Lembar kerja ' . $subject['name'] . ' gratis yang disusun per topik sesuai ' . $country['standard'] . ': ' . implode(', ', $tnames) . ', dan lainnya. Setiap materi berisi penjelasan, latihan, dan kunci jawaban.' : ($ko ? $country['standard'] . '에 맞춰 주제별로 정리한 무료 ' . $subject['name'] . ' 학습지: ' . implode(', ', $tnames) . ' 등. 단원마다 개념 정리, 연습 문제, 정답이 있습니다.' : ($es ? 'Fichas de ' . mb_strtolower($subject['name']) . ' gratis organizadas por temas, según la ' . $country['standard'] . ': '
                    . implode(', ', $tnames) . ' y más, con lecciones, ejercicios y soluciones.' : ($pt ? 'Atividades de ' . mb_strtolower($subject['name']) . ' grátis organizadas por tema, de acordo com a ' . $country['standard'] . ': '
                    . implode(', ', $tnames) . ' e mais, com aulas, exercícios e gabaritos.' : ($it ? 'Schede di ' . strtolower($subject['name']) . ' gratis divise per argomento, secondo le ' . $country['standard'] . ': '
                    . implode(', ', $tnames) . ', ecc., con lezioni, esercizi e soluzioni.' : ($fr ? 'Fiches de ' . strtolower($subject['name']) . ' gratuites classées par thème, conformes aux ' . $country['standard'] . ' : '
                    . implode(', ', $tnames) . ', etc., avec leçons, exercices et corrigés.' : ($de ? 'Kostenlose ' . $subject['name'] . '-Arbeitsblätter nach Themen, passend zu den ' . $country['standard'] . ': '
                    . implode(', ', $tnames) . ' und mehr, mit Erklärungen, Übungen und Lösungen.'
            : ($zh ? zt('依主題整理的免費') . $subject['name'] . zt('學習單，依照') . $country['standard'] . '：' . implode('、', $tnames)
                    . zt('等，每個單元都有說明、練習和解答。')
                  : 'Free ' . strtolower($subject['name']) . ' worksheets by topic, aligned to the ' . $country['standard']
                    . ': ' . implode(', ', $tnames) . ' and more, with lessons, practice and answer keys.'))))))))),
    'canonical' => $path,
));
site_header($crumbs);
?>
<main class="sn-wrap">
<?php if ($sv): ?>
<h1><?= h($subject['name']) ?> – arbetsblad efter tema</h1>
<div class="sx-hero"><p>Varje temasida samlar alla områden inom ett tema, från den första årskursen där det tas upp till den sista, enligt <?= h($country['standard']) ?>.</p></div>
<?php elseif ($trk): ?>
<h1>Konulara Göre <?= h($subject['name']) ?> Çalışma Kâğıtları</h1>
<div class="sx-hero"><p>Her konu sayfası, bir konudaki tüm çalışma kâğıtlarını konunun ilk işlendiği sınıftan son sınıfa kadar <?= h($country['standard']) ?> sırasıyla bir araya getirir.</p></div>
<?php elseif ($idn): ?>
<h1>Lembar Kerja <?= h($subject['name']) ?> per Topik</h1>
<div class="sx-hero"><p>Setiap halaman topik mengumpulkan semua materi dalam satu topik, dari kelas pertama topik itu dipelajari sampai kelas terakhir, sesuai <?= h($country['standard']) ?>.</p></div>
<?php elseif ($es): ?>
<h1>Fichas de <?= h(mb_strtolower($subject['name'])) ?> por temas</h1>
<div class="sx-hero"><p>Cada página reúne todas las fichas de un mismo tema, desde el primer curso en que se estudia hasta el último, según la <?= h($country['standard']) ?>.</p></div>
<?php elseif ($pt): ?>
<h1>Atividades de <?= h(mb_strtolower($subject['name'])) ?> por tema</h1>
<div class="sx-hero"><p>Cada página reúne todas as atividades de um mesmo tema, do primeiro ano em que ele é estudado até o último, de acordo com a <?= h($country['standard']) ?>.</p></div>
<?php elseif ($it): ?>
<h1>Schede di <?= h(strtolower($subject['name'])) ?> per argomento</h1>
<div class="sx-hero"><p>Ogni pagina raccoglie tutte le schede di uno stesso argomento, dalla prima classe in cui si studia all’ultima, secondo le <?= h($country['standard']) ?>.</p></div>
<?php elseif ($fr): ?>
<h1>Fiches de <?= h(strtolower($subject['name'])) ?> par thème</h1>
<div class="sx-hero"><p>Chaque page de thème rassemble toutes les fiches d’un même thème, de la première classe où il est étudié à la dernière, conformes aux <?= h($country['standard']) ?>.</p></div>
<?php elseif ($de): ?>
<h1><?= h($subject['name']) ?>-Arbeitsblätter nach Themen</h1>
<div class="sx-hero"><p>Jede Themenseite sammelt alle Arbeitsblätter zu einem Thema, von der ersten Klasse, in der es vorkommt, bis zur letzten, passend zu den <?= h($country['standard']) ?>.</p></div>
<?php elseif ($ko): ?>
<h1><?= h($subject['name']) ?> 학습지: 주제별로 찾기</h1>
<div class="sx-hero"><p>주제 페이지마다 그 주제의 모든 단원을 처음 배우는 학년부터 마지막 학년까지 모았습니다. <?= h($country['standard']) ?>에 맞췄습니다.</p></div>
<?php elseif ($zh): ?>
<h1><?= h($subject['name']) ?><?= zt('學習單：依主題找') ?></h1>
<div class="sx-hero"><p><?= zt('每個主題頁收錄這個主題的所有單元，從最早學到的年級排到最後的年級，依照') ?><?= h($country['standard']) ?>。</p></div>
<?php else: ?>
<h1><?= h($subject['name']) ?> Worksheets by Topic</h1>
<div class="sx-hero"><p>Each topic page collects every skill on that topic, from the first <?= h(strtolower(rtrim(T('grades'), 's'))) ?> it is taught to the last, aligned to the <?= h($country['standard']) ?>.</p></div>
<?php endif; ?>
<ul class="sx-list">
<?php foreach ($all as $tk => $units): $tp = $path . $tk . '/'; ?>
<li><div class="m"><span class="t"><?= h(topic_name($defs[$tk], $seg[0])) ?></span>
  <span class="d"><?= h(topic_range($units)) ?> · <?= h(sprintf(T('skills_count'), count($units))) ?></span>
  <span class="k"><?= h(topic_blurb($defs[$tk], $seg[0])) ?></span></div>
  <p class="act"><a class="q" href="<?= url($tp) ?>"><?= h(topic_name($defs[$tk], $seg[0]) . ($sv ? ' – arbetsblad' : ($trk ? ' çalışma kâğıtları' : ($idn ? '' : ($ko ? ' 학습지' : ($es ? ': fichas' : ($pt ? ': atividades' : ($it ? ': schede' : ($fr ? ' : fiches' : ($de ? ': Arbeitsblätter' : ($zh ? zt('學習單') : ' worksheets'))))))))))) ?></a></p></li>
<?php endforeach; ?>
</ul>
</main>
<?php
echo breadcrumb_ld($crumbs);
site_footer($country['lang'], false);
?>
</body>
</html>
