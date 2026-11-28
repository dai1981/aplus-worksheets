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

## トピック別ページとプレビュー画像（毎回あわせて強くする）

- トピック別ページ `/{国}/{教科}/topics/{topic}/` は `site/worksheets/inc/topics.php` の正規表現（単元 slug に一致）で自動で集まる。3単元以上で公開
- 新しい単元を作ったら、どのトピックに入るか確認する（`unit_topic_slugs()`）。どれにも入らない・違うトピックに入るときは `in`/`out` の正規表現を直す
- 新しい分野が3単元以上たまったら、`topic_defs()` に新しいトピックを足す（name・blurb、英国式は name_gb/blurb_gb）
- プレビュー画像 `.../preview.png`（1200×630、og:image・サイトマップ）は単元・学年・トピックで自動。ファイルは作らない（毎回 PHP の GD で描く）
- 新しい国は `topic_gb()`（英国式の綴り）と core.php の UI 文言を確認する

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

新しい国は GDP の高い順（中国本土は Google が使えず AdSense の効果が小さいので後回し）

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
1. add-subtract-fractions-unlike ✓
2. multiply-fractions ✓
3. divide-fractions ✓
4. add-subtract-decimals ✓
5. multiply-divide-decimals ✓
6. volume ✓
7. numerical-expressions ✓
8. coordinate-plane ✓
9. multi-digit-multiplication ✓
10. long-division-two-digit-divisors ✓
11. decimal-place-value-rounding ✓
12. fractions-as-division ✓
13. multiplication-as-scaling ✓
14. measurement-conversions ✓
15. classify-two-dimensional-figures ✓
16. patterns-and-relationships ✓
17. line-plots-fractions ✓

US / Math / Grade 6（Common Core）— 1,000 以上はカンマ付き。負の数は「−」（U+2212）
1. ratios ✓
2. unit-rates ✓
3. ratio-tables ✓
4. percents ✓
5. divide-fractions-by-fractions ✓
6. gcf-and-lcm ✓
7. negative-numbers ✓
8. exponents-order-of-operations ✓
9. one-step-equations ✓
10. writing-evaluating-expressions ✓
11. equivalent-expressions ✓
12. area-of-polygons ✓
13. absolute-value-and-ordering ✓
14. coordinate-plane-four-quadrants ✓
15. inequalities ✓
16. mean-median-mode-range ✓
17. surface-area-nets ✓
18. volume-fractional-edges ✓
19. decimal-operations ✓
20. converting-units-with-ratios ✓

US / Math / Grade 1（Common Core）— 120 まで（カンマなし）。文はとても短く、6〜7歳が読める英語で。絵（SVG）を多く
1. addition-subtraction-within-20 ✓
2. word-problems-within-20 ✓
3. add-three-numbers ✓
4. place-value-tens-ones ✓
5. count-to-120 ✓
6. compare-two-digit-numbers ✓
7. add-within-100 ✓
8. ten-more-ten-less ✓
9. subtract-multiples-of-10 ✓
10. telling-time-hour-half-hour ✓
11. measuring-length ✓
12. equal-sign-missing-numbers ✓
13. addition-subtraction-strategies ✓
14. organize-data ✓
15. shapes-and-attributes ✓
16. halves-and-fourths ✓

UK / Maths / Year 4（National Curriculum in England）— country `uk`、subject `maths`、grade `year-N`、A4。
イギリス英語（colour, metre, maths, pupils, £/p, trapezium, exchange）。1,000 以上はカンマ。standard_code は「Year 4: 分野名」
1. times-tables ✓
2. place-value ✓
3. rounding ✓
4. roman-numerals ✓
5. column-addition-and-subtraction ✓
6. mental-multiplication-and-division ✓
7. short-multiplication ✓
8. fractions ✓
9. decimals ✓
10. money ✓
11. converting-units ✓
12. area-and-perimeter ✓
13. time-12-and-24-hour-clock ✓
14. angles-and-shapes ✓
15. lines-of-symmetry ✓
16. coordinates ✓
17. bar-charts-and-time-graphs ✓

UK / Maths / Year 6（KS2 SATs の学年）— Year 4 と同じルール
1. place-value-and-rounding ✓
2. long-multiplication ✓
3. long-division ✓
4. order-of-operations ✓
5. factors-multiples-and-primes ✓
6. simplifying-and-comparing-fractions ✓
7. adding-and-subtracting-fractions ✓
8. multiplying-and-dividing-fractions ✓
9. fractions-decimals-and-percentages ✓
10. decimal-calculations ✓
11. percentages-of-amounts ✓
12. ratio-and-proportion ✓
13. algebra ✓
14. converting-units ✓
15. area-perimeter-and-volume ✓
16. angles ✓
17. circles-and-nets ✓
18. coordinates-and-transformations ✓
19. pie-charts-and-line-graphs ✓
20. mean ✓

UK / Maths / Year 5 — Year 4 と同じルール
1. place-value-to-a-million ✓
2. rounding ✓
3. roman-numerals-to-1000 ✓
4. column-addition-and-subtraction ✓
5. factors-multiples-and-primes ✓
6. multiplication ✓
7. short-division ✓
8. multiply-and-divide-by-10-100-1000 ✓
9. equivalent-fractions-and-mixed-numbers ✓
10. adding-and-subtracting-fractions ✓
11. multiplying-fractions ✓
12. decimals-and-percentages ✓
13. converting-units ✓
14. area-and-perimeter ✓
15. measuring-angles ✓
16. reflection-and-translation ✓
17. line-graphs-and-tables ✓

UK / Maths / Year 3 — 1,000 まで。文は短く、絵を多く
1. place-value ✓
2. mental-addition-and-subtraction ✓
3. column-addition-and-subtraction ✓
4. 3-4-and-8-times-tables ✓
5. multiplication-and-division ✓
6. fractions ✓
7. tenths-and-adding-fractions ✓
8. measuring-length-mass-and-capacity ✓
9. perimeter ✓
10. money ✓
11. telling-the-time ✓
12. angles-and-lines ✓
13. 2d-and-3d-shapes ✓
14. bar-charts-and-pictograms ✓

UK / Maths / Year 2（KS1）— 100 まで。文はとても短く、絵を多く
1. place-value-to-100 ✓
2. counting-in-2s-3s-5s-and-10s ✓
3. number-bonds-to-20-and-100 ✓
4. adding-and-subtracting-2-digit-numbers ✓
5. 2-5-and-10-times-tables ✓
6. multiplication-and-division ✓
7. fractions ✓
8. money ✓
9. telling-the-time-to-5-minutes ✓
10. measuring ✓
11. 2d-and-3d-shapes ✓
12. position-and-direction ✓
13. pictograms-and-tally-charts ✓

UK / Maths / Year 1（KS1）— 100 まで（計算は 20 まで）。とても短い文、ほぼ全問に絵
1. counting-to-100 ✓
2. number-bonds-to-10-and-20 ✓
3. addition-and-subtraction-within-20 ✓
4. counting-in-2s-5s-and-10s ✓
5. halves-and-quarters ✓
6. length-height-mass-and-capacity ✓
7. money ✓
8. time ✓
9. 2d-and-3d-shapes ✓
10. position-and-direction ✓

UK / Maths / Year 7–9（KS3。National Curriculum の KS3 は 3 学年まとめての内容なので、White Rose 等の一般的な配分で学年に分ける）— Year 4 と同じルール。
生成スクリプトは `gen_uk_maths_y7_*`、共通部品は `tools/uk_ks3.py`（ws_common の上に UK の名前・£・make）。負の数は「−」。standard_code は「KS3: Number」形式（Number／Algebra／Ratio, proportion and rates of change／Geometry and measures／Probability／Statistics）

UK / Maths / Year 7
1. place-value-and-ordering ✓ 2. negative-numbers ✓ 3. order-of-operations ✓ 4. factors-multiples-and-primes ✓ 5. powers-and-roots ✓
6. rounding-and-estimation ✓ 7. fractions-decimals-and-percentages ✓ 8. adding-and-subtracting-fractions ✓ 9. multiplying-and-dividing-fractions ✓
10. percentages-of-amounts ✓ 11. algebraic-notation-and-substitution ✓ 12. simplifying-expressions ✓ 13. solving-equations ✓ 14. sequences ✓
15. ratio-and-proportion ✓ 16. angles ✓ 17. perimeter-and-area ✓ 18. coordinates-and-straight-line-graphs ✓ 19. averages-and-range ✓ 20. probability ✓

UK / Maths / Year 8
1. indices ✓ 2. standard-form ✓ 3. expanding-and-factorising ✓ 4. equations-with-unknowns-on-both-sides ✓ 5. inequalities ✓
6. changing-the-subject-of-a-formula ✓ 7. linear-graphs ✓ 8. percentage-change-and-interest ✓ 9. direct-and-inverse-proportion ✓
10. speed-distance-and-time ✓ 11. circles ✓ 12. volume-and-surface-area-of-prisms ✓ 13. angles-in-parallel-lines-and-polygons ✓
14. transformations ✓ 15. probability-of-combined-events ✓ 16. frequency-tables-and-charts ✓ 17. units-and-scale-drawings ✓

UK / Maths / Year 9
1. pythagoras-theorem ✓ 2. trigonometry ✓ 3. similarity-and-congruence ✓ 4. expanding-and-factorising-quadratics ✓ 5. simultaneous-equations ✓
6. quadratic-graphs ✓ 7. arithmetic-and-geometric-sequences ✓ 8. compound-interest-and-growth ✓ 9. volume-of-cylinders-cones-and-spheres ✓
10. arcs-and-sectors ✓ 11. bearings-and-loci ✓ 12. scatter-graphs-and-correlation ✓ 13. plans-and-elevations ✓ 14. real-life-graphs ✓
15. rounding-and-error-intervals ✓ 16. ratio-problems-and-best-buys ✓

UK / Maths / Year 10–11（KS4、GCSE Mathematics。DfE の GCSE subject content を一般的な配分で 2 学年に分ける）— Year 4 と同じルール。standard_code は「KS4: Algebra」形式、standard_url は GCSE mathematics subject content。
生成スクリプトは `gen_uk_maths_y10_*`・`gen_uk_maths_y11_*`（seed は 910NN・911NN）、共通部品は `tools/uk_gcse.py`：
port(他国の生成スクリプト名, seed, year, slug, sort, strand, std_text, title, short, meta=, rep=[(古い, 新しい)], swap={"one_x": 自前の関数}, set_titles=, body=, faq=, kb=, ks=) で SG Secondary・US 高校の build() を新しい seed と UK の名前・£・数の書き方で動かし、文をイギリス式に直して（ukify：Secondary N→Year N、O-Level→GCSE、$→£、空白区切り→カンマ）書く。
LEAKS（Singapore・GST・$・feet・miles・ringgit・Common Core など）が残ると止まるので、rep で直すか swap で問題関数を替える。US の内容が GCSE と違うとき（関数の四則、漸化式、parent function）は swap と body/faq で UK 版にする。make_gcse() は自前の単元用。seo_title は「Year 10 Maths: Surds Worksheets (GCSE)」
Year 10: 1. indices ✓ 2. standard-form ✓ 3. surds ✓ 4. algebraic-fractions ✓ 5. solving-quadratic-equations ✓ 6. quadratic-equations-in-context ✓ 7. equations-with-algebraic-fractions ✓ 8. inequalities ✓ 9. coordinate-geometry ✓
10. quadratic-graphs-and-turning-points ✓ 11. cubic-reciprocal-and-exponential-graphs ✓ 12. direct-and-inverse-proportion ✓ 13. congruent-and-similar-triangles ✓ 14. area-and-volume-of-similar-shapes ✓ 15. sine-and-cosine-rules ✓ 16. bearings-and-angles-of-elevation ✓ 17. probability-tree-diagrams ✓
Year 11: 1. sequences ✓ 2. composite-and-inverse-functions ✓ 3. transformations-of-graphs ✓ 4. exponential-growth-and-decay ✓ 5. equation-of-a-circle ✓ 6. circle-theorems ✓ 7. chords-and-tangents ✓ 8. vectors ✓ 9. vector-proof ✓ 10. trigonometry-in-3d ✓ 11. venn-diagrams-and-set-notation ✓ 12. cumulative-frequency-and-box-plots ✓
13. histograms ✓ 14. iteration ✓ 15. algebraic-proof ✓ 16. velocity-time-graphs ✓
（5・13〜16 と A level の proof・product-and-quotient-rules・hypothesis-testing-normal-and-correlation は `tools/uk_gap_units.py`（build(slug, year)）と自前の問題 `tools/uk_gap_own.py`。GCSE は seed 91100 + sort で make_gcse、A level は uk_alevel.unit。histogram は文脈ごとに階級幅（HCTX）、v–t グラフの区切りは目盛りの上、乗り物は速さで選ぶ（veh_for））
トピック：chords-and-tangents→circles、^venn-diagrams→probability、^histograms$→data-and-graphs、^iteration$・^proof$→algebra、velocity-time-graphs→mechanics

UK / Maths / Year 12–13（A level Mathematics。DfE の GCE AS and A level subject content。Year 12 は AS の内容、Year 13 は残り）— standard_code は「A level Mathematics: Pure mathematics」（Statistics・Mechanics）、domain は Pure Mathematics／Statistics／Mechanics、standard_url は GCE AS and A level mathematics、seo_title は「Year 12 A Level Maths: Quadratics Worksheets」。
単元の定義は `tools/uk_alevel_units.py`（units() が Year 12、units13() が Year 13。gen_uk_maths_y12_*・y13_* は build(slug, year) を呼ぶだけ。seed は 91000 + 100 × 学年 + sort）。
共通部品は `tools/uk_alevel.py`：mk(他国の生成スクリプト, 関数名, rep=, drop=, ln=True, keep=) で IN Class 11–12・US Algebra 2／Precalculus・SG Sec の問題関数を UK の名前とイギリス式の語（gradient・factorise・cosec・the second quadrant・square units・brackets、ln=True で log→ln）にして使う（IN の生成スクリプトは import すると JSON を書くので、mk は書き込みを止めて import する）。₹・synthetic division・Quadrant などが残る問題は落とす。unit() は単元全体で同じ問題を出さない。
自前の問題は `tools/uk_alevel_own.py`（二次不等式、一次と二次の連立、絶対値、部分分数、媒介変数、微分・接線・停留点、積分、反復法・Newton–Raphson・台形公式、抽出法、二項分布、仮説検定、suvat、v–t グラフ、F = ma、エレベーター、滑車、力の分解、摩擦と斜面、モーメント、放物運動、変化する加速度。g = 9.8）。正弦定理・余弦定理の逆三角関数は arcsin・arccos・arctan だけ（sec⁻¹ などは drop）
Year 12: 1. indices-and-surds ✓ 2. quadratics ✓ 3. equations-and-inequalities ✓ 4. polynomials-and-the-factor-theorem ✓ 5. graphs-and-transformations ✓ 6. straight-lines-and-circles ✓ 7. binomial-expansion ✓ 8. trigonometry ✓ 9. exponentials-and-logarithms ✓
10. differentiation ✓ 11. integration ✓ 12. vectors ✓ 13. statistical-sampling-and-data ✓ 14. probability ✓ 15. binomial-distribution-and-hypothesis-testing ✓ 16. kinematics ✓ 17. forces-and-newtons-laws ✓
Year 13: 1. functions-and-modulus ✓ 2. partial-fractions ✓ 3. sequences-and-series ✓ 4. radians-arcs-and-sectors ✓ 5. trigonometric-functions-and-formulae ✓ 6. differentiation-techniques ✓ 7. integration-techniques ✓ 8. parametric-and-differential-equations ✓
9. numerical-methods ✓ 10. vectors-in-3d ✓ 11. normal-distribution ✓ 12. conditional-probability ✓ 13. moments-and-friction ✓ 14. projectiles-and-variable-acceleration ✓ 15. product-and-quotient-rules ✓ 16. hypothesis-testing-normal-and-correlation ✓
Year 12 に 18. proof ✓（相関の検定の臨界値は問題文に書く。両側 5%・片側 5%・片側 1% の PMCC 表）
UK / Maths は Year 1〜13 まで完了
トピック（topics.php の uk）：calculus の名前を Calculus に（integration・numerical-methods・differential-equations）、binomial-distribution・normal-distribution→probability、partial-fractions→algebra、product-and-quotient-rules→calculus、hypothesis-testing→probability、新トピック mechanics（kinematics・newtons-laws・moments-and-friction・projectiles・velocity-time-graphs）

AU / Maths（Australian Curriculum v9.0）— country `au`、subject `maths`、grade `year-N`、A4。
オーストラリア英語（colour, metre, maths, analog, mixed numeral, column graph, students）。お金は $ と c（1c・2c 硬貨なし）。
数は 4 桁はそのまま（4536）、5 桁以上は空白区切り（10 000、ノーブレークスペース）。standard_code は v9 のコード（例: AC9M3N01）

AU / Maths / Year 3（NAPLAN の学年）
1. place-value-to-10000 ✓
2. adding-and-subtracting ✓
3. mental-strategies-and-number-sentences ✓
4. multiplication-facts-3-4-5-and-10 ✓
5. multiplying-and-dividing ✓
6. fractions ✓
7. money ✓
8. measuring-length-mass-and-capacity ✓
9. telling-the-time ✓
10. angles-as-turns ✓
11. 3d-objects ✓
12. maps-and-locations ✓
13. data-and-graphs ✓
14. chance ✓

AU / Maths / Year 5（NAPLAN の学年）
1. decimals ✓
2. factors-and-multiples ✓
3. comparing-fractions ✓
4. percentages ✓
5. adding-and-subtracting-fractions ✓
6. multiplication ✓
7. division ✓
8. estimation-and-money-problems ✓
9. number-sentences-multiplication-and-division ✓
10. metric-units ✓
11. perimeter-and-area ✓
12. 12-and-24-hour-time ✓
13. measuring-angles ✓
14. nets ✓
15. coordinates-and-transformations ✓
16. line-graphs-and-data ✓
17. chance ✓

AU / Maths / Year 4
1. multiplication-facts-to-10-x-10 ✓
2. decimals-tenths-and-hundredths ✓
3. equivalent-fractions ✓
4. multiplication-and-division-strategies ✓
5. adding-and-subtracting-large-numbers ✓
6. multiplying-and-dividing-by-10-and-100 ✓
7. counting-by-fractions-and-mixed-numerals ✓
8. rounding-and-estimation ✓
9. money-and-financial-problems ✓
10. odd-and-even-numbers ✓
11. number-sentences-addition-and-subtraction ✓
12. reading-scales-and-temperature ✓
13. perimeter-and-area ✓
14. time-am-pm-and-duration ✓
15. comparing-angles ✓
16. grid-references-and-maps ✓
17. symmetry ✓
18. shapes-and-composite-objects ✓
19. data-and-graphs ✓
20. chance ✓

AU / Maths / Year 6（高校準備の学年。NAPLAN はない）
1. integers-and-negative-numbers ✓
2. prime-composite-and-square-numbers ✓
3. comparing-and-ordering-fractions ✓
4. adding-and-subtracting-fractions ✓
5. adding-and-subtracting-decimals ✓
6. multiplying-and-dividing-decimals-by-powers-of-10 ✓
7. percentages-of-quantities ✓
8. estimation-and-financial-problems ✓
9. multiplying-and-dividing-larger-numbers ✓
10. number-patterns ✓
11. order-of-operations-and-equations ✓
12. converting-metric-units ✓
13. area-of-rectangles ✓
14. timetables-and-itineraries ✓
15. angles-on-a-line-and-at-a-point ✓
16. prisms-and-cross-sections ✓
17. cartesian-plane-four-quadrants ✓
18. transformations-and-tessellations ✓
19. interpreting-data ✓
20. probability ✓

AU / Maths / Year 2（文は短く、絵を多く。NAPLAN はない）
1. place-value-to-1000 ✓
2. addition-and-subtraction-facts-to-20 ✓
3. adding-and-subtracting-2-digit-numbers ✓
4. word-problems-and-number-sentences ✓
5. twos-doubling-and-halving ✓
6. multiplying-and-dividing-with-groups ✓
7. money ✓
8. halves-quarters-and-eighths ✓
9. number-patterns ✓
10. telling-the-time-to-the-quarter-hour ✓
11. calendars-and-dates ✓
12. measuring-length-mass-and-capacity ✓
13. turns ✓
14. 2d-shapes ✓
15. maps-and-directions ✓
16. data-tables-and-graphs ✓

AU / Maths / Year 1（とても短い文、ほぼ全問に絵）
1. numbers-to-120 ✓
2. tens-and-ones ✓
3. addition-and-subtraction-within-20 ✓
4. skip-counting-by-2s-5s-and-10s ✓
5. word-problems-and-money ✓
6. sharing-and-grouping ✓
7. repeating-patterns ✓
8. measuring-and-comparing ✓
9. days-weeks-months-and-time ✓
10. shapes-and-objects ✓
11. position-and-directions ✓
12. data-and-tally-marks ✓
13. chance ✓

AU / Maths / Foundation（最初の学年。州ごとに Kindergarten・Prep・Pre-primary・Reception・Transition と呼ぶ。5〜6歳）— grade `foundation`（name「Foundation」、sort 0）。生成スクリプトは `gen_au_maths_f_*`、共通部品は `tools/f_common.py`（k_pics・k_common の上にオーストラリア英語・AU の名前・sky_svg・days_svg・pictograph_svg・pattern_svg・glasses_svg・make）。とても短い文、ほぼ全問に絵。unit.php で educationalLevel に州ごとの呼び名を入れる
1. numbers-to-20 ✓ 2. subitising-to-5 ✓ 3. counting-and-comparing-collections ✓ 4. part-part-whole-to-10 ✓ 5. adding-and-taking-away ✓ 6. sharing-and-grouping ✓
7. repeating-patterns ✓ 8. comparing-length-mass-and-capacity ✓ 9. days-and-times-of-day ✓ 10. shapes ✓ 11. position-and-location ✓ 12. sorting-and-data ✓

AU / Maths / Year 7–8（高校。生成スクリプトは `gen_au_maths_y7_*`・`gen_au_maths_y8_*`、共通部品は `tools/au_hs.py`（ws_common の上に AU の数の書き方・$・make）。負の数は「−」。standard_code は v9 のコード（例: AC9M8N04）、standard_url は v9 の Mathematics ページ）

AU / Maths / Year 7
1. square-numbers-and-square-roots ✓ 2. prime-factorisation-and-index-notation ✓ 3. fractions-decimals-and-percentages ✓ 4. rounding-and-estimation ✓ 5. adding-and-subtracting-fractions ✓ 6. multiplying-and-dividing-fractions ✓
7. percentages-and-discounts ✓ 8. adding-and-subtracting-integers ✓ 9. ratios ✓ 10. formulas-and-substitution ✓ 11. algebraic-expressions ✓ 12. solving-linear-equations ✓
13. area-of-triangles-and-parallelograms ✓ 14. volume-of-prisms ✓ 15. circumference-and-pi ✓ 16. angles-and-parallel-lines ✓ 17. angle-sum-of-triangles-and-polygons ✓ 18. transformations-on-the-cartesian-plane ✓
19. mean-median-mode-and-range ✓ 20. stem-and-leaf-plots ✓ 21. probability ✓

AU / Maths / Year 8
1. irrational-numbers-and-recurring-decimals ✓ 2. index-laws ✓ 3. integers-and-rational-numbers ✓ 4. percentages-profit-and-loss ✓ 5. expanding-and-factorising ✓ 6. linear-equations ✓
7. linear-inequalities ✓ 8. graphing-linear-relations ✓ 9. area-and-perimeter-of-composite-shapes ✓ 10. volume-and-capacity ✓ 11. circumference-and-area-of-circles ✓ 12. time-zones-and-duration ✓
13. rates ✓ 14. pythagoras-theorem ✓ 15. congruent-and-similar-triangles ✓ 16. properties-of-quadrilaterals ✓ 17. sampling-and-data ✓ 18. probability-of-two-events ✓

CA-ON / Math（Ontario Curriculum 2020）— country `ca-on`（name「Ontario, Canada」）、subject `math`、grade `grade-N`、Letter。生成スクリプトは `gen_caon_math_*`。
カナダ英語（colour, metre, centre, math, grade, students, trapezoid, counterclockwise, bar graph）。お金は $ と ¢（nickel 5¢・dime・quarter・loonie・toonie、ペニーなし）。
数は 4 桁はそのまま、5 桁以上はノーブレークスペース区切り。standard_code は「Grade 3: B2.2」形式。EQAO は Grade 3・6

CA-ON / Math / Grade 3（EQAO の学年）
1. multiplication-facts-for-2-5-and-10 ✓
2. numbers-to-1000 ✓
3. adding-and-subtracting-to-1000 ✓
4. multiplication-and-division ✓
5. fractions-and-fair-shares ✓
6. rounding-and-estimating ✓
7. patterns ✓
8. equations-and-equivalence ✓
9. money-and-making-change ✓
10. telling-time ✓
11. length-and-perimeter ✓
12. mass-and-capacity ✓
13. area ✓
14. 2d-shapes-and-3d-objects ✓
15. location-and-movement ✓
16. data-and-graphs ✓
17. probability ✓

CA-ON / Math / Grade 6（EQAO の学年）
1. fractions-decimals-and-percents ✓
2. integers ✓
3. large-numbers-and-decimals ✓
4. adding-and-subtracting-fractions ✓
5. adding-and-subtracting-decimals ✓
6. multiplying-and-dividing-decimals ✓
7. multiplying-and-dividing-with-fractions ✓
8. factors-primes-and-divisibility ✓
9. ratios-rates-and-percents ✓
10. patterns-and-expressions ✓
11. equations-and-inequalities ✓
12. area-of-polygons ✓
13. measuring-angles ✓
14. cartesian-plane-and-transformations ✓
15. quadrilaterals-and-congruence ✓
16. metric-units-and-time ✓
17. data-and-graphs ✓
18. probability ✓
19. financial-literacy ✓

CA-ON / Math / Grade 4（EQAO なし）
1. multiplication-facts-to-10-x-10 ✓
2. numbers-to-10000 ✓
3. rounding-and-estimating ✓
4. adding-and-subtracting-to-10000 ✓
5. multiplying-by-one-digit-numbers ✓
6. dividing-by-one-digit-numbers ✓
7. fractions ✓
8. decimal-tenths ✓
9. patterns ✓
10. equations-and-inequalities ✓
11. data-and-graphs ✓
12. probability ✓
13. angles-and-rectangles ✓
14. coordinates-and-transformations ✓
15. mass-capacity-and-metric-units ✓
16. elapsed-time ✓
17. area-of-rectangles ✓
18. money-and-financial-literacy ✓

CA-ON / Math / Grade 5（EQAO なし。HST 13% は financial-literacy のみ）
1. multiplication-facts-to-12-x-12 ✓
2. numbers-to-100000 ✓
3. adding-and-subtracting-whole-numbers-and-decimals ✓
4. multiplying-two-digit-numbers ✓
5. dividing-by-two-digit-numbers ✓
6. equivalent-fractions-and-mixed-numbers ✓
7. decimals-to-hundredths ✓
8. fractions-decimals-and-percents ✓
9. multiplying-and-dividing-with-unit-fractions ✓
10. ratios-and-rates ✓
11. patterns ✓
12. expressions-equations-and-inequalities ✓
13. data-and-graphs ✓
14. probability ✓
15. triangles-and-congruence ✓
16. coordinates-and-transformations ✓
17. measuring-angles ✓
18. area-of-parallelograms-and-triangles ✓
19. metric-conversions ✓
20. financial-literacy ✓

CA-ON / Math / Grade 2（200 まで。文は短く、絵を多く）
1. numbers-to-200 ✓
2. counting-to-200 ✓
3. odd-and-even-numbers ✓
4. addition-and-subtraction-facts-to-20 ✓
5. adding-and-subtracting-to-100 ✓
6. equal-groups-and-sharing ✓
7. fractions-and-fair-shares ✓
8. patterns ✓
9. equality-and-missing-numbers ✓
10. data-and-graphs ✓
11. probability ✓
12. 2d-shapes-and-symmetry ✓
13. maps-and-directions ✓
14. measuring-length ✓
15. time ✓
16. money ✓

CA-ON / Math / Grade 1（50 まで。とても短い文、ほぼ全問に絵）
1. numbers-to-50 ✓
2. counting-and-estimating-to-50 ✓
3. addition-and-subtraction-facts-to-10 ✓
4. adding-and-subtracting-to-20 ✓
5. word-problems-to-50 ✓
6. equal-groups-and-fair-shares ✓
7. patterns ✓
8. equal-and-not-equal ✓
9. sorting-and-graphs ✓
10. probability ✓
11. 2d-shapes-and-3d-objects ✓
12. position-and-directions ✓
13. comparing-length-mass-and-capacity ✓
14. calendar-days-weeks-and-months ✓
15. money ✓

CA-ON / Math / Grade 7（EQAO なし。10億まで、負の数は −）
1. powers-and-large-numbers ✓
2. perfect-squares-and-square-roots ✓
3. comparing-fractions-and-decimals ✓
4. fractions-decimals-and-percents ✓
5. adding-and-subtracting-integers ✓
6. adding-and-subtracting-fractions ✓
7. gcf-and-lcm ✓
8. multiplying-and-dividing-fractions ✓
9. multiplying-and-dividing-decimals ✓
10. proportional-reasoning ✓
11. order-of-operations ✓
12. linear-growing-patterns ✓
13. algebraic-expressions ✓
14. equations-and-inequalities ✓
15. circle-graphs-and-data ✓
16. probability-of-independent-and-dependent-events ✓
17. transformations-and-dilations ✓
18. circles ✓
19. surface-area-and-volume ✓
20. exchange-rates-and-interest ✓

CA-ON / Math / Grade 8（EQAO なし。次は Grade 9）
1. scientific-notation ✓
2. square-roots-and-real-numbers ✓
3. percents ✓
4. adding-and-subtracting-integers ✓
5. multiplying-and-dividing-integers ✓
6. operations-with-fractions ✓
7. order-of-operations-with-rational-numbers ✓
8. proportional-relationships ✓
9. linear-relations ✓
10. expressions-and-binomials ✓
11. equations-and-inequalities ✓
12. scatter-plots-and-data ✓
13. probability-venn-and-tree-diagrams ✓
14. tessellations-and-transformations ✓
15. scale-drawings ✓
16. angle-properties ✓
17. pythagorean-theorem ✓
18. composite-area-and-volume ✓
19. interest-and-credit ✓

CA-BC / Math（BC Mathematics Curriculum K–9）— country `ca-bc`（name「British Columbia, Canada」）、subject `math`、grade `grade-N`、Letter。生成スクリプトは `gen_cabc_math_*`。
Ontario と同じカナダ英語・お金・数の書き方。税は GST 5% + PST 7%（HST・13% は使わない）。評価は FSA（Grade 4・7）。
standard_code は「Grade 4: Number」形式、standard_text は BC の Content 原文、standard_url は https://curriculum.gov.bc.ca/curriculum/mathematics/N/core

CA-BC / Math / Grade 4（FSA の学年）
1. multiplication-and-division-facts-to-100 ✓
2. numbers-to-10000 ✓
3. adding-and-subtracting-to-10000 ✓
4. multiplying-and-dividing-by-one-digit-numbers ✓
5. comparing-and-ordering-fractions ✓
6. decimals-to-hundredths ✓
7. adding-and-subtracting-decimals ✓
8. one-step-equations ✓
9. increasing-and-decreasing-patterns ✓
10. 12-and-24-hour-time ✓
11. regular-and-irregular-polygons ✓
12. perimeter ✓
13. line-symmetry ✓
14. bar-graphs-and-pictographs ✓
15. probability-experiments ✓
16. money-and-making-change ✓

CA-BC / Math / Grade 7（FSA の学年）
1. adding-and-subtracting-integers ✓
2. multiplying-and-dividing-integers ✓
3. order-of-operations ✓
4. adding-and-subtracting-decimals ✓
5. multiplying-and-dividing-decimals ✓
6. fractions-decimals-and-percents ✓
7. ratios ✓
8. two-step-equations ✓
9. linear-relations ✓
10. circumference-and-area-of-circles ✓
11. volume-of-prisms-and-cylinders ✓
12. cartesian-coordinates-and-graphing ✓
13. combinations-of-transformations ✓
14. circle-graphs ✓
15. probability-of-two-independent-events ✓
16. financial-percentages ✓

CA-BC / Math / Kindergarten（5〜6歳）— grade `kindergarten`（name「Kindergarten」、sort 0）。10 まで。とても短い文、ほぼ全問に絵。生成スクリプトは `gen_cabc_math_k_*`、共通部品は `tools/bck_common.py`（k_pics・k_common の上にカナダ英語・BC の名前・mcq（10 を超える誤答を落とす）・collect・letters・finish・make）。AU Foundation と BC Grade 1 の問題関数・絵を再利用。standard_code は「Kindergarten: Number」形式
1. numbers-to-10 ✓ 2. ways-to-make-5 ✓ 3. comparing-quantities-to-10 ✓ 4. decomposing-numbers-to-10 ✓ 5. change-in-quantity-to-10 ✓ 6. repeating-patterns ✓
7. equal-and-not-equal ✓ 8. comparing-length-mass-and-capacity ✓ 9. 2d-shapes-and-3d-objects ✓ 10. concrete-graphs ✓ 11. likelihood ✓ 12. canadian-coins ✓

CA-BC / Math / Grade 1（文はとても短く、絵を多く）
1. numbers-to-20 ✓
2. ways-to-make-10 ✓
3. addition-and-subtraction-to-20 ✓
4. change-in-quantity ✓
5. equal-and-not-equal ✓
6. repeating-patterns ✓
7. measuring-with-non-standard-units ✓
8. 2d-shapes-and-3d-objects ✓
9. concrete-graphs ✓
10. likelihood ✓
11. coins-and-money ✓

CA-BC / Math / Grade 2（文は短く、絵を多く）
1. numbers-to-100 ✓
2. benchmarks-25-50-and-100 ✓
3. addition-and-subtraction-facts-to-20 ✓
4. adding-and-subtracting-to-100 ✓
5. change-in-quantity ✓
6. equality-and-inequality ✓
7. repeating-and-increasing-patterns ✓
8. measuring-length ✓
9. 2d-shapes-and-3d-objects ✓
10. pictographs ✓
11. likelihood ✓
12. coins-to-100-cents ✓

CA-BC / Math / Grade 3
1. numbers-to-1000 ✓
2. fractions ✓
3. adding-and-subtracting-to-1000 ✓
4. multiplication-and-division ✓
5. one-step-equations ✓
6. increasing-and-decreasing-patterns ✓
7. measuring-length-mass-and-capacity ✓
8. time ✓
9. 3d-objects ✓
10. bar-graphs-and-pictographs ✓
11. likelihood-of-simulated-events ✓
12. money-to-100-dollars ✓

CA-BC / Math / Grade 5
1. numbers-to-1000000 ✓
2. decimals-to-thousandths ✓
3. equivalent-fractions ✓
4. benchmarks-and-estimation ✓
5. adding-and-subtracting-whole-numbers ✓
6. multiplication-to-three-digits ✓
7. division-with-remainders ✓
8. adding-and-subtracting-decimals ✓
9. one-step-equations-with-variables ✓
10. pattern-rules ✓
11. area-and-perimeter ✓
12. duration-of-time ✓
13. prisms-and-pyramids ✓
14. single-transformations ✓
15. double-bar-graphs ✓
16. probability-experiments ✓
17. money-and-financial-plans ✓

CA-BC / Math / Grade 6
1. thousandths-to-billions ✓
2. gcf-and-lcm ✓
3. improper-fractions-and-mixed-numbers ✓
4. ratios ✓
5. percents-and-discounts ✓
6. order-of-operations ✓
7. multiplying-and-dividing-decimals ✓
8. one-step-equations ✓
9. patterns-tables-and-graphs ✓
10. perimeter-of-complex-shapes ✓
11. area-of-triangles-parallelograms-and-trapezoids ✓
12. angles ✓
13. volume-and-capacity ✓
14. triangles ✓
15. combinations-of-transformations ✓
16. line-graphs ✓
17. probability ✓
18. budgeting-and-consumer-math ✓

CA-BC / Math / Grade 8
1. squares-cubes-and-roots ✓
2. percents-less-than-1-and-greater-than-100 ✓
3. proportional-reasoning ✓
4. adding-and-subtracting-fractions ✓
5. multiplying-and-dividing-fractions ✓
6. expressions-and-substitution ✓
7. two-step-equations ✓
8. linear-relations ✓
9. surface-area-and-volume ✓
10. pythagorean-theorem ✓
11. views-and-nets ✓
12. central-tendency ✓
13. probability-of-two-independent-events ✓
14. best-buys ✓

CA-BC / Math / Grade 9（Mathematics 9）
1. exponent-laws ✓
2. operations-with-rational-numbers ✓
3. adding-and-subtracting-polynomials ✓
4. multiplying-and-dividing-polynomials ✓
5. linear-equations ✓
6. linear-relations-and-graphs ✓
7. similar-shapes-and-scale-diagrams ✓
8. statistics-in-society ✓
9. budgets-and-transactions ✓

SG / Maths（MOE 2021 Primary Mathematics Syllabus, Standard）— country `sg`（name「Singapore」）、subject `maths`、grade `primary-N`（表示は「Primary N」/「PN」）、A4。生成スクリプトは `gen_sg_maths_pN_*`。
イギリス英語（colour, metre, maths, cuboid, trapezium, renaming, picture graph, multiplication tables）。単位は ℓ と ml、時刻は「7.30 am」（ドット・ピリオドなし）、24時間制は「1930」。お金は $ と ¢（5¢・10¢・20¢・50¢・$1 硬貨、1¢ は使わない）。GST 9% は P5 のみ。
数は 4 桁はそのまま、5 桁以上はノーブレークスペース区切り（MOE シラバスと同じ）。文章題は bar model（units）を使う。standard_code は「Primary 4: Fractions」形式、standard_url は https://www.moe.gov.sg/primary/curriculum/syllabus

SG / Maths / Primary 6（PSLE の学年。PSLE はここだけタイトルに入れる）
1. dividing-fractions ✓
2. fraction-word-problems ✓
3. percentage ✓
4. ratio ✓
5. ratio-word-problems ✓
6. algebra ✓
7. area-and-circumference-of-circles ✓
8. volume-of-cubes-and-cuboids ✓
9. angles-in-composite-figures ✓
10. average ✓

SG / Maths / Primary 5
1. numbers-to-10-million ✓
2. multiplying-and-dividing-by-10-100-1000 ✓
3. order-of-operations ✓
4. fractions-and-division ✓
5. adding-and-subtracting-mixed-numbers ✓
6. multiplying-fractions ✓
7. decimals-and-measurement ✓
8. percentage ✓
9. discount-gst-and-interest ✓
10. rate ✓
11. area-of-triangles ✓
12. volume-of-cubes-and-cuboids ✓
13. angles ✓
14. triangles ✓
15. parallelograms-rhombuses-and-trapeziums ✓

SG / Maths / Primary 4
1. numbers-to-100000 ✓
2. rounding-and-estimation ✓
3. factors-and-multiples ✓
4. multiplication ✓
5. division ✓
6. mixed-numbers-and-improper-fractions ✓
7. fraction-of-a-set ✓
8. adding-and-subtracting-fractions ✓
9. decimals ✓
10. adding-and-subtracting-decimals ✓
11. multiplying-and-dividing-decimals ✓
12. area-and-perimeter ✓
13. angles ✓
14. rectangles-and-squares ✓
15. line-symmetry ✓
16. nets ✓
17. tables-line-graphs-and-pie-charts ✓

SG / Maths / Primary 3
1. numbers-to-10000 ✓
2. addition-and-subtraction ✓
3. multiplication-tables-6-7-8-and-9 ✓
4. multiplication-and-division ✓
5. equivalent-fractions ✓
6. adding-and-subtracting-fractions ✓
7. money ✓
8. length-mass-and-volume ✓
9. time ✓
10. area-and-perimeter ✓
11. angles ✓
12. perpendicular-and-parallel-lines ✓
13. bar-graphs ✓

SG / Maths / Primary 2（文は短く、絵を多く）
1. numbers-to-1000 ✓
2. odd-and-even-numbers ✓
3. addition-and-subtraction ✓
4. multiplication-tables-2-3-4-5-and-10 ✓
5. multiplication-and-division ✓
6. fractions ✓
7. adding-and-subtracting-fractions ✓
8. money ✓
9. length-mass-and-volume ✓
10. time ✓
11. 2d-shapes-and-patterns ✓
12. 3d-shapes ✓
13. picture-graphs ✓

SG / Maths / Primary 1（とても短い文、ほぼ全問に絵）
1. numbers-to-100 ✓
2. ordinal-numbers ✓
3. number-bonds ✓
4. addition-and-subtraction-within-20 ✓
5. addition-and-subtraction-within-100 ✓
6. multiplication-and-division ✓
7. money ✓
8. length ✓
9. time ✓
10. 2d-shapes ✓
11. picture-graphs ✓

SG / Maths / Secondary 1–4（MOE 2020 O-Level / G3 Mathematics。旧 Express）— grade `secondary-N`（表示は「Secondary N」、sort 7〜10、12〜16歳。Sec 4 が O-Level の学年）。生成スクリプトは `gen_sg_maths_sN_*`、共通部品は `tools/sg_sec.py`（uk_ks3 と同じ API。SG の名前・$・数の書き方、STD_TEXT（シラバス原文）、TITLES、seo_title は make が自動。`adopt(mod, R)` で他国の生成スクリプトの問題関数を SG の名前・$・数の書き方のまま再利用できる）。Sec 3–4 は答えを 3 有効数字・角度は小数第 1 位（O-Level と同じ）。
多くは UK KS3 の生成スクリプトを SG 式に移したもの（£→$、miles→km、VAT→GST 9%、stem-and-leaf diagram）。負の数は「−」。standard_code は「Secondary 1: Ratio and Proportion」形式（N1〜N7・G1〜G5・S1〜S2 の小項目名）、standard_url は MOE 2020 Express/N(A) シラバス PDF

SG / Maths / Secondary 1
1. primes-hcf-and-lcm ✓ 2. integers-and-the-number-line ✓ 3. approximation-and-estimation ✓ 4. ratio ✓ 5. percentage ✓ 6. rate-and-speed ✓
7. algebraic-expressions-and-substitution ✓ 8. simplifying-linear-expressions ✓ 9. number-patterns ✓ 10. linear-equations ✓ 11. linear-graphs-and-gradient ✓
12. angles-triangles-and-quadrilaterals ✓ 13. parallel-lines-and-polygons ✓ 14. perimeter-and-area ✓ 15. volume-and-surface-area-of-prisms-and-cylinders ✓

SG / Maths / Secondary 2
1. expansion-and-factorisation ✓ 2. algebraic-fractions ✓ 3. changing-the-subject-of-a-formula ✓ 4. linear-inequalities ✓ 5. simultaneous-equations ✓
6. quadratic-equations ✓ 7. quadratic-graphs ✓ 8. direct-and-inverse-proportion ✓ 9. map-scales ✓ 10. congruence-and-similarity ✓ 11. pythagoras-theorem ✓
12. trigonometric-ratios ✓ 13. volume-of-cones-and-spheres ✓ 14. mean-median-and-mode ✓ 15. stem-and-leaf-diagrams ✓ 16. frequency-tables-and-grouped-data ✓ 17. probability ✓

SG / Maths / Secondary 3
1. indices ✓ 2. standard-form ✓ 3. quadratic-formula-and-completing-the-square ✓ 4. fractional-equations ✓ 5. quadratic-equation-word-problems ✓
6. simultaneous-linear-inequalities ✓ 7. sketching-quadratic-graphs ✓ 8. power-and-exponential-graphs ✓ 9. coordinate-geometry ✓ 10. congruent-and-similar-triangles ✓
11. area-and-volume-of-similar-figures ✓ 12. sine-and-cosine-rules ✓ 13. bearings-and-angles-of-elevation ✓ 14. arc-length-sector-area-and-radians ✓
15. symmetry-properties-of-circles ✓ 16. angle-properties-of-circles ✓

SG / Maths / Secondary 4（O-Level の学年）
1. sets-and-venn-diagrams ✓ 2. matrices ✓ 3. vectors ✓ 4. vector-geometry ✓ 5. problems-in-three-dimensions ✓
6. cumulative-frequency-and-box-plots ✓ 7. standard-deviation ✓ 8. probability-of-combined-events ✓

US / Math / Grade 7（Common Core）— 1,000 以上はカンマ付き。負の数は「−」（U+2212）。共通部品は `tools/ws_common.py`
1. adding-and-subtracting-integers ✓
2. multiplying-and-dividing-integers ✓
3. two-step-equations ✓
4. proportional-relationships ✓
5. percent-problems ✓
6. simplifying-expressions ✓
7. circles-area-and-circumference ✓
8. angle-relationships ✓
9. probability ✓
10. two-step-inequalities ✓
11. unit-rates-with-fractions ✓
12. rational-number-word-problems ✓
13. converting-fractions-to-decimals ✓
14. scale-drawings ✓
15. area-surface-area-volume ✓
16. compound-probability ✓
17. random-sampling ✓
18. comparing-data-distributions ✓
19. constructing-triangles-and-cross-sections ✓

US / Math / Grade 8（Common Core）— 1,000 以上はカンマ付き。負の数は「−」。生成スクリプトは `gen_us_math_g8_*`（共通部品は `tools/ws_common.py`）
1. linear-equations ✓
2. systems-of-equations ✓
3. slope ✓
4. functions ✓
5. linear-functions ✓
6. exponent-rules ✓
7. scientific-notation ✓
8. square-and-cube-roots ✓
9. rational-and-irrational-numbers ✓
10. pythagorean-theorem ✓
11. transformations ✓
12. congruence-and-similarity ✓
13. angle-relationships-parallel-lines ✓
14. volume-of-cylinders-cones-spheres ✓
15. scatter-plots ✓
16. two-way-tables ✓
17. distance-on-coordinate-plane ✓

US / Math / Kindergarten（Common Core）— grade `kindergarten`（name「Kindergarten」、sort 0、5〜6歳）。生成スクリプトは `gen_us_math_gk_*`、絵の部品は `tools/k_pics.py`。
20 まで（数えるのは 100 まで）。文はとても短く、5〜6歳が読める英語で。ほぼ全問に絵。standard_code は「K.CC.B.5」形式
1. counting-to-20 ✓
2. counting-to-100 ✓
3. writing-numbers-0-to-20 ✓
4. comparing-numbers ✓
5. addition-within-10 ✓
6. subtraction-within-10 ✓
7. make-10 ✓
8. decompose-numbers-to-10 ✓
9. add-and-subtract-within-5 ✓
10. teen-numbers-tens-and-ones ✓
11. compare-length-and-weight ✓
12. sort-and-count ✓
13. 2d-and-3d-shapes ✓
14. positions ✓
15. build-and-compose-shapes ✓

US / Math / Algebra 1（Common Core 高校）— grade `algebra-1`（name「Algebra 1」、sort 9、14〜15歳）。1,000 以上はカンマ付き。負の数は「−」。生成スクリプトは `gen_us_math_a1_*`、共通部品は `tools/us_hs.py`（au_hs と同じ API。make は CCSS の高校コード「A-REI.B.3」から standard_url を作る。domain は引数で指定）。トピック `quadratics` あり
1. multi-step-equations ✓ 2. literal-equations ✓ 3. multi-step-and-compound-inequalities ✓ 4. absolute-value-equations-and-inequalities ✓ 5. function-notation ✓
6. domain-and-range ✓ 7. forms-of-linear-equations ✓ 8. systems-of-linear-equations ✓ 9. systems-of-linear-inequalities ✓ 10. rational-exponents ✓
11. simplifying-radicals ✓ 12. exponential-growth-and-decay ✓ 13. arithmetic-and-geometric-sequences ✓ 14. polynomial-operations ✓ 15. factoring-polynomials ✓
16. solving-quadratics-by-factoring ✓ 17. quadratic-formula-and-completing-the-square ✓ 18. graphing-quadratic-functions ✓ 19. box-plots-and-standard-deviation ✓ 20. correlation-and-residuals ✓

US / Math / Geometry（Common Core 高校）— grade `geometry`（name「Geometry」、sort 10、15〜16歳）。生成スクリプトは `gen_us_math_ge_*`、共通部品は `tools/us_hs.py`（make に grade="geometry"）と図の部品 `tools/us_geo.py`（Canvas: poly・angle・right・ticks・chevrons・side_label など）。domain は引数で指定。トピック `circles`・`congruence-and-similarity` あり
1. points-lines-and-planes ✓ 2. segment-addition-and-midpoints ✓ 3. distance-and-midpoint-formulas ✓ 4. angle-pairs ✓ 5. conditional-statements-and-proof ✓
6. parallel-lines-and-transversals ✓ 7. slopes-of-parallel-and-perpendicular-lines ✓ 8. rigid-transformations ✓ 9. triangle-angle-theorems ✓ 10. congruent-triangles ✓
11. midsegments-and-triangle-centers ✓ 12. polygons-and-quadrilaterals ✓ 13. dilations-and-similarity ✓ 14. similar-triangles ✓ 15. pythagorean-theorem-and-special-right-triangles ✓
16. right-triangle-trigonometry ✓ 17. law-of-sines-and-cosines ✓ 18. circle-angles-and-arcs ✓ 19. arc-length-and-sector-area ✓ 20. equations-of-circles ✓
21. volume-of-solids ✓ 22. cross-sections-and-solids-of-revolution ✓ 23. conditional-probability ✓

US / Math / Algebra 2（Common Core 高校）— grade `algebra-2`（name「Algebra 2」、sort 11、16〜17歳）。生成スクリプトは `gen_us_math_a2_*`、共通部品は `tools/us_hs.py`（make に grade="algebra-2"）と多項式の部品 `tools/a2_common.py`（poly・pmul・peval・synth・sf・ps・lin）。domain は引数で指定。トピック `trigonometry` あり
1. complex-numbers ✓ 2. polynomial-division-and-remainder-theorem ✓ 3. polynomial-functions-and-zeros ✓ 4. polynomial-identities-and-factoring ✓ 5. rational-expressions ✓
6. rational-and-radical-equations ✓ 7. composition-and-inverse-functions ✓ 8. transformations-of-functions ✓ 9. exponential-functions-and-e ✓ 10. logarithms-and-their-properties ✓
11. exponential-and-logarithmic-equations ✓ 12. sequences-and-series ✓ 13. unit-circle-and-radians ✓ 14. graphs-of-sine-and-cosine ✓ 15. normal-distribution ✓
16. statistical-studies-and-margin-of-error ✓

US / Math / Precalculus（Common Core 高校の (+) 基準）— grade `precalculus`（name「Precalculus」、sort 12、17〜18歳）。生成スクリプトは `gen_us_math_pc_*`、共通部品は `tools/us_hs.py`（make に grade）と `tools/pc_common.py`（pis・trig・vhtml・surd・mat・det_h・vec・curve_svg など）。行列は `<span class='mx m2'>`（ws.css・ws-print.css）。トピック `vectors-and-matrices` あり
1. rational-functions-and-asymptotes ✓ 2. six-trigonometric-functions ✓ 3. inverse-trigonometric-functions ✓ 4. trigonometric-identities ✓ 5. sum-and-difference-formulas ✓
6. solving-trigonometric-equations ✓ 7. complex-numbers-in-polar-form ✓ 8. vectors ✓ 9. vector-operations ✓ 10. matrix-operations ✓
11. determinants-and-inverse-matrices ✓ 12. binomial-theorem ✓ 13. conic-sections ✓ 14. permutations-and-combinations ✓ 15. expected-value ✓
16. polar-coordinates ✓

TW / Math（十二年國教課綱・108課綱）— country `tw`（name「台灣」、lang `zh-TW`）、subject `math`（數學）、grade `grade-N`（國小N年級）、A4。生成スクリプトは `gen_tw_math_gN_*`、共通部品は `tools/tw_common.py`（num・mcq・lesson・make_unit・clock など）。
繁體中文・台灣用語（公分、毫米、公升、毫升、公斤、公克、元、直式、餘數、驗算）。時刻は「上午 9 時 40 分」、時間量は「1 小時 45 分鐘」。4 桁まではそのまま、10,000 以上はカンマ。餘數は「29 ÷ 4 ＝ 7……1」。
standard_code は課綱の學習內容コード（例: N-3-1）、standard_text は課綱の原文。domain は 數與量／空間與形狀／關係／資料與不確定性。body_html は「怎麼想 → 例題 → 常見錯誤」。
UI 文言は core.php の 'zh-TW'。プレビュー画像は Noto Sans TC のサブセットを使うので、**tw の単元を足したら `python3 tools/build_cjk_font.py` を実行してフォントもコミット**する（使う文字だけを入れる）。

TW / Math / Grade 3（國小三年級）
1. numbers-to-10000 ✓ 2. add-subtract-within-10000 ✓ 3. multiply-by-one-digit ✓ 4. division ✓ 5. divide-by-one-digit ✓
6. two-step-word-problems ✓ 7. estimation ✓ 8. fractions ✓ 9. decimals ✓ 10. number-line ✓ 11. millimeters ✓
12. angles ✓ 13. area-square-centimeters ✓ 14. liters-and-milliliters ✓ 15. kilograms-and-grams ✓ 16. time ✓
17. squares-and-rectangles ✓ 18. circles ✓ 19. nets ✓ 20. tables ✓ 21. multiplication-division-relationship ✓ 22. patterns ✓

TW / Math / Grade 4（國小四年級）
1. numbers-to-100-million ✓ 2. multi-digit-multiplication ✓ 3. multi-digit-division ✓ 4. two-step-word-problems ✓ 5. rounding ✓
6. fractions ✓ 7. equivalent-fractions ✓ 8. decimals ✓ 9. number-line ✓ 10. kilometers ✓ 11. angles ✓ 12. rotation ✓
13. area-and-perimeter ✓ 14. volume ✓ 15. time ✓ 16. perpendicular-and-parallel ✓ 17. congruent-figures ✓ 18. triangles ✓
19. quadrilaterals ✓ 20. order-of-operations ✓ 21. calculation-rules ✓ 22. formulas ✓ 23. patterns-odd-and-even ✓ 24. bar-and-line-graphs ✓

TW / Math / Grade 5（國小五年級）
1. place-value ✓ 2. multi-step-word-problems ✓ 3. factors-and-multiples ✓ 4. simplifying-fractions ✓ 5. adding-and-subtracting-fractions ✓
6. multiplying-fractions ✓ 7. fractions-as-division ✓ 8. dividing-fractions ✓ 9. multiplying-decimals ✓ 10. dividing-decimals ✓ 11. percentages ✓
12. rounding-decimals ✓ 13. area-units ✓ 14. metric-tons ✓ 15. volume-and-capacity ✓ 16. time-calculations ✓
17. triangle-and-quadrilateral-properties ✓ 18. area-of-triangles-and-quadrilaterals ✓ 19. sectors ✓ 20. line-symmetry ✓
21. volume-and-surface-area ✓ 22. faces-parallel-and-perpendicular ✓ 23. solids ✓ 24. three-step-problems-and-averages ✓
25. distributive-property ✓ 26. formulas-with-symbols ✓ 27. making-line-graphs ✓

TW / Math / Grade 6（國小六年級）— 圓周率は 3.14
1. prime-factorization ✓ 2. gcf-and-lcm ✓ 3. dividing-fractions ✓ 4. dividing-decimals ✓ 5. word-problems ✓ 6. ratios ✓
7. speed ✓ 8. base-and-compared-quantities ✓ 9. enlargement-and-reduction ✓ 10. map-scales ✓ 11. circumference ✓
12. area-of-circles ✓ 13. volume-of-prisms-and-cylinders ✓ 14. calculation-rules ✓ 15. quantity-relationships ✓
16. classic-word-problems ✓ 17. counting ✓ 18. pie-charts ✓ 19. likelihood ✓

TW / Math / Grade 7（國中七年級）— 負數は「－」（全角）、負數は（－5）とかっこ、式の部品は `tools/tw_g7.py`（sn・par・opv・lin・tidy_sets）
1. positive-and-negative-numbers ✓ 2. number-line-and-absolute-value ✓ 3. adding-and-subtracting-integers ✓
4. multiplying-and-dividing-integers ✓ 5. mixed-operations ✓ 6. laws-of-operations ✓ 7. exponents ✓ 8. scientific-notation ✓
9. primes ✓ 10. standard-factorization ✓ 11. algebraic-expressions ✓ 12. solving-linear-equations ✓ 13. equation-word-problems ✓
14. exponent-laws ✓ 15. systems-of-equations ✓ 16. solving-systems ✓ 17. coordinate-plane ✓ 18. graphs-of-linear-equations ✓
19. ratio-and-proportion ✓ 20. direct-and-inverse-proportion ✓ 21. linear-inequalities ✓ 22. geometry-symbols-and-perpendicular ✓
23. three-views ✓ 24. line-symmetry ✓ 25. statistical-charts ✓ 26. mean-median-mode ✓

TW / Math / Grade 8（國中八年級）— 根式は `tools/tw_g8.py`（poly・pmul・rt・simp・qroots）、線分は `<span class='ov'>AB</span>`
1. multiplication-formulas ✓ 2. polynomials ✓ 3. polynomial-multiplication-and-division ✓ 4. square-roots ✓ 5. operations-with-radicals ✓
6. approximating-square-roots ✓ 7. pythagorean-theorem ✓ 8. distance-formula ✓ 9. factoring ✓ 10. cross-method ✓ 11. quadratic-equations ✓
12. quadratic-formula ✓ 13. cumulative-relative-frequency ✓ 14. arithmetic-sequences ✓ 15. arithmetic-series ✓ 16. geometric-sequences ✓
17. linear-functions ✓ 18. parallel-lines ✓ 19. polygon-angle-sums ✓ 20. congruent-triangles ✓ 21. triangle-properties ✓
22. equilateral-triangle-area ✓ 23. parallelograms ✓ 24. special-quadrilaterals ✓

TW / Math / Grade 9（國中九年級）— 図の部品は `tools/tw_g9.py`（poly_svg・pi・vform・parab）。四分位數は前半・後半の中位數（資料の個數は 4 で割って 1 余る數を避ける）
1. continued-ratios ✓ 2. similar-figures ✓ 3. similar-triangles ✓ 4. proportional-segments ✓ 5. special-right-triangles ✓
6. arc-length-and-sector-area ✓ 7. points-lines-and-circles ✓ 8. inscribed-angles ✓ 9. circumcenter ✓ 10. incenter ✓ 11. centroid ✓
12. quadratic-functions ✓ 13. graphs-of-quadratic-functions ✓ 14. maximum-and-minimum ✓ 15. box-plots ✓ 16. probability ✓
17. lines-and-planes-in-space ✓ 18. surface-area-and-volume ✓ 19. geometric-proofs ✓

TW / Math / Grade 1（國小一年級）— 絵は `tools/tw_pics.py`（k_pics の絵に中國語の aria-label、台灣の硬幣・紙鈔 money_svg）。とても短い文、ほぼ全問に絵
1. numbers-to-100 ✓ 2. addition-meaning ✓ 3. subtraction-meaning ✓ 4. addition-facts-to-18 ✓ 5. subtraction-facts-to-18 ✓
6. add-subtract-within-100 ✓ 7. number-sentences ✓ 8. money ✓ 9. comparing-length ✓ 10. dates-and-time ✓ 11. shapes ✓
12. sorting-and-counting ✓

TW / Math / Grade 2（國小二年級）— 直式・積木・尺・分數の絵は `tools/tw_pics.py`（col・blocks・ruler・frac・array）。短い文、絵を多く
1. numbers-to-1000 ✓ 2. column-addition ✓ 3. column-subtraction ✓ 4. addition-subtraction-word-problems ✓ 5. estimation ✓ 6. money ✓
7. meaning-of-multiplication ✓ 8. multiplication-tables ✓ 9. sharing-and-grouping ✓ 10. two-step-problems ✓ 11. unit-fractions ✓
12. centimeters-and-meters ✓ 13. capacity-weight-and-area ✓ 14. telling-time ✓ 15. years-months-and-days ✓ 16. shapes ✓
17. comparing-and-number-properties ✓ 18. sorting-and-tables ✓

TW / Math は國小一年級〜國中九年級まで完了。次は下の「その後」から
tw のトピック別ページは `topic_defs_tw()`（topics.php、中国語の name・blurb、tw の slug 用の正規表現）。tw の単元を足したらどのトピックに入るか確認する
グラフ・物差しなど印刷で大きく出したい図は `<svg data-pf='lg' ...>` にする

US-TX / Math（Texas Essential Knowledge and Skills, TEKS §111.5 など）— country `us-tx`（name「Texas, USA」、lang en）、subject `math`、grade `grade-N`、Letter。生成スクリプトは `gen_ustx_math_gN_*`、共通部品は `tools/tx_common.py`（Texas の名前・地名、US の綴りと文法の自動修正 us_text、1,000 以上のカンマ自動付与、他国の生成スクリプトの問題関数を使う adopt・run・run_many、Kid・mcq・collect・letters・finish（他国の語の混入を LEAKS で検出）・make、strip_svg（strip diagram）・pv_chart_svg・words）。
US 英語・お金は $ と ¢（ペニーあり、$1・$5・$10・$20 札）。standard_code は TEKS のコード（例: 3.4F、複数は「3.3F, 3.3G」）、standard_text は TEKS 原文、standard_url は TEA の Chapter 111 Subchapter A。STAAR は Grade 3 から。重さは weight（mass と言わない）。多くの単元は US Common Core・Ontario・Australia の問題関数を Texas 向けに再利用（別の seed で別の問題になる）

US-TX / Math / Grade 3（STAAR の最初の学年）
1. place-value-to-100000 ✓ 2. comparing-and-ordering-numbers ✓ 3. rounding-and-estimating ✓ 4. adding-and-subtracting-within-1000 ✓ 5. multiplication-facts ✓
6. division-facts ✓ 7. multiplying-two-digit-by-one-digit ✓ 8. multiplication-and-division-word-problems ✓ 9. missing-factors-and-input-output-tables ✓ 10. odd-and-even-numbers ✓
11. fractions ✓ 12. fractions-on-a-number-line ✓ 13. equivalent-and-comparing-fractions ✓ 14. value-of-coins-and-bills ✓ 15. area ✓ 16. perimeter ✓
17. time-intervals ✓ 18. liquid-volume-and-weight ✓ 19. 2d-and-3d-figures ✓ 20. frequency-tables-dot-plots-and-bar-graphs ✓ 21. personal-financial-literacy ✓

US-TX / Math / Grade 4（STAAR の学年。1,000 以上はカンマ、10億まで）— 生成スクリプトは `gen_ustx_math_g4_*`（多くは US Grade 4 の問題関数を build_sets で再利用。他国の問題関数に People を渡すときはその生成スクリプトの People を使う）
1. place-value-to-billions ✓ 2. comparing-and-rounding-whole-numbers ✓ 3. decimals-tenths-and-hundredths ✓ 4. comparing-decimals-and-number-lines ✓ 5. adding-and-subtracting-whole-numbers-and-decimals ✓ 6. multiplying-by-10-and-100 ✓
7. multiplying-two-digit-numbers ✓ 8. multiplying-by-one-digit-numbers ✓ 9. long-division ✓ 10. estimating-with-rounding-and-compatible-numbers ✓ 11. multiplication-and-division-word-problems ✓ 12. multi-step-problems-and-strip-diagrams ✓
13. input-output-tables-and-number-patterns ✓ 14. decomposing-fractions ✓ 15. equivalent-and-comparing-fractions ✓ 16. adding-and-subtracting-fractions ✓ 17. area-and-perimeter-formulas ✓ 18. lines-angles-and-triangles ✓
19. lines-of-symmetry ✓ 20. measuring-angles ✓ 21. measurement-conversions ✓ 22. measurement-word-problems ✓ 23. frequency-tables-dot-plots-and-stem-and-leaf-plots ✓ 24. personal-financial-literacy ✓

US-TX / Math / Grade 5（STAAR の学年。小数は 1000 分の 1 まで）— 生成スクリプトは `gen_ustx_math_g5_*`（US Grade 5・Grade 4 の問題関数を build_sets で再利用、ほかは自前）。メートル法は mass（STAAR の参考資料と同じ）、ヤード・ポンド法は weight
1. decimal-place-value-to-thousandths ✓ 2. comparing-and-rounding-decimals ✓ 3. estimating ✓ 4. multiplying-three-digit-by-two-digit-numbers ✓ 5. dividing-by-two-digit-divisors ✓ 6. multiplying-decimals ✓
7. dividing-decimals ✓ 8. adding-and-subtracting-fractions ✓ 9. adding-and-subtracting-decimals ✓ 10. multiplying-whole-numbers-and-fractions ✓ 11. dividing-with-unit-fractions ✓ 12. prime-and-composite-numbers ✓
13. multi-step-problems-and-equations ✓ 14. numerical-patterns-and-graphs ✓ 15. order-of-operations ✓ 16. volume-of-rectangular-prisms ✓ 17. perimeter-area-and-volume-problems ✓ 18. classifying-two-dimensional-figures ✓
19. measurement-conversions ✓ 20. coordinate-plane ✓ 21. data-and-scatterplots ✓ 22. personal-financial-literacy ✓

US-TX / Math / Grade 6（STAAR の学年。負の数は「−」）— 生成スクリプトは `gen_ustx_math_g6_*`（US Grade 6・7 の問題関数を build_sets で再利用、ほかは自前）。standard_url は TEA の Chapter 111 Subchapter B（tx_common.make が Grade 6 以上で自動で切り替え）
1. integers-and-rational-numbers ✓ 2. comparing-and-ordering-rational-numbers ✓ 3. adding-and-subtracting-integers ✓ 4. multiplying-and-dividing-integers ✓ 5. dividing-fractions ✓
6. multiplying-and-dividing-decimals ✓ 7. ratios-and-rates ✓ 8. ratio-tables-and-graphs ✓ 9. fractions-decimals-and-percents ✓ 10. percent-problems ✓ 11. converting-units ✓
12. independent-and-dependent-quantities ✓ 13. exponents-and-order-of-operations ✓ 14. expressions-and-equations ✓ 15. equivalent-expressions ✓ 16. triangle-properties ✓
17. area-of-triangles-parallelograms-and-trapezoids ✓ 18. volume-of-rectangular-prisms ✓ 19. one-step-equations ✓ 20. one-step-inequalities ✓ 21. coordinate-plane ✓
22. dot-plots-histograms-and-box-plots ✓ 23. mean-median-range-and-iqr ✓ 24. categorical-data-and-relative-frequency ✓ 25. personal-financial-literacy ✓

US-TX / Math / Grade 7（STAAR の学年）— 生成スクリプトは `gen_ustx_math_g7_*`（US Grade 6〜8 の問題関数を build_sets で再利用。US Grade 7・8 の生成スクリプトはモジュールの R を使うので、新しい seed で R を入れ替える）。他の TX 生成スクリプトを import するときは imports に書く（extra に書くと GRADE が上書きされる）。tx_common.us_text は「an $8」などの冠詞も直す
1. sets-of-rational-numbers ✓ 2. adding-and-subtracting-rational-numbers ✓ 3. multiplying-and-dividing-rational-numbers ✓ 4. rational-number-word-problems ✓ 5. constant-rate-of-change ✓
6. unit-rates-with-fractions ✓ 7. constant-of-proportionality ✓ 8. percent-increase-and-decrease ✓ 9. converting-between-measurement-systems ✓ 10. similar-figures ✓ 11. scale-drawings ✓
12. circumference-and-area-of-circles ✓ 13. area-of-composite-figures ✓ 14. volume-of-prisms-and-pyramids ✓ 15. lateral-and-total-surface-area ✓ 16. linear-relationships ✓
17. two-step-equations ✓ 18. two-step-inequalities ✓ 19. equations-with-angles-and-triangles ✓ 20. probability-and-predictions ✓ 21. sample-spaces-and-compound-events ✓
22. random-samples-and-inferences ✓ 23. comparing-data-with-dot-plots-and-box-plots ✓ 24. sales-tax-income-tax-and-budgets ✓ 25. interest-net-worth-and-incentives ✓

US-TX / Math / Grade 8（STAAR の学年）— 生成スクリプトは `gen_ustx_math_g8_*`（US Grade 7・8 の問題関数を build_sets で再利用。Grade 7 と同じく R を新しい seed に入れ替える）。お金の教育（8.12）は 4 単元
1. sets-of-real-numbers ✓ 2. approximating-irrational-numbers ✓ 3. scientific-notation ✓ 4. ordering-real-numbers ✓ 5. dilations ✓ 6. slope ✓
7. proportional-and-non-proportional-relationships ✓ 8. writing-linear-equations ✓ 9. functions ✓ 10. scatterplots-and-trend-lines ✓ 11. equations-with-variables-on-both-sides ✓
12. systems-of-equations ✓ 13. angle-relationships-and-parallel-lines ✓ 14. transformations ✓ 15. pythagorean-theorem ✓ 16. distance-on-the-coordinate-plane ✓
17. volume-of-cylinders-cones-and-spheres ✓ 18. surface-area-of-prisms-and-cylinders ✓ 19. mean-absolute-deviation ✓ 20. random-samples-and-simulations ✓
21. cost-of-credit-and-loans ✓ 22. saving-and-investing-over-time ✓ 23. payment-methods-and-financial-responsibility ✓ 24. paying-for-college ✓

US-TX / Math / Grade 2（STAAR なし。1,200 まで。文は短く、絵を多く）— 生成スクリプトは `gen_ustx_math_g2_*`（US Grade 2・3、Ontario、AU の問題関数を build_sets で再利用、ほかは自前）。他国の A〜D の絵の問題（`build`・`_abcd`）は生成スクリプトの中で絵を作ってから渡す
1. place-value-to-1200 ✓ 2. comparing-and-ordering-numbers ✓ 3. number-lines ✓ 4. 10-more-10-less-100-more-100-less ✓ 5. addition-and-subtraction-facts-to-20 ✓
6. adding-and-subtracting-two-digit-numbers ✓ 7. adding-and-subtracting-within-1000 ✓ 8. word-problems-and-number-sentences ✓ 9. odd-and-even-numbers ✓ 10. counting-coins ✓
11. equal-groups-multiplication-and-division ✓ 12. halves-fourths-and-eighths ✓ 13. 2d-shapes-and-polygons ✓ 14. 3d-solids ✓ 15. measuring-length ✓ 16. length-word-problems ✓
17. area-with-square-units ✓ 18. telling-time-to-the-minute ✓ 19. pictographs-and-bar-graphs ✓ 20. personal-financial-literacy ✓

US-TX / Math / Grade 1（120 まで。とても短い文、絵を多く）— 生成スクリプトは `gen_ustx_math_g1_*`（US Grade 1・2、AU Year 1、Ontario、TX Grade 2 の問題関数を build_sets で再利用、ほかは自前）。AU の問題関数はオーストラリアの語（kookaburra・c の硬貨など）を keep で落とす
1. numbers-to-120 ✓ 2. comparing-and-ordering-numbers ✓ 3. adding-tens-and-ones ✓ 4. making-10 ✓ 5. addition-and-subtraction-facts-to-20 ✓
6. addition-and-subtraction-strategies ✓ 7. word-problems-within-20 ✓ 8. counting-coins ✓ 9. counting-to-120 ✓ 10. skip-counting-by-2s-5s-and-10s ✓
11. 10-more-and-10-less ✓ 12. equal-sign-and-missing-numbers ✓ 13. adding-three-numbers ✓ 14. 2d-shapes ✓ 15. 3d-solids ✓ 16. halves-and-fourths ✓
17. measuring-length ✓ 18. telling-time-to-the-hour-and-half-hour ✓ 19. tally-marks-and-graphs ✓ 20. personal-financial-literacy ✓

US-TX / Math / Kindergarten（5〜6歳。20 まで、数えるのは 100 まで。とても短い文、ほぼ全問に絵）— grade `kindergarten`（sort 0）。生成スクリプトは `gen_ustx_math_gk_*`（US Kindergarten・AU Foundation・US Grade 2・TX Grade 1 の問題関数を build_sets で再利用、ほかは自前）。自前の問題は pick() で場面を1回ずつ使い、名前だけ違う問題を作らない。tx_common.us_text は ladybird→ladybug、kookaburra→robin も直す
1. counting-to-20 ✓ 2. reading-and-writing-numbers-0-to-20 ✓ 3. subitizing ✓ 4. one-more-and-one-less ✓ 5. comparing-numbers-to-20 ✓ 6. composing-and-decomposing-numbers-to-10 ✓
7. addition-within-10 ✓ 8. subtraction-within-10 ✓ 9. addition-and-subtraction-strategies ✓ 10. counting-to-100-by-ones-and-tens ✓ 11. naming-coins ✓ 12. 2d-shapes ✓
13. 3d-solids ✓ 14. comparing-length-capacity-and-weight ✓ 15. sorting-and-picture-graphs ✓ 16. personal-financial-literacy ✓

US-TX / Math / Algebra I（TEKS §111.39、STAAR Algebra I の科目。高校）— grade `algebra-1`（name「Algebra I」、sort 9）。standard_url は TEA の Chapter 111 Subchapter C（tx_common.make が algebra で自動で切り替え）。生成スクリプトは `gen_ustx_math_a1_*`（US Algebra 1・Algebra 2・Geometry・Grade 8 の問題関数を build_sets で再利用、ほかは自前）。US の固定の文章題（problems()）は半分（10問）だけ使い、残りは別の問題関数で埋める。domain は TEKS の分野名（Linear Functions, Equations, and Inequalities／Quadratic Functions and Equations／Exponential Functions and Equations／Number and Algebraic Methods／Algebraic Reasoning）
1. functions-and-function-notation ✓ 2. domain-and-range ✓ 3. slope-and-rate-of-change ✓ 4. graphing-linear-functions ✓ 5. writing-linear-equations ✓ 6. parallel-and-perpendicular-lines ✓
7. direct-variation ✓ 8. solving-linear-equations ✓ 9. linear-inequalities ✓ 10. systems-of-linear-equations ✓ 11. systems-of-linear-inequalities ✓ 12. correlation-and-lines-of-fit ✓
13. transformations-of-linear-functions ✓ 14. polynomial-operations ✓ 15. dividing-polynomials ✓ 16. factoring ✓ 17. graphing-quadratic-functions ✓ 18. writing-quadratic-functions ✓
19. transformations-of-quadratic-functions ✓ 20. solving-quadratic-equations ✓ 21. exponential-functions ✓ 22. exponents-and-radicals ✓ 23. arithmetic-and-geometric-sequences ✓ 24. literal-equations-and-formulas ✓

US-TX / Math / Geometry（TEKS §111.41。高校）— grade `geometry`（name「Geometry」、sort 10）。standard_url は Subchapter C（tx_common.make は grade- 以外を ch111c にする）。生成スクリプトは `gen_ustx_math_ge_*`（US Geometry・Precalculus・Grade 7、TX Grade 8、AU Year 8 の問題関数を build_sets で再利用、ほかは自前）。domain は TEKS の分野名（Coordinate and Transformational Geometry／Logical Argument and Constructions／Proof and Congruence／Similarity, Proof, and Trigonometry／Two-Dimensional and Three-Dimensional Figures／Circles／Probability）。tx_common.us_text は trapezium→trapezoid も直す
1. points-lines-planes-and-definitions ✓ 2. conditional-statements-and-counterexamples ✓ 3. segments-midpoints-and-partitions ✓ 4. distance-slope-and-midpoint-formulas ✓ 5. equations-of-parallel-and-perpendicular-lines ✓
6. angles-and-parallel-lines ✓ 7. transformations ✓ 8. reflectional-and-rotational-symmetry ✓ 9. triangle-angle-theorems ✓ 10. triangle-inequality-theorem ✓ 11. proving-triangles-congruent ✓
12. midsegments-bisectors-and-medians ✓ 13. quadrilaterals-and-polygon-angles ✓ 14. dilations-and-similar-figures ✓ 15. similar-triangles-and-proportionality ✓ 16. right-triangle-similarity-and-geometric-mean ✓
17. pythagorean-theorem-and-special-right-triangles ✓ 18. trigonometric-ratios ✓ 19. cross-sections-and-solids-of-revolution ✓ 20. dimensional-change ✓ 21. area-of-regular-polygons-and-composite-figures ✓
22. surface-area ✓ 23. volume ✓ 24. circle-angles-chords-tangents-and-secants ✓ 25. arc-length-sector-area-and-radians ✓ 26. equations-of-circles ✓ 27. permutations-and-combinations ✓
28. geometric-probability ✓ 29. independent-and-conditional-probability ✓

US-TX / Math / Algebra II（TEKS §111.40。高校）— grade `algebra-2`（name「Algebra II」、sort 11）。standard_url は Subchapter C。生成スクリプトは `gen_ustx_math_a2_*`（US Algebra 1・Algebra 2・Precalculus の問題関数を build_sets で再利用、ほかは自前）。TX Algebra I で使った US の固定の文章題（problems()）は使わない。親関数の変形は `fam(tr.one_x, "sqrt")` で US Algebra 2 の PARENTS を絞り、1/x・∛x・b^x・log_b x（b は 2・10・e）は自前の `tf(kind)`、f(bx) は自前の `one_bx_maker`。domain は TEKS の分野名（Attributes of Functions and Their Inverses／Systems of Equations and Inequalities／Quadratic and Square Root Functions, Equations, and Inequalities／Exponential and Logarithmic Functions and Equations／Cubic, Cube Root, Absolute Value, and Rational Functions, Equations, and Inequalities／Number and Algebraic Methods／Data）。年（2015 など）は自動でカンマが付くので文章題に書かない
1. parent-functions ✓ 2. inverse-functions ✓ 3. domain-and-range-notation ✓ 4. systems-of-three-equations ✓ 5. linear-quadratic-systems ✓ 6. systems-of-linear-inequalities ✓
7. quadratic-through-three-points ✓ 8. parabolas-focus-and-directrix ✓ 9. completing-the-square-and-vertex-form ✓ 10. quadratic-equations-and-inequalities ✓ 11. square-root-functions-and-equations ✓ 12. exponential-and-logarithmic-functions ✓
13. logarithms ✓ 14. exponential-and-logarithmic-equations ✓ 15. cubic-and-cube-root-functions ✓ 16. absolute-value-functions-equations-and-inequalities ✓ 17. rational-functions ✓ 18. rational-equations-and-inverse-variation ✓
19. complex-numbers ✓ 20. polynomial-operations-and-division ✓ 21. factoring-polynomials ✓ 22. rational-expressions ✓ 23. radicals-and-rational-exponents ✓ 24. data-and-regression ✓

US-TX / Math / Precalculus（TEKS §111.42。高校）— grade `precalculus`（name「Precalculus」、sort 12）。standard_code は「P.2A」形式。生成スクリプトは `gen_ustx_math_pc_*`（US Algebra 2・Precalculus・Geometry の問題関数を build_sets で再利用、ほかは自前）。TX Algebra II・Geometry で使った問題関数は、できるだけ別の問題関数か自前に替える。domain は TEKS の分野名（Functions／Relations and Geometric Reasoning／Number and Measure／Algebraic Reasoning）。不等式の区間表記は自前の `solve_ineq`（pc の生成スクリプト内）
1. composition-of-functions ✓ 2. even-odd-and-inverse-functions ✓ 3. piecewise-and-step-functions ✓ 4. transformations-of-functions ✓ 5. key-features-of-polynomial-functions ✓ 6. end-behavior ✓ 7. asymptotes-of-rational-functions ✓
8. discontinuities ✓ 9. modeling-with-functions ✓ 10. trigonometric-values-of-special-angles ✓ 11. degrees-radians-and-reference-angles ✓ 12. linear-and-angular-velocity ✓ 13. graphs-of-trigonometric-functions ✓ 14. sinusoidal-models ✓
15. inverse-trigonometric-functions ✓ 16. trigonometric-identities ✓ 17. trigonometric-equations ✓ 18. bearings-and-angles-of-elevation ✓ 19. law-of-sines-and-law-of-cosines ✓ 20. vectors ✓ 21. parametric-equations ✓
22. polar-coordinates-and-graphs ✓ 23. conic-sections ✓ 24. ellipses-and-hyperbolas ✓ 25. sequences-series-and-sigma-notation ✓ 26. logarithmic-and-exponential-equations ✓ 27. polynomial-equations-and-inequalities ✓ 28. rational-inequalities ✓

US-TX / Math は Kindergarten〜Precalculus まで完了。ws_common.num は割り切れない小数で None を返すので、選択肢の文字列に入れるときは `num(x) or num(x, "f")` にする

PH / Math（DepEd MATATAG Curriculum, Mathematics）— country `ph`（name「Philippines」、lang en、hreflang en-ph）、subject `math`、grade `grade-N`、Letter。生成スクリプトは `gen_ph_math_gN_*`、共通部品は `tools/ph_common.py`（tx_common と同じ API。フィリピンの名前・地名、localize で他国の生成スクリプトの名前をフィリピンの名前に置き換え、us_text で US の綴り（round→around、ml→mL、a.m.. の重複も直す）、LEAKS で $・¢・£・inch・miles・Texas などの混入を落とす、peso（₱25、₱1,250、₱45.50）、make）。
US 英語・メートル法だけ・お金は ₱ と centavos（25 centavos 硬貨・₱1 硬貨・₱50〜₱1,000 札）。時刻は「9:30 a.m.」。1,000 以上はカンマ（DepEd の CG は空白区切りだがカンマを使う）。場面はフィリピン（sari-sari store、jeepney、pandesal、Carabao mango、Cebu、Davao）。
standard_code は MATATAG の分野名「Grade 4: Number and Algebra」／「Grade 4: Measurement and Geometry」／「Grade 4: Data and Probability」、standard_text は CG の learning competency の原文、standard_url は Grade 1・4・7 は CG の PDF（ph_common.STD_URLS）。年齢は US と同じ（Grade N = N+5〜N+6 歳、unit.php）。
Grade 4 の分数は CG のとおり分母 10 まで（他国の問題関数は keep の den10・den_q10 で絞る）

PH / Math / Grade 4（MATATAG。Q1〜Q4 の順）
1. angles ✓ 2. triangles-and-quadrilaterals ✓ 3. perimeter ✓ 4. numbers-up-to-1000000 ✓ 5. rounding-and-estimating ✓ 6. adding-and-subtracting-to-1000000 ✓
7. multiplying-whole-numbers ✓ 8. dividing-whole-numbers ✓ 9. multi-step-word-problems-and-money ✓ 10. order-of-operations-mdas ✓ 11. proper-improper-fractions-and-mixed-numbers ✓
12. adding-and-subtracting-similar-fractions ✓ 13. converting-units-of-length-mass-and-capacity ✓ 14. converting-time-and-elapsed-time ✓ 15. comparing-and-ordering-dissimilar-fractions ✓
16. equivalent-fractions-and-simplest-form ✓ 17. factors-and-multiples ✓ 18. adding-and-subtracting-dissimilar-fractions ✓ 19. line-symmetry ✓ 20. reflection-and-glide-reflection ✓
21. decimal-numbers-to-hundredths ✓ 22. comparing-ordering-and-rounding-decimals ✓ 23. patterns ✓ 24. number-sentences-properties-and-equivalent-facts ✓ 25. tables-and-line-graphs ✓

PH / Math / Grade 7（MATATAG。高校の最初の学年）— 生成スクリプトは `gen_ph_math_g7_*`。UK KS3・AU Year 7–8・SG Sec・US Grade 6–8・TX・Ontario・BC の問題関数（one_x・set_x）を再利用。
ph_common.adopt は gbp・aud・sgd などのお金の関数を peso に替える（モジュール独自の money は imports の extra で `mod.money = peso`）。単位換算の単元だけ `ph_common.ALLOW_IMPERIAL = True`（CG が across different systems のため）。
LEAKS にカナダ・オーストラリア・英国・米国の地名と雪のスポーツを入れてある。新しく混ざったら LEAKS に足す。VAT は 12%。「standard form」は「decimal form」に直す
1. classifying-and-drawing-polygons ✓ 2. angle-pairs ✓ 3. interior-and-exterior-angles-of-polygons ✓ 4. percentage-increase-and-decrease ✓ 5. discount-commission-vat-and-simple-interest ✓
6. budgets-and-financial-plans ✓ 7. rates-and-speed ✓ 8. fractions-decimals-and-percentages ✓ 9. ordering-rational-numbers-on-a-number-line ✓ 10. operations-on-rational-numbers ✓
11. square-roots-and-cube-roots ✓ 12. irrational-numbers-on-the-number-line ✓ 13. sets-subsets-union-and-intersection ✓ 14. subsets-of-real-numbers ✓ 15. converting-units-of-measure ✓
16. volume-of-cylinders ✓ 17. volume-of-pyramids ✓ 18. data-collection-and-sampling ✓ 19. frequency-distribution-tables ✓ 20. statistical-graphs ✓
21. integers-and-absolute-value ✓ 22. adding-and-subtracting-integers ✓ 23. multiplying-and-dividing-integers ✓ 24. order-of-operations-gemdas ✓
25. algebraic-expressions ✓ 26. properties-of-equality-and-solving-equations ✓ 27. formulas-and-solving-for-a-variable ✓ 28. scientific-notation ✓ 29. probability-experiments-and-outcomes ✓

PH / Math / Grade 1（MATATAG。100 まで、計算は 20 まで・100 までは繰り上がり／繰り下がりなし。とても短い文、ほぼ全問に絵）— 生成スクリプトは `gen_ph_math_g1_*`。US Grade 1・AU Year 1／Foundation・UK Year 1・SG Primary 1・Ontario・BC・TX Grade 1・AU Year 2（turns・time）の問題関数を再利用。
120 までの問題関数は keep の le100 で絞る。足し算の単元は add20（引き算の話を落とす）。お金は自前の money_svg（₱1・₱5・₱10・₱20 硬貨、₱20・₱50・₱100 札、centavo なし）。
ph_common.run_many は A〜D の絵の問題（"build"）を組み立ててから使う。pence（5p）・puck も LEAKS
1. 2d-shapes ✓ 2. composing-and-decomposing-shapes ✓ 3. counting-to-100 ✓ 4. reading-and-writing-numbers-to-100 ✓ 5. comparing-and-ordering-numbers-to-20 ✓ 6. ordinal-numbers ✓
7. composing-and-decomposing-numbers-to-10 ✓ 8. addition-within-20 ✓ 9. addition-word-problems-within-20 ✓ 10. measuring-length-with-non-standard-units ✓ 11. ordering-numbers-to-100 ✓
12. skip-counting-by-2s-5s-and-10s ✓ 13. tens-and-ones ✓ 14. adding-within-100-without-regrouping ✓ 15. pictographs ✓ 16. subtraction-within-20 ✓
17. missing-numbers-and-equivalent-expressions ✓ 18. subtracting-within-100-without-regrouping ✓ 19. repeating-patterns ✓ 20. halves-and-quarters ✓
21. philippine-money ✓ 22. half-turns-and-quarter-turns ✓ 23. telling-time ✓ 24. days-of-the-week-and-months-of-the-year ✓

PH の次: MATATAG の CG が出ている学年（1・4・7）は完了。Grades 2・3・5・6・8 は CG が公開されたら（DepEd の MATATAG ページを確認）。catalog.json に学年を足す

ZA / Maths（CAPS Mathematics。Intermediate Phase は Grade 4–6）— country `za`（name「South Africa」、lang en、hreflang en-za）、subject `maths`、grade `grade-N`、A4。生成スクリプトは `gen_za_maths_gN_*`、共通部品は `tools/za_common.py`（ph_common と同じ API。南アの名前・地名、localize、gb_text でイギリス式の綴り（colour・metre・trapezium・anti-clockwise・maths・learners・tuck shop・spaza shop・biscuits・sweets）、LEAKS で $・₱・£・inch・Texas・フィリピンや英国の地名などを落とす、rand（R25、R1 250、R45,50）・cents（50c）、make）。
数の書き方は南ア式: 1 000 以上は空白区切り（4 536、10 000。ノーブレークスペース）、小数はコンマ（2,5・R12,50）。za_numbers が SVG の文字も含めて自動で直す（小数が並ぶときは「1,5; 2,5」）。容量は mℓ と ℓ。時刻は 24 時間制「14:30」も使う。
standard_code は CAPS の topic「Grade 4: 1.1 Whole numbers」形式、standard_text は CAPS の concepts and skills の要約、standard_url は CAPS IP Mathematics Gr 4-6 の PDF。domain は CAPS の 5 分野（Numbers, Operations and Relationships／Patterns, Functions and Algebra／Space and Shape (Geometry)／Measurement／Data Handling）。年齢は US と同じ（unit.php）。topic_gb() に za を入れた
Grade 4 の分数は CAPS のとおり halves〜eighths（keep の den8。同値分数は den12）。数は 10 000 まで（le10000）

ZA / Maths / Grade 4（CAPS）
1. whole-numbers-to-10000 ✓ 2. rounding-off-to-10-100-and-1000 ✓ 3. addition-and-subtraction ✓ 4. calculation-techniques ✓ 5. multiplication-tables-to-10-x-10 ✓ 6. multiplication ✓
7. division ✓ 8. multiples-and-factors ✓ 9. properties-of-operations ✓ 10. common-fractions ✓ 11. money-rate-and-ratio-problems ✓ 12. numeric-patterns ✓ 13. geometric-patterns ✓
14. number-sentences ✓ 15. 2d-shapes-and-angles ✓ 16. 3d-objects ✓ 17. symmetry ✓ 18. composite-shapes-and-tessellations ✓ 19. viewing-objects ✓ 20. position-and-movement ✓
21. length ✓ 22. mass ✓ 23. capacity-and-volume ✓ 24. time ✓ 25. temperature ✓ 26. perimeter-area-and-volume ✓ 27. collecting-and-organising-data ✓
28. pictographs-bar-graphs-and-pie-charts ✓ 29. probability ✓

ZA / Maths / Grade 5（CAPS。数は 6 桁まで、小数なし（お金の R45,50 だけ）、分数は twelfths まで、温度は正の数だけ）— 生成スクリプトは `gen_za_maths_g5_*`。G4 の生成スクリプトの問題関数（換算・お金・温度など）も再利用。za_common.gb_text は ZA_PLACES で AU の動物・米国の鳥・Sydney・fall も南ア向けに直す
1. whole-numbers-to-6-digits ✓ 2. rounding-off-to-5-10-100-and-1000 ✓ 3. addition-and-subtraction ✓ 4. calculation-techniques ✓ 5. multiplication ✓ 6. division ✓ 7. multiples-and-factors ✓ 8. properties-of-operations ✓ 9. common-fractions ✓ 10. adding-and-subtracting-fractions ✓ 11. money-rate-and-ratio-problems ✓ 12. numeric-patterns ✓ 13. geometric-patterns ✓ 14. number-sentences ✓ 15. 2d-shapes ✓ 16. angles ✓ 17. 3d-objects ✓ 18. symmetry ✓ 19. transformations ✓ 20. viewing-objects ✓ 21. position-and-movement ✓ 22. length ✓ 23. mass ✓ 24. capacity-and-volume ✓ 25. time ✓ 26. temperature ✓ 27. perimeter-area-and-volume ✓ 28. collecting-and-organising-data ✓ 29. pictographs-bar-graphs-and-pie-charts ✓ 30. probability ✓

ZA / Maths / Grade 6（CAPS。数は 9 桁まで、小数は 3 桁まで（コンマ）、負の数なし、分数は twelfths まで＋100分の1）— 生成スクリプトは `gen_za_maths_g6_*`。時刻表は自前（Gautrain・MyCiTi・Metrorail・Durban bus）。za_ok は SVG の文字と aria-label も LEAKS で調べる（AU・カナダの地名や動物、maple）。gb_text は Year N→Grade N、Pupil・Student→Learner、Fall→Autumn も直す
1. whole-numbers-to-9-digits ✓ 2. rounding-off ✓ 3. addition-and-subtraction ✓ 4. calculation-techniques ✓ 5. multiplication ✓ 6. division ✓ 7. multiples-factors-and-prime-numbers ✓ 8. properties-and-order-of-operations ✓ 9. common-fractions ✓ 10. adding-and-subtracting-fractions ✓ 11. fractions-of-whole-numbers ✓ 12. decimal-fractions ✓ 13. adding-and-subtracting-decimals ✓ 14. multiplying-and-dividing-decimals ✓ 15. percentages ✓ 16. money-rate-and-ratio-problems ✓ 17. numeric-patterns ✓ 18. geometric-patterns ✓ 19. number-sentences ✓ 20. 2d-shapes ✓ 21. angles ✓ 22. 3d-objects ✓ 23. symmetry ✓ 24. transformations-enlargements-and-reductions ✓ 25. position-and-movement ✓ 26. length ✓ 27. mass ✓ 28. capacity-and-volume ✓ 29. time ✓ 30. temperature ✓ 31. perimeter-area-and-volume ✓ 32. collecting-and-organising-data ✓ 33. pictographs-bar-graphs-and-pie-charts ✓ 34. probability ✓

ZA / Maths / Grade 7（CAPS Senior Phase。負の数は「−」、円・π・指数表記は Grade 8 以降なので出さない（keep の ok7））— 生成スクリプトは `gen_za_maths_g7_*`。UK Year 7・AU Year 7 の one_x を collect で多く再利用。standard_url は CAPS SP Mathematics Gr 7-9 の PDF（STD_URL_SP）。
Senior Phase は `za_common.GBP_TO_RAND = True`（UK・AU の問題関数の £・$ を R に、pence を cents に）。za_ok は GST・HST と 15% 以外の VAT を落とす。gb_text は mom→mother。財務（利益・割引・VAT 15%・予算・単利）は自前
1. whole-numbers ✓ 2. multiples-factors-and-prime-factorisation ✓ 3. calculating-with-whole-numbers ✓ 4. ratio-and-rate ✓ 5. financial-maths ✓ 6. exponents ✓ 7. integers ✓ 8. common-fractions ✓ 9. multiplying-fractions ✓ 10. percentages ✓ 11. decimal-fractions ✓ 12. calculating-with-decimals ✓ 13. numeric-and-geometric-patterns ✓ 14. functions-and-relationships ✓ 15. algebraic-expressions ✓ 16. algebraic-equations ✓ 17. graphs ✓ 18. geometry-of-straight-lines ✓ 19. triangles-and-quadrilaterals ✓ 20. 3d-objects ✓ 21. transformation-geometry ✓ 22. area-and-perimeter ✓ 23. surface-area-and-volume ✓ 24. collecting-and-summarising-data ✓ 25. bar-graphs-histograms-and-pie-charts ✓ 26. probability ✓

ZA / Maths / Grade 8（CAPS Senior Phase。円・π・指数表記・ピタゴラスあり。三角比・二次方程式はなし（keep の ok8））— 生成スクリプトは `gen_za_maths_g8_*`。UK Year 7–9・AU Year 7–8・SG Sec 1 の one_x を再利用。財務（割賦・複利・為替）は自前（為替は「Suppose 1 euro = R20」の形で dollar を使わない）。
za_common: gb_text は standard form→scientific notation、za_ok は「= None」の壊れた解説を落とす、collect は ValueError なども飛ばす
1. whole-numbers ✓ 2. financial-maths ✓ 3. integers ✓ 4. exponents ✓ 5. scientific-notation ✓ 6. common-fractions ✓ 7. decimal-fractions ✓ 8. numeric-and-geometric-patterns ✓ 9. functions-and-relationships ✓ 10. algebraic-expressions ✓ 11. algebraic-equations ✓ 12. graphs ✓ 13. geometry-of-straight-lines ✓ 14. triangles-congruence-and-similarity ✓ 15. quadrilaterals-and-polygons ✓ 16. transformation-geometry ✓ 17. 3d-objects ✓ 18. area-and-perimeter ✓ 19. surface-area-and-volume ✓ 20. theorem-of-pythagoras ✓ 21. collecting-and-summarising-data ✓ 22. histograms-pie-charts-and-line-graphs ✓ 23. probability ✓

ZA / Maths / Grade 9（CAPS Senior Phase。負の指数・因数分解（共通因数・平方の差・三項式）・因数分解で解く方程式・指数方程式・円柱あり。三角比・連立方程式・円錐・球はなし（keep の ok9））— 生成スクリプトは `gen_za_maths_g9_*`。SG Sec 1–3・UK Year 8–9・AU Year 8 の one_x を再利用。手数料・家賃は自前、複利・割賦・為替は G8 の問題関数
1. real-numbers ✓ 2. financial-maths ✓ 3. exponents ✓ 4. scientific-notation ✓ 5. numeric-and-geometric-patterns ✓ 6. functions-and-relationships ✓ 7. algebraic-expressions ✓ 8. factorisation ✓ 9. algebraic-equations ✓ 10. linear-graphs ✓ 11. geometry-of-straight-lines ✓ 12. similar-and-congruent-triangles ✓ 13. quadrilaterals-and-polygons ✓ 14. transformation-geometry ✓ 15. 3d-objects-views-and-nets ✓ 16. area-and-perimeter ✓ 17. surface-area-and-volume ✓ 18. theorem-of-pythagoras ✓ 19. collecting-and-summarising-data ✓ 20. scatter-plots-histograms-and-pie-charts ✓ 21. probability ✓

ZA / Maths / Grade 10（CAPS FET Phase。standard_url は CAPS FET Mathematics Gr 10-12 の PDF（STD_URL_FET）。三角比は 0°〜360°、三角方程式は 0°〜90°。複素数・対数・弧度法・正弦／余弦定理・独立事象・有理指数はなし（keep の ok10））— 生成スクリプトは `gen_za_maths_g10_*`。US Algebra 1・Geometry、UK Year 8–9、SG Sec 1–4、AU Year 7–8 の one_x を再利用。特別角・三角方程式・三角関数のグラフ・y = ax² + q・y = a/x + q・y = abˣ + q・逆数比・P(x; y)・単利・インフレ・排反／余事象は自前。
domain は「Algebra and Number Patterns／Functions／Trigonometry／Euclidean and Analytical Geometry／Finance and Growth／Measurement／Statistics and Probability」。
za_common.gb_text（GBP_TO_RAND のとき）は座標 (3, 4)→(3; 4)、m∠→∠、slope→gradient、penny→cent も直す
1. number-system-and-surds ✓ 2. products-and-factorisation ✓ 3. algebraic-fractions ✓ 4. exponents-and-exponential-equations ✓ 5. number-patterns ✓ 6. linear-and-literal-equations ✓ 7. quadratic-equations ✓ 8. simultaneous-equations ✓ 9. linear-inequalities ✓ 10. trigonometric-ratios ✓ 11. special-angles-equations-and-2d-problems ✓ 12. trigonometric-functions ✓ 13. linear-and-quadratic-functions ✓ 14. hyperbolic-and-exponential-functions ✓ 15. euclidean-geometry ✓ 16. analytical-geometry ✓ 17. finance-and-growth ✓ 18. statistics ✓ 19. measurement ✓ 20. probability ✓

ZA / Maths / Grade 11（CAPS FET Phase。対数・弧度法・sec/csc/cot・複合角／2倍角・微分はなし（kp(ok11) で他国の問題関数を絞る））— 生成スクリプトは `gen_za_maths_g11_*`。US Algebra 1・Geometry、SG Sec 3–4、UK Year 8–9、TX Algebra II の one_x を kp() で再利用。判別式・二次不等式・二次数列・接線・傾斜角・y = a(x + p)² + q・y = a/(x + p) + q・y = ab^(x + p) + q・k と p の三角関数グラフ・還元公式・恒等式・一般解・減価償却・実効金利は自前（fk(fun, kind) は種類ごとに 1 つの uniq を共有して、セットをまたいで同じ問題を出さない）。
za_common.gb_text は Law of Sines→Sine rule、perpendicular slopes→perpendicular gradients も直す
1. exponents-and-surds ✓ 2. completing-the-square-and-quadratic-formula ✓ 3. nature-of-roots ✓ 4. quadratic-inequalities ✓ 5. simultaneous-linear-and-quadratic-equations ✓ 6. quadratic-number-patterns ✓ 7. analytical-geometry ✓ 8. quadratic-functions ✓ 9. hyperbolic-and-exponential-functions ✓ 10. trigonometric-functions ✓ 11. reduction-formulae-and-identities ✓ 12. trigonometric-equations ✓ 13. sine-cosine-and-area-rules ✓ 14. euclidean-geometry-circle-theorems ✓ 15. finance-growth-and-decay ✓ 16. probability ✓ 17. statistics ✓

ZA / Maths / Grade 12（CAPS FET Phase、NSC（matric）の学年。弧度法・sec/csc/cot・tan の複合角・nCr・ln/e・積分はなし（kp(ok12)）。kp() は関数ごとに 1 つの uniq を共有し、localize・gb_text 後の文で重複を判定する）— 生成スクリプトは `gen_za_maths_g12_*`。US Algebra 2・Precalculus・Geometry・Algebra 1、SG Sec 4 の one_x を kp() で再利用。年金（将来価値・現在価値・返済額・回数・減債基金）、微分（極限・定義・公式・接線・三次関数・最適化・速度）、数列の和・Σ・無限和、逆関数、対数、円の接線、比例定理、回帰、数え上げは自前。
南アの小数は小数点以下 3 桁がちょうど 3 桁だと za_numbers が千の位の区切りと見なす（0,075 → 0 075）ので、利率は「7,5% ÷ 12」、和は分数で書く。トピック `calculus`（Differential Calculus）を足した
1. arithmetic-and-geometric-sequences-and-series ✓ 2. sigma-notation-and-sum-to-infinity ✓ 3. inverse-functions ✓ 4. logarithms ✓ 5. future-value-annuities-and-sinking-funds ✓ 6. present-value-annuities-and-loans ✓ 7. factor-theorem-and-cubic-polynomials ✓ 8. limits-and-first-principles ✓ 9. rules-of-differentiation ✓ 10. equations-of-tangents ✓ 11. cubic-functions ✓ 12. optimisation-and-rates-of-change ✓ 13. compound-and-double-angles ✓ 14. problems-in-three-dimensions ✓ 15. analytical-geometry-circles ✓ 16. euclidean-geometry-proportionality-and-similarity ✓ 17. regression-and-correlation ✓ 18. counting-principle-and-probability ✓

ZA / Maths / Grade 1–3（CAPS Foundation Phase。standard_url は CAPS FP Mathematics Gr 1-3 の PDF（STD_URL_FP）。G1 は 20 まで（数えるのは 100 まで）、G2 は 99 まで（数えるのは 200 まで）、G3 は 999 まで。とても短い文、絵を多く）— 生成スクリプトは `gen_za_maths_g1_*`・`g2_*`・`g3_*`。
数・計算・文章題・かけ算わり算は自前（num_k・calc_k・story_k・group_k を F(fun, kind, 範囲) で使う。k_pics の絵）、お金は自前（mk(kind, 上限の cents)、10c〜R5 の硬貨と R10〜R200 の札の絵）。図形・位置・時刻・測定・データ・分数・パターンは UK Year 1–3・AU Year 1–3・Ontario Grade 1–3・US Grade 1 のセット関数を run で再利用（le(n) で数の上限、nomoney でお金の問題を落とす）。
za_common: adopt は大文字で始まる地名のリストだけを南アの地名に替える（tree・house などはそのまま）、za_ok は名前や語を置き換えたあとで選択肢が重なる問題を落とす、conkers→marbles、loonies・snowbank などを LEAKS に
ZA / Maths / Grade 1
1. counting-to-100 ✓ 2. numbers-to-20 ✓ 3. tens-and-ones ✓ 4. number-bonds-to-10 ✓ 5. addition-and-subtraction-to-20 ✓ 6. problem-solving-to-20 ✓ 7. grouping-and-sharing ✓ 8. halves-and-quarters ✓ 9. money ✓ 10. patterns ✓ 11. 2d-shapes-and-3d-objects ✓ 12. position-and-direction ✓ 13. time ✓ 14. length-mass-and-capacity ✓ 15. data-handling ✓
ZA / Maths / Grade 2
1. numbers-to-200 ✓ 2. place-value ✓ 3. odd-and-even-numbers ✓ 4. addition-and-subtraction-facts-to-20 ✓ 5. adding-and-subtracting-to-99 ✓ 6. problem-solving-to-99 ✓ 7. multiplication-by-2-5-and-10 ✓ 8. sharing-and-grouping ✓ 9. fractions ✓ 10. money ✓ 11. patterns ✓ 12. 2d-shapes-3d-objects-and-symmetry ✓ 13. position-and-direction ✓ 14. time ✓ 15. length-mass-and-capacity ✓ 16. data-handling ✓
ZA / Maths / Grade 3
1. numbers-to-1000 ✓ 2. place-value ✓ 3. adding-and-subtracting-to-999 ✓ 4. mental-mathematics ✓ 5. problem-solving-to-999 ✓ 6. times-tables-2-3-4-5-and-10 ✓ 7. multiplication-and-division ✓ 8. fractions ✓ 9. money ✓ 10. patterns ✓ 11. 2d-shapes-and-3d-objects ✓ 12. symmetry ✓ 13. position-and-maps ✓ 14. time ✓ 15. length ✓ 16. mass-and-capacity ✓ 17. perimeter-and-area ✓ 18. data-handling ✓

ZA / Maths / Grade R（Reception Year、5〜6歳）— grade `grade-r`（name「Grade R」、sort 0）。standard_url は CAPS Gr R の PDF（STD_URL_R）。10 まで、とても短い文、ほぼ全問に絵。お金（認識だけ）・かけ算わり算はなし。生成スクリプトは `gen_za_maths_gr_*`。US Kindergarten・AU Foundation・SG Primary 1（ordinal）・UK Year 1・US Grade 1 の問題関数を再利用、数・文章題・分ける問題は自前（FC で 10 を超える誤答を近い数に替え、÷ を使わない）。le は「1 cats」のような文法の誤り・kaya などの混入も落とす。図形は circle・triangle・square・rectangle・ball・box だけを答えにする（basic）。unit.php で educationalLevel を Grade R / Reception Year に
1. counting-to-10 ✓ 2. number-symbols-and-names-to-10 ✓ 3. comparing-and-ordering-to-10 ✓ 4. ordinal-numbers-to-tenth ✓ 5. adding-and-taking-away-to-10 ✓ 6. story-sums-to-10 ✓ 7. sharing-and-halves ✓ 8. patterns ✓ 9. 2d-shapes-and-3d-objects ✓ 10. position-and-direction ✓ 11. time ✓ 12. length-mass-and-capacity ✓ 13. sorting-and-data ✓

ZA / Maths は Grade R〜12 まで完了

DE / Mathe（KMK-Bildungsstandards Mathematik Primarbereich, Fassung 2022。学年への配分は各州の Lehrplan の一般的な内容）— country `de`（name「Deutschland」、lang `de`、hreflang de-de）、subject `mathe`（Mathe）、grade `klasse-N`（Klasse N、N+5〜N+6 歳）、A4。生成スクリプトは `gen_de_mathe_kN_*`、共通部品は `tools/de_common.py`（num・dez・eur（3,50 €・45 ct）・Kids（名前と er/sie）・mcq・mix・lesson・example・make_unit・schriftlich（Karopapier の筆算）・zahlenstrahl・dienes・stellenwerttafel・saeulen・strichliste・geld_svg・solid_svg・clock）。
ドイツ語、du で話しかける短い文。記号は 3 · 4（Malpunkt）、12 : 3、17 : 5 = 3 Rest 2。小数はコンマ（2,50 €）、5 桁以上はノーブレークスペース区切り。時刻は「8:15 Uhr」、時間量は「1 h 25 min」。「halb vier」= 3:30 Uhr。
domain は Leitidee（Zahl und Operation／Raum und Form／Muster, Strukturen und funktionaler Zusammenhang／Größen und Messen／Daten und Zufall）、standard_code は「Leitidee Zahl und Operation」、standard_text は要約、standard_url は KMK の Primarbereich Mathe PDF。body_html は「So geht's → Beispiel → Typische Fehler」。
q・c・e の中の < > は &lt; &gt;（faq・standard_text・key は生の < >）。数・名詞の単数（1 Kästchen はよいが 1 Stücke は不可）に注意。
サイトの UI 文言は core.php の 'de'（T と js_text。js の桁区切りは sep = '.'）、学年＋教科の語順は gs()（「Mathe Klasse 3」）、英語の小文字化は lc()。トピックは topics.php の `topic_defs_de()`（ドイツ語の slug 用）。topic.php・topics.php に $de の文言がある

DE / Mathe / Klasse 3
1. zahlen-bis-1000 ✓ 2. zahlen-vergleichen-und-ordnen ✓ 3. runden-und-ueberschlagen ✓ 4. plus-und-minus-bis-1000 ✓ 5. schriftliche-addition ✓ 6. schriftliche-subtraktion ✓ 7. einmaleins ✓
8. multiplizieren-und-dividieren ✓ 9. dividieren-mit-rest ✓ 10. sachaufgaben ✓ 11. geld ✓ 12. laengen ✓ 13. gewichte ✓ 14. uhrzeit-und-zeitspannen ✓
15. koerper-und-figuren ✓ 16. achsensymmetrie ✓ 17. zahlenfolgen-und-muster ✓ 18. diagramme-und-tabellen ✓ 19. wahrscheinlichkeit ✓
DE / Mathe / Klasse 4（Zahlen bis 1 000 000）— 生成スクリプトは `gen_de_mathe_k4_*`（make_unit に grade="klasse-4"）。数詞は de_common.wort、6 桁の位取り表は stellentafel。
長さ・重さ・容量のコンマ表記（3,250 kg）の共通問題は `tools/de_k4_groessen.py`（komma・zwei・lesen・kleiner・groesser・rechnen）。Würfelnetz の折りたたみは K3 の roll・is_net を使う
1. zahlen-bis-1-million ✓ 2. runden-und-ueberschlagen ✓ 3. schriftlich-addieren-und-subtrahieren ✓ 4. schriftliche-multiplikation ✓ 5. schriftliche-division ✓ 6. rechengesetze-und-klammern ✓
7. brueche-im-alltag ✓ 8. sachaufgaben ✓ 9. laengen-mit-komma ✓ 10. gewichte-und-tonnen ✓ 11. rauminhalte ✓ 12. rechnen-mit-geld ✓ 13. zeit-und-kalender ✓ 14. massstab ✓
15. umfang-und-flaecheninhalt ✓ 16. parallel-senkrecht-und-vierecke ✓ 17. wuerfel-und-quader ✓ 18. daten-und-diagramme ✓ 19. kombinatorik-und-wahrscheinlichkeit ✓
DE / Mathe / Klasse 2（Zahlen bis 100。短い文、絵を多く）— 生成スクリプトは `gen_de_mathe_k2_*`（make_unit に grade="klasse-2"）。絵の部品は `tools/de_k2.py`（k_pics の絵にドイツ語の aria-label：hunderterfeld・punktfeld・gruppen・reihe・zahlenstrahl100、DING で物の名前）。
Flächen und Körper・Symmetrie・Diagramme は Klasse 3 の生成スクリプトの問題関数を、モジュールの R を新しい seed に入れ替えて再利用（Diagramme は 100 を超える数を le100 で落とす）
1. zahlen-bis-100 ✓ 2. zahlen-vergleichen-und-ordnen ✓ 3. plus-und-minus-bis-20 ✓ 4. plus-bis-100 ✓ 5. minus-bis-100 ✓ 6. ergaenzen-bis-100 ✓
7. multiplizieren-verstehen ✓ 8. einmaleins-mit-2-5-und-10 ✓ 9. kleines-einmaleins ✓ 10. geteilt-aufteilen-und-verteilen ✓ 11. sachaufgaben ✓ 12. geld ✓
13. laengen ✓ 14. uhrzeit ✓ 15. flaechen-und-koerper ✓ 16. spiegeln-und-symmetrie ✓ 17. zahlenmauern-und-muster ✓ 18. strichlisten-und-diagramme ✓
DE / Mathe / Klasse 1（Zahlen bis 20。とても短い文、ほぼ全問に絵）— 生成スクリプトは `gen_de_mathe_k1_*`（make_unit に grade="klasse-1"）。絵は k_pics（tenframe・dice・bond・box・two_groups・crossed_row・hop_line・pencils・towers・table_scene・box_scene・shelf など）を de_k2.de() でドイツ語の aria-label にして使う。
Formen・Formenmuster は Klasse 2 の生成スクリプトの問題関数を R を入れ替えて再利用。topic の正規表現に verdoppeln（plus-und-minus）・lage-und（geometrie）を足した
1. zahlen-bis-10 ✓ 2. zahlen-bis-20 ✓ 3. zahlen-vergleichen ✓ 4. zerlegen-und-ergaenzen ✓ 5. plus-bis-10 ✓ 6. minus-bis-10 ✓
7. plus-und-minus-bis-20 ✓ 8. plus-und-minus-ueber-die-10 ✓ 9. verdoppeln-und-halbieren ✓ 10. rechengeschichten-und-sachaufgaben ✓ 11. geld ✓
12. laengen-vergleichen-und-messen ✓ 13. uhrzeit-und-tagesablauf ✓ 14. formen-und-koerper ✓ 15. lage-und-richtung ✓ 16. muster-und-zahlenfolgen ✓ 17. strichlisten-und-tabellen ✓
DE / Mathe / Klasse 5（Sekundarstufe I。KMK-Bildungsstandards ESA/MSA 2022、de_common.STD_URL_SEK。make_unit は grade が klasse-5〜10 なら自動で Sek I の URL）— 生成スクリプトは `gen_de_mathe_k5_*`（make_unit に grade="klasse-5"）。
Leitidee に「F」Funktionaler Zusammenhang を足した。負の数を選択肢に入れるときは mcq(…, neg=True)。K3・K4 の問題関数（achsensymmetrie・umfang_und_flaecheninhalt・wuerfel_und_quader・daten_und_diagramme・brueche）を R を入れ替えて再利用。
zahlenstrahl は長いラベルに合わせて左右の余白を広げる。トピック: negative-zahlen・potenzen→zahlen、teiler・primzahl→mal-und-geteilt、strecken・koordinaten・winkel→geometrie、volumen→groessen
1. natuerliche-zahlen-und-stellenwerte ✓ 2. runden-und-schaetzen ✓ 3. negative-zahlen ✓ 4. addieren-und-subtrahieren ✓ 5. multiplizieren-und-dividieren ✓ 6. terme-und-rechengesetze ✓
7. potenzen-und-quadratzahlen ✓ 8. teiler-vielfache-und-primzahlen ✓ 9. brueche-und-anteile ✓ 10. laengen-massen-und-zeit ✓ 11. sachaufgaben-und-kombinatorik ✓ 12. strecken-geraden-und-strahlen ✓
13. koordinatensystem ✓ 14. winkel ✓ 15. achsen-und-punktsymmetrie ✓ 16. flaecheninhalt-und-umfang ✓ 17. volumen-und-oberflaeche-von-quadern ✓ 18. haeufigkeiten-und-diagramme ✓ 19. muster-terme-und-variablen ✓
DE / Mathe / Klasse 6（Sek I）— 生成スクリプトは `gen_de_mathe_k6_*`（make_unit に grade="klasse-6"）、共通部品は `tools/de_k6.py`（bh＝Fraction を HTML の分数に（gemischt=True で帯分数）、dz＝Fraction を正確な小数（コンマ）に、割り切れないときは ValueError、mcq＝誤答が足りないとき None を返して作り直し）。
お金は「%d,%02d €」で表示し、四捨五入は int(x * 100 + 1/2)（round() は偶数丸めになるので使わない）。循環小数は `<span class='ov'>3</span>`。トピック brueche-und-dezimalzahlen（Brüche, Dezimalzahlen und Prozente）を足した。zuordnung・gleichung→muster、kreis・dreieck→geometrie、negative→zahlen
1. brueche-erweitern-und-kuerzen ✓ 2. brueche-vergleichen-und-ordnen ✓ 3. gemischte-zahlen ✓ 4. brueche-addieren-und-subtrahieren ✓ 5. brueche-multiplizieren ✓ 6. brueche-dividieren ✓
7. dezimalzahlen-und-stellenwerte ✓ 8. brueche-und-dezimalzahlen ✓ 9. dezimalzahlen-addieren-und-subtrahieren ✓ 10. dezimalzahlen-multiplizieren-und-dividieren ✓ 11. prozente ✓ 12. rechnen-mit-negativen-zahlen ✓
13. zuordnungen-und-dreisatz ✓ 14. terme-und-gleichungen ✓ 15. kreise-und-kreisdiagramme ✓ 16. dreiecke-und-vierecke ✓ 17. flaecheninhalt-von-parallelogramm-und-dreieck ✓ 18. daten-und-wahrscheinlichkeit ✓
19. sachaufgaben-mit-bruechen-und-dezimalzahlen ✓
DE / Mathe / Klasse 7（Sek I）— 生成スクリプトは `gen_de_mathe_k7_*`（make_unit に grade="klasse-7"）、共通部品は `tools/de_k7.py`（de_k6 の上に mcq（neg=True）・rd（四捨五入）・eur（12,50 €、負は −）・pz（%）・zk）。
負の数は「−」、かっこ付きで（−3）。図はすべて `lg=True`（印刷で大きく。横長の viewBox にすると読みやすい）。トピック: rational→zahlen、zins→brueche-und-dezimalzahlen、terme→muster、prism→geometrie、boxplot→daten-und-zufall
1. rationale-zahlen ✓ 2. rechnen-mit-rationalen-zahlen ✓ 3. prozentrechnung ✓ 4. prozentuale-veraenderung ✓ 5. zinsrechnung ✓ 6. proportionale-und-antiproportionale-zuordnungen ✓
7. terme-umformen ✓ 8. lineare-gleichungen ✓ 9. gleichungen-in-sachaufgaben ✓ 10. winkel-an-geradenkreuzungen ✓ 11. winkelsummen-in-dreiecken-und-vielecken ✓ 12. dreiecke-konstruieren ✓
13. besondere-linien-im-dreieck ✓ 14. flaecheninhalt-von-vierecken ✓ 15. prismen ✓ 16. boxplots-und-kennwerte ✓ 17. wahrscheinlichkeit ✓
DE / Mathe / Klasse 8（Sek I）— 生成スクリプトは `gen_de_mathe_k8_*`（make_unit に grade="klasse-8"）、共通部品は `tools/de_k8.py`（de_k7 の上に expr（項の並び → 2x² − 3x + 5）・gl（y = mx + b）・par（負の数をかっこに）・kosy（座標平面の SVG。目盛りは偶数だけ大きく、lg））。
π は Taschenrechner の値で「auf eine Nachkommastelle」（末尾の 0 も表示）。Definitionsmenge は「D = ℚ ∖ {2}」。連立方程式は「I: …<br>II: …<br>」。トピック lineare-funktionen-und-gleichungssysteme を足した。wurzel→zahlen、ausmultipl・binomisch→muster（mal-und-geteilt の out に ausmultipl）、kongruenz・thales・zylinder→geometrie
1. potenzen-und-zehnerpotenzen ✓ 2. quadratwurzeln-und-reelle-zahlen ✓ 3. ausmultiplizieren-und-ausklammern ✓ 4. binomische-formeln ✓ 5. lineare-funktionen ✓ 6. geradengleichungen-aufstellen ✓
7. lineare-gleichungssysteme-grafisch-loesen ✓ 8. lineare-gleichungssysteme-rechnerisch-loesen ✓ 9. gleichungssysteme-in-sachaufgaben ✓ 10. kongruenzsaetze ✓ 11. satz-des-thales ✓
12. kreisumfang-und-kreisflaeche ✓ 13. zylinder ✓ 14. mehrstufige-zufallsexperimente ✓ 15. bruchterme-und-bruchgleichungen ✓
DE / Mathe / Klasse 9（Sek I）— 生成スクリプトは `gen_de_mathe_k9_*`（make_unit に grade="klasse-9"）、共通部品は `tools/de_k9.py`（de_k8 の上に zahl・zr（四捨五入した小数、末尾の 0 も表示）・qf（ax² + bx + c）・sform（y = a(x − d)² + e、かっこ内はノーブレークスペース）・parabel（放物線の SVG）・rdreieck（直角三角形の SVG、直角は C））。
長さ・お金の答えは分数でなく小数（割り切れないときは zr で丸める）。解の集合は「L = {−5; 3}」。トピック quadratische-funktionen-und-gleichungen を足した（lineare-funktionen-… の out に quadratisch）。potenz・wurzel→zahlen、pythagoras・aehnlich・strahlen・trigonometr・pyramide・kegel・kugel→geometrie、vierfelder→daten-und-zufall
1. potenzgesetze ✓ 2. rechnen-mit-wurzeln ✓ 3. quadratische-funktionen ✓ 4. scheitelpunktform-und-normalform ✓ 5. quadratische-gleichungen ✓ 6. quadratische-gleichungen-in-sachaufgaben ✓
7. satz-des-pythagoras ✓ 8. pythagoras-in-figuren-und-koerpern ✓ 9. aehnlichkeit-und-zentrische-streckung ✓ 10. strahlensaetze ✓ 11. trigonometrie ✓ 12. pyramide-und-kegel ✓ 13. kugel ✓ 14. vierfeldertafeln ✓
DE / Mathe / Klasse 10（Sek I の最後の学年）— 生成スクリプトは `gen_de_mathe_k10_*`（make_unit に grade="klasse-10"）、共通部品は `tools/de_k10.py`（de_k9 の上に pi_txt（π の倍数 → 「3π/2」）・kurve（任意の関数のグラフ。fs=[(f, 色, 名前)]、xr・yr=(lo, hi, 目盛り)、xlab で目盛りの文字を変える（π 単位）、lg））。
Bogenmaß は 180° = π。三角関数の値は「½√3」の形。電卓の答えは小数第 1〜2 位まで（「≈」）。トピック exponential-potenz-und-winkelfunktionen（Exponential-, Potenz- und Winkelfunktionen）を足した（lineare-funktionen-… の out に exponential|potenzfunktion|polynom|sinus、zahlen の out に potenzfunktion）。logarithm→zahlen、bogenmass・einheitskreis・sinussatz→geometrie、erwartungswert→daten-und-zufall
1. exponentialfunktionen ✓ 2. exponentielles-wachstum-und-zerfall ✓ 3. logarithmus ✓ 4. potenzfunktionen ✓ 5. polynomfunktionen ✓ 6. bogenmass-und-kreisausschnitt ✓
7. trigonometrie-am-einheitskreis ✓ 8. sinus-und-kosinusfunktion ✓ 9. sinussatz-und-kosinussatz ✓ 10. erwartungswert ✓
DE / Mathe は Klasse 1〜10 まで完了。次は GDP 順で次の国（日本は国内向けで別サイト。インドは下）

IN / Maths（CBSE 2025-26 / NCERT 教科書の章立て）— country `in`（name「India」、lang en、hreflang en-in）、subject `maths`、grade `class-N`（name「Class N」、N+5〜N+6 歳、unit.php）、A4。生成スクリプトは `gen_in_maths_cN_*`、共通部品は `tools/in_common.py`（sg_sec と同じ API。インドの数の書き方 1,23,456（lakh）・₹（inr）・インドの名前と地名、fv、adopt（他国の生成スクリプトの名前・お金・数をインド式に）、ok（LEAKS で $・GST・Singapore・miles など他国の語を落とす。4 桁以上の小数の選択肢も落とす）、collect は名前と代名詞を除いた問題文で重複を判定、make（CBSE の Unit と NCERT の章番号。q の先頭の図は qfig に入れて後ろへ、図は data-pf='lg'、ハイフンのマイナスを − に））。
1 単元 = NCERT の 1 章（章の名前を slug に）。standard_code は「Class 10, Chapter 4: Quadratic Equations」、domain は CBSE の Unit 名（Number Systems／Algebra／Coordinate Geometry／Geometry／Trigonometry／Mensuration／Statistics and Probability）、standard_text は CBSE シラバスの要約、standard_url は cbseacademic の Maths_Sec_2025-26.pdf。
イギリス式の綴り（colour, metre, factorisation, zeroes, maths）。π は 22/7（半径は 7 の倍数）、segment は π = 3.14・√3 = 1.73。三角比の値は 1/√2・√3/2 の形、高さと距離は 20√3 m の形。topic_gb() に in を入れた。topics.php の topic_defs() に $country === 'in' の調整（real-numbers→factors・exponents、progression→algebra、triangles→congruence-and-similarity、trigonometry・areas-related・surface-areas を shapes から外す）
SG Sec 2–3・US Geometry・AU Year 8 の問題関数を adopt で再利用（連立方程式、因数分解、二次方程式の文章題、相似、接線）

IN / Maths / Class 10（CBSE の board exam の学年）
1. real-numbers ✓ 2. polynomials ✓ 3. pair-of-linear-equations-in-two-variables ✓ 4. quadratic-equations ✓ 5. arithmetic-progressions ✓ 6. triangles ✓ 7. coordinate-geometry ✓
8. introduction-to-trigonometry ✓ 9. some-applications-of-trigonometry ✓ 10. circles ✓ 11. areas-related-to-circles ✓ 12. surface-areas-and-volumes ✓ 13. statistics ✓ 14. probability ✓

IN / Maths / Class 9（CBSE。NCERT の 12 章）— 生成スクリプトは `gen_in_maths_c9_*`。AU Year 8・US Algebra 1・Geometry・SG Sec 1・3 の問題関数を再利用（in_common.gb で米国式の綴り・m∠・CPCTC・HL→RHS などを直す）。
P を点の関数に使うモジュール（gen_sg_maths_s3_angle_properties_of_circles）は adopt しない。Statistics の CBSE Unit は「St」（UNITS）。LEAKS の "None" は「= None」などだけ（"None" という正しい答えを残す）。
度数折れ線の問題は 0 から始まる階級を使わない（仮の階級の階級値が負になるため）。topics.php の in の調整に number-systems→exponents-and-roots、heron→area-and-perimeter、euclid→angles を足した
1. number-systems ✓ 2. polynomials ✓ 3. coordinate-geometry ✓ 4. linear-equations-in-two-variables ✓ 5. introduction-to-euclids-geometry ✓ 6. lines-and-angles ✓
7. triangles ✓ 8. quadrilaterals ✓ 9. circles ✓ 10. herons-formula ✓ 11. surface-areas-and-volumes ✓ 12. statistics ✓

IN / Maths / Class 6–8（NCERT Ganita Prakash。1 単元 = 1 章。Class 7・8 は Part 1・2 に分かれ、章番号はパートごとに 1 から）— 生成スクリプトは `gen_in_maths_c6_*`・`c7_*`・`c8_*`。
in_common.unit(level, part, chapter, slug, sort, strand, …, spec, R) で作る（part=0 は Class 6、spec は [(セット名, [(maker, 数)])] × 5）。standard_code は「Class 8, Ganita Prakash Part 2, Chapter 1: …」、standard_url は STD_URL_MID（NCERT textbook）、domain は strand N/A/G/M/D（Number／Algebra／Geometry／Mensuration／Data Handling）。sort は Part 1 → Part 2 の通し番号。
unit() は全 maker を mid_ok で包む（MID_LEAKS で surf・backyard・sweets など他国の語を落とす、正解と同じ値の未約分の誤答（5/40 と 1/8）を落とす、a octagon → an octagon）。£ を書く UK の maker は in_common.rs()（£→₹、p→paise）。
UK KS3・AU Year 7–8・SG Sec 1–2・US Geometry、IN Class 9 の statistics（one_bar・one_hist・K）・triangles（ind）、Class 8 number play（one_crypt）、Class 6 prime time（one_common・one_prob）を再利用。topics.php の in の調整に Ganita Prakash の章名（$gp）を足した
Class 6: 1. patterns-in-mathematics ✓ 2. lines-and-angles ✓ 3. number-play ✓ 4. data-handling-and-presentation ✓ 5. prime-time ✓ 6. perimeter-and-area ✓ 7. fractions ✓ 8. playing-with-constructions ✓ 9. symmetry ✓ 10. the-other-side-of-zero ✓
Class 7 Part 1: 1. large-numbers-around-us ✓ 2. arithmetic-expressions ✓ 3. a-peek-beyond-the-point ✓ 4. expressions-using-letter-numbers ✓ 5. parallel-and-intersecting-lines ✓ 6. number-play ✓ 7. a-tale-of-three-intersecting-lines ✓ 8. working-with-fractions ✓
Class 7 Part 2: 1. geometric-twins ✓ 2. operations-with-integers ✓ 3. finding-common-ground ✓ 4. another-peek-beyond-the-point ✓ 5. connecting-the-dots ✓ 6. constructions-and-tilings ✓ 7. finding-the-unknown ✓
Class 8 Part 1: 1. a-square-and-a-cube ✓ 2. power-play ✓ 3. a-story-of-numbers ✓ 4. quadrilaterals ✓ 5. number-play ✓ 6. we-distribute-yet-things-multiply ✓ 7. proportional-reasoning-1 ✓
Class 8 Part 2: 1. fractions-in-disguise ✓ 2. the-baudhayana-pythagoras-theorem ✓ 3. proportional-reasoning-2 ✓ 4. exploring-some-geometric-themes ✓ 5. tales-by-dots-and-lines ✓ 6. algebra-play ✓ 7. area ✓

IN / Maths / Class 1–5（NCERT Joyful Mathematics（Class 1–2）・Maths Mela（Class 3–5）。1 単元 = 1 章）— 生成スクリプトは `gen_in_maths_c1_*`〜`c5_*`、共通部品は `tools/in_prim.py`（ph_common をインド向けにしたもの：インドの名前・地名、us_text（GB_WORDS）でイギリス式の綴り・$/£→₹・cuboid・L と mL・mixed number・Terry Fox Run などの言い換え、in_ok は LEAKS を SVG の文字・aria-label にも使う、collect・run_many・build_sets・finish）とお金の絵 `tools/in_money.py`（1〜20 ルピー硬貨、10〜500 ルピー札。one_name・one_count・one_cmp・one_buy・one_make(lim)）。
in_prim.unit(level, slug, sort, strand, chapter, …, specs, seed, max_num) で作る。specs の部品は `rn(mod("他国の生成スクリプト", seed), "set_x", 数, keep)`（引数を名前から自動で埋める。spots などは rn(..., spots=…) で渡す）と `co(maker, 数)`、数の問題は `num_maker(lo, hi, kinds)`。standard_code は「Class 5, Maths Mela Chapter 9: Coconut Farm」、domain は strand N/G/M/P/D（Numbers and Operations／Shapes and Space／Measurement／Patterns／Data Handling）、standard_url は NCERT textbook。seed は 60N0c（Class N の c 章）。
Class 1–2 は数にカンマなし、Class 3 から 1,000（インド式 1,00,000）。topics.php の in の調整に Class 1–5 の章名（$jm）を足した
Class 1: 1. finding-the-furry-cat ✓ 2. what-is-long-what-is-round ✓ 3. mango-treat ✓ 4. making-10 ✓ 5. how-many ✓ 6. vegetable-farm ✓ 7. linas-family ✓ 8. fun-with-numbers ✓ 9. utsav ✓ 10. how-do-i-spend-my-day ✓ 11. how-many-times ✓ 12. how-much-can-we-spend ✓ 13. so-many-toys ✓
Class 2: 1. a-day-at-the-beach ✓ 2. shapes-around-us ✓ 3. fun-with-numbers ✓ 4. shadow-story ✓ 5. playing-with-lines ✓ 6. decoration-for-festival ✓ 7. ranis-gift ✓ 8. grouping-and-sharing ✓ 9. which-season-is-it ✓ 10. fun-at-the-fair ✓ 11. data-handling ✓
Class 3: 1. whats-in-a-name ✓ 2. toy-joy ✓ 3. double-century ✓ 4. vacation-with-my-nani-maa ✓ 5. fun-with-shapes ✓ 6. house-of-hundreds-1 ✓ 7. raksha-bandhan ✓ 8. fair-share ✓ 9. house-of-hundreds-2 ✓ 10. fun-at-class-party ✓ 11. filling-and-lifting ✓ 12. give-and-take ✓ 13. time-goes-on ✓ 14. the-surajkund-fair ✓
Class 4: 1. shapes-around-us ✓ 2. hide-and-seek ✓ 3. pattern-around-us ✓ 4. thousands-around-us ✓ 5. sharing-and-measuring ✓ 6. measuring-length ✓ 7. the-cleanest-village ✓ 8. weigh-it-pour-it ✓ 9. equal-groups ✓ 10. elephants-tigers-and-leopards ✓ 11. fun-with-symmetry ✓ 12. ticking-clocks-and-turning-calendar ✓ 13. the-transport-museum ✓ 14. data-handling ✓
Class 5: 1. we-the-travellers-1 ✓ 2. fractions ✓ 3. angles-as-turns ✓ 4. we-the-travellers-2 ✓ 5. far-and-near ✓ 6. the-dairy-farm ✓ 7. shapes-and-patterns ✓ 8. weight-and-capacity ✓ 9. coconut-farm ✓ 10. symmetrical-designs ✓ 11. grandmothers-quilt ✓ 12. racing-seconds ✓ 13. animal-jumps ✓ 14. maps-and-locations ✓ 15. data-through-pictures ✓

IN / Maths / Class 11–12（CBSE Senior Secondary 2025-26 / NCERT。1 単元 = 1 章、Class 12 の章番号は Part I・II の通し番号）— 生成スクリプトは `gen_in_maths_c11_*`・`gen_in_maths_c12_*`、共通部品は `tools/in_sr.py`（in_common の上に U()（in_common.unit を level 11・12、part なしで呼ぶ。全 maker を tidy で包み「− −2」→「+ 2」「+ −3」→「− 3」）、use(mod, name, R, pairs)（adopt＋gb＋文字の置き換え。pairs に正規表現も可）、T2（誤答の重複を除く）、poly・xp・sup・pi（π の倍数）・surd・rt（√ の簡約）・frs、ⁿCᵣ の C()・P()、US の <sub>n</sub>C を ⁿC にする NCR）。
standard_code は「Class 12, Chapter 7: Integrals」、standard_url は CBSE SrSec の Maths_SrSec_2025-26.pdf（in_common.STD_URL_SR、level ≥ 11 で自動）、domain は CBSE の Unit（SF Sets and Functions／II Algebra／III Coordinate Geometry／Ca Calculus／VII Statistics and Probability／RF Relations and Functions／V3 Vectors and Three-Dimensional Geometry／LP Linear Programming／Pr Probability）。seed は 9111cc・9121cc。
US Algebra 2・Precalculus・Geometry、TX Algebra II・Precalculus、SG Sec 3–4 の問題関数を use() で再利用（Quadrant II→the second quadrant、ft の問題は落とす）、微積分・ベクトル（î ĵ k̂）・3D・LPP・微分方程式は自前。行列は pc_common.mat／det_h。NCERT の log は自然対数。topics.php の in の調整に calculus（名前を Calculus に）・vectors-and-matrices・coordinates-and-position を足した
Class 11: 1. sets ✓ 2. relations-and-functions ✓ 3. trigonometric-functions ✓ 4. complex-numbers-and-quadratic-equations ✓ 5. linear-inequalities ✓ 6. permutations-and-combinations ✓ 7. binomial-theorem ✓ 8. sequences-and-series ✓ 9. straight-lines ✓ 10. conic-sections ✓ 11. introduction-to-three-dimensional-geometry ✓ 12. limits-and-derivatives ✓ 13. statistics ✓ 14. probability ✓
Class 12: 1. relations-and-functions ✓ 2. inverse-trigonometric-functions ✓ 3. matrices ✓ 4. determinants ✓ 5. continuity-and-differentiability ✓ 6. application-of-derivatives ✓ 7. integrals ✓ 8. application-of-integrals ✓ 9. differential-equations ✓ 10. vector-algebra ✓ 11. three-dimensional-geometry ✓ 12. linear-programming ✓ 13. probability ✓

IN / Maths は Class 1〜12 まで完了。次は GDP 順で次の国

FR / Maths（Programmes 2024 du cycle 2、BO n°41 du 31 octobre 2024、2025 年度から）— country `fr`（name「France」、lang `fr`、hreflang fr-fr）、subject `maths`（Maths）、grade `ce2`（name「CE2」、sort 3、8〜9歳。cp 1・ce1 2・ce2 3・cm1 4・cm2 5、unit.php に年齢あり）、A4。生成スクリプトは `gen_fr_maths_ce2_*`、共通部品は `tools/fr_common.py`（num・dec・eur（3,50 €・45 c）・hm（8 h 15）・dur（1 h 25 min）・fp（: ; ? ! の前にノーブレークスペース。mcq が q と e に自動で使う）・Kids（名前と il/elle）・mcq・mix・lesson（Comment faire → Exemple → Erreurs fréquentes）・make_unit・lettres（数詞）・図：droite・numeration・blocs・barres・argent_svg（€ の硬貨と札）・solide_svg・horloge・posee（筆算）・bande・disque・droite_frac（分数））。
フランス語、tu で話しかける短い文。記号は × と ÷。1 000 以上はノーブレークスペース区切り、小数はコンマ。アポストロフィは ’（まっすぐな ' は使わない）。「de」「que」「à le」の縮約に注意（d’élèves、qu’Ambre、au rond）。
short_title は冠詞なしで大文字始まり（「Fractions」「Addition posée」）。standard_code は「CE2 · Grandeurs et mesures」形式（domain は Nombres, calcul et résolution de problèmes／Grandeurs et mesures／Espace et géométrie／Organisation et gestion des données）、standard_text は要約、standard_url は BO 2024 n°41。
UI 文言は core.php の 'fr'（js の桁区切りはノーブレークスペース、'colon' で「 :」）。トピックは topics.php の `topic_defs_fr()`（nombres・addition-et-soustraction・multiplication-et-division・fractions・problemes・grandeurs-et-mesures・geometrie・donnees）。topic.php・topics.php に $fr の文言。preview.php の大文字は mb_strtoupper（pv_up）
symétrie・solides は DE Klasse 3 の生成スクリプトの関数（grid・mirror・wuerfelnetz・bauplan）を R を入れ替えて使い、文字をフランス語に置き換える

FR / Maths / CE2
1. nombres-jusqu-a-10-000 ✓ 2. comparer-et-ranger-les-nombres ✓ 3. calcul-mental ✓ 4. addition-posee ✓ 5. soustraction-posee ✓ 6. tables-de-multiplication ✓
7. multiplication-posee ✓ 8. division-et-partages ✓ 9. fractions ✓ 10. additionner-et-soustraire-des-fractions ✓ 11. problemes ✓ 12. longueurs-et-perimetres ✓
13. masses-et-contenances ✓ 14. heures-et-durees ✓ 15. monnaie ✓ 16. solides ✓ 17. figures-planes-et-angles-droits ✓ 18. symetrie-axiale ✓
19. se-reperer-et-se-deplacer ✓ 20. tableaux-et-diagrammes ✓

FR / Maths / CM1・CM2（Programmes 2025 du cycle 3、BO n°16 du 17 avril 2025。CM1 は 2025 年度、CM2 は 2026 年度から）— grade `cm1`（sort 4）・`cm2`（sort 5）。
生成スクリプトは `gen_fr_maths_cm1_*` に `build(lv)`（lv = 1 または 2）を書き、`gen_fr_maths_cm2_*` は `build(2)` を呼ぶだけ（seed は 52100 + 100 × lv + 番号）。共通部品は `tools/fr_c3.py`（fr_common の上に dz（整数 → コンマの小数）・lettres_big（999 999 999 までの数詞）・nomfrac（3/4 → trois quarts）・RANGS／RANGP・de（d’élèves）・droite_dec・unit（seo_title を自動、standard_text に「(résumé du programme 2025 du cycle 3)」））。
fr_common.make_unit は cm1・cm2 で standard_url を BO 2025（STD_URL_C3）にし、domain に「P」Proportionnalité と「D」Organisation et gestion de données et probabilités を使う。
範囲：CM1 は 999 999・小数 2 桁・分母 20 まで、CM2 は 999 999 999・小数 3 桁・分母 60 まで。CE2 の生成スクリプトの問題関数（時刻・グラフ・図形・立体・対称）を R を入れ替えて再利用。
set を作ってから list にするときは sorted() してから shuffle（文字列を含む set は実行ごとに順番が変わる）。トピックに nombres-decimaux と algebre-et-proportionnalite を足した
1. nombres（cm1: nombres-jusqu-a-999-999、cm2: nombres-jusqu-a-999-999-999）✓ 2. comparer-encadrer-et-ranger-les-nombres ✓ 3. multiples-et-diviseurs ✓ 4. calcul-mental ✓ 5. addition-et-soustraction-posees ✓
6. multiplication-posee ✓ 7. division（cm1: division-euclidienne、cm2: division-decimale）✓ 8. fractions ✓ 9. comparer-additionner-et-soustraire-des-fractions ✓
10. fraction-d-une-quantite（cm2: fraction-d-une-quantite-et-multiplication）✓ 11. fractions-decimales ✓ 12. nombres-decimaux ✓ 13. egalites-a-trous-et-programmes-de-calcul ✓ 14. problemes ✓
15. proportionnalite ✓ 16. longueurs-et-perimetres ✓ 17. masses-et-contenances ✓ 18. aires ✓ 19. angles ✓ 20. heures-et-durees ✓ 21. figures-planes ✓ 22. symetrie-axiale ✓
23. solides-et-patrons ✓ 24. tableaux-et-graphiques ✓ 25. probabilites ✓

FR / Maths / CP・CE1（Programmes 2024 du cycle 2、BO n°41。CE2 と同じルール）— grade `cp`（sort 1、6〜7歳）・`ce1`（sort 2）。
生成スクリプトは `gen_fr_maths_cp_*` に `build(lv)`（lv = 0 は CP、1 は CE1、seed は 53000 + 100 × lv + 番号）、`gen_fr_maths_ce1_*` は `build(1)` を呼ぶだけ（CE1 だけの 4 単元は自前）。共通部品は `tools/fr_c2.py`（fr_common の上に G・GN、CHOSE（k_pics の絵 → フランス語の名詞と性）、ch・nom・un・le・de、pic（k_pics の SVG にフランス語の aria-label）、pl（1 dizaine / 3 dizaines）、que・de_n（qu’Ambre・d’Ambre）、unit（seo_title を自動、standard_text に「(résumé du programme 2024 du cycle 2)」））。
範囲：CP は 100 まで（計算は 20 まで、2 桁の繰り上がり 1 回まで、お金は整数の €、時刻は heure pile）、CE1 は 999 まで（分数は 1 以下、時刻は quart・demie）。CP はほぼ全問に絵（k_pics・f_common.glasses_svg）。CE2 の生成スクリプトの問題関数（時刻・お金・図形・立体・対称・座標・データ・分数・九九）を R を入れ替えて再利用（CE1 の範囲外は包んで落とす：losange、2 unités、小数 × 整数など）。
トピック：compter→nombres、complements・doubles-et-moities→addition-et-soustraction、tables-d-addition は multiplication の out
CP: 1. nombres-jusqu-a-100 ✓ 2. comparer-et-ranger-les-nombres ✓ 3. compter-et-suites ✓ 4. tables-d-addition ✓ 5. calcul-mental ✓ 6. addition-posee ✓ 7. sens-de-la-soustraction ✓ 8. doubles-et-moities ✓ 9. problemes ✓
10. longueurs ✓ 11. masses-et-contenances ✓ 12. monnaie ✓ 13. lire-l-heure ✓ 14. figures-planes ✓ 15. solides ✓ 16. se-reperer-et-se-deplacer ✓ 17. tableaux-et-diagrammes ✓
CE1: 1. nombres-jusqu-a-1000 ✓ 2. comparer-et-ranger-les-nombres ✓ 3. compter-pair-et-impair ✓ 4. complements-a-la-dizaine-et-a-100 ✓ 5. calcul-mental ✓ 6. addition-posee ✓ 7. soustraction-posee ✓ 8. doubles-et-moities ✓ 9. problemes ✓
10. longueurs-et-perimetres ✓ 11. masses-et-contenances ✓ 12. monnaie ✓ 13. heures-et-durees ✓ 14. figures-planes-et-angles-droits ✓ 15. solides ✓ 16. se-reperer-et-se-deplacer ✓ 17. tableaux-et-diagrammes ✓
18. sens-de-la-multiplication ✓ 19. tables-de-multiplication ✓ 20. fractions ✓ 21. symetrie-axiale ✓

FR / Maths / 6e〜3e（collège。6e は Programme 2025 du cycle 3（BO n°16、2025 年度から）、5e・4e・3e は Programme 2026 du cycle 4（BO 2026 n°10、MENE2602912A））— grade `6e`（sort 6）・`5e`（7）・`4e`（8）・`3e`（9）、unit.php の年齢は 11〜14 歳。
生成スクリプトは `gen_fr_maths_{6e,5e,4e,3e}_*`（seed は 601xx・602xx・603xx・604xx）、共通部品は `tools/fr_c4.py`（fr_common の上に d（Fraction → コンマの小数、割り切れないと ValueError）・dk（桁数を固定）・par（負のときだけかっこ）・fq（Fraction → HTML の分数）・expr（3x − 5）・val・M（正解と同じ値の誤答を落とす mcq(neg=True)）・pl・que・de_n・euro・em（整数の € は ,00 なし）・relabel・figure（三角形などの図：辺の長さ・直角・等しい長さの印。ラベルは外側に）・unit（seo_title と standard_text の末尾を自動））。
fr_common.make_unit：6e は DOMAIN_C3（N/G/E/D/P）と STD_URL_C3、5e〜3e は DOMAIN_C4（N Nombres et calculs／A Calcul littéral et algébrique／F Proportionnalité et fonctions／E Espace et géométrie／D Données et probabilités）と STD_URL_C4。
cycle 4 の新しい programme では素数・素因数分解を扱わない（3e は「diviseurs communs」と「plus grand diviseur commun」で既約分数）。3e の四分位数は collège の定義（Q1 は ⌈n/4⌉ 番目、Q3 は ⌈3n/4⌉ 番目の値）。
ベクトルは `<span class='vec'>AB</span>`（矢印は ws.css・ws-print.css の .vec）。式は改行されないよう NB でつなぐ。図の辺の長さが重なる配置（Thalès）は数を図に書かず問題文に書く。
トピック：nombres-relatifs・puissances-et-racines・calcul-litteral-et-equations・fonctions を足した（topic_defs_fr()）。geometrie に milieu・cone・reperage、donnees に statistique、algebre の ratio は (^|-)ratios?(-|$)（operations の誤一致を避ける）
FR / Maths / 6e: 1. nombres-entiers-et-decimaux ✓ 2. comparer-ranger-et-arrondir ✓ 3. addition-et-soustraction-de-decimaux ✓ 4. multiplication-de-decimaux ✓ 5. division ✓ 6. multiples-diviseurs-et-criteres ✓ 7. priorites-operatoires ✓ 8. fractions-et-nombres-mixtes ✓ 9. calculer-avec-des-fractions ✓ 10. proportionnalite-et-pourcentages ✓ 11. agrandissements-reductions-et-echelles ✓ 12. schemas-en-barres-et-balances ✓ 13. droites-paralleles-et-perpendiculaires ✓ 14. angles ✓ 15. mediatrice-et-cercle ✓ 16. triangles-et-quadrilateres ✓ 17. perimetres-et-aires ✓ 18. volumes ✓ 19. solides-et-patrons ✓ 20. durees ✓ 21. donnees-et-diagrammes ✓ 22. probabilites ✓
FR / Maths / 5e: 1. nombres-relatifs ✓ 2. additionner-et-soustraire-des-relatifs ✓ 3. comparer-additionner-et-soustraire-des-fractions ✓ 4. enchainements-d-operations ✓ 5. carres-et-cubes ✓ 6. calcul-litteral ✓ 7. premieres-equations ✓ 8. proportionnalite ✓ 9. pourcentages-et-proportions ✓ 10. fonctions-tableaux-et-graphiques ✓ 11. reperage-dans-le-plan ✓ 12. symetrie-centrale ✓ 13. angles-et-parallelisme ✓ 14. triangles ✓ 15. parallelogrammes ✓ 16. aires ✓ 17. volumes-et-conversions ✓ 18. statistiques ✓ 19. probabilites ✓
FR / Maths / 4e: 1. multiplier-et-diviser-des-relatifs ✓ 2. operations-sur-les-fractions ✓ 3. puissances ✓ 4. racine-carree ✓ 5. developper-et-factoriser ✓ 6. equations ✓ 7. programmes-de-calcul ✓ 8. proportionnalite-et-ratios ✓ 9. pourcentages-et-coefficients-multiplicateurs ✓ 10. fonctions-et-representations-graphiques ✓ 11. translations ✓ 12. droite-des-milieux ✓ 13. theoreme-de-pythagore ✓ 14. reciproque-et-contraposee-de-pythagore ✓ 15. cercle-circonscrit-au-triangle-rectangle ✓ 16. pyramides-et-cones ✓ 17. statistiques ✓ 18. probabilites ✓
FR / Maths / 3e（brevet）: 1. fractions-irreductibles-et-diviseurs ✓ 2. puissances-et-notation-scientifique ✓ 3. racines-carrees-et-equation-x2-a ✓ 4. developper-et-factoriser ✓ 5. identites-remarquables ✓ 6. equations-produit-nul-et-inequations ✓ 7. pourcentages-ratios-et-echelles ✓ 8. fonctions-image-et-antecedent ✓ 9. fonctions-lineaires-et-affines ✓ 10. theoreme-de-thales ✓ 11. trigonometrie ✓ 12. vecteurs-et-translations ✓ 13. sphere-et-sections ✓ 14. volumes ✓ 15. statistiques ✓ 16. probabilites ✓

FR / Maths / Seconde（lycée。Programme 2026 de seconde générale et technologique、BO 2026 n°14、MENE2602914A）— grade `seconde`（sort 10、15歳）。生成スクリプトは `gen_fr_maths_seconde_*`（seed は 605xx）、共通部品は fr_c4（unit の standard_text 末尾は「(résumé du programme 2026 de seconde)」）。
fr_common.make_unit は seconde で DOMAIN_LY（N Nombres et calculs, algèbre／G Géométrie／F Fonctions／S Statistiques et probabilités／P Algorithmique et programmation）と STD_URL_LY。
連立方程式は `<span class='sys'>式1<br>式2</span>`、Python のコードは `<span class='code'>…<br>…</span>`（字下げは NB、< > は &lt; &gt;、文字列はシングルクォート。ws.css・ws-print.css）。符号表・変化表は生成スクリプト内の自前 SVG。
トピック：valeur-absolue→nombres、arithmetique→multiplication-et-division、systeme・signes→calcul-litteral-et-equations、variations-et-extremums→fonctions、colinearite→geometrie、echantillon→donnees。algorithmique-et-python はトピックなし
1. arithmetique ✓ 2. nombres-reels-et-intervalles ✓ 3. valeur-absolue-et-encadrements ✓ 4. puissances-et-racines-carrees ✓ 5. calcul-litteral ✓ 6. equations-et-inequations ✓ 7. tableaux-de-signes ✓
8. fonctions-generalites ✓ 9. fonctions-de-reference ✓ 10. variations-et-extremums ✓ 11. fonctions-affines ✓ 12. vecteurs ✓ 13. coordonnees-et-colinearite ✓ 14. equations-de-droites ✓
15. systemes-lineaires ✓ 16. geometrie-plane ✓ 17. pourcentages-et-evolutions ✓ 18. statistiques ✓ 19. probabilites ✓ 20. echantillonnage ✓ 21. algorithmique-et-python ✓

FR / Maths / Première（spécialité。Programme 2026 de spécialité de première、BO 2026 n°14、MENE2602917A、2026 年度から）— grade `premiere`（name「Première」、sort 11、16歳）。生成スクリプトは `gen_fr_maths_premiere_*`（seed は 606xx）、共通部品は `tools/fr_ly1.py`（fr_c4 の上に E・nz・P2（ax² + bx + c）・sq（√ の簡約）・pit／pif（π の倍数、pif は HTML の分数）・trig_val（cos・sin の値の正確な文字列）・FR・U（u<sub>n</sub>）・vtab（変化表、dsig で f′ の符号の行）・arbre（重み付き樹形図）・code（Python）・loi（確率分布の表）・kurve・kosy）。
fr_ly1.M は「(x)(」を「x(」に直し、「Voici la loi de X :表 …」は問題文を先にする。環境変数 FRLY_WARN=1 で実行すると、誤答が足りず mcq が数字をずらして補った問題を FILL: で表示する（数字以外の答えで出たら誤答を足す）。
fr_common.make_unit は premiere で DOMAIN_1（A Algèbre／F Analyse／G Géométrie／S Probabilités et statistiques／P Algorithmique et programmation／L Vocabulaire ensembliste et logique）と STD_URL_1、standard_code は「Première spécialité · Analyse」。key_big・key_sub はプレーンテキスト（u(n)、q^n、e^(kt) と書く）。
トピック：suites（Suites numériques）・second-degre・derivation を足した。exponentiel・deriv→fonctions、scalaire・kashi→geometrie、aleatoire・variance→donnees、multiplication-et-division の out に suite。ensembles-et-logique・listes-en-python はトピックなし。
preview.php の pv_wrap の省略ループが末尾の空白で止まらなくなる不具合を直した（変化がなければ抜ける）
1. ensembles-et-logique ✓ 2. suites-numeriques ✓ 3. suites-arithmetiques ✓ 4. suites-geometriques ✓ 5. sommes-et-limites-de-suites ✓ 6. forme-canonique-et-sommet ✓ 7. equations-du-second-degre ✓ 8. signe-du-second-degre ✓
9. nombre-derive-et-tangente ✓ 10. fonctions-derivees ✓ 11. derivee-et-variations ✓ 12. fonction-exponentielle ✓ 13. croissance-et-decroissance-exponentielles ✓ 14. cercle-trigonometrique-et-radian ✓ 15. fonctions-cosinus-et-sinus ✓
16. produit-scalaire ✓ 17. al-kashi-et-applications-du-produit-scalaire ✓ 18. vecteur-normal-et-equations-de-droites ✓ 19. equations-de-cercles-et-paraboles ✓
20. probabilites-conditionnelles ✓ 21. independance-et-probabilites-totales ✓ 22. variables-aleatoires-et-esperance ✓ 23. variance-et-ecart-type ✓ 24. listes-en-python ✓

FR / Maths は CP〜première まで完了。次は terminale（spécialité、Programme 2026 は 2027 年度から。BO 2026 n°14 MENE2602919A）か、GDP 順で次の国

IT / Matematica（Indicazioni nazionali per il curricolo。新しい Indicazioni は DM 9 dicembre 2025 n. 221（GU n. 21 del 27/01/2026）、2026/27 年度にクラス 1 から、上の学年は 2012 年版（DM 254/2012）が移行期間中も有効）— country `it`（name「Italia」、lang `it`、hreflang it-it）、subject `matematica`（Matematica）、grade `classe-N`（name「Classe terza」など、classe-prima 6〜7 歳。unit.php に年齢あり）、A4。
生成スクリプトは `gen_it_matematica_c3_*`（seed は 7030N）、共通部品は `tools/it_common.py`（num（4 桁はそのまま 1000、5 桁以上はノーブレークスペース 12 000）・dec（コンマ 2,5）・eur（3,50 €、c=True で 50 cent）・ora（8:15）・dur（1 h 25 min）・pl（1 matita / 3 matite）・Kids（名前と lui/lei）・mcq・lesson（Come si fa → Esempio → Errori frequenti。examples は (q, steps, ans) のタプル）・make_unit（seo_title と standard_code「Classe terza · Numeri」と standard_text の末尾を自動）・lettere（9999 までの数詞）・図：retta・blocchi・tabella_valore（h da u）・istogramma・soldi_svg（硬貨は「10 c」）・solido_svg・orologio・colonna（筆算）・striscia・cerchio）。
イタリア語、tu で話しかける短い文。記号は × と :（割り算）。余りは「23 : 5 = 4 con resto 3」。位は h, da, u（uk）。単位は m, dm, cm, mm, dam, hm, km、kg, hg, dag, g、l, dl, cl, ml。peso lordo / netto / tara。
domain は N Numeri／S Spazio e figure／M Misure／D Relazioni, dati e previsioni／P Problemi、standard_url は MIM の curricolo PDF。q・c・e の中の < > は &lt; &gt;（faq・standard_text・key は生の < >）。環境変数 IT_WARN=1 で、誤答が足りず数字をずらして補った問題を FILL: で表示する。
多くの単元は FR CE2 の生成スクリプトの図（règle・balance・verre doseur・figures・grille・robot）と DE Klasse 3（Würfelnetz・Bauplan・Achsensymmetrie）の問題関数を、モジュールの R を入れ替え、文をイタリア語にして再利用。
UI 文言は core.php の 'it'、トピックは topics.php の `topic_defs_it()`（numeri・addizione-e-sottrazione・moltiplicazione-e-divisione・frazioni-e-decimali・problemi・misure・geometria・dati-e-probabilita）。topic.php・topics.php に $it の文言

IT / Matematica / Classe terza
1. numeri-fino-a-1000 ✓ 2. confrontare-e-ordinare-i-numeri ✓ 3. calcolo-mentale ✓ 4. addizioni-in-colonna ✓ 5. sottrazioni-in-colonna ✓ 6. tabelline ✓ 7. moltiplicazioni-in-colonna ✓
8. divisioni ✓ 9. moltiplicare-e-dividere-per-10-100-1000 ✓ 10. frazioni ✓ 11. numeri-decimali ✓ 12. problemi ✓ 13. misure-di-lunghezza ✓ 14. peso-e-capacita ✓
15. euro ✓ 16. orologio-e-tempo ✓ 17. linee-e-angoli ✓ 18. figure-piane-e-perimetro ✓ 19. solidi ✓ 20. simmetria-e-percorsi ✓ 21. dati-e-probabilita ✓

IT / Matematica / Classe quinta（INVALSI の学年。数は 10 億まで、小数は 1000 分の 1 まで、負の数は「−」（mcq(…, neg=True)））— 生成スクリプトは `gen_it_matematica_c5_*`（seed は 7050N）。make_unit は classe-quarta・quinta で standard_text の末尾を「al termine della classe quinta」に
1. grandi-numeri ✓ 2. numeri-relativi ✓ 3. numeri-romani ✓ 4. numeri-decimali ✓ 5. addizioni-e-sottrazioni-con-i-decimali ✓ 6. moltiplicazioni-e-divisioni-con-i-decimali ✓ 7. divisioni-con-due-cifre-al-divisore ✓
8. multipli-divisori-e-numeri-primi ✓ 9. potenze ✓ 10. espressioni ✓ 11. frazioni ✓ 12. operazioni-con-le-frazioni ✓ 13. percentuali ✓ 14. compravendita ✓ 15. problemi ✓
16. misure-ed-equivalenze ✓ 17. perimetro-e-area-dei-poligoni ✓ 18. cerchio-e-circonferenza ✓ 19. solidi-e-volume ✓ 20. trasformazioni-e-piano-cartesiano ✓ 21. statistica-e-probabilita ✓

IT / Matematica / Classe seconda（INVALSI の学年。100 まで。文は短く、絵を多く）— 生成スクリプトは `gen_it_matematica_c2_*`（seed は 7020N）、絵の部品は `tools/it_c2.py`（k_pics・de_k2 の絵にイタリア語の aria-label：COSE（名詞の単数・複数・性）、cose・nome・un_・quanti（Quanti/Quante）、riga・gruppi・tabella100・punti・retta100・mucchio）。
線・図形・立体・対称・データは classe terza の生成スクリプトの問題関数を R を入れ替えて再利用
1. numeri-fino-a-100 ✓ 2. confrontare-e-ordinare-i-numeri ✓ 3. pari-e-dispari ✓ 4. addizioni-entro-100 ✓ 5. sottrazioni-entro-100 ✓ 6. addizioni-e-sottrazioni-in-colonna ✓ 7. la-moltiplicazione ✓
8. tabelline ✓ 9. la-divisione ✓ 10. doppio-e-meta ✓ 11. problemi ✓ 12. euro ✓ 13. orologio-e-calendario ✓ 14. misure ✓ 15. linee-e-regioni ✓ 16. figure-e-solidi ✓ 17. simmetria-e-percorsi ✓ 18. classificazioni-e-dati ✓

トピック（topic_defs_it）：potenze・pari-e-dispari・espressioni→numeri、doppio→moltiplicazione、percentuali→frazioni-e-decimali、compravendita→problemi、cerchio・trasformazioni・cartesiano→geometria

IT / Matematica / Classe quarta（数は 999 999 まで、小数は 1000 分の 1 まで）— 生成スクリプトは `gen_it_matematica_c4_*`（seed は 7040N）。多くは classe terza・quinta の生成スクリプトの問題関数を R と K（Kids(R)）を入れ替えて再利用。
角度の図（goniometro・angle_fig）と三角形・四角形の図（tri_pts・shape_svg。辺の印 ticks、直角 rights）は `gen_au_maths_y5_angles` を relabel で使う。トピック：multipli→numeri、triangol・quadrilater・isometri・area→geometria
1. numeri-entro-il-milione ✓ 2. addizioni-e-sottrazioni ✓ 3. moltiplicazioni ✓ 4. divisioni ✓ 5. multipli-e-divisori ✓ 6. frazioni ✓ 7. frazione-di-un-numero ✓
8. numeri-decimali ✓ 9. operazioni-con-i-decimali ✓ 10. problemi ✓ 11. misure ✓ 12. compravendita ✓ 13. misure-di-tempo ✓ 14. angoli ✓
15. triangoli ✓ 16. quadrilateri ✓ 17. perimetro ✓ 18. area ✓ 19. isometrie ✓ 20. statistica-e-probabilita ✓

IT / Matematica / Classe prima（20 まで。とても短い文、ほぼ全問に絵）— 生成スクリプトは `gen_it_matematica_c1_*`（seed は 7010N）、絵の部品は `tools/it_c1.py`（k_pics の絵にイタリア語の aria-label：dieci・dado・due（2 つの群と記号）・barrati・scatola・salti・coppia・regoli・carte・retta・piatto・ritmo、num_parola、Q）。
線・図形・位置・測定・時間・分類は classe seconda の生成スクリプトの問題関数を R を入れ替えて再利用（範囲外は包んで落とす）。トピック：amici-del→addizione-e-sottrazione
1. numeri-fino-a-10 ✓ 2. numeri-fino-a-20 ✓ 3. confrontare-i-numeri ✓ 4. amici-del-10 ✓ 5. addizioni-entro-10 ✓ 6. sottrazioni-entro-10 ✓ 7. addizioni-e-sottrazioni-entro-20 ✓
8. problemi ✓ 9. euro ✓ 10. misure ✓ 11. il-tempo ✓ 12. linee-e-figure ✓ 13. posizioni-e-percorsi ✓ 14. ritmi-classificazioni-e-dati ✓

IT / Matematica / Prima media・Seconda media（scuola secondaria di primo grado。grade は prima-media（sort 6）・seconda-media（7）・terza-media（8）、unit.php に年齢あり）— 生成スクリプトは `gen_it_matematica_m1_*`・`m2_*`（seed は 711NN・712NN）、共通部品は `tools/it_media.py`（d（コンマの小数、割り切れないと ValueError）・dk・fq（分数の HTML）・par・sgn・expr・val、M（正解と同じ値の誤答を落とす mcq(neg=True)、IT_WARN=1 で FILL）、W（None・負の数・重複を落とす）、L（lesson）、unit（standard_text の末尾は「al termine della classe terza della scuola secondaria di primo grado」）、figure（fr_c4）・kosy（de_k8）・kurve（de_k10））。
domain に F Relazioni e funzioni を足した。座標は「P(3; 5)」（セミコロン）。seconda media の piano cartesiano は第 1 象限だけ（負の数は terza）。π・√2・√3 は 3,14・1,414・0,866 で計算。
トピック（topic_defs_it）：mcd・insiemi・radice→numeri、segmenti・rette・pitagora・similitudine→geometria、statistic→dati-e-probabilita（out に cartesian）。proporzioni-e-funzioni（rapporti・proporzional・retta・funzion）と calcolo-letterale-ed-equazioni（letterale・monomi・polinomi・equazion）を足した
Prima media: 1. insiemi ✓ 2. numeri-naturali-e-operazioni ✓ 4. potenze ✓ 5. espressioni ✓ 6. divisibilita-e-numeri-primi ✓ 7. mcd-e-mcm ✓ 8. frazioni ✓ 9. operazioni-con-le-frazioni ✓ 10. enti-geometrici-e-segmenti ✓ 11. angoli ✓ 12. rette-parallele-e-perpendicolari ✓ 13. triangoli ✓ 14. poligoni-e-quadrilateri ✓ 15. statistica ✓
Seconda media: 1. numeri-decimali-e-frazioni ✓ 2. radice-quadrata ✓ 3. rapporti-e-proporzioni ✓ 4. proporzionalita-diretta-e-inversa ✓ 5. percentuali ✓ 6. piano-cartesiano-e-grafici ✓ 7. area-dei-poligoni ✓ 8. teorema-di-pitagora ✓ 9. applicazioni-del-teorema-di-pitagora ✓ 10. trasformazioni-isometriche ✓ 11. similitudine-e-talete ✓ 12. probabilita ✓

Terza media（gen_it_matematica_m3_*、seed 713NN。単項式・多項式の部品は `tools/it_m3.py`（mono・P・show・mul・add・evalp）。負の数は sgn で「+3／−3」。π の答えは「10π cm」の形か 3,14）: 1. numeri-relativi ✓ 2. operazioni-con-i-numeri-relativi ✓ 3. calcolo-letterale-monomi ✓ 4. polinomi-e-prodotti-notevoli ✓ 5. equazioni-di-primo-grado ✓ 6. problemi-con-le-equazioni ✓ 7. piano-cartesiano-e-retta ✓ 8. circonferenza-e-cerchio ✓ 9. lunghezza-della-circonferenza-e-area-del-cerchio ✓ 10. poliedri-prismi-e-piramidi ✓ 11. solidi-di-rotazione ✓ 12. probabilita-di-eventi-composti ✓ 13. statistica-e-indici-di-posizione ✓
misure の out に circonferenz（lunghezza-della-circonferenza は geometria だけ）

IT / Matematica / Liceo（liceo scientifico。Indicazioni nazionali per i licei、DM 211/2010。新しい Indicazioni は 2027/28 から）— grade は prima-liceo（sort 9、14歳）〜quinta-liceo（13、18歳、esame di Stato）。生成スクリプトは `gen_it_matematica_l1_*`〜`l5_*`（seed は 72NNN：72100 + 100 × (学年 − 1) + 番号）、共通部品は `tools/it_liceo.py`（it_media・it_m3 の上に nz・E・P2（ax² + bx + c）・poly（[a_n, …, a_0] → 多項式）・ex・sol（x = a ∨ x = b）・vtab・albero・code・uniq・isq・surd・simp_root、show（次数順）、W（None と重複を落とす。負の数も残す、値のまま返す）・WP（正の数だけ）、fr_ly1 の sq・pit・pif・FR・trig_val）。
it_common.make_unit は grade が -liceo で standard_url を STD_URL_LICEI（Gazzetta Ufficiale の DM 211/2010）、standard_text の末尾を「(sintesi degli obiettivi specifici di apprendimento di matematica del liceo scientifico, …)」に。unit.php は liceo の学年で「Indicazioni nazionali per i licei」と表示。domain は A Aritmetica e algebra／G Geometria／F Relazioni e funzioni／Q Dati e previsioni。
答えの「x − −3」「+ −2」は poly・fq で作り、生成後に「+ −」「− −」を grep で確かめる。Fraction を % d に渡さない（fq）。set を回すときは sorted()。生成スクリプトの終了コードを確かめる（パイプで grep すると失敗が見えない）
トピック（topic_defs_it）：geometria-analitica（cartesian・fasci-di-rette・parabola・ellisse・iperbole・geometria-analitica）、esponenziali-e-logaritmi、goniometria-e-trigonometria、analisi（Limiti, derivate e integrali：limiti・continuita・asintot・derivat・massimi・studio-di-funzione・integral・differenzial・dominio-e-segno）を足した。proporzioni-e-funzioni・calcolo-letterale-ed-equazioni の out で重ならないようにしてある
Prima liceo: 1. insiemi-e-logica ✓ 2. numeri-naturali-interi-e-razionali ✓ 3. monomi-e-polinomi ✓ 4. prodotti-notevoli ✓ 5. scomposizione-in-fattori ✓ 6. divisione-tra-polinomi-e-ruffini ✓ 7. equazioni-lineari ✓ 8. disequazioni-lineari ✓ 9. funzioni ✓ 10. statistica ✓ 11. triangoli-e-criteri-di-congruenza ✓ 12. rette-perpendicolari-e-parallele ✓
Seconda liceo: 1. frazioni-algebriche ✓ 2. equazioni-fratte-e-letterali ✓ 3. sistemi-lineari ✓ 4. radicali ✓ 5. piano-cartesiano-e-retta ✓ 6. equazioni-di-secondo-grado ✓ 7. disequazioni-di-secondo-grado ✓ 8. parallelogrammi-e-trapezi ✓ 9. circonferenza-e-poligoni-inscritti ✓ 10. equivalenza-e-teoremi-di-euclide-e-pitagora ✓ 11. similitudine-e-teorema-di-talete ✓ 12. probabilita ✓
Terza liceo: 1. equazioni-e-disequazioni-con-valore-assoluto-e-irrazionali ✓ 2. funzioni-e-loro-proprieta ✓ 3. successioni-e-progressioni ✓ 4. retta-e-fasci-di-rette ✓ 5. parabola ✓ 6. circonferenza-nel-piano-cartesiano ✓ 7. ellisse ✓ 8. iperbole ✓ 9. trasformazioni-geometriche ✓ 10. statistica-bivariata ✓
Quarta liceo: 1. funzione-esponenziale ✓ 2. logaritmi ✓ 3. equazioni-esponenziali-e-logaritmiche ✓ 4. goniometria ✓ 5. formule-goniometriche ✓ 6. equazioni-goniometriche ✓ 7. trigonometria ✓ 8. numeri-complessi ✓ 9. geometria-nello-spazio ✓ 10. calcolo-combinatorio ✓ 11. probabilita-condizionata-e-bayes ✓
Quinta liceo: 1. geometria-analitica-nello-spazio ✓ 2. dominio-e-segno-di-una-funzione ✓ 3. limiti ✓ 4. forme-indeterminate-e-limiti-notevoli ✓ 5. continuita-e-asintoti ✓ 6. derivate ✓ 7. teoremi-del-calcolo-differenziale ✓ 8. massimi-minimi-e-flessi ✓ 9. studio-di-funzione ✓ 10. integrali-indefiniti ✓ 11. integrali-definiti-e-aree ✓ 12. equazioni-differenziali ✓ 13. distribuzioni-di-probabilita ✓

IT / Matematica は classe prima〜quinta liceo まで完了。新しい Indicazioni per i licei が出たら（2027/28）単元を見直す。次は GDP 順で次の国（ロシアは Google 広告が配信されないので後回し）

BR / Matemática（BNCC、Base Nacional Comum Curricular）— country `br`（name「Brasil」、lang `pt-BR`、hreflang pt-br、standard「BNCC」）、subject `matematica`（Matemática）、grade `N-ano`（name「3º ano」、1º ano = 6〜7 歳、unit.php）、A4。
生成スクリプトは `gen_br_matematica_N_*`（seed は 80N0c、絵の部品の R は 809xx）、共通部品は `tools/br_common.py`（num（1.000、4.536：4 桁から点で区切る）・dec（コンマ）・reais（R$ 3,50、c=True で 50 centavos）・hora（8h、8h15）・dur（1 h 25 min）・pl・Kids（名前と ela/ele）・mcq（BR_WARN=1 で FILL、R$ は 1 レアル単位で補う）・lesson（Como pensar → Exemplo → Erros comuns）・make_unit（codes に BNCC の EF03MA05 などを渡し standard_code に、seo_title「Adição – 3º ano: atividades de matemática com gabarito」）・extenso（9.999 までの数詞）・図：reta・material_dourado・quadro_valor（UM C D U）・grafico・dinheiro_svg（硬貨 5〜50 centavos と 1 real、紙幣 R$ 2〜200）・solido_svg・relogio・digital・armada（conta armada、点を外す）・faixa・disco・arranjo・grupos・linha・COISAS（k_pics の物の名前と性））。
fr_common の絵の数（1 000）は brn() で 1.000 に。ポルトガル語、você で話しかける短い文。記号は × と ÷、余りは「23 ÷ 4 = 5 e resto 3」。単位は m・cm・mm、kg・g・mg、L・mL。お金の文は reais() を使う（"R$ %d" を書かない）。
domain は BNCC のユニダージ・テマチカ（N Números／A Álgebra／G Geometria／M Grandezas e medidas／E Probabilidade e estatística）、standard_url は BNCC の PDF。q の文に答えを決める情報（数・選択肢）を入れる（同じ文の問題は重複扱いで作れない）。誤答のリストを [:3] で切らない（mcq が重複を落としてから 3 つ取る）。
UI 文言は core.php の 'pt-BR'（js の桁区切りは '.'）、トピックは topics.php の `topic_defs_br()`（numeros・adicao-e-subtracao・multiplicacao-e-divisao・geometria・grandezas-e-medidas・probabilidade-e-estatistica）、topic.php・topics.php に $pt の文言

BR / Matemática / 3º ano（BNCC EF03MA01〜EF03MA28）
1. numeros-ate-9999 ✓ 2. comparar-e-ordenar-numeros ✓ 3. calculo-mental ✓ 4. adicao ✓ 5. subtracao ✓ 6. problemas-de-adicao-e-subtracao ✓ 7. tabuada ✓ 8. multiplicacao ✓
9. divisao ✓ 10. metade-terca-e-quarta-parte ✓ 11. sequencias-numericas ✓ 12. igualdade ✓ 13. localizacao-e-trajetos ✓ 14. figuras-geometricas-espaciais ✓ 15. figuras-geometricas-planas ✓
16. medidas-de-comprimento ✓ 17. massa-e-capacidade ✓ 18. area ✓ 19. horas-e-intervalos-de-tempo ✓ 20. sistema-monetario ✓ 21. tabelas-e-graficos ✓ 22. probabilidade ✓

BR / Matemática / 5º ano（SAEB の学年。999.999 まで、小数は milésimos まで、分数・porcentagem は 10%・25%・50%・75%・100%）— 生成スクリプトは `gen_br_matematica_5_*`（seed は 805NN、make_unit に grade="5-ano"）。
br_common に dz（整数 × 10^−k → コンマの小数）・quadro_decimal（U, d c m）・reta_frac を足し、quadro_valor は 6 列（CM DM UM C D U）まで。3º ano の生成スクリプト（probabilidade の saco・roleta、figuras espaciais の planificações、DE の bauplan）を R を入れ替えて再利用。
トピック fracoes-e-decimais（Frações, decimais e porcentagem）を足した。contagem→probabilidade-e-estatistica、proporcionalidade→multiplicacao-e-divisao、cartesiano・ampliacao→geometria、perimetro・volume→grandezas-e-medidas
1. numeros-ate-centenas-de-milhar ✓ 2. numeros-decimais ✓ 3. fracoes ✓ 4. fracoes-equivalentes ✓ 5. comparar-e-ordenar-fracoes-e-decimais ✓ 6. porcentagem ✓ 7. adicao-e-subtracao ✓ 8. multiplicacao ✓
9. divisao ✓ 10. multiplicacao-e-divisao-com-decimais ✓ 11. problemas-de-contagem ✓ 12. igualdade-e-termo-desconhecido ✓ 13. proporcionalidade-e-partilha ✓ 14. plano-cartesiano ✓
15. figuras-espaciais-e-planificacoes ✓ 16. poligonos ✓ 17. ampliacao-e-reducao ✓ 18. medidas-e-transformacoes ✓ 19. perimetro-e-area ✓ 20. volume ✓ 21. probabilidade ✓ 22. tabelas-e-graficos ✓

BR / Matemática / 4º ano（BNCC EF04MA01〜EF04MA28。99.999 まで、小数は centésimos まで、分数は単位分数、確率は分数なし）— 生成スクリプトは `gen_br_matematica_4_*`（seed は 804NN、再利用する他学年のモジュールの R は 809NN、make_unit に grade="4-ano"）。
br_common に use(モジュール名, seed, 関数名…, preds=…)（他学年の生成スクリプトを import して R を入れ替え、問題関数を返す）・keep・lim(最大の数, 小数の桁)・nums_in を足した。多くの単元は 3º・5º ano の問題関数を use で再利用（同じ関数を 2 回使うときは同じ seed）。
simetria は DE Klasse 3 の Achsensymmetrie の図を使う。5º poligonos の角度の図は左にはみ出さないように頂点を右へ寄せた。トピック：decimos→fracoes-e-decimais、relacoes-entre・propriedades・multiplos→multiplicacao-e-divisao、prismas→geometria、temperatura→grandezas-e-medidas
1. numeros-ate-dezenas-de-milhar ✓ 2. adicao-e-subtracao ✓ 3. relacoes-entre-as-operacoes ✓ 4. propriedades-e-calculo-mental ✓ 5. multiplicacao ✓ 6. divisao ✓ 7. problemas-de-contagem ✓ 8. fracoes-unitarias ✓
9. decimos-e-centesimos ✓ 10. sequencias-e-multiplos ✓ 11. igualdade ✓ 12. localizacao-e-movimentacao ✓ 13. prismas-e-piramides ✓ 14. angulos-retos-e-nao-retos ✓ 15. simetria-de-reflexao ✓
16. medidas-de-comprimento-massa-e-capacidade ✓ 17. area ✓ 18. horas-e-intervalos-de-tempo ✓ 19. temperatura ✓ 20. sistema-monetario ✓ 21. probabilidade ✓ 22. tabelas-e-graficos ✓

BR / Matemática / 2º ano（BNCC EF02MA01〜EF02MA23。1.000 まで。文は短く、絵を多く）— 生成スクリプトは `gen_br_matematica_2_*`（seed は 802NN、use で再利用する 3º のモジュールの R は 809NN（80901〜80915））、共通部品は `tools/br_2.py`（parts・wrong（3 桁の誤答）・md（cubo grande なしの material dourado）・cdu、padrao（f_common.pattern_svg に図形と色の名前）・opcoes・FORMAS・CORES、mes_svg（月のカレンダー、日曜始まり、marks で丸）・dia_semana・DIAS・MESES）。
多くの単元は 3º ano の問題関数を `use(..., preds=(lim(999, 0),))` で再利用。図形の問題では quadrado も retângulo なので、retângulo を問うときに quadrado を出さない。かけ算は 2・3・4・5 だけ、÷ は使わない（metade・terça parte は「2 つ・3 つの等しいグループに分ける」）。
トピック：quantidades→numeros、calendario→grandezas-e-medidas
1. numeros-ate-1000 ✓ 2. comparar-e-ordenar-numeros ✓ 3. compor-e-decompor-numeros ✓ 4. estimar-e-comparar-quantidades ✓ 5. fatos-basicos-de-adicao-e-subtracao ✓ 6. adicao-e-subtracao ✓
7. problemas-de-adicao-e-subtracao ✓ 8. multiplicacao-por-2-3-4-e-5 ✓ 9. dobro-metade-triplo-e-terca-parte ✓ 10. sequencias-numericas ✓ 11. padroes-e-sequencias-repetitivas ✓
12. localizacao-e-trajetos ✓ 13. figuras-geometricas-espaciais ✓ 14. figuras-geometricas-planas ✓ 15. medidas-de-comprimento ✓ 16. massa-e-capacidade ✓ 17. calendario ✓
18. horas-e-intervalos-de-tempo ✓ 19. sistema-monetario ✓ 20. probabilidade ✓ 21. tabelas-e-graficos ✓ 22. pesquisa-e-organizacao-de-dados ✓

BR / Matemática / 1º ano（BNCC EF01MA01〜EF01MA22。100 まで、計算は 20 まで。とても短い文、ほぼ全問に絵）— 生成スクリプトは `gen_br_matematica_1_*`（seed は 801NN、use で再利用する 2º・3º のモジュールの R は 80970〜80988）、共通部品は `tools/br_1.py`（k_pics の絵にポルトガル語の aria-label：fila・espalhados・quadro_dez・dados・dois_grupos・riscados・torres・lapis・ligacao・caixa、nome・quantos・art・fem、EXTENSO・ORD_M）。
多くの単元は 2º ano の問題関数を `use(..., preds=(lim(20 か 100, 0),))` で再利用。女の子の序数は「a 4ª」。トピック：dezenas・ordinais・classificar→numeros、periodos→grandezas-e-medidas
1. numeros-ate-100 ✓ 2. numeros-ordinais ✓ 3. contar-e-estimar-quantidades ✓ 4. comparar-e-ordenar-numeros ✓ 5. dezenas-e-unidades ✓ 6. fatos-basicos-da-adicao ✓ 7. adicao-e-subtracao-ate-20 ✓
8. problemas-de-adicao-e-subtracao ✓ 9. classificar-e-ordenar-objetos ✓ 10. sequencias-e-padroes ✓ 11. localizacao ✓ 12. figuras-geometricas-espaciais ✓ 13. figuras-geometricas-planas ✓
14. comprimento-massa-e-capacidade ✓ 15. periodos-do-dia ✓ 16. calendario-e-datas ✓ 17. sistema-monetario ✓ 18. probabilidade ✓ 19. tabelas-e-graficos ✓ 20. pesquisa ✓

BR / Matemática / 9º ano（SAEB の学年。BNCC EF09MA01〜EF09MA23。負の数は「−」）— 生成スクリプトは `gen_br_matematica_9_*`（seed は 890NN）、共通部品は `tools/br_9.py`（d（Fraction → ブラジル式の小数。places を付けると末尾の 0 を消す、keep=True で残す）・fq・expr・P2・par・sq（√ の簡約）・M（neg=True の mcq、重複と "None" を落とす）・figure（fr_c4）・kosy（de_k8）・paralelas（平行線と横断線の 8 つの角）・circulo（円と中心角・円周角）・formas（三角形などをまとめて描く。辺の文字は各図形の外側）・tri_pts・unit）。
座標の分数は fq（「(5/2, 3)」の形。小数のコンマと座標のコンマが混ざらないように）。vistas-ortogonais は UK Year 9 plans-and-elevations の問題関数（UK.R を入れ替え、文と図の文字をポルトガル語に置換）。トピック algebra-e-funcoes（Álgebra e funções）を足した
1. numeros-reais ✓ 2. potencias-e-radicais ✓ 3. notacao-cientifica ✓ 4. porcentagens-e-juros-compostos ✓ 5. funcoes ✓ 6. razoes-entre-grandezas ✓ 7. grandezas-proporcionais ✓ 8. produtos-notaveis-e-fatoracao ✓
9. equacoes-do-2-grau ✓ 10. angulos-e-retas-paralelas ✓ 11. angulos-na-circunferencia ✓ 12. semelhanca-de-triangulos ✓ 13. relacoes-metricas-no-triangulo-retangulo ✓ 14. teorema-de-pitagoras ✓ 15. poligonos-regulares ✓
16. distancia-e-ponto-medio ✓ 17. vistas-ortogonais ✓ 18. unidades-de-medida-muito-grandes-e-pequenas ✓ 19. volume-de-prismas-e-cilindros ✓ 20. probabilidade ✓ 21. graficos-e-estatistica ✓ 22. pesquisa-amostral ✓

BR / Matemática / 6º ano（BNCC EF06MA01〜EF06MA34）— 生成スクリプトは `gen_br_matematica_6_*`（seed は 860NN、use で再利用する 5º・9º のモジュールの R は 869NN）。共通部品は br_9（unit に grade="6-ano"、bank（[(問, 答, [誤答])] から選ぶ問題関数）・tab・ntab を足した）。
5º の問題関数（figuras espaciais・poligonos・ampliacao・perimetro e area・medidas・probabilidade・tabelas e graficos）と 9º の graficos を use で再利用。5º perimetro-e-area の L 字の図の文字切れを直した。
トピック：arredondamento→numeros（numeros の out に primos）、mmc・operacoes-com-numeros→multiplicacao-e-divisao、retas→geometria、partilha→algebra-e-funcoes（adicao の out に partilha）
1. numeros-naturais-e-sistema-de-numeracao ✓ 2. operacoes-com-numeros-naturais ✓ 3. multiplos-divisores-e-numeros-primos ✓ 4. mmc-e-mdc ✓ 5. fracoes ✓ 6. operacoes-com-fracoes ✓ 7. numeros-decimais ✓
8. operacoes-com-decimais ✓ 9. arredondamento-e-estimativa ✓ 10. porcentagem ✓ 11. igualdade-e-partilha ✓ 12. plano-cartesiano ✓ 13. prismas-e-piramides ✓ 14. poligonos-triangulos-e-quadrilateros ✓
15. ampliacao-e-reducao ✓ 16. retas-paralelas-e-perpendiculares ✓ 17. grandezas-e-medidas ✓ 18. angulos ✓ 19. perimetro-e-area ✓ 20. probabilidade ✓ 21. tabelas-e-graficos ✓

BR / Matemática / 7º ano（BNCC EF07MA01〜EF07MA37）— 生成スクリプトは `gen_br_matematica_7_*`（seed は 870NN、use で再利用する 5º・6º・9º のモジュールの R は 879NN）。
9º の grandezas-proporcionais・angulos-e-retas-paralelas・poligonos-regulares・volume・graficos・pesquisa-amostral、6º の mmc-e-mdc・probabilidade、5º の volume を use で再利用。
トピック：circunferencia→geometria、algebrica・proporcionalidade-direta・^sequencias$→algebra-e-funcoes（numeros の out に ^sequencias$）、media→probabilidade-e-estatistica
1. multiplos-divisores-mmc-e-mdc ✓ 2. numeros-inteiros ✓ 3. operacoes-com-numeros-inteiros ✓ 4. fracoes-e-seus-significados ✓ 5. numeros-racionais ✓ 6. porcentagem-acrescimos-e-descontos ✓ 7. linguagem-algebrica-e-expressoes ✓
8. sequencias ✓ 9. equacoes-do-1-grau ✓ 10. proporcionalidade-direta-e-inversa ✓ 11. transformacoes-no-plano-cartesiano ✓ 12. angulos-e-retas-paralelas ✓ 13. triangulos ✓ 14. poligonos-e-angulos-internos ✓
15. circunferencia-e-comprimento ✓ 16. area-de-figuras-planas ✓ 17. volume-de-blocos-retangulares ✓ 18. probabilidade-e-frequencia ✓ 19. media-e-amplitude ✓ 20. graficos-de-setores-e-pesquisa ✓

BR / Matemática / 8º ano（BNCC EF08MA01〜EF08MA27）— 生成スクリプトは `gen_br_matematica_8_*`（seed は 880NN、use で再利用する 6º・7º・9º のモジュールの R は 889NN）。共通部品は br_9（unit に grade="8-ano"）。
use は問題関数だけを包むので、図の関数（9º volume の cil など）はモジュールを import して直接使う。histograma は graficos-e-classes-de-frequencia の histo、classes は「10 ⊢ 20」。
トピック：radiciacao→numeros、dizimas→fracoes-e-decimais、principio・tendencia→probabilidade-e-estatistica（media は (^|-)media(-|$)、mediatriz に当たらないように）、sequencias-recursivas→algebra-e-funcoes、transformacoes-geometricas・mediatriz→geometria、grandezas-e-medidas の out に tendencia
1. potencias-e-notacao-cientifica ✓ 2. radiciacao ✓ 3. principio-multiplicativo ✓ 4. porcentagens ✓ 5. dizimas-periodicas ✓ 6. expressoes-algebricas-e-polinomios ✓ 7. equacoes-com-duas-incognitas ✓
8. sistemas-de-equacoes ✓ 9. equacoes-do-2-grau-do-tipo-ax2-b ✓ 10. sequencias-recursivas-e-nao-recursivas ✓ 11. grandezas-proporcionais ✓ 12. congruencia-de-triangulos ✓ 13. mediatriz-bissetriz-e-construcoes ✓
14. transformacoes-geometricas ✓ 15. area-de-figuras-planas-e-do-circulo ✓ 16. volume-e-capacidade ✓ 17. probabilidade ✓ 18. graficos-e-classes-de-frequencia ✓ 19. medidas-de-tendencia-central ✓ 20. pesquisa-amostral ✓

BR / Matemática / Ensino Médio（BNCC EM13MAT101〜EM13MAT511。BNCC の EM は学年に分かれていないので、教科書の一般的な配分で 1ª〜3ª série に分ける）— grade `1-serie`・`2-serie`・`3-serie`（name「1ª série」…、sort 10〜12、unit.php で 15〜18 歳と educationalLevel「Ensino Médio」）。
生成スクリプトは `gen_br_matematica_em1_*`（2ª は em2、3ª は em3。seed は 910NN・920NN・930NN、use で再利用する 8º・9º のモジュールの R は 919NN・929NN・939NN）、共通部品は `tools/br_em.py`（br_9・br_common の上に curva（de_k10.kurve、数を 1.000 の形に）・R2（Fraction → R$ 1.234,56）・pc・sg・unit（grade を必ず渡す））。standard_code は EM13MAT のコード、standard_url は BNCC の PDF（EF と同じ）。
key_big・key_sub・faq は生の < >（q・c・e・body は &lt; &gt;）。トピック：funcao・progressao・sistemas-lineares・logaritmos・maximo-e-minimo→algebra-e-funcoes、grandezas-compostas→grandezas-e-medidas

BR / Matemática / 1ª série
1. notacao-cientifica-e-medidas ✓ 2. grandezas-compostas ✓ 3. funcoes-e-taxa-de-variacao ✓ 4. funcao-afim ✓ 5. funcao-quadratica ✓ 6. maximo-e-minimo-da-funcao-quadratica ✓ 7. funcoes-definidas-por-partes ✓
8. progressao-aritmetica ✓ 9. progressao-geometrica ✓ 10. funcao-exponencial ✓ 11. logaritmos ✓ 12. funcao-logaritmica ✓ 13. sistemas-lineares ✓ 14. tabelas-e-graficos-estatisticos ✓ 15. medidas-de-tendencia-central-e-dispersao ✓

BR / Matemática / 2ª série（br_em に tri_ret（直角三角形、直角は C）・tri（三辺から三角形）・pit（π の倍数）・trig（特別角の sen/cos/tg の文字列））。トピック trigonometria を足した（geometria に isometricas・cilindros・trigonometria-no・leis-dos-senos、grandezas-e-medidas に cilindros・superficies、probabilidade の principio は principio-multiplicativo|principio-fundamental に絞った（Cavalieri に当たらない））
1. trigonometria-no-triangulo-retangulo ✓ 2. leis-dos-senos-e-dos-cossenos ✓ 3. ciclo-trigonometrico-e-radianos ✓ 4. funcoes-seno-e-cosseno ✓ 5. transformacoes-isometricas-e-homotetias ✓ 6. areas-de-superficies ✓ 7. poligonos-regulares-e-ladrilhamentos ✓
8. prismas-e-piramides ✓ 9. cilindros-cones-e-esferas ✓ 10. volumes-e-principio-de-cavalieri ✓ 11. principio-fundamental-da-contagem ✓ 12. permutacoes-arranjos-e-combinacoes ✓ 13. probabilidade-e-espaco-amostral ✓ 14. probabilidade-condicional-e-eventos-sucessivos ✓

BR / Matemática / 3ª série（br_em に code（Python・アルゴリズムの <span class='code'>）・fluxo（フローチャートの SVG）。トピック matematica-financeira（juros・orcamento・financiamento・taxas-e-indices）を足した。probabilidade に correlacao・histograma・box-plot、grandezas-e-medidas に escalas。algoritmos・programacao はトピックなし。グラフの縦軸が 4 桁になるときは千単位にする（左が切れる））
1. juros-simples-e-compostos ✓ 2. orcamento-e-financiamentos ✓ 3. taxas-e-indices ✓ 4. modelos-com-funcoes ✓ 5. histograma-box-plot-e-ramo-e-folhas ✓ 6. pesquisa-amostral-e-relatorio ✓ 7. correlacao-e-reta-de-ajuste ✓
8. algoritmos-e-fluxogramas ✓ 9. introducao-a-programacao ✓ 10. escalas-e-projecoes-cartograficas ✓

BR / Matemática は 1º ano〜3ª série まで完了（EM13MAT のスキルはすべてどこかの単元に入っている）。次は GDP 順で次の国（juros, finanças, índices, modelos, box-plot, pesquisa amostral, regressão, algoritmos, programação, cartografia, polígonos regulares, riscos）

ES / Matemáticas（LOMLOE、Real Decreto 157/2022 の Educación Primaria の saberes básicos）— country `es`（name「España」、lang `es`、hreflang es-es、standard「LOMLOE」）、subject `matematicas`（Matemáticas）、grade `N-primaria`（name「4.º de Primaria」、N+5〜N+6 歳、unit.php）、A4。
生成スクリプトは `gen_es_matematicas_N_*`（seed は 44NNN：4.º は 44001〜）、共通部品は `tools/es_common.py`（num（4 桁はそのまま 4536、5 桁以上はノーブレークスペース 12 345。RAE）・dec・dz（コンマの小数）・eur（3,50 €、c=True で 45 céntimos）・hora（8:15）・dur（1 h 25 min）・pl・Kids（名前と ella/él）・ao・mcq（ES_WARN=1 で FILL）・bank・lesson（Cómo se hace → Ejemplo → Errores frecuentes）・make_unit（seo_title「Fracciones – 4.º de Primaria: fichas de matemáticas con soluciones」、standard_code「4.º de Primaria · Sentido numérico」）・letra（999 999 までの数詞、veintiún mil）・nomfrac（3/4 → tres cuartos）・図：recta（every は値の単位：every=5 * step）・bloques・tabla_valor（CM DM UM C D U）・tabla_decimal・grafico・dinero_svg・cuerpo_svg・reloj・vertical（筆算）・tira・circulo）と測定の部品 `tools/es_medida.py`（LON・MAS・CAP、conv・compound・comparar）。
スペイン語（スペイン）、tú で話しかける短い文。記号は × と :（割り算）、余りは「23 : 5 = 4 y resto 3」。時刻は「las tres y cuarto」「las cuatro menos veinte」、24 時間制は 17:30。単位は km hm dam m dm cm mm、kg g t、L dL cL mL。
domain は LOMLOE の sentidos（N Sentido numérico／M Sentido de la medida／E Sentido espacial／A Sentido algebraico／S Sentido estocástico）、standard_text は saberes básicos の要約、standard_url は BOE-A-2022-3296。角度・三角形・四角形の図は `gen_au_maths_y5_angles`（angle_fig・protractor_svg・tri_pts・shape_svg）を relabel で使う。
q・c・e の中の < > は &lt; &gt;。選択肢は必ず 4 つ（「<」「>」「=」の 3 択は文の比較にする）。同じ文の問題は重複扱いなので、数を問題文に入れる。
UI 文言は core.php の 'es'（js の桁区切りはノーブレークスペース）、トピックは topics.php の `topic_defs_es()`（numeros・suma-y-resta・multiplicacion-y-division・fracciones-y-decimales・problemas・magnitudes-y-medida・geometria・estadistica-y-probabilidad）、topic.php・topics.php に $es の文言

ES / Matemáticas / 4.º de Primaria（segundo ciclo の最後の学年。数は 999 999 まで、小数は centésimas まで）
1. numeros-de-hasta-seis-cifras ✓ 2. comparar-y-redondear-numeros ✓ 3. numeros-romanos ✓ 4. suma-y-resta ✓ 5. calculo-mental-y-estimacion ✓ 6. multiplicacion ✓ 7. division ✓
8. multiplos-y-divisores ✓ 9. problemas-de-dos-operaciones ✓ 10. fracciones ✓ 11. fracciones-equivalentes ✓ 12. numeros-decimales ✓ 13. suma-y-resta-de-decimales ✓
14. medidas-de-longitud ✓ 15. masa-y-capacidad ✓ 16. el-tiempo-y-el-reloj ✓ 17. el-dinero ✓ 18. angulos ✓ 19. triangulos-y-cuadrilateros ✓ 20. perimetro-y-area ✓
21. cuerpos-geometricos ✓ 22. simetria-y-coordenadas ✓ 23. patrones-e-igualdades ✓ 24. graficos-y-tablas ✓ 25. probabilidad ✓

ES / Matemáticas / 5.º・6.º de Primaria（tercer ciclo）— 生成スクリプトは `gen_es_matematicas_6_*` に `build(lv)`（lv = 5 または 6、seed は 40000 + 1000 × lv + 番号）、`gen_es_matematicas_5_*` は `build(5)` を呼ぶだけ（5.º だけの medida-del-tiempo、6.º だけの longitud-y-area-del-circulo は自前）。
共通部品は `tools/es_c3.py`（es_common の上に fq（Fraction → 分数の HTML、mixto=True で帯分数）・d（Fraction → コンマの小数、割り切れないと ValueError）・sg（−3）・W・M（neg=True の mcq））。es_common に letra_big（999 999 999 まで）、tabla_valor は 9 列（CMi DMi UMi …）。4.º の生成スクリプトの問題関数は es_common.use で R を入れ替えて再利用（triangulos-y-cuadrilateros・cuerpos-geometricos・probabilidad）。
範囲：5.º は 9 999 999・小数 3 桁・分母 10 まで・porcentajes は 10/20/25/50/75 %、6.º は 999 999 999・負の数・m.c.m./m.c.d.・分数の × ÷・π = 3,14・m³。
ページ上部（title ≤ 50 字・key_big ≤ 36 字・key_sub ≤ 50 字）は make_unit が assert で止める。トピックに algebra-y-proporcionalidad（patrones・ecuaciones・expresiones・proporcionalidad）を足した。potencias・jerarquia→numeros、area- は magnitudes-y-medida だけ
5.º: 1. numeros-grandes ✓ 2. numeros-enteros ✓ 3. potencias ✓ 4. multiplos-divisores-y-primos ✓ 5. jerarquia-de-las-operaciones ✓ 6. fracciones ✓ 7. operaciones-con-fracciones ✓ 8. numeros-decimales ✓ 9. operaciones-con-decimales ✓ 10. porcentajes ✓ 11. proporcionalidad ✓ 12. expresiones-y-ecuaciones ✓
13. medidas-de-longitud-masa-y-capacidad ✓ 14. medidas-de-superficie ✓ 15. angulos ✓ 16. poligonos-y-circulo ✓ 17. area-de-figuras-planas ✓ 19. cuerpos-y-volumen ✓ 20. coordenadas-y-movimientos ✓ 21. estadistica ✓ 22. probabilidad ✓ 23. medida-del-tiempo ✓
6.º: 1. numeros-grandes ✓ 2. numeros-enteros ✓ 3. potencias-y-raiz-cuadrada ✓ 4. multiplos-divisores-mcm-y-mcd ✓ 5. jerarquia-de-las-operaciones ✓ 6. fracciones ✓ 7. operaciones-con-fracciones ✓ 8. numeros-decimales ✓ 9. operaciones-con-decimales ✓ 10. porcentajes ✓ 11. proporcionalidad ✓ 12. expresiones-y-ecuaciones ✓
13. medidas-de-longitud-masa-y-capacidad ✓ 14. medidas-de-superficie ✓ 15. angulos ✓ 16. poligonos-y-circulo ✓ 17. area-de-figuras-planas ✓ 18. longitud-y-area-del-circulo ✓ 19. cuerpos-y-volumen ✓ 20. coordenadas-y-movimientos ✓ 21. estadistica ✓ 22. probabilidad ✓

ES / Matemáticas / 1.º・2.º・3.º de Primaria（primer ciclo と 3.º）— 1.º・2.º と共有する単元は `gen_es_matematicas_3_*` に `build(lv)`（lv = 1〜3、seed は 30000 + 1000 × lv + 番号）、`gen_es_matematicas_2_*`・`_1_*` は build を呼ぶだけ。
3.º は 4.º と同じ segundo ciclo なので、多くの単元は `tools/es_low.py` の `src(4.º の生成スクリプト名, seed, 関数名…, mx=9999, sin=(…), rep=[(古い文字, 新しい文字)])` で 4.º の問題関数を数の上限・語の除外・文字の置き換え付きで再利用し、`unit(lv, slug, sort, …, spec, seed, pic)` で作る（4.º A → 3.º A など）。
絵は `tools/es_pics.py`（k_pics の絵にスペイン語の aria-label：COSAS（名詞と性）・cuantos・cosas、fila・disperso・marco10・dados・dos_grupos・tachados・torres・lapices・caja・regletas・salto・grupos・matriz・plato）。範囲：1.º は 99 まで（計算は 20 まで）、2.º は 999 まで（かけ算は 2・3・4・5・10 の段）、3.º は 9999 まで。
トピック：estadistica-y-probabilidad の out に tablas-de-multiplicar
3.º: 1. numeros-hasta-9999 ✓ 2. comparar-ordenar-y-redondear ✓ 3. suma-y-resta ✓ 4. calculo-mental ✓ 5. tablas-de-multiplicar ✓ 6. multiplicacion ✓ 7. division ✓ 8. problemas ✓ 9. fracciones ✓ 10. patrones-e-igualdades ✓
11. medidas-de-longitud ✓ 12. masa-y-capacidad ✓ 13. el-reloj-y-el-calendario ✓ 14. el-dinero ✓ 15. perimetro ✓ 16. rectas-y-angulos ✓ 17. poligonos ✓ 18. cuerpos-geometricos ✓ 19. orientacion-y-simetria ✓ 20. graficos-y-tablas ✓ 21. probabilidad ✓

2.º・1.º だけの単元は `gen_es_matematicas_2_*`（build(lv)、lv = 1・2）、`gen_es_matematicas_1_*` は build(1) を呼ぶだけ。2.º の probabilidad・orientación・gráficos は es_low.src で 4.º を再利用（rep で 4.º → 2.º）。
絵と名詞を合わせる（problemas の DIBUJO：canicas→ball など。合う絵がなければ絵なし）。トピック：dobles・repartos→multiplicacion-y-division、mitad-tercio→fracciones-y-decimales、monedas・medir→magnitudes-y-medida（numeros の out に medir）、posiciones・orientacion→geometria、seguro-posible→estadistica-y-probabilidad
2.º: 1. numeros-hasta-999 ✓ 2. comparar-y-ordenar-numeros ✓ 3. suma-y-resta-con-llevadas ✓ 4. calculo-mental ✓ 5. la-multiplicacion ✓ 6. repartos ✓ 7. problemas ✓ 8. mitad-tercio-y-cuarto ✓ 9. patrones-y-series ✓
11. longitud-masa-y-capacidad ✓ 12. el-reloj-y-el-calendario ✓ 13. el-dinero ✓ 14. figuras-planas ✓ 15. cuerpos-geometricos ✓ 16. orientacion-en-el-espacio ✓ 17. graficos-y-tablas ✓ 18. seguro-posible-o-imposible ✓
1.º: 1. numeros-hasta-99 ✓ 2. comparar-y-ordenar-numeros ✓ 3. sumas-y-restas-hasta-20 ✓ 4. sumas-y-restas-hasta-99 ✓ 5. problemas ✓ 6. dobles-y-mitades ✓ 7. patrones-y-series ✓ 8. medir-y-comparar ✓
9. el-reloj ✓ 10. monedas-y-billetes ✓ 11. figuras-planas ✓ 12. cuerpos-geometricos ✓ 13. posiciones ✓ 14. recuento-y-graficos ✓

ES / Matemáticas / ESO（Real Decreto 217/2022。1.º〜3.º と 4.º の saberes básicos を教科書の一般的な配分で学年に分ける）— grade `1-eso`〜`4-eso`（name「1.º de ESO」、sort 7〜10、unit.php で 12〜16 歳と educationalLevel「Educación Secundaria Obligatoria」）。standard_url は BOE-A-2022-4975（es_common.STD_URL_ESO）。
生成スクリプトは `gen_es_matematicas_{1,2,3,4}eso_*`、共通部品は `tools/es_eso.py`（es_c3 の上に E・expr・poly・P2・par・sup・nz・rq・raiz（2√3）・sol（x₁ = …, x₂ = …）・kosy・kurve・figure（スペイン語のラベル）・L・tabla・unit(lv, R, slug, dom, …, sort)・use_（他学年の問題関数を R を入れ替えて使い、× を · にする））。
ESO の掛け算は「·」、負の数は「−」、小数の並びは「; 」で区切る（コンマの小数と紛れないように）。周期小数は `<span class='ov'>3</span>`、連立は `<span class='sys'>…<br>…</span>`。数え上げは C<sub>n,k</sub>・V<sub>n,k</sub>。π は 3,14。
いくつかの学年で同じ分野の単元は、一番下の学年のファイルに build(lv) を書き、ほかの学年はラッパー（`from gen_es_matematicas_2eso_potencias import build; build(4)`）。seed は 47000（1.º）・48000（2.º）・49000（3.º）・50000（4.º）＋番号、共有ファイルは基準の seed ＋ (lv − 基準の学年) × 1000。
トピック：funciones（Funciones）を足した。divisibilidad→multiplicacion-y-division、radicales・logaritmos→numeros、algebraico・polinomios・inecuaciones・sucesiones→algebra-y-proporcionalidad、pitagoras・semejanza・trigonometria・movimientos・analitica・espacio→geometria、combinatoria→estadistica-y-probabilidad。poligonos-y-areas は geometria だけ、areas-y-volumenes-de-cuerpos は magnitudes-y-medida だけ
1.º: 1. divisibilidad ✓ 2. numeros-enteros ✓ 3. potencias-y-raices ✓ 4. fracciones ✓ 5. numeros-decimales ✓ 6. proporcionalidad-y-porcentajes ✓ 7. lenguaje-algebraico ✓ 8. ecuaciones-de-primer-grado ✓ 9. coordenadas-y-graficas ✓ 10. rectas-y-angulos ✓ 11. poligonos-y-areas ✓ 12. circunferencia-y-circulo ✓ 13. estadistica ✓ 14. probabilidad ✓
2.º: 1. fracciones-y-decimales ✓ 2. potencias-y-notacion-cientifica ✓ 3. proporcionalidad-directa-e-inversa ✓ 4. porcentajes ✓ 5. polinomios-e-identidades-notables ✓ 6. ecuaciones-de-primer-y-segundo-grado ✓ 7. sistemas-de-ecuaciones ✓ 8. funciones-lineales ✓ 9. teorema-de-pitagoras ✓ 10. semejanza-y-teorema-de-tales ✓ 11. areas-y-volumenes-de-cuerpos ✓ 12. estadistica ✓ 13. probabilidad ✓
3.º: 1. numeros-racionales-e-irracionales ✓ 2. potencias-y-radicales ✓ 3. sucesiones-y-progresiones ✓ 4. polinomios-y-ruffini ✓ 5. ecuaciones-de-segundo-grado ✓ 6. sistemas-de-ecuaciones ✓ 7. funciones-y-sus-propiedades ✓ 8. funciones-lineales-y-cuadraticas ✓ 9. movimientos-en-el-plano ✓ 10. geometria-del-espacio ✓ 11. estadistica ✓ 12. probabilidad ✓
4.º: 1. numeros-reales-e-intervalos ✓ 2. radicales-y-logaritmos ✓ 3. polinomios-y-fracciones-algebraicas ✓ 4. ecuaciones-y-sistemas ✓ 5. inecuaciones ✓ 6. semejanza ✓ 7. trigonometria ✓ 8. geometria-analitica ✓ 9. funciones-elementales ✓ 10. porcentajes-e-interes-compuesto ✓ 11. estadistica-bidimensional ✓ 12. combinatoria ✓ 13. probabilidad ✓

ES / Matemáticas / Bachillerato（Real Decreto 243/2022、Bachillerato de Ciencias y Tecnología の Matemáticas I・II）— grade `1-bachillerato`・`2-bachillerato`（name「1.º de Bachillerato」、sort 11・12、unit.php で 16〜18 歳と educationalLevel「Bachillerato」）。standard_url は BOE-A-2022-5521（es_common.STD_URL_BACH）、standard_code は「Matemáticas I · Sentido algebraico」形式。
生成スクリプトは `gen_es_matematicas_{1,2}bach_*`（seed は 51000＋番号・52000＋番号）、共通部品は `tools/es_bach.py`（es_eso の上に unit（grade を -bachillerato に）・r2（四捨五入、コンマ）・nf・mat・det_h（行列と行列式、ws.css の .mx）・V・pi_txt・det2・det3・mmul・tr・W）と `tools/es_espacio.py`（空間の V・add・esc・cruz・mod2・plano・param・continua・simp）。
límites・derivadas・aplicaciones de las derivadas は 1.º の生成スクリプトに build(lv) を書き、2.º はラッパー（2.º は L'Hôpital・Bolzano・curvatura・Rolle などを足す）。distribución binomial・normal は gen_es_matematicas_2bach_distribuciones.py の build(kind)。
確率の選択肢は 0〜1 の外を Wp で落とす。「y = x² y y = 3x」のように接続詞の y と変数の y が並ぶ文は「la parábola y = x² y la recta y = 3x」「r: … y s: …」と書く。
トピック：analisis（Límites, derivadas e integrales）を足した。matrices・determinantes・gauss→algebra-y-proporcionalidad、vectores・conicas・triangulos・planos・distancias→geometria、distribucion→estadistica-y-probabilidad、magnitudes-y-medida の out に integrales
1.º（Matemáticas I）: 1. numeros-reales-y-logaritmos ✓ 2. numeros-complejos ✓ 3. ecuaciones-e-inecuaciones ✓ 4. sistemas-metodo-de-gauss ✓ 5. trigonometria ✓ 6. resolucion-de-triangulos ✓ 7. vectores-en-el-plano ✓ 8. geometria-analitica ✓ 9. lugares-geometricos-y-conicas ✓ 10. funciones ✓ 11. limites-y-continuidad ✓ 12. derivadas ✓ 13. aplicaciones-de-las-derivadas ✓ 14. estadistica-bidimensional ✓
2.º（Matemáticas II、PAU）: 1. matrices ✓ 2. determinantes ✓ 3. sistemas-de-ecuaciones-lineales ✓ 4. vectores-en-el-espacio ✓ 5. rectas-y-planos-en-el-espacio ✓ 6. posiciones-angulos-y-distancias ✓ 7. limites-y-continuidad ✓ 8. derivadas ✓ 9. aplicaciones-de-las-derivadas ✓ 10. integrales-indefinidas ✓ 11. integrales-definidas-y-areas ✓ 12. probabilidad ✓ 13. distribucion-binomial ✓ 14. distribucion-normal ✓

ES / Matemáticas Aplicadas a las Ciencias Sociales I・II（Real Decreto 243/2022、Bachillerato de Humanidades y Ciencias Sociales）— grade `1-bachillerato-ccss`・`2-bachillerato-ccss`（name「1.º de Bachillerato CCSS」、sort 13・14、unit.php で 16〜18 歳）。standard_code は「Matemáticas Aplicadas a las CC. SS. I · Sentido numérico」、standard_url は BOE-A-2022-5521。
生成スクリプトは `gen_es_matematicas_{1,2}ccss_*`（seed は 53000＋番号・54000＋番号、use_ で再利用するモジュールは 532xx・541xx・542xx・543xx）、共通部品は `tools/es_ccss.py`（es_bach の上に unit・eu（12 345,60 €）・pc（3,5 %）・dd・phi・Z_CRIT）。
多くは Matemáticas I・II・3.º ESO の問題関数を use_ で再利用し、社会科学の場面（利子、税、需要と供給、限界費用、調査の分割表）の問題を足す。use_ で 1.º CCSS のモジュールを使うときは、先にそのモジュールを import してから、その中で使う 1bach/2bach のモジュールを自分の seed で use_ する（後から import すると R が戻される）。
自前: aritmetica-mercantil（IVA 21 %、TAE、préstamo）、programacion-lineal（region() で整数の頂点、pic() で可行領域の SVG）、muestreo、intervalos-de-confianza（z = 1,645／1,96／2,575、E を先に丸めてから区間）。s_contingencia（1.º CCSS probabilidad）は 2.º でも使う
1.º CCSS: 1. aritmetica-mercantil ✓ 2. numeros-reales-y-logaritmos ✓ 3. ecuaciones-e-inecuaciones ✓ 4. sistemas-de-ecuaciones ✓ 5. funciones ✓ 6. limites-y-continuidad ✓ 7. derivadas ✓ 8. estadistica-bidimensional ✓ 9. probabilidad ✓ 10. distribuciones-binomial-y-normal ✓
2.º CCSS（PAU）: 1. matrices ✓ 2. sistemas-de-ecuaciones-lineales ✓ 3. programacion-lineal ✓ 4. limites-y-continuidad ✓ 5. derivadas-y-aplicaciones ✓ 6. integrales ✓ 7. probabilidad ✓ 8. muestreo-y-distribucion-de-medias ✓ 9. intervalos-de-confianza ✓
トピック：mercantil→fracciones-y-decimales、programacion-lineal→algebra-y-proporcionalidad、muestreo・intervalos-de-confianza→estadistica-y-probabilidad

ES / Matemáticas は 1.º de Primaria〜2.º de Bachillerato（Ciencias y Tecnología と CCSS）まで完了。次は GDP 順で次の国（メキシコ）

MX / Matemáticas（SEP、Plan de Estudio 2022・Nueva Escuela Mexicana、Programa sintético 2024。算数は Saberes y Pensamiento Científico の中の contenidos）— country `mx`（name「México」、lang `es-MX`、hreflang es-mx、standard「NEM」、paper letter＝「tamaño carta」）、subject `matematicas`、grade `N-primaria`（name「3.er grado de primaria」、N+5〜N+6 歳、unit.php）。
生成スクリプトは `gen_mx_matematicas_N_*`（seed は 63NNN）、共通部品は `tools/mx_common.py`（num（SEP と同じく 1 000 以上はノーブレークスペース区切り）・dec（小数は点 2.5）・peso（$25、$3.50、50 centavos）・hora_letra（「cuarto para las cuatro」「diez para las dos」）・Kids（メキシコの名前）・dinero_svg（50¢・$1・$2・$5・$10・$20 硬貨、$20〜$1 000 札）・make_unit／unit（standard_code「Fase 4, 3.er grado · Suma y resta, su relación como operaciones inversas」、standard_url は Programa sintético Fase 4 の PDF、domain は contenido の短い名前））。
スペインの生成スクリプトの問題関数を `src(モジュール名, seed, *関数名, lv=, mx_=最大の数, sin_=, extra=, patch=)` で再利用する。src は mx_text() で €→$・céntimos→centavos・小数のコンマ→点・4 桁の区切り・「:」→「÷」・resto→residuo・語（zumo→jugo、autobús→camión、agujas→manecillas、gráfico→gráfica、colegio→escuela、スペインの地名→メキシコの都市）を直し、LEAKS・LEAK_RE（「las cuatro menos cuarto」・vosotros・tarta など）が残る問題は落とす。sin_ は q の HTML も見る（「cL」は class に当たる）ので、単位の除外は extra に正規表現で書く。patch={"dicho": hora_letra} で時刻の言い方をメキシコ式に。
年（nació・año・cumple を含む問題の 1950〜2050）は区切らない。トピックは topic_defs_es() を共用（blurb_mx あり）。core.php の T・J に 'es-MX'（Grados、Respuestas、Encierra en un círculo、El mejor de México）

MX / Matemáticas / 3.er grado de primaria（Fase 4。9 999 まで、足し算は 3 桁、かけ算の積は 3 桁、わり算は 2 桁 ÷ 1 桁、分数は 2・4・8・16）
1. numeros-hasta-9999 ✓ 2. comparar-y-ordenar-numeros ✓ 3. suma-y-resta ✓ 4. calculo-mental ✓ 5. tablas-de-multiplicar ✓ 6. multiplicacion ✓ 7. division ✓ 8. problemas ✓ 9. fracciones ✓
10. cuerpos-geometricos ✓ 11. figuras-geometricas ✓ 12. medidas-de-longitud ✓ 13. masa-y-capacidad ✓ 14. perimetro ✓ 15. el-reloj-y-el-tiempo ✓ 16. el-dinero ✓ 17. tablas-y-graficas ✓ 18. sucesiones-y-patrones ✓

MX / Matemáticas / 4.º grado de primaria（Fase 4。99 999 まで、ordinales は vigésimo まで、かけ算は 3 桁 × 2 桁、わり算は 3 桁 ÷ 1・2 桁、分数は tercios・quintos・sextos・novenos・décimos、小数は centésimos まで）— 生成スクリプトは `gen_mx_matematicas_4_*`（seed は 640NN、ES 4.º の再利用は 642NN、ES 5.º（ES6 の build を lv=5）は 643NN、自前の R は 641NN）。
mx_common の WORDS で décimas→décimos・centésimas→centésimos、coma debajo de coma→punto debajo de punto、hucha→alcancía、ortoedro→prisma rectangular、valla→cerca、baldosa→loseta、forma compleja→con dos unidades、ha recorrido→recorrió などの完了形も直す。年（año・nació を含む問題の 1000〜2100）は区切らない。
src の filter は ES の書式（小数はコンマ）の文に効くので、小数の正規表現は [.,] にする。答えと同じ値の分数の誤答は落とす（suma-y-resta-de-fracciones の mcq）
1. numeros-hasta-99999 ✓ 2. comparar-y-redondear-numeros ✓ 3. suma-y-resta ✓ 4. multiplicacion ✓ 5. division ✓ 6. dobles-triples-y-mitades ✓ 7. problemas ✓ 8. fracciones ✓ 9. fracciones-equivalentes ✓
10. numeros-decimales ✓ 11. suma-y-resta-de-decimales ✓ 12. suma-y-resta-de-fracciones ✓ 13. longitud-masa-y-capacidad ✓ 14. el-tiempo ✓ 15. perimetro-y-area ✓ 16. prismas-y-piramides ✓ 17. cuadrilateros ✓ 18. tablas-y-graficas ✓

MX / Matemáticas / 5.º・6.º grado de primaria（Fase 5、STD_URL は 2024/08/6.pdf。CONT の Fase 5 の内容: Q Relaciones de proporcionalidad、U Ubicación espacial、L5 Medición de la longitud, masa y capacidad、V Perímetro, área y noción de volumen、B Nociones de probabilidad）— 生成スクリプトは `gen_mx_matematicas_5_*`・`gen_mx_matematicas_6_*`（seed は 650NN・660NN、ES 6.º の build を lv=5 / lv=6 で再利用するのは 653NN・663NN、ES 4.º は 652NN・662NN、自前の R は 651NN・661NN）。
ES6 の numeros_grandes は LV ではなく D（桁数）を使うので src の patch={"D": 9}。mx_common.mx_text は「 : 」（数・語・かっこの前後に空白）を ÷ に、「escala 1 : 100」を 1:100 に直す。4 桁の数は小数点の前でも区切る（1 133.54）
6.º の numeración maya は自前の SVG（maya_svg：punto・raya・caracol、下から上へ 1・20・400）。plano-cartesiano は自前の第 1 象限の SVG（data-pf='lg'）
5.º: 1. numeros-hasta-cientos-de-millones ✓ 2. multiplicacion-y-division ✓ 3. numeros-decimales ✓ 4. operaciones-con-decimales ✓ 5. fracciones ✓ 6. suma-y-resta-de-fracciones ✓ 7. multiplicacion-de-fracciones-por-un-natural ✓ 8. proporcionalidad ✓
9. porcentajes ✓ 10. longitud-masa-y-capacidad ✓ 11. perimetro-y-area ✓ 12. volumen ✓ 13. angulos ✓ 14. poligonos-y-circulo ✓ 15. tablas-y-graficas ✓ 16. probabilidad ✓
6.º: 1. sistemas-de-numeracion ✓ 2. fracciones-y-decimales ✓ 3. suma-y-resta-de-fracciones ✓ 4. operaciones-con-decimales ✓ 5. division-de-fracciones-entre-naturales ✓ 6. proporcionalidad ✓ 7. porcentajes ✓ 8. circunferencia-y-pi ✓
9. poligonos-regulares ✓ 10. plano-cartesiano ✓ 11. perimetro-y-area ✓ 12. volumen ✓ 13. graficas-circulares ✓ 14. media-moda-y-rango ✓ 15. probabilidad ✓

MX / Matemáticas / 1.er・2.º grado de primaria（Fase 3、STD_URL は 2024/06/Programa_Sintetico_Fase_3.pdf。CONT に S3・P3。1.º は 100 まで（計算は 20 まで、2 桁は繰り上がりなし）、かけ算は答え 10 まで。2.º は 1 000 まで、かけ算・わり算は 10 未満。標準単位（cm・kg・L）とお金はなし）— 1.º・2.º で共有する単元は `gen_mx_matematicas_1_*` に `build(lv)`（seed は 60000 + 1000 × lv + 番号、ES の再利用は 6x9xx）、`gen_mx_matematicas_2_*` はラッパー。共通部品は `tools/mx_12.py`（BIG（src の mx_ に渡す。ES の lim は SVG の数字を数えて落とすので、数の範囲は q_le・all_le で絞る）・std_units（標準単位を落とす）・calendario_svg・s_calendario・s_ayer・s_iguales）。
mx_common の WORDS で palmo→cuarta、octógono→octágono、STOP→ALTO、recuento→conteo。SVG の aria-label の gráfico も gráfica に
1.º: 1. numeros-hasta-100 ✓ 2. comparar-y-ordenar-numeros ✓ 3. sucesiones-y-patrones ✓ 4. sumas-y-restas-hasta-20 ✓ 5. calculo-mental ✓ 6. problemas-de-suma-y-resta ✓ 7. sumas-iguales-y-multiplicacion ✓ 8. cuerpos-geometricos ✓ 9. figuras-geometricas ✓ 10. longitud-y-masa ✓ 11. dias-semanas-y-meses ✓ 12. tablas-y-pictogramas ✓
2.º: 1. numeros-hasta-1000 ✓ 2. comparar-y-ordenar-numeros ✓ 3. sucesiones-y-patrones ✓ 4. suma-y-resta ✓ 5. calculo-mental ✓ 6. problemas-de-suma-y-resta ✓ 7. multiplicacion ✓ 8. reparto-y-division ✓ 9. dobles-y-mitades ✓ 10. figuras-geometricas ✓ 11. longitud-masa-y-capacidad ✓ 12. calendario ✓ 13. tablas-y-pictogramas ✓
トピック：calendario・dias-semanas→magnitudes-y-medida、pictogramas→estadistica-y-probabilidad

MX / Matemáticas / 1.er grado de secundaria（Fase 6、STD_URL は 2024/08/7.pdf。CONT は 6FD・6PN・6OP・6RP・6IA・6EC・6FU・6RA・6CF・6CC・6ME・6OR・6TC・6AZ（Fase 6 の 14 contenidos）。grade `1-secundaria`（sort 7、unit.php で 12〜13 歳と educationalLevel「Educación secundaria」）。lv=7（8・9 は 2.º・3.º）
生成スクリプトは `gen_mx_matematicas_1s_*`（seed は 670NN、ES の再利用は 673NN〜675NN）、自前の問題は `tools/mx_s1.py`（setup(R) してから使う。fd_*・pn_context・ec_problem・pc_problem（IVA 16 %、メキシコの値段）・fu_table・fu_graph・ra_notacion・ra_distancia・cf_construccion・cc_rectas・ingles（yarda・pulgada・galón・onza・libra）・cuerpos・circular・sc_figuras・sc_contexto・az_compara。種類を引数で選べる：S.cuerpos("cvAp")）。
ES の問題関数は src() で再利用。スペインの値段は pesos にすると不自然なので extra=(nomoney,) で落とす（nomoney は € も見る）。src は ES の関数の ValueError・AssertionError も None にする。ESO の「·」は「×」に、m.c.d.→MCD、m.c.m.→mcm、選択肢の「-3」→「−3」。確率のコインは rep で cara/cruz→águila/sol（WORDS に入れると cuerpos の caras まで変わる）
1. numeros-con-signo ✓ 2. operaciones-con-numeros-con-signo ✓ 3. fracciones-y-decimales ✓ 4. operaciones-con-fracciones-y-decimales ✓ 5. mcd-y-mcm ✓ 6. sucesiones-aritmeticas ✓ 7. lenguaje-algebraico ✓
8. ecuaciones-lineales ✓ 9. problemas-con-ecuaciones ✓ 10. porcentajes ✓ 11. proporcionalidad ✓ 12. rectas-y-angulos ✓ 13. construcciones-con-regla-y-compas ✓ 14. cuerpos-geometricos ✓
15. rectas-notables-de-la-circunferencia ✓ 16. perimetro-y-area-de-poligonos ✓ 17. perimetro-y-area-del-circulo ✓ 18. conversion-de-unidades ✓ 19. tablas-y-graficas ✓ 20. frecuencias-y-medidas-de-tendencia-central ✓ 21. probabilidad ✓
トピック：construcciones→geometria、conversion-de-unidades→magnitudes-y-medida、mcd-y-mcm→multiplicacion-y-division、tendencia-central→estadistica-y-probabilidad（magnitudes の out）、geometria の out に perimetro-y-area

MX / Matemáticas / 2.º・3.er grado de secundaria（Fase 6。grade `2-secundaria`（sort 8）・`3-secundaria`（sort 9）、lv=8・9）— 生成スクリプトは `gen_mx_matematicas_2s_*`（seed 681NN、ES は 683NN〜684NN）・`gen_mx_matematicas_3s_*`（seed 691NN、ES は 693NN〜694NN）、自前の問題は `tools/mx_s2.py`（setup(R)。rn_recta・prop_ops・alg_figuras・desig・prop_inv・ang_cruce・notables・triangulos・circ_ang・distancias・graf_linea・histograma・prob2・jerarquia・seq_cuad・alg_vol・reparto・variacion・poligonos・solidos・esfera・compuestas・dispersion・prob3・ec2_problema・trig_calc。種類を引数で選ぶ）。
mix の重複チェックは単元全体で共有なので、同じ問題関数を複数のセットで使うときは合計数がその関数の作れる問題数を超えないようにする。ES の因数分解は答えと同じ式を順番違いで誤答にすることがあるので extra=(S.nocommute,)。mx_item は選択肢の「1x」を「x」に直す。三角比は 0〜90° だけ（tg→tan）
2.º: 1. numeros-con-signo-en-la-recta ✓ 2. propiedades-de-las-operaciones ✓ 3. potencias-y-raiz-cuadrada ✓ 4. notacion-cientifica ✓ 5. expresiones-algebraicas-de-perimetros-y-areas ✓ 6. operaciones-con-polinomios ✓ 7. desigualdades ✓ 8. sistemas-de-ecuaciones ✓ 9. proporcionalidad-directa-e-inversa ✓
10. funciones-lineales ✓ 11. angulos-entre-rectas ✓ 12. rectas-y-puntos-notables-del-triangulo ✓ 13. triangulos-y-cuadrilateros ✓ 14. angulos-en-la-circunferencia ✓ 15. distancias-y-desigualdad-del-triangulo ✓ 16. histogramas-y-graficas-de-linea ✓ 17. media-mediana-moda-y-rango ✓ 18. probabilidad-de-eventos ✓
3.º: 1. jerarquia-de-operaciones ✓ 2. sucesiones-cuadraticas ✓ 3. productos-notables-y-factorizacion ✓ 4. areas-y-volumenes-con-expresiones-algebraicas ✓ 5. ecuaciones-cuadraticas ✓ 6. problemas-con-ecuaciones-cuadraticas ✓ 7. variacion-lineal-cuadratica-e-inversa ✓ 8. reparto-proporcional ✓ 9. poligonos-regulares-y-teselados ✓ 10. congruencia-y-semejanza-de-triangulos ✓
11. solidos-de-revolucion-y-desarrollos-planos ✓ 12. volumen-de-prismas-piramides-y-cilindros ✓ 13. esfera-cono-y-cilindro ✓ 14. perimetro-y-area-de-figuras-compuestas ✓ 15. teorema-de-pitagoras ✓ 16. razones-trigonometricas ✓ 17. interpretacion-de-graficas ✓ 18. medidas-de-dispersion ✓ 19. eventos-independientes-y-juegos-justos ✓
トピック（topic_defs_es）：notacion-cientifica・propiedades-de-las-operaciones→numeros、desigualdades・productos-notables・factorizacion・reparto-proporcional→algebra、variacion-→funciones、esfera・trigonometric→geometria、volumen-de-→magnitudes（geometria の out）、histogramas・interpretacion-de-graficas・eventos・dispersion→estadistica（magnitudes の out に con-expresiones・expresiones-algebraicas・dispersion）

MX / Matemáticas / Bachillerato（MCCEMS、Pensamiento Matemático の progresiones de aprendizaje（SEP 2023）と DGB の Temas Selectos de Matemáticas（2024））— grade は科目ごと：`pensamiento-matematico-1`（sort 10、1.er semestre）・`-2`（11）・`-3`（12）・`temas-selectos-1`（13）・`temas-selectos-2`（14）。lv = 10〜14（mx_common.BACH に名前・URL）。
1 単元 = 1 progresión。unit の cont は (グループ, progresión の番号, 名前) のタプルで、standard_code は「Pensamiento Matemático I · Progresión 4: Técnicas de conteo」。unit.php で 15〜18 歳と educationalLevel「Educación media superior (bachillerato)」。
生成スクリプトは `gen_mx_matematicas_pm1_*`（seed は 1001NN、ES の再利用は 1003NN）、自前の問題は `tools/mx_pm1.py`（setup(R)。p1〜p15 に種類を渡す：S.p13("sd")）。bank 型の問題は文が同じだと重複扱いなので、数や場面を文に入れる
Pensamiento Matemático I: 1. variabilidad-y-toma-de-decisiones ✓ 2. probabilidad-frecuencial ✓ 3. probabilidad-teorica ✓ 4. tecnicas-de-conteo ✓ 5. probabilidad-condicional-y-teorema-de-bayes ✓ 6. tipos-de-variables ✓ 7. graficas-estadisticas ✓ 8. tablas-de-doble-entrada ✓ 9. correlacion-y-recta-de-ajuste ✓ 10. valores-atipicos-y-paradoja-de-simpson ✓ 11. muestreo ✓ 12. estudios-observacionales-y-experimentos ✓ 13. medidas-de-tendencia-central-y-dispersion ✓ 14. distribucion-normal ✓ 15. prueba-de-hipotesis ✓
Pensamiento Matemático II（seed 1101NN・ES 1103NN、自前は `tools/mx_pm2.py` の lp1・lp6・lp8・lp10・lp11・lp12。ES の programación lineal のガナンシアは ×100 してペソに）: 1. lenguaje-natural-y-lenguaje-matematico ✓ 2. lenguaje-algebraico-y-productos-notables ✓ 3. modelacion-algebraica ✓ 4. divisibilidad-y-numeros-primos ✓ 5. mcd-y-mcm ✓ 6. numeros-reales ✓ 7. proporcionalidad-y-porcentajes ✓ 8. matematica-financiera ✓ 9. areas ✓ 10. pitagoras-congruencia-y-semejanza ✓ 11. geometria-analitica ✓ 12. funciones-lineales-cuadraticas-y-polinomiales ✓ 13. sistemas-de-ecuaciones-lineales ✓ 14. programacion-lineal ✓
Pensamiento Matemático III（seed 1201NN・ES 1203NN、自前は `tools/mx_pm3.py` の q1〜q15。ES の 1bach límites・derivadas・aplicaciones は lv=1）: 1. origen-del-calculo ✓ 2. recta-tangente ✓ 3. modelacion-con-funciones ✓ 4. analisis-grafico-de-funciones ✓ 5. limites ✓ 6. continuidad ✓ 7. la-derivada ✓ 8. reglas-de-derivacion ✓ 9. razon-de-cambio-instantanea ✓ 10. analisis-de-funciones-con-derivadas ✓ 11. optimizacion ✓ 12. funciones-exponenciales-y-logaritmicas ✓ 13. funciones-trigonometricas ✓ 14. modelacion-con-ecuaciones-diferenciales ✓ 15. teorema-fundamental-del-calculo ✓
Temas Selectos de Matemáticas I（4.º semestre、seed 1301NN・ES 1303NN、自前は `tools/mx_tsm.py` の t1〜t9）: 1. geometria-y-razones-trigonometricas ✓ 2. leyes-de-senos-y-cosenos ✓ 3. geometria-euclidiana-y-no-euclidiana ✓ 4. rectas-y-sistemas-de-ecuaciones ✓ 5. parabola ✓ 6. circunferencia ✓ 7. elipse ✓ 8. ecuacion-general-de-segundo-grado ✓ 9. fractales ✓
Temas Selectos de Matemáticas II（6.º semestre、seed 1401NN・ES 1403NN、自前は mx_tsm の u1〜u7 と mx_pm3）: 1. composicion-y-sistemas-dinamicos ✓ 2. sucesiones-y-series ✓ 3. sumas-de-riemann ✓ 4. integral-indefinida ✓ 5. integral-definida-y-teorema-fundamental ✓ 6. ecuaciones-diferenciales ✓ 7. metodos-numericos ✓
bachillerato の make_unit は自前の問題の 4 桁以上の数も nums_mx で 1 000 区切りにする（「en 2015」などの年は除く）。src の rep は ES の原文（mx_text の前）に効く
MX / Matemáticas / Preescolar（3.er grado de preescolar、Fase 2、STD_URL は 2024/08/3.pdf。5〜6歳。grade `preescolar`（sort 0、lv=0）。CONT は P0N Números・P0E Espacio y formas・P0M Medidas・P0C Clasificación y datos）— 10 まで（数えるのは 20 まで）。とても短い文、ほぼ全問に絵。
生成スクリプトは `gen_mx_matematicas_pre_*`（build(slug) を呼ぶだけ）、単元の定義は `tools/mx_pre_units.py`（spec(slug)。ES 2.º の問題関数は es(mod, *names, n=上限) で lv=1・all_le(n) 付きで再利用、seed は 59900＋モジュール名）、自前の問題は `tools/mx_pre.py`（setup(R)。contar・palabra・antes_despues・serie・salta・comparar・ordinal・ordinal_carrera・historia・descomponer・repartir・dinero・tiempo・medir・clasificar。種類を引数で選ぶ）。
mx_common の単数の修正に canica・paleta・lápiz など。unit.php で educationalLevel「Educación preescolar」
1. contar-hasta-10 ✓ 2. numeros-hasta-el-20 ✓ 3. comparar-colecciones ✓ 4. numeros-ordinales ✓ 5. agregar-y-quitar ✓ 6. separar-y-repartir ✓ 7. monedas-y-billetes ✓ 8. posiciones-y-recorridos ✓ 9. figuras-y-cuerpos ✓ 10. patrones ✓ 11. longitud-peso-y-capacidad ✓ 12. el-tiempo ✓ 13. clasificar-y-registrar-datos ✓
トピック：contar-hasta→numeros、agregar-y-quitar→suma-y-resta、separar-y-repartir→multiplicacion-y-division、clasificar-y-registrar→estadistica-y-probabilidad

MX / Matemáticas は preescolar・primaria・secundaria・bachillerato（Pensamiento Matemático I〜III、Temas Selectos I・II）まで完了。次は GDP 順で次の国

KR / Math（2022 개정 수학과 교육과정。初等 3〜4学年は 2025 年度、5〜6 学年は 2026 年度から）— country `kr`（name「대한민국」、lang `ko`、hreflang ko-kr、standard「2022 개정 교육과정」）、subject `math`（수학）、grade `grade-N`（name「초등 3학년」、unit.php の年齢は US と同じ）、A4。
生成スクリプトは `gen_kr_math_gN_*`、共通部品は `tools/kr_common.py`（num（4 桁はそのまま、5 桁以上はカンマ）・dnum・won・josa（名前・語の助詞：josa('사과', '을/를')）・Names・mcq（誤答が足りないと None）・lesson（생각하는 방법 → 예제 → 자주 하는 실수）・unit(grade, slug, sort, code, std, title, short, meta, key_big, key_sub, think, examples, mist, faq, spec, seed)（seo_title「… | 초등 3학년 수학 학습지 (정답 포함)」と domain は code から自動）・clock（sec で초바늘）・ff・read_num（수 읽기））と図 `tools/kr_pics.py`（点の名前は ㄱㄴㄷ…：line_kind（선분・반직선・직선）・poly（直角の印）・grid_poly・ruler（cm と mm）・beaker・scale（저울）・circle_fig・pic_graph（그림그래프）・frac_bar・frac_circle・number_line、k_pics の絵に韓国語の aria-label：groups・row・array）。
unit() は出力の文を tidy で直す：**数・単位・分数の直後の助詞は自動で読みに合わせる**（12를・13을、3 kg을・5 cm를、8로・6으로、<b>7</b>이）。名前や語の後は josa() を使う。
1 単元のまとまりは kr_g3_mul.py（곱셈 3 単元）・kr_g3_div.py（나눗셈 2）・kr_g3_frac.py（분수・소수 5）・kr_g3_meas.py（들이・무게 2）の build(which)、gen_ はそれを呼ぶだけ。
pick_unique は問題文（q）で重複を判定するので、q に数や名前を入れて変化させる（文が固定の ○× などは数が限られる）。
standard_code は成就基準コード「[4수01-03]」（複数は空白区切り）、standard_text は成就基準の原文、standard_url は NCIC の 2022 수학과 교육과정（kr_common.STD_URL）。domain は 수와 연산／변화와 관계／도형과 측정／자료와 가능성。
UI 文言は core.php の 'ko'（T と js_text）と ko_josa()、トピックは topics.php の `topic_defs_kr()`（whole-numbers・addition-and-subtraction・multiplication-and-division・fractions-and-decimals・estimation・shapes・measurement・data）、topic.php・topics.php に $ko の文言。
プレビュー画像は Noto Sans KR のサブセット（preview.php の PV_CJK = 'kr'、韓国語は空白で改行）。**kr の単元を足したら `python3 tools/build_cjk_font.py` を実行してフォントもコミット**（TC と KR の両方を作る。TC には ハングル、KR には漢字を入れない）

KR / Math / 초등 3학년（3-1 → 3-2 の順）
1. add-and-subtract-three-digit-numbers ✓ 2. lines-rays-and-angles ✓ 3. right-triangles-rectangles-and-squares ✓ 4. meaning-of-division ✓ 5. multiply-two-digit-by-one-digit ✓ 6. length-mm-and-km ✓ 7. time-in-seconds ✓
8. fractions ✓ 9. decimals ✓ 10. multiply-three-digit-by-one-digit ✓ 11. multiply-two-digit-by-two-digit ✓ 12. division-with-remainders ✓ 13. divide-three-digit-by-one-digit ✓ 14. circles ✓
15. fraction-of-a-number ✓ 16. proper-improper-and-mixed-fractions ✓ 17. comparing-fractions ✓ 18. capacity-liters-and-milliliters ✓ 19. weight-kilograms-and-grams ✓ 20. picture-graphs ✓ 21. estimation ✓
KR / Math / 초등 4학년（4-1 → 4-2。生成スクリプトは `gen_kr_math_g4_*`、まとまりは kr_g4_num.py（数・計算・規則）・kr_g4_geo.py（角度・移動・位置・三角形・垂直と平行・四角形・多角形。角度の図は gen_au_maths_y5_angles を relabel）・kr_g4_fd.py（分数・小数。4 학년は약분しないので fs(v, d) で分母を固定）・kr_g4_data.py（막대・꺾은선그래프）の build(which)。助詞は josa、単位で終わる語は unit_josa）
1. large-numbers ✓ 2. comparing-large-numbers ✓ 3. measuring-angles ✓ 4. angle-sums-of-triangles-and-quadrilaterals ✓ 5. multiply-three-digit-by-two-digit ✓ 6. divide-by-two-digit-numbers ✓ 7. sliding-flipping-and-turning-shapes ✓
8. position-and-direction ✓ 9. bar-graphs ✓ 11. number-patterns ✓ 12. equal-sign-and-equations ✓ 13. adding-and-subtracting-fractions ✓ 14. triangles ✓ 15. decimals-hundredths-and-thousandths ✓
16. adding-and-subtracting-decimals ✓ 17. perpendicular-and-parallel-lines ✓ 18. quadrilaterals ✓ 19. line-graphs ✓ 20. polygons ✓
トピック：position→shapes
KR / Math / 초등 5학년（5-1 → 5-2。生成スクリプトは `gen_kr_math_g5_*`、まとまりは kr_g5_num.py（혼합 계산・약수와 배수・최대공약수・수의 범위・어림）・kr_g5_frac.py（약분과 통분・크기 비교・분수의 덧셈과 뺄셈・분수의 곱셈・소수의 곱셈。答えは기약분수）・kr_g5_geo.py（둘레・넓이・합동・대칭・직육면체と전개도）・kr_g5_data.py（규칙과 대응・평균・가능성）。図は `tools/kr_pics56.py`（iso_cubes（앞の矢印つき）・views_panel・box_svg・circle_svg・strip_graph・pie_graph・range_line・sym_grid））
1. order-of-operations ✓ 2. factors-and-multiples ✓ 3. gcf-and-lcm ✓ 4. rules-and-correspondence ✓ 5. simplifying-and-common-denominators ✓ 6. comparing-fractions-and-decimals ✓ 7. adding-and-subtracting-fractions ✓
8. perimeter-of-polygons ✓ 9. area-units-and-rectangles ✓ 10. area-of-parallelograms-triangles-trapezoids-and-rhombuses ✓ 11. range-of-numbers ✓ 12. rounding-up-down-and-off ✓ 13. multiplying-fractions ✓
14. congruent-figures ✓ 15. line-and-point-symmetry ✓ 16. multiplying-decimals ✓ 17. cuboids-and-cubes ✓ 18. averages ✓ 19. likelihood ✓
KR / Math / 초등 6학년（6-1 → 6-2。生成スクリプトは `gen_kr_math_g6_*`、まとまりは kr_g6_num.py（분수・소수의 나눗셈）・kr_g6_ratio.py（비와 비율・백분율・띠/원그래프・비례식・비례배분）・kr_g6_geo.py（각기둥과 각뿔・겉넓이와 부피・쌓기나무・원주・원의 넓이・원기둥/원뿔/구。원주율 3.14））
1. dividing-fractions-by-whole-numbers ✓ 2. prisms-and-pyramids ✓ 3. dividing-decimals-by-whole-numbers ✓ 4. ratios-and-rates ✓ 5. percentages ✓ 6. strip-and-circle-graphs ✓ 7. surface-area-and-volume-of-cuboids ✓
8. dividing-fractions ✓ 9. dividing-decimals ✓ 10. stacking-cubes-and-views ✓ 11. ratios-and-proportions ✓ 12. proportional-distribution ✓ 13. circumference-and-pi ✓ 14. area-of-circles ✓ 15. cylinders-cones-and-spheres ✓
トピック（topic_defs_kr）：factors-and-multiples（약수와 배수）・ratios-and-proportions（규칙과 비율）を足した。order-of→multiplication、range-of→estimation、congruent・symmetry・cuboids・prisms・cylinders・stacking→shapes、perimeter・area・volume・circumference→measurement、averages→data。
助詞：ㄱ〜ㅂ（点・面の名前）は받침ありとして「이에요・과」を直接書く

KR / Math / 초등 1학년・2학년（2022 개정、2024 年度から）— 共通部品は `tools/kr_low.py`（k_pics の絵に韓国語の aria-label と 가나다라：row・scatter・tenframe・rods・bond・two・crossed・cards・chart・pencils・towers・scale・glasses、수 모형 blocks、돈 money（10〜500원 동전・1000원 지폐）、고유어 native・native_c（한 개・스무 개）、ORD（첫째…）。
import すると kr_common.tidy を拡張して、名詞（사과・꽃…）と助数詞（3장을・몇 권을）の後の助詞、받침の後の 예요→이에요・라고→이라고 も直す）。1학년は 100 まで、計算は 20 まで、とても短い文。2학년は 9999 まで、곱셈구구。
まとまりは kr_g1_num（수 3）・kr_g1_calc（덧셈과 뺄셈 4）・kr_g1_geo（모양・비교・시각・규칙 5）・kr_g2_num（세・네 자리 수）・kr_g2_calc（덧셈・뺄셈・세 수・□ 4）・kr_g2_mul（곱셈・곱셈구구）・kr_g2_meas（cm・m・시각과 시간・달력）・kr_g2_geo（도형・쌓기나무・규칙）・kr_g2_data（분류・표와 그래프）の build(which)。
1학년の입체는「상자・둥근 기둥・공 모양」、평면은「□・△・○ 모양」、2학년から삼각형・사각형・원。トピック `patterns`（규칙 찾기）を足した

KR / Math / 초등 1학년（1-1 → 1-2）
1. numbers-to-9 ✓ 2. solid-shapes ✓ 3. addition-and-subtraction-within-9 ✓ 4. comparing-length-weight-area-and-capacity ✓ 5. numbers-to-50 ✓ 6. numbers-to-100 ✓
7. two-digit-addition-and-subtraction ✓ 8. adding-three-numbers-and-making-10 ✓ 9. addition-and-subtraction-within-20 ✓ 10. flat-shapes ✓ 11. telling-time-hours-and-half-hours ✓ 12. patterns ✓
KR / Math / 초등 2학년（2-1 → 2-2）
1. three-digit-numbers ✓ 2. triangles-quadrilaterals-and-circles ✓ 3. stacking-cubes ✓ 4. adding-two-digit-numbers ✓ 5. subtracting-two-digit-numbers ✓ 6. adding-and-subtracting-three-numbers ✓
7. addition-subtraction-relationship-and-missing-numbers ✓ 8. measuring-length-in-cm ✓ 9. sorting ✓ 10. meaning-of-multiplication ✓ 11. four-digit-numbers ✓ 12. multiplication-tables ✓
13. length-in-meters-and-centimeters ✓ 14. telling-time-to-the-minute ✓ 15. calendar-days-weeks-months-and-years ✓ 16. tables-and-graphs ✓ 17. patterns ✓

KR / Math / 중학교 1〜3학년（2022 개정 중학교 수학。grade は grade-7〜grade-9、name「중학교 N학년」、sort 7〜9、unit.php の年齢は N+5〜N+6）— 生成スクリプトは `gen_kr_math_g7_*`〜`g9_*`（2 行のラッパー）、本体は `tools/kr_m1a.py`・`kr_m1b.py`（중1）、`kr_m2a.py`・`kr_m2b.py`（중2）、`kr_m3a.py`・`kr_m3b.py`（중3）の build(key)、seed は 827NN・828NN・829NN。
共通部品は `tools/kr_mid.py`（kr_low・kr_common の上に sup・neg（−、分数）・par・sg・dec・P（多項式）・rt（√ の簡約）・M（4 択、誤答が 3 つそろわないと None）・N（数の答え）・figure（fr_c4）・kosy（de_k8）・kurve（de_k10）。tidy を拡張して「(6, 1)은」「(−3)을」のかっこの後の助詞と、x²을・(2a²)³을 のように上付き数字（제곱）の後の助詞を直す。cm²・m³ はそのまま）。
standard_code は成就基準「[9수02-13]」、domain は 9수01〜04 から自動。助詞の対は받침ありを先に書く（josa(w, "과/와")）。誤答に正解と同じ式が順番違いで入らないようにする（因数分解は (x + 大)(x + 小) にそろえる）。q の文が同じ問題は重複扱いなので、選択肢を q に並べるか数を入れる。
トピック（topic_defs_kr）に number-systems（정수, 유리수, 실수）・algebra（문자와 식）・equations（방정식과 부등식）・functions（함수와 그래프）を足した。shapes・data は中学校の slug も入る（data の out に function|coordinates）。ratios-and-proportions は (^|-)ratios?(-|$)（operations・rational に当たらない）

KR / Math / 중학교 1학년
1. prime-factorization ✓ 2. integers-and-rational-numbers ✓ 3. adding-and-subtracting-integers-and-rational-numbers ✓ 4. multiplying-and-dividing-integers-and-rational-numbers ✓ 5. algebraic-expressions ✓ 6. linear-equations ✓
7. linear-equation-word-problems ✓ 8. coordinates-and-graphs ✓ 9. direct-and-inverse-proportion ✓ 10. points-lines-planes-and-angles ✓ 11. constructions-and-congruent-triangles ✓ 12. polygons ✓
13. circles-and-sectors ✓ 14. polyhedra-and-solids-of-revolution ✓ 15. surface-area-and-volume ✓ 16. representative-values ✓ 17. frequency-distributions-and-histograms ✓ 18. relative-frequency ✓
KR / Math / 중학교 2학년
1. repeating-decimals ✓ 2. exponent-laws-and-monomials ✓ 3. polynomial-operations ✓ 4. linear-inequalities ✓ 5. systems-of-linear-equations ✓ 6. systems-of-equations-word-problems ✓
7. linear-functions ✓ 8. graphs-of-linear-functions ✓ 9. linear-functions-and-equations ✓ 10. isosceles-triangles ✓ 11. circumcenter-and-incenter ✓ 12. properties-of-quadrilaterals ✓
13. similar-figures ✓ 14. parallel-lines-and-segment-ratios ✓ 15. pythagorean-theorem ✓ 16. counting ✓ 17. probability ✓
KR / Math / 중학교 3학년（이차함수의 최댓값・최솟값は高校なので「증가와 감소」にした）
1. square-roots ✓ 2. irrational-and-real-numbers ✓ 3. operations-with-radicals ✓ 4. multiplying-polynomials ✓ 5. factoring ✓ 6. quadratic-equations ✓
7. quadratic-equation-word-problems ✓ 8. quadratic-functions ✓ 9. graphs-of-quadratic-functions ✓ 10. trigonometric-ratios ✓ 11. applications-of-trigonometric-ratios ✓ 12. chords-and-tangents ✓
13. inscribed-angles ✓ 14. variance-and-standard-deviation ✓ 15. box-plots ✓ 16. scatter-plots-and-correlation ✓

KR / Math / 고등학교（2022 개정。科目ごとに grade：`common-math-1`（공통수학1、sort 10）・`common-math-2`（공통수학2、11）・`algebra`（대수、12）・`calculus-1`（미적분Ⅰ、13）・`probability-and-statistics`（확률과 통계、14）。unit.php で typicalAgeRange と educationalLevel「고등학교」）— 生成スクリプトは `gen_kr_math_cm1_*`・`cm2_*`・`alg_*`・`calc1_*`・`ps_*`（2 行のラッパー）、本体は `tools/kr_h1.py`〜`kr_h5.py` の build(key)、seed は 830NN〜834NN。
共通部品は `tools/kr_hs.py`（kr_mid の上に px（係数リスト → 多項式）・padd・pmul・peval・pdiv・cx（복소수）・surd・mx（행렬 .mx）・roots・W・graph（kurve、data-pf='lg'、xlab で π 目盛り））。kr_common.unit は standard_code の [10공수1-…]・[12대수…]・[12미적Ⅰ-…]・[12확통…] から domain（DOMAIN_HS）と seo_title「… | 고등학교 공통수학1 학습지 (정답 포함)」を作る。
key_big・key_sub に「<」を書かない（plain_text の assert）。負の数を %d で出さない（neg）。数・式の後の助詞は tidy が直すが、<sub> の後（₄C₃을）は直らないので文を変える。表は fr_common.table（.sn-table）。점근선は赤い点線を SVG に足す。
トピック（topic_defs_kr_all）：고등학교の slug は topic_hs_kr() で 1 つずつ割り当てる（他のトピックの out に自動で入る。중학교と同じ slug の polynomial-operations・factoring は従来どおり）。新トピック coordinate-geometry・sets-and-logic・exponents-and-logarithms・trigonometry・sequences・calculus・counting・probability-and-statistics

KR / Math / 공통수학1: 1. polynomial-operations ✓ 2. identities-and-remainder-theorem ✓ 3. factoring ✓ 4. complex-numbers ✓ 5. discriminant ✓ 6. roots-and-coefficients ✓ 7. quadratic-equations-and-functions ✓ 8. maximum-and-minimum-of-quadratic-functions ✓
9. cubic-and-quartic-equations ✓ 10. simultaneous-quadratic-equations ✓ 11. linear-inequalities-and-absolute-values ✓ 12. quadratic-inequalities ✓ 13. counting-principles ✓ 14. permutations ✓ 15. combinations ✓ 16. matrices ✓
KR / Math / 공통수학2: 1. distance-and-internal-division ✓ 2. equations-of-lines ✓ 3. distance-from-a-point-to-a-line ✓ 4. equations-of-circles ✓ 5. circles-and-lines ✓ 6. translations-and-reflections ✓ 7. sets ✓ 8. set-operations ✓
9. propositions-and-conditions ✓ 10. necessary-and-sufficient-conditions ✓ 11. absolute-inequalities ✓ 12. functions ✓ 13. composite-and-inverse-functions ✓ 14. rational-functions ✓ 15. irrational-functions ✓
KR / Math / 대수: 1. radicals-and-roots ✓ 2. exponents ✓ 3. logarithms ✓ 4. common-logarithms ✓ 5. exponential-and-logarithmic-functions ✓ 6. exponential-and-logarithmic-equations ✓ 7. radians-and-general-angles ✓
8. trigonometric-functions ✓ 9. graphs-of-trigonometric-functions ✓ 10. law-of-sines-and-cosines ✓ 11. arithmetic-sequences ✓ 12. geometric-sequences ✓ 13. sigma-notation ✓ 14. recursive-sequences-and-induction ✓
KR / Math / 미적분Ⅰ: 1. limits-of-functions ✓ 2. continuity ✓ 3. derivatives ✓ 4. rules-of-differentiation ✓ 5. tangent-lines-and-mean-value-theorem ✓ 6. increasing-decreasing-and-extrema ✓
7. graphs-and-maximum-minimum ✓ 8. equations-inequalities-and-velocity ✓ 9. indefinite-integrals ✓ 10. definite-integrals ✓ 11. area-between-curves ✓ 12. velocity-and-distance ✓
KR / Math / 확률과 통계: 1. permutations-with-repetition ✓ 2. combinations-with-repetition ✓ 3. binomial-theorem ✓ 4. probability-and-addition-rule ✓ 5. conditional-probability ✓ 6. independence-and-multiplication-rule ✓
7. discrete-random-variables ✓ 8. binomial-distribution ✓ 9. normal-distribution（표준정규분포표を問題に入れる）✓ 10. sampling-and-estimation ✓

KR / Math / 유치원（만 5세、2019 개정 누리과정 자연탐구「생활 속에서 탐구하기」）— grade `kindergarten`（name「유치원」、sort 0）。10까지（数えるのは 20까지）。とても短い文、ほぼ全問に絵。
生成スクリプトは `gen_kr_math_k_*`（build を呼ぶだけ）、本体は `tools/kr_k.py`（UNITS に単元を定義、reseed で kr_g1_num・kr_g1_calc・kr_g1_geo・kr_g2_data の R を入れ替えて再利用、위치와 방향・똑같이 나누기・모양/소리의 규칙・세 줄 비교は自前、le(mk, n) で n を超える数を落とす、이름「하나」は使わない）。
kr_common.unit に domain 引数（유치원は 수 세기와 셈／위치와 모양／길이와 무게 비교／규칙 찾기／분류하기）、standard_code は「누리과정 자연탐구: 생활 속에서 탐구하기」、standard_url は STD_URL_NURI。core.php の grade_standard() で유치원の基準名を「2019 개정 누리과정」に（grade.php・unit.php・preview.php）
1. counting-to-10 ✓ 2. numbers-to-20 ✓ 3. comparing-quantities ✓ 4. ordinal-numbers ✓ 5. putting-together-and-taking-apart ✓ 6. adding-and-taking-away ✓ 7. sharing-and-grouping ✓
8. position-and-direction ✓ 9. shapes ✓ 10. comparing-length-weight-and-capacity ✓ 11. patterns ✓ 12. sorting-and-classifying ✓

KR / Math は유치원・초등 1학년〜고등학교（공통수학1・2、대수、미적분Ⅰ、확률과 통계）まで完了。次は 미적분Ⅱ・기하 などの選択科目か、GDP 順で次の国

CN / Math（义务教育数学课程标准（2022年版）。単元は人教版の順）— country `cn`（name「中国」、lang `zh-CN`、hreflang zh-cn）、subject `math`（数学）、grade `grade-N`（一年级…六年级）、A4。
生成スクリプトは `tools/cn_g1.py`〜`cn_g6.py`（1 学年 1 ファイル、`python3 tools/cn_g5.py [slug…]`。seed は 9N1cc）。共通部品は `tools/cn_common.py`（adopt：台湾版の生成スクリプトを新しい seed で動かし、OpenCC で简体字にして PRE・TERMS で大陸の語（厘米・千克・竖式・数轴・条形统计图・乘法口诀・正比例・周长・棱长 など）に直す。LEAKS で台湾の地名・お金を落とす。build_sets の部品は (maker, 数) か ("tw", モジュール, セット番号, 数[, keep])、数 None は 20 問まで埋める、負の数は最大 |数| 問。run_grade・lesson（怎么想 → 例题 → 常见错误）・unit（seo_title「…｜X年级数学练习题（附答案）」、standard_code「第N学段 · 数与运算」））。
自前の問題は `tools/cn_low.py`（1〜2 年级：位置・数・図形・钟表・人民币・规律）、`cn_mid.py`（竖式・倍・方向・两位数乘法・小数・公顷・鸡兔同笼）、`cn_high.py`（数对・方向和距离・税率利率・圆柱圆锥・鸽巢问题・解方程（正の数だけ））。
domain は 数与运算／数量关系／图形的认识与测量／图形的位置与运动／统计与概率（1〜2 年级は 数据分类）。数は 4 桁でもカンマなし。π は 3.14。
UI 文言は core.php の 'zh-CN'（zt() で繁体字の文言を简体字に）、トピックは topics.php の `topic_defs_cn()`。プレビュー画像は Noto Sans SC（PV_CJK = 'sc'）。**cn の単元を足したら `python3 tools/build_cjk_font.py` を実行してフォントもコミット**
CN / Math / 一年级: position, numbers-within-10, composing-numbers-within-10, addition-and-subtraction-within-10, 3d-shapes, numbers-11-to-20, addition-with-carrying-within-20, telling-time-hours, 2d-shapes, subtraction-with-borrowing-within-20, sorting-and-classifying, numbers-to-100, rmb, add-and-subtract-within-100, finding-patterns, number-sentences ✓
CN / Math / 二年级: centimeters-and-meters, written-addition-and-subtraction-within-100, angles, meaning-of-multiplication, multiplication-tables, telling-time, data-collection, division-within-tables, mixed-operations, division-with-remainders, numbers-to-10000, grams-and-kilograms, estimation ✓
CN / Math / 三年级: hours-minutes-seconds, add-subtract-within-10000, measurement-units, meaning-of-times, multiply-by-one-digit, rectangles-and-squares, fractions, directions, divide-by-one-digit, tables, two-digit-by-two-digit-multiplication, area, years-months-days, decimals, estimation, two-step-problems ✓
CN / Math / 四年级: large-numbers, hectares-and-square-kilometers, measuring-angles, three-digit-by-two-digit, parallel-perpendicular-and-quadrilaterals, divide-by-two-digit, bar-graphs-and-averages, order-of-operations, laws-of-operations, meaning-and-properties-of-decimals, triangles, adding-and-subtracting-decimals, axial-symmetry, rounding-and-approximate-numbers, chickens-and-rabbits, observing-objects ✓
CN / Math / 五年级: multiplying-decimals, position-ordered-pairs, dividing-decimals, likelihood, simple-equations, area-of-polygons, factors-and-multiples, cuboids-and-cubes, meaning-and-properties-of-fractions, rotation, adding-and-subtracting-fractions, line-graphs ✓
CN / Math / 六年级: multiplying-fractions, position-and-direction-2, dividing-fractions, ratios, circles, percentages, pie-charts, negative-numbers, discounts-and-interest, cylinders-and-cones, proportion, pigeonhole-principle ✓
CN / Math / 七〜九年级（初中、第四学段。domain は 数与代数／图形与几何／统计与概率（cn_common.DOMAIN_JH、dom は N・A・G・T・D））— 生成スクリプトは `tools/cn_g7.py`〜`cn_g9.py`（seed は 97101〜・98101〜・99101〜）。台湾の國中の生成スクリプトを adopt で再利用（TERMS で 同旁内角・消元法・方程组・科学记数法・垂直平分线・频数/频率・直角边（股）・勾股定理・≌・∽・≤ ≥・概率・公式法 などに直す。筝形・筊・列联表は no() で落とす）。
自前の問題は `tools/cn_jh.py`（平方根・立方根、不等式组、一元一次方程の応用、分式、加权平均数・方差、旋转・中心对称、反比例函数、锐角三角函数、投影、用频率估计概率）。負の数は台湾版と同じ「－」。build_sets の maker も負の数で「最大 |数| 問」。
小学と同じ slug は使わない（トピックが slug だけで決まるため：八年级は algebraic-fractions・triangles-and-polygons、九年级は circle-geometry）。
CN / Math / 七年级: rational-numbers, adding-and-subtracting-rational-numbers, multiplying-and-dividing-rational-numbers, powers-and-scientific-notation, algebraic-expressions, linear-equations, linear-equation-word-problems, geometric-figures, intersecting-and-parallel-lines, real-numbers, coordinate-plane, systems-of-linear-equations, inequalities, data-collection-and-description ✓
CN / Math / 八年级: triangles-and-polygons, congruent-triangles, axial-symmetry, multiplying-polynomials, multiplication-formulas, factorization, algebraic-fractions, quadratic-radicals, pythagorean-theorem, parallelograms, linear-functions, data-analysis ✓
CN / Math / 九年级: quadratic-equations, quadratic-functions, rotation, circle-geometry, probability, inverse-proportion-functions, similarity, trigonometric-functions, projections-and-views ✓
CN / Math / 高中（普通高中数学课程标准（2017年版2020年修订）、人教A版 2019 の章の順）— grade は教科書：`required-1`（必修第一册、sort 10）・`required-2`（必修第二册）・`elective-1`〜`elective-3`（选择性必修第一〜三册、sort 12〜14）。unit.php で 15〜18 歳と educationalLevel「普通高中」、core.php の grade_standard() で基準名を高中の课标に。standard_url は教育部 2020 年の通知（cn_common.STD_URL_HS）、standard_code は「必修课程 · 函数」形式、domain は 预备知识／函数／几何与代数／概率与统计（DOMAIN_HS、dom は P・F・G・S）。
生成スクリプトは `tools/cn_hsa.py`（必修第一册）、`cn_hsb.py required-2|elective-1`、`cn_hsc.py elective-2|elective-3`（seed は 2011NN・2021NN・2031NN・2041NN・2051NN）。問題はすべて自前、共通部品は `tools/cn_hsu.py`（S・P・poly・lin・rt・pis・iv・sup、mcq は tidy で -3 → －3、「＋ －」→「－」、1x → x を直す）。各 maker は種類（kind）ごとに 20 問以上作れるようにする（足りないと pick が止まる）。kb・ks・title・meta に < を書かない。
初中・小学と同じ slug は使わない（angles-and-trigonometric-functions、equations-of-circles）。トピックに 集合、逻辑与不等式・三角函数・向量与复数・解析几何・数列与导数・计数原理与概率分布 を足した。
preview.php の pv_cjk_safe()：Noto Sans SC/TC/KR にない上付き・下付き文字（⁴〜⁹、ₙ、ŷ、⅓ など）を ^5・n などに置き換える
CN / Math / 必修第一册: sets, logic, quadratic-inequalities, functions, exponents-and-logarithms, exponential-and-logarithmic-functions, angles-and-trigonometric-functions, trigonometric-identities, graphs-of-trigonometric-functions ✓
CN / Math / 必修第二册: plane-vectors, solving-triangles, complex-numbers, solid-geometry, statistics, probability ✓
CN / Math / 选择性必修第一册: space-vectors, lines, equations-of-circles, ellipses, hyperbolas, parabolas ✓
CN / Math / 选择性必修第二册: sequences, derivatives, applications-of-derivatives ✓
CN / Math / 选择性必修第三册: counting-principles, binomial-theorem, random-variables, conditional-probability-and-normal-distribution, paired-data ✓
CN / Math / 幼儿园大班（5～6岁、《3-6岁儿童学习与发展指南》科学领域・数学认知（教育部 2012）。grade `kindergarten`（name「幼儿园大班」、sort 0）。10 以内（数えるのは 20 まで）、とても短い文、ほぼ全問に絵）— 生成スクリプトは `tools/cn_k.py`（seed は 901NN）。cn_low の問題と自前の問題（按群数数・比多少・序数・分与合・実物の加減・長短/高矮/粗細/厚薄/軽重・量的相对性・图形・分类・统计图・规律）。
cn_common.unit は g == 0 で standard_code「数学认知 · 感知和理解数、量及数量关系」（DOMAIN_K：U 目标1・N 目标2・G 目标3）、standard_url は《指南》全文（STD_URL_K、unicef.cn の PDF）。core.php の grade_standard()、unit.php に cn の kindergarten（educationalLevel 幼儿园大班）。一年级と同じ slug は使わない
CN / Math / 幼儿园大班: counting-to-10, numbers-to-20, counting-in-groups, comparing-quantities, ordinal-numbers, splitting-and-combining-numbers, adding-and-taking-away, comparing-length-height-thickness-and-weight, recognizing-shapes, position-and-direction, repeating-patterns, sorting-and-recording ✓
CN / Math は幼儿园大班・小学一年级〜高中（必修・选择性必修）まで完了。mq-geo.js と mq.php の MQ_GEO（このリポジトリの外）に cn があるか確認する

ID / Matematika（Kurikulum Merdeka、Capaian Pembelajaran：Keputusan Kepala BSKAP No. 046/H/KR/2025。数学は BKPDM 020/2026 で変更なし）— country `id`（name「Indonesia」、lang `id`、hreflang id-id、standard「Kurikulum Merdeka」）、subject `matematika`、grade `kelas-N`（name「Kelas N」、unit.php で N+5〜N+6 歳と educationalLevel Sekolah Dasar など）、A4。
生成スクリプトは `tools/id_k4.py [番号…]`（seed は 40400 + sort、問題関数は id_k4a・id_k4b・id_k4c の uN()）、共通部品は `tools/id_common.py`（num（1.000 から点で区切る）・dec（コンマ）・rp（Rp6.750）・Kids（Buku Siswa の名前）・mcq（足りない誤答は桁に合わせた近い数、0 以下は出さない）・lesson（Cara berpikir → Contoh → Kesalahan yang sering terjadi）・make_unit（seo_title「X Kelas 4 SD: Latihan Soal dan Lembar Kerja dengan Kunci Jawaban」、standard_code「Fase B · Bilangan」）・garis_bilangan・nilai_tempat・blok・diagram_batang・bersusun。de_common の絵を D.num を差し替えて使う）。
インドネシア語、kamu で話しかける短い文。記号は × と :（割り算）、余りは「29 : 4 = 7 sisa 1」。単元の範囲は CP の Fase B（kelas 3–4）：数は 10.000 まで、足し算・引き算は 1.000 まで、かけ算・わり算は 100 まで、お金はリブ単位。
domain は CP の elemen（B Bilangan／A Aljabar／P Pengukuran／G Geometri／D Analisis Data dan Peluang）、standard_url は internal-portal.kemdikbud.go.id/download/file/1933。
UI 文言は core.php の 'id'（T と J）、トピックは topics.php の `topic_defs_id()`（data の in は (^|-)data(-|$)、out に datar）、topic.php・topics.php に $idn の文言。みんなでクイズ（mq.js）にはまだ id の言語がない（英語で出る）

ID / Matematika / Kelas 4（Fase B）
1. bilangan-cacah-sampai-10000 ✓ 2. membandingkan-dan-mengurutkan-bilangan ✓ 3. menyusun-dan-menguraikan-bilangan ✓ 4. penjumlahan-dan-pengurangan ✓ 5. perkalian-dan-pembagian ✓ 6. faktor-dan-kelipatan ✓
7. soal-cerita ✓ 8. pecahan ✓ 9. pecahan-senilai ✓ 10. desimal-dan-persen ✓ 11. kalimat-matematika ✓ 12. pola-gambar-dan-pola-bilangan ✓ 13. pengukuran-panjang-dan-berat ✓
14. luas-dan-volume ✓ 15. bangun-datar ✓ 16. menyusun-dan-mengurai-bangun-datar ✓ 17. piktogram-dan-diagram-batang ✓
ID / Matematika / Kelas 5（Fase C：数は 1.000.000 まで、四則は 100.000 まで、KPK・FPB、分数の四則（分数 × ÷ 自然数）、小数は 1 桁、比と比例、角度、時間、立方体・直方体、マス目の地図、確率）— 生成スクリプトは `tools/id_k5.py [番号…]`（seed は 40500 + sort、問題関数は id_k5a（Bilangan 1〜10）・id_k5b（11〜20）の uN()）。
id_common.mcq は分数（<span class='fr'>）の誤答が足りないとき分子・分母を 1 ずらして補う。角度の図は gen_au_maths_y5_angles（protractor_svg・angle_fig）、立体は kr_pics56.iso_cubes（「앞」→ depan）と id_k4b.kubus、jaring-jaring は fold() で立方体に折れるか判定（11 種類）
1. bilangan-cacah-sampai-1000000 ✓ 2. penjumlahan-dan-pengurangan ✓ 3. perkalian ✓ 4. pembagian ✓ 5. kpk-dan-fpb ✓ 6. pecahan-campuran ✓ 7. penjumlahan-dan-pengurangan-pecahan ✓
8. perkalian-dan-pembagian-pecahan ✓ 9. desimal ✓ 10. soal-cerita-uang ✓ 11. kalimat-matematika ✓ 12. pola-bilangan ✓ 13. rasio-dan-proporsi ✓ 14. keliling-dan-luas-bangun-datar ✓
15. mengukur-sudut ✓ 16. durasi-waktu ✓ 17. kubus-dan-balok ✓ 18. peta-berpetak ✓ 19. tabel-frekuensi-dan-diagram ✓ 20. peluang ✓
ID / Matematika / Kelas 3（Fase B：数は 1.000 まで、九九は 10 × 10 まで、分数は単位分数と同分母、お金は Rp20.000 まで）— 生成スクリプトは `tools/id_k3.py [番号…]`（seed は 40300 + sort）。
数・計算・お金は自前（uang_svg：Rp100〜Rp1.000 硬貨、Rp1.000〜Rp20.000 札）。かけ算・わり算・分数・パターン・kalimat matematika・測定・図形・データは Kelas 4 の問題関数を maker(d4, 名前) で取り出し、lim(mk, 1000) で 1.000 までに絞って再利用（文・lesson・faq は Kelas 3 向けに新しく）
1. bilangan-cacah-sampai-1000 ✓ 2. membandingkan-dan-mengurutkan-bilangan ✓ 3. penjumlahan ✓ 4. pengurangan ✓ 5. perkalian ✓ 6. pembagian ✓ 7. pecahan ✓
8. uang ✓ 9. pola-bilangan-dan-gambar ✓ 10. kalimat-matematika ✓ 11. pengukuran-panjang-dan-berat ✓ 12. luas-dan-volume ✓ 13. bangun-datar ✓ 14. piktogram-dan-diagram-batang ✓
ID / Matematika / Kelas 6（Fase C の応用：四則混合、概数、KPK・FPB の文章題、分数・小数・百分率、縮尺、n 番目の数、二段階の方程式、台形・たこ形、三角形の角、体積、8 方位、カレンダー、最頻値）— 生成スクリプトは `tools/id_k6.py [番号…]`（seed は 40600 + sort）。
Kelas 5 の問題関数を maker(d5, 名前) で再利用し、自前の問題を足す（d2：百分の一単位の整数 → 0,25、kompas：8 方位の図、tri_svg：三角形の角、dots_svg：三角数・四角数・長方形数）
1. operasi-hitung-campuran ✓ 2. pembulatan-dan-taksiran ✓ 3. kpk-dan-fpb-dalam-soal-cerita ✓ 4. pecahan-desimal-dan-persen ✓ 5. operasi-hitung-pecahan ✓ 6. operasi-hitung-desimal ✓
7. persen ✓ 8. soal-cerita-pecahan ✓ 9. perbandingan-dan-skala ✓ 10. pola-bilangan-dan-pola-titik ✓ 11. persamaan-sederhana ✓ 12. luas-bangun-datar-dan-gabungan ✓
13. sudut-dan-segitiga ✓ 14. bangun-ruang-dan-volume ✓ 15. lokasi-dan-arah-mata-angin ✓ 16. waktu-jadwal-dan-kalender ✓ 17. modus-dan-penyajian-data ✓ 18. peluang ✓
トピック（topic_defs_id）：operasi-hitung-campuran→perkalian-dan-pembagian、persamaan→aljabar-dan-pola、arah-mata-angin→geometri、bangun-ruang はgeometri だけ、luas- は pengukuran だけ
ID / Matematika / Kelas 1・2（Fase A：Kelas 1 は 20 まで、Kelas 2 は 100 まで（計算は CP のとおり 20 まで）。とても短い文、ほぼ全問に絵）— 生成スクリプトは `tools/id_k12.py 1|2 [番号…]`（seed は 40000 + 100 × 学年 + sort）。
k_pics の絵に pic() でインドネシア語の aria-label（BENDA：apel・bintang・bola…、インドネシア語は複数形なし）。問題関数は m_hitung・m_fakta（cross で 10 を越えるか）・m_cerita・m_pola・m_data（turus・pikto）など、範囲を引数で渡して両学年で使う。0 が答えになる計算は作らない。
balok の絵は自前（balok_svg）。Kelas 2 の平面図形・図形の合成は Kelas 4 の問題関数（id_k4c u15・u16）を maker_of で使う（berapa は 20 までに絞る）。
トピック：posisi→geometri、kesamaan・lompat-hitung→aljabar-dan-pola、mengukur→pengukuran（out に sudut）、puluhan-dan-satuan→bilangan-cacah、setengah→pecahan
Kelas 1: 1. bilangan-sampai-10 ✓ 2. penjumlahan-sampai-10 ✓ 3. pengurangan-sampai-10 ✓ 4. bilangan-11-sampai-20 ✓ 5. membandingkan-dan-mengurutkan-bilangan ✓ 6. penjumlahan-dan-pengurangan-sampai-20 ✓ 7. soal-cerita ✓
8. bangun-datar ✓ 9. bangun-ruang ✓ 10. membandingkan-panjang-dan-berat ✓ 11. pola-gambar-dan-bilangan ✓ 12. posisi-benda ✓ 13. turus-dan-piktogram ✓
Kelas 2: 1. bilangan-sampai-100 ✓ 2. puluhan-dan-satuan ✓ 3. membandingkan-dan-mengurutkan-bilangan ✓ 4. lompat-hitung-dan-bilangan-genap-ganjil ✓ 5. penjumlahan-dan-pengurangan-sampai-20 ✓ 6. kesamaan-dan-tanda-sama-dengan ✓ 7. soal-cerita ✓
8. setengah-dan-seperempat ✓ 9. mengukur-dengan-satuan-tidak-baku ✓ 10. bangun-datar-dan-bangun-ruang ✓ 11. menyusun-dan-mengurai-bangun-datar ✓ 12. pola ✓ 13. turus-dan-piktogram ✓
ID / Matematika / Kelas 7–9（SMP、Fase D）— 生成スクリプトは `tools/id_smp.py 7|8|9 [番号…]`（seed は 40000 + 100 × 学年 + 番号）、単元は `tools/id_smp7.py`・`id_smp8.py`・`id_smp9.py` の UNITS（問題関数はすべて自前のインドネシア語）。
共通部品は id_smp（M＝負の数も残す 4 択、誤答が 3 つそろわないと None。MN・MD は数・小数の答え（unit="rupiah" で Rp、"°" は空白なし）、sn・fq・dz・par・expr・lin・sup・pw、図：numline・kosy（de_k8）・kurve（de_k10）・figure（fr_c4）・poly_ang（多角形と内角）・sejajar（平行線と横断線の 8 つの角）・pie）。float を sn・fq に渡すと ValueError（Fraction を使う）。
id_common.make_unit の seo_title は Kelas 7–9 で「SMP」。トピックに bilangan-bulat-dan-rasional・pangkat-dan-akar・persamaan-dan-fungsi を足した（aritmetika-sosial→pecahan-desimal-dan-persen、statistika→data-dan-peluang）
Kelas 7: 1. bilangan-bulat ✓ 2. operasi-bilangan-bulat ✓ 3. bilangan-rasional ✓ 4. operasi-bilangan-rasional ✓ 5. rasio-dan-proporsi ✓ 6. bentuk-aljabar ✓ 7. persamaan-linear-satu-variabel ✓
8. pertidaksamaan-linear-satu-variabel ✓ 9. aritmetika-sosial ✓ 10. garis-dan-sudut ✓ 11. segitiga-dan-segi-empat ✓ 12. luas-permukaan-dan-volume-kubus-dan-balok ✓ 13. penyajian-data ✓ 14. peluang ✓
Kelas 8: 1. bilangan-berpangkat ✓ 2. notasi-ilmiah ✓ 3. teorema-pythagoras ✓ 4. relasi-dan-fungsi ✓ 5. persamaan-garis-lurus ✓ 6. sistem-persamaan-linear-dua-variabel ✓ 7. faktorisasi-bentuk-aljabar ✓
8. lingkaran ✓ 9. prisma-dan-limas ✓ 10. transformasi-geometri ✓ 11. statistika ✓ 12. peluang-empirik-dan-teoretik ✓
Kelas 9: 1. bentuk-akar ✓ 2. persamaan-kuadrat ✓ 3. fungsi-kuadrat ✓ 4. kesebangunan ✓ 5. kekongruenan ✓ 6. sudut-pusat-dan-sudut-keliling ✓ 7. tabung-kerucut-dan-bola ✓
8. dilatasi ✓ 9. ukuran-penyebaran-data ✓ 10. peluang-kejadian-majemuk ✓ 11. pola-bilangan-dan-barisan ✓
ID / Matematika / Kelas 10–12（SMA。Kelas 10 は Fase E、Kelas 11–12 は Fase F）— 生成スクリプトは `tools/id_smp.py 10|11|12 [番号…]`（seed は 40000 + 100 × 学年 + 番号）、単元は `tools/id_sma10.py`・`id_sma11.py`・`id_sma12.py` の UNITS（id_smp.modname が 10 以上で id_smaN を読む。FASE で standard_text の末尾と fase を切り替え、seo_title は SMA）。
共通部品は id_smp（mat：行列 .mx、det=True で行列式）と id_sma10（LOG・SIN/COS/TAN・surd・sub・neg）、id_sma12（P：{次数: 係数} → 多項式（変数を引数で）・deriv・integ・ev・nPr・nCr）。対数は `<sup>2</sup>log 8`、特別角は「½√3」、区間・不等号は &lt; &gt;。
トピック（topic_defs_id）に trigonometri（trigonometri・aturan-sinus）と kalkulus（limit・turunan・integral）を足した。eksponen・logaritma→pangkat-dan-akar、barisan・polinomial・matriks→aljabar-dan-pola、bunga-majemuk→pecahan-desimal-dan-persen、vektor・dimensi-tiga→geometri、korelasi・simpangan・pencacahan・permutasi→data-dan-peluang。bilangan-kompleks はトピックなし
Kelas 10: 1. eksponen ✓ 2. logaritma ✓ 3. barisan-dan-deret ✓ 4. bunga-majemuk-pertumbuhan-dan-peluruhan ✓ 5. vektor ✓ 6. perbandingan-trigonometri ✓ 7. aturan-sinus-kosinus-dan-luas-segitiga ✓
8. sistem-persamaan-linear-tiga-variabel ✓ 9. sistem-pertidaksamaan-linear-dua-variabel ✓ 10. persamaan-dan-fungsi-kuadrat ✓ 11. statistika-data-berkelompok ✓ 12. peluang-kejadian-saling-lepas-dan-saling-bebas ✓
Kelas 11: 1. komposisi-fungsi-dan-fungsi-invers ✓ 2. persamaan-lingkaran ✓ 3. korelasi-dan-regresi-linear ✓ 4. peluang-bersyarat ✓ 5. polinomial ✓ 6. matriks ✓ 7. fungsi-trigonometri ✓ 8. bilangan-kompleks ✓ 9. ragam-dan-simpangan-baku ✓
Kelas 12: 1. kaidah-pencacahan ✓ 2. permutasi-dan-kombinasi ✓ 3. limit-fungsi-aljabar ✓ 4. turunan-fungsi-aljabar ✓ 5. aplikasi-turunan ✓ 6. integral-tak-tentu ✓ 7. integral-tentu-dan-luas-daerah ✓ 8. transformasi-geometri-dan-komposisinya ✓ 9. dimensi-tiga ✓
ID / Matematika / TK（TK B、5〜6歳、Fase Fondasi）— grade `tk`（name「TK」、sort 0）。10 まで（数えるのは 20 まで）、とても短い文、ほぼ全問に絵、記号（&lt; &gt;）は使わない。生成スクリプトは `tools/id_tk.py [番号…]`（seed は 40000 + 番号）。id_k12（Kelas 1・2）の問題関数を範囲を絞って再利用し、比べる・分ける・時間（f_common.sky_svg・days_svg）・容量（glasses_svg）・分類・色は自前。id_common.make_unit は grade="tk" で seo_title「… untuk TK: Lembar Kerja …」、unit.php で educationalLevel TK B / Taman Kanak-kanak / PAUD
1. membilang-sampai-10 ✓ 2. bilangan-sampai-20 ✓ 3. membandingkan-banyak-benda ✓ 4. urutan-bilangan ✓ 5. menambah-benda ✓ 6. mengurangi-benda ✓ 7. membagi-sama-banyak ✓
8. mengenal-bentuk ✓ 9. posisi-dan-arah ✓ 10. membandingkan-ukuran ✓ 11. waktu-sehari-hari ✓ 12. pola ✓ 13. mengelompokkan-dan-data ✓
ID / Matematika は TK・Kelas 1〜12（SD・SMP・SMA）まで完了。次は GDP 順で次の国

TR / Matematik（Türkiye Yüzyılı Maarif Modeli、İlkokul Matematik Dersi Öğretim Programı 2024）— country `tr`（name「Türkiye」、lang `tr`、hreflang tr-tr、standard「Türkiye Yüzyılı Maarif Modeli」）、subject `matematik`、grade `N-sinif`（name「3. Sınıf」、unit.php で N+5〜N+6 歳と educationalLevel İlkokul／Ortaokul／Lise）、A4。
生成スクリプトは `tools/tr_s3.py [番号…]`（seed は 90300 + 番号、問題関数は tr_s3a（1〜10）・tr_s3b（11〜22）の UNITS）、共通部品は `tools/tr_common.py`（num（1.000 から点で区切る）・dec（コンマ）・tl・kurus・para（kuruş → 3 TL 25 kuruş）・oku（数詞）・saat_oku（「saat üçü on geçiyor」「saat beşe çeyrek var」）・hm（08.30）・Kids・mcq・M（誤答が足りないと None）・lesson（Nasıl düşünürüz? → Örnek → Sık yapılan hatalar）・make_unit（seo_title「Kesirler 3. Sınıf Matematik: Çalışma Kâğıdı ve Cevaplı Test」、key_big ≤ 40・key_sub ≤ 60）・図：sayi_dogrusu・basamak_tablosu・bloklar・sutun_grafigi・cetele・alt_alta・saat_svg）。
トルコ語、sen で話しかける短い文。記号は × と ÷、余りは「bölüm 3, kalan 2」。**数字・人名の直後に接尾辞を付けない**（「345 sayısının」のように語を挟む）。文頭の大文字は tr_s3a.cap（i → İ、ı → I）、疑問の小辞は mi()（「75 dakika mı」）。所有の文は属格＋所有（「Bir küpün kaç köşesi vardır?」）。
domain は S Sayılar ve Nicelikler／I İşlemlerden Cebirsel Düşünmeye／G Nesnelerin Geometrisi／V Veriye Dayalı Araştırma、standard_code は MAT コード（「MAT.3.1.1, MAT.3.1.2」）、standard_url は tymm.meb.gov.tr のプログラム PDF。
UI 文言は core.php の 'tr'（T と js_text、sep '.'）、プレビュー画像の大文字は pv_up（PV_TR で i → İ）、トピックは topics.php の `topic_defs_tr()`（sayilar・toplama-ve-cikarma・carpma-ve-bolme・kesirler・oruntuler-ve-esitlik・olcme・geometri・veri）、topic.php・topics.php に $trk の文言。みんなでクイズ（mq.js）にはまだ tr の言語がない（英語で出る）

TR / Matematik / 3. Sınıf
1. 1000e-kadar-sayilar ✓ 2. sayilari-siralama-ve-yuvarlama ✓ 3. ritmik-sayma ✓ 4. tek-ve-cift-sayilar ✓ 5. oruntuler ✓ 6. kesirler ✓ 7. saat-okuma ✓ 8. zaman-olcu-birimleri ✓ 9. uzunluk-ve-kutle-olcme ✓ 10. paralarimiz ✓
11. toplama-islemi ✓ 12. cikarma-islemi ✓ 13. carpma-islemi ✓ 14. bolme-islemi ✓ 15. dort-islem-problemleri ✓ 16. esitlik ✓ 17. geometrik-cisimler ✓ 18. geometrik-sekiller ✓ 19. cevre-uzunlugu ✓ 20. sivi-olcme ✓ 21. simetri ✓ 22. veri-toplama-ve-nokta-grafigi ✓
TR / Matematik / 4.〜6. Sınıf — 生成スクリプトは `tools/tr_run.py 学年 [番号…]`（seed は 90000 + 100 × 学年 + 番号、単元は tr_sNa・tr_sNb・tr_sNc の UNITS、図や部品は `tools/tr_g.py`：ff・mf・dz・grid_shape・poly（辺の長さ・目盛り・直角）・circle_fig・pie_chart・parallel_fig（平行線と横断線の 8 つの角、コード 1〜8）・stem_leaf・freq_table・dot_plot・withopts（選択肢を問題文に入れて重複を避ける））。角度の図は gen_au_maths_y5_angles の Pic・angle_fig・protractor_svg・shape_svg。
5.〜6. sınıf は Ortaokul Matematik Dersi Öğretim Programı（2026 DÖP、tr_common.STD_URL_ORTA）。domain は C5／C6（İşlemlerle Cebirsel Düşünme（ve Değişimler））・GS Geometrik Şekiller・GN Geometrik Nicelikler・IA İstatistiksel Araştırma Süreci・VO Veriden Olasılığa（4. sınıf の olasılık・veri は OV）。
トルコ語の小文字は tr_common.low()（İ → i、I → ı。.lower() を使わない）。数字の後の接尾辞は固定の文だけに書く（1’den、%20’si）。変数の数字の後には付けない
TR / Matematik / 4. Sınıf
1. alti-basamakli-sayilar ✓ 2. basamak-ve-boluk ✓ 3. siralama-ve-yuvarlama ✓ 4. ritmik-sayma ✓ 5. oruntuler ✓ 6. kesir-cesitleri ✓ 7. denk-kesirler ✓ 8. kesirleri-karsilastirma ✓ 9. bir-coklugun-kesri ✓
10. kesirlerle-toplama-ve-cikarma ✓ 11. uzunluk-ve-kutle-donusumleri ✓ 12. zihinden-toplama-ve-cikarma ✓ 13. dort-basamakli-toplama-ve-cikarma ✓ 14. carpma-ve-bolmede-tahmin ✓ 15. zihinden-carpma-ve-bolme ✓
16. carpma-ve-bolme ✓ 17. dort-islem-problemleri ✓ 18. esitlik-ve-esit-degildir ✓ 19. geometrik-cisimlerin-acinimlari ✓ 20. ucgen-kare-ve-dikdortgen ✓ 21. cevre-ve-alan ✓ 22. acilar ✓ 23. simetri ✓
24. imkansiz-olabilir-kesin ✓ 25. veri-toplama-ve-grafikler ✓
TR / Matematik / 5. Sınıf（2026 DÖP のテーマ順）
1. temel-geometrik-kavramlar ✓ 2. aci-olcme ✓ 3. dogrularin-olusturdugu-acilar ✓ 4. cokgenler ✓ 5. ucgenler-ve-cember ✓ 6. buyuk-sayilar ✓ 7. dogal-sayilarla-problemler ✓ 8. dikdortgenin-cevresi ✓
9. dikdortgenin-alani ✓ 10. cevre-ve-alan-iliskisi ✓ 11. kesirler ✓ 12. ondalik-gosterim ✓ 13. yuzdeler ✓ 14. farkli-gosterimleri-karsilastirma ✓ 15. veri-ve-grafikler ✓ 16. esitlik-ve-islem-ozellikleri ✓
17. islem-onceligi ✓ 18. oruntuler ✓ 19. algoritmalar ✓ 20. olasilik ✓
TR / Matematik / 6. Sınıf（EBOB・EKOK の語は使わない（DÖP のとおり）。π は 3 と 3,14。devirli は <span class='ov'>）
1. carpanlar-ve-katlar ✓ 2. bolunebilme-kurallari ✓ 3. asal-sayilar-ve-asal-carpanlar ✓ 4. ortak-bolenler-ve-ortak-katlar ✓ 5. ondalik-gosterimde-basamak-degeri ✓ 6. kesir-ve-bolme-iliskisi ✓
7. kesirlerle-islemler ✓ 8. ondalik-gosterimlerle-islemler ✓ 9. yuzde-problemleri ✓ 10. uzunluk-olcme ✓ 11. cebirsel-ifadeler ✓ 12. oruntuler-ve-cebirsel-ifadeler ✓ 13. algoritmalar-ve-cebirsel-ifadeler ✓
14. paralel-dogrular-ve-kesen ✓ 15. dortgenler ✓ 16. ucgen-ve-dortgende-acilar ✓ 17. alan-olcu-birimleri ✓ 18. paralelkenar-ve-ucgenin-alani ✓ 19. cember-uzunlugu-ve-pi ✓ 20. merkez-acisi-ve-yay ✓
21. veri-analizi ✓ 22. deneysel-olasilik ✓
トピック（topic_defs_tr）：sayilar・toplama-ve-cikarma・carpma-ve-bolme・carpanlar-ve-bolunebilme・kesirler（Kesirler, Ondalık Gösterim ve Yüzde）・oruntuler-ve-esitlik（Örüntüler, Eşitlik ve Cebir）・olcme・geometri・veri・olasilik
TR / Matematik / 7. Sınıf（2026 DÖP。負の数は「−」、tr_g7.py に sn（符号付きの数・分数）・par・dq・dpar・ondalik（循環小数は <span class='ov'>）・lin・terms・gen（名前の属格：Elif’in・Can’ın・Duru’nun）。単元は tr_s7a（1〜9）・tr_s7b（10〜18）・tr_s7c（19〜27）。立体の図は kr_pics56 の iso_cubes（「앞」→「Ön」）・views_panel・box_svg。DOMAIN に D Dönüşüm・C8 Cebirsel Düşünme ve Değişimler を足した）
1. tam-sayilar-ve-rasyonel-sayilar ✓ 2. rasyonel-sayilarin-ondalik-gosterimi ✓ 3. rasyonel-sayilari-karsilastirma-ve-siralama ✓ 4. rasyonel-sayilarla-toplama-ve-cikarma ✓ 5. rasyonel-sayilarla-carpma-ve-bolme ✓ 6. rasyonel-sayi-problemleri ✓
7. oran ✓ 8. oranti ✓ 9. dogru-oranti-problemleri ✓ 10. cebirsel-ifadelerle-islemler ✓ 11. birinci-dereceden-bir-bilinmeyenli-denklemler ✓ 12. birinci-dereceden-bir-bilinmeyenli-esitsizlikler ✓
13. denklem-ve-esitsizlik-problemleri ✓ 14. sayilarla-ispat-ve-oruntuler ✓ 15. cebirsel-islemler-ve-algoritma ✓ 16. yansima-donusumu ✓ 17. orta-dikme-ve-aciortay ✓ 18. ucgende-kenarortay-aciortay-ve-yukseklik ✓
19. es-kuplerle-yapilar-ve-gorunumleri ✓ 20. dikdortgenler-prizmasinin-yuzey-alani ✓ 21. dikdortgenler-prizmasinin-hacmi ✓ 22. hacim-olcme-birimleri ✓ 23. dairenin-ve-daire-diliminin-alani ✓ 24. eskenar-dortgen-ve-yamugun-alani ✓
25. veri-analizi-ve-ortalama-mutlak-sapma ✓ 26. teorik-olasilik-ve-tumleyen-olay ✓ 27. ayrik-ve-ayrik-olmayan-olaylar ✓
トピックに rasyonel-sayilar（Tam Sayılar ve Rasyonel Sayılar）・oran-ve-oranti・denklemler-ve-esitsizlikler を足した。hacim・hacmi→olcme（geometri の out）、olcme の out は (^|-)aci（hacim の「aci」に当たらないように）、kup・yansima→geometri、olaylar→olasilik
TR / Matematik / 8. Sınıf（2026 DÖP。単元は tr_s8a（1〜12：S・C8）・tr_s8b（13〜23：GS・GN・D・IA・VO）。図は id_smp.kosy・figure（右角は (頂点, A, B)）。「en uzundur・en kısadır」「kaç ayrıta／köşeye／yüze」に注意）
1. uslu-ifadeler ✓ 2. uslu-ifadelerle-islemler ✓ 3. bilimsel-gosterim ✓ 4. karekoklu-ifadeler ✓ 5. rasyonel-ve-irrasyonel-sayilar ✓ 6. gercek-sayilar-ve-sayi-araliklari ✓
7. dik-koordinat-sistemi ✓ 8. dogrusal-iliskiler-ve-fonksiyonlar ✓ 9. dogrusal-fonksiyonlarin-grafikleri ✓ 10. egim ✓ 11. iki-dogrusal-fonksiyonun-durumu ✓ 12. dogrusal-fonksiyon-problemleri-ve-algoritma ✓
13. ucgende-aci-kenar-iliskisi ✓ 14. ucgen-esitsizligi ✓ 15. eslik ✓ 16. benzerlik ✓ 17. pisagor-bagintisi ✓ 18. cisimlerin-yuzey-acinimlari ✓ 19. silindirin-yuzey-alani-ve-hacmi ✓
20. oteleme-donusumu ✓ 21. koordinat-duzleminde-oteleme-ve-yansima ✓ 22. veri-analizi-ve-yorumlama ✓ 23. olasilik-yaklasimlari ✓
トピックに uslu-ve-karekoklu-ifadeler・dogrusal-fonksiyonlar を足した（oruntuler・veri の out に dogrusal、denklemler の out に ucgen-esitsizligi）。eslik・benzerlik・pisagor・oteleme→geometri
TR / Matematik / 1.〜2. Sınıf（İlkokul 2024 程序。1. sınıf は 20 まで（ritmik sayma 100 まで、toplama eldesiz）、2. sınıf は 100 まで（eldeli、çarpma 5 まで、bölme 20 まで kalansız）。とても短い文、ほぼ全問に絵）— `python3 tools/tr_run.py 1|2`、単元は tr_s1a・tr_s2a、問題関数と絵は `tools/tr_p12.py`（k_pics の絵にトルコ語の aria-label、BENDA・SHAPE・CISIM、izgara（yönerge の kareli zemin）、es_svg（eş şekiller、同じ縮尺）、cetvel、A.para_svg のお金）。2. sınıf の simetri は tr_s3b.u21 の問題関数（from_unit）
1. sınıf: 1. 20ye-kadar-sayilar ✓ 2. sira-sayilari ✓ 3. sayilari-karsilastirma ✓ 4. ritmik-sayma ✓ 5. oruntuler ✓ 6. nesne-sayisini-tahmin-etme ✓ 7. uzunluk-ve-kutle-olcme ✓ 8. paralarimiz ✓
9. toplama-islemi ✓ 10. cikarma-islemi ✓ 11. toplama-ve-cikarma-problemleri ✓ 12. esitlik-ve-islemler-arasi-iliski ✓ 13. yon-konum-ve-es-nesneler ✓ 14. geometrik-cisimler ✓ 15. geometrik-sekiller ✓ 16. veri-toplama-ve-nesne-grafigi ✓
2. sınıf: 1. 100e-kadar-sayilar ✓ 2. iki-basamakli-sayilar ✓ 3. sayilari-karsilastirma-ve-siralama ✓ 4. ritmik-sayma ✓ 5. oruntuler ✓ 6. nesne-sayisini-tahmin-etme ✓ 7. butun-yarim-ve-ceyrek ✓ 8. paralarimiz ✓ 9. zaman-olcme ✓ 10. uzunluk-ve-kutle-olcme ✓ 11. toplama-islemi ✓
12. cikarma-islemi ✓ 13. toplama-ve-cikarma-problemleri ✓ 14. carpma-islemi ✓ 15. bolme-islemi ✓ 16. esitlik ✓ 17. geometrik-cisimler ✓ 18. geometrik-sekiller ✓ 19. sivi-olcme ✓ 20. yon-ve-konum ✓ 21. simetri ✓ 22. veri-toplama-ve-grafikler ✓
トピック：nesne-sayisini→sayilar、yarim-ve-ceyrek→kesirler、konum→geometri
TR / Matematik / 9. Sınıf（Lise。Ortaöğretim Matematik DÖP 2026、tr_common.STD_URL_LISE、DOMAIN に SY Sayılar・N Nicelikler ve Değişimler・ES Eşlik ve Benzerlik・AB Algoritma ve Bilişim）— 単元は tr_s9a（1〜4）・tr_s9b（5〜18）。tr_s9a.reuse(mod, "uN", 名前) で 7.〜8. sınıf の問題関数を使う（tr_s9a.setup が MODS の setup を呼ぶ）。グラフの問題は 1 本だけ描いて式を選ばせる（複数の線はラベルが重なる）
1. uslu-ifadeler ✓ 2. koklu-ifadeler ✓ 3. gercek-sayi-araliklari ✓ 4. sayi-kumeleri ✓ 5. gercek-sayilarin-islem-ozellikleri ✓ 6. dogrusal-fonksiyonlar ✓ 7. mutlak-deger-fonksiyonu ✓ 8. dogrusal-denklem-ve-esitsizlik-problemleri ✓ 9. ucgende-aci-ve-kenar-ozellikleri ✓
10. geometrik-donusumler ✓ 11. eslik-ve-benzerlik-kosullari ✓ 12. benzer-ucgenler-olusturma ✓ 13. tales-oklid-ve-pisagor-teoremleri ✓ 14. eslik-ve-benzerlik-problemleri ✓ 15. algoritma-temelli-problemler ✓ 16. mantik-baglaclari-ve-niceleyiciler ✓ 17. tek-nicel-degiskenli-veri ✓ 18. deneysel-ve-teorik-olasilik ✓
10. sınıf の MAT.10.x（DÖP の PDF の 200000 文字目あたり）: Geometrik Şekiller（trigonometrik oranlar、yardımcı elemanlar、alan、sinüs-kosinüs teoremi）、İki kategorik değişken、Sayılar（asal çarpan・bölen、EBOB-EKOK、kalan）…
TR / Matematik / 10. Sınıf（Ortaöğretim DÖP 2026。単元は tr_s10a（1〜10）・tr_s10b（11〜20）、lise の共通部品は `tools/tr_lise.py`（TRIG（特別角の文字列）・TVAL・TRIP（ピタゴラス数）・poly・peval・nCr・nPr・frs・U（meta を自動）・W3（誤答の重複を落とす））。DOMAIN に SAB Sayma, Algoritma ve Bilişim・AN Analitik İnceleme・GC Geometrik Cisimler・DM Değişimin Matematiği・HV Hazır Veriler を足した。
変数の数・角度の後に接尾辞を付けない（「m(A) = 60° olsun」「%30 kadarı」「%40 olasılıkla」）。tr_run の safe は TypeError・KeyError・IndexError も None にする）
1. dik-ucgende-trigonometrik-oranlar ✓ 2. trigonometrik-ozdeslikler ✓ 3. ucgende-yardimci-elemanlar ✓ 4. ucgenin-alani ✓ 5. sinus-ve-kosinus-teoremleri ✓ 6. iki-kategorik-degiskenli-veri ✓ 7. asal-carpanlar-ve-bolenler ✓
8. ebob-ve-ekok ✓ 9. bolunebilme-ve-kalan ✓ 10. fonksiyon-olma-sartlari ✓ 11. karesel-fonksiyon ✓ 12. karekok-ve-rasyonel-fonksiyonlar ✓ 13. ters-fonksiyonlar ✓ 14. fonksiyonlarla-denklem-ve-esitsizlik-problemleri ✓
15. sayma-stratejileri ✓ 16. algoritmik-islemler ✓ 17. iki-nokta-arasi-uzaklik ✓ 18. dogrunun-analitik-incelenmesi ✓ 19. kosullu-olasilik ✓ 20. bayes-teoremi ✓
トピックに fonksiyonlar・trigonometri を足した（olcme の out に kalan、olasilik に sayma-stratejileri・bayes、carpanlar に ebob）
TR / Matematik / 11. Sınıf（単元は tr_s11a（1〜7：veri・dörtgen・çokgen・trigonometrik fonksiyonlar。pis（π の倍数）・tval（特別角の符号付きの値））・tr_s11b（8〜14：trigonometrik denklemler・üstel・logaritma（lg：log₂ 8、底 10 は log）・bileşke・dört işlem））
1. iki-nicel-degiskenli-veri ✓ 2. dortgenlerin-ozellikleri ✓ 3. ozel-dortgenler ✓ 4. cokgenler ✓ 5. cokgen-problemleri ✓ 6. trigonometrik-fonksiyonlar ✓ 7. trigonometrik-fonksiyonlarin-grafikleri ✓
8. trigonometrik-denklemler ✓ 9. ustel-fonksiyon ✓ 10. logaritma ✓ 11. logaritmik-fonksiyon ✓ 12. ustel-ve-logaritmik-denklemler ✓ 13. bileske-fonksiyon ✓ 14. fonksiyonlarda-dort-islem ✓
トピックに ustel-ve-logaritmik-fonksiyonlar を足した（sayilar の out に logaritm（ritmik に当たる）、veri・denklemler・fonksiyonlar の out に trigonometri など）
TR / Matematik / 12. Sınıf（単元は tr_s12a（1〜9：diziler・polinomlar（pmul・pdiv・fct）・çember）・tr_s12b（10〜19：cisimler・limit・türev（deriv）・hazır veriler））
1. aritmetik-diziler ✓ 2. geometrik-diziler ✓ 3. diziler-ve-fonksiyonlar ✓ 4. polinomlar ✓ 5. polinom-bolme-ve-kalan ✓ 6. polinom-ve-rasyonel-denklemler ✓ 7. cemberin-elemanlari ✓ 8. cemberde-acilar ✓ 9. cember-ve-daire-problemleri ✓
10. prizma-ve-silindir ✓ 11. piramit-koni-ve-kure ✓ 12. cisim-problemleri ✓ 13. limit ✓ 14. belirsizlik-ve-sureklilik ✓ 15. turevin-tanimi ✓ 16. turev-kurallari ✓ 17. turevin-geometrik-yorumu ✓ 18. turevin-uygulamalari ✓ 19. hazir-veriler-uzerinde-calisma ✓
トピックに diziler-ve-polinomlar・limit-ve-turev を足した（geometri に cemberin・cemberde・cember-ve-daire・prizma-ve-silindir・piramit-koni）
TR / Matematik / Okul Öncesi（60–72 ay、5〜6歳。Maarif Modeli Okul Öncesi Eğitim Programı 2024 の Matematik alanı MAB.1〜MAB.14、tr_common.STD_URL_OO）— grade `okul-oncesi`（name「Okul Öncesi」、sort 0）。`python3 tools/tr_run.py 0`、単元は tr_s0a（tr_p12 の問題関数を lim(mk, 10) で 10 までに絞って再利用、bakista・paylastir・esit_mi・karsi は自前）。
DOMAIN に SAY Sayma・MM Matematiksel Muhakeme・PC Matematiksel Problem Çözme・MT Matematiksel Temsil・VK Veri ile Çalışma を足した。seo_title は「… Okul Öncesi Matematik (5-6 Yaş): Etkinlik Kâğıdı ve Cevaplar」。unit.php で typicalAgeRange 5-6、core.php の grade_standard() で基準名を Okul Öncesi Eğitim Programı に
1. ritmik-sayma ✓ 2. nesne-sayma ✓ 3. bir-bakista-sayma ✓ 4. butun-ve-parca ✓ 5. geometrik-sekiller ✓ 6. konum-ve-yon ✓ 7. olcme-ve-karsilastirma ✓ 8. oruntuler ✓ 9. karsilastirma-ve-siralama ✓ 10. artma-ve-azalma ✓ 11. paylastirma ✓ 12. veri-toplama-ve-grafik ✓
TR / Matematik は okul öncesi・1.〜12. sınıf まで完了。mq-geo.js と mq.php の MQ_GEO（このリポジトリの外）に tr があるか確認する。次は GDP 順で次の国

CH / Mathematik（Lehrplan 21, Deutschschweiz）— country `ch`（name「Schweiz」、lang `de`（UI は Deutschland と共用）、hreflang de-ch、standard「Kompetenzen des Lehrplans 21」）、subject `mathematik`（Mathematik）、grade `klasse-N`（name「3. Klasse」、unit.php で N+5〜N+6 歳と Primarstufe／Sekundarstufe I）、A4。
`python3 tools/ch_run.py 3 [Nummer …]`、単元は `tools/ch_k3.py` の UNITS（slug, sort, LP21 のコード, Kompetenzbereich, 元）。元が gen_de_mathe_* の名前なら Deutschland の生成スクリプトを新しい seed（130000 + 1000 × Klasse + 番号）で動かし、make_unit の中身を受け取って書く（ch_common.from_de。FIX で個別に直す）。元が関数なら自前（ch_k3_geld：スイスの硬貨・紙幣の絵）。
共通部品は `tools/ch_common.py`：de_common.mcq を差し替えて、すべての問題の文をスイス式に直す（ch_text：ß → ss、1’000（4 けたから ’。年は除く）、小数は点 2.5、3 × 4、3.50 Fr.・45 Rp.、Euro/Cent → Franken/Rappen、Velo・Brötli・Gipfeli・Schulthek・Primarschule、ドイツの都市 → スイスの都市、「Klasse 3」→「3. Klasse」）。5 Rp. で割り切れない金額と LEAKS（€・ct・Euro・ß・Komma など）が残る問題は落とす。名前は de_common.GIRLS/BOYS をスイスの名前に置き換える。
standard_code は LP21 のコード（「MA.1.A.1, MA.1.C.2」）、standard_text は Kompetenz の文（KOMP）、domain は Zahl und Variable／Form und Raum／Grössen, Funktionen, Daten und Zufall、standard_url は Lehrplan 21 Mathematik（St. Gallen の PDF）。トピックは topic_defs_ch()（topic_defs_de を ss・Franken und Rappen に直したもの）

CH / Mathematik / 3. Klasse（Zahlenraum bis 1’000）
1. zahlen-bis-1000 ✓ 2. zahlen-vergleichen-und-ordnen ✓ 3. runden-und-ueberschlagen ✓ 4. plus-und-minus-bis-1000 ✓ 5. schriftliche-addition ✓ 6. schriftliche-subtraktion ✓ 7. einmaleins ✓
8. multiplizieren-und-dividieren ✓ 9. dividieren-mit-rest ✓ 10. sachaufgaben ✓ 11. geld ✓ 12. laengen ✓ 13. gewichte ✓ 14. uhrzeit-und-zeitspannen ✓
15. koerper-und-figuren ✓ 16. achsensymmetrie ✓ 17. zahlenfolgen-und-muster ✓ 18. diagramme-und-tabellen ✓ 19. wahrscheinlichkeit ✓
CH / Mathematik / 4. Klasse（Zahlenraum bis 1 Million。ch_k4.py、rechnen-mit-geld は自前（ch_k3_geld.build4）、daten-und-diagramme は PRE で距離表をスイスの都市に）
1. zahlen-bis-1-million ✓ 2. runden-und-ueberschlagen ✓ 3. schriftlich-addieren-und-subtrahieren ✓ 4. schriftliche-multiplikation ✓ 5. schriftliche-division ✓ 6. rechengesetze-und-klammern ✓ 7. brueche-im-alltag ✓
8. sachaufgaben ✓ 9. laengen-in-dezimalschreibweise ✓ 10. gewichte-und-tonnen ✓ 11. rauminhalte ✓ 12. rechnen-mit-geld ✓ 13. zeit-und-kalender ✓ 14. massstab ✓
15. umfang-und-flaecheninhalt ✓ 16. parallel-senkrecht-und-vierecke ✓ 17. wuerfel-und-quader ✓ 18. daten-und-diagramme ✓ 19. kombinatorik-und-wahrscheinlichkeit ✓
ch_common: from_de の pre(mod) で main の前にモジュールのデータを差し替えられる。Deutschland の文字どおりの名前（Paul, Ben …）は DE_NAMES でスイスの名前に（Kids の名前とは別の名前）
CH / Mathematik / 2. Klasse（Zahlenraum bis 100、Einmaleins。ch_k2.py、geld は FIX で本文・FAQ をスイスの硬貨・紙幣に。5 Fr. は硬貨（Fünffrankenstück）、Noten は 10〜1000 Fr.）
1. zahlen-bis-100 ✓ 2. zahlen-vergleichen-und-ordnen ✓ 3. plus-und-minus-bis-20 ✓ 4. plus-bis-100 ✓ 5. minus-bis-100 ✓ 6. ergaenzen-bis-100 ✓ 7. multiplizieren-verstehen ✓ 8. einmaleins-mit-2-5-und-10 ✓ 9. kleines-einmaleins ✓
10. geteilt-aufteilen-und-verteilen ✓ 11. sachaufgaben ✓ 12. geld ✓ 13. laengen ✓ 14. uhrzeit ✓ 15. flaechen-und-koerper ✓ 16. spiegeln-und-symmetrie ✓ 17. zahlenmauern-und-muster ✓ 18. strichlisten-und-diagramme ✓
CH / Mathematik / 1. Klasse（Zahlenraum bis 20。ch_k1.py、geld は自前（ch_k3_geld.build1））
1. zahlen-bis-10 ✓ 2. zahlen-bis-20 ✓ 3. zahlen-vergleichen ✓ 4. zerlegen-und-ergaenzen ✓ 5. plus-bis-10 ✓ 6. minus-bis-10 ✓ 7. plus-und-minus-bis-20 ✓ 8. plus-und-minus-ueber-die-10 ✓ 9. verdoppeln-und-halbieren ✓
10. rechengeschichten-und-sachaufgaben ✓ 11. geld ✓ 12. laengen-vergleichen-und-messen ✓ 13. uhrzeit-und-tagesablauf ✓ 14. formen-und-koerper ✓ 15. lage-und-richtung ✓ 16. muster-und-zahlenfolgen ✓ 17. strichlisten-und-tabellen ✓
CH / Mathematik / 5. Klasse（ch_k5.py、Deutschland Klasse 5 から。負の数・累乗は Zyklus 3 なので外し、EXTRA の _noneg で問題文に負の数がある問題を落とす）
1. natuerliche-zahlen-und-stellenwerte ✓ 2. runden-und-schaetzen ✓ 3. addieren-und-subtrahieren ✓ 4. multiplizieren-und-dividieren ✓ 5. terme-und-rechengesetze ✓ 6. teiler-vielfache-und-primzahlen ✓ 7. brueche-und-anteile ✓ 8. muster-terme-und-variablen ✓
9. laengen-massen-und-zeit ✓ 10. sachaufgaben-und-kombinatorik ✓ 11. strecken-geraden-und-strahlen ✓ 12. winkel ✓ 13. koordinatensystem ✓ 14. achsen-und-punktsymmetrie ✓ 15. flaecheninhalt-und-umfang ✓ 16. volumen-und-oberflaeche-von-quadern ✓ 17. haeufigkeiten-und-diagramme ✓
CH / Mathematik / 6. Klasse（ch_k6.py、Deutschland Klasse 6 から。分数の乗除・負の数・方程式・平行四辺形の面積は Zyklus 3 なので外した）
1. brueche-erweitern-und-kuerzen ✓ 2. brueche-vergleichen-und-ordnen ✓ 3. gemischte-zahlen ✓ 4. brueche-addieren-und-subtrahieren ✓ 5. dezimalzahlen-und-stellenwerte ✓ 6. brueche-und-dezimalzahlen ✓ 7. dezimalzahlen-addieren-und-subtrahieren ✓
8. dezimalzahlen-multiplizieren-und-dividieren ✓ 9. prozente ✓ 10. zuordnungen-und-dreisatz ✓ 11. sachaufgaben-mit-bruechen-und-dezimalzahlen ✓ 12. dreiecke-und-vierecke ✓ 13. kreise ✓ 14. daten-und-wahrscheinlichkeit ✓
お金は money_ok で 5 Rp. 単位・小数 2 けたでない金額（2.99 Fr.、0.9 Fr.）の問題を落とす
CH / Mathematik / 7.–9. Klasse（Sekundarstufe I、Zyklus 3。ch_k7.py〜ch_k9.py、Deutschland Klasse 7–10 から LP21 のコードと学年に合わせて選んだ。MWST は 8.1 %（Lebensmittel 2.6 %）：ch_k8 の PRE で mwst を差し替え、FIX で本文・FAQ を直す。LEAKS に「19 % Mehrwert」）
7. Klasse: 1. negative-zahlen ✓ 2. rechnen-mit-negativen-zahlen ✓ 3. potenzen-und-quadratzahlen ✓ 4. brueche-multiplizieren ✓ 5. brueche-dividieren ✓ 6. terme-und-gleichungen ✓ 7. terme-umformen ✓ 8. lineare-gleichungen ✓ 9. gleichungen-in-sachaufgaben ✓ 10. prozentrechnung ✓ 11. proportionale-und-antiproportionale-zuordnungen ✓ 12. winkel-an-geradenkreuzungen ✓ 13. winkelsummen-in-dreiecken-und-vielecken ✓ 14. dreiecke-konstruieren ✓ 15. flaecheninhalt-von-parallelogramm-und-dreieck ✓ 16. flaecheninhalt-von-vierecken ✓ 17. prismen ✓ 18. wahrscheinlichkeit ✓
8. Klasse: 1. rationale-zahlen ✓ 2. rechnen-mit-rationalen-zahlen ✓ 3. potenzen-und-zehnerpotenzen ✓ 4. quadratwurzeln-und-reelle-zahlen ✓ 5. ausmultiplizieren-und-ausklammern ✓ 6. binomische-formeln ✓ 7. prozentuale-veraenderung ✓ 8. zinsrechnung ✓ 9. lineare-funktionen ✓ 10. geradengleichungen-aufstellen ✓ 11. besondere-linien-im-dreieck ✓ 12. kongruenzsaetze ✓ 13. satz-des-thales ✓ 14. kreisumfang-und-kreisflaeche ✓ 15. zylinder ✓ 16. boxplots-und-kennwerte ✓ 17. mehrstufige-zufallsexperimente ✓
9. Klasse: 1. lineare-gleichungssysteme-grafisch-loesen ✓ 2. lineare-gleichungssysteme-rechnerisch-loesen ✓ 3. gleichungssysteme-in-sachaufgaben ✓ 4. bruchterme-und-bruchgleichungen ✓ 5. potenzgesetze ✓ 6. rechnen-mit-wurzeln ✓ 7. quadratische-funktionen ✓ 8. quadratische-gleichungen ✓ 9. satz-des-pythagoras ✓ 10. pythagoras-in-figuren-und-koerpern ✓ 11. aehnlichkeit-und-zentrische-streckung ✓ 12. strahlensaetze ✓ 13. pyramide-und-kegel ✓ 14. kugel ✓ 15. vierfeldertafeln ✓
CH / Mathematik / Kindergarten（Zyklus 1 の 2 年、4〜6歳。grade `kindergarten`（sort 0）、`python3 tools/ch_run.py 0`、単元は ch_k0.py。Deutschland Klasse 1 の生成スクリプトから、LIMIT（upto(10) など）で 10 を超える数の問題を落とし、PRE の _soft_mix で足りない分を同じ単元の別の問題関数で埋め、FIX で「Klasse 1」「Schule」などを Kindergarten に直す。unit.php で typicalAgeRange 4-6、topic_defs_ch に KG の slug）
1. zahlen-bis-10 ✓ 2. zaehlen-bis-20 ✓ 3. mengen-vergleichen ✓ 4. zahlen-zerlegen ✓ 5. dazuzaehlen-bis-10 ✓ 6. wegnehmen-bis-10 ✓ 7. formen-und-koerper ✓ 8. lage-und-richtung ✓ 9. muster ✓ 10. laengen-vergleichen ✓ 11. tagesablauf-und-uhr ✓ 12. sortieren-und-zaehlen ✓
CH / Mathematik / Gymnasium 1.〜4. Klasse（Rahmenlehrplan Gymnasiale Maturitätsschulen, EDK 20. Juni 2024、ch_common.STD_URL_GYM・KOMP_GYM・DOMAIN_GYM（A Arithmetik und Algebra／N Analysis／G Geometrie／S Stochastik）、codes は「2.2 Differenzialrechnung」形式、standard_code は「RLP Mathematik 2.2 Differenzialrechnung」）— grade `gymnasium-1`〜`gymnasium-4`（name「Gymnasium 1. Klasse」、sort 10〜13、unit.php で 15〜19 歳）。
`python3 tools/ch_run.py 10|11|12|13`（k ≥ 10 は gymnasium-(k − 9)、C.KEEP_DOT = True で Malpunkt · を残す（Skalarprodukt と × を区別））、単元は ch_k10〜ch_k13。Deutschland Klasse 10 の単元は FIX の ch_gym.gymfix で「Klasse 10」を Gymnasium に。
自前の単元は `tools/ch_gym.py`（build(spec)：spec(R) が title・short・meta・kb・ks・think・ex・mist・faq・sets=[(Titel, [(maker, n)])] を返す。mcq（neg=True）・z・fz・par・poly（{指数: 係数}、文字のキーは先に並ぶ）・lin・vec（Spaltenvektor .mx m1）・pt）と ch_gym_a（LGS mit 3 Unbekannten・Folgen・Reihen・gebrochenrationale Funktionen）・ch_gym_b（Vektoren・Skalarprodukt・Geraden und Ebenen・Kombinatorik・bedingte W.・Binomialverteilung）・ch_gym_c（Ableitung・Ableitungsregeln・Kurvendiskussion・Extremwertaufgaben・Stammfunktionen・Integral・Statistik）。
maker ごとの問題の数は scratchpad の mk.py のように 3000 回呼んで確かめる（足りないと pick_unique が止まる）。トピックに differenzial-und-integralrechnung・vektorgeometrie を足した（topic_defs_ch の $gym・$gout）。core.php の grade_standard() で基準名を Rahmenlehrplan に
Gymnasium 1: 1. potenzfunktionen ✓ 2. polynomfunktionen ✓ 3. gleichungssysteme-mit-drei-unbekannten ✓ 4. exponentialfunktionen ✓ 5. exponentielles-wachstum-und-zerfall ✓ 6. logarithmus ✓
Gymnasium 2: 1. bogenmass-und-kreisausschnitt ✓ 2. trigonometrie-am-einheitskreis ✓ 3. sinus-und-kosinusfunktion ✓ 4. sinussatz-und-kosinussatz ✓ 5. arithmetische-und-geometrische-folgen ✓ 6. reihen-und-grenzwerte ✓ 7. gebrochenrationale-funktionen-und-asymptoten ✓
Gymnasium 3: 1. vektoren ✓ 2. skalarprodukt-und-winkel ✓ 3. geraden-und-ebenen-im-raum ✓ 4. kombinatorik ✓ 5. bedingte-wahrscheinlichkeit ✓ 6. erwartungswert ✓ 7. binomialverteilung ✓
Gymnasium 4: 1. ableitung-und-tangente ✓ 2. ableitungsregeln ✓ 3. kurvendiskussion ✓ 4. extremwertaufgaben ✓ 5. stammfunktionen ✓ 6. bestimmtes-integral-und-flaechen ✓ 7. statistische-kennzahlen ✓
CH / Mathematik（Deutschschweiz）は Kindergarten〜9. Klasse と Gymnasium 1.〜4. Klasse まで完了。次はフランス語圏（PER）・イタリア語圏（Ticino）か、GDP 順で次の国

SE / Matematik（Lgr22, kursplanen i matematik。åk 1–3・4–6・7–9 の centralt innehåll を学年に分ける）— country `se`（name「Sverige」、lang `sv`、hreflang sv-se、standard「Lgr22」）、subject `matematik`、grade `arskurs-N`（name「Årskurs N」、unit.php で N+6〜N+7 歳と educationalLevel Grundskolan, lågstadiet／mellanstadiet／högstadiet）、A4。
生成スクリプトは `tools/se_a3.py [nummer…]`（seed は 95300 + 番号、単元は se_a3a（1〜12）・se_a3b（13〜23）の UNITS）、共通部品は `tools/se_common.py`（num（1 000 から空白区切り、ノーブレークスペース）・dec（コンマ）・kr（25 kr、öre なし）・u・ord_（trehundrafyrtiofem）・klocka_ord（kvart över tre、halv fyra = 3.30、fem i halv fyra）・hm（14.30）・Kids（hon/han）・mcq（誤答が足りないと近い数で補う、fill=False で None）・lesson（Så tänker du → Exempel → Vanliga fel）・make_unit（seo_title「X årskurs 3: arbetsblad i matematik med facit」、standard_code「Lgr22 åk 1–3 · Geometri」、standard_text の末尾に「(sammanfattning av det centrala innehållet …)」）・図：tallinje・positionstabell・basemat・stapel・streck・uppstallning・klocka）。
スウェーデン語、du で話しかける短い文。記号は × と :（割り算）、余りは「17 : 5 = 3 rest 2」。単位は mm cm dm m km mil、g hg kg、ml cl dl l。名詞の性に注意（ett klot、ett rätblock、ett äpple、halva pizzan）。
domain は Lgr22 の 6 分野（T Taluppfattning och tals användning／A Algebra／G Geometri／S Sannolikhet och statistik／F Samband och förändring／P Problemlösning）。standard_url は Skolverket の kursplan matematik。symmetri は DE Klasse 3 の生成スクリプトの図（grid・half・mirror・broken・shifted・four）を R を入れ替えて使う。
UI 文言は core.php の 'sv'（T と js_text、sep はノーブレークスペース、lc は 'mb'（mb_strtolower））、トピックは topics.php の `topic_defs_se()`（tal・addition-och-subtraktion・multiplikation-och-division・brak-decimaltal-och-procent・algebra・matning・geometri・statistik-och-sannolikhet、トピックの呼び名は「tema」）、topic.php・topics.php に $sv の文言。みんなでクイズ（mq.js）にはまだ sv の言語がない（英語で出る）

SE / Matematik / Årskurs 3（det första året med nationella prov）
1. tal-till-1000 ✓ 2. jamfora-och-ordna-tal ✓ 3. overslagsrakning-och-rimlighet ✓ 4. huvudrakning ✓ 5. addition-med-uppstallning ✓ 6. subtraktion-med-uppstallning ✓ 7. multiplikation-och-tabellerna ✓ 8. division ✓
9. problemlosning ✓ 10. enkla-brak ✓ 11. likheter-och-likhetstecknet ✓ 12. monster-och-talfoljder ✓ 13. dubbelt-och-halften ✓ 14. pengar ✓ 15. klockan-och-tid ✓ 16. langd ✓ 17. massa-och-volym ✓
18. geometriska-figurer ✓ 19. geometriska-kroppar ✓ 20. symmetri ✓ 21. lagesord-och-stegvisa-instruktioner ✓ 22. tabeller-och-diagram ✓ 23. slump-och-sannolikhet ✓
SE / Matematik / Årskurs 4–6（mellanstadiet。årskurs 6 が nationella prov の学年）— `python3 tools/se_m46.py 4|5|6 [nummer…]`（seed は 95000 + 100 × årskurs + 番号、単元の並びは se_m46.GRADES）。
単元の関数は lv（4・5・6）を受け取り、同じ slug でも範囲と問題が学年で変わる：se_m_a（tal-och-positionssystemet・avrundning-och-overslag・addition-och-subtraktion・multiplikation・division・prioriteringsregler・negativa-tal）、
se_m_b（brak・decimaltal・procent・ekvationer-och-uttryck・monster-och-talfoljder・proportionalitet）、se_m_c（langd-massa-och-volym・tid・omkrets-och-area・vinklar・geometriska-figurer-och-kroppar・symmetri・koordinatsystem・skala）、
se_m_d（tabeller-och-diagram・medelvarde-typvarde-och-median・sannolikhet・kombinatorik・problemlosning）。共通部品は `tools/se_m.py`（R・K・M（負の数も可、誤答が 3 つそろわないと None、値が同じ分数（5/10 と 1/2）は誤答にしない）・fr・fq・d（Fraction → コンマの小数）・tab・PLATS・MAXN）。
範囲：åk 4 は 100 000 まで・小数は hundradelar まで、åk 5 は 1 miljon まで・tusendelar・procent・negativa tal、åk 6 は 10 miljoner・bråk の異分母・2 段階の方程式・skala・volym。se_m46.build は文中の 4 桁以上の数を 1 000 の形にそろえる（SVG・タグと「år 1907」などの年は除く）。
図：角度・分度器・三角形は gen_au_maths_y5_angles、立方体の積み木は kr_pics56.iso_cubes、座標は de_k8.kosy（lo=0）
SE / Matematik / Årskurs 4: 1. tal-och-positionssystemet ✓ 2. avrundning-och-overslag ✓ 3. addition-och-subtraktion ✓ 4. multiplikation ✓ 5. division ✓ 6. problemlosning ✓ 7. brak ✓ 8. decimaltal ✓ 9. ekvationer-och-uttryck ✓ 10. monster-och-talfoljder ✓
11. langd-massa-och-volym ✓ 12. tid ✓ 13. omkrets-och-area ✓ 14. vinklar ✓ 15. geometriska-figurer-och-kroppar ✓ 16. symmetri ✓ 17. koordinatsystem ✓ 18. tabeller-och-diagram ✓ 19. sannolikhet ✓
SE / Matematik / Årskurs 5: 1. tal-och-positionssystemet ✓ 2. avrundning-och-overslag ✓ 3. addition-och-subtraktion ✓ 4. multiplikation ✓ 5. division ✓ 6. prioriteringsregler ✓ 7. negativa-tal ✓ 8. problemlosning ✓ 9. brak ✓ 10. decimaltal ✓ 11. procent ✓ 12. ekvationer-och-uttryck ✓
13. monster-och-talfoljder ✓ 14. proportionalitet ✓ 15. langd-massa-och-volym ✓ 16. tid ✓ 17. omkrets-och-area ✓ 18. vinklar ✓ 19. geometriska-figurer-och-kroppar ✓ 20. symmetri ✓ 21. koordinatsystem ✓ 22. tabeller-och-diagram ✓ 23. medelvarde-typvarde-och-median ✓ 24. sannolikhet ✓ 25. kombinatorik ✓
SE / Matematik / Årskurs 6: 1. tal-och-positionssystemet ✓ 2. avrundning-och-overslag ✓ 3. addition-och-subtraktion ✓ 4. multiplikation ✓ 5. division ✓ 6. prioriteringsregler ✓ 7. negativa-tal ✓ 8. problemlosning ✓ 9. brak ✓ 10. decimaltal ✓ 11. procent ✓ 12. ekvationer-och-uttryck ✓
13. monster-och-talfoljder ✓ 14. proportionalitet ✓ 15. langd-massa-och-volym ✓ 16. omkrets-och-area ✓ 17. vinklar ✓ 18. geometriska-figurer-och-kroppar ✓ 19. skala ✓ 20. koordinatsystem ✓ 21. tabeller-och-diagram ✓ 22. medelvarde-typvarde-och-median ✓ 23. sannolikhet ✓ 24. kombinatorik ✓
トピック（topic_defs_se）に samband-och-forandring（proportionalitet・skala・koordinat）と problemlosning を足した。prioritering→multiplikation-och-division、kombinatorik→statistik-och-sannolikhet
SE / Matematik / Årskurs 7–9（högstadiet）— `python3 tools/se_h79.py 7|8|9 [nummer…]`（seed は 97000 + 100 × årskurs + 番号、単元の並びは se_h79.GRADES）。
単元の関数は lv を受け取る：se_h_a（tal：negativa-tal・prioriteringsregler・delbarhet・brak・decimaltal・potenser・grundpotensform・reella-tal）、se_h_b（algebra：uttryck・ekvationer・mönster och formler・parenteser・formler・olikheter・kvadreringsreglerna・ekvationssystem・x²）、
se_h_c（samband：procent・förändringsfaktor・proportionalitet・funktioner・linjära funktioner・räta linjen・tolka grafer・ränta och lån・exponentiell förändring）、se_h_d（geometri：vinklar・polygoner・area・cirkeln・enheter・skala・volym・begränsningsarea・Pythagoras・likformighet・pyramid/kon/klot・cirkelsektorer）、se_h_e（lägesmått・spridningsmått・diagram・sannolikhet・kombinatorik・problemlösning）。
共通部品は `tools/se_h.py`（se_m の上に M（値が同じ誤答を落とす）・MN（数の答え、割り切れない誤答は落とす、° は空白なし）・MQ（選択肢を問題文に入れて重複を防ぐ）・expr・lin・par・sg・rd・sup・gen（Olles／Elias）・kosy・kurve・figure）。π は「Använd π ≈ 3,14」で答えを正確な小数に。連立は `<span class='sys'>`。図は tr_g.poly（unit_="" で数に単位を付けて渡す）・tr_g.parallel_fig・AU.shape_svg（ラベルが置けないと ValueError）・kr_pics56.box_svg・自前の solid（cylinder・kon・klot・pyramid・prisma）・ladagram
SE / Matematik / Årskurs 7: 1. negativa-tal ✓ 2. prioriteringsregler ✓ 3. delbarhet-och-primtal ✓ 4. brak ✓ 5. decimaltal ✓ 6. potenser-och-kvadratrotter ✓ 7. procent ✓ 8. algebraiska-uttryck ✓ 9. ekvationer ✓ 10. monster-och-formler ✓ 11. proportionalitet ✓ 12. vinklar ✓ 13. omkrets-och-area ✓ 14. cirkeln ✓ 15. enheter ✓ 16. lagesmatt ✓ 17. sannolikhet ✓ 18. problemlosning ✓
SE / Matematik / Årskurs 8: 1. potenser ✓ 2. grundpotensform-och-prefix ✓ 3. parenteser-och-faktorisering ✓ 4. ekvationer ✓ 5. formler ✓ 6. olikheter ✓ 7. procent-och-forandringsfaktor ✓ 8. funktioner-och-grafer ✓ 9. proportionalitet ✓ 10. skala ✓ 11. vinklar-och-polygoner ✓ 12. prisma-och-cylinder ✓ 13. begransningsarea ✓ 14. tabeller-och-diagram ✓ 15. kombinatorik ✓ 16. sannolikhet ✓ 17. problemlosning ✓
SE / Matematik / Årskurs 9（nationella prov）: 1. reella-tal ✓ 2. kvadreringsreglerna ✓ 3. ekvationssystem ✓ 4. ekvationer-med-x2 ✓ 5. linjara-funktioner ✓ 6. rata-linjens-ekvation ✓ 7. tolka-grafer ✓ 8. ranta-och-lan ✓ 9. exponentiell-forandring ✓ 10. pythagoras-sats ✓ 11. likformighet ✓ 12. pyramid-kon-och-klot ✓ 13. cirkelsektorer ✓ 14. spridningsmatt ✓ 15. sannolikhet ✓ 16. problemlosning ✓
SE / Matematik / Årskurs 1–2（lågstadiet）— `python3 tools/se_l12.py 1|2 [nummer…]`（seed は 96000 + 100 × årskurs + 番号）、単元は `tools/se_l.py` の UNITS（lv = 1, 2）。絵は k_pics（P() で svenska aria-label、SAK で物の名前と en/ett）、åk 3 の問題関数を maker(B.u16, "matt") で取り出し lim(mk, 100) で数を絞って再利用（symmetri・lägesord・diagram・slump・figurer och kroppar・längd）。åk 1 は 20 まで（talraden は 100 まで）、åk 2 は 100 まで
SE / Matematik / Årskurs 1: 1. tal-till-20 ✓ 2. talraden-till-100 ✓ 3. jamfora-tal ✓ 4. talkamrater ✓ 5. addition-till-10 ✓ 6. subtraktion-till-10 ✓ 7. addition-och-subtraktion-till-20 ✓ 8. problemlosning ✓ 9. dubbelt-och-halften ✓ 10. monster ✓ 11. pengar ✓ 12. klockan ✓ 13. langd-och-vikt ✓ 14. geometriska-figurer ✓ 15. lagesord ✓ 16. tabeller-och-diagram ✓
SE / Matematik / Årskurs 2: 1. tal-till-100 ✓ 2. tiotal-och-ental ✓ 3. jamfora-och-ordna-tal ✓ 4. udda-och-jamna-tal ✓ 5. huvudrakning ✓ 6. addition-och-subtraktion-till-100 ✓ 7. problemlosning ✓ 8. multiplikation ✓ 9. delning ✓ 10. halvor-och-fjardedelar ✓ 11. monster ✓ 12. pengar ✓ 13. klockan ✓ 14. langd ✓ 15. geometriska-figurer-och-kroppar ✓ 16. symmetri ✓ 17. lagesord-och-programmering ✓ 18. tabeller-och-diagram ✓ 19. slump-och-chans ✓
トピック（topic_defs_se）に potenser-och-reella-tal（Potenser, primtal och reella tal）を足し、samband-och-forandring を「Proportionalitet, funktioner och grafer」に。algebra の out に rata-linjen
SE / Matematik / Förskoleklass（6 歳、Lgr22 kapitel 3）— grade `forskoleklass`（name「Förskoleklass」、sort 0、unit.php で typicalAgeRange 6-7）。`python3 tools/se_f.py [nummer…]`（seed は 96000 + 番号）。
単元は se_f.UNITS（se_l の åk 1–2 の問題関数を名前で取り出し、lim で数を 10〜20 までに絞る。「delning:dela」のように別の単元の関数も使える）。standard_code は「Lgr22 förskoleklass · Taluppfattning och tals användning」、core.php の grade_standard() で基準名を「Lgr22, förskoleklassen」に
1. rakna-till-20 ✓ 2. talraden ✓ 3. jamfora-antal ✓ 4. talkamrater-till-10 ✓ 5. lagga-till ✓ 6. ta-bort ✓ 7. dubbelt-och-dela-lika ✓ 8. monster ✓ 9. former ✓ 10. lagesord ✓ 11. langd-och-vikt ✓ 12. pengar ✓ 13. klockan-och-tid ✓ 14. sortera-och-rakna ✓

SE / Matematik / Gymnasiet（Gy25 ämnesplan i matematik、naturvetenskaps- och teknikprogrammet の c 系列）— grade `matematik-1c`・`matematik-2c`・`matematik-3c`・`matematik-4`・`matematik-5`（name「Matematik nivå 1c」…、sort 10〜14、unit.php で 16〜19 歳と educationalLevel「Gymnasieskolan」、grade_standard() は「Ämnesplan i matematik för gymnasieskolan (Gy25)」）。
`python3 tools/se_gy.py 1c|2c|3c|4|5 [nummer…]`（seed は 98000 + 1000 × ORDER.index(nivå) + 番号、単元の並びは se_gy.COURSES）。単元は `tools/se_g1.py`〜`se_g5.py` の UNITS（引数なしの関数）、共通部品は `tools/se_g.py`（se_h の上に take（åk 7–9 の単元関数から問題関数を取り出す）・nz・xp・pol（{指数: 係数} → 多項式）・deriv・ev・integ・U・graf）。se_g3 に P_（′）・ps・frac_html・rpol・ekx（e<sup>kx</sup>）、se_g4 に cx（a + bi）・pis（π の倍数）・sinv/cosv（特別角の値）・MF（分数の答え）。
standard_code は「Gy25 Matematik nivå 3c · Differential- och integralkalkyl」、standard_url は Skolverket のämnesplan（MATE は 1c・2c、MAT は 3c 以上、se_common.STD_URL_GY）。DOMAIN に FK・AF・TV・SS・LG・DI・KT・TR・DE・DM・PT を足した。talbaser は 2 進数を 1 000 区切りにしないよう se_gy が除外する。
トピック（topic_defs_se）に trigonometri（Trigonometri och vektorer）・derivata-och-integraler・diskret-matematik（Diskret matematik, logik och bevis）を足した
Matematik nivå 1c: 1. potenser-och-rotter ✓ 2. algebra-och-faktorisering ✓ 3. ekvationer-och-formler ✓ 4. funktioner ✓ 5. linjara-funktioner ✓ 6. linjara-olikheter ✓ 7. exponentialfunktioner ✓ 8. potensekvationer ✓ 9. forandringsfaktor ✓ 10. trigonometri ✓ 11. vektorer ✓ 12. sannolikhet ✓ 13. statistik-och-kallkritik ✓ 14. ranta-och-amortering ✓
Matematik nivå 2c: 1. ekvationssystem ✓ 2. kvadreringsreglerna-och-konjugatregeln ✓ 3. andragradsekvationer ✓ 4. andragradsfunktioner ✓ 5. logaritmer ✓ 6. exponentialekvationer ✓ 7. rotekvationer ✓ 8. standardavvikelse-och-percentiler ✓ 9. normalfordelning ✓ 10. regression-och-korrelation ✓ 11. logik-och-bevis ✓ 12. geometriska-satser ✓
Matematik nivå 3c: 1. absolutbelopp-och-rationella-uttryck ✓ 2. polynom ✓ 3. gransvarden ✓ 4. derivatans-definition ✓ 5. deriveringsregler ✓ 6. tangenter ✓ 7. talet-e-och-ln ✓ 8. extrempunkter-och-andraderivata ✓ 9. optimering ✓ 10. primitiva-funktioner ✓ 11. integraler ✓ 12. triangelsatser ✓
Matematik nivå 4: 1. komplexa-tal-i-rektangular-form ✓ 2. komplexa-tal-i-polar-form ✓ 3. polynomekvationer-och-faktorsatsen ✓ 4. enhetscirkeln-och-radianer ✓ 5. trigonometriska-formler ✓ 6. trigonometriska-ekvationer ✓ 7. trigonometriska-grafer ✓ 8. kedjeregeln ✓ 9. produkt-och-kvotregeln ✓ 10. grafer-och-asymptoter ✓ 11. integraler-och-volymer ✓
Matematik nivå 5: 1. differentialekvationer-av-forsta-ordningen ✓ 2. differentialekvationer-av-andra-ordningen ✓ 3. tillampningar-av-differentialekvationer ✓ 4. mangdlara ✓ 5. kombinatorik ✓ 6. talteori-och-kongruensrakning ✓ 7. talbaser ✓ 8. rekursiva-talfoljder ✓ 9. bevismetoder-och-induktion ✓ 10. grafer-och-natverk ✓
SE / Matematik は förskoleklass・årskurs 1〜9・gymnasiet（nivå 1c〜5）まで完了。次は GDP 順で次の国（a・b 系列（1a・1b・2a・2b）は必要なら後で）

NG / Mathematics（NERDC 9-Year Basic Education Curriculum。単元の順は Primary の first・second・third term の scheme of work）— country `ng`（name「Nigeria」、lang en、hreflang en-ng、standard「NERDC 9-Year Basic Education Curriculum: Mathematics」）、subject `maths`（name「Mathematics」）、grade `primary-N`（name「Primary N」、unit.php で N+5〜N+6 歳と educationalLevel「Primary school (9-Year Basic Education)」）、A4。
`python3 tools/ng_p4.py [番号…]`（seed は 150400 + 番号、再利用するモジュールの R は 1509NN）。単元は ng_p4.units() の U(...)、自前の問題は `tools/ng_p4a.py`（skip counting・words・比較・÷10〜50・LCM・HCF・小数・平方・naira と kobo・profit and loss・open sentences・km/m・kg/g・litres/cl・calendar・cardinal points（compass_svg・cp_map）・horizontal/vertical・2D/3D・mode・chance、Roman numerals の rm_write）。
共通部品は `tools/ng_common.py`（ph_common の写し：ナイジェリアの名前と都市、ng_text（US→英国式の綴り、hundred and、pesos→naira、Grade/Year N→Primary N、learners→pupils、standard form→figures）、localize（他国とフィリピンの名前・地名をナイジェリアのものに）、LEAKS、naira（₦1,250.50）、make（seo_title「X – Primary 4 Mathematics Worksheets with Answers (NERDC)」））。US・UK・SG・PH・AU の生成スクリプトの問題関数を mod() で adopt して再利用。
1,000 以上はカンマ、小数は点。お金は ₦ と kobo（₦1 = 100 kobo）。容量は litres と cl。INCH の正規表現が「982 in Roman」「205,040 in words」に当たるので、数の直後に in を書かない。
standard_code は「Primary 4: Number and Numeration」（Number and Numeration／Basic Operations／Algebraic Processes／Measurement／Geometry／Everyday Statistics）、standard_url は https://nerdc.gov.ng/ 。topic_gb() に ng、topics.php に ng の調整（open-sentences→algebra、lowest-common-multiple→factors-and-multiples、decimal-fractions は decimals だけ）

NG / Mathematics / Primary 4
1. whole-numbers-up-to-one-million ✓ 2. skip-counting ✓ 3. comparing-and-ordering-numbers ✓ 4. roman-numerals ✓ 5. addition-and-subtraction ✓ 6. multiplication ✓ 7. division ✓ 8. lowest-common-multiple ✓
9. factors-and-highest-common-factor ✓ 10. fractions ✓ 11. equivalent-fractions-and-adding-fractions ✓ 12. decimal-fractions ✓ 13. multiplying-and-dividing-decimals ✓ 14. squares-and-square-roots ✓ 15. estimation-and-rounding ✓
16. money ✓ 17. open-sentences ✓ 18. length ✓ 19. weight ✓ 20. perimeter-and-area ✓ 21. time ✓ 22. capacity ✓ 23. plane-shapes-symmetry-and-angles ✓ 24. 3d-shapes ✓ 25. everyday-statistics ✓
Primary 1–3・5–6・JSS 1–3 の生成スクリプトは `tools/ng_p1.py`〜`ng_p6.py`・`ng_j1.py`〜`ng_j3.py`（`python3 tools/ng_p5.py [番号…]`。seed は 150N00 + 番号（JSS は 160N00）、再利用するモジュールは 15N9xx・16N9xx）。共通の土台は `tools/ng_unit.py`：
units() に U(slug, 分野, 基準の要約, title, short, meta, key_big, key_sub, sets, think, examples, mistakes, faq) を並べ、main(grade, label, units, base) を呼ぶ。セットの部品は co(自前の maker, 数)、cx(他国の one_x, 数)（お金の問題は落とす）、rs(他国のモジュール, "set_x", 数)（引数は名前から自動：rnd・seen・P・PK・pos・people など。足りないときは rs(..., J=...) で渡す）。
build_sets2 は部品が足りないとき同じセットの他の部品で埋め、他国のセット関数が 4 秒以上かかると打ち切る（無限ループ対策）。le(n) は問題文と正解の数を n 以下に絞る。
自前の問題は `tools/ng_p5a.py`（2 進数・他の進法・温度・利子・割引・手数料・VAT 7.5%・割賦・方位・平均・時刻・速さ・比・2 乗と 3 乗・quantitative reasoning・円）、`tools/ng_low.py`（₦ の硬貨と紙幣の絵 money_svg と LEVEL["MAX"] でお金の上限、Primary 3 の約数、同分母の分数、Primary 1 の絵の問題 p1_*）、`tools/ng_ja.py`（他の進法の計算、複利・減価償却、変分、方程式の文章題）。
ng_common：LABEL（"Primary 5"・"JSS 1"、seo_title に使う）、JSS では "in standard form" を "in figures" に直さない、Year/Grade 7〜9 → JSS 1〜3、ones → units、ℓ → litres、cu cm → cm³、rectangular prism → cuboid、数の空白区切り（70 000）→ カンマ、4 桁以上の小数にもカンマ、"+ −5" → "− 5"、"a octagon" → "an octagon"。adopt は文字列のリストの PLACES だけを置き換える。
2 進数は 1011₂（下付き数字の前の数にはカンマを付けない）。"23 in base b" のように数の直後に in を書かない（INCH で落ちる）。他国のお金（£・$）の問題は ₦ にすると金額が非現実的なので使わない（自前の naira の問題を使う）。
JSS の分野は Number and Numeration／Basic Operations／Algebraic Processes／Mensuration and Geometry／Everyday Statistics、standard_code は「JSS 1: Algebraic Processes」。unit.php で JSS は 12〜15 歳と educationalLevel「Junior Secondary School (Upper Basic Education)」。
トピック（topics.php の ng）：directed-numbers→integers、lcm-and-hcf→factors-and-multiples、commercial-arithmetic・compound-interest→money、approximation→rounding、variation→ratios、quantitative-reasoning→algebra、新しいトピック number-bases（Number Bases）
NG / Mathematics / Primary 1: 1. counting-objects ✓ 2. numbers-up-to-100 ✓ 3. tens-and-units ✓ 4. comparing-numbers ✓ 5. counting-in-2s-5s-and-10s ✓ 6. addition ✓ 7. subtraction ✓ 8. addition-and-subtraction-word-problems ✓ 9. halves-and-quarters ✓ 10. sorting-and-pictograms ✓ 11. money ✓ 12. length-and-capacity ✓ 13. time ✓ 14. shapes ✓
NG / Mathematics / Primary 2: 1. numbers-up-to-200 ✓ 2. counting-in-2s-5s-and-10s ✓ 3. odd-and-even-numbers ✓ 4. addition ✓ 5. subtraction ✓ 6. addition-and-subtraction-word-problems ✓ 7. multiplication ✓ 8. division ✓ 9. fractions ✓ 10. money ✓ 11. length ✓ 12. weight-and-capacity ✓ 13. time ✓ 14. shapes ✓ 15. pictograms ✓
NG / Mathematics / Primary 3: 1. numbers-up-to-999 ✓ 2. odd-and-even-numbers-and-comparing ✓ 3. fractions ✓ 4. equivalent-and-ordering-fractions ✓ 5. addition ✓ 6. subtraction ✓ 7. addition-and-subtraction-word-problems ✓ 8. adding-and-subtracting-fractions ✓ 9. multiplication ✓ 10. division ✓ 11. factors ✓ 12. money ✓ 13. length ✓ 14. perimeter-and-area ✓ 15. capacity ✓ 16. weight ✓ 17. time ✓ 18. calendar ✓ 19. shapes-and-symmetry ✓ 20. pictograms ✓
NG / Mathematics / Primary 5: 1. whole-numbers-up-to-millions ✓ 2. roman-numerals ✓ 3. addition-and-subtraction ✓ 4. multiplication-and-division ✓ 5. prime-numbers-factors-and-multiples ✓ 6. fractions ✓ 7. ratio ✓ 8. adding-and-subtracting-fractions ✓ 9. multiplying-and-dividing-fractions ✓ 10. squares-and-square-roots ✓ 11. estimation-and-rounding ✓ 12. decimals ✓ 13. percentages ✓ 14. algebraic-processes ✓ 15. commercial-arithmetic ✓ 16. perimeter-and-area ✓ 17. volume-and-capacity ✓ 18. time ✓ 19. temperature ✓ 20. bearings-and-directions ✓ 21. angles ✓ 22. plane-shapes ✓ 23. three-dimensional-shapes ✓ 24. length-and-weight ✓ 25. binary-numbers ✓ 26. data-presentation ✓ 27. mean-median-and-mode ✓
NG / Mathematics / Primary 6（Common Entrance）: 1. whole-numbers-up-to-billions ✓ 2. number-bases ✓ 3. factors-lcm-and-hcf ✓ 4. fractions ✓ 5. decimals ✓ 6. percentages ✓ 7. ratio-and-proportion ✓ 8. squares-cubes-and-roots ✓ 9. order-of-operations ✓ 10. algebraic-expressions-and-equations ✓ 11. commercial-arithmetic ✓ 12. length-weight-and-capacity ✓ 13. perimeter-and-area ✓ 14. circles ✓ 15. volume ✓ 16. speed-distance-and-time ✓ 17. angles ✓ 18. plane-shapes-and-solids ✓ 19. averages ✓ 20. data-presentation ✓ 21. probability ✓ 22. quantitative-reasoning ✓
NG / Mathematics / JSS 1: 1. whole-numbers-and-place-value ✓ 2. lcm-and-hcf ✓ 3. fractions ✓ 4. decimals-and-percentages ✓ 5. estimation-and-approximation ✓ 6. number-bases ✓ 7. directed-numbers ✓ 8. order-of-operations ✓ 9. algebraic-expressions ✓ 10. simple-equations ✓ 11. perimeter-and-area ✓ 12. volume-of-cubes-and-cuboids ✓ 13. angles ✓ 14. plane-and-solid-shapes ✓ 15. data-presentation ✓ 16. averages ✓
NG / Mathematics / JSS 2: 1. number-bases ✓ 2. standard-form ✓ 3. approximation-and-significant-figures ✓ 4. squares-and-square-roots ✓ 5. directed-numbers ✓ 6. percentages ✓ 7. commercial-arithmetic ✓ 8. ratio-and-proportion ✓ 9. expansion-and-factorisation ✓ 10. linear-equations ✓ 11. graphs-of-linear-equations ✓ 12. angles-in-parallel-lines-and-polygons ✓ 13. area-of-plane-shapes ✓ 14. volume-of-prisms-and-cylinders ✓ 15. pythagoras-theorem ✓ 16. statistics ✓ 17. probability ✓
NG / Mathematics / JSS 3（BECE）: 1. indices ✓ 2. compound-interest-and-depreciation ✓ 3. variation ✓ 4. factorisation-of-quadratic-expressions ✓ 5. simultaneous-linear-equations ✓ 6. change-of-subject-of-formula ✓ 7. linear-inequalities ✓ 8. similar-shapes ✓ 9. trigonometry ✓ 10. area-and-volume-of-solids ✓ 11. arcs-and-sectors ✓ 12. bearings-and-distances ✓ 13. data-presentation ✓ 14. measures-of-central-tendency ✓ 15. probability ✓
NG / Mathematics / Kindergarten（Nursery 2・KG、5〜6歳、Primary 1 の前の年。grade `kindergarten`（sort 0）、unit.php で educationalLevel Kindergarten / Nursery 2 / ECCDE）— `python3 tools/ng_k.py`（seed は 150000 + 番号、再利用するモジュールは 1580NN）。10 まで（数えるのは 20 まで）、とても短い文、ほぼ全問に絵。
US Kindergarten（gk、引数 K は ng_unit.ARG で Kids）・AU Foundation・SG Primary 1 ordinal（nm は Names）の問題関数を rs() で再利用し、ng_low の p1_* とお金（LEVEL["MAX"] = 50）を足す。noaus で koala・footy などと「1 blue dots」の文法の誤りを落とす。分野は TH_K（Number and Numeration／Basic Operations／Patterns／Measurement／Shapes and Space／Sorting and Data）
1. counting-to-10 ✓ 2. numbers-to-20 ✓ 3. comparing-numbers ✓ 4. ordinal-numbers ✓ 5. number-bonds-to-10 ✓ 6. adding-to-10 ✓ 7. taking-away-within-10 ✓ 8. sharing-and-grouping ✓ 9. naira-money ✓ 10. comparing-length-weight-and-capacity ✓ 11. days-and-times-of-day ✓ 12. shapes ✓ 13. position-and-direction ✓ 14. patterns ✓ 15. sorting-and-data ✓
NG / Mathematics / SSS 1〜3（Senior Secondary School General Mathematics、WAEC・NECO の範囲。SSS 3 が試験の学年）— grade `sss-1`〜`sss-3`（sort 10〜12、unit.php で 15〜18 歳と educationalLevel Senior Secondary School）。`python3 tools/ng_s1.py`〜`ng_s3.py`（seed は 1701NN・1702NN・1703NN、再利用するモジュールは 1719NN・1729NN・1739NN）。分野は ng_s1.TH_S（Number and Numeration／Algebraic Processes／Mensuration／Geometry／Trigonometry／Statistics and Probability／Introductory Calculus／Vectors and Transformation）。
SG Sec 2–4・UK Year 8–9・US Algebra 1/2・Geometry・Precalculus・IN Class 9–12 の one_x を cx() で再利用、自前の問題は `tools/ng_sa.py`（modular arithmetic・logarithms（log 2 = 0.3010 など）・logical reasoning・percentage error・linear と quadratic の連立・微分（d_*）・積分（i_*）・longitude and latitude（R = 6400 km、π = 22/7）・shares・income tax・annuity・loan・0°〜360° の三角比（t_*））。mcq は負の int を落とすので、負の数は sn() で文字列にして渡す。
ng_common：GRADE が sss のとき m∠ → ∠、to the nearest tenth → correct to 1 decimal place、slope → gradient、「+ −分数」→「− 分数」。Grade/Class 10–12 → SSS 1–3。インドの名前・地名、₹・rupee・lakh・India を LEAKS に。「foot of the tower」は INCH にしない。ng_ok は ng_text 後に選択肢が重なる問題を落とす。IN の一部の生成スクリプト（gen_in_maths_c11_sets など）は import すると自分の JSON を書き直す（内容は同じ）。US Algebra 2 の三角関数のグラフは弧度法なので使わない（SSS は度）
SSS 1: 1. number-bases ✓ 2. modular-arithmetic ✓ 3. indices-and-standard-form ✓ 4. logarithms ✓ 5. sets-and-venn-diagrams ✓ 6. logical-reasoning ✓ 7. quadratic-equations ✓ 8. lengths-and-areas-of-plane-shapes ✓ 9. surface-area-and-volume-of-solids ✓ 10. trigonometric-ratios ✓ 11. angles-of-elevation-and-depression ✓ 12. bearings ✓ 13. data-presentation ✓ 14. measures-of-central-tendency ✓ 15. probability ✓
SSS 2: 1. approximation-and-percentage-error ✓ 2. sequences-and-series ✓ 3. completing-the-square-and-quadratic-formula ✓ 4. simultaneous-linear-and-quadratic-equations ✓ 5. linear-inequalities ✓ 6. algebraic-fractions ✓ 7. graphs-of-quadratic-functions ✓ 8. circle-theorems ✓ 9. chords-and-tangents ✓ 10. sine-and-cosine-rules ✓ 11. trigonometric-graphs-and-angles ✓ 12. bearings-and-distances ✓ 13. cumulative-frequency ✓ 14. measures-of-dispersion ✓ 15. probability-of-combined-events ✓
SSS 3: 1. surds ✓ 2. matrices-and-determinants ✓ 3. coordinate-geometry ✓ 4. differentiation ✓ 5. applications-of-differentiation ✓ 6. integration ✓ 7. longitude-and-latitude ✓ 8. vectors ✓ 9. transformations ✓ 10. commercial-arithmetic ✓ 11. permutations-and-combinations ✓
トピック（topics.php の ng）：cumulative-frequency・measures-of-dispersion→data-and-graphs、chords-and-tangents→circles、integration→calculus、longitude-and-latitude→measurement
NG / Mathematics は Kindergarten〜SSS 3 まで完了。mq-geo.js と mq.php の MQ_GEO に ng を足した（2026-11-26）

その後: …（新しい学年・国は `catalog.json` に追加）

## 理科（Science）

教科を増やすときは catalog.json の subjects に（国, slug）を足す。理科は subject `science`（name「Science」）。
基準の名前は国の standard（算数用）と別なので、core.php の `subject_standard()` の表に「国/教科 → 基準名」を足す（grade_standard・国ページ・教科ページ・トピックページ・プレビューがこれを使う）。
トピックは教科ごと：topics.php の `topic_defs($country, $subject)` が science なら `topic_defs_science()`（matter・forces-and-motion・energy・living-things-and-ecosystems・earth-and-space・earths-systems・engineering-design）。
生成スクリプトは `gen_{国}_science_{学年}_*`、共通部品は `tools/sci_common.py`：
- `Unit(seed)` の `sets([(セット名, [maker, (maker, 上限), ...]) × 5])`。maker は item を返す関数（None で作り直し）。同じ問題文＋答えは単元の中で1回だけ。1つの maker は1セットに6問まで（(maker, n) で変える。足りないときは自動で少しずつ増やす）
- `bank([(問題, 答え, [誤答3], 解説)])` は手書きの問題（作るときに検査する）
- `item()`・`lesson(考え方HTML, [(例題, [手順], 答え)], [よくある間違い])`・`make(grade, slug, sort, NGSSコード, 原文, title, seo_title, short, meta, key_big, key_sub, body, faq, sets)`（standard_url は NGSS の PE ページ、domain は PS/LS/ESS/ETS から自動）
- 図：`bar_chart`・`pie`・`arrow`・`sun`。食物網は `tools/sci_foodweb.py`（meadow・pond・ocean・forest・desert、手で配置した図、矢印は「食べられるもの → 食べるもの」、plural()）
- 印刷で大きく出す図（食物網・公転・物質の循環・地球と重力）は `<svg data-pf='xl'>`（print.php が全幅にし、入らないときは次の小さい問題を入れる）
問題文に答えを決める数・名前・場面を入れる（同じ文は重複扱い）。誤答は「よくある間違い」から。理科の事実は正確に（食物網の食べるもの、星の距離、水の割合など）

US / Science / Grade 5（NGSS）
1. matter-is-made-of-particles (5-PS1-1) ✓ 2. properties-of-materials (5-PS1-3) ✓ 3. mixtures-and-solutions ✓ 4. physical-and-chemical-changes (5-PS1-4) ✓ 5. conservation-of-mass (5-PS1-2) ✓
6. gravity (5-PS2-1) ✓ 7. energy-in-food (5-PS3-1) ✓ 8. what-plants-need-to-grow (5-LS1-1) ✓ 9. food-webs (5-LS2-1) ✓ 10. decomposers-and-the-cycle-of-matter ✓
11. sun-and-stars (5-ESS1-1) ✓ 12. shadows-day-and-night (5-ESS1-2) ✓ 13. patterns-in-the-night-sky ✓ 14. earths-systems (5-ESS2-1) ✓ 15. water-on-earth (5-ESS2-2) ✓
16. protecting-earths-resources (5-ESS3-1) ✓ 17. engineering-design (3-5-ETS1) ✓

US / Science / Grade 4（NGSS。seed は 401xx）
1. energy-and-speed (4-PS3-1) ✓ 2. energy-transfer (4-PS3-2) ✓ 3. electric-circuits (4-PS3-2) ✓ 4. energy-conversions (4-PS3-4) ✓ 5. collisions (4-PS3-3) ✓
6. waves (4-PS4-1) ✓ 7. light-and-how-we-see (4-PS4-2) ✓ 8. sending-information-with-patterns (4-PS4-3) ✓ 9. plant-structures (4-LS1-1) ✓ 10. animal-structures (4-LS1-1) ✓
11. senses-and-the-brain (4-LS1-2) ✓ 12. rock-layers-and-fossils (4-ESS1-1) ✓ 13. weathering-and-erosion (4-ESS2-1) ✓ 14. earths-features-and-maps (4-ESS2-2) ✓
15. energy-resources (4-ESS3-1) ✓ 16. natural-hazards (4-ESS3-2) ✓
トピック waves-and-light（Waves, Light and Information）を足した。classifier() は分類が 3 つ以下だと what 側の誤答が足りないので、自前の maker を書く。
Unit の重複判定は問題文（図・表を除く文）なので、文に場面・名前・数を入れて変化させる

US / Science / Grade 3（NGSS。seed は 301xx）
1. balanced-and-unbalanced-forces (3-PS2-1) ✓ 2. patterns-of-motion (3-PS2-2) ✓ 3. magnets-and-static-electricity (3-PS2-3) ✓ 4. designing-with-magnets (3-PS2-4) ✓
5. life-cycles (3-LS1-1) ✓ 6. animal-groups (3-LS2-1) ✓ 7. inherited-traits (3-LS3-1) ✓ 8. traits-and-the-environment (3-LS3-2) ✓ 9. fossils-and-past-environments (3-LS4-1) ✓
10. variation-and-survival (3-LS4-2) ✓ 11. habitats-and-survival (3-LS4-3) ✓ 12. environmental-change (3-LS4-4) ✓ 13. weather-data (3-ESS2-1) ✓ 14. climates-of-the-world (3-ESS2-2) ✓
15. weather-hazards (3-ESS3-1) ✓

US / Science / Grade 6–8（NGSS MS は 3 学年まとめての基準なので、California の Preferred Integrated Model の配分で学年に分ける。seed は 601xx・701xx・801xx）
Grade 6（✓ 12 単元すべて）: cells-and-cell-theory (MS-LS1-1)、parts-of-a-cell (MS-LS1-2)、body-systems (MS-LS1-3)、senses-and-the-nervous-system (MS-LS1-8)、particles-and-states-of-matter (MS-PS1-4)、
thermal-energy-and-temperature (MS-PS3-4)、designing-to-control-heat-transfer (MS-PS3-3)、the-water-cycle (MS-ESS2-4)、air-masses-and-weather (MS-ESS2-5)、ocean-and-atmosphere-circulation (MS-ESS2-6)、
global-temperature-and-climate-change (MS-ESS3-5)、engineering-design-process (MS-ETS1-1〜4)
Grade 7（✓ 17 単元すべて）: atoms-and-molecules (MS-PS1-1)、properties-and-chemical-reactions (MS-PS1-2)、synthetic-materials (MS-PS1-3)、conservation-of-atoms (MS-PS1-5)、energy-in-chemical-reactions (MS-PS1-6)、
photosynthesis (MS-LS1-6)、cellular-respiration (MS-LS1-7)、resources-and-populations (MS-LS2-1)、interactions-in-ecosystems (MS-LS2-2)、cycling-of-matter-and-energy-flow (MS-LS2-3)、
ecosystem-changes (MS-LS2-4)、protecting-biodiversity (MS-LS2-5)、the-rock-cycle (MS-ESS2-1)、shaping-earths-surface (MS-ESS2-2)、plate-tectonics (MS-ESS2-3)、natural-resources (MS-ESS3-1)、human-impact-on-the-environment (MS-ESS3-3, MS-ESS3-4)
Grade 8（✓ 22 単元すべて）: newtons-third-law (MS-PS2-1)、forces-and-motion (MS-PS2-2)、electric-and-magnetic-forces (MS-PS2-3, MS-PS2-5)、gravity-and-mass (MS-PS2-4)、kinetic-energy (MS-PS3-1)、potential-energy (MS-PS3-2)、
energy-transfer-and-motion (MS-PS3-5)、wave-properties (MS-PS4-1)、light-and-sound-waves (MS-PS4-2)、digital-signals (MS-PS4-3)、plant-and-animal-reproduction (MS-LS1-4, MS-LS1-5)、
genes-and-mutations (MS-LS3-1)、asexual-and-sexual-reproduction (MS-LS3-2)、fossil-record (MS-LS4-1, MS-LS4-2)、embryo-similarities (MS-LS4-3)、natural-selection (MS-LS4-4, MS-LS4-6)、
artificial-selection-and-genetic-engineering (MS-LS4-5)、earth-moon-sun-system (MS-ESS1-1)、gravity-in-the-solar-system (MS-ESS1-2)、scale-of-the-solar-system (MS-ESS1-3)、geologic-time-scale (MS-ESS1-4)、forecasting-natural-hazards (MS-ESS3-2)
1 つの問題関数が同じ数・同じ文を何度も作らないよう、生成スクリプトの中で once(key, n) を使って回数を決める（名前だけ違う問題を減らす）

US / Science / K–2（NGSS。grade `kindergarten`（sort 0）・`grade-1`・`grade-2`。生成スクリプトは `gen_us_science_gk_*`（seed 91xx）・`g1_*`（101xx）・`g2_*`（201xx））
K–2 は**ページの上を軽く**：make() が title ≤ 40・key_big ≤ 40・key_sub ≤ 90 字を assert。body は `kid_lesson(絵, 太字の一文, [短い要点 3 つ], 例題, よくある間違い)`（絵と一文を先に、例題と間違いは後ろ）。太字の一文は key_big と同じにしない。
絵は `tools/sci_kids.py`（icon・card・row（words が長いとセル幅を自動で広げる）・scene、k_pics の絵も使える）。K はとても短い文でほぼ全問に絵、G1 は短い文で絵を多く。
同じ once のキーを別の問題関数で使わない（("eat", k) のように接頭辞を付ける）。似た答え（「plants and animals」と「plants and small animals」、嵐と竜巻など）を誤答に入れない
Kindergarten: 1. pushes-and-pulls (K-PS2-1) ✓ 2. changing-speed-and-direction (K-PS2-2) ✓ 3. sunlight-warms-earth (K-PS3-1) ✓ 4. shade-structures (K-PS3-2) ✓ 5. what-plants-and-animals-need (K-LS1-1) ✓
6. weather (K-ESS2-1) ✓ 7. how-living-things-change-their-environment (K-ESS2-2) ✓ 8. where-plants-and-animals-live (K-ESS3-1) ✓ 9. severe-weather (K-ESS3-2) ✓ 10. caring-for-earth (K-ESS3-3) ✓
Grade 1: 1. sound-and-vibrations (1-PS4-1) ✓ 2. light-and-seeing (1-PS4-2) ✓ 3. light-and-materials (1-PS4-3) ✓ 4. sending-signals-with-light-and-sound (1-PS4-4) ✓ 5. plant-and-animal-parts (1-LS1-1) ✓
6. parents-and-offspring (1-LS1-2) ✓ 7. young-plants-and-animals (1-LS3-1) ✓ 8. sun-moon-and-stars (1-ESS1-1) ✓ 9. daylight-and-seasons (1-ESS1-2) ✓
Grade 2: 1. properties-of-materials (2-PS1-1) ✓ 2. choosing-materials (2-PS1-2) ✓ 3. building-with-small-pieces (2-PS1-3) ✓ 4. heating-and-cooling (2-PS1-4) ✓ 5. what-plants-need (2-LS2-1) ✓
6. pollination-and-seed-dispersal (2-LS2-2) ✓ 7. habitats-and-biodiversity (2-LS4-1) ✓ 8. fast-and-slow-earth-changes (2-ESS1-1) ✓ 9. stopping-wind-and-water-erosion (2-ESS2-1) ✓
10. maps-of-land-and-water (2-ESS2-2) ✓ 11. solid-and-liquid-water (2-ESS2-3) ✓ 12. solving-problems-like-an-engineer (K-2-ETS1) ✓
トピック（topic_defs_science）：small-pieces・heating-and-cooling→matter、pollinat・offspring・living-things→living-things、engineer→engineering-design、sound-and-vibration→waves-and-light、shade→energy、sunlight-warms→energy だけ

US / Science / 高校（NGSS HS は科目に分かれていないので、一般的な 4 科目に分ける）— grade は科目：`biology`（sort 9）・`chemistry`（10）・`physics`（11）・`earth-and-space-science`（12）。unit.php に年齢と educationalLevel、core.php の gs() は科目名だけ
Biology（gen_us_science_bio_*、seed 901NN。HS-LS1〜LS4）: 1. dna-and-protein-synthesis ✓ 2. levels-of-organization ✓ 3. homeostasis-and-feedback ✓ 4. cell-division-and-differentiation ✓ 5. photosynthesis ✓ 6. carbon-and-macromolecules ✓ 7. cellular-respiration ✓
8. populations-and-carrying-capacity ✓ 9. energy-flow-and-matter-cycling ✓ 10. carbon-cycle ✓ 11. ecosystem-stability-and-biodiversity ✓ 12. group-behavior ✓ 13. meiosis-and-genetic-variation ✓ 14. punnett-squares-and-heredity ✓
15. evidence-for-evolution ✓ 16. natural-selection-and-adaptation ✓ 17. changes-in-trait-frequency ✓ 18. speciation-extinction-and-biodiversity ✓
Chemistry（gen_us_science_chem_*、seed 902NN。HS-PS1・PS2-6・PS3-4。共通データは `tools/sci_chem.py`：EL（元素）・EN/IE/RAD（傾向は実データで確かめた組だけを問う）・valence・ion_charge・atoms（式の原子数、かっこ対応）・split_eq・tally・eq_html・AM（教室用の原子量）・molar・num（カンマ付き）・STOICH（つり合った式））:
1. atomic-structure-and-isotopes ✓ 2. periodic-table-and-trends ✓ 3. chemical-bonding ✓ 4. intermolecular-forces-and-properties ✓ 5. types-of-chemical-reactions ✓ 6. balancing-chemical-equations ✓ 7. the-mole-and-molar-mass ✓
8. stoichiometry ✓ 9. energy-in-chemical-reactions ✓ 10. reaction-rates ✓ 11. chemical-equilibrium ✓ 12. nuclear-chemistry ✓ 13. thermal-energy-and-specific-heat ✓ 14. molecular-structure-and-materials ✓
化学の質量・量は現実に合わせる（Fe:S = 7:4 など、反応しきる量の比）。4 けた以上の数はカンマ（num、または生成後に commas()）
Physics（gen_us_science_phys_*、seed 903NN。HS-PS2・PS3・PS4。共通部品は `tools/sci_phys.py`：num（カンマ、負は −）・sci（× 10 の累乗）・uniq（答えと違う誤答 3 つ。足りないと None）・safe（maker を包み、誤答がそろわない問題を飛ばす）。g = 9.8 m/s²）:
1. motion-and-kinematics ✓ 2. newtons-laws-and-net-force ✓ 3. momentum-and-collisions ✓ 4. impulse-and-collision-safety ✓ 5. gravitational-force ✓ 6. electric-force-and-coulombs-law ✓ 7. electromagnetism-and-induction ✓ 8. kinetic-and-potential-energy ✓
9. conservation-of-energy ✓ 10. energy-conversion-and-efficiency ✓ 11. electric-and-magnetic-fields ✓ 12. wave-properties ✓ 13. digital-and-analog-signals ✓ 14. wave-particle-duality ✓ 15. electromagnetic-radiation-and-matter ✓ 16. wave-technologies ✓
物理の数値は現実に合わせる（衝突後の運動エネルギーが前より増えない、ランプの強さなど）。人の名前を使う問題は who で代名詞を避ける
Earth and Space Science（gen_us_science_ess_*、seed 904NN。HS-ESS1〜3。sci_phys の num・uniq・safe を使う）: 1. the-sun-and-nuclear-fusion ✓ 2. the-big-bang ✓ 3. stars-and-the-origin-of-elements ✓ 4. keplers-laws-and-orbits ✓ 5. plate-tectonics-and-crust-age ✓ 6. earths-early-history ✓
7. landforms-and-earth-processes ✓ 8. earths-interior-and-mantle-convection ✓ 9. feedbacks-in-earth-systems ✓ 10. climate-and-energy-flow ✓ 11. water-and-earth-materials ✓ 12. carbon-cycle-and-earth-systems ✓ 13. coevolution-of-life-and-earth ✓
14. natural-resources-and-hazards ✓ 15. sustainability-and-human-impact ✓ 16. climate-change-data-and-models ✓
トピック：big-bang・kepler・orbit・universe→earth-and-space、matter の out に nuclear-fusion・earth-materials、living-things の out に climate-and-energy
US / Science は Kindergarten〜Grade 8・高校 4 科目（Biology・Chemistry・Physics・Earth and Space Science）まで完了。次は他の国の理科か、GDP 順で次の国の算数

UK / Science（National Curriculum in England, science programmes of study）— country `uk`、subject `science`、grade `year-N`、A4。生成スクリプトは `gen_uk_science_yN_*`（seed は 6NNcc：Year 6 は 616cc）、共通部品は `tools/uk_sci.py`（sci_common の上に make_uk(year, slug, sort, topic, std_text, …)：standard_code「Year 6: Light」、domain は programme of study の見出し（Light、Electricity、Animals, including humans、Living things and their habitats、Evolution and inheritance、Working scientifically）、standard_url は GOV.UK の science programmes of study。UK の名前（uk_ks3.People）。LEAKS で color・meter・liter・behavior・gray・aluminum・flashlight・Mom・inch など米国の語を落とす（newton meter は除く））と図 `tools/uk_sci_pics.py`（circuit・parallel・symbol：英国の回路記号（cell・battery・lamp・switch_open/closed・buzzer・motor・gap・wire）、layers（地層と化石）、seeing（光源→物→目の光線図）、shadow_setup）。
イギリス英語（colour, metre, litre, centre, torch, Mum, aluminium, fibre, mould, favourite, pupils）。sci_common.make に country・url を足した（Year 1・2 は K–2 と同じくページ上部を軽く）。Unit.take は TypeError・KeyError なども None 扱い。
**Unit の重複判定は問題文（タグを除く）＋正解なので、図だけ違う問題は同じ文にしない**（文に数・名前・選択肢を入れる）
UK / Science / Year 6
1. classifying-living-things ✓ 2. classification-keys ✓ 3. micro-organisms ✓ 4. the-circulatory-system ✓ 5. diet-exercise-and-lifestyle ✓ 6. transporting-nutrients-and-water ✓ 7. fossils ✓ 8. inheritance-and-variation ✓
9. adaptation-and-evolution ✓ 10. how-light-travels ✓ 11. how-we-see ✓ 12. shadows-and-reflection ✓ 13. circuit-symbols ✓ 14. brightness-and-voltage ✓ 15. circuits-and-switches ✓ 16. working-scientifically ✓
トピック：classif・circulatory・diet-・nutrient・^fossils$・micro-organism→living-things、voltage→energy、how-we-see・reflection→waves-and-light（earth-and-space の out に reflection）、working-scientifically（新トピック、3 単元以上で公開）
UK / Science / Year 5（seed 615cc）
1. life-cycles ✓ 2. reproduction-in-plants-and-animals ✓ 3. growing-up-and-old-age ✓ 4. properties-of-materials ✓ 5. dissolving-and-solutions ✓ 6. separating-mixtures ✓ 7. reversible-and-irreversible-changes ✓
8. the-solar-system ✓ 9. day-night-and-the-moon ✓ 10. gravity ✓ 11. air-and-water-resistance ✓ 12. friction ✓ 13. levers-pulleys-and-gears ✓ 14. working-scientifically ✓（Year 6 の問題関数を import し、EXP・CONC・seed を入れ替えて再利用）
トピック：resistance・friction・lever→forces-and-motion、growing-up→living-things、reversible→matter
UK / Science / Year 4（seed 614cc。Year 6 の生成スクリプトを import して U・R・P を新しい seed に入れ替え、uk_sci.USED.clear() してから問題関数を再利用できる）
1. grouping-living-things ✓ 2. using-classification-keys ✓ 3. changing-environments ✓ 4. the-digestive-system ✓ 5. teeth ✓ 6. food-chains ✓ 7. solids-liquids-and-gases ✓
8. changes-of-state ✓ 9. the-water-cycle ✓ 10. how-sounds-are-made ✓ 11. pitch-and-volume ✓ 12. electrical-appliances-and-circuits ✓ 13. conductors-and-insulators ✓ 14. working-scientifically ✓
uk_sci の LEAKS は「sound meter・newton meter」など計器の meter を除く（英国でも計器は meter）
**セットの配分を書く前に、各問題関数が作れる問題の数を数える**（ちょうど同じ数だと soft cap で足りなくなる。余裕をもたせる）
UK / Science / Year 3（seed 613cc。図は uk_sci_pics の plant(labels)（花・葉・茎・根に A〜D）と magnets(a, b)・_bar（棒磁石、N は赤・S は青））
1. parts-of-a-flowering-plant ✓ 2. what-plants-need-to-grow ✓ 3. how-water-moves-in-plants ✓ 4. flowers-pollination-and-seeds ✓ 5. food-and-nutrition ✓ 6. skeletons-and-muscles ✓ 7. comparing-and-grouping-rocks ✓
8. how-fossils-are-formed ✓ 9. soils ✓ 10. light-and-dark ✓ 11. shadows ✓ 12. pushes-pulls-and-surfaces ✓ 13. magnets-attract-and-repel ✓ 14. magnetic-materials ✓ 15. working-scientifically ✓
Year 5・6 の問題関数を再利用（reproduction・diet・fossils・light・shadows・friction・working scientifically）。2 つのモジュールを使うときは両方の U・R・P を同じ Unit にする（shadows）。
光の実験は暗い所の植物の高さを測らない（暗所の植物は伸びる）。葉の数にする。鋼の釘で引っかけるのは granite・basalt・obsidian 以外（marble・slate も傷が付く）。英国の 1p・2p 硬貨は鋼なので磁石の問題に硬貨を使わない
pool を数える: `cd tools; python3 sci_pool.py モジュール名 g_x g_y`（maker を 5000 回呼んで問題文＋答えの種類を数える）。図だけ違う問題は数に入らない
トピック：nutrition・skeleton・fossils-are→living-things、fossils-are・^soils$→earths-systems（out に water-moves）、^shadows$→waves-and-light
UK / Science / Year 2（KS1。seed 612cc。ページの上は軽く（title ≤ 40・key_big ≤ 40・key_sub ≤ 90）、body は kid_lesson（K.row の絵＋太字の一文）。共通部品は `tools/uk_ks1.py`（sci_kids の絵に英国の名前：bug → ladybird、flashlight → torch。card・row・which_of）。LEAKS に ladybug
1. living-dead-and-never-alive ✓ 2. habitats ✓ 3. microhabitats ✓ 4. simple-food-chains ✓ 5. seeds-and-bulbs ✓ 6. what-plants-need-to-stay-healthy ✓
7. animals-and-their-young ✓ 8. what-animals-need-to-survive ✓ 9. staying-healthy ✓ 10. uses-of-everyday-materials ✓ 11. changing-the-shape-of-materials ✓ 12. working-scientifically ✓
**set の配分は pool を数えてから書く。`if False`・`(g, 0)`・`[...][:n]` のような仮の書き方を set に残さない**（`grep -n "if False\|, 0)" ファイル` で確かめる）
誤答に正解と同じ意味の選択肢を入れない（「too cold」が 2 つ、「melt」が 2 つなど）。答えの種類（good・cold・hot など）で誤答を選ぶ
トピック：living-dead・seeds-and-bulbs・staying-healthy→living-things
UK / Science / Year 1（KS1。seed 611cc。Year 2 と同じルール。人の体の図は uk_sci_pics.body(labels)（体の右側から線を引き、ラベルの縦位置は 30 px 以上あける））
1. garden-and-wild-plants ✓ 2. deciduous-and-evergreen-trees ✓ 3. parts-of-a-plant ✓ 4. animal-groups ✓ 5. carnivores-herbivores-and-omnivores ✓ 6. animal-bodies ✓
7. parts-of-the-body ✓ 8. the-five-senses ✓ 9. objects-and-materials ✓ 10. properties-of-materials ✓ 11. four-seasons ✓ 12. weather-and-day-length ✓
性質の問題の誤答は物ごとに手で書く（紙やすりに「dull」も当てはまるため）。天気の誤答は近い天気（stormy と windy、foggy と cloudy、frosty と snowy）を外す
トピック：carnivore・evergreen→living-things、day-length→earth-and-space、four-seasons→earths-systems
UK / Science / KS3 Year 7–9（National Curriculum の KS3 science は 3 学年まとめての内容なので、一般的な配分で学年に分ける）— seed は 617cc・618cc・619cc。make_ks3(year, slug, sort, subject, topic, …)：standard_code「KS3 Biology: Cells and organisation」、domain は Biology／Chemistry／Physics。
US の NGSS 生成スクリプトの問題関数は `uk_sci.adopt_us(モジュール名, U)`（U・R・UK の People を入れる）と `ukm(maker)`（UKSP でイギリス式に直す：colour・metre・aluminium・caesium・non-metal・reactivity series・displacement・fertiliser・rubbish・power station・sledge・toilet など。米国の語・単位が残ると落とす。名前・数字・表を除いた文で重複を判定するので、データだけ違う同じ問題は 1 回）で再利用する。
US の生成スクリプトの数は ukm を通すと少なくなる。sci_pool.py で ukm した名前（us_x = ukm(M.g_x)）を数えてから配分を書く。US の族の番号（17・18）は使わない（UK は group 7・0）。不溶の金属酸化物（鉄・銅）を「アルカリ性」にしない。お金は 100p 以上を £1.04 の形に
Year 7: 1. cells ✓ 2. specialised-cells-and-organisation ✓ 3. skeleton-and-muscles ✓ 4. human-reproduction ✓ 5. plant-reproduction ✓ 6. particles-and-states-of-matter ✓ 7. elements-atoms-and-compounds ✓ 8. acids-and-alkalis ✓ 9. mixtures-and-separation ✓ 10. forces ✓ 11. sound ✓ 12. light ✓ 13. space ✓
Year 8: 1. food-and-digestion ✓ 2. breathing-and-gas-exchange ✓ 3. respiration ✓ 4. photosynthesis ✓ 5. ecosystems-and-food-webs ✓ 6. periodic-table ✓ 7. metals-and-non-metals ✓ 8. chemical-reactions ✓ 9. rocks-and-the-rock-cycle ✓ 10. the-atmosphere-and-climate ✓ 11. electricity ✓ 12. magnetism-and-electromagnets ✓ 13. energy-and-power ✓
Year 9: 1. inheritance-and-dna ✓ 2. variation-and-evolution ✓ 3. health-and-drugs ✓ 4. exothermic-and-endothermic-reactions ✓ 5. reactivity-and-extraction ✓ 6. materials ✓ 7. speed-and-motion ✓ 8. pressure ✓ 9. work-and-moments ✓ 10. waves ✓ 11. thermal-energy ✓ 12. gravity-and-space ✓
KS3 の範囲を超える US の問題（ΔH・kJ/mol・g/mol・逆反応の活性化エネルギー）は包んで落とす。KS3 の用語：resultant force・polythene・ethene・fibreglass
トピック：digestion・gas-exchange・health-and-drugs→living-things、metals-and・extraction→matter、^pressure$・moments→forces-and-motion、gravity-and-space→earth-and-space も
UK / Science / KS4 Year 10–11（GCSE Combined Science。AQA などの一般的な配分で 2 学年に分ける）— seed は 620cc・621cc。make_ks4(year, slug, sort, subject, topic, …)：standard_code「KS4 Biology: Bioenergetics」、domain は Biology／Chemistry／Physics。
共通部品は `tools/uk_ks4.py`：U4(seed) → (U, R, P, us)。us("chem_reaction_rates", "g_rate", drop=(…), rep=((古い, 新しい), …)) で US 高校の問題関数をイギリス式（ukm）にして使う（rep で文字を置き換え、drop で語を含む問題を落とす）。us.uk(モジュール, 関数) で UK の生成スクリプトの問題関数を同じ U・R・P で使う。build(U, year, slug, sort, subject, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets)。
生成スクリプトは `if __name__ == "__main__":` の後で build を呼ぶ（sci_pool.py で import しても JSON を書かない）。体積は cm³、血糖は mmol/L、g = 9.8 N/kg、photon・ATP・meiosis I は使わない（rep・drop で消す）。UKSP に trolley・lorry・ionise・fertilise などを足した
Year 10: 1. cell-structure-and-transport ✓ 2. cell-division ✓ 3. organisation-and-enzymes ✓ 4. infection-and-response ✓ 5. atomic-structure-and-the-periodic-table ✓ 6. bonding-and-structure ✓ 7. quantitative-chemistry ✓ 8. chemical-changes ✓ 9. energy-changes ✓ 10. energy ✓ 11. electricity ✓ 12. particle-model-and-density ✓ 13. atomic-structure-and-radioactivity ✓
Year 11: 1. photosynthesis-and-respiration ✓ 2. homeostasis-and-hormones ✓ 3. genetics-and-evolution ✓ 4. ecology ✓ 5. rates-and-equilibrium ✓ 6. organic-chemistry ✓ 7. chemical-analysis ✓ 8. chemistry-of-the-atmosphere ✓ 9. using-resources ✓ 10. forces-and-motion ✓ 11. waves-and-the-electromagnetic-spectrum ✓ 12. magnetism-and-electromagnetism ✓
トピック：infection・enzyme・^ecology$→living-things（out に bonding-and-structure）、quantitative・chemical-analysis・organic→matter、atmosphere→earths-systems、forces-and-motion の out に electromagnetic-spectrum
UK / Science / Year 12–13（A level Biology・Chemistry・Physics。DfE の GCE AS and A level subject content。Year 12 は AS の内容、Year 13 は残り。1 つの学年ページに 3 科目が並ぶ（domain が Biology／Chemistry／Physics））— standard_code は「A level Chemistry: Physical chemistry」形式、standard_url は GOV.UK の GCE AS and A level biology, chemistry, physics and psychology、seo_title は「Year 12 A Level Physics: Electricity Worksheets」。
問題は `tools/al_bio.py`・`al_chem.py`・`al_phys.py`（すべて自前。各モジュールの R を build が入れ替える。maker は k=None で種類を選び、K(f, "kind", …) で種類を固定）。UNITS(year) に U(subject, sort, slug, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets) を並べる。
共通部品は `tools/uk_alsci.py`：nf（3 有効数字、1,000 からカンマ、10⁻³ 未満・10⁶ 以上は × 10ⁿ）、nq（数の答え。誤答は実際の間違いから、すべて整数なら整数で表示、3 つそろわないと None）、tq（文の答え）、once_maker（手書きの問題の bank）、build(mod, year, slug)（seed は 700000 + 100 × 学年 + sort、「-5」を「−5」に、米国式の語を LEAK で止める）。gen_uk_science_y12_*・y13_* は build を呼ぶだけ。
bank は単元全体で 1 回ずつしか使えないので、使う数より 3〜5 行多く書く。pool は scratchpad の alpool.py（maker を 4000 回呼んで種類を数える）で確かめてから配分を書く。定数は data sheet の値（h = 6.63 × 10⁻³⁴、g = 9.81、R = 8.31、Kw = 1.00 × 10⁻¹⁴）、A<sub>r</sub> は小数第 1 位
Year 12: Biology 1. biological-molecules ✓ 2. cells-and-the-immune-system ✓ 3. exchange-and-transport ✓ 4. genetic-information-and-variation ✓／Chemistry 6. atomic-structure-and-amount-of-substance ✓ 7. bonding-and-energetics ✓ 8. kinetics-and-equilibria ✓ 9. redox-and-inorganic-chemistry ✓ 10. organic-chemistry-alkanes-alkenes-and-alcohols ✓／Physics 11. particles-and-quantum-phenomena ✓ 12. waves-and-optics ✓ 13. mechanics-and-materials ✓ 14. electricity ✓
Year 13: Biology 1. photosynthesis-respiration-and-energy-transfer ✓ 2. response-and-homeostasis ✓ 3. genetics-populations-and-evolution ✓ 4. gene-expression-and-biotechnology ✓／Chemistry 5. thermodynamics-and-rate-equations ✓ 6. acids-bases-and-electrode-potentials ✓ 7. transition-metals ✓ 8. further-organic-chemistry-and-analysis ✓／Physics 9. circular-motion-and-oscillations ✓ 10. thermal-physics-and-ideal-gases ✓ 11. gravitational-and-electric-fields ✓ 12. capacitors-and-magnetic-fields ✓ 13. nuclear-physics ✓
トピック：biological-molecules・exchange-and-transport→living-things、kinetics・acids-bases・transition-metals→matter、mechanics・gravitational→forces-and-motion、thermal・capacitor→energy、genetic-information は energy・waves の out
UK / Science は Year 1〜13（KS1〜KS4 Combined Science、A level Biology・Chemistry・Physics）まで完了。次は他の国の理科

IN / Science（CBSE 2025-26 Science syllabus / NCERT 教科書。1 単元 = 1 章）— country `in`、subject `science`、grade `class-N`、A4。standard_code は「Class 10, Chapter 11: Electricity」、domain は CBSE の Unit（Chemical Substances – Nature and Behaviour／World of Living／Natural Phenomena／Effects of Current／Natural Resources）、standard_url は cbseacademic の Science_Sec_2025-26.pdf（in_sci.STD_URL）。core.php の subject_standard() に 'in/science'。
共通部品は `tools/in_sci.py`（U(sort, slug, chapter, unit_name, std, title, short, meta, kb, ks, think, ex, mist, faq, sets)、pairs(rows, fwd, back)（表から両方向の問題）、K(f, *kinds)、build(mod, level, slug)：seed は 720000 + 100 × level + sort、インドの名前、「-5」→「−5」、LEAK（米国式の語と $・£・pupils・GCSE・miles など）で止める）。数は uk_alsci の nf・nq・tq・once_maker。
単元の定義は `tools/in_sci10.py`（UNITS(level)）＝ in_sci10a（化学 Ch 1–4）＋ in_sci10b（生物 Ch 5–8・13）＋ in_sci10c（物理 Ch 9–12：New Cartesian sign convention、鏡 1/v + 1/u = 1/f、レンズ 1/v − 1/u = 1/f、P = 1/f、V = IR、₹ の kWh、Fleming の左手の法則、220 V・50 Hz）。gen_in_science_c10_* は build を呼ぶだけ。
IN / Science / Class 10: 1. chemical-reactions-and-equations ✓ 2. acids-bases-and-salts ✓ 3. metals-and-non-metals ✓ 4. carbon-and-its-compounds ✓ 5. life-processes ✓ 6. control-and-coordination ✓ 7. how-do-organisms-reproduce ✓ 8. heredity ✓
9. light-reflection-and-refraction ✓ 10. the-human-eye-and-the-colourful-world ✓ 11. electricity ✓ 12. magnetic-effects-of-electric-current ✓ 13. our-environment ✓
トピック：carbon-and-its→matter、life-processes・control-and-coordination・our-environment→living-things、human-eye→waves-and-light、light-reflection は energy の out
IN / Science / Class 9（CBSE の Unit：Matter – Its Nature and Behaviour／Organization in the Living World／Motion, Force and Work／Food; Food Production。standard_text は CBSE 2025-26 の原文。separating the components of a mixture と commercial unit of energy（kWh）は CBSE が除外）— 単元の定義は `tools/in_sci9.py`（UNITS(9) ＝ in_sci9a 化学 Ch 1–4 ＋ in_sci9b 生物 Ch 5・6・12 ＋ in_sci9c 物理 Ch 7–11）。gen_in_science_c9_* は build を呼ぶだけ。
in_sci9 は TRIM = True：build が 3 有効数字の末尾の 0 を消し（60.0 → 60、0.500 → 0.5）、4 けた以上の整数にカンマを付ける（「in 1665」のような年は除く）。in_sci9b.odd_one(groups, q, qn) は「Which of these is a pulse?」「… is not …?」の問題。g は 9.8（PE・power は問題文に「Take g = 10 m/s²」）、π は 22/7
1. matter-in-our-surroundings ✓ 2. is-matter-around-us-pure ✓ 3. atoms-and-molecules ✓ 4. structure-of-the-atom ✓ 5. the-fundamental-unit-of-life ✓ 6. tissues ✓ 7. motion ✓ 8. force-and-laws-of-motion ✓ 9. gravitation ✓ 10. work-and-energy ✓ 11. sound ✓ 12. improvement-in-food-resources ✓
トピック：^gravitation$→forces-and-motion、unit-of-life・^tissues$・food-resources→living-things（earths-systems の out に food-resources、living-things の out に structure-of-the-atom）
IN / Science / Class 6–8（NCERT Curiosity。1 単元 = 1 章。CBSE の Unit はないので domain は The Nature of Science／The World of the Living／Materials／Physical Phenomena／Earth and Space）— 単元の定義は `tools/in_sciN.py`（BOOK = "Curiosity"、STD_URL は NCERT の教科書ページ（Class 6 は textbook.php?fecu1=0-12）、TRIM = True）＝ in_sciNa ＋ in_sciNb。
in_sci.build は mod.BOOK があると standard_code を「Class 6, Curiosity Chapter 4: Exploring Magnets」、seo_title を「(NCERT Curiosity Chapter 4)」にし、standard_url に mod.STD_URL を使う。
in_sci6a に Class 6–8 用の odd_one（説明は「X: ラベル.」の形で動詞の数の一致を避ける。non-・in…able・opaque などの否定のラベルでは「not」の問題を作らない）と nq（単位の前に空白、100 万以上・0.001 未満・負の誤答を落とす）
IN / Science / Class 6: 1. the-wonderful-world-of-science ✓ 2. diversity-in-the-living-world ✓ 3. mindful-eating-a-path-to-healthy-body ✓ 4. exploring-magnets ✓ 5. measurement-of-length-and-motion ✓ 6. materials-around-us ✓
7. temperature-and-its-measurement ✓ 8. a-journey-through-states-of-water ✓ 9. methods-of-separation-in-everyday-life ✓ 10. living-creatures-exploring-their-characteristics ✓ 11. natures-treasures ✓ 12. beyond-earth ✓
トピック：separation→matter、^temperature-and→energy、living-world・living-creatures→living-things、beyond-earth→earth-and-space（earths-systems の out）、natures-treasures→earths-systems、world-of-science→working-scientifically
IN / Science / Class 7（STD_URL は textbook.php?gecu1=0-12）: 1. the-ever-evolving-world-of-science ✓ 2. exploring-substances-acidic-basic-and-neutral ✓ 3. electricity-circuits-and-their-components ✓ 4. the-world-of-metals-and-non-metals ✓
5. changes-around-us-physical-and-chemical ✓ 6. adolescence-a-stage-of-growth-and-change ✓ 7. heat-transfer-in-nature ✓ 8. measurement-of-time-and-motion ✓ 9. life-processes-in-animals ✓ 10. life-processes-in-plants ✓ 11. light-shadows-and-reflections ✓ 12. earth-moon-and-the-sun ✓
LEAKS の " nan" は空白つきの部分一致なので nanosecond も止まる。トピック：acidic-basic・physical-and-chemical→matter、adolescence→living-things
IN / Science / Class 8（STD_URL は textbook.php?hecu1=0-13）: 1. exploring-the-investigative-world-of-science ✓ 2. the-invisible-living-world-beyond-our-naked-eye ✓ 3. health-the-ultimate-treasure ✓ 4. electricity-magnetic-and-heating-effects ✓
5. exploring-forces ✓ 6. pressure-winds-storms-and-cyclones ✓ 7. particulate-nature-of-matter ✓ 8. nature-of-matter-elements-compounds-and-mixtures ✓ 9. the-amazing-world-of-solutes-solvents-and-solutions ✓ 10. light-mirrors-and-lenses ✓
11. keeping-time-with-the-skies ✓ 12. how-nature-works-in-harmony ✓ 13. our-home-earth-a-unique-life-sustaining-planet ✓
in_sci.build の TRIM のカンマは年に付けない（「(1986)」「the year 2026」「of 1987」「since 1973」の形と「2023 was」。単位が続く数にはカンマ）。年を文頭に書かない（「The year 2024 is…」と書く）
set を回して選択肢を作らない（文字列の set は実行ごとに順番が変わる。sorted() する）。生成スクリプトを 2 回動かして md5 が同じか確かめる
トピック：^health-the・nature-works→living-things、time-with-the-skies→earth-and-space（out に our-home-earth）、cyclone→earths-systems
IN / Science / Class 3–5（NCERT Our Wondrous World（EVS: The World Around Us、2025 年の新しい教科書）。subject は science のまま、seo_title は「Class 3 EVS Worksheet」（in_sciN.SUBJ = "EVS"）、BOOK = "Our Wondrous World"、STD_URL は NCERT の教科書ページ）— 単元は `tools/in_sciN.py` ＝ in_sciNa ＋ in_sciNb。domain は教科書のテーマ（Our Families and Communities／Life Around Us／Water／Food and Health／Things Around Us など）。とても短い文、₹ のお金の問題は in_sci3a.c_money
Class 1–2 は NCERT に理科・EVS の教科がない（Joyful Mathematics・英語・ヒンディー語などだけ）ので作らない
IN / Science / Class 3: 1. family-and-friends ✓ 2. going-to-the-mela ✓ 3. celebrating-festivals ✓ 4. getting-to-know-plants ✓ 5. plants-and-animals-live-together ✓ 6. living-in-harmony ✓ 7. water-a-precious-gift ✓ 8. food-we-eat ✓ 9. staying-healthy-and-happy ✓ 10. this-world-of-things ✓ 11. making-things ✓ 12. taking-charge-of-waste ✓
トピック：world-of-things・making-things→matter、food-we-eat・living-in-harmony→living-things、charge-of-waste→earths-systems（family・mela・festivals はトピックなし）
IN / Science / Class 4: 1. living-together ✓ 2. exploring-our-neighbourhood ✓ 3. nature-trail ✓ 4. growing-up-with-nature ✓ 5. food-for-health ✓ 6. happy-and-healthy-living ✓ 7. how-things-work ✓ 8. how-things-are-made ✓ 9. different-lands-different-lives ✓ 10. our-sky ✓
in_sci4.NOCOMMA = {"1098"}：TRIM のカンマを付けない数（電話番号）。鳥の「feet」も LEAK で止まるので toes・claws と書く
トピック：nature-trail・food-for-health・healthy-living→living-things、things-are-made→matter、how-things-work→forces-and-motion、different-lands→earths-systems
IN / Science / Class 5: 1. water-the-essence-of-life ✓ 2. journey-of-a-river ✓ 3. the-mystery-of-food ✓ 4. our-school-a-happy-place ✓ 5. our-vibrant-country ✓ 6. some-unique-places ✓ 7. energy-how-things-work ✓ 8. clothes-how-things-are-made ✓ 9. rhythms-of-nature ✓ 10. earth-our-shared-home ✓
domain は教科書のテーマ（Life Around Us／Health and Well-being／Incredible India／Things Around Us／Our Amazing Planet）。日の出・日の入りの問題は現実の時刻に合わせる（6 月の Delhi は 5 時台〜7 時台）
トピック：mystery-of-food・our-shared-home→living-things、journey-of-a-river→earths-systems、rhythms-of-nature→earth-and-space、^how-things-work$→forces-and-motion（Class 5 の energy-how-things-work は energy だけ）
IN / Science / Class 11–12（CBSE Senior Secondary 2025-26 / NCERT Physics・Chemistry・Biology。1 単元 = 1 章。1 つの学年ページに 3 科目が並ぶ（domain が Physics／Chemistry／Biology）。sort は学年の中で Physics → Chemistry → Biology の通し番号）— 単元は `tools/in_s11p.py`・`in_s11c.py`・`in_s11b.py`（Class 12 は in_s12*）の UNITS()、まとめは `tools/in_sci11.py`（TRIM・G98 = True）。gen_in_science_c11_* は build を呼ぶだけ（seed は 720000 + 100 × 学年 + sort）。
共通部品は `tools/in_srs.py`：SU(subj, sort, slug, chapter, …, chname=)（standard_code「Class 11 Physics, Chapter 5: Laws of Motion」、seo「… Class 11 Physics Worksheet with Answers (NCERT Chapter 5)」、standard_url は CBSE の Physics／Chemistry／Biology_SrSec_2025-26.pdf）、A(al_phys などの maker, kinds)（UK A level の問題関数を使う）、N（数の答え）、B（bank）。化学・生物は T() で UK の単位を NCERT 式に（dm³→L、cm³→mL、mol dm⁻³→mol L⁻¹、Mr→molar mass）。g = 9.8（G98 で 9.81 も直す）。
自前の数値 maker は ri()・rf() で数を広く散らして pool を確保する（固定のタプルだと pool が足りない）。生物は OD(groups)（項目はグループ間で重複不可。FAM（_fam）で同じ系統のグループから誤答を選ぶ）と pairs と bank が中心。bank の使用数は行数 − 3 まで
Class 11: Physics 1. units-and-measurements ✓ 2. motion-in-a-straight-line ✓ 3. motion-in-a-plane ✓ 4. laws-of-motion ✓ 5. work-energy-and-power ✓ 6. system-of-particles-and-rotational-motion ✓ 7. gravitation ✓ 8. mechanical-properties-of-solids ✓ 9. mechanical-properties-of-fluids ✓ 10. thermal-properties-of-matter ✓ 11. thermodynamics ✓ 12. kinetic-theory ✓ 13. oscillations ✓ 14. waves ✓
／Chemistry 15. some-basic-concepts-of-chemistry ✓ 16. structure-of-atom ✓ 17. classification-of-elements-and-periodicity-in-properties ✓ 18. chemical-bonding-and-molecular-structure ✓ 19. chemical-thermodynamics（NCERT Ch 5 Thermodynamics）✓ 20. equilibrium ✓ 21. redox-reactions ✓ 22. organic-chemistry-some-basic-principles-and-techniques ✓ 23. hydrocarbons ✓
／Biology 24. the-living-world ✓ 25. biological-classification ✓ 26. plant-kingdom ✓ 27. animal-kingdom ✓ 28. morphology-of-flowering-plants ✓ 29. anatomy-of-flowering-plants ✓ 30. structural-organisation-in-animals ✓ 31. cell-the-unit-of-life ✓ 32. biomolecules ✓ 33. cell-cycle-and-cell-division ✓ 34. photosynthesis-in-higher-plants ✓ 35. respiration-in-plants ✓ 36. plant-growth-and-development ✓ 37. breathing-and-exchange-of-gases ✓ 38. body-fluids-and-circulation ✓ 39. excretory-products-and-their-elimination ✓ 40. locomotion-and-movement ✓ 41. neural-control-and-coordination ✓ 42. chemical-coordination-and-integration ✓
トピック：chemical-thermodynamics・kinetic-theory→matter と energy、properties-of-solids・fluids→matter と forces-and-motion、rotational-motion→forces-and-motion、oscillations→forces-and-motion と waves-and-light、breathing・excretory・locomotion・^biomolecules$→living-things（matter の out に anatomy（atom に当たる））
Class 12（単元は `tools/in_s12p.py`・`in_s12c.py`・`in_s12b.py`、まとめは `tools/in_sci12.py`。sort は Physics 1–14 → Chemistry 15–24 → Biology 25–37）: Physics 1. electric-charges-and-fields ✓ 2. electrostatic-potential-and-capacitance ✓ 3. current-electricity ✓ 4. moving-charges-and-magnetism ✓ 5. magnetism-and-matter ✓ 6. electromagnetic-induction ✓ 7. alternating-current ✓ 8. electromagnetic-waves ✓ 9. ray-optics-and-optical-instruments ✓ 10. wave-optics ✓ 11. dual-nature-of-radiation-and-matter ✓ 12. atoms ✓ 13. nuclei ✓ 14. semiconductor-electronics ✓
／Chemistry 15. solutions ✓ 16. electrochemistry ✓ 17. chemical-kinetics ✓ 18. the-d-and-f-block-elements ✓ 19. coordination-compounds ✓ 20. haloalkanes-and-haloarenes ✓ 21. alcohols-phenols-and-ethers ✓ 22. aldehydes-ketones-and-carboxylic-acids ✓ 23. amines ✓ 24. biomolecules ✓
／Biology 25. sexual-reproduction-in-flowering-plants ✓ 26. human-reproduction ✓ 27. reproductive-health ✓ 28. principles-of-inheritance-and-variation ✓ 29. molecular-basis-of-inheritance ✓ 30. evolution ✓ 31. human-health-and-disease ✓ 32. microbes-in-human-welfare ✓ 33. biotechnology-principles-and-processes ✓ 34. biotechnology-and-its-applications ✓ 35. organisms-and-populations ✓ 36. ecosystem ✓ 37. biodiversity-and-conservation ✓
OD のグループ名は答えが二通りに読めないようにする（「a hormone of the menstrual cycle」と「a hormone made by the placenta」は両方に oestrogen が入るので不可。作る場所で分ける）。class-12 の biomolecules（化学）は slug が Class 11 生物と同じなので living-things に入る
トピック：haloalkanes・alcohols-phenols・aldehydes-ketones・^amines$・coordination・d-and-f-block・electrochemistry・^nuclei$・semiconductor→matter、alternating-current・electrostatic-potential→energy、electric-charges→forces-and-motion、ray-optics→waves-and-light、biotechnology・human-health・microbes-in-human・reproductive-health→living-things
IN / Science は Class 3〜12 まで完了（Class 1–2 は NCERT に EVS がない）。次は他の国の理科

SG / Science（MOE Primary Science Syllabus 2023。Primary 3〜6）— country `sg`、subject `science`、grade `primary-N`、A4。生成スクリプトは `gen_sg_science_pN_*`（seed は 63000 + 100 × N + sort）、共通部品は `tools/sg_sci.py`
（sci_common・uk_sci の上に SG の名前（sg_sec）、make_sg(level, slug, sort, theme, topic, …)：standard_code「Primary 6: Energy forms and uses (Photosynthesis)」、domain はテーマ（Diversity／Cycles／Systems／Interactions／Energy）、standard_url は MOE の syllabus ページ。
LEAKS（米国式の綴り、Year N・GCSE・£・badger など英国だけの語）と英国の名前が残ると止まる。UK の問題関数は adopt_uk(モジュール, U) と sgm(maker) で SG の名前にして使える）。
イギリス式の綴り。場面はシンガポール（Hydrilla、balsam、pandan、hibiscus、rain tree、hawker、MRT）。名前だけ違う問題を作らない（once のキーに名前・植物名を入れない）。PSLE 形式の実験（表・変数・公平な実験）を最後のセットに
P3: 1. living-and-non-living-things ✓ 2. classifying-living-things ✓ 3. diversity-of-materials ✓ 4. life-cycles-of-animals ✓ 5. life-cycles-of-plants ✓ 6. magnets ✓
P4: 1. plant-parts-and-functions ✓ 2. digestive-system ✓ 3. matter ✓ 4. light-and-shadows ✓ 5. heat-and-temperature ✓ 6. heat-conductors-and-insulators ✓
P5: 1. reproduction-in-plants ✓ 2. reproduction-in-humans ✓ 3. water-and-changes-of-state ✓ 4. the-water-cycle ✓ 5. cells ✓ 6. plant-transport-system ✓ 7. respiratory-and-circulatory-systems ✓ 8. electrical-circuits ✓ 9. conductors-and-circuit-diagrams ✓
P3〜P5 の生成スクリプトは UK の問題関数を `use(U, "gen_uk_science_…", rep=[(古い, 新しい)], drop=[語])` で使う（S.g_x は SG の名前・イギリス式、S.B1 は手書きの問題（bank）のリスト。drop で SG のシラバスにない語（vacuole・mitochondria・particle・voltage など）を含む問題を落とす）。sgm は SG_REP で英国の物（jumper・oak tree・woodland・robin など）を直し、a/an を直す。数の問題を作る関数が多いときは `upto(f, n)` で単元全体の数を制限する。回路図は uk_sci_pics.circuit・parallel、温度計の図は gen_sg_science_p4_heat_and_temperature.thermo。トピック：light-and-shadows は earth-and-space の out
P6: 1. photosynthesis ✓ 2. energy-forms-and-conversion ✓ 3. forces-and-their-effects ✓ 4. frictional-force ✓ 5. gravitational-and-elastic-spring-force ✓ 6. food-chains-and-food-webs ✓ 7. habitats-populations-and-communities ✓ 8. adaptations ✓ 9. mans-impact-on-the-environment ✓
P6 の食物網は `tools/sg_webs.py`（mangrove swamp・school garden・pond・coral reef。add() で実行時だけ sci_foodweb に足す。sci_foodweb.WEBS を US の単元が使うので sci_foodweb.py は書き換えない）。ばねばかりの図は gen_sg_science_p6_forces_and_their_effects の balance_svg と g_read（目盛り 10 N／50 N に合わせて物を選ぶ）。
upto(f, n) は重複で捨てられた問題も数えるので、他国の問題関数を upto で使うときはセットの数に余裕をもたせる。トピック：^adaptations$→living-things、mans-impact→living-things と earths-systems
SG / Science / Lower Secondary Science（MOE 2021 G2/G3 Lower Secondary Science Syllabus。Sec 1–2 の 2 年分を学校の一般的な配分で分ける）— grade `secondary-1`（sort 7）・`secondary-2`（sort 8）。生成スクリプトは `gen_sg_science_s1_*`・`s2_*`（seed は 64000 + 100 × 学年 + sort）、共通部品は `tools/sg_lss.py`
（make_lss(level, slug, sort, theme, topic, …)：standard_code「Secondary 2: Electrical Systems」、domain は The Scientific Endeavour／Diversity／Models／Interactions／Systems、standard_url は MOE の LSS シラバス PDF。luse(U, モジュール) は sg_sci.use に SEC_REP（pupils→students、oesophagus→gullet (oesophagus)）と SEC_DROP（W = mg の g、V = IR、moments、ions、音速など LSS にない内容）を足したもの。
sgnum() が数を SG 式に直す（4 桁はそのまま、5 桁以上はノーブレークスペース）。seo(level, 名前) で seo_title。PSLE・pupil は使わない（make_lss が止める））。
LSS にない内容：W = mg の計算、V = IR、モーメントの式、イオン、音（Topic 9 は力とエネルギーだけ）。UK KS3・SG P5/P6 の問題関数を再利用（P5・P6 のモジュールは import して U・R・P を入れ替える。P5 の語は sec() で xylem・phloem・stomata に）。
sg_sci.sgm の a/an の修正は「0.5 A and」を「An」にしないように直した。gen_uk_science_y7_cells の「They where」を直した
Sec 1: 1. the-scientific-endeavour ✓ 2. physical-properties-of-matter ✓ 3. elements-compounds-and-mixtures ✓ 4. separation-techniques ✓ 5. ray-model-of-light ✓ 6. cells ✓ 7. particulate-nature-of-matter ✓ 8. atoms-and-molecules ✓
Sec 2: 1. forces-and-pressure ✓ 2. energy-and-work-done ✓ 3. heat-transfer-and-its-effects ✓ 4. chemical-changes ✓ 5. acids-and-alkalis ✓ 6. interactions-within-ecosystems ✓ 7. electrical-systems ✓ 8. human-digestive-system ✓ 9. transport-systems-in-living-things ✓ 10. human-sexual-reproductive-system ✓
core.php：grade_standard() で sg の science は secondary なら「MOE Lower Secondary Science Syllabus (2021)」。トピック：scientific-endeavour→working-scientifically、reproductive-system→living-things
SG / Science / Upper Secondary（Singapore-Cambridge O-Level Physics 6091・Chemistry 6092・Biology 6093、Sec 3–4。1 つの学年ページに 3 科目が並ぶ（domain が Physics／Chemistry／Biology））— grade `secondary-3`（sort 9）・`secondary-4`（sort 10）。生成スクリプトは `gen_sg_science_s3_*`・`s4_*`、seed は seed_of(学年, 科目, sort) = 65000 + 100 × 学年 + 20 × 科目の番号 + sort。
共通部品は `tools/sg_ol.py`：OL(seed) → (U, R, P, src)。src(モジュール, 関数名, rep=, drop=) で UK・US・SG の問題関数を SG の名前・イギリス式にして使う（読み込んだ gen_・al_ モジュールの U・R・P をこの単元に向ける。OL_DROP で UK・US・Year・A level・£・feet・miles を落とす）。
make_ol(学年, 科目, slug, sort, topic, 原文の要約, title, short, meta, kb, ks, think, ex, mist, faq, sets)：standard_code「O-Level Physics (6091): Kinematics」、seo「Secondary 3 Physics: Kinematics Worksheets (O-Level 6091 with Answers)」。数は sgnum（5 桁以上はノーブレークスペース）、a/an は _AN2（1 文字のラベル A・B の前は直さない）。英国の名前・PSLE・GCSE・Year N・学生の意味の pupil（目の pupil はよい）・Physics の 9.8 が残ると止まる。
部品：nq（3 有効数字、末尾の 0 を消す）・ex（問題のデータは丸めずに書く）・rows(R, 表, 順, 逆)・pool(R, 手書きの行)・graph（折れ線、data-pf='lg'）・keep。O-Level の g は 10 N/kg。答えは 3 有効数字（角度は小数第 1 位）
sg_sci.sgm の a/an の直しは and・is・in・or・of・at・as・are・if の前の A を An にしない（A and B など）。遺伝子型の選択肢は大文字小文字だけ違うと重複扱い（item が小文字で比べる）なので「Tt (heterozygous)」の形にする
Sec 3 — Physics: 1. physical-quantities-units-and-measurement ✓ 2. kinematics ✓ 3. dynamics ✓ 4. turning-effect-of-forces ✓ 5. pressure ✓ 6. energy ✓ 7. kinetic-particle-model-of-matter ✓ 8. thermal-processes ✓ 9. thermal-properties-of-matter ✓ 10. general-wave-properties ✓ 11. electromagnetic-spectrum ✓ 12. light ✓
／Chemistry: 13. experimental-chemistry ✓ 14. particulate-nature-of-matter ✓ 15. chemical-bonding-and-structure ✓ 16. chemical-calculations ✓ 17. acid-base-chemistry ✓ 18. qualitative-analysis ✓
／Biology: 19. cell-structure-and-organisation ✓ 20. movement-of-substances ✓ 21. biological-molecules ✓ 22. nutrition-in-humans ✓ 23. nutrition-and-transport-in-flowering-plants ✓ 24. transport-in-humans ✓ 25. respiration-in-humans ✓
Sec 4 — Physics: 1. static-electricity ✓ 2. current-of-electricity ✓ 3. dc-circuits ✓ 4. practical-electricity ✓ 5. magnetism ✓ 6. electromagnetism ✓ 7. electromagnetic-induction ✓ 8. radioactivity ✓
／Chemistry: 9. redox-chemistry ✓ 10. patterns-in-the-periodic-table ✓ 11. chemical-energetics ✓ 12. rate-of-reactions ✓ 13. organic-chemistry ✓ 14. maintaining-air-quality ✓
／Biology: 15. excretion-in-humans ✓ 16. homeostasis-coordination-and-response ✓ 17. infectious-diseases ✓ 18. molecular-genetics ✓ 19. reproduction ✓ 20. inheritance ✓ 21. organisms-and-their-environment ✓
新しい 6091 にない内容（ノギス・マイクロメーターの読み、気体の法則、凹レンズ、CRO、温度の単元）は出さない。Sound は General Wave Properties に入れ、Radioactivity を足した
トピック：^kinematics$・^dynamics$・turning-effect→forces-and-motion、electromagnetic-spectrum→waves-and-light、physical-quantities→working-scientifically、^radioactivity$・chemical-calculations・qualitative-analysis など→matter、air-quality→earths-systems、movement-of-substances・transport-in-humans・excretion-in-humans・infectious-diseases→living-things
SG / Science は Primary 3〜Secondary 4（O-Level Physics・Chemistry・Biology）まで完了。次は他の国の理科

AU / Science（Australian Curriculum v9.0 Science。Foundation〜Year 10）— country `au`、subject `science`、grade `foundation`・`year-N`、A4。生成スクリプトは `gen_au_science_f_*`・`gen_au_science_yN_*`（seed は seed_of(学年, sort) = 66000 + 100 × 学年 + sort）。
standard_code は v9 のコード（AC9S5U01、inquiry は「AC9S8I01, …」）、domain は strand（Biological sciences／Chemical sciences／Earth and space sciences／Physical sciences／Science inquiry）、standard_url は v9 の Science ページ。core.php の subject_standard() に 'au/science'。
共通部品は `tools/au_sci.py`：AU(seed) → (U, R, P, src)。src(他国の生成スクリプト, "g_x", rep=, drop=) で UK・US・SG の問題関数を AU の名前・オーストラリア英語にして使う（aum：ukm → AU の名前 → AU_REP（esky・footpath・icy pole・slater・column graph・jumper・gum tree・lift・windscreen・gumboot・bicarb soda・neuron・tonnes・jewellery・stabilise・autumn・cupboard など）→ a/an。名前と数字を除いた文＋正解で単元の中の重複を落とす）。
src.B(モジュール, "B1") はバンク全体を 1 つの maker にする（U.sets の中にリストを書くと黙って無視されるため）。src.mod(名前) は他の生成スクリプト（AU の Year 6〜9 の working scientifically など）を R・U・P をそろえて import する。limit(f, n) は単元全体の上限、keep(f, pred) で絞る。
make_au(year, slug, sort, code, strand, std_text, title, short, meta, key_big, key_sub, think, ex, mist, faq, sets, allow=, pic=)：LEAKS（米国・英国・シンガポールの語、北半球の季節 SEASON_RE、£・$ 以外の通貨など）が残ると止まる（意図した語は allow=）。Foundation〜Year 2 は pic=（K.row の絵）で kid_lesson、think は (一文, [要点3つ])、title ≤ 40・key_big ≤ 40・key_sub ≤ 90。
大きな数は "{:,}".format(n) で書く（sgnum が 5 桁以上をノーブレークスペース区切りにする。先に空白で区切ると壊れる）。食物網は `tools/au_webs.py`（bush・billabong・reef・outback。au_webs.add() のあと SG Primary 6 の食物網の問題関数で WEBS = au_webs.NAMES）。
他国の問題関数のプールは scratchpad の inv.py で数えてから配分を書く（足りないと U.sets が「not enough questions」で止まる。どのセットかは dbg.py）。AU_REP の動物の置き換え（badger→wombat、hedgehog→echidna、squirrel→possum）で食べ物や絵が合わなくなる問題は drop で落とす。季節は南半球（12〜2 月が夏）、北部は wet/dry season。g = 9.8 N/kg（UK の 10 N/kg の問題は Year 8 の PE だけ）
Foundation: 1. features-of-plants-and-animals ✓ 2. grouping-living-things ✓ 3. how-objects-move ✓ 4. materials-and-their-properties ✓
Year 1: 1. needs-of-living-things ✓ 2. habitats ✓ 3. daily-and-seasonal-changes ✓ 4. pushes-and-pulls ✓
Year 2: 1. earth-and-the-sky ✓ 2. sound ✓ 3. changing-the-shape-of-materials ✓ 4. breaking-and-building-with-materials ✓
Year 3: 1. living-and-non-living-things ✓ 2. life-cycles ✓ 3. soils-rocks-and-minerals ✓ 4. heat-sources-and-heat-transfer ✓ 5. solids-liquids-and-changes-of-state ✓ 6. working-scientifically ✓
Year 4: 1. producers-consumers-and-decomposers ✓ 2. food-chains-and-food-webs ✓ 3. the-water-cycle ✓ 4. friction-and-contact-forces ✓ 5. gravity-and-magnetism ✓ 6. natural-and-made-materials ✓ 7. working-scientifically ✓
Year 5: 1. structural-adaptations ✓ 2. behavioural-adaptations ✓ 3. weathering-erosion-and-deposition ✓ 4. slow-and-rapid-changes-to-earths-surface ✓ 5. light-sources-and-how-light-travels ✓ 6. shadows-reflection-and-refraction ✓ 7. solids-liquids-and-gases ✓ 8. working-scientifically ✓
Year 6: 1. physical-conditions-of-habitats ✓ 2. the-solar-system ✓ 3. day-night-and-seasons ✓ 4. electric-circuits ✓ 5. conductors-insulators-and-energy ✓ 6. reversible-and-irreversible-changes ✓ 7. working-scientifically ✓
Year 7: 1. classification-and-dichotomous-keys ✓ 2. food-webs-and-ecosystems ✓ 3. earth-sun-and-moon ✓ 4. balanced-and-unbalanced-forces ✓ 5. particle-theory ✓ 6. mixtures-and-separation ✓ 7. working-scientifically ✓
Year 8: 1. cells ✓ 2. body-systems ✓ 3. plate-tectonics ✓ 4. rock-cycle ✓ 5. energy-transfers-and-transformations ✓ 6. elements-compounds-and-mixtures ✓ 7. physical-and-chemical-change ✓ 8. working-scientifically ✓
Year 9: 1. nervous-and-endocrine-systems ✓ 2. reproduction ✓ 3. the-carbon-cycle ✓ 4. waves-sound-and-light ✓ 5. conservation-of-energy-and-efficiency ✓ 6. atomic-structure-and-radioactivity ✓ 7. chemical-reactions-and-equations ✓ 8. working-scientifically ✓
Year 10: 1. genetics-and-inheritance ✓ 2. evolution-and-natural-selection ✓ 3. the-big-bang-and-the-universe ✓ 4. global-systems-and-climate-change ✓ 5. newtons-laws-of-motion ✓ 6. the-periodic-table ✓ 7. reaction-types-and-rates ✓ 8. working-scientifically ✓
トピック：nervous-and-endocrine・adaptation→living-things、^the-carbon-cycle$・seasonal-changes→earths-systems（out に earth-sun・earth-and-the-sky）、objects-move→forces-and-motion、energy の out に waves-sound-and-light
AU / Science / Year 11–12（Australian Curriculum: Senior Secondary Biology・Chemistry・Physics・Earth and Environmental Science。Year 11 は Unit 1–2、Year 12 は Unit 3–4。1 つの学年ページに 4 科目が並ぶ（domain が科目名））— 州の科目（QCE・WACE・HSC・VCE）とは別に、全国共通の ACARA の senior 版に合わせた。
standard_code は「Physics Unit 2: Waves」（科目＋Unit 番号＋sub-unit）、standard_text の末尾に「(Senior Secondary Physics, Unit 2: Linear motion and waves)」、standard_url は australiancurriculum.edu.au/senior-secondary-curriculum/science/{科目}、seo_title は「Year 12 Physics: Special Relativity Worksheets (Australian Curriculum)」。
生成スクリプトは `gen_au_science_y11_*`・`y12_*`（build を呼ぶだけ）、単元は `tools/au_sr11b.py`・`au_sr11c.py`・`au_sr11p.py`・`au_sr11e.py`（Year 12 は au_sr12*）の UNITS()、まとめは `au_sr11.py`・`au_sr12.py`。seed は au_sci.seed_of(学年, sort)。sort は学年の中で Biology → Chemistry → Physics → EES の通し番号。
共通部品は `tools/au_sr.py`：SR(subject, unit, sort, slug, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, allow=)、sets は lambda X: [...]。
X.ch(モジュール, slug, セット番号, 学年, only=, rep=, drop=) で UK A level（al_bio・al_chem・al_phys、学年 12・13）と IN Class 11–12（in_s11b〜in_s12p）の単元のセットをそのまま 1 つの maker にする（IN の odd-one-out「Which of these is …」は落とす）。X.al(al_* の関数, 種類…)、X.gen(gen_ モジュール, "g_x")、X.pool(行)、X.w(自前の maker)、X.f(factory(R))。
すべて au_sci.aum を通る（AU の名前・綴り・単位、重複は単元で 1 回）。GEN_REP で nonrenewable・hurricane・wildfire を直し、mg/dL・kcal・NCERT・A level などの問題は落とす。Biology と Chemistry だけ cm³→mL、dm⁻³→L⁻¹（mol/L）。g = 9.8。数のカンマは外して sgnum（5 桁以上はノーブレークスペース）。文中の " は curly quotes に。ore grade・Golden Mile のように LEAKS の語を使う単元は allow=("grade", "mile")。
自前の数値問題：相対論（γ・時間の遅れ・ローレンツ収縮・ミューオン・E = mc²・相対論的運動量）、Wien の法則、F = BIL・トルク、鉱石の品位と埋蔵量の年数、地震（マグニチュード・S–P 時間・津波の速さ √(gd)）。
Year 11: Biology 1. biodiversity-and-classification ✓ 2. ecosystem-dynamics ✓ 3. cells-and-membranes ✓ 4. enzymes-photosynthesis-and-respiration ✓ 5. multicellular-organisms ✓／Chemistry 6. atomic-structure-and-the-periodic-table ✓ 7. bonding-and-properties-of-materials ✓ 8. moles-and-chemical-reactions ✓ 9. intermolecular-forces-and-gases ✓ 10. aqueous-solutions-and-acidity ✓ 11. rates-of-reaction ✓
／Physics 12. heating-processes ✓ 13. ionising-radiation-and-nuclear-reactions ✓ 14. electrical-circuits ✓ 15. linear-motion-and-force ✓ 16. waves ✓／EES 17. earth-systems-and-the-geosphere ✓ 18. atmosphere-hydrosphere-and-biosphere ✓ 19. energy-for-earth-processes ✓ 20. atmospheric-and-ocean-circulation ✓ 21. biogeochemical-cycles ✓
Year 12: Biology 1. dna-genes-and-protein-synthesis ✓ 2. cell-division-and-inheritance ✓ 3. mutations-and-biotechnology ✓ 4. evolution-and-population-genetics ✓ 5. homeostasis ✓ 6. infectious-disease-and-immunity ✓／Chemistry 7. chemical-equilibrium ✓ 8. acids-bases-and-ph ✓ 9. oxidation-and-reduction ✓ 10. electrochemical-cells ✓ 11. organic-chemistry ✓ 12. chemical-synthesis-and-analysis ✓
／Physics 13. projectile-and-circular-motion ✓ 14. gravitational-fields-and-orbits ✓ 15. electromagnetism ✓ 16. special-relativity ✓ 17. quantum-theory ✓ 18. the-standard-model ✓／EES 19. mineral-and-energy-resources ✓ 20. water-soil-and-renewable-resources ✓ 21. managing-environmental-impacts ✓ 22. geological-hazards ✓ 23. climate-change-and-weather-hazards ✓
core.php の grade_standard() で Year 11–12 の基準名を「Australian Curriculum: Senior Secondary …」に、unit.php で educationalLevel に Senior secondary。トピックは新しい slug を ^…$ で足した（他の国の割り当ては変えていない）
AU / Science は Foundation〜Year 12 まで完了。次は他の国の理科

CA-ON / Science（The Ontario Curriculum, Grades 1–8: Science and Technology, 2022）— country `ca-on`、subject `science`、grade `grade-N`、Letter。各学年 4 strand（B Life Systems／C Matter and Energy／D Structures and Mechanisms／E Earth and Space Systems。A STEM Skills は単元の中で）。
standard_code は「Grade 4: B2.4, B2.5」、domain は strand 名、standard_text の末尾に「(summary of the Ontario Science and Technology curriculum, 2022, Strand B: Life Systems – Habitats and Communities)」、standard_url は dcp.edu.gov.on.ca の grade-N/strands。seo_title は「Grade 4 Science: Light Worksheets (Ontario Curriculum)」。
単元の定義は `tools/caon_sci1.py`〜`caon_sci8.py` の UNITS()（CU(strand, sort, slug, code, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, pic=)、sets は lambda X）、gen_caon_science_gN_* は caon_sci.build を呼ぶだけ。seed は 67000 + 100 × 学年 + sort。
共通部品は `tools/caon_sci.py`：X.gen(他国の生成スクリプト, "g_x", rep=, drop=, n=)・X.B(バンク)・X.pool(行)・X.rows(表, fwd, back, extra=)・X.f(factory)（自前の数値問題。raw なので数だけ違う問題も別に数える）。
すべて cam() を通る：uk_sci.ukm でイギリス式にしてから CA_REP でカナダ英語（colour・centre・metre・litre・grey・fibre はそのまま、-ize、aluminum、tire、truck、gasoline、flashlight、Mom、candy、cookie、garbage、sidewalk、ladybug、sow bug、spring scale、bar graph、esophagus、soccer ball、thumbtack、mL、a.m.）とカナダの名前に。LEAKS（米国式の綴り、英国・豪州の語と動物、Year N、£・pence、inch・mile・°F、UK・U.S.）と南半球の季節（SEASON_RE）が残る問題は落とす。sound level meter などの計器は meter でよい。名前と数字を除いた問題文＋正解で単元の中の重複を落とす。
Grade 1–2 はページの上を軽く（pic に sci_kids.row か自前の SVG、think は (一文, [要点3つ])、title ≤ 40・key_big ≤ 40・key_sub ≤ 90）。Grade 5 の FORCE_ROWS（構造と力）は Grade 7 form-and-function でも使う。
プールの数は scratchpad の probe.py（モジュール:関数）と cainv.py（単元ごと）で数え、足りないセットは dbg.py で見つける
CA-ON / Science / Grade 1: 1. living-and-non-living-things ✓ 2. needs-of-living-things ✓ 3. the-body-and-senses ✓ 4. energy-in-our-lives ✓ 5. objects-and-materials ✓ 6. everyday-structures ✓ 7. day-night-and-weather ✓ 8. the-four-seasons ✓
CA-ON / Science / Grade 2: 1. animal-life-cycles ✓ 2. animal-features-and-groups ✓ 3. animals-and-people ✓ 4. solids-and-liquids ✓ 5. heating-and-cooling ✓ 6. simple-machines ✓ 7. pushes-pulls-and-movement ✓ 8. air-and-water-in-the-environment ✓ 9. caring-for-air-and-water ✓
CA-ON / Science / Grade 3: 1. plant-parts-and-needs ✓ 2. plant-life-cycles-and-seeds ✓ 3. plants-and-people ✓ 4. forces-and-motion ✓ 5. magnets-and-static-electricity ✓ 6. strong-and-stable-structures ✓ 7. soils ✓ 8. soils-and-the-environment ✓
CA-ON / Science / Grade 4: 1. habitats-and-communities ✓ 2. food-chains-and-food-webs ✓ 3. adaptations-and-human-impact ✓ 4. light ✓ 5. sound ✓ 6. pulleys-and-gears ✓ 7. rocks-and-minerals ✓ 8. weathering-and-erosion ✓
CA-ON / Science / Grade 5: 1. respiratory-and-circulatory-systems ✓ 2. digestive-and-other-organ-systems ✓ 3. healthy-body-systems ✓ 4. properties-of-matter ✓ 5. physical-and-chemical-changes ✓ 6. forces-acting-on-structures ✓ 7. energy-and-resources ✓
CA-ON / Science / Grade 6: 1. classifying-living-things ✓ 2. protecting-biodiversity ✓ 3. static-electricity ✓ 4. electric-circuits ✓ 5. forces-of-flight ✓ 6. flight-in-nature-and-technology ✓ 7. the-solar-system ✓ 8. earth-moon-and-sun ✓ 9. space-exploration ✓
CA-ON / Science / Grade 7: 1. interactions-in-ecosystems ✓ 2. human-impact-and-sustainability ✓ 3. pure-substances-and-mixtures ✓ 4. solutions-and-separating-mixtures ✓ 5. form-and-function ✓ 6. heat-and-temperature ✓ 7. heat-in-the-environment ✓
CA-ON / Science / Grade 8: 1. cells-and-cell-theory ✓ 2. cell-processes-and-organization ✓ 3. fluids-density-and-buoyancy ✓ 4. fluid-pressure-and-technology ✓ 5. systems-and-mechanical-advantage ✓ 6. water-on-earth-and-the-water-cycle ✓ 7. water-quality-and-conservation ✓
トピック：structures の単元（everyday・strong-and-stable・forces-acting-on・form-and-function）→engineering-design（living の out）、flight は energy・waves-and-light の out で forces-and-motion、fluids→matter、simple-machines・systems-and-mechanical-advantage→forces-and-motion、space-exploration→earth-and-space、soils-and-the-environment→earths-systems
CA-ON / Science / Grade 9–12（高校。Grade 9 は SNC1W（2022）、Grade 10 は SNC2D Academic（Grades 9 and 10: Science, 2008）、Grade 11–12 は大学進学コース SBI3U・SCH3U・SPH3U・SBI4U・SCH4U・SPH4U（Grades 11 and 12: Science, 2008）。1 つの学年ページに 3 科目が並ぶ（domain が「Biology (SBI3U)」）。Grade 9–10 は strand ごとに 2 単元、Grade 11–12 は strand ごとに 1 単元）— standard_code は「SBI3U: D3.1, D3.2」、standard_url は SNC1W の strands ページ／science910_2008.pdf／2009science11_12.pdf、seo_title は「Grade 11 Biology (SBI3U): Evolution Worksheets (Ontario)」。core.php の grade_standard() で Grade 9–12 の基準名を切り替え。
単元は `tools/caon_hs9.py`〜`caon_hs12.py` の UNITS()（HU(course, strand, sort, slug, code, std, …, sets)）、gen_caon_science_g9_*〜g12_* は caon_hs.build を呼ぶだけ（seed は caon_sci.seed_of）。共通部品は `tools/caon_hs.py`：caon_sci.X に X.ch(UK A level・IN Class 11–12 の単元, slug, セット番号, year)・X.al を足したもの。HS_REP で -ise・-yse を -ize・-yze に、anticlockwise→counterclockwise、earthed→grounded、9.81→9.8、mol dm⁻³→mol/L（生物・化学は cm³→mL）。HS_DROP で RTP・24 dm³・g = 10 N/kg・インドの鏡とレンズの符号規約（1/v、u = −）・シンガポールの地名を落とす。
鏡とレンズはオンタリオの式（1/f = 1/d₀ + 1/dᵢ、実像が正、M = −dᵢ/d₀）の自前の問題 caon_hs10.optics。気体の体積は STP 22.4 L/mol・SATP 24.8 L/mol（caon_hs11.molar_volume）。宇宙開発（Canadarm・RADARSAT）・気候変動の適応と緩和・酸性雨（カナディアン・シールド、Sudbury）・目は手書きの問題
Grade 9 (SNC1W): 1. ecosystems-and-sustainability ✓ 2. climate-change-and-ecosystems ✓ 3. atoms-and-the-periodic-table ✓ 4. elements-and-compounds ✓ 5. static-and-current-electricity ✓ 6. circuits-ohms-law-and-energy ✓ 7. the-sun-and-the-solar-system ✓ 8. the-universe-and-space-exploration ✓
Grade 10 (SNC2D): 1. cells-and-cell-division ✓ 2. tissues-organs-and-systems ✓ 3. chemical-reactions-and-equations ✓ 4. acids-and-bases ✓ 5. climate-change ✓ 6. climate-change-impacts-and-solutions ✓ 7. light-and-reflection ✓ 8. refraction-and-lenses ✓
Grade 11: SBI3U 1. diversity-of-living-things ✓ 2. evolution ✓ 3. genetic-processes ✓ 4. animals-structure-and-function ✓ 5. plants-anatomy-growth-and-function ✓／SCH3U 6. matter-chemical-trends-and-chemical-bonding ✓ 7. chemical-reactions ✓ 8. quantities-in-chemical-reactions ✓ 9. solutions-and-solubility ✓ 10. gases-and-atmospheric-chemistry ✓／SPH3U 11. kinematics ✓ 12. forces ✓ 13. energy-and-society ✓ 14. waves-and-sound ✓ 15. electricity-and-magnetism ✓
Grade 12: SBI4U 1. biochemistry ✓ 2. metabolic-processes ✓ 3. molecular-genetics ✓ 4. homeostasis ✓ 5. population-dynamics ✓／SCH4U 6. organic-chemistry ✓ 7. structure-and-properties-of-matter ✓ 8. energy-changes-and-rates-of-reaction ✓ 9. chemical-systems-and-equilibrium ✓ 10. electrochemistry ✓／SPH4U 11. dynamics ✓ 12. energy-and-momentum ✓ 13. gravitational-electric-and-magnetic-fields ✓ 14. the-wave-nature-of-light ✓ 15. revolutions-in-modern-physics ✓
トピック：新しい slug を ^…$ で足した（elements-and-compounds・gases-and-atmospheric-chemistry→matter、tissues-organs-and-systems・biochemistry・metabolic-processes→living-things、refraction-and-lenses・revolutions-in-modern-physics→waves-and-light、light の 2 単元は energy の out）
CA-ON / Science は Grade 1〜12 まで完了。次は BC の理科（K〜Grade 10）か、他の国の理科。Grade 11–12 の college・workplace コース（SBI3C・SCH4C など）・SES4U・SNC2P は必要なら後で

CA-BC / Science（BC's Curriculum: Science K–10 と Grade 11–12 の科目）— country `ca-bc`、subject `science`、grade `kindergarten`・`grade-N`、Letter。K–10 は Big Idea ごとに 1〜2 単元、domain は Biology／Chemistry／Physics／Earth and Space Science。Grade 11 のページに Chemistry 11・Life Sciences 11・Physics 11・Earth Sciences 11、Grade 12 のページに Anatomy and Physiology 12・Chemistry 12・Physics 12・Geology 12（domain が科目名）。
standard_code は「Grade 4: Biology」（科目は科目名）、standard_url は curriculum.gov.bc.ca/curriculum/science/{K|N}/core と /11/chemistry など。seo_title は「Grade 4 Science: Biomes Worksheets (BC Curriculum)」「Physics 12: Special Relativity Worksheets (BC Curriculum)」。core.php の subject_standard()・grade_standard() に ca-bc。
単元は `tools/cabc_s0.py`（K–2）・`cabc_s3.py`（3–5）・`cabc_s6.py`（6–8）・`cabc_s9.py`（9–10）・`cabc_s11.py`（11–12）の UNITS(grade)、gen_cabc_science_{k|gN}_* は cabc_sci.build を呼ぶだけ。seed は 69000 + 100 × 学年 + sort（K = 0）。
共通部品は `tools/cabc_sci.py`：BU(area, sort, slug, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, pic=, allow=)、sets は lambda X: S(X, [(セット名, "モジュール:slug:セット番号") または (セット名, [(部品, 数)])])。
"caon_sci1〜8・caon_hs9〜12・au_sr11*・au_sr12*:slug:N" はその単元のセットを BC の X で作り直して使う（X.o）、"al_*・in_s*:slug:N" は X.ch。GM(X, "us_science_g8_x", "g_a", "B1", n=20) は他国の生成スクリプトの問題関数を分けて使う。
オンタリオの地名・制度（Toronto・Great Lakes・EQAO・HST・SNC1W・13 % など、BC_DROP）を含む問題は落とす。Ontario の生成スクリプトの UK の語が「Ontario」に置き換わることがあるので GM も _clean で落とす
Kindergarten: features-of-plants-and-animals ✓ familiar-materials ✓ pushes-pulls-and-motion ✓ weather-and-seasons ✓
Grade 1: living-things-and-their-features ✓ materials-and-their-properties ✓ light-and-sound ✓ patterns-in-the-sky-and-land ✓
Grade 2: life-cycles ✓ changing-materials ✓ forces-and-magnets ✓ water-and-the-water-cycle ✓
Grade 3: biodiversity-and-ecosystems ✓ food-chains-and-food-webs ✓ matter-and-particles ✓ thermal-energy ✓ landforms-and-erosion ✓
Grade 4: sensing-and-responding ✓ biomes ✓ phases-of-matter ✓ energy-and-energy-transformations ✓ earth-moon-and-sun ✓
Grade 5: body-systems ✓ solutions-and-solubility ✓ simple-machines-and-power ✓ the-rock-cycle-and-earth-resources ✓
Grade 6: nervous-and-endocrine-systems ✓ excretory-and-reproductive-systems ✓ mixtures-and-separation ✓ newtons-laws-and-gravity ✓ the-solar-system-and-galaxy ✓ space-exploration-and-extreme-environments ✓
Grade 7: evolution-and-natural-selection ✓ elements-and-compounds ✓ electromagnetism-and-electricity ✓ fossils-and-geologic-time ✓ climate-change ✓
Grade 8: cells-and-cell-theory ✓ micro-organisms-and-immunity ✓ kinetic-molecular-and-atomic-theory ✓ light-and-electromagnetic-radiation ✓ plate-tectonics ✓
Grade 9: asexual-and-sexual-reproduction ✓ atoms-and-the-periodic-table ✓ ionic-and-covalent-compounds ✓ electric-circuits-and-ohms-law ✓ matter-cycles-and-earths-spheres ✓ sustainability-and-human-impact ✓
Grade 10: dna-and-inheritance ✓ mutations-and-selection ✓ chemical-reactions ✓ acids-and-bases ✓ nuclear-energy-and-radiation ✓ energy-transformations ✓ the-big-bang-and-the-universe ✓
Grade 11: Chemistry 11（atomic-theory-and-electron-configuration・chemical-bonding-and-molecular-shape・the-mole-and-stoichiometry・solutions-and-concentration・reactions-and-energy-changes・organic-chemistry）✓／Life Sciences 11（classification-of-living-things・cells-and-viruses・evolution・energy-transformations-in-living-things・reproduction-and-life-cycles）✓／Physics 11（kinematics・projectile-motion・forces-and-newtons-laws・energy-work-and-power・dc-circuits・waves-and-sound）✓／Earth Sciences 11（earth-materials-and-the-rock-cycle・plate-tectonics・the-atmosphere-and-weather・energy-budget-and-climate-change・water-and-the-oceans・the-solar-system-and-stars）✓
Grade 12: Anatomy and Physiology 12（biological-molecules-and-enzymes・dna-and-protein-synthesis・genomics-and-biotechnology・homeostasis-and-the-nervous-and-endocrine-systems・digestive-respiratory-and-circulatory-systems・health-disease-and-immunity）✓／Chemistry 12（reaction-kinetics・chemical-equilibrium・solubility-equilibrium・acids-bases-and-ph・oxidation-and-reduction・electrochemical-cells）✓／Physics 12（special-relativity・static-equilibrium-and-torque・circular-motion・gravitation-and-orbits・electric-forces-and-fields・magnetic-forces-and-induction・momentum-and-impulse）✓／Geology 12（minerals-and-rocks・geologic-time-and-dating・earthquakes-and-seismic-waves・plate-tectonics-and-volcanoes・surface-processes）✓
トピック：新しい slug を ^…$ で足した（biomes・sensing-and-responding・health-disease-and-immunity→living-things、simple-machines-and-power・static-equilibrium-and-torque→forces-and-motion、surface-processes→earths-systems、ionic-and-covalent-compounds→matter、space-exploration-and-extreme-environments→earth-and-space。earthquakes-and-seismic-waves は energy・waves の out）
CA-BC / Science は Kindergarten〜Grade 12 まで完了

ZA / Science（CAPS。Grades 4–6 は Natural Sciences and Technology（Intermediate Phase）、7–9 は Natural Sciences（Senior Phase）、10–12 は Physical Sciences と Life Sciences（FET。1 つの学年ページに domain「Physical Sciences: Chemistry」「Physical Sciences: Physics」「Life Sciences」が並ぶ））— country `za`、subject `science`、grade `grade-N`、A4。
standard_code は「Grade 10 Physical Sciences: Electrostatics」形式、Grades 4–9 の domain は strand（Life and Living／Matter and Materials／Energy and Change／Planet Earth and Beyond）、standard_url は WCED の NST ページ・DBE の CAPS SP NS／FET Physical Sciences／FET Life Sciences の PDF、seo_title は「Grade 12 Physical Sciences: Doppler Effect Worksheets (CAPS)」。core.php の subject_standard() と grade_standard() に za/science。
単元は `tools/za_s4.py`（G4–6）・`za_s7.py`（G7–9）・`za_s10.py`・`za_s11.py`・`za_s12.py` の UNITS(grade)、gen_za_science_gN_* は za_sci.build を呼ぶだけ（seed は 71000 + 100 × 学年 + sort）。FET の自前の問題・手書きの pool は `tools/za_fet.py`（U、M（部品に数を割り振る）、share（電荷の分配）・vpm（鉛直投射）・doppler・gold_grade、DOPPLER・FERT・VERT・HUMAN・PLANT・MINE・SKEL・BODY・LAND などの pool、PHYLA・PGROUP の rows 表）。
共通部品は `tools/za_sci.py`（cabc_sci.X の上に南アの名前（za_common）・ZA_REP（イギリス式、learners、mol·dm⁻³、lift、colourless・favour・behaviour、-ise）・LEAKS・ZA_DROP（他国の地名、RTP、g = 10、インドのレンズの符号）、num（コンマの小数・4 536、FET の化学・物理は m·s⁻¹ などの SI）、kb・ks・std の <sub> は外す）。S(X, [(セット名, "mod:slug:N[:year]" か [(部品, 数)])]) で caon_hs・au_sr・cabc_s（year が要る）・al_*・in_s* の単元のセット、GM で他国の生成スクリプトの問題関数。
in_s* の odd-one-out（Which of these is …）は caon_hs.X.ch が落とすので、in_s11b の分類・plant-kingdom・animal-kingdom などはほぼ使えない（自前の pool・rows にする）。pool の行数ぎりぎりまで取ると take が足りなくなる（行数の 8 割まで）。zbct のように 1 プロセスで続けて作ると結果が変わることがあるので、生成スクリプトは 1 つずつ別のプロセスで動かして確かめる
Grade 4: living-and-non-living-things ✓ plants-and-animal-habitats ✓ solids-liquids-and-gases ✓ energy-and-energy-transfer ✓ energy-and-sound ✓ the-earth-the-sun-and-the-moon ✓
Grade 5: animal-skeletons ✓ food-chains-and-life-cycles ✓ metals-and-non-metals ✓ stored-energy-and-electricity ✓ energy-and-movement ✓ the-surface-of-the-earth-and-fossils ✓
Grade 6: photosynthesis-and-nutrition ✓ ecosystems-and-food-webs ✓ mixtures-and-solutions ✓ mixtures-and-water-resources ✓ electric-circuits ✓ the-solar-system ✓
Grade 7: the-biosphere-and-biodiversity ✓ sexual-reproduction-and-variation ✓ properties-of-materials-and-separating-mixtures ✓ acids-bases-and-the-periodic-table ✓ sources-of-energy-and-potential-and-kinetic-energy ✓ heat-transfer-and-insulation ✓ the-sun-the-earth-and-the-moon ✓
Grade 8: photosynthesis-and-respiration ✓ interactions-in-the-environment ✓ micro-organisms ✓ atoms-and-the-particle-model ✓ chemical-reactions ✓ static-electricity-and-electric-circuits ✓ visible-light ✓ the-solar-system-and-beyond ✓
Grade 9: cells-and-systems-in-the-human-body ✓ human-reproduction ✓ circulatory-respiratory-and-digestive-systems ✓ compounds-and-reactions-with-oxygen ✓ acids-bases-and-ph ✓ forces ✓ electric-cells-resistance-and-circuits ✓ the-earth-as-a-system-and-mining ✓ the-birth-life-and-death-of-stars ✓
Grade 10: Chemistry（classification-of-matter・states-of-matter-and-the-kinetic-molecular-theory・the-atom・the-periodic-table・chemical-bonding・physical-and-chemical-change・reactions-in-aqueous-solution・quantitative-aspects-of-chemical-change・the-hydrosphere）✓／Physics（transverse-pulses-and-waves・sound・electromagnetic-radiation・magnetism・electrostatics・electric-circuits・vectors-scalars-and-motion-in-one-dimension・mechanical-energy）✓／Life Sciences（the-chemistry-of-life・cells-the-basic-units-of-life・cell-division-mitosis・plant-and-animal-tissues・support-and-transport-systems-in-plants・support-systems-in-animals・transport-systems-in-mammals・biosphere-to-ecosystems・biodiversity-and-classification・history-of-life-on-earth）✓
Grade 11: Physics（vectors-in-two-dimensions・newtons-laws-and-application-of-newtons-laws・newtons-law-of-universal-gravitation・geometrical-optics・2d-and-3d-wavefronts・electrostatics-coulombs-law-and-electric-fields・electromagnetism・electric-circuits-ohms-law-and-power）✓／Chemistry（atomic-combinations-molecular-structure・intermolecular-forces・ideal-gases-and-thermal-properties・quantitative-aspects-of-chemical-change・energy-and-chemical-change・acids-and-bases・redox-reactions・the-lithosphere-and-mining）✓／Life Sciences（biodiversity-of-micro-organisms・biodiversity-of-plants・biodiversity-of-animals・photosynthesis・animal-nutrition・cellular-respiration・gaseous-exchange・excretion-in-humans・population-ecology・human-impact-on-the-environment）✓
Grade 12（NSC）: Physics（momentum-and-impulse・vertical-projectile-motion・work-energy-and-power・doppler-effect・electric-circuits-and-internal-resistance・electrodynamics・optical-phenomena-and-properties-of-materials）✓／Chemistry（organic-molecules・rate-and-extent-of-reaction・chemical-equilibrium・acids-bases-and-titrations・electrochemical-reactions・the-chemical-industry-fertilisers）✓／Life Sciences（dna-the-code-of-life・meiosis・reproduction-in-vertebrates・human-reproduction・genetics-and-inheritance・nervous-system-and-senses・endocrine-system-and-homeostasis・plant-responses-to-the-environment・evolution・human-evolution）✓
トピック：ZA の slug を ^…$ で足した（topics.php の topic_defs_science。classification-of-matter・electric-cells-resistance-and-circuits・optical-phenomena・electric-circuits-and-internal-resistance は out で直した）
ZA / Science は Grade 4〜12 まで完了。Foundation Phase（Grade R–3）は Life Skills（Beginning Knowledge）の中なので、必要なら後で

PH / Science（DepEd MATATAG Science Curriculum, Grades 3–10。理科は Grade 3 から。四半期ごとに 1 分野）— country `ph`、subject `science`、grade `grade-N`、Letter。アメリカ英語、learners、フィリピンの名前と地名。
domain は Grades 3–6 が Materials／Living Things／Force, Motion, and Energy／Earth and Space、Grades 7–10 が Science of Materials／Life Science／Force, Motion, and Energy／Earth and Space Science（学年ごとの四半期の順は ph_sci.QUARTER）。standard_code は「Grade 8, Quarter 3: Earth and Space Science」、standard_url は DepEd の MATATAG ページ、seo_title は「Grade 9 Science: Typhoons Worksheets (MATATAG)」、meta は set の見出しから自動。core.php の subject_standard() に ph/science。
単元は `tools/ph_s3.py`（G3–6）・`ph_s7.py`（G7–10）の UNITS(grade)、gen_ph_science_gN_* は ph_sci.build を呼ぶだけ（seed は 73000 + 100 × 学年 + sort）。
共通部品は `tools/ph_sci.py`：PU（自前の文）と CP(area, sort, slug, "mod:slug[:year]", std, **上書き)（caon_sci*・caon_hs*・cabc_s*・au_sr*・za_s* の単元の文と 5 セットを使う。a・b・ex・mist・faq・sets・title で上書き）。問題は共通の流れ（イギリス式）を通ってから、build の us() でアメリカ式（color・center・meter・-ize（語尾の決まった語だけ。organism・Polaris は変えない）・gasoline・flashlight・mom・bar graph）と 1,000 区切り（年は除く）に直す。
LEAKS に他国の地名・動物（kangaroo・moose・lion…）・雪とスポーツ・winter・autumn、R と €。最後の検査（_bad_final）はアメリカ式の語を通す。フィリピン独自の内容は `tools/ph_pools.py`（TYPHOON（PAGASA の Signal No. 1〜5）・VOLCANO（Mayon・Taal・Pinatubo、PHIVOLCS）・QUAKE・SEASON_PH（amihan・habagat）・TIDES・PH_ECO・PH_ENDANGERED・SKILLS・WEATHER・CONST）。
caon・cabc の K–2 の単元は think が絵つきなので CP できない（PU で文を書いてセットだけ使う）
Grade 3: science-in-daily-life ✓ materials-and-their-uses ✓ living-and-non-living-things ✓ basic-needs-of-living-things ✓ moving-objects ✓ light-and-sound ✓ the-non-living-environment ✓ patterns-in-weather ✓ the-sun-moon-and-stars ✓
Grade 4: materials-and-their-uses ✓ gathering-scientific-information ✓ body-systems-of-plants-and-animals ✓ plants-animals-and-habitats ✓ animal-life-cycles ✓ food-chains ✓ forces-and-movement ✓ magnets ✓ sound-light-and-heat-energy ✓ soils ✓ characteristics-of-weather ✓ characteristics-of-the-sun ✓
Grade 5: matter-and-its-three-states ✓ scientific-investigation ✓ body-systems-in-animals ✓ microorganisms ✓ life-cycles-of-living-things ✓ specialized-plant-structures ✓ contact-and-non-contact-forces ✓ friction-and-gravity ✓ static-electricity ✓ conductors-insulators-and-simple-circuits ✓ landforms-rocks-and-minerals ✓ weathering-and-erosion ✓ the-water-cycle-and-weather-disturbances ✓ the-solar-system ✓
Grade 6: changes-of-state ✓ physical-and-chemical-changes ✓ mixtures-and-separation-techniques ✓ the-circulatory-system ✓ plant-reproduction ✓ vertebrates-and-invertebrates ✓ food-webs-and-interactions ✓ simple-machines ✓ sound-waves ✓ volcanoes ✓ seasons-and-earths-motions ✓ constellations ✓
Grade 7: the-particle-model-of-matter ✓ solutions-solubility-and-concentration ✓ planning-and-recording-investigations ✓ the-microscope-and-cells ✓ cellular-reproduction ✓ levels-of-biological-organization ✓ energy-transfer-in-ecosystems ✓ balanced-and-unbalanced-forces ✓ distance-displacement-and-velocity ✓ heat-transfer ✓ earthquakes ✓ the-suns-influence-on-earth ✓
Grade 8: organ-systems-working-together ✓ heredity ✓ taxonomic-classification ✓ photosynthesis-respiration-and-cycles ✓ the-atom-and-subatomic-particles ✓ elements-and-compounds ✓ the-periodic-table ✓ continents-and-crustal-features ✓ typhoons ✓ tides ✓ acceleration-and-motion-graphs ✓ work-and-energy ✓ renewable-energy ✓ properties-of-light ✓
Grade 9: newtons-laws-of-motion ✓ electric-circuits ✓ electromagnetic-waves ✓ plate-boundaries-and-continental-drift ✓ structure-of-the-earth-and-geologic-time ✓ the-solar-system-and-space-technologies ✓ dna-and-mutations ✓ biodiversity-and-endangered-species ✓ ecosystems-in-the-philippines ✓ chemical-bonding ✓ properties-of-compounds-and-chemical-formulas ✓
Grade 10: plate-tectonics-and-mountain-formation ✓ global-climate ✓ climate-change-and-sustainability ✓ projectile-motion ✓ momentum-and-collisions ✓ generation-and-distribution-of-electricity ✓ renewable-and-non-renewable-energy ✓ chemical-reactions-and-equations ✓ acids-bases-and-salts ✓ rates-of-reaction ✓ homeostasis ✓ mechanisms-of-evolution ✓ biotechnology ✓ carrying-capacity-and-population-growth ✓
PH / Science / Grade 11–12（DepEd Strengthened Senior High School Curriculum。Grade 11 は全員が学ぶ General Science（Term 1 Physical Science・Term 2 Chemistry and Life Science・Term 3 Earth and Space Science）、Grade 12 のページは STEM の選択科目（Biology 1・2、Chemistry 1、Physics 1・2、Earth and Space Science 1。Grade 11 か 12 で学ぶ）を並べる（domain は Physical Science／Life Science／Earth and Space Science／Biology／Chemistry／Physics））— 単元は `tools/ph_s11.py` の UNITS(11)・UNITS(12)（G・GC は General Science、E・EC は選択科目。PU・CP に course と q（Term／Quarter の番号））。
ph_sci.build は grade ≥ 11 で standard_code を「Physics 1, Quarter 2: Dynamics」「Grade 11 General Science, Term 1: …」、seo_title を「Physics 1: … Worksheets (Strengthened SHS)」、standard_url を科目の PDF（URL_COURSE、General Science は URL_SHS）にする。フィリピン独自の問題は ph_pools の CHEMISTS（Banzon・Lim-Sylianco など）・HOUSEHOLD・PH_GEO（Philippine Mobile Belt・Huxley's line）・DRRM（NDRRMC・go bag・hazard map）。core.php の grade_standard() に ph/science の Grade 11・12
Grade 11: physics-in-daily-life ✓ translational-and-rotational-motion ✓ simple-and-compound-machines ✓ the-physics-of-fluids ✓ utilization-of-electricity ✓ understanding-and-using-light-and-sound ✓ chemists-and-their-impact ✓ household-and-personal-care-products ✓ chemical-reactions-in-everyday-life ✓ solutions-in-the-environment ✓ unifying-themes-of-life-science ✓ the-importance-of-cells ✓ organ-systems-working-together ✓ philippine-ecosystems ✓ uniqueness-of-planet-earth ✓ uniqueness-of-the-philippines ✓ uses-of-earth-materials ✓ geologic-and-hydrometeorological-processes ✓ natural-hazards-and-disaster-preparedness ✓
Grade 12: Biology 1（the-cell・the-cell-cycle・transport-mechanisms・photosynthesis・cellular-respiration）✓／Biology 2（plant-tissues-and-organs・animal-tissues・organ-systems-in-animals）✓／Chemistry 1（scientific-measurement・quantum-theory-and-electronic-structure・isotopes-and-atomic-mass・percentage-composition-and-formulas・chemical-nomenclature・chemical-bonds-and-properties）✓／Physics 1（measurement-and-kinematics・forces-and-newtons-laws・work-energy-and-power・momentum-and-impulse・rotational-mechanics・periodic-motion）✓／Physics 2（gravitation・fluid-mechanics・heat-and-thermodynamics）✓／Earth and Space Science 1（the-universe-and-the-solar-system・history-and-structure-of-the-earth・minerals-rocks-and-soils・energy-sources）✓
トピック：新しい slug を ^…$ で足した（work-energy-and-power は in・za と共通の slug なので forces-and-motion に足していない）
PH / Science は Grade 3〜12 まで完了。Chemistry 2・Earth and Space Science 2 などの残りの選択科目は DepEd の CG が出たら

NG / Science（2025 年の改訂カリキュラムの教科名：Primary 1–3 Basic Science、Primary 4–6 Basic Science and Technology、JSS 1–3 Intermediate Science、SSS は Biology・Chemistry・Physics（WAEC・NECO）。1 つの SSS の学年ページに 3 科目が並ぶ（domain が科目名））— country `ng`、subject `science`、grade は数学と同じ primary-N・jss-N・sss-N、A4。イギリス英語（colour・metre・-ise・aeroplane・anticlockwise・programme・rubbish・mol dm⁻³）、pupils（Primary）・students（JSS・SSS）、1,000 以上はカンマ。
domain は Basic が NERDC のテーマ（Learning About Our Environment／Living and Non-Living Things／You and Energy／Science and Development）、standard_code は「Primary 4 Basic Science and Technology: You and Energy」「SSS 2 Physics: Waves」、seo_title は「… Worksheets (NERDC)」「(WAEC/NECO)」、standard_url は nerdc.gov.ng。core.php の subject_standard()・grade_standard() に ng/science。
単元は `tools/ng_s.py` の T（学年 → (テーマ, slug, "モジュール:slug:学年")）で、NC が他国の X 形式の単元（ph_s3・ph_s7・ph_s11・za_s4・za_s7・za_s10〜12・cabc_s11 など）の文とセットを使う（Philippine の単元は自分のセットの一覧をそのまま）。O[slug] に sub=[(古い文, 新しい文)]（フィリピン・南アの話をナイジェリアの話に：NiMet・harmattan・Kainji・NigeriaSat・Zuma Rock・Great Green Wall・Lake Chad など）と fill={セット名: [足すセット]}（足りないセット）。gen_ng_science_{primary1|jss1|sss1}_* は ng_sci.build(ng_s, 学年, slug) を呼ぶだけ（seed は 74000 + 100 × (primary N／JSS 6 + N／SSS 9 + N) + sort）。
共通部品は `tools/ng_sci.py`（ph_sci と同じ形。build の最初に _patch() する：ph_s* を import すると au_sci がフィリピン向けに戻るため。全部のセットの問題を _light で通し、フィリピン・南ア・北米の語（typhoon・PAGASA・jeepney・Karoo・oak・robin・bear・snow・summer の場面など）と他国の名前・お金を落とす。最後に米国式の綴りが残ると止まる）
Primary 1: science-in-daily-life ✓ living-and-non-living-things ✓ basic-needs-of-living-things ✓ materials-and-their-uses ✓ moving-objects ✓ light-and-sound ✓ the-non-living-environment ✓ patterns-in-weather ✓ the-sun-moon-and-stars ✓
Primary 2: plants-animals-and-habitats ✓ animal-life-cycles ✓ food-chains ✓ forces-and-movement ✓ magnets ✓ sound-light-and-heat-energy ✓ soils ✓ characteristics-of-the-sun ✓
Primary 3: gathering-scientific-information ✓ body-systems-of-plants-and-animals ✓ matter-and-its-three-states ✓ life-cycles-of-living-things ✓ contact-and-non-contact-forces ✓ characteristics-of-weather ✓ landforms-rocks-and-minerals ✓ the-solar-system ✓
Primary 4: scientific-investigation ✓ body-systems-in-animals ✓ microorganisms ✓ specialized-plant-structures ✓ friction-and-gravity ✓ static-electricity ✓ conductors-insulators-and-simple-circuits ✓ weathering-and-erosion ✓
Primary 5: changes-of-state ✓ physical-and-chemical-changes ✓ mixtures-and-separation-techniques ✓ the-circulatory-system ✓ plant-reproduction ✓ vertebrates-and-invertebrates ✓ simple-machines ✓ sound-waves ✓
Primary 6: photosynthesis-and-nutrition ✓ food-webs-and-interactions ✓ metals-and-non-metals ✓ mixtures-and-water-resources ✓ stored-energy-and-electricity ✓ electric-circuits ✓ the-surface-of-the-earth-and-fossils ✓ constellations ✓
JSS 1: planning-and-recording-investigations ✓ the-particle-model-of-matter ✓ solutions-solubility-and-concentration ✓ the-microscope-and-cells ✓ levels-of-biological-organization ✓ energy-transfer-in-ecosystems ✓ balanced-and-unbalanced-forces ✓ distance-displacement-and-velocity ✓ heat-transfer ✓ the-suns-influence-on-earth ✓
JSS 2: cellular-reproduction ✓ organ-systems-working-together ✓ taxonomic-classification ✓ photosynthesis-respiration-and-cycles ✓ the-atom-and-subatomic-particles ✓ elements-and-compounds ✓ acceleration-and-motion-graphs ✓ work-and-energy ✓ properties-of-light ✓ renewable-energy ✓
JSS 3: heredity ✓ human-reproduction ✓ the-periodic-table ✓ chemical-bonding ✓ newtons-laws-of-motion ✓ electric-circuits ✓ electromagnetic-waves ✓ structure-of-the-earth-and-geologic-time ✓ the-solar-system-and-space-technologies ✓ climate-change-and-sustainability ✓
SSS 1: Biology（biodiversity-and-classification・cells-the-basic-units-of-life・biosphere-to-ecosystems・photosynthesis・animal-nutrition）✓／Chemistry（classification-of-matter・states-of-matter-and-the-kinetic-molecular-theory・the-atom・the-periodic-table・chemical-bonding）✓／Physics（scientific-measurement・vectors-scalars-and-motion-in-one-dimension・forces-and-newtons-laws・energy-work-and-power・heat-and-thermodynamics）✓
SSS 2: Biology（transport-systems-in-mammals・gaseous-exchange・cellular-respiration・excretion-in-humans・population-ecology）✓／Chemistry（quantitative-aspects-of-chemical-change・ideal-gases-and-thermal-properties・acids-and-bases・redox-reactions・energy-and-chemical-change）✓／Physics（transverse-pulses-and-waves・sound・geometrical-optics・projectile-motion・momentum-and-impulse）✓
SSS 3: Biology（nervous-system-and-senses・endocrine-system-and-homeostasis・genetics-and-inheritance・evolution・human-impact-on-the-environment）✓／Chemistry（organic-molecules・rate-and-extent-of-reaction・chemical-equilibrium・electrochemical-reactions・the-lithosphere-and-mining）✓／Physics（electrostatics-coulombs-law-and-electric-fields・electric-circuits-ohms-law-and-power・electromagnetism・electrodynamics・optical-phenomena-and-properties-of-materials）✓
NG / Science は Primary 1〜SSS 3 まで完了（slug は他国と共通なので topics.php の変更なし）。NERDC が改訂版の詳しい単元表を出したら並びを見直す

CN / 科学（义务教育科学课程标准（2022年版）。単元は教科版の順）— country `cn`、subject `science`（科学）、grade `grade-N`（一年级…六年级）、A4。简体字で直接書く（OpenCC は使わない）。
生成は `python3 tools/cn_sci.py 学年 [slug|番号…]`（seed は 95000 + 100 × 学年 + 番号）、単元は `tools/cn_s1.py`（一・二年级）・`cn_s3.py`（三・四）・`cn_s5.py`（五・六）の UNITS(g)。
cn_sci.U(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, sets)、sets は lambda K: [(セット名, [(部品, 数)])] × 5。部品は K.P(rows, fwd, back)（対の表。正しい／まちがった「配对」の問題も作る）・K.G(groups, pos, neg)（pos・neg に必ず {g} を入れる）・K.TF(正しい文, [(まちがい, 正しくは)], topic)・K.B(手書きの行)・K.F(fn)。
domain は 物质科学／生命科学／地球与宇宙科学／技术与工程（dom は M・L・E・T）、standard_code は「第二学段（3～4年级） · 物质科学」、standard_url は教育部の課標ページ（cn_common.STD_URL）。繁体字とラテン文字（cm・kg・mL・N などを除く）が残ると止まる。
バンクは使う数より 2〜4 行多く書く（ちょうどだと足りなくなる）。表が 3 行以下の P は問題が作れない。容量は scratchpad の cn/cap.py で確かめる
トピックは topics.php の `topic_defs_science_cn()`（中国語の名前、単元 slug を ^(…)$ で列挙。他の国の理科のトピックは変えない）
一年级: plants ✓ comparing-and-measuring ✓ objects-around-us ✓ animals ✓
二年级: our-earth-home ✓ materials ✓ magnets ✓ ourselves ✓
三年级: water ✓ air ✓ weather ✓ motion-of-objects ✓ life-cycle-of-animals ✓ sun-earth-and-moon ✓
四年级: sound ✓ breathing-and-digestion ✓ motion-and-force ✓ growth-of-plants ✓ electric-circuits ✓ rocks-and-soil ✓
五年级: light ✓ changes-of-earths-surface ✓ measuring-time ✓ healthy-living ✓ living-things-and-environment ✓ ship-research ✓ heat ✓ environment-and-us ✓
六年级: the-tiny-world ✓ motion-of-the-earth ✓ energy ✓ tools-and-technology ✓ little-engineers ✓ biodiversity ✓ changes-of-matter ✓ the-universe ✓
CN / 理科（初中・高中）— 初中は义务教育物理・化学・生物学・地理课程标准（2022年版）、高中は普通高中课程标准（2017年版2020年修订）。単元は人教版の順。grade は grade-7〜grade-12（name 七年级〜九年级、高一・高二・高三）、1 つの学年ページに科目が並ぶ（domain が 物理／化学／生物学／地理、dom は P・C・B・D）。
standard_code は初中「第四学段（7～9年级） · 物理」、高中「普通高中物理 · 必修第一册」（U(..., part=教科書名) が必須）、standard_url は初中が cn_common.STD_URL、高中が STD_URL_HS。seo_title「…｜高一物理练习题（附答案）」。core.php の grade_standard() で学年ごとの基準名
単元は `tools/cn_s7.py`（生物・地理）、`cn_s8.py` ＝ cn_s8p・cn_s8b・cn_s8d、`cn_s9.py` ＝ cn_s9p・cn_s9c、`cn_s10.py` ＝ cn_s10p・c・b・d、`cn_s11.py` ＝ cn_s11p・c・b・d、`cn_s12.py`（4 科目）。`python3 tools/cn_sci.py 学年`（seed は 95000 + 100 × 学年 + 番号）
高中の単元は `tools/cn_hs.py` の H(dom, part, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T=[3 つの表 (セット名, rows, fwd, back[, extra])], TF の正誤, topic, calc=)：セットは表 3 つ・計算（calc 15 問＋表 5 問）か混合・正誤。数の問題は `tools/cn_num.py`（num：10 万以上と 0.001 未満は 6.02×10²³、nq：誤答 3 つがそろわないと None、単位の前に空白（° % ‰ は空白なし））。物理は g 取 10 m/s²
K.P の rows に (k, v, tag) を書くと誤答は同じ tag の行からだけ取る。2 値の表は extra で誤答を足す。kb・ks・title・what に「<」を書かない。cn_sci.py は __main__ ではなく import した cn_sci で動かす（LATIN の判定が別になるため）
CN / 理科 七年级（生物学・地理）: living-things-and-the-biosphere the-cell levels-of-organization green-plants photosynthesis-and-respiration human-reproduction-and-development nutrition-and-digestion breathing-and-circulation excretion-and-regulation the-earth-and-maps land-and-ocean weather-and-climate population-and-settlements asia-and-world-regions ✓
CN / 理科 八年级（物理・生物学・地理）: mechanical-motion sound-phenomena changes-of-state light-phenomena lenses-and-their-applications mass-and-density force motion-and-force-8 pressure buoyancy work-and-mechanical-energy simple-machines major-groups-of-animals animal-movement-and-behavior bacteria-fungi-and-viruses classification-and-biodiversity reproduction-and-development heredity-and-variation evolution-of-life infectious-disease-and-health territory-population-and-ethnic-groups terrain-and-climate rivers-and-lakes natural-resources transport-agriculture-and-industry four-geographic-regions ✓
CN / 理科 九年级（物理・化学）: internal-energy heat-engines current-and-circuits voltage-and-resistance ohms-law electric-power household-electricity electricity-and-magnetism information-and-energy into-the-world-of-chemistry air-and-oxygen atoms-molecules-and-elements water-and-chemical-formulas chemical-equations carbon-and-its-oxides combustion-and-fuels metals-and-metal-materials solutions acids-and-bases salts-and-fertilizers chemistry-and-life ✓
CN / 理科 高一（必修）: 物理 describing-motion uniformly-accelerated-motion forces-and-equilibrium force-and-motion-relationships projectile-and-circular-motion universal-gravitation-and-spaceflight work-energy-and-mechanical-energy／化学 classification-and-ionic-reactions redox-reactions sodium-and-chlorine amount-of-substance iron-and-metal-materials periodic-law-and-chemical-bonds sulfur-nitrogen-and-silicon reaction-energy-and-rate organic-compounds／生物学 molecules-of-the-cell cell-structure transport-across-membranes enzymes-and-atp cellular-respiration-and-photosynthesis cell-cycle-and-differentiation mendelian-inheritance meiosis-and-sex-linked-inheritance dna-structure-and-replication gene-expression mutation-and-breeding evolution-and-speciation／地理 earth-in-the-universe atmosphere-on-earth water-on-earth landforms vegetation-and-soil natural-disasters population-distribution-and-migration urbanization-and-urban-structure industrial-and-agricultural-location transport-and-regional-development human-environment-and-sustainability ✓
CN / 理科 高二（物理必修第三册・选择性必修）: 物理 electrostatic-field circuits-and-electrical-energy momentum-and-its-conservation mechanical-vibrations-and-waves light magnetic-forces-on-currents-and-charges electromagnetic-induction-and-alternating-current／化学 thermochemistry reaction-rate-and-chemical-equilibrium ionic-equilibria-in-solution electrochemistry atomic-structure-and-properties molecular-structure-and-properties crystal-structure-and-properties／生物学 homeostasis-and-nervous-regulation hormonal-regulation immune-regulation plant-life-regulation populations communities ecosystems humans-and-the-environment／地理 earth-motions plate-tectonics-and-landforms weather-systems atmospheric-circulation-and-climate ocean-currents integrity-and-differentiation regions-and-regional-development interregional-connections ✓
CN / 理科 高三（选择性必修第三册・选择性必修3）: 物理 molecular-kinetic-theory-and-gases laws-of-thermodynamics quantum-and-atomic-structure atomic-nucleus／化学 organic-compounds-and-hydrocarbons hydrocarbon-derivatives biomolecules-and-polymers／生物学 fermentation-engineering cell-engineering genetic-engineering／地理 resources-and-national-security environment-and-national-security ✓
トピック（topic_defs_science_cn）：化学→matter、力学→forces-and-motion、熱・電気・光・波・原子→energy、生物→living-things-and-ecosystems、地球仪・地球の運動→earth-and-space、ほかの地理（人文地理を含む）→earths-systems
CN / 科学・理科は小学一年级〜高三まで完了。次は他の国の理科（地理の選択性必修2 の残り、地理 選択性必修3 の残りは必要なら後で）

TW / 自然科學（十二年國教課綱 自然科學領域、108課綱）— country `tw`、subject `science`（name「自然科學」）、grade `grade-3`〜`grade-12`（國小三年級〜高中三年級。國小一、二年級は生活課程なのでなし）、A4。
`python3 tools/tw_sci.py 学年 [slug …]`（`--check` で中国の話が残る欄を表示。seed は 96000 + 100 × 学年 + 番号）。中国の理科の単元（cn_s*）を import して、cn_sci.it を tw_it に差し替え、問題を OpenCC s2tw（s2twp は 支持→支援・程序→程式 になるので使わない）と TERMS（位能・力學能・莫耳數・重量百分濃度・酵素・粒線體・族群・天擇・等加速度・正向力／壓力（CN の 压强→壓力、压力→正向力）・冷次定律・勞侖茲力・陰電性・游離能・混成・官能基・地函・滯留鋒…）で台灣の言葉にする。
中国だけの話（我國・長江・人民幣・天宮…、LEAKS）を含む表の行・問題は落とし（TK の P・G・TF・B）、ADD・ADD_G・ADD_TF・ADD_B で台灣の行（臺灣黑熊・櫻花鉤吻鮭・墾丁國家公園・臺北盆地…）を足す。単元の説明・FAQ は FIX で台灣の話に直す。問題が少し足りないときは同じ単元の他のセットの部品で埋める
単元の並び（GRADES）は台灣の教科書の一般的な配分：國小三〜六＝cn 小学（三年級に植物・動物・磁鐵を足す）、國中七＝生物、八＝理化（光・聲・熱と化学すべて）、九＝理化（力・電）と地球科學、高一＝部定必修 物理・化學・生物・地球科學、高二・高三＝加深加廣選修。domain は國小が 物質與能量／生命世界／地球與太空／科技與工程、國中が 生物／理化／地球科學、高中が 物理／化學／生物／地球科學。standard_code は「第四學習階段（國中） · 理化」「第五學習階段（高中） · 部定必修物理」、standard_url は國家教育研究院の自然科學領域課綱 PDF
トピックは topics.php の topic_defs_science_tw()（cn の正規表現に台灣の名前と説明）。core.php の subject_standard()・grade_standard() に tw/science
TW / 自然科學 は國小三年級〜高中三年級（153 単元）まで完了

KR / 과학（2022 개정 과학과 교육과정。초등 3~4학년군・5~6학년군は各 16 영역、중학교 1~3학년군は 23 영역、고등학교は 공통 과목 통합과학1·2 と 일반 선택 물리학·화학·생명과학·지구과학）— country `kr`、subject `science`（과학）、A4。
grade は grade-3〜grade-6（초등）、grade-7〜grade-9（중학교 1〜3학년）、`integrated-science-1`・`integrated-science-2`・`physics`・`chemistry`・`life-science`・`earth-science`（name「통합과학1」…、sort 10〜15、unit.php で 15〜17 歳と educationalLevel 고등학교、core.php の gs() は科目名だけ）。
초등은 영역 (1)~(8) を 3·5학년、(9)~(16) を 4·6학년、중학교は 중1 = 7 영역（2025 年の教科書）、중2・중3 = 8 영역ずつ。
生成は `python3 tools/kr_sci.py 学年 [slug|番号…]`（seed は 85000 + 100 × 学年の番号（고등학교は 10〜15）+ 番号）、単元は `tools/kr_s3.py`（3·4학년）・`kr_s5.py`（5·6학년）・`kr_s7.py`〜`kr_s9.py`（중학교）・`kr_s10.py`（통합과학1·2）・`kr_s11.py`（물리학·화학）・`kr_s12.py`（생명과학·지구과학）の UNITS(grade)。問題はすべて自前の韓国語。
kr_sci.H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T=[3 つの表], TFt, TFf, topic, tp, calc=, bank=)：表は (セット名, rows, fwd, back[, extra]) か (セット名, {グループ: [物]})、セットは表 3 つ・(calc 15 + 表 5) か混合・正誤。tp は topics.php のトピック。
助詞：‘{k}’・‘{v}’ の直後の助詞（은/는・이/가・을/를・과/와・으로/로）は kr_sci.fix_josa が中身の最後の文字（単位は kr_common.unit_josa）に合わせて直す。文のような値（…한다）を ‘{v}’ 물건은? の形にしない（「다음 설명에 알맞은 것은? ‘{v}’」にする）。
正誤の文は kr_sci.polite が「…다.」を「…ㅂ니다./…습니다.」にそろえる（正しい文とまちがいの文の文体で答えが分からないように）。「25 %」は pct で「25%」に。数は 1,000 からカンマ（kr_sci.num）、nq の単位は 초・분・시간・배・개・가지などは空白なし。
standard_code は「초등학교 3~4학년군 · 물질」「중학교 1~3학년군 · 운동과 에너지」「물리학 · 힘과 에너지」形式（domain は 초·중が 운동과 에너지／물질／생명／지구와 우주／과학과 사회、고등학교は 영역名）、standard_url は NCIC。core.php の subject_standard() に kr/science。
トピックは topics.php の topic_defs_science_kr()（単元 slug を ^(…)$ で列挙。science-and-society（과학과 사회）を足した。mq の分野には入らない）。プールの数は scratchpad の kr/cap.py で確かめる
KR / 과학 / 초등 3학년: 1. forces-in-our-lives 2. animal-life 3. plant-life 4. life-cycles 5. objects-and-materials 6. earth-and-the-sea 7. properties-of-sound 8. infectious-diseases-and-healthy-living ✓
KR / 과학 / 초등 4학년: 1. using-magnets 2. changes-of-state-of-water 3. changes-of-the-land 4. diverse-living-things 5. observing-the-night-sky 6. living-things-and-the-environment 7. various-gases 8. climate-change-and-our-lives ✓
KR / 과학 / 초등 5학년: 1. rock-layers-and-fossils 2. properties-of-light 3. dissolving-and-solutions 4. human-body-structure-and-function 5. separating-mixtures 6. weather-and-our-lives 7. heat-and-our-lives 8. resources-and-energy ✓
KR / 과학 / 초등 6학년: 1. acids-and-bases 2. motion-of-objects 3. plant-structure-and-function 4. earths-motions 5. seasonal-changes 6. combustion 7. using-electricity 8. science-and-my-career ✓
KR / 과학 / 중학교 1학년: 1. science-and-sustainable-life 2. organization-and-diversity-of-life 3. heat 4. changes-of-state-of-matter 5. action-of-forces 6. properties-of-gases 7. the-solar-system ✓
KR / 과학 / 중학교 2학년: 1. composition-of-matter 2. electricity-and-magnetism 3. plants-and-energy 4. animals-and-energy 5. changes-of-the-geosphere 6. light-and-waves 7. characteristic-properties-of-matter 8. hydrosphere-and-ocean-circulation ✓
KR / 과학 / 중학교 3학년: 1. laws-of-chemical-reactions-and-energy 2. atmosphere-and-weather 3. motion-and-energy 4. stimulus-and-response 5. reproduction-and-heredity 6. stars-and-the-universe 7. science-technology-and-civilization 8. disasters-and-safety ✓
KR / 과학 / 통합과학1: 1. basic-quantities-and-measurement 2. origin-of-elements 3. periodic-table-and-elements 4. chemical-bonding-and-properties 5. electrical-properties-of-materials 6. earth-system 7. mechanical-systems 8. life-systems-and-information-flow ✓
KR / 과학 / 통합과학2: 1. oxidation-and-reduction 2. acids-bases-and-neutralization 3. geologic-time-and-biodiversity 4. ecosystems-and-environment 5. global-environmental-change 6. energy-conversion-and-power-generation 7. renewable-energy 8. science-and-future-society ✓
KR / 과학 / 물리학: 1. motion-and-newtons-laws 2. momentum-and-equilibrium 3. energy-and-heat 4. electric-fields-and-circuits 5. magnetic-fields-and-induction 6. light-and-matter ✓
KR / 과학 / 화학: 1. mole-and-chemical-equations 2. atomic-structure-and-periodicity 3. chemical-bonds-and-molecular-shape 4. chemical-equilibrium 5. acids-bases-and-ph 6. neutralization-and-redox ✓
KR / 과학 / 생명과학: 1. characteristics-of-life 2. human-metabolism 3. neurons-and-the-nervous-system 4. homeostasis 5. immunity-and-disease 6. chromosomes-and-cell-division 7. human-genetics ✓
KR / 과학 / 지구과학: 1. plate-tectonics 2. rocks-and-geologic-history 3. weather-systems 4. ocean-and-atmosphere-interaction 5. planets-and-the-solar-system 6. stars-and-the-universe ✓
KR / 과학 は초등 3학년〜고등학교（통합과학1·2、물리학·화학·생명과학·지구과학）まで完了。진로 선택（역학과 에너지 など）は必要なら後で

ID / IPA（Kurikulum Merdeka の Capaian Pembelajaran。SD は IPAS（kelas 3–6、IPA の章だけ）、SMP は IPA（kelas 7–9）、SMA kelas 10 は IPA（Fase E）、kelas 11–12 は Fisika・Kimia・Biologi（Fase F。1 つの学年ページに 3 科目が並ぶ（domain が科目名））。単元は Kemendikbud の Buku Siswa の順）— country `id`、subject `science`（name「IPA」）、grade `kelas-N`、A4。
生成は `python3 tools/id_sci.py kelas-N [slug|番号…]`（seed は 86000 + 100 × 学年 + 番号）、単元は `tools/id_s3.py`（kelas 3・4）・`id_s5.py`（5・6）・`id_s7.py`〜`id_s12.py` の UNITS("kelas-N")。問題はすべて自前のインドネシア語。
id_sci.H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T=[3 つの表], TFt, TFf, topic, tp, calc=, bank=)：kr_sci.H と同じ形（表は (セット名, rows, fwd, back[, extra]) か (セット名, {グループ: [物]})、セットは表 3 つ・(calc 15 + 表 5) か混合・正誤）。TF の文は「.」で終える。数は 1.000（点）・小数はコンマ（id_sci.num・nq）。esc() が q・c・e・body の「< 」「 >」を &lt; &gt; に、「...」を「…」にする（check.py の double period）。
domain は SD・SMP が Makhluk Hidup／Zat dan Perubahannya／Energi, Gaya, dan Gerak／Bumi dan Antariksa／Sains dan Lingkungan、kelas 11–12 が Fisika／Kimia／Biologi。standard_code は「Fase D · Zat dan Perubahannya」、standard_url は id_common.STD_URL、seo_title は「… Kelas 7 IPA: Latihan Soal … dengan Kunci Jawaban」（≤6 は IPAS、11–12 は科目名）。title ≤ 60・kb ≤ 60・ks ≤ 150 を assert（cap.py は見ないので生成で確かめる）。
組み合わせの表（P）は、誤答の組が実は正しくなるもの（因果の連鎖、複数を食べる動物など）を使わない。遺伝子型のように大文字小文字だけ違う選択肢は item が重複扱いにする。
トピックは topics.php の topic_defs_science_id()（単元 slug を ^(…)$ で列挙、インドネシア語の名前。working-scientifically の 4 単元は mq の分野なし）。core.php の subject_standard() に id/science
ID / IPA / Kelas 3: 1. mengenal-hewan-di-sekitar-kita ✓ 2. siklus-hidup-makhluk-hidup ✓ 3. metamorfosis ✓ 4. komponen-biotik-dan-abiotik ✓ 5. hubungan-antarmakhluk-hidup ✓ 6. energi-di-sekitar-kita ✓ 7. bentang-alam-indonesia ✓
ID / IPA / Kelas 4: 1. perubahan-bentuk-energi ✓ 2. fotosintesis ✓ 3. gaya-dan-gaya-gesek ✓ 4. gaya-magnet ✓ 5. musim-dan-iklim-indonesia ✓ 6. efek-rumah-kaca-dan-gas-karbon ✓ 7. keanekaragaman-hayati ✓ 8. menjadi-pahlawan-lingkungan ✓
ID / IPA / Kelas 5: 1. ekosistem ✓ 2. rantai-dan-jaring-makanan ✓ 3. siklus-air ✓ 4. masa-pubertas ✓ 5. cahaya-dan-sifatnya ✓ 6. bayangan-dan-warna ✓ 7. bunyi-dan-perambatannya ✓ 8. pemantulan-dan-peredaman-bunyi ✓
ID / IPA / Kelas 6: 1. sistem-gerak-manusia ✓ 2. sistem-saraf ✓ 3. kesehatan-sistem-gerak ✓ 4. bumi-matahari-dan-bulan ✓ 5. rotasi-dan-revolusi-bumi ✓ 6. sistem-tata-surya ✓ 7. energi-tak-terbarukan ✓ 8. energi-terbarukan ✓ 9. bumi-kita-terancam-bahaya ✓
ID / IPA / Kelas 7: 1. hakikat-sains-dan-metode-ilmiah ✓ 2. laboratorium-dan-pengukuran ✓ 3. wujud-zat-dan-model-partikel ✓ 4. perubahan-wujud-zat ✓ 5. perubahan-fisika-dan-kimia ✓ 6. massa-jenis ✓ 7. suhu-dan-termometer ✓ 8. kalor-dan-perpindahannya ✓ 9. pemuaian ✓ 10. gerak-lurus ✓ 11. gaya-dan-hukum-newton ✓ 12. klasifikasi-makhluk-hidup ✓ 13. ekologi-dan-interaksi ✓ 14. sistem-tata-surya ✓ 15. pengaruh-gerak-bumi-dan-bulan ✓
ID / IPA / Kelas 8: 1. makanan-dan-nutrisi ✓ 2. sistem-pencernaan ✓ 3. sistem-peredaran-darah ✓ 4. sistem-pernapasan ✓ 5. sistem-ekskresi ✓ 6. usaha-dan-energi ✓ 7. pesawat-sederhana ✓ 8. tekanan-zat-padat-dan-cair ✓ 9. tekanan-gas-dan-penerapannya ✓ 10. getaran-dan-gelombang ✓ 11. cahaya-dan-alat-optik ✓ 12. pemisahan-campuran ✓ 13. tanah-dan-kehidupan ✓
ID / IPA / Kelas 9: 1. pertumbuhan-dan-perkembangan ✓ 2. sistem-koordinasi ✓ 3. sistem-reproduksi-manusia ✓ 4. homeostasis ✓ 5. listrik-statis ✓ 6. listrik-dinamis ✓ 7. kemagnetan-dan-induksi ✓ 8. reaksi-kimia ✓ 9. asam-basa-dan-garam ✓ 10. laju-reaksi ✓ 11. kromosom-dna-dan-gen ✓ 12. pewarisan-sifat ✓ 13. bioteknologi ✓ 14. isu-isu-lingkungan ✓
ID / IPA / Kelas 10: 1. besaran-satuan-dan-dimensi ✓ 2. angka-penting-dan-ketidakpastian ✓ 3. virus-dan-peranannya ✓ 4. struktur-atom ✓ 5. sistem-periodik-unsur ✓ 6. hukum-dasar-kimia ✓ 7. kimia-hijau ✓ 8. keanekaragaman-hayati-dan-klasifikasi ✓ 9. bakteri-dan-fungi ✓ 10. energi-terbarukan ✓ 11. perubahan-iklim ✓
ID / IPA / Kelas 11: Fisika（vektor-dan-gerak-parabola・dinamika-gerak-hukum-newton・gerak-melingkar・momentum-dan-impuls・fluida-statis・fluida-dinamis・gelombang-mekanik-dan-bunyi・termodinamika）✓／Kimia（ikatan-kimia-dan-bentuk-molekul・stoikiometri・termokimia・laju-reaksi-dan-kesetimbangan・hidrokarbon-dan-minyak-bumi）✓／Biologi（sel-dan-organel・transpor-membran・jaringan-tumbuhan・jaringan-hewan・sistem-imun）✓
ID / IPA / Kelas 12: Fisika（listrik-statis-dan-kapasitor・rangkaian-arus-searah・medan-magnet-dan-induksi-elektromagnetik・gelombang-elektromagnetik・fisika-kuantum・fisika-inti-dan-radioaktivitas）✓／Kimia（asam-basa-dan-ph・larutan-penyangga-dan-hidrolisis・sifat-koligatif-larutan・redoks-dan-elektrokimia・senyawa-karbon-dan-gugus-fungsi・polimer-dan-biomolekul）✓／Biologi（enzim-dan-metabolisme・respirasi-seluler-dan-fotosintesis・dna-dan-sintesis-protein・pembelahan-sel・pola-pewarisan-sifat・mutasi・evolusi）✓

ID / IPA は kelas 3〜12（SD IPAS・SMP IPA・SMA IPA／Fisika・Kimia・Biologi）まで完了。SD kelas 1–2 は IPAS がない（Fase A は IPAS なし）。kelas 11–12 の Biologi の残り（sistem organ の詳しい章）は必要なら後で

DE / Naturwissenschaften（Klasse 1–4 は Sachunterricht（GDSU Perspektivrahmen Sachunterricht 2013、domain は Lebende Natur／Nicht lebende Natur／Technik／Wetter, Erde und Himmel）、Klasse 5–6 は Naturwissenschaften（Biologie／Physik）、Klasse 7–10 は Biologie・Chemie・Physik（KMK-Bildungsstandards MSA 2004 i. d. F. vom 13.06.2024。1 つの学年ページに 3 科目が並ぶ（domain が科目名））。州ごとの Lehrplan に共通する一般的な配分で学年に分ける）— country `de`、subject `science`（name「Naturwissenschaften」）、grade `klasse-N`、A4。
生成は `python3 tools/de_sci.py klasse-N [slug|番号…]`（seed は 87000 + 100 × 学年 + 番号）、単元は `tools/de_s1.py`（Kl 1・2）・`de_s3.py`（3・4）・`de_s5.py`（5・6）・`de_s7.py`〜`de_s10.py` の UNITS(grade)。問題はすべて自前のドイツ語。
de_sci.H は id_sci.H と同じ形（表 3 つ・混合（calc 15 + T[1] 5、なければ T0 7 + T1 7 + T2 6）・正誤）。表の 6 番目の要素 match=False で「Welches Paar passt …」を作らない（値が重なる表）。行の 3 番目に tag を書くと誤答は同じ tag の行からだけ。
item は選択肢を小文字で比べるので、AA と aa のように大文字小文字だけ違う選択肢・キーを作らない（言葉を足す）。表の値は互いに排他的に（複数の食べ物を食べる動物、重なる栄養素などを避ける）。G の文は「Was gehört (nicht) zu {g}?」で g は与格（den Insekten）。正誤の文は「.」で終える。
数はドイツ式（小数はコンマ、5 桁以上はノーブレークスペース、6,02 · 10²³、単位の前にノーブレークスペース）、引用符は „…“。g ≈ 10 N/kg と問題文に書く。Kl 1–2 は title・kb ≤ 40、ks ≤ 100。
standard_code は「Perspektivrahmen Sachunterricht · Naturwissenschaftliche Perspektive」「Bildungsstandards Chemie (MSA)」、standard_url は Klinkhardt の Perspektivrahmen PDF と IQB の Bildungsstandards PDF（de_sci.STD_URL）、seo_title は「Kräfte – Physik Klasse 7: Arbeitsblätter mit Lösungen」。core.php の subject_standard()・grade_standard() に de/science。
トピックは topics.php の topic_defs_science_de()（ドイツ語の name、単元 slug を ^(…)$ で列挙。de の単元を足したら tp ごとに slug を足す）
DE / Naturwissenschaften / Klasse 1: unser-koerper-und-die-sinne tiere-um-uns-herum pflanzen-und-ihre-teile jahreszeiten-und-wetter stoffe-und-ihre-eigenschaften ✓
DE / Naturwissenschaften / Klasse 2: haustiere-und-ihre-pflege vom-samen-zur-pflanze wasser-eis-und-dampf magnete gesunde-ernaehrung-und-zaehne ✓
DE / Naturwissenschaften / Klasse 3: tiere-im-wald baeume-und-fruehblueher luft-und-wind licht-und-schatten schwimmen-und-sinken stabile-bauwerke-und-bruecken wetter-beobachten-und-messen ✓
DE / Naturwissenschaften / Klasse 4: der-menschliche-koerper lebensraum-wiese-und-teich strom-und-stromkreis schall-und-hoeren feuer-und-brandschutz hebel-und-einfache-maschinen sonne-erde-und-mond wasserkreislauf-und-wasser-sparen ✓
DE / Naturwissenschaften / Klasse 5: kennzeichen-des-lebendigen wirbeltierklassen saeugetiere-und-gebisse bluetenpflanzen tiere-im-winter temperatur-und-thermometer waerme-und-ihre-ausbreitung magnetismus ✓
DE / Naturwissenschaften / Klasse 6: zellen-und-mikroskop ernaehrung-und-verdauung atmung-und-blutkreislauf skelett-und-muskeln pubertaet-und-entwicklung licht-und-sehen schall elektrischer-stromkreis ✓
DE / Naturwissenschaften / Klasse 7: oekosystem-wald fotosynthese-und-zellatmung oekosystem-see wirbellose-tiere stoffe-und-ihre-eigenschaften teilchenmodell-und-aggregatzustaende gemische-und-trennverfahren chemische-reaktionen verbrennung-und-sauerstoff reflexion-und-brechung linsen-und-optische-geraete geschwindigkeit-und-bewegung kraefte ✓
DE / Naturwissenschaften / Klasse 8: vom-einzeller-zum-vielzeller sinnesorgane nervensystem-und-gehirn infektionen-und-immunsystem atombau-und-periodensystem metalle-und-redoxreaktionen salze-und-ionenbindung dichte-und-masse druck-und-auftrieb arbeit-energie-und-leistung einfache-maschinen-und-hebelgesetz ✓
DE / Naturwissenschaften / Klasse 9: hormone-und-regelung genetik-dna-und-zellteilung vererbung-und-mendel oekologie-und-stoffkreislaeufe saeuren-und-laugen neutralisation-und-stoffmenge molekuele-und-elektronenpaarbindung elektrischer-widerstand-und-ohmsches-gesetz elektrische-energie-und-leistung elektromagnetismus ✓
DE / Naturwissenschaften / Klasse 10: evolution gentechnik-und-biotechnologie stoffwechsel-und-enzyme kohlenwasserstoffe alkohole-und-carbonsaeuren kunststoffe radioaktivitaet kernenergie-und-energieversorgung beschleunigte-bewegung newtonsche-gesetze induktion-und-generator ✓
DE / Naturwissenschaften / Klasse 11–13（gymnasiale Oberstufe：11 = Einführungsphase、12 = Qualifikationsphase 1、13 = Qualifikationsphase 2。KMK-Bildungsstandards für die Allgemeine Hochschulreife in Biologie, Chemie und Physik（18.06.2020）。1 つの学年ページに 3 科目が並ぶ）— 単元は `tools/de_s11.py`〜`de_s13.py`。
de_sci.build は n ≥ 11 で standard_code を「Bildungsstandards Physik (Allgemeine Hochschulreife)」、standard_url を KMK の AHR ページ（STD_URL_AHR）、seo_title に「(Oberstufe)」。core.php の grade_standard() で基準名を AHR に、unit.php で educationalLevel「Gymnasiale Oberstufe」。
計算は calc（各単元 15 問）。数はドイツ式（num：3 有効数字、1,6 · 10⁻¹⁹）。表の値は互いに排他的に（「Was ändert sich?」のような重なる表は作らない）
Klasse 11: zellbiologie-und-biomembranen enzyme-und-enzymkinetik zellatmung-und-energiestoffwechsel oekologie-populationen-und-umweltfaktoren molekuelstruktur-und-zwischenmolekulare-kraefte funktionelle-gruppen-und-isomerie reaktionsgeschwindigkeit chemisches-gleichgewicht kinematik-und-wurfbewegungen impuls-und-stoesse kreisbewegung-und-gravitation mechanische-schwingungen ✓
Klasse 12: proteinbiosynthese-und-genregulation neurobiologie-und-synapsen molekulargenetische-methoden humangenetik-und-stammbaumanalyse saeure-base-gleichgewichte-und-ph-wert titration-und-puffer redoxreaktionen-und-elektrochemie batterien-akkus-und-elektrolyse elektrisches-feld-und-kondensator magnetfeld-und-lorentzkraft elektromagnetische-induktion wellen-und-interferenz ✓
Klasse 13: fotosynthese-lichtreaktion-und-calvin-zyklus evolutionstheorie-und-artbildung energiefluss-und-stoffkreislaeufe oekosysteme-und-nachhaltigkeit organische-reaktionsmechanismen aromaten-und-farbstoffe kunststoffe-und-polymerisation naturstoffe-kohlenhydrate-fette-und-proteine quantenobjekte-und-photoeffekt atomhuelle-und-spektren atomkern-und-radioaktivitaet elektromagnetische-schwingungen-und-wellen ✓
DE / Naturwissenschaften は Klasse 1〜13 まで完了
FR / Sciences（CP–CE2 は Questionner le monde（cycle 2）、CM1–6e は Sciences et technologie（cycle 3）：programme de sciences et technologie, arrêté du 5 juin 2026, BO n° 24 du 11 juin 2026（CP・CM1 は 2026 年度、CE1・CE2・CM2・6e は 2027 年度から）。5e–3e は physique-chimie と SVT（programmes du cycle 4, BO n° 31 du 30 juillet 2020、学年への配分は一般的な進度）、seconde は physique-chimie と SVT（2019）、première・terminale は enseignements de spécialité physique-chimie と SVT。1 つの学年ページに 2 科目が並ぶ（domain が科目名））— country `fr`、subject `science`（name「Sciences」）、grade は数学と同じ cp〜premiere と `terminale`（name「Terminale」、sort 12、unit.php で 17 歳）、A4。
生成は `python3 tools/fr_sci.py 学年 [slug|番号…]`（seed は 76000 + 100 × n + 番号、n は cp 1〜terminale 12）、単元は `tools/fr_sc2.py`（cp・ce1・ce2）・`fr_sc3.py`（cm1・cm2）・`fr_sc6.py`・`fr_sc5.py`・`fr_sc4.py`・`fr_sc3e.py`・`fr_sc10.py`（seconde）・`fr_sc11.py`（première）・`fr_sc12.py`（terminale）の UNITS(grade)。問題はすべて自前のフランス語。
fr_sci.H は de_sci.H と同じ形（表 3 つ・混合（calc 15 + T[1] 5、なければ T0 7 + T1 7 + T2 6）・Vrai ou faux ?）。G のグループ名は「des herbivores」「du vivant」の形（Lequel fait partie {g} ?）。esc() が「de le → du」「à les → aux」「de eau → d’eau」などの縮約と、: ; ? ! の前のノーブレークスペース、「1 000」のノーブレークスペースを直す。
数はフランス式（num：3 有効数字、小数はコンマ、1 000 から区切る、10⁶ 以上と 10⁻³ 未満は 6,02 × 10²³）。kb・ks・title・what に < > を書かない（「sous 7」「inférieur à K」）。大文字小文字だけ違う選択肢（n と N、AA と aa）は it() が捨てる。
standard_code は「Programme du cycle 3 · Matière, mouvement et énergie」「Programme du cycle 4 · Physique-chimie」「Spécialité de terminale · Sciences de la vie et de la Terre」、standard_url は BO 2026 n°24（cycle 2・3）、eduscol の cycle 4、lycée は eduscol（PC）と education.gouv.fr の lycée programmes（SVT）。seo_title「Le pH – Physique-chimie 3e : fiches et exercices corrigés」。core.php の subject_standard()・grade_standard() に fr/science
トピックは topics.php の topic_defs_science_fr()（フランス語の name、単元 slug を ^(…)$ で列挙。engineering-design は Objets techniques et numérique、mq の分野には入らない）
FR / Sciences / CP: le-vivant-et-le-non-vivant l-eau-solide-et-liquide les-aliments le-corps-et-la-sante les-objets-techniques ✓
FR / Sciences / CE1: les-besoins-des-plantes les-regimes-alimentaires-des-animaux les-cinq-sens l-air-et-l-eau le-circuit-electrique les-dents-et-les-repas ✓
FR / Sciences / CE2: le-cycle-de-vie-des-plantes la-croissance-des-animaux les-chaines-alimentaires mesurer-les-masses-et-les-volumes les-muscles-et-l-effort l-information-et-les-robots ✓
FR / Sciences / CM1: les-melanges-et-leur-separation les-ombres-et-les-phases-de-la-lune classer-le-vivant la-reproduction-des-animaux la-meteo-et-les-mesures le-cerveau-et-la-puberte les-objets-et-la-programmation ✓
FR / Sciences / CM2: les-etats-de-la-matiere les-circuits-electriques les-mouvements-et-le-systeme-solaire les-fossiles-et-les-temps-geologiques les-risques-naturels-et-le-climat digestion-circulation-et-reproduction concevoir-et-fabriquer-un-objet ✓
FR / Sciences / 6e: les-changements-d-etat-et-les-paliers masse-et-volume les-melanges-et-l-air la-vitesse-et-le-mouvement jour-nuit-et-saisons l-energie-et-les-circuits cellules-especes-et-parente pollinisation-et-decomposition sante-conservation-et-fermentation ✓
FR / Sciences / 5e: particules-et-etats-de-la-matiere melanges-et-solutions mouvements-et-vitesse circuits-en-serie-et-en-derivation la-lumiere-et-sa-propagation respiration-et-milieux-de-vie digestion-et-nutriments paysages-erosion-et-roches le-coeur-et-la-circulation ✓
FR / Sciences / 4e: atomes-molecules-et-transformations-chimiques masse-volumique tension-intensite-et-loi-d-ohm le-son-et-les-signaux forces-et-interactions reproduction-sexuee-et-asexuee puberte-et-reproduction-humaine seismes-volcans-et-tectonique meteo-climat-et-changement-climatique ✓
FR / Sciences / 3e: atomes-ions-et-noyau acides-bases-et-ph poids-et-gravitation energie-cinetique-et-conservation puissance-et-energie-electrique genetique-adn-et-chromosomes evolution-et-selection-naturelle immunite-et-vaccination systeme-nerveux-et-reflexes ✓
FR / Sciences / seconde: corps-purs-melanges-et-solutions atome-et-tableau-periodique la-quantite-de-matiere transformations-chimiques transformations-nucleaires mouvement-et-forces ondes-sonores-et-lumiere signaux-electriques-et-capteurs l-organisme-pluricellulaire biodiversite-et-evolution geosciences-sols-et-agrosystemes corps-humain-sexualite-et-microbiote ✓
FR / Sciences / première: composition-d-un-systeme-chimique suivi-d-une-transformation-et-avancement oxydoreduction-et-titrage structure-des-molecules-et-cohesion chimie-organique-et-combustions interactions-fondamentales-et-champs mouvement-et-forces-premiere energie-mecanique-et-travail ondes-mecaniques-progressives lumiere-lentilles-et-photon energie-electrique-et-rendement replication-mitose-et-mutations expression-du-patrimoine-genetique enzymes-et-metabolisme structure-et-dynamique-du-globe ecosystemes-et-services-ecosystemiques immunite-innee-et-adaptative ✓
FR / Sciences / terminale: acides-bases-ph-et-pka cinetique-chimique evolution-spontanee-et-piles synthese-organique-et-rendement lois-de-newton-et-mouvements orbites-et-lois-de-kepler thermodynamique-et-transferts-thermiques diffraction-interferences-et-doppler condensateur-et-circuit-rc radioactivite-et-decroissance brassages-genetiques-et-meiose evolution-et-histoire-des-especes datation-et-histoire-de-la-terre la-plante-et-la-domestication climats-passes-et-futurs cerveau-comportements-et-stress ✓
FR / Sciences は CP〜terminale まで完了

ES / Ciencias（LOMLOE。1.º〜6.º de Primaria は Conocimiento del Medio Natural, Social y Cultural（RD 157/2022）の理科の部分（domain は La vida en nuestro planeta／Materia, fuerzas y energía／Iniciación en la actividad científica／Tecnología y digitalización）、
1.º〜4.º de ESO は Biología y Geología・Física y Química（RD 217/2022。1.º ESO は BG、2.º ESO は FQ、3.º・4.º は両方）、1.º de Bachillerato は Biología, Geología y Ciencias Ambientales と Física y Química、
2.º de Bachillerato は Biología・Química・Física・Geología y Ciencias Ambientales（RD 243/2022。1 つの学年ページに科目が並ぶ（domain が科目名））。学年への配分は一般的な教科書の順）— country `es`、subject `science`（name「Ciencias」）、grade は数学と同じ（N-primaria・N-eso・N-bachillerato）、A4。
生成は `python3 tools/es_sci.py 学年 [slug|番号…]`（seed は 78000 + 100 × n + 番号、n は 1-primaria 1〜2-bachillerato 12）、単元は `tools/es_sc1.py`（1.º・2.º）・`es_sc3.py`（3.º・4.º）・`es_sc5.py`（5.º・6.º）・`es_sc7.py`〜`es_sc12.py` の UNITS(grade)。問題はすべて自前のスペイン語。
es_sci.H は fr_sci.H と同じ形（表 3 つ・混合（calc 15 + T[1] 5、なければ T0 7 + T1 7 + T2 6）・¿Verdadero o falso?）。G のグループ名は「los herbívoros」「el tronco」の形（¿Cuál pertenece a {g}?、esc() が a el → al、de el → del に）。
**表の逆向きの問題（back）で値が句のときは D =「¿Qué corresponde a esta descripción: {v}?」**（「¿Qué órgano {v}?」は値の動詞・名詞で文法が崩れる）。冠詞の付いたテンプレート（「¿Qué es el {k}?」）は表のキーの性・数がそろっているときだけ。
グループの項目と表の値は互いに排他的に（成体の植物も水が要る、雷は低くて大きい、などの重なりを作らない）。ok_text は ¿?・¡! の数、「a el」「de el」、ß などの他言語の文字（ü・â は可）を止める。割り算の「 : 」は可。
数はスペイン式（num：3 有効数字、小数はコンマ、5 けた以上はノーブレークスペース、4 けたはそのまま、6,02 · 10²³）。g = 9,8 m/s²、ESO・Bachillerato の掛け算は「·」。% は「25 %」（空白あり）。title ≤ 60・kb ≤ 60・ks ≤ 150（1.º・2.º は 40・40・100）、kb・ks・title・what に < > を書かない。
standard_code は「LOMLOE Primaria (segundo ciclo) · Materia, fuerzas y energía」「LOMLOE ESO · Física y Química」「LOMLOE Bachillerato · Química」、standard_url は es_common.STD_URL・STD_URL_ESO・STD_URL_BACH、seo_title は「El mol – Física y Química 3.º de ESO: fichas con soluciones」。core.php の subject_standard()・grade_standard() に es/science。
トピックは topics.php の topic_defs_science_es()（スペイン語の name、単元 slug を ^(…)$ で列挙。es の単元を足したら tp ごとに slug を足す）
ローカルの tools/schema.sql は standard_code が VARCHAR(40) のまま（本番は 175 文字のコードが入っているので広げてある）。ローカルで表示を試すときだけ ALTER する
ES / Ciencias / 1.º de Primaria: los-seres-vivos los-animales las-plantas el-cuerpo-y-los-sentidos los-materiales empujar-y-tirar ✓
ES / Ciencias / 2.º de Primaria: vertebrados-e-invertebrados la-vida-de-las-plantas los-habitats la-alimentacion-sana el-agua-y-sus-estados la-luz-y-el-sonido ✓
ES / Ciencias / 3.º de Primaria: los-animales-vertebrados los-animales-invertebrados la-nutricion-de-las-plantas el-aparato-locomotor la-materia-y-sus-propiedades las-fuerzas el-metodo-cientifico ✓
ES / Ciencias / 4.º de Primaria: los-reinos-de-los-seres-vivos los-sentidos-y-el-sistema-nervioso la-digestion-y-la-respiracion los-ecosistemas-y-las-cadenas-alimentarias las-mezclas la-energia-y-sus-fuentes las-maquinas ✓
ES / Ciencias / 5.º de Primaria: la-celula-y-los-tejidos la-circulacion-y-la-excrecion masa-volumen-y-densidad cambios-fisicos-y-quimicos el-calor-y-la-temperatura la-luz la-programacion-y-los-robots ✓
ES / Ciencias / 6.º de Primaria: los-microorganismos la-reproduccion-humana la-salud-y-los-habitos-saludables la-electricidad-y-el-magnetismo fuerzas-y-movimiento el-sonido la-energia-y-el-desarrollo-sostenible ✓
ES / Ciencias / 1.º de ESO: metodo-cientifico-y-laboratorio el-universo-y-el-sistema-solar la-tierra-y-la-luna minerales-y-rocas la-atmosfera la-hidrosfera la-celula-y-la-organizacion-de-los-seres-vivos la-clasificacion-de-los-seres-vivos las-plantas los-animales-invertebrados los-animales-vertebrados los-ecosistemas ✓
ES / Ciencias / 2.º de ESO: magnitudes-y-unidades la-materia-y-sus-propiedades estados-de-agregacion-y-teoria-cinetica sustancias-puras-y-mezclas los-cambios-quimicos el-movimiento las-fuerzas la-energia calor-y-temperatura la-luz-y-el-sonido ✓
ES / Ciencias / 3.º de ESO: la-organizacion-del-cuerpo-humano alimentacion-y-nutricion aparatos-digestivo-y-respiratorio aparatos-circulatorio-y-excretor sistema-nervioso-y-endocrino la-reproduccion-humana salud-y-enfermedad el-relieve-y-los-agentes-geologicos el-atomo-y-la-tabla-periodica enlace-quimico-y-formulacion el-mol-y-las-reacciones-quimicas la-electricidad ✓
ES / Ciencias / 4.º de ESO: la-celula-y-el-ciclo-celular genetica-mendeliana adn-y-biotecnologia la-evolucion la-tectonica-de-placas la-historia-de-la-tierra ecologia-y-medio-ambiente cinematica las-leyes-de-newton presion-y-fluidos trabajo-energia-y-potencia reacciones-quimicas-y-estequiometria quimica-del-carbono ✓
ES / Ciencias / 1.º de Bachillerato: ecologia-y-sostenibilidad historia-de-la-tierra-y-de-la-vida dinamica-y-composicion-terrestre fisiologia-e-histologia-animal fisiologia-e-histologia-vegetal los-microorganismos-y-formas-acelulares estructura-atomica-y-enlace-quimico gases-y-disoluciones estequiometria-y-termoquimica quimica-organica cinematica-del-punto-material dinamica energia-mecanica-y-trabajo ✓
ES / Ciencias / 2.º de Bachillerato: las-biomoleculas la-celula-eucariota el-metabolismo-celular genetica-molecular microbiologia-y-biotecnologia inmunologia modelo-cuantico-y-propiedades-periodicas enlace-quimico-y-geometria-molecular cinetica-quimica equilibrio-quimico acidos-y-bases reacciones-redox-y-electroquimica campo-gravitatorio campo-electrico campo-magnetico-e-induccion ondas-y-optica fisica-moderna riesgos-geologicos recursos-naturales-y-sostenibilidad ✓
ES / Ciencias は 1.º de Primaria〜2.º de Bachillerato まで完了

IT / Scienze（Indicazioni nazionali per il curricolo 2012 のスキエンツェ（primaria・secondaria di primo grado）、liceo scientifico は DM 211/2010 の Fisica と Scienze naturali（Biologia・Chimica・Scienze della Terra）。liceo は 1 つの学年ページに科目が並ぶ（domain が Fisica／Biologia／Chimica／Scienze della Terra））— country `it`、subject `science`（name「Scienze」）、grade は数学と同じ（classe-prima〜classe-quinta、prima-media〜terza-media、prima-liceo〜quinta-liceo）、A4。
生成は `python3 tools/it_sci.py 学年 [slug|番号…]`（seed は 79000 + 100 × n + 番号、n は classe-prima 1〜quinta-liceo 13）、単元は `tools/it_sc1.py`（classe prima・seconda）・`it_sc3.py`（terza・quarta）・`it_sc5.py`（quinta）・`it_sc6.py`〜`it_sc8.py`（media）・`it_sc9.py`〜`it_sc13.py`（liceo）の UNITS(grade)。問題はすべて自前のイタリア語。
it_sci.H は es_sci.H と同じ形（表 3 つ・混合（calc 15 + T[1] 5、なければ T0 7 + T1 7 + T2 6）・Vero o falso?）。G のグループ名は「gli erbivori」の形（Quale appartiene a {g}? → agli erbivori）。esc() が前置詞＋冠詞を縮約し（a gli → agli、su le → sulle、di l’ → dell’。冠詞が大文字の「di Le Châtelier」は直さない）、文字に挟まれた ' を ’ にする。表の逆向きで値が句のときは D =「A che cosa corrisponde questa descrizione: {v}?」。
数はイタリア式（num：3 有効数字、小数はコンマ、5 けた以上はノーブレークスペース、6,02 × 10²³）、g = 9,8。title ≤ 60・kb ≤ 60・ks ≤ 150（classe prima・seconda は 40・40・100）。グループの項目と表の値は互いに排他的に（極性分子と水素結合、溶解した固体の分離など）。
standard_code は「Indicazioni nazionali · Scienze, scuola primaria · Oggetti, materiali e trasformazioni」「Indicazioni nazionali per i licei · Scienze naturali (Chimica)」、standard_url は it_common.STD_URL・STD_URL_LICEI、seo_title は「La cellula – Scienze classe quinta: schede ed esercizi con soluzioni」（liceo は科目名）。core.php の subject_standard()・grade_standard() に it/science。
トピックは topics.php の topic_defs_science_it()（イタリア語の name、単元 slug を ^(…)$ で列挙）
IT / Scienze / classe prima: esseri-viventi-e-non-viventi i-cinque-sensi gli-animali le-piante i-materiali ✓
IT / Scienze / classe seconda: il-ciclo-vitale-delle-piante animali-e-ambienti l-acqua-e-i-suoi-stati solidi-liquidi-e-gas le-stagioni-e-il-tempo ✓
IT / Scienze / classe terza: il-metodo-scientifico la-materia l-acqua l-aria il-suolo ecosistemi ✓
IT / Scienze / classe quarta: classificazione-dei-viventi le-piante-e-la-fotosintesi invertebrati vertebrati il-calore catene-alimentari ✓
IT / Scienze / classe quinta: la-cellula-e-il-corpo-umano apparato-digerente-e-respiratorio circolazione-ed-escrezione sistema-nervoso-e-sensi l-energia luce-e-suono il-sistema-solare ✓
IT / Scienze / prima media: metodo-scientifico-e-misure stati-della-materia calore-e-temperatura idrosfera-atmosfera-e-suolo la-cellula classificazione-dei-viventi le-piante gli-animali ecosistemi ✓
IT / Scienze / seconda media: trasformazioni-chimiche acidi-e-basi il-moto le-forze leve-ed-equilibrio pressione-e-galleggiamento apparato-locomotore alimentazione-e-digestione respirazione-e-circolazione ✓
IT / Scienze / terza media: sistema-nervoso-e-ormoni riproduzione-e-genetica evoluzione elettricita magnetismo energia-e-fonti onde-luce-e-suono vulcani-e-terremoti rocce-e-minerali universo-e-sistema-solare ✓
IT / Scienze / prima liceo: grandezze-e-misure vettori-e-forze equilibrio-dei-solidi equilibrio-dei-fluidi materia-miscugli-e-sostanze leggi-ponderali-e-teoria-atomica caratteristiche-dei-viventi la-terra-nel-sistema-solare idrosfera-e-atmosfera ✓
IT / Scienze / seconda liceo: cinematica dinamica ottica-geometrica temperatura-e-calore la-mole la-cellula-e-le-membrane mitosi-e-meiosi biodiversita-ed-evoluzione ✓
IT / Scienze / terza liceo: lavoro-ed-energia quantita-di-moto-e-urti gravitazione-universale gas-perfetti-e-teoria-cinetica struttura-dell-atomo tavola-periodica legami-chimici genetica-mendeliana dna-e-sintesi-proteica minerali-e-rocce ✓
IT / Scienze / quarta liceo: termodinamica onde-e-suono ottica-ondulatoria campo-elettrico corrente-elettrica stechiometria-e-soluzioni equilibrio-chimico acidi-basi-e-ph ossidoriduzioni-ed-elettrochimica anatomia-e-fisiologia-umana ✓
IT / Scienze / quinta liceo: campo-magnetico induzione-elettromagnetica onde-elettromagnetiche relativita-ristretta fisica-quantistica-e-nucleare chimica-organica biochimica-e-metabolismo biotecnologie tettonica-delle-placche atmosfera-e-cambiamenti-climatici ✓
IT / Scienze は classe prima〜quinta liceo（liceo scientifico）まで完了

## みんなでクイズ ランキング（/worksheets/ranking/）

- 本体は eigo-duke.com の共通ファイル（`/common/php/mq.php`・`/common/js/mq.js`・`mq-geo.js`・`mq-rank.js`）。このリポジトリには `views/ranking.php`（ページの型枠）と `api/mq.php`（共通ファイルを読むだけ）だけ
- 集計テーブルは mq.php と同じ DB の qz_area・qz_done・qz_stat・qz_unit（mq.php が自動で作る。qz_stat・qz_unit は足すだけ）
- クラス：先生の端末に名前なしのクラス番号（16けた）を残し（localStorage の mq:cls、クラス名は端末の中だけ）、結果を qz_cres（クラス番号×単元×日、足すだけ）に記録。クラスの継続比較・上位 ◯% の表示はまだ（データだけためている）
- 文言は ja・en・zh（繁體）・zhs（简体、html lang zh-CN）・ko・id・tr・sv・de・fr・it・es・pt（mq.js の W、mq-rank.js の T。soloTop・soloFew・soloOne も全言語）。apu2 のランキングは ?lang=de・?lang=ko・?lang=zh-CN・?lang=sv などで言語を切り替え（views/ranking.php の $RK）
- mq-geo.js の n・lv は [ja, en, zh, de, fr, it, es, pt, ko, zhs, id, tr, sv] の 13 個。地域名は「その国のことば|English」、その国のことばで出す言語の番号は nl（kr は [8]、cn は [9, 2, 0]、id は [10]、tr は [11]、ch は [3, 4, 5]、se は [12]、ないときは [0]）。国は 23（id 38 州・tr 81 県・ch 26 州を 2026-11-25、se 21 län・ng 37 州を 2026-11-26 に追加）。生成は geo.py（eigo-duke 側の作業フォルダ）
- 共通ファイルを直すときは、ユーザーの手元の写しが古いことがある。前回納品した版（MQ_VER・VER の日付が新しいもの）をもとにする。MQ_VER（mq.php）と VER（mq.js）はそろえて上げる
- 国・地域のコードは mq-geo.js と mq.php の MQ_GEO をそろえる（新しい国を足したら両方に）
- 管理画面 /mq/admin.html（eigo-duke.com）は 2026-11-26 からパスワードなし（mq.php の adm_ は認証しない。読むだけ）
- 分野で国をくらべる（?sub=math&fd=fractions）：分野は `site/worksheets/inc/fields.php`（mq_fields に 12 言語の名前、MQ_TOPIC_FIELD で各国のトピック → 分野、MQ_SCI_FIELD、トピックに入らない単元は slug で補う）。`php tools/build_mq_fields.php` が inc/mq-fields.json（分野 → 単元）を作る（Actions も FTP の前に実行）。api/mq.php の $MQ_FIELD_FILE で mq.php に渡し、k_filter が fd の単元だけに絞る。新しい国・トピックを足したら MQ_TOPIC_FIELD に入れる（build_mq_fields.php が分野なしの単元を数える）。単元ページの Ranking ボタンはその単元の分野の国別比較を開く
- ひとりで解いた結果の地域：結果の下に地域を選ぶ欄（mq-geo.js をそのとき読む）。選んだ地域は localStorage の mq:area（みんなでクイズと共通）。a=solo に rg を送り、mq.php が qz_sstat の地域の行と qz_srhist（ひとりで × 地域の点数分布）に記録。地域・国・世界の「上位 ◯%」は pos_calc（a=pos と共通、人数が MQ_RANK_MIN 未満は目安）の p。Texas・Ontario・BC のページは地域を選ばなくてもその州
- 英語漬け.com（2026-11-27）：ひとりで解いた結果の下に都道府県を選ぶ欄（mq.js の soloRk、mq:area に保存、次から a=solo に rg）。ランキングページ /mq/ranking.html は MQR_CONF.subjects に { k, n（表示名）, s（フォルダ：shakai・exam/koten など）, only（国でくらべない教科は "jp"：比較タブと国の選択を出さない） } と scope: "rg"。mq.js の jpOnly()：/sansu/・/sugaku/・/rika/ 以外は「せかい」の行を出さない。mq.php の k_filter は eigo-duke では sub をフォルダの LIKE '/x/%' にする
- 地域の順位（2026-11-27）：mq.php の rg_rank が国の中の地域の順位 [順位, 数, 仮か, ‰, 1つ上の地域, ‰] を pos_calc の rr に入れる（人数が足りない地域は仮データ＝せかい・国の正答率＋area_off）。表示は mq.js の .mq-rr（rrA・rrUp・rrTop）と ws.js の .sn-rr（core.php の soloRR・soloRRUp・soloRRTop）
- apu2 のひとりで解いた結果：送信と「国で上位 ◯%／◯位」（2〜9 人は順位、速すぎて数えないときは soloFast）は ws.js（mq.php の a=solo が返す c・w を使う）。見出しの Ranking ボタン（.sn-rk、スマホではタイトルの右）は ranking/?cc=…&k=ページ&src=b。mq.js の watchSolo・見出しの .sn-rkb・a=pos の「あなたの位置」は eigo-duke だけ（if (!APU)）

## 日本語辞書（/japanese/{言語}/word/{単語}.html）— PHP + DB

- 単語ページは `site/japanese/_dict/word.php` が DB の **jd_word**（1語1行、13言語の訳を JSON）から作る。ルーティングは `site/japanese/.htaccess`
- 言語: en vi zh tw ko id es pt fr de ru th ar（13言語。単語ページは PHP なのでファイルは増えない）
- 正本は `jdict/words/*.json`（公開済みの全語・13言語）。外のフォルダには頼らない（作業環境が消えても作り直せる）
- 語を増やす: `jdict/todo/BATCH.json`（40語の一覧）→ キュー `jdict/queue.txt`（`tools/jdict_next.sh` で1つ取り出す）→
  書き手が `jdict/BRIEF.md` のとおり `jdict/batches/BATCH/`（base.json＋8言語）を作る → `python3 tools/jdict_check.py BATCH` でエラー0 →
  `python3 tools/build_jdict.py`（そろったバッチを取り込み、words・一覧ページ・index.json・サイトマップ・lastmod を作る。tw は zh から OpenCC）→ コミット・push
- `build_jdict.py` は新しい語がないとき公開済みのファイルを1文字も変えない（変わったら不具合）
- 反映: push で Actions が `site/japanese/` の変わったファイルだけを `/aplus/japanese/` へ put（mirror は使わない。単語の .html が多いため）、`tools/sync_jd.py` → `worksheets/api/jd_sync.php` が jd_word へ書く
- 公開済みの語の URL（slug）は build_jdict.py が jdict/words から読んで固定する。作成途中のバッチがあっても、いつでも公開してよい
- jd_word は追加・上書きだけ（INSERT … ON DUPLICATE KEY UPDATE）。DELETE・DROP・ALTER は書かない
- 移行中: サーバーに単語の .html が残っている間はそちらが優先。削除し終えたら `.htaccess` の `RewriteCond %{REQUEST_FILENAME} !-f` を消す

## apu2.com のトップ・About・プライバシーポリシー・会社紹介（site/top/。push で /aplus/ へ）

- `site/top/` は apu2.com のルート（/aplus/）と同じ並び（site/top/index.html → /aplus/index.html、site/top/de/about.html → /aplus/de/about.html、site/top/ja/company/index.html → /aplus/ja/company/index.html）
- push すると Actions が site/top/ の変わった .html だけを put（上書きのみ・削除なし。mirror は使わない）。全部送り直すときは workflow_dispatch の top_all
- 2026-11-28 にユーザーのサーバーの版（/, ja, de, fr, it, es, id, pt, tr, ko, tw, vi, au, ca, sg, uk, us の index・about、ja・id・ko・tw・vi・zh の company。zh の index・about も）を入れた。ほかの国・言語はユーザーが送ってきたら同じ場所に足す
- 直すときは site/top/ のファイルを直す（下の build_top.py で作り直したら out/ から site/top/ へ写す）

- 英語（/）と de・fr・it・es・pt・tr（/de/ など）の index.html・about.html は `tools/apu2_top/build_top.py`、privacypolicy.html（13言語のタブ）は `build_pp.py` で作る（出力は tools/apu2_top/out/）。文言と算数の国の一覧は `top_data.py`（MATH・CC・T・A）。en_*.html は元にした英語ページ
- トップ・About は 14 言語（en ja vi id zh tw ko de fr it es pt tr sv）すべて build_top.py で作る（2026-11-26 から ja〜ko のトップも。T[L] の order で節の順、j_c・e_c でその言語の講座、e_more で追加のリンク）。us・uk・au・ca・sg のトップと About だけは手で作った別のファイル。言語を足したら `python3 patch_en.py 元のファイル…` で言語メニュー・hreflang・フッターをそろえる（元のファイルはユーザーにもらう）
- 新しい国の算数を足したら MATH（並びの位置に insert）・CC（全言語の国名）・OWN・SHORT に足して作り直す。「{nk} の教育課程・{nc} の国と地域」は MATH から自動で数える（{nk1}・{nk2} は「ほか N」）
- 各言語フォルダ（/de/ /vi/ など）のトップ・About は、その言語の内容だけ（ほかの国の算数・「13言語すべて」のリンクは出さない）。算数はその国の学年の一覧（cards.py が content/ から学年と単元数を数える）。ja は 英語漬け.com の教科の一覧（top_data.JA_SUBJ）
- 英語圏の国別トップ・About（/us/ /uk/ /au/ /ca/ /sg/）は `build_cc.py`（もとのページ cc_src/ の head・header・footer を使い、その国の算数・理科の全学年を一覧にする。ほかの国へのリンクは出さない）。学年・単元を足したら build_top.py と build_cc.py を実行して out/ から site/top/ へ写す
- 新しい言語は LANGS・NEW・HREFLANG・SEL・LOCALE・CC・T・A と build_pp.py の P・ORDER に足す（top_data.py の末尾の sv を参照）

## 触ってはいけないもの

- `site/worksheets/inc/secret.php`（サーバーにだけある鍵。リポジトリに入れない）
- DB は ws_ で始まる4テーブルと jd_word 以外を変更しない（`api/sync.php` は ws_ の4つ、`api/jd_sync.php` は jd_word だけを書く）
- `/aplus/` の他のフォルダ、`/aplus/sitemap.php`（このリポジトリの外）
