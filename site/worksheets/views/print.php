<?php
$country = get_country($seg[0]);
$subject = $country ? get_subject($seg[0], $seg[1]) : null;
$grade = $subject ? get_grade($seg[0], $seg[1], $seg[2]) : null;
$u = $grade ? get_unit($seg[0], $seg[1], $seg[2], $seg[3]) : null;
if (!$u) not_found();
T(array($country['lang']));

$gbase = $seg[0] . '/' . $seg[1] . '/' . $seg[2] . '/';
$upath = $gbase . $u['slug'] . '/';
$path = $upath . 'print/';
$sets = json_decode($u['sets_json'], true);
$letter = ($country['paper'] === 'letter');
$kind = $grade['name'] . ' ' . $subject['name'];

/* ------------------------------------------------------------------
   How many questions fit on each sheet.
   Each question gets an estimated height (mm). Short questions sit two to a row.
   Sheet 1 takes questions from set 1, sheet 2 from sets 2-3, sheet 3 from sets 4-5,
   adding questions in order until the sheet is full.
   ------------------------------------------------------------------ */
function q_half($it) {
    $text = strip_tags(strip_figs($it['q']));
    $mx = 0;
    foreach ($it['c'] as $c) $mx = max($mx, mb_strlen(strip_tags($c)));
    if ($mx > 18) return false;
    return has_fig($it['q']) || mb_strlen($text) <= 90;
}
function q_long_choices($it) {
    foreach ($it['c'] as $c) if (mb_strlen(strip_tags($c)) > 28) return true;
    return false;
}
function fig_mm($html) {                       // height of the picture as printed
    if (!preg_match("/<svg[^>]*viewBox='0 0 ([\d.]+) ([\d.]+)'/", $html, $m)) return 0;
    $w = (float)$m[1]; $h = (float)$m[2];
    if ($w <= 0) return 0;
    $fw = min($w * 0.2646, 52);
    $cap = (abs($w - $h) < 1) ? 34 : 27;         // square pictures (clocks) print larger
    return min($fw * $h / $w, $cap) + 2;
}
function sq_mark($html) {                       // tag square pictures so CSS can print them larger
    return preg_replace_callback("/<svg([^>]*viewBox='0 0 ([\\d.]+) ([\\d.]+)')/", function ($m) {
        return abs((float)$m[2] - (float)$m[3]) < 1 ? '<svg data-sq="1"' . $m[1] : $m[0];
    }, $html);
}
function q_mm($it, $half) {
    $q = strip_figs($it['q']);
    $frac = strpos($q . implode('', $it['c']), "class='fr'") !== false;
    $len = mb_strlen(strip_tags($q));
    $lines = max(1, (int)ceil($len / ($half ? 44 : 92)));
    $line = $frac ? 8.5 : 6.2;
    $h = 4.5 + $lines * $line;                                   // question text + padding
    $clen = 0;
    foreach ($it['c'] as $c) $clen += mb_strlen(strip_tags($c)) + 4;
    if (q_long_choices($it)) $h += 4 * 5.6;                      // one choice per line
    else $h += ($frac ? 8 : 6) * max(1, (int)ceil($clen / ($half ? 40 : 88)));
    if (has_fig($it['q'])) $h += fig_mm($it['q']);
    return $h;
}
function layout_mm($items) {                   // height of the grid for these questions
    $total = 0; $pending = null;
    foreach ($items as $it) {
        $half = q_half($it); $h = q_mm($it, $half);
        if ($half) {
            if ($pending === null) { $pending = $h; }
            else { $total += max($pending, $h); $pending = null; }
        } else {
            if ($pending !== null) { $total += $pending; $pending = null; }
            $total += $h;
        }
    }
    if ($pending !== null) $total += $pending;
    return $total;
}
function fill_sheet($sets, $sources, $cap, $max_each) {
    $out = array(); $share = $cap / count($sources);
    foreach ($sources as $k => $si) {
        if (!isset($sets[$si])) continue;
        $limit = $share * ($k + 1);                               // unused room moves to the next set
        $n = 0;
        foreach ($sets[$si]['items'] as $it) {
            if ($n >= $max_each) break;
            $try = array_merge($out, array($it));
            if ($n >= 2 && layout_mm($try) > $limit) break;       // at least 2 from every set
            $out = $try; $n++;
        }
    }
    return $out;
}

$small = $letter ? 0 : 12;                     // A4 is 12mm taller than Letter
$plan = array(
    array('label' => T('p_warmup'), 'src' => array(0),    'cap' => 182 + $small, 'max' => 8),
    array('label' => T('p_prac1'),  'src' => array(1, 2), 'cap' => 210 + $small, 'max' => 9),
    array('label' => T('p_prac2'),  'src' => array(3, 4), 'cap' => 210 + $small, 'max' => 9),
);
$pages = array();
$no = 0;
foreach ($plan as $pg) {
    $qs = array();
    foreach (fill_sheet($sets, $pg['src'], $pg['cap'], $pg['max']) as $it) {
        $it['no'] = ++$no;
        $qs[] = $it;
    }
    $pages[] = array('label' => $pg['label'], 'qs' => $qs);
}
$QN = $no;

function sheet_head($kind, $label, $title, $is_key = false) {
    echo '<div class="pr-head"><div class="pr-ttl"><p class="pr-kind">' . h($kind) . ' · <b>' . h($label) . '</b></p>';
    echo '<h1 class="pr-h1">' . h($title) . '</h1></div>';
    if ($is_key) echo '<div class="pr-mark">' . h(T('for_check')) . '</div>';
    else echo '<div class="pr-name"><div><span>' . h(T('name')) . '</span></div><div><span>' . h(T('date')) . '</span></div><div><span>' . h(T('score')) . '</span> &nbsp; &nbsp; &nbsp; / ' . $GLOBALS['QN'] . '</div></div>';
    echo "</div>\n";
}
function sheet_foot($u, $kind, $upath, $pg) {
    echo '<div class="pr-foot"><div class="f1"><b>' . h(SITE_NAME) . '</b> | ' . h($kind) . ' · ' . h($u['short_title'])
       . ($u['standard_code'] ? ' (' . h($u['standard_code']) . ')' : '') . '<br>' . h(abs_url($upath)) . '<br>' . h(T('license')) . '</div>';
    echo '<div class="pr-qr" data-qr="' . h(abs_url($upath)) . '"></div>';
    echo '<div class="pr-pg">' . h($pg) . " / 4</div></div>\n";
}

$title = $u['short_title'] . ' Worksheet (' . $grade['name'] . ')';
page_head(array(
    'lang' => $country['lang'], 'hreflang' => $country['hreflang'],
    'title' => $grade['name'] . ' ' . $u['short_title'] . ' Worksheet with Answer Key (Printable, ' . ($letter ? 'Letter' : 'A4') . ') | ' . SITE_NAME,
    'desc' => 'Free printable ' . $grade['name'] . ' ' . strtolower($u['short_title']) . ' worksheet'
              . ($u['standard_code'] ? ' (' . $u['standard_code'] . ')' : '')
              . ': ' . $QN . ' questions on 3 pages plus an answer key. Print it or save it as a PDF.',
    'canonical' => $path, 'og_type' => 'article', 'css' => 'ws-print.css',
    'body_class' => 'prbody ' . ($letter ? 'paper-letter' : 'paper-a4'),
    'head' => '<style>@page{size:' . ($letter ? 'letter' : 'A4') . " portrait;margin:0}</style>\n",
));
?>
<div class="pr-bar">
  <a href="<?= url($gbase) ?>"><?= h($kind) ?></a>
  <a href="<?= url($upath) ?>"><?= h(T('lesson_link')) ?>: <?= h($u['short_title']) ?></a>
  <span class="sp"></span>
  <span class="pr-note"><?= h(T('print_note')) ?></span>
  <?php if ($u['pdf_url']): ?><a class="pr-dl" href="<?= h($u['pdf_url']) ?>" download><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v10.2l3.6-3.6 1.4 1.4-6 6-6-6 1.4-1.4 3.6 3.6V3h2zM4 19h16v2H4v-2z"/></svg><?= h(T('pdf_btn')) ?></a><?php endif; ?>
  <button class="pr-print" type="button" onclick="window.print()"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h10v4H7V3zm-3 6h16a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-2v-4H6v4H4a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1zm4 8h8v4H8v-4z"/></svg><?= h(T('print_btn')) ?></button>
</div>
<?php foreach ($pages as $pi => $pg): ?>
<div class="pr-sheet">
<?php sheet_head($kind, $pg['label'], $u['title'], false); ?>
<?php if ($pi === 0): ?>
<div class="pr-key"><p class="k1"><?= h($u['key_big']) ?></p><p class="k2"><?= h($u['key_sub']) ?></p></div>
<?php endif; ?>
<p class="pr-lead"><?= h(T('circle')) ?><span><?= h(sprintf(T('total_q'), count($pg['qs']))) ?></span></p>
<div class="pr-qs">
<?php foreach ($pg['qs'] as $it):
    $fig = has_fig($it['q']);
    $cls = 'pr-q' . (q_half($it) ? ' half' : '') . ($fig ? ' wf' : '');
    $long = q_long_choices($it);
?>
  <div class="<?= $cls ?>"><div class="pr-qh"><span class="pr-n">(<?= $it['no'] ?>)</span><span class="pr-t"><?= sq_mark($it['q']) ?></span></div><div class="pr-ch<?= $long ? ' col1' : '' ?>"><?php foreach ($it['c'] as $c): ?><span><?= $c ?></span><?php endforeach; ?></div></div>
<?php endforeach; ?>
</div>
<?php sheet_foot($u, $kind, $upath, $pi + 1); ?>
</div>
<?php endforeach; ?>
<div class="pr-sheet">
<?php sheet_head($kind, T('p_key'), $u['title'], true); ?>
<div class="pr-ans">
<?php foreach ($pages as $pg): ?>
<h3><?= h($pg['label']) ?></h3>
<div class="pr-agrid">
<?php foreach ($pg['qs'] as $it): ?>
  <div class="pr-a"><b>(<?= $it['no'] ?>)</b><span><i class="an"><?= $it['a'] + 1 ?>)</i><?= $it['c'][$it['a']] ?></span></div>
<?php endforeach; ?>
</div>
<?php endforeach; ?>
</div>
<?php sheet_foot($u, $kind, $upath, 4); ?>
</div>
<?php
echo breadcrumb_ld(array(array(T('worksheets'), ''), array($country['name'], $seg[0] . '/'),
    array($subject['name'], $seg[0] . '/' . $seg[1] . '/'), array($grade['name'], $gbase),
    array($u['short_title'], $upath), array(T('print'), $path)));
?>
<script>
/* shrink text a little if a sheet would spill onto a second page */
(function(){
  var ss = document.querySelectorAll('.pr-sheet');
  for (var i = 0; i < ss.length; i++) {
    var s = ss[i], ph = parseFloat(getComputedStyle(s).minHeight), f = 1;
    while (s.offsetHeight > ph + 1 && f > 0.72) { f -= 0.04; s.style.setProperty('--fs', f.toFixed(2)); }
  }
})();
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js"></script>
<script>
(function(){
  if (typeof qrcode !== 'function') return;
  var els = document.querySelectorAll('.pr-qr[data-qr]');
  for (var i = 0; i < els.length; i++) {
    try {
      var q = qrcode(0, 'M');
      q.addData(els[i].getAttribute('data-qr'));
      q.make();
      els[i].innerHTML = q.createSvgTag({cellSize: 2, margin: 0, scalable: true});
    } catch (e) {}
  }
})();
</script>
</body>
</html>
