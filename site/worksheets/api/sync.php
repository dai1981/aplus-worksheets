<?php
/* =========================================================
   GitHub Actions からのDB更新の受け口
   - 署名（HMAC-SHA256）が合うリクエストだけ受け付ける
   - 書き込むのは ws_country / ws_subject / ws_grade / ws_unit の4テーブルだけ
   - 鍵は inc/secret.php（GitHub には置かない。サーバーに手で1回だけ置く）
   ========================================================= */
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

function out($code, $arr) { http_response_code($code); echo json_encode($arr, JSON_UNESCAPED_UNICODE); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') out(405, array('ok' => false, 'error' => 'POST only'));

$secret = __DIR__ . '/../inc/secret.php';
if (!is_file($secret)) out(403, array('ok' => false, 'error' => 'sync is not enabled (inc/secret.php missing)'));
require $secret;
if (!defined('WS_SYNC_KEY') || strlen(WS_SYNC_KEY) < 32) out(403, array('ok' => false, 'error' => 'bad key setting'));

// --- 署名チェック（5分以内・本文ごと署名）
$t   = isset($_SERVER['HTTP_X_WS_TIME']) ? $_SERVER['HTTP_X_WS_TIME'] : '';
$sig = isset($_SERVER['HTTP_X_WS_SIG'])  ? $_SERVER['HTTP_X_WS_SIG']  : '';
$raw = file_get_contents('php://input');
if (!ctype_digit($t) || abs(time() - (int)$t) > 300) out(401, array('ok' => false, 'error' => 'time'));
if (!hash_equals(hash_hmac('sha256', $t . "\n" . $raw, WS_SYNC_KEY), $sig)) out(401, array('ok' => false, 'error' => 'signature'));

// --- 本文は base64(gzip(JSON))。WAF に HTML/SVG を誤検知させないため
$bin  = base64_decode($raw, true);
$json = ($bin === false) ? false : @gzdecode($bin);
$data = ($json === false) ? null : json_decode($json, true);
if (!is_array($data)) out(400, array('ok' => false, 'error' => 'payload'));

require __DIR__ . '/../inc/config.php';

$COLS = array(
    'ws_country' => array('code', 'name', 'lang', 'hreflang', 'paper', 'standard', 'intro', 'sort'),
    'ws_subject' => array('country', 'slug', 'name', 'intro', 'sort'),
    'ws_grade'   => array('country', 'subject', 'slug', 'name', 'intro', 'sort'),
    'ws_unit'    => array('country', 'subject', 'grade', 'slug', 'title', 'seo_title', 'short_title', 'domain',
                          'standard_code', 'standard_url', 'standard_text', 'meta_desc', 'key_big', 'key_sub',
                          'body_html', 'faq_json', 'sets_json', 'pdf_url', 'sort', 'updated'),
);
$KEYOK = '/^[a-z0-9-]{1,80}$/';

function put($pdo, $table, $cols, $row) {
    $vals = array();
    foreach ($cols as $c) $vals[] = array_key_exists($c, $row) ? $row[$c] : null;
    $sql = 'REPLACE INTO ' . $table . ' (' . implode(',', $cols) . ') VALUES (' . rtrim(str_repeat('?,', count($cols)), ',') . ')';
    $st = $pdo->prepare($sql);
    $st->execute($vals);
}

try {
    $pdo = new PDO(DB_DSN, DB_USER, DB_PASS, array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
    $pdo->beginTransaction();
    $n = array('countries' => 0, 'subjects' => 0, 'grades' => 0, 'units' => 0);
    $done = array();

    $cat = isset($data['catalog']) ? $data['catalog'] : array();
    foreach (array('countries' => 'ws_country', 'subjects' => 'ws_subject', 'grades' => 'ws_grade') as $k => $tb) {
        if (empty($cat[$k])) continue;
        foreach ($cat[$k] as $r) { put($pdo, $tb, $COLS[$tb], $r); $n[$k]++; }
    }

    foreach ((isset($data['units']) ? $data['units'] : array()) as $u) {
        foreach (array('country', 'subject', 'grade', 'slug') as $k) {
            if (!isset($u[$k]) || !preg_match($KEYOK, $u[$k])) throw new Exception('bad key: ' . $k);
        }
        if (empty($u['title']) || empty($u['sets']) || !is_array($u['sets'])) throw new Exception('unit incomplete: ' . $u['slug']);
        $row = $u;
        $row['faq_json']  = json_encode(isset($u['faq']) ? $u['faq'] : array(), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $row['sets_json'] = json_encode($u['sets'], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        foreach (array('seo_title', 'short_title', 'domain', 'standard_code', 'standard_url', 'pdf_url') as $k) {
            if (!isset($row[$k])) $row[$k] = '';
        }
        if (!isset($row['sort'])) $row['sort'] = 0;
        put($pdo, 'ws_unit', $COLS['ws_unit'], $row);
        $n['units']++;
        $done[] = $u['country'] . '/' . $u['subject'] . '/' . $u['grade'] . '/' . $u['slug'];
    }

    $pdo->commit();
    out(200, array('ok' => true, 'count' => $n, 'units' => $done));
} catch (Exception $e) {
    if (isset($pdo) && $pdo->inTransaction()) $pdo->rollBack();
    out(500, array('ok' => false, 'error' => $e->getMessage()));
}
