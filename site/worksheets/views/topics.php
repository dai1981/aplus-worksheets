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
$zh = $country['lang'] === 'zh-TW';
$sbase = $seg[0] . '/' . $seg[1] . '/';
$path = $sbase . 'topics/';
$crumbs = array(array(T('worksheets'), ''), array($country['name'], $seg[0] . '/'),
                array($subject['name'], $sbase), array($zh ? '主題' : 'Topics', $path));

$tnames = array_map(function ($k) use ($defs, $seg) { return topic_name($defs[$k], $seg[0]); }, array_slice(array_keys($all), 0, 6));
page_head(array(
    'lang' => $country['lang'], 'hreflang' => $country['hreflang'],
    'title' => $zh ? $subject['name'] . '學習單：依主題找｜' . $country['standard'] . ' | ' . SITE_NAME
                   : $subject['name'] . ' Worksheets by Topic (' . $country['standard'] . ') | ' . SITE_NAME,
    'desc' => $zh ? '依主題整理的免費' . $subject['name'] . '學習單，依照' . $country['standard'] . '：' . implode('、', $tnames)
                    . '等，每個單元都有說明、練習和解答。'
                  : 'Free ' . strtolower($subject['name']) . ' worksheets by topic, aligned to the ' . $country['standard']
                    . ': ' . implode(', ', $tnames) . ' and more, with lessons, practice and answer keys.',
    'canonical' => $path,
));
site_header($crumbs);
?>
<main class="sn-wrap">
<?php if ($zh): ?>
<h1><?= h($subject['name']) ?>學習單：依主題找</h1>
<div class="sx-hero"><p>每個主題頁收錄這個主題的所有單元，從最早學到的年級排到最後的年級，依照<?= h($country['standard']) ?>。</p></div>
<?php else: ?>
<h1><?= h($subject['name']) ?> Worksheets by Topic</h1>
<div class="sx-hero"><p>Each topic page collects every skill on that topic, from the first <?= h(strtolower(rtrim(T('grades'), 's'))) ?> it is taught to the last, aligned to the <?= h($country['standard']) ?>.</p></div>
<?php endif; ?>
<ul class="sx-list">
<?php foreach ($all as $tk => $units): $tp = $path . $tk . '/'; ?>
<li><div class="m"><span class="t"><?= h(topic_name($defs[$tk], $seg[0])) ?></span>
  <span class="d"><?= h(topic_range($units)) ?> · <?= h(sprintf(T('skills_count'), count($units))) ?></span>
  <span class="k"><?= h(topic_blurb($defs[$tk], $seg[0])) ?></span></div>
  <p class="act"><a class="q" href="<?= url($tp) ?>"><?= h(topic_name($defs[$tk], $seg[0]) . ($zh ? '學習單' : ' worksheets')) ?></a></p></li>
<?php endforeach; ?>
</ul>
</main>
<?php
echo breadcrumb_ld($crumbs);
site_footer($country['lang'], false);
?>
</body>
</html>
