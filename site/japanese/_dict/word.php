<?php
/* =========================================================
   日本語辞書の単語ページ（/japanese/{L}/word/{slug}.html）
   DB の jd_word（1語1行、全言語の訳を JSON で持つ）から作る。
   ルーティングは /japanese/.htaccess（静的な .html があるうちはそちらが優先）。
   ========================================================= */

require __DIR__ . '/inc/jd.php';

$L = isset($_GET['l']) ? (string)$_GET['l'] : '';
$S = isset($_GET['s']) ? (string)$_GET['s'] : '';
if (!isset($JU[$L]) || !preg_match('/^[a-z0-9-]{1,100}$/', $S)) jd_not_found($L ?: 'en');

try {
    $row = jd_row($S);
} catch (Exception $e) {
    http_response_code(503);
    header('Retry-After: 300');
    exit('Temporarily unavailable.');
}
if (!$row) jd_not_found($L);
$w = json_decode($row['data'], true);
if (!is_array($w)) jd_not_found($L);

// --- キャッシュ（中身・型枠・言語が同じなら 304）
$etag = '"jd-' . md5($row['hash'] . '|' . $L . '|' . JD_TEMPLATE) . '"';
header('ETag: ' . $etag);
header('Cache-Control: public, max-age=86400');
// ロリポップ（LiteSpeed）のサーバー側キャッシュ：同じページは1日 PHP・DB を通さずに返す
header('X-LiteSpeed-Cache-Control: public,max-age=86400');
if (!empty($row['updated'])) header('Last-Modified: ' . gmdate('D, d M Y H:i:s', strtotime($row['updated'] . ' 00:00:00')) . ' GMT');
if (isset($_SERVER['HTTP_IF_NONE_MATCH']) && trim($_SERVER['HTTP_IF_NONE_MATCH']) === $etag) { http_response_code(304); exit; }

// --- 関連語（近くの語・類義語・反義語・クイズの選択肢・前後の語）をまとめて読む
$need = array();
foreach ($w['near'] as $x) $need[] = $x;
foreach (array('syn', 'ant') as $k) foreach ($w[$k] as $x) if ($x[1]) $need[] = $x[1];
$qz = isset($w['quiz'][$L]) ? $w['quiz'][$L] : $w['quiz']['*'];
foreach (array('m', 'x') as $k) if (isset($qz[$k])) foreach ($qz[$k][0] as $x) $need[] = $x;
if ($w['prev']) $need[] = $w['prev'];
if ($w['next']) $need[] = $w['next'];
$O = jd_rows($need);
$O[$w['s']] = $w;

header('Content-Type: text/html; charset=UTF-8');
echo jd_word_page($w, $L, $O, $qz);
