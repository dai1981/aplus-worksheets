# How to write one dictionary batch (Japanese learner dictionary, 13 languages)

Readers are foreign learners of Japanese, anime fans and travellers. Each page must be correct, simple and useful.

## Input
`jdict/todo/BATCH.json` — a list of words: `{"w","kana","romaji","pos","en","cat"}` (`en` is only a hint).

## Output (write all 9 files)
Folder `jdict/batches/BATCH/`:

1. `base.json` — a JSON list, one object per word, in the input order:
```json
{"w": "炭治郎", "k": "たんじろう", "r": "tanjirou", "jlpt": "", "cat": "works", "pos": "proper noun", "forms": "",
 "sen": [{"en": "...", "vi": "...", "zh": "...", "ko": "..."}],
 "ex":  [{"ja": "炭治郎[たんじろう]は…。", "r": "Tanjirou wa ….", "en": "...", "vi": "...", "zh": "...", "ko": "..."}, {...}],
 "ph":  [{"ja": "炭治郎[たんじろう]のコスプレ", "en": "...", "vi": "...", "zh": "...", "ko": "..."}, {...}],
 "note": {"en": "...", "vi": "...", "zh": "...", "ko": "..."},
 "kj": [["炭", "タン", "すみ"], ["治", "ジ・チ", "おさ(める)・なお(す)"], ["郎", "ロウ", ""]],
 "syn": [], "ant": []}
```
2. `id.json es.json pt.json fr.json de.json ru.json th.json ar.json` — one object per language:
```json
{"炭治郎|たんじろう": {"sen": ["..."], "ex": ["...", "..."], "ph": ["...", "..."], "note": "..."}}
```
   The key is `w|k`. The lists have the same length and order as in base.json.

## Fields
- `w`, `k`, `r`: copy from the input (`k` = kana, `r` = romaji). Fix only a clear mistake, and say so in your reply.
- `cat`: copy from the input. `jlpt`: "" (only JLPT word lists use N5–N1).
- `pos`: noun, verb, i-adjective, na-adjective, adverb, expression, interjection, proper noun …
- `forms`: verbs and adjectives only, e.g. `食べます・食べて・食べない・食べた`. Otherwise "".
- `sen`: 1–3 senses. Dictionary style, short (e.g. "Domain Expansion (the ultimate technique in Jujutsu Kaisen)"). Most common sense first.
- `ex`: exactly 2 example sentences. Short and natural (JLPT N4–N3 level where possible). Both must contain the headword.
  - `ja` with furigana: every run of kanji is followed by its reading in square brackets: `電車[でんしゃ]に傘[かさ]を忘[わす]れた。` For names write the whole name: `炭治郎[たんじろう]`. Never leave a kanji without a reading.
  - `r`: Hepburn romaji of the whole sentence, first letter capital, long vowels as ou/uu (Tanjirou), particles は→wa, を→o, へ→e.
- `ph`: 2–3 very common short phrases with the word (furigana as above).
- `note`: 1–3 sentences that help a learner: what it is, the literal meaning of the kanji or the origin of the name, nuance or how it is used. One checkable fact is good.
- `kj`: one entry per distinct kanji in `w`: `[kanji, on (katakana, "・" between), kun (hiragana, okurigana in brackets)]`. "" when there is none. [] when `w` has no kanji.
- `syn`, `ant`: Japanese words (strings) only when there is a real synonym/antonym, else [].

## Translations
- vi, zh (Simplified), ko in base.json; id, es, pt, fr, de, ru, th, ar in the 8 files. Do not write Traditional Chinese (it is made from zh).
- Translate the meaning naturally, not word by word. Keep Japanese names and titles as they are commonly written in that language (official localized titles when you are sure, else romanized).
- No mixing of scripts (no Cyrillic in the Arabic text, etc.). No emoji.

## Accuracy rules
- State only facts you are sure of. Leave out a date, number or origin you are unsure about.
- Works and characters: describe them; never quote long lines, lyrics or passages. A short catchphrase that is itself the headword is fine.
- No sexual, hateful or violent detail. No living real persons except as the author/creator of a work.

## Check, then reply
Run `python3 tools/jdict_check.py BATCH` and fix every error. Reply only with: batch name, number of words, any input you corrected, and anything left unsure.
Put any helper scripts in your own temporary folder (`mktemp -d`), never in the repository.
