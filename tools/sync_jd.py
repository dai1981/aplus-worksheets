# -*- coding: utf-8 -*-
"""
jdict/words/*.json  ->  DB の jd_word テーブル（日本語辞書、1語1行）

  python tools/sync_jd.py --all                 # 全部
  python tools/sync_jd.py --since <commit>      # そのコミット以降に変わったファイルだけ

流れは sync_db.py と同じ（WAF に止められないように2段階）:
  1. 200語ずつ gzip にして FTP で /aplus/worksheets/inc/queue/jd.json.gz に置く（毎回同じ名前で上書き）
  2. api/jd_sync.php に「そのファイルのハッシュ」だけを署名付きで送る → サーバーが jd_word に書く
環境変数: WS_SYNC_KEY, FTP_SERVER, FTP_USERNAME, FTP_PASSWORD
"""
import glob, gzip, hashlib, hmac, json, os, subprocess, sys, tempfile, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
WORDS = os.path.join(ROOT, "jdict", "words")
URL = os.environ.get("JD_SYNC_URL", "https://www.apu2.com/worksheets/api/jd_sync.php")
QUEUE_DIR = os.environ.get("WS_QUEUE_DIR", "/aplus/worksheets/inc/queue")
FTP_OPTS = "set ftp:ssl-allow true; set ssl:verify-certificate no; set net:max-retries 2; set net:timeout 30;"


def files_all():
    return sorted(glob.glob(os.path.join(WORDS, "*.json")))


def files_since(since):
    if not since or set(since) == {"0"}:
        return files_all()
    try:
        names = subprocess.check_output(["git", "diff", "--name-only", "--diff-filter=AM", since, "HEAD", "--", "jdict/words"],
                                        cwd=ROOT, text=True).split()
    except subprocess.CalledProcessError:
        return files_all()
    return [os.path.join(ROOT, n) for n in names if n.endswith(".json")]


def ftp_put(local):
    host, user, pw = os.environ["FTP_SERVER"], os.environ["FTP_USERNAME"], os.environ["FTP_PASSWORD"]
    script = "%s open -u %s,%s %s; mkdir -p -f %s; put %s -o %s/jd.json.gz" % (
        FTP_OPTS, json.dumps(user), json.dumps(pw), json.dumps(host), QUEUE_DIR, json.dumps(local), QUEUE_DIR)
    r = subprocess.run(["lftp", "-c", script], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("FTP upload failed: " + (r.stderr or r.stdout)[-400:].replace(pw, "***"))


def apply(sha, key):
    body = json.dumps({"file": "jd.json.gz", "sha256": sha}).encode()
    t = str(int(time.time()))
    sig = hmac.new(key.encode(), t.encode() + b"\n" + body, hashlib.sha256).hexdigest()
    req = urllib.request.Request(URL, data=body, method="POST", headers={"Content-Type": "application/json", "X-WS-Time": t, "X-WS-Sig": sig})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            res = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        raise SystemExit("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:400]))
    j = json.loads(res)
    if not j.get("ok"):
        raise SystemExit("Server error: " + res[:400])
    return j


def main():
    key = os.environ.get("WS_SYNC_KEY", "")
    if len(key) < 32:
        raise SystemExit("WS_SYNC_KEY is not set")
    a = sys.argv[1:]
    files = files_all() if a[:1] == ["--all"] else files_since(a[1] if len(a) > 1 else "")
    total = 0
    for p in files:
        words = json.load(open(p, encoding="utf-8"))
        data = gzip.compress(json.dumps({"words": words}, ensure_ascii=False).encode("utf-8"))
        with tempfile.NamedTemporaryFile(suffix=".json.gz", delete=False) as f:
            f.write(data)
            tmp = f.name
        try:
            ftp_put(tmp)
        finally:
            os.unlink(tmp)
        j = apply(hashlib.sha256(data).hexdigest(), key)
        total += j["count"]
        print("synced", os.path.basename(p), j["count"])
    print("done: %d word(s) from %d file(s)" % (total, len(files)))


if __name__ == "__main__":
    main()
