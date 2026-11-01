# -*- coding: utf-8 -*-
"""
content/*.json  ->  DB の ws_ テーブル

  python tools/sync_db.py --all                      # 全単元
  python tools/sync_db.py --since <commit>           # そのコミット以降に変わった単元だけ
  python tools/sync_db.py us/math/grade-3/area ...   # 指定した単元だけ

流れ（ロリポップの WAF に止められないように2段階）:
  1. データを gzip にして FTP で /aplus/worksheets/inc/queue/sync.json.gz に置く（毎回同じ名前で上書き。ファイルは増えない）
  2. api/sync.php に「そのファイルのハッシュ」だけを署名付きで送る → サーバーが取り込む

環境変数: WS_SYNC_KEY, FTP_SERVER, FTP_USERNAME, FTP_PASSWORD（GitHub Secrets）。lftp を使う。
"""
import glob, gzip, hashlib, hmac, json, os, subprocess, sys, tempfile, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
CONTENT = os.path.join(ROOT, "content")
URL = os.environ.get("WS_SYNC_URL", "https://www.apu2.com/worksheets/api/sync.php")
QUEUE_DIR = os.environ.get("WS_QUEUE_DIR", "/aplus/worksheets/inc/queue")
FTP_OPTS = os.environ.get("WS_FTP_OPTS", "set ftp:ssl-allow true; set ssl:verify-certificate no; set net:max-retries 2; set net:timeout 30;")
CHUNK = 10                              # 1回に取り込む単元数（サーバーのメモリを使いすぎない）


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def all_units():
    return [p for p in sorted(glob.glob(os.path.join(CONTENT, "**", "*.json"), recursive=True))
            if os.path.basename(p) != "catalog.json"]


def changed_units(since):
    if not since or set(since) == {"0"}:
        return all_units()
    try:
        names = subprocess.check_output(
            ["git", "diff", "--name-only", "--diff-filter=AM", since, "HEAD", "--", "content"],
            cwd=ROOT, text=True).split()
    except subprocess.CalledProcessError:
        print("git diff failed, sending all units")
        return all_units()
    return [os.path.join(ROOT, n) for n in names
            if n.endswith(".json") and os.path.basename(n) != "catalog.json"]


def ftp_put(local):
    """lftp で queue に置く（上書きのみ。削除はしない）"""
    host, user, pw = os.environ["FTP_SERVER"], os.environ["FTP_USERNAME"], os.environ["FTP_PASSWORD"]
    port = os.environ.get("WS_FTP_PORT", "")
    script = "%s open %s-u %s,%s %s; mkdir -p -f %s; put %s -o %s/sync.json.gz" % (
        FTP_OPTS, ("-p %s " % port) if port else "", json.dumps(user), json.dumps(pw), json.dumps(host),
        QUEUE_DIR, json.dumps(local), QUEUE_DIR)
    r = subprocess.run(["lftp", "-c", script], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("FTP upload of queue file failed: " + (r.stderr or r.stdout)[-400:].replace(pw, "***"))


def apply(sha, key):
    body = json.dumps({"file": "sync.json.gz", "sha256": sha}).encode()
    t = str(int(time.time()))
    sig = hmac.new(key.encode(), t.encode() + b"\n" + body, hashlib.sha256).hexdigest()
    req = urllib.request.Request(URL, data=body, method="POST", headers={
        "Content-Type": "application/json", "X-WS-Time": t, "X-WS-Sig": sig})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            res = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        res = e.read().decode("utf-8", "replace")
        raise SystemExit("HTTP %d: %s" % (e.code, res[:400]))
    try:
        j = json.loads(res)
    except ValueError:
        raise SystemExit("Not JSON: " + res[:400])
    if not j.get("ok"):
        raise SystemExit("Server error: " + res[:400])
    return j


def send(payload, key):
    data = gzip.compress(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
    with tempfile.NamedTemporaryFile(suffix=".json.gz", delete=False) as f:
        f.write(data)
        tmp = f.name
    try:
        ftp_put(tmp)
    finally:
        os.unlink(tmp)                  # 手元（GitHub 側）の一時ファイルだけを消す
    return apply(hashlib.sha256(data).hexdigest(), key)


def main():
    key = os.environ.get("WS_SYNC_KEY", "")
    if len(key) < 32:
        raise SystemExit("WS_SYNC_KEY is not set")
    args = sys.argv[1:]
    if args[:1] == ["--all"]:
        files = all_units()
    elif args[:1] == ["--since"]:
        files = changed_units(args[1] if len(args) > 1 else "")
    else:
        files = [os.path.join(CONTENT, a + ".json") for a in args]
    files = [p for p in files if os.path.exists(p)]

    cat = load(os.path.join(CONTENT, "catalog.json"))
    chunks = [files[i:i + CHUNK] for i in range(0, len(files), CHUNK)] or [[]]
    for i, ch in enumerate(chunks):
        payload = {"units": [load(p) for p in ch]}
        if i == 0:
            payload["catalog"] = cat
        j = send(payload, key)
        print("synced:", j["count"], ", ".join(j["units"]))
    print("done: %d unit(s)" % len(files))


if __name__ == "__main__":
    main()
