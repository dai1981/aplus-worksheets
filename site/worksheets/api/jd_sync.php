<?php
/* =========================================================
   GitHub Actions からの日本語辞書（jd_word）更新の受け口
   - 署名（HMAC-SHA256）が合うリクエストだけ受け付ける（鍵は worksheets と同じ inc/secret.php）
   - 書き込むのは jd_word テーブルだけ。行の追加と上書きのみ（DELETE・DROP・ALTER はしない）
   - テーブルが無いときだけ CREATE TABLE IF NOT EXISTS で作る
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

$t   = isset($_SERVER['HTTP_X_WS_TIME']) ? $_SERVER['HTTP_X_WS_TIME'] : '';
$sig = isset($_SERVER['HTTP_X_WS_SIG'])  ? $_SERVER['HTTP_X_WS_SIG']  : '';
$raw = file_get_contents('php://input');
if (!ctype_digit($t) || abs(time() - (int)$t) > 300) out(401, array('ok' => false, 'error' => 'time'));
if (!hash_equals(hash_hmac('sha256', $t . "\n" . $raw, WS_SYNC_KEY), $sig)) out(401, array('ok' => false, 'error' => 'signature'));

// データ本体は FTP で inc/queue/jd.json.gz に置かれている。本文は {"file":"jd.json.gz","sha256":"..."} だけ
$req = json_decode($raw, true);
if (!is_array($req) || !isset($req['file'], $req['sha256']) || $req['file'] !== 'jd.json.gz') out(400, array('ok' => false, 'error' => 'request'));
$qf = __DIR__ . '/../inc/queue/jd.json.gz';
$bin = is_file($qf) ? file_get_contents($qf) : false;
if ($bin === false) out(400, array('ok' => false, 'error' => 'queue file missing'));
if (!hash_equals(hash('sha256', $bin), (string)$req['sha256'])) out(409, array('ok' => false, 'error' => 'queue file hash mismatch'));
$json = @gzdecode($bin);
$data = ($json === false) ? null : json_decode($json, true);
if (!is_array($data) || !isset($data['words']) || !is_array($data['words'])) out(400, array('ok' => false, 'error' => 'payload'));

require __DIR__ . '/../inc/config.php';

try {
    $pdo = new PDO(DB_DSN, DB_USER, DB_PASS, array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
    $pdo->exec('CREATE TABLE IF NOT EXISTS jd_word (
        slug    VARCHAR(100) NOT NULL PRIMARY KEY,
        data    MEDIUMTEXT   NOT NULL,
        hash    CHAR(32)     NOT NULL,
        updated DATE         NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci');
    // 中身が変わった語だけ updated を今日にする（updated を hash より先に書く）
    $st = $pdo->prepare('INSERT INTO jd_word (slug, data, hash, updated) VALUES (?, ?, ?, CURDATE())
        ON DUPLICATE KEY UPDATE updated = IF(hash <> VALUES(hash), CURDATE(), updated), data = VALUES(data), hash = VALUES(hash)');
    $pdo->beginTransaction();
    $n = 0;
    foreach ($data['words'] as $w) {
        if (!isset($w['s']) || !preg_match('/^[a-z0-9-]{1,100}$/', $w['s']) || empty($w['w']) || empty($w['sen'])) throw new Exception('bad word');
        $d = json_encode($w, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $st->execute(array($w['s'], $d, md5($d)));
        $n++;
    }
    $pdo->commit();
    out(200, array('ok' => true, 'count' => $n));
} catch (Exception $e) {
    if (isset($pdo) && $pdo->inTransaction()) $pdo->rollBack();
    out(500, array('ok' => false, 'error' => $e->getMessage()));
}
