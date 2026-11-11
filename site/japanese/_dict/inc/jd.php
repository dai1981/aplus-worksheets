<?php
/* =========================================================
   日本語辞書（PHP + DB）: 設定・DB・文言・ページの型枠
   DB は jd_word テーブルだけを読む（書き込みは worksheets/api/jd_sync.php だけ）
   ========================================================= */

if (!defined('DB_DSN')) require __DIR__ . '/../../../worksheets/inc/config.php';   // DB の接続情報（worksheets と共通）

define('JD_BASE', 'https://www.apu2.com');
define('JD_TEMPLATE', '2026-11-09a');                       // 型枠を変えたら上げる（ETag が変わる）

$__ju = json_decode(file_get_contents(__DIR__ . '/ju.json'), true);
$JU   = $__ju['ui'];
$JM   = $__ju['meta'];
unset($__ju);

function jd_db() {
    static $pdo = null;
    if ($pdo === null) {
        $pdo = new PDO(DB_DSN, DB_USER, DB_PASS, array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                                                      PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC));
    }
    return $pdo;
}
function jd_row($slug) {
    $st = jd_db()->prepare('SELECT data, hash, updated FROM jd_word WHERE slug = ?');
    $st->execute(array($slug));
    $r = $st->fetch();
    return $r ? $r : null;
}
function jd_rows($slugs) {
    $slugs = array_values(array_unique(array_filter($slugs)));
    if (!$slugs) return array();
    $st = jd_db()->prepare('SELECT slug, data FROM jd_word WHERE slug IN (' . rtrim(str_repeat('?,', count($slugs)), ',') . ')');
    $st->execute($slugs);
    $out = array();
    foreach ($st->fetchAll() as $r) $out[$r['slug']] = json_decode($r['data'], true);
    return $out;
}

/* ---------------------------------------------------------------- 文字 */
function e($s) { return htmlspecialchars((string)$s, ENT_QUOTES | ENT_HTML5, 'UTF-8'); }
function jd_fmt($tpl, $v) {
    $r = array();
    foreach ($v as $k => $x) $r['{' . $k . '}'] = $x;
    return strtr($tpl, $r);
}
define('JD_RUBY', '/([\x{3400}-\x{9FFF}\x{F900}-\x{FAFF}々〆ヶケ0-9０-９]+)\[([^\]]+)\]/u');
function jd_ruby($s) {
    $s = htmlspecialchars((string)$s, ENT_COMPAT | ENT_HTML5, 'UTF-8');
    return preg_replace(JD_RUBY, '<ruby>$1<rt>$2</rt></ruby>', $s);
}
function jd_plain($s) { return preg_replace(JD_RUBY, '$1', (string)$s); }
function jd_json($v) { return json_encode($v, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES); }

/* ---------------------------------------------------------------- URL */
function jd_dict_url($L) { return '/japanese/' . $L . '/word/'; }
function jd_word_url($L, $s) { return '/japanese/' . $L . '/word/' . $s . '.html'; }
function jd_home_url($L) { global $JM; return in_array($L, $JM['hub'], true) ? '/' . $L . '/' : '/'; }
function jd_about_url($L) { global $JM; return in_array($L, $JM['hub'], true) ? '/' . $L . '/about.html' : '/about.html'; }
function jd_priv_url($L) { global $JM; return '/privacypolicy.html' . (in_array($L, $JM['priv'], true) ? '?lang=' . $L : ''); }
function jd_crumbs($L) {
    global $JU, $JM;
    $t = $JU[$L];
    $c = array(array($t['home'], jd_home_url($L)));
    if (in_array($L, $JM['jlearn'], true)) $c[] = array($t['learn'], '/japanese/' . $L . '/');
    $c[] = array($t['dict'], jd_dict_url($L));
    return $c;
}

/* ---------------------------------------------------------------- 語の情報 */
function jd_pos($p, $L) {
    global $JU;
    $out = array();
    foreach (explode(',', $p) as $x) {
        $x = trim($x);
        $out[] = isset($JU[$L]['pos'][$x]) ? $JU[$L]['pos'][$x] : $x;
    }
    return implode(', ', $out);
}
function jd_mean($w, $L, $n = 3) {
    $out = array();
    foreach (array_slice($w['sen'], 0, $n) as $s) $out[] = $s[$L];
    return implode('; ', $out);
}
function jd_level($w, $L) { global $JU; return $w['jlpt'] ? 'JLPT ' . $w['jlpt'] : $JU[$L]['cat'][$w['cat']]; }
function jd_head_word($w) { return $w['w'] === $w['k'] ? $w['w'] : $w['w'] . '（' . $w['k'] . '）'; }
function jd_chip($x, $L, $label = null) {
    return '<a class="word-chip" href="' . jd_word_url($L, $x['s']) . '"><span class="chip-en">' . e($label !== null ? $label : $x['w'])
         . '</span><span class="chip-ja">' . e($x['sen'][0][$L]) . '</span></a>';
}

/* ---------------------------------------------------------------- 型枠 */
const JD_SPK = <<<'X'
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M3 9v6h4l5 5V4L7 9H3z"/><path class="wave" d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z" opacity="0.7"/><path class="wave" d="M19 12c0-3.53-2.04-6.58-5-8.05v2.23c2.02 1.29 3.38 3.55 3.38 5.82 0 2.27-1.36 4.53-3.38 5.82v2.23c2.96-1.47 5-4.52 5-8.05z" opacity="0.5"/></svg>
X;
const JD_SPK_S = <<<'X'
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9v6h4l5 5V4L7 9H3z"/><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z" opacity="0.7"/></svg>
X;
const JD_CSS = <<<'X'
<style>
.vi-top{position:relative;z-index:200}
.crumb{max-width:680px;margin:8px auto 0;padding:0 12px;font-size:12.5px;color:var(--ink-sub)}
.crumb a{color:var(--ink-sub);text-decoration:underline}
.lang-sw{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0 4px}
.lang-sw a{font-size:12px;border:1px solid var(--accent-bd);border-radius:999px;padding:3px 10px;color:var(--brand);text-decoration:none;background:#fff}
.faq-q{font-weight:800;color:var(--ink);margin:10px 0 2px}
.faq-a{color:var(--ink-sub);font-size:14px;margin:0 0 8px}
.dict-hero{background:var(--hero-grad);color:#fff;border-radius:16px;padding:18px;margin-bottom:10px}
.dict-hero h1{margin:0 0 6px;font-size:26px;font-weight:900}
.dict-hero p{margin:0;font-size:14px;opacity:.92}
.jrow{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 10px}
.jrow a{min-width:40px;height:38px;padding:0 8px;display:grid;place-items:center;border-radius:8px;font-weight:800;font-size:17px;text-decoration:none;background:var(--brand);color:#fff}
.jrow a.on{background:var(--brand-deep)}
.jrow span{min-width:40px;height:38px;display:grid;place-items:center;border-radius:8px;font-size:17px;background:#e6ece8;color:#9aa69f}
.wl{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr;gap:6px}
@media(min-width:540px){.wl{grid-template-columns:1fr 1fr}}
.wl a{display:flex;flex-direction:column;background:#fff;border:1px solid var(--hairline);border-radius:10px;padding:9px 12px;text-decoration:none}
.wl a:hover{border-color:var(--brand);text-decoration:none}
.wl b{color:var(--brand);font-size:17px}.wl small{color:var(--ink-sub);font-size:12px;margin-left:6px;font-weight:600}.wl span{color:var(--ink-sub);font-size:13px}
.jlv{display:inline-block;font-size:11px;font-weight:800;border-radius:6px;padding:1px 6px;margin-left:6px;background:var(--accent-bg);color:var(--brand-deep);vertical-align:2px}
.j-read{font-size:19px;color:rgba(255,255,255,.92);margin-top:2px;font-weight:700}
.j-rom{font-size:14px;color:rgba(255,255,255,.78)}
[lang=ja]{font-style:normal!important}
.example-en ruby rt,.phrase-en ruby rt{font-size:.55em;color:var(--ink-mute);font-weight:500}
.example-en{line-height:2.1}
.ex-rom{font-size:13px;color:var(--ink-mute);font-style:italic;margin:2px 0}
.kj{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.kj div{background:#fff;border:1px solid var(--hairline);border-radius:10px;padding:10px;display:flex;gap:10px;align-items:center}
.kj b{font-size:34px;line-height:1;color:var(--ink)}
.kj span{font-size:12.5px;color:var(--ink-sub);line-height:1.5}
.wg-kana{font-size:13px;color:var(--ink-sub);font-weight:600;margin-left:6px}
.jcount{display:inline-block;font-size:13px;font-weight:800;color:var(--brand-deep);background:#fff;border:1px solid var(--accent-bd);border-radius:999px;padding:3px 10px;margin:0 6px 6px 0}
.jfilter{display:flex;gap:6px;flex-wrap:wrap;margin:4px 0 10px}
.jfilter button{border:1px solid var(--accent-bd);background:#fff;color:var(--brand);border-radius:999px;padding:4px 12px;font-weight:700;cursor:pointer}
.jfilter button.on{background:var(--brand);color:#fff}
[dir=rtl] .example-en,[dir=rtl] .phrase-en,[dir=rtl] .ex-rom,[dir=rtl] .j-rom,[dir=rtl] .meaning-note,[dir=rtl] .jdict-form input{direction:ltr;unicode-bidi:isolate}
[dir=rtl] .example-en,[dir=rtl] .phrase-en,[dir=rtl] .ex-rom,[dir=rtl] .meaning-note{text-align:right}
[dir=rtl] .warn-box{border-left:0;border-right:4px solid var(--warn-bd);border-radius:10px 0 0 10px}
[dir=rtl] .usage-block{border-left:0;border-right:4px solid var(--accent-soft);padding:8px 13px 8px 0}
.jpn{display:flex;justify-content:space-between;gap:8px;margin:14px 0 0}
.jpn a{flex:1;max-width:49%;background:#fff;border:1px solid var(--hairline);border-radius:10px;padding:9px 12px;text-decoration:none;color:var(--brand);font-weight:700;font-size:14px}
.jpn a.nx{text-align:right;margin-left:auto}
.jpn small{display:block;color:var(--ink-sub);font-weight:600;font-size:11.5px}
.quiz-blank .qx{display:block;margin:6px 0;font-size:17px;line-height:2}
.quiz-blank .qo{display:block;margin:3px 0}
</style>
X;
const JD_QUIZ_JS = <<<'X'
<script>
(function(){var T=%s;document.querySelectorAll('.quiz-card').forEach(function(card){var qs=card.querySelectorAll('.quiz-q'),sc=card.querySelector('.quiz-score'),n=0,c=0;
qs.forEach(function(q){var r=q.getAttribute('data-correct');q.querySelectorAll('.quiz-choice').forEach(function(b){b.addEventListener('click',function(){if(q.classList.contains('answered'))return;q.classList.add('answered');n++;var ok=b.getAttribute('data-ans')===r;if(ok)c++;
q.querySelectorAll('.quiz-choice').forEach(function(x){if(x.getAttribute('data-ans')===r)x.classList.add('correct');else if(x===b&&!ok)x.classList.add('wrong');});
var f=q.querySelector('.quiz-feedback');f.className='quiz-feedback '+(ok?'correct-fb':'wrong-fb');f.textContent=ok?T.ok:T.ng.replace('{a}',r+' '+q.getAttribute('data-a'));
if(sc&&n===qs.length){sc.textContent=T.score.replace('{c}',c).replace('{t}',qs.length);sc.style.display='block';}});});});});})();
</script>
X;

function jd_head($L, $title, $desc, $canon, $alts, $ld) {
    global $JU, $JM;
    $alt = array();
    foreach ($alts as $k => $u) $alt[] = '<link rel="alternate" hreflang="' . $JM['hl'][$k] . '" href="' . JD_BASE . $u . '">';
    $alt[] = '<link rel="alternate" hreflang="x-default" href="' . JD_BASE . $alts['en'] . '">';
    return '<!DOCTYPE html>
<html lang="' . $JM['hl'][$L] . '"' . ($L === 'ar' ? ' dir="rtl"' : '') . '>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>' . e($title) . '</title>
<meta name="description" content="' . e($desc) . '">
<link rel="canonical" href="' . JD_BASE . $canon . '">
' . implode("\n", $alt) . '
<meta property="og:type" content="article">
<meta property="og:url" content="' . JD_BASE . $canon . '">
<meta property="og:title" content="' . e($title) . '">
<meta property="og:description" content="' . e($desc) . '">
<meta property="og:site_name" content="aplus">
<meta property="og:locale" content="' . $JM['og'][$L] . '">
<meta name="google-adsense-account" content="ca-pub-3234684892462480">
<script type="application/ld+json">' . jd_json($ld) . '</script>
<link rel="stylesheet" href="/common/css/word-page.css?v=20261016b">
<link rel="stylesheet" href="/japanese/vi/css/vi-quiz.css?v=20261015a">
' . JD_CSS . '
<script async src="https://www.googletagmanager.com/gtag/js?id=G-JXYPVC45WC"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-JXYPVC45WC\');</script>
</head>
<body>
<header class="vi-top"><div class="in"><a class="vi-brand" href="' . jd_home_url($L) . '">a<span>plus</span></a><a class="vi-crumb" href="' . jd_dict_url($L) . '">' . $JU[$L]['dict'] . '</a></div></header>
';
}

function jd_searchbar($L) {
    global $JU, $JM;
    $t = $JU[$L];
    return '<div class="search-header"><form class="jdict-form" action="' . jd_dict_url($L) . '" data-lang="' . $L . '" data-v="' . $JM['v'] . '" data-empty="' . e($t['empty']) . '">'
         . '<input type="text" name="q" placeholder="' . e($t['search']) . '" aria-label="' . e($t['search']) . '"><!--
    --><button type="submit">' . e($t['btn']) . '</button></form></div>
';
}

function jd_langs($L, $alts) {
    global $JM;
    $h = '';
    foreach ($alts as $k => $u) if ($k !== $L) $h .= '<a href="' . $u . '" lang="' . $JM['hl'][$k] . '">' . $JM['name'][$k] . '</a>';
    return $h;
}

function jd_foot($L, $alts) {
    global $JU, $JM;
    $t = $JU[$L];
    return '<footer class="vi-foot">
  <a href="' . jd_home_url($L) . '">' . $t['home'] . '</a>' . (in_array($L, $JM['jlearn'], true) ? '<a href="/japanese/' . $L . '/">' . $t['learn'] . '</a>' : '')
       . '<a href="' . jd_about_url($L) . '">About</a><a href="' . jd_priv_url($L) . '">Privacy</a>
  <div class="vi-langs" style="margin-top:8px">' . jd_langs($L, $alts) . '</div>
  <div style="margin-top:8px">&copy; aplus</div>
</footer>
<script src="/common/js/pronunciation.js?v=' . $JM['v'] . '"></script>
<script src="/common/js/jdict-suggest.js?v=' . $JM['v'] . '"></script>
<script src="/japanese/vi/js/ad-vi.js?v=20261015a"></script>
</body>
</html>
';
}

function jd_quiz($w, $L, $O, $qz) {
    global $JU;
    $t = $JU[$L];
    $qs = array();
    if (isset($qz['m'])) {
        $opts = array();
        foreach ($qz['m'][0] as $s) $opts[] = isset($O[$s]) ? $O[$s]['sen'][0][$L] : '';
        $qs[] = array(e(jd_fmt($t['q_mean'], array('w' => $w['w']))), $opts, $qz['m'][1], $w['sen'][0][$L], false);
    }
    if (isset($qz['r'])) {
        $qs[] = array(e(jd_fmt($t['q_read'], array('w' => $w['w']))), $qz['r'][0], $qz['r'][1], $w['k'], false);
    }
    if (isset($qz['x']) && !empty($w['ex'])) {
        $opts = array();
        foreach ($qz['x'][0] as $s) $opts[] = (isset($O[$s]) && !empty($O[$s]['ex'])) ? $O[$s]['ex'][0][$L] : '';
        $q = e($t['q_ex']) . '<span class="qx" lang="ja">' . jd_ruby($w['ex'][0]['ja']) . '</span>';
        $qs[] = array($q, $opts, $qz['x'][1], $w['ex'][0][$L], true);
    }
    $out = '';
    $letters = array('A', 'B', 'C', 'D');
    foreach ($qs as $i => $q) {
        list($text, $opts, $correct, $ans, $long) = $q;
        foreach ($opts as $o) if ($o === '') continue 2;          // 選択肢の語が見つからないときは出さない
        $b = array();
        foreach ($letters as $j => $x) $b[] = $long ? '<span class="qo">' . $x . '&nbsp;' . e($opts[$j]) . '</span>' : $x . '&nbsp;' . e($opts[$j]);
        $btns = '';
        foreach ($letters as $x) $btns .= '<button type="button" class="quiz-choice" data-ans="' . $x . '">' . $x . '</button>';
        $out .= '<div class="quiz-q" data-correct="' . $correct . '" data-a="' . e($ans) . '">
  <div class="quiz-blank">Q' . ($i + 1) . '. ' . $text . ($long ? '' : '<br>') . implode($long ? '' : ' &nbsp; ', $b) . '</div>
  <div class="quiz-choices">' . $btns . '</div>
  <div class="quiz-feedback"></div>
</div>';
    }
    return $out;
}

function jd_word_page($w, $L, $O, $qz) {
    global $JU, $JM;
    $t = $JU[$L];
    $s = $w['s'];
    $url = jd_word_url($L, $s);
    $alts = array();
    foreach ($JM['langs'] as $k) $alts[$k] = jd_word_url($k, $s);
    $pos = jd_pos($w['pos'], $L);
    $m = jd_mean($w, $L);
    $fm = array('w' => $w['w'], 'k' => $w['k'], 'r' => $w['r'], 'm' => $m, 'pos' => $pos, 'lv' => $w['jlpt']);
    $title = jd_fmt($w['jlpt'] ? $t['title'] : $t['title2'], $fm);
    $desc = jd_fmt($t['desc'], $fm);
    $ex0 = $w['ex'][0];
    $faqs = array(
        array(jd_fmt($t['faq1'], $fm), jd_head_word($w) . ' (' . $pos . '): ' . $m . '.'),
        array(jd_fmt($t['faq2'], $fm), jd_fmt($t['faq2a'], $fm)),
        array(jd_fmt($t['faq3'], $fm), jd_fmt($t['faq3a'], array('ex' => jd_plain($ex0['ja']), 'tr' => $ex0[$L]))),
    );
    $crumbs = jd_crumbs($L);
    $bl = array();
    foreach (array_merge($crumbs, array(array($w['w'], $url))) as $i => $c) {
        $bl[] = array('@type' => 'ListItem', 'position' => $i + 1, 'name' => $c[0], 'item' => JD_BASE . $c[1]);
    }
    $fq = array();
    foreach ($faqs as $f) $fq[] = array('@type' => 'Question', 'name' => $f[0], 'acceptedAnswer' => array('@type' => 'Answer', 'text' => $f[1]));
    $ld = array('@context' => 'https://schema.org', '@graph' => array(
        array('@type' => 'DefinedTerm', 'name' => $w['w'], 'alternateName' => array($w['k'], $w['r']), 'description' => $m, 'inLanguage' => 'ja',
              'url' => JD_BASE . $url, 'inDefinedTermSet' => array('@type' => 'DefinedTermSet', 'name' => $t['dict'], 'url' => JD_BASE . jd_dict_url($L)),
              'additionalProperty' => array(
                  array('@type' => 'PropertyValue', 'name' => 'reading', 'value' => $w['k']),
                  array('@type' => 'PropertyValue', 'name' => $w['jlpt'] ? 'JLPT' : 'category', 'value' => $w['jlpt'] ? $w['jlpt'] : $JM['cat_en'][$w['cat']]),
                  array('@type' => 'PropertyValue', 'name' => 'part of speech', 'value' => $pos))),
        array('@type' => 'BreadcrumbList', 'itemListElement' => $bl),
        array('@type' => 'FAQPage', 'mainEntity' => $fq)));

    $senses = '';
    foreach ($w['sen'] as $i => $x) {
        $senses .= '<li><span class="meaning-num">' . ($i + 1) . '</span><span><span class="meaning-ja">' . e($x[$L]) . '</span>'
                 . ($L !== 'en' ? '<span class="meaning-note">' . e($x['en']) . '</span>' : '') . '</span></li>';
    }
    $exs = '';
    foreach ($w['ex'] as $x) {
        $exs .= '<div class="usage-block"><div class="example-wrap"><div class="example-en" lang="ja">' . jd_ruby($x['ja'])
              . '<button class="ex-speak-btn" data-word="' . e(jd_plain($x['ja'])) . '" data-lang="ja-JP" aria-label="' . $t['listen'] . '">' . JD_SPK_S . '</button></div>'
              . '<div class="ex-rom">' . e($x['r']) . '</div><div class="example-ja">' . e($x[$L]) . '</div></div></div>';
    }
    $phs = '';
    foreach ($w['ph'] as $x) $phs .= '<div class="phrase-item"><div class="phrase-en" lang="ja">' . jd_ruby($x['ja']) . '</div><div class="phrase-ja">' . e($x[$L]) . '</div></div>';
    $chips = function ($lst) use ($O, $L) {
        $h = '';
        foreach ($lst as $x) $h .= ($x[1] && isset($O[$x[1]])) ? jd_chip($O[$x[1]], $L, $x[0]) : '<span class="word-chip"><span class="chip-en">' . e($x[0]) . '</span></span>';
        return $h;
    };
    $rel = '';
    if (!empty($w['syn'])) $rel .= '<div class="card-title-text">' . $t['syn'] . '</div><div class="chips-grid">' . $chips($w['syn']) . '</div>';
    if (!empty($w['ant'])) $rel .= '<div class="card-title-text" style="margin-top:12px">' . $t['ant'] . '</div><div class="chips-grid">' . $chips($w['ant']) . '</div>';
    $kj = '';
    foreach ($w['kj'] as $k) $kj .= '<div><b lang="ja">' . e($k[0]) . '</b><span>' . $t['on'] . ': ' . e($k[1] !== '' ? $k[1] : '-') . '<br>' . $t['kun'] . ': ' . e($k[2] !== '' ? $k[2] : '-') . '</span></div>';
    $near = '';
    foreach ($w['near'] as $x) if (isset($O[$x])) $near .= jd_chip($O[$x], $L);
    $forms = $w['forms'] !== '' ? '<span class="word-badge">' . $t['forms'] . ': <span lang="ja">' . e($w['forms']) . '</span></span>' : '';
    $read = $w['k'] !== $w['w'] ? '<div class="j-read" lang="ja">' . e($w['k']) . '</div>' : '';
    $faq_html = '';
    foreach ($faqs as $f) $faq_html .= '<p class="faq-q">' . e($f[0]) . '</p><p class="faq-a">' . e($f[1]) . '</p>';
    $cr = array();
    foreach ($crumbs as $c) $cr[] = '<a href="' . $c[1] . '">' . $c[0] . '</a>';
    $pn = '';
    foreach (array('prev' => '', 'next' => ' class="nx"') as $k => $cls) {
        if ($w[$k] && isset($O[$w[$k]])) {
            $x = $O[$w[$k]];
            $pn .= '<a href="' . jd_word_url($L, $x['s']) . '"' . $cls . ' rel="' . $k . '"><small>' . ($k === 'prev' ? '‹ ' . e($t['prev']) : e($t['next']) . ' ›') . '</small><span lang="ja">' . e($x['w']) . '</span></a>';
        }
    }
    $recent = "<script>try{var k='aplus_jrecent_" . $L . "',a=JSON.parse(localStorage.getItem(k)||'[]').filter(function(x){return x[1]!==" . jd_json($s)
            . "});a.unshift([" . jd_json($w['w']) . "," . jd_json($s) . "," . jd_json($w['sen'][0][$L]) . "]);localStorage.setItem(k,JSON.stringify(a.slice(0,10)));}catch(e){}</script>\n";
    $quizjs = sprintf(JD_QUIZ_JS, jd_json(array('ok' => $t['ok'], 'ng' => $t['ng'], 'score' => $t['score'])));

    return jd_head($L, $title, $desc, $url, $alts, $ld) . jd_searchbar($L) . '<nav class="crumb">' . implode(' › ', $cr) . ' › ' . e($w['w']) . '</nav>
<div class="main-wrap">
  <div class="word-title-card">
    <div class="word-title-row">
      <h1 lang="ja">' . e($w['w']) . '</h1>
      <button class="speak-btn" data-word="' . e($w['k']) . '" data-lang="ja-JP" title="' . $t['listen'] . '" aria-label="' . $t['listen'] . '">' . JD_SPK . '</button>
      <span class="word-hinshi">' . e($pos) . '</span>
    </div>
    ' . $read . '<div class="j-rom">' . e($w['r']) . '</div>
    <div class="word-badges"><span class="word-badge">' . e(jd_level($w, $L)) . '</span>' . $forms . '</div>
    <div class="word-meaning-main">' . e($m) . '</div>
  </div>

  <div class="info-card">
    <span class="card-label label-meaning">' . $t['mean'] . '</span>
    <ul class="meaning-list">' . $senses . '</ul>
  </div>

  <div id="adunit"></div>

  <div class="info-card">
    <span class="card-label label-usage">' . $t['ex'] . '</span>
    ' . $exs . '
    <div class="warn-box">' . e($w['note'][$L]) . '</div>
  </div>

  <div class="info-card">
    <span class="card-label label-phrase">' . $t['ph'] . '</span>
    <div class="phrase-grid">' . $phs . '</div>
  </div>

  ' . ($kj ? '<div class="info-card"><span class="card-label">' . $t['kanji'] . '</span><div class="kj">' . $kj . '</div></div>' : '') . '

  ' . ($rel ? '<div class="info-card"><span class="card-label label-related">' . $t['syn'] . ' / ' . $t['ant'] . '</span>' . $rel . '</div>' : '') . '

  <div class="info-card quiz-card">
    <span class="card-label label-quiz">' . $t['quiz'] . '</span>
    ' . jd_quiz($w, $L, $O, $qz) . '
    <div class="quiz-score" style="display:none"></div>
  </div>

  <div class="info-card">
    <span class="card-label">' . $t['faq'] . '</span>
    ' . $faq_html . '
  </div>

  <div class="info-card">
    <span class="card-label label-related">' . $t['related'] . '</span>
    <div class="chips-grid">' . $near . '</div>
    ' . ($pn ? '<nav class="jpn">' . $pn . '</nav>' : '') . '
    <p style="margin:12px 0 0;text-align:center"><a href="' . jd_dict_url($L) . 'row-' . $w['row'] . '.html">' . $t['back'] . '</a></p>
  </div>
  <div class="lang-sw">' . jd_langs($L, $alts) . '</div>
</div>
' . $recent . $quizjs . jd_foot($L, $alts);
}

/* 見つからない語：404 を返し、その言語の辞書へ案内する */
function jd_not_found($L) {
    global $JU;
    if (!isset($JU[$L])) $L = 'en';
    http_response_code(404);
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Robots-Tag: noindex');
    $t = $JU[$L];
    echo '<!DOCTYPE html><html lang="' . e($L) . '"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
       . '<title>' . e($t['dict']) . ' | aplus</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/common/css/word-page.css?v=20261016b"></head><body>'
       . '<div class="main-wrap"><div class="info-card"><p>' . e($t['empty']) . '</p><p><a href="' . jd_dict_url($L) . '">' . e($t['back']) . '</a></p></div></div></body></html>';
    exit;
}
