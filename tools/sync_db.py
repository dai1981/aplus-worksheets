# -*- coding: utf-8 -*-
"""
content/*.json  ->  https://www.apu2.com/worksheets/api/sync.php  (DB の ws_ テーブルを更新)

  python tools/sync_db.py --all                      # 全単元を送る
  python tools/sync_db.py --since <commit>           # そのコミット以降に変わった単元だけ送る
  python tools/sync_db.py us/math/grade-3/area ...   # 指定した単元だけ送る

環境変数 WS_SYNC_KEY（GitHub Secrets）で署名する。catalog.json は毎回送る（小さいため）。
標準ライブラリのみ。
"""
import base64, glob, gzip, hashlib, hmac, json, os, subprocess, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
CONTENT = os.path.join(ROOT, "content")
URL = os.environ.get("WS_SYNC_URL", "https://www.apu2.com/worksheets/api/sync.php")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def all_units():
    out = []
    for p in sorted(glob.glob(os.path.join(CONTENT, "**", "*.json"), recursive=True)):
        if os.path.basename(p) != "catalog.json":
            out.append(p)
    return out


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


def post(payload, key):
    body = base64.b64encode(gzip.compress(json.dumps(payload, ensure_ascii=False).encode("utf-8")))
    t = str(int(time.time()))
    sig = hmac.new(key.encode(), t.encode() + b"\n" + body, hashlib.sha256).hexdigest()
    req = urllib.request.Request(URL, data=body, method="POST", headers={
        "Content-Type": "text/plain", "X-WS-Time": t, "X-WS-Sig": sig,
        "User-Agent": "aplus-worksheets-sync/1"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            res = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        res = e.read().decode("utf-8", "replace")
        raise SystemExit("HTTP %d: %s" % (e.code, res[:500]))
    try:
        j = json.loads(res)
    except ValueError:
        raise SystemExit("Not JSON (WAF?): " + res[:500])
    if not j.get("ok"):
        raise SystemExit("Server error: " + res[:500])
    return j


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

    cat = load(os.path.join(CONTENT, "catalog.json"))
    j = post({"catalog": cat, "units": []}, key)
    print("catalog:", j["count"])

    for p in files:                     # 1単元ずつ送る（1回のリクエストを小さく保つ）
        if not os.path.exists(p):
            continue
        j = post({"units": [load(p)]}, key)
        print("unit:", ", ".join(j["units"]))
    print("done: %d unit(s)" % len(files))


if __name__ == "__main__":
    main()
