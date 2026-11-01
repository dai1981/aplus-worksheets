# Aplus worksheets — 自動アップロード＆DB更新

main に push すると、GitHub Actions が次の3つを自動で行います。

1. 問題データのチェック（`tools/check.py`）。エラーがあればここで止まり、本番は変わりません
2. `site/worksheets/` をロリポップの `/aplus/worksheets/` へ FTP アップロード（上書きのみ・削除なし）
3. 変わった単元だけを DB（ws_ テーブル）へ反映（`tools/sync_db.py` → `api/sync.php`）
   - データは FTP で `inc/queue/sync.json.gz` に置いて取り込みます（ロリポップのWAFに止められないため）。毎回同じ名前で上書きするので、ファイルは増えません

## 初回設定（1回だけ）

### 1. サーバーに鍵ファイルを置く
別に送った `secret.php` を FFFTP で **`/aplus/worksheets/inc/`** に置く。
（inc フォルダは外から見えない設定になっています）

### 2. GitHub に Secrets を4つ登録
リポジトリの **Settings → Secrets and variables → Actions → New repository secret**

| 名前 | 値 |
|------|----|
| `FTP_SERVER`   | 他のリポジトリと同じ |
| `FTP_USERNAME` | 他のリポジトリと同じ |
| `FTP_PASSWORD` | 他のリポジトリと同じ |
| `WS_SYNC_KEY`  | `secret.php` の `'...'` の中の文字列 |

### 3. 1回目の実行
**Actions → Deploy worksheets (apu2.com) → Run workflow**
（`DB: send every unit` にチェックを入れると全単元をDBへ送ります）

## 安全のしくみ

- DB のパスワードは GitHub に置きません。サーバー上の既存 `dbConnection.php` を使います
- `api/sync.php` は鍵で署名されたリクエストだけ受け付け、5分以上前のものは拒否します
- 書き込むのは ws_country / ws_subject / ws_grade / ws_unit の4テーブルだけ。削除はしません
- FTP はアップロード（上書き）のみで、サーバーのファイルを削除しません。送るのは `site/worksheets/` にあるファイルだけで、`secret.php` や `/aplus/` の他のフォルダは触りません
- 不要になったファイルをサーバーから消したいときは、FFFTP で手作業で消してください

## うまくいかないとき

| 表示 | 対処 |
|------|------|
| `HTTP 403 ... secret.php missing` | 手順1の場所を確認 |
| `HTTP 401 signature` | `WS_SYNC_KEY` と `secret.php` の文字列が同じか確認 |
| `queue file hash mismatch` | もう一度 Run workflow |
| FTP で失敗 | deploy.yml の `set ftp:ssl-allow true;` を `false` に変えて再実行 |

## 手作業で入れたいとき（予備）

`python tools/build_add.py out.sql us/math/grade-3/perimeter` で SQL を作り、phpMyAdmin でインポート。
