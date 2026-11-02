# Aplus worksheets（apu2.com/worksheets/）

各国の学習指導要領に沿った、無料のレッスン＋100問クイズ＋印刷用プリント（4ページ）。
ページは PHP が DB から作る動的ページ。**静的HTMLは作らない**（ロリポップのファイル数上限のため）。

## 仕組み

| 場所 | 中身 | 本番への反映 |
|------|------|-------------|
| `site/worksheets/` | PHP・CSS・JS（ページの型枠） | GitHub Actions が FTP で `/aplus/worksheets/` へ |
| `content/catalog.json` | 国・教科・学年 | Actions が `api/sync.php` 経由で DB（ws_country / ws_subject / ws_grade） |
| `content/{国}/{教科}/{学年}/{単元}.json` | 1単元のレッスン・問題 | Actions が DB の ws_unit へ（変わった単元だけ） |
| `tools/gen_*.py` | 単元JSONを作る生成スクリプト | （実行してJSONをコミットする） |
| `tools/check.py` | 公開前チェック | Actions が毎回実行。エラーなら止まる |

main に push すると `.github/workflows/deploy.yml` が「チェック → FTP → DB更新」を自動で行う。
FTP は上書きのみ（`--delete` を絶対に付けない）。DB は ws_ の4テーブルへの REPLACE だけ（DELETE・DROP・ALTER を書かない）。

## 「次の単元」と言われたら

1. 下のロードマップで、まだ `content/` に無い最初の単元を選ぶ
2. `tools/gen_{国}_{教科}_{学年}_{単元}.py` を新しく作る（既存の `gen_us_math_g3_time.py` などと同じ形）
   - 出力: `content/{国}/{教科}/{学年}/{slug}.json`
   - `random.Random(固定の数)` を使い、何度実行しても同じ問題になるようにする
3. `python3 tools/gen_....py` を実行
4. `python3 tools/check.py` がエラー0・警告0になるまで直す
5. 生成スクリプトとJSONを **main に直接コミット**して push（ブランチ・PRは作らない）
   - メッセージ例: `Add us/math/grade-3/perimeter (3.MD.D.8)`
6. ユーザーには短く日本語で、作った単元と確認URLを伝える
   - 例: https://www.apu2.com/worksheets/us/math/grade-3/perimeter/

## 単元JSONの形

```json
{
  "country": "us", "subject": "math", "grade": "grade-3", "slug": "perimeter",
  "title": "H1", "seo_title": "<title>", "short_title": "Perimeter",
  "domain": "学年ページでのグループ見出し（例: Measurement & Data）",
  "standard_code": "3.MD.D.8", "standard_url": "...", "standard_text": "基準の原文",
  "meta_desc": "...", "key_big": "一番大事な考え（大きく表示）", "key_sub": "補足",
  "body_html": "レッスン本文のHTML", "faq": [{"q": "...", "a": "..."}],
  "sets": [ {"title": "セット名", "items": [ {"q": "問題HTML", "c": ["4つの選択肢"], "a": 0, "e": "解説"} ] } ],
  "pdf_url": "", "sort": 7, "updated": "YYYY-MM-DD"
}
```

- セットは **5つ、各20問**（合計100問）。易しい → 難しい の順。最後は文章題
- `sort` は学年ページでの並び順。既存の最大値＋1
- HTML の属性は **シングルクォート**、バックスラッシュ禁止（`check.py` で検出）
- 図は inline SVG（`viewBox='0 0 W H'` を必ず付ける）。時計など正方形の図は印刷で大きく出る
- 分数は `<span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>`

## 品質ルール（学習者に分かりやすく、正確に）

- 誤答は「よくある間違い」から作る（適当な数字にしない）
- 英語の文法を確認: `1 minute`（複数形にしない）、`p.m.` の後に `.` を重ねない、人名と代名詞の一致
- 場面と数値を現実に合わせる（登校は朝、映画は夜、9:60 のような時刻を作らない）
- 同じ問題を繰り返さない。答えが0になる問題（9:00 to 9:00）を作らない
- `body_html` は「考え方 → 例 → よくある間違い」の順で、短い文で
- 絵文字は使わない（必要ならSVG）

## ロードマップ（効果の高い順）

US / Math / Grade 3（Common Core）
1. multiplication-facts ✓ 2. division-facts ✓ 3. rounding ✓ 4. fractions ✓ 5. telling-time ✓ 6. area ✓
7. perimeter ✓
8. add-subtract-within-1000 ✓
9. two-step-word-problems ✓
10. picture-and-bar-graphs ✓
11. line-plots-measurement ✓
12. quadrilaterals ✓
13. mass-and-volume ✓
14. multiply-by-multiples-of-10 ✓
15. properties-of-multiplication ✓
16. partition-shapes ✓

US / Math / Grade 4（Common Core）
1. multi-digit-multiplication ✓
2. long-division ✓
3. equivalent-fractions ✓
4. compare-fractions ✓
5. add-subtract-fractions ✓
6. multiply-fractions-by-whole-numbers ✓
7. decimals-tenths-hundredths ✓
8. place-value-rounding ✓
9. add-subtract-multi-digit ✓
10. factors-multiples-prime ✓
11. multiplicative-comparison-word-problems ✓
12. measurement-conversions ✓
13. area-perimeter-formulas ✓
14. measuring-angles ✓
15. lines-angles-shapes ✓
16. line-symmetry ✓
17. number-shape-patterns ✓
18. line-plots-fractions ✓

Grade 4 からは 1,000 以上の数にカンマを付ける（例: 4,536）。

US / Math / Grade 2（Common Core）— 1000 まで（カンマなし。Grade 3 と同じ）。文は短く、7〜8歳が読める英語で
1. addition-subtraction-facts ✓
2. add-subtract-within-100 ✓
3. word-problems-within-100 ✓
4. place-value ✓
5. counting-money ✓
6. telling-time-5-minutes ✓
7. add-subtract-within-1000 ✓
8. compare-three-digit-numbers ✓
9. skip-counting ✓
10. odd-and-even ✓
11. arrays-repeated-addition ✓
12. measuring-length ✓
13. length-word-problems ✓
14. graphs-and-line-plots ✓
15. shapes-and-attributes ✓
16. halves-thirds-fourths ✓

US / Math / Grade 5（Common Core）— 1,000 以上はカンマ付き
1. add-subtract-fractions-unlike（5.NF.A.1-2）
2. multiply-fractions（5.NF.B.4, B.6）
3. divide-fractions（5.NF.B.7）
4. add-subtract-decimals（5.NBT.B.7）
5. multiply-divide-decimals（5.NBT.B.7）
6. volume（5.MD.C.3-5）
7. numerical-expressions（5.OA.A.1-2）
8. coordinate-plane（5.G.A.1-2）
9. multi-digit-multiplication（5.NBT.B.5）
10. long-division-two-digit-divisors（5.NBT.B.6）
11. decimal-place-value-rounding（5.NBT.A.1-4）
12. fractions-as-division（5.NF.B.3）
13. multiplication-as-scaling（5.NF.B.5）
14. measurement-conversions（5.MD.A.1）
15. classify-two-dimensional-figures（5.G.B.3-4）
16. patterns-and-relationships（5.OA.B.3）
17. line-plots-fractions（5.MD.B.2）

その後: UK / Australia / Canada …（新しい学年・国は `catalog.json` に追加）

## 触ってはいけないもの

- `site/worksheets/inc/secret.php`（サーバーにだけある鍵。リポジトリに入れない）
- DB は ws_ で始まる4テーブル以外を変更しない（`api/sync.php` もこの4つしか書かない）
- `/aplus/` の他のフォルダ、`/aplus/sitemap.php`（このリポジトリの外）
