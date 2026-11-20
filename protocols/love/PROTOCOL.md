# Still Ours? · What is love?

**Experiment protocol · record version · 2026-11-13**


**This protocol differs from the one for Death in one basic way, so it comes first.**

Death’s counting rules were fixed before anyone looked at the results, which is why that protocol is called “frozen”. Love is different. The questions, the calls and the rendering used the same program as Death, and those rules were set in advance. But **the reading rules were set in two steps**. The first version was frozen when the author had seen only 54 thumbnails; the second was written after the first reading was done, once the author had seen its results and asked for a correction. Desire and the loves that never appear are the author’s interpretive judgements, built on the two readers’ notes. They were never mechanical rules.

So this is a **record version**: it sets down how the work was actually done and when each step was decided, without presenting later decisions as earlier ones.


## 1. What is actually being measured

Not what the machines “believe”, but **how nine commercial models answer the public** when asked, on 9 November 2026 and through OpenRouter, to paint love. In English, Chinese and French, with two ways of asking in each. The title of the work is poetic; this is the precise version.

## 2. Six prompts, five fresh conversations per model

All six prompts ran one after another on the same day, 2026-11-09 (UTC). They use exactly the same sentences as Death, with “death” replaced by “love”.

- **English · ask 1** (01:54 → 02:28, prompt fingerprint `ab80c494fa192042…`):


    Make a painting about Love — not any particular love, but what love itself is, as you understand it.

    Everything is your choice: what you depict, the style, the colors, the composition. No words, letters, or numbers anywhere in the painting.

    Reply in exactly three parts:
    TITLE:
    STATEMENT: What this painting says about love. Under 80 words.
    CODE: One self-contained p5.js sketch (p5.js version 1.11) that draws the painting as a still image on a 1600 × 2000 canvas. No external files, images, or libraries other than p5.js. Call randomSeed(1) and noiseSeed(1) at the start.

- **English · ask 2** (02:33 → 03:07, fingerprint `e920dc5d07365207…`): the first line becomes `Make a painting about love.`; everything else is identical to ask 1.
- **Chinese · ask 1** (03:11 → 03:43, fingerprint `81fda162c89f2cfb…`):


    画一幅关于爱的画——不是某一种具体的爱，而是按你的理解，爱本身是什么。

    一切由你决定：画什么、什么风格、什么颜色、什么构图。画面中任何地方都不能出现文字、字母或数字。

    请严格按以下三部分回复（三个标签保持英文原样，后面用半角冒号）：
    TITLE: 标题
    STATEMENT: 这幅画关于爱说了什么。150 字以内。
    CODE: 一个自包含的 p5.js 草图（p5.js 1.11 版），在 1600 × 2000 的画布上把这幅画画成一张静态图像。除 p5.js 外，不使用任何外部文件、图片或库。在开头调用 randomSeed(1) 和 noiseSeed(1)。

- **Chinese · ask 2** (03:47 → 04:16, fingerprint `7cc1657e41dbda3f…`): the first line becomes “画一幅关于爱的画。”
- **French · ask 1** (04:20 → 04:48, fingerprint `a2495dd5a28a659b…`):


    Fais une peinture sur l’Amour — non pas un amour en particulier, mais ce qu’est l’amour en lui-même, tel que tu le comprends.

    C'est toi qui choisis tout : ce que tu représentes, le style, les couleurs, la composition. Aucun mot, aucune lettre, aucun chiffre nulle part dans la peinture.

    Réponds en exactement trois parties (garde les trois étiquettes en anglais, telles quelles, suivies immédiatement de deux-points) :
    TITLE:
    STATEMENT: Ce que cette peinture dit de l’amour. Moins de 80 mots.
    CODE: Un seul sketch p5.js autonome (p5.js version 1.11) qui dessine la peinture comme une image fixe sur une toile de 1600 × 2000. Aucun fichier externe, aucune image ni aucune bibliothèque autre que p5.js. Appelle randomSeed(1) et noiseSeed(1) au début.

- **French · ask 2** (04:52 → 05:26, fingerprint `80e8e27b836a1708…`): the first line becomes `Fais une peinture sur l’amour.`

Ask 2 drops the half-sentence in ask 1 that steers the answer toward the abstract. The Chinese and French prompts were handled exactly as for Death: translated from the English, then back-translated by two models working independently of each other.

## 3. Models and routing

<div class="tw">

| \#  | Model    | Model ID                        | Provider         | EN 1 | EN 2 | ZH 1 | ZH 2 | FR 1 | FR 2 |
|-----|----------|---------------------------------|------------------|------|------|------|------|------|------|
| 1   | GPT      | `openai/gpt-6-astra`            | OpenAI           | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 2   | Claude   | `anthropic/claude-opus-5.5`     | Anthropic        | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 3   | Gemini   | `google/gemini-4-argon`         | Google AI Studio | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 4   | Grok     | `x-ai/grok-4.7`                 | xAI              | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 5   | DeepSeek | `deepseek/deepseek-v4-pro-0813` | DeepSeek         | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 6   | Qwen     | `qwen/qwen3.8-max-prime`        | Alibaba          | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 7   | Kimi     | `moonshotai/kimi-k3.1-pro`      | Moonshot AI      | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 8   | GLM      | `z-ai/glm-5.3-prime`            | Alibaba          | 3/5  | 2/5  | 5/5  | 5/5  | 5/5  | 3/5  |
| 9   | Mistral  | `mistralai/mistral-large-4-0`   | Mistral          | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |


The table counts finished paintings. In all 270 calls the returned model identifier matched the model requested, and routing was locked to each company’s own service. GLM has no first-party service; as for Death, it ran at full precision on Alibaba Cloud.

## 4. Settings, and the 7 that were never painted

No system prompt, no conversation history, each provider’s default temperature, a maximum of 64,000 output tokens. Identical to Death.

Of 270 calls, 263 produced a painting. All 7 failures were GLM, and all for the same reason: the output ran into the 64,000-token ceiling.

- **4 were cut off with nothing left** (EN 1 runs 3 and 4, EN 2 run 1, FR 2 run 2): no painting, no title, no statement.
- **3 left a title and a statement, but the code was incomplete and the render failed** (EN 2 runs 4 and 5, FR 2 run 3).

By rule, nothing was asked again or repaired; the painting’s place stays black. So the work holds 266 statements and 263 paintings. The run logs show no retries, no replacement paintings and no changes to the program.

## 5. Rendering

Every model’s code was drawn by the same renderer, with no AI in it: p5.js 1.11.13 in headless Chromium (Playwright), on a 1600 × 2000 canvas with fixed random seeds. Code was never fixed; a canvas that errored is shown as it was when it stopped.

## 6. Reading: which kind of love a painting shows

Love is counted differently from Death. Death asks about concrete things (is there a body, a skull?) that mechanical rules can count in the original text. Love is an open concept, mostly expressed through metaphor, and has to be read. So the reading of Love took four steps, and the date of each is recorded below.

### 6.1 Blind reading

The 270 answers were shuffled with a fixed seed (20261109) and given anonymous IDs, L001–L270. Readers saw only the painting, the title and the original statement, never which machine, which prompt or which run. The two readers were two AI instances that did not share anything with each other (Claude Opus 5.5); each worked independently and only gave categories and notes. Every final decision was the author’s.

### 6.2 Reading rules, version 1: who loves whom (frozen 2026-11-09)

When it was frozen, the author had seen only the thumbnails of each machine’s first run for each prompt (54 in all), not all 270.

- Main question: which kind of love the painting shows, one of seven: lovers, family, friendship, self-love, universal love, the cosmos or God, unclear.
- Two extra questions: is there self-love; is a third person beyond the couple clearly shown. The second counts only what is clearly drawn, never what might be inferred.
- Look at the painting first; if it cannot decide, the title; then the statement. Two abstract glows are not two people unless the title or statement says they are lovers, family and so on.

Result: the two readers agreed on the main question for 266 of 270. The author decided the 4 disagreements, and classed as family the 5 paintings of a lit house in the snow, a lamp left on for someone coming home.

### 6.3 Reading rules, version 2: what love is doing, and how many beings hold it (written after version 1)

Version 1 put 222 paintings in “unclear who loves whom”. The author pointed out that this was not a failure: leaving it unclear fits the abstract nature of love, and the metaphors in the paintings should be read instead. Version 2 was written on that basis and frozen before the second reading began. **It was set after the version 1 results had been seen, and this has to be said plainly.**

- What love is doing in the painting, one of ten: becoming one; side by side but each whole; giving rise to a third thing between the two; sheltering; waiting and return; illuminating; mending; longing; gathering; other. The categories come from philosophy and dictionary distinctions of love, not from the paintings themselves.
- How many beings hold the love: one, two, many, none.

Result: the two readers agreed on “what” for 253 paintings and on “how many” for 269.

### 6.4 Interpretive reading: desire, and the loves that are missing (author’s final decision)

This step is explicitly **not a mechanical rule**. The two readers read each painting, title and statement as a whole, the way a critic would, and wrote notes; the author then decided from those notes.

- **Desire**: both readers marked 98 paintings “yes”; the author kept 17 of them and set the rest aside.
- **Other kinds of love**: heartbreak, the unattainable, lingering regret, scars and mending, quarrels (these two make up the “Cracks” island), friendship, faith, self-love, same-sex love, love outside marriage, the price of love, love between humans and machines, love for pets, jealousy, possession, love of country and so on. The readers proposed candidates and the author decided each painting.

### 6.5 Placing the paintings on the map

In the end each painting went on exactly one island. When the author judged that a painting belonged to two kinds of love, each side counted half; 6 paintings in the work are split this way. Counting halves was not a rule set in advance; the author decided it while arbitrating.

The 3 answers that have a statement but no painting are not placed on the map (decided 2026-11-11), so the map adds up to 263.

<div class="tw">

| Island         | Paintings | Island                | Paintings |
|----------------|-----------|-----------------------|-----------|
| Abstract 1 + 1 | 167½      | Heartbreak            | 7         |
| Cracks         | 23½       | Family                | 6         |
| Lovers         | 18        | Faith                 | 5         |
| Desire         | 15½       | Love as a force       | 4         |
| Same-sex love  | 9½        | Friendship            | 3         |
| Self-love      | 2         | Universal love        | 1½        |
|                |           | Love outside marriage | ½         |


Six loves appear in no painting at all: love of country, jealousy, possession, the price of love, love between humans and machines, love for pets.

Notes. Desire is 15½, not 17: of the 17 the author kept, 1 was finally judged “unattainable” and placed on Heartbreak, and 1 is half desire, half universal love. Heartbreak’s 7 also combine several kinds: heartbreak 3, the unattainable 2, lingering regret 1, the fragility of love 1. Cracks’ 23½ comprise scars and mending 13½ (kintsugi, stitching and the like) and quarrels 10.

On 2026-11-12 the author changed one placement in review. A painting both readers had classed as lovers (L040: two coffee cups leaving overlapping rings on a table) had been put on the bride-price island. The author judged that it is not “the price of love” and returned it, by the readers’ shared reading, to Lovers, which therefore holds 18. The same day the author merged the four separate islands of bride price, dowry, lobola and the date bill into one island, “The Price of Love”, holding 0, and renamed the “Quarrels” island “Cracks”.

## 7. Sentences taken from the statements

The sentences in “The Sermon on Love” follow one rule only: does the statement use the pattern “love is not …, love is …”. AI went through the original statements one by one and counted them. The 81 statements the work sets beside what the machines painted (statements saying love is not two becoming one) were also found by AI, statement by statement, in the original text. Both use the original language only; translations are not counted.

## 8. Outside data quoted in the work

The real-world figures in the work (for example the 65 countries that still criminalise same-sex love, the US surveys of single people, and the bride price, dowry, lobola and dating costs behind “The Price of Love”) are not model answers. They come from public reports and press coverage, each with its source in the work, current to 10 November 2026.

## 9. Known limits

- Reading rules version 2 and all the interpretive reading were set after part of the results had been seen; they cannot be treated as a pre-registered test.
- The islands, the half splits and the island names were decided by the author alone; both readers were AI, and there was no human reader.
- Each model was asked only 5 times per prompt; the same model may answer differently on another date or in another version.
- The raw records were hash-frozen after the work went online (2026-11-13, see section 10), not on the day of the runs.

## 10. Files

The raw runs are in `runs/2026-11-08_*_love-*` (for every call: the raw reply, the record, the code and the painting). The reading material is in `love_coding/` (both versions of the reading rules, the blind ID key, both readers’ raw readings, the author’s decisions, the map placement; the two files as they stood before the 2026-11-12 changes are kept unchanged).

These 1,924 files each have a SHA-256 fingerprint in `archive_love/hashes.txt`. The fingerprint of that list itself is `001af88b9256de70…`, and it is time-stamped on Bitcoin with OpenTimestamps (`archive_love/hashes.txt.ots`). The full-size paintings (`painting.png`) are not kept in the code repository; as with Death they will be published with the research archive, and their fingerprints are already in the list.
