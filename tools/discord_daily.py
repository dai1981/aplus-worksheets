# -*- coding: utf-8 -*-
"""
Discord の #daily-word に「今日の単語」を1つ投稿する（GitHub Actions が毎朝実行）。
  DISCORD_WEBHOOK_DAILY=... python3 tools/discord_daily.py [--dry] [--date YYYY-MM-DD]
語は jdict/words/*.json から選ぶ。同じ日付なら必ず同じ語になる（再実行しても重ならない）。
名前・地名・ブランドは除き、JLPT の語・文法・アニメ・スラング・文化・ことわざから選ぶ。
"""
import datetime, glob, json, os, random, re, sys, urllib.request

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BASE = "https://www.apu2.com/japanese/%s/word/%s.html"
LANGS = ['en', 'vi', 'zh', 'tw', 'ko', 'id', 'es', 'pt', 'fr', 'de', 'ru', 'th', 'ar']
LABEL = {'en': 'English', 'vi': 'Tiếng Việt', 'zh': '简体中文', 'tw': '繁體中文', 'ko': '한국어', 'id': 'Indonesia', 'es': 'Español',
         'pt': 'Português', 'fr': 'Français', 'de': 'Deutsch', 'ru': 'Русский', 'th': 'ไทย', 'ar': 'العربية'}
SKIP_CAT = {'name', 'place', 'brand'}


def pool():
    words = []
    for f in sorted(glob.glob(os.path.join(REPO, "jdict", "words", "*.json"))):
        for r in json.load(open(f, encoding="utf-8")):
            if r.get('cat') in SKIP_CAT or not r.get('ex') or not r.get('sen'):
                continue
            words.append(r)
    words.sort(key=lambda r: r['s'])
    random.Random(20261112).shuffle(words)   # 並びを固定（毎日1つずつ進む）
    return words


def plain(ja):
    return re.sub(r'\[[^\]]*\]', '', ja)


def message(r, day):
    lv = 'JLPT ' + r['jlpt'] if r.get('jlpt') else {'grammar': 'JLPT grammar', 'works': 'Anime & manga', 'anime': 'Anime & manga', 'slang': 'Slang',
                                                   'culture': 'Japanese culture', 'proverb': 'Idiom & proverb'}.get(r.get('cat'), 'Japanese')
    head = r['w'] + ('' if r['w'] == r['k'] else '（' + r['k'] + '）')
    lines = ['**%s** · %s · %s' % (head, r['r'], lv), '']
    for L in LANGS:
        m = r['sen'][0].get(L)
        if m:
            lines.append('%s: %s' % (LABEL[L], m))
    ex = r['ex'][0]
    lines += ['', '> ' + plain(ex['ja']), '> ' + ex.get('en', '')]
    links = ' · '.join('[%s](%s)' % (L.upper(), BASE % (L, r['s'])) for L in LANGS)
    lines += ['', links]
    return {
        "username": "Word of the Day",
        "allowed_mentions": {"parse": []},
        "embeds": [{
            "title": "Word of the Day — " + head,
            "url": BASE % ('en', r['s']),
            "description": "\n".join(lines)[:4000],
            "color": 0x5865F2,
            "footer": {"text": "aplus Japanese Dictionary · " + day},
        }],
    }


def main():
    dry = '--dry' in sys.argv
    day = sys.argv[sys.argv.index('--date') + 1] if '--date' in sys.argv else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()
    ws = pool()
    n = (datetime.date.fromisoformat(day) - datetime.date(2026, 11, 12)).days
    r = ws[n % len(ws)]
    body = message(r, day)
    if dry:
        print(json.dumps(body, ensure_ascii=False, indent=1))
        return
    url = os.environ.get("DISCORD_WEBHOOK_DAILY", "")
    if not url.startswith("https://"):
        sys.exit("DISCORD_WEBHOOK_DAILY is not set")
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": "aplus-daily-word (https://www.apu2.com, 1.0)"})
    with urllib.request.urlopen(req, timeout=30) as res:
        print("posted", r['s'], res.status)


if __name__ == "__main__":
    main()
