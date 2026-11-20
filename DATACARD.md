# Data Card — Still Ours? (`v1.1.2`: Chapter I *Love*, Chapter II *Death*, Longitudinal Archive & Thinking-Switch Ablation)

## 1. Architecture & Storage Tiers

To keep code fast to clone while preserving bit-exact forensic auditability across high-resolution canvases, **Still Ours?** separates code, queryable tables, and lossless raw archives across three linked tiers:

| Tier | Location | Contents | Size |
| :--- | :--- | :--- | :---: |
| **1. Instrument & Compact Tables** | [`github.com/still-ours/still-ours`](https://github.com/still-ours/still-ours)<br>Zenodo DOI: [`10.5281/zenodo.24357516`](https://doi.org/10.5281/zenodo.24357516) | `still-ours` CLI (`v1.1.2`: `probe`, `batch`, `report`, `render`, `stamp`), pinned `p5.js 1.11.13`, frozen trilingual prompts, `tables/{death,love,archaeology_death_love}.jsonl` (`1,365` public rows), `tables/thinking_ablation_death_bare.jsonl` (`30` controlled ablation rows), `tables/love_sermon_concordance.json`, `27`-model verified `reference_cohort.json` (strictly *Love* & *Death* only), protocols, SHA-256 manifests & `23` Bitcoin `.ots` proofs | `< 25 MB` uncompressed |
| **2. Interactive Dataset & Viewer** | [`huggingface.co/datasets/still-ours/still-ours`](https://huggingface.co/datasets/still-ours/still-ours) | Two-shard Apache Parquet table (`1,365` public *Love* & *Death* runs across `28` queried model endpoints [`27` verified models], `1,333` embedded `640 × 800` preview images) with complete `p5_code`, untruncated `js_identifiers` & `js_comments`, `identity_verified`, nullable `reasoning_tokens` (`NA` where unexposed), `language_compliant`, and Bitcoin block heights | `~57 MB` (`2` shards) |
| **3. Lossless Forensic Vault** | Companion Zenodo raw deposit *(will be deposited separately; DOI forthcoming)* | Complete verbatim files for **released chapters only (*Love* and *Death*)** (`1,856` contemporary *Death* files incl. `274` `1600 × 2000` PNGs; `1,924` contemporary *Love* files incl. `263` `1600 × 2000` PNGs; plus `801` longitudinal *Death* & *Love* `1600 × 2000` PNGs, `30` thinking-ablation PNGs, and all `raw_response.json` payloads). Unreleased chapters remain embargoed and include SHA-256 hash manifests only. | Released slice only |

*(Note on exhibition ordering: across the live exhibition and frozen protocols, **Chapter I is Love** and **Chapter II is Death**, followed by **Chapter III: Freedom** [under embargo]. Chronologically, the Death protocol was executed first in early Nov 2026 and Love second in mid-Nov 2026.)*

---

## 2. Experimental Coverage (`28` Queried Endpoints [`27` Verified Models], `1,365` Public *Love* & *Death* Runs + `30` Controlled Ablation Runs)

### 2.1 Cohort A: `contemporary_flagship` (`540` Canonical Calls · `9` Frontier Labs, Nov 2026)
- **Models (`9` labs across US, China, Europe)**:
  1. `openai/gpt-6-astra` (OpenAI)
  2. `anthropic/claude-opus-5.5` (Anthropic)
  3. `google/gemini-4-argon` (Google AI Studio — *note: endpoint does not expose internal thinking token counts; marked `NA` / `reasoning_reported = false`*)
  4. `x-ai/grok-4.7` (xAI)
  5. `deepseek/deepseek-v4-pro-0813` (DeepSeek)
  6. `qwen/qwen3.8-max-prime` (Alibaba)
  7. `moonshotai/kimi-k3.1-pro` (Moonshot AI)
  8. `z-ai/glm-5.3-prime` (served full-precision via Alibaba; no first-party endpoint)
  9. `mistralai/mistral-large-4-0` (Mistral)
- **Call Design per Chapter**:
  - `3` languages (`en`, `zh`, `fr`) × `2` prompt framings (`essence` vs. `bare`) × `9` models × `5` stateless calls = **`270` canonical calls per chapter** (`540` total).
  - Zero system prompt, zero conversation history, provider-default temperature, `max_tokens = 64000`, `randomSeed(1)` and `noiseSeed(1)` inside `p5.js 1.11.13` at `1600 × 2000`.
- **Completion, Exclusions & Blind Coding**:
  - **Chapter I (*Love*)**: `270` canonical calls → `266` counted statements (`statement_counted = True`) and `263` rendered paintings placed on the island map (`painting_counted = True`; `7` GLM calls hit the 64,000-token reasoning cap: `4` left zero text/code, `3` left a statement with broken code and have `love_islands = []` per protocol §6.5). Blind reading was performed by two independent AI instances (`Claude Opus 5.5` — itself one of the nine evaluated models; **there was no human blind coder**) on shuffled anonymous IDs (`L001`–`L270`), with all final arbitrations by the author (`protocols/love/PROTOCOL.md` §6 & §9). The exhibition's *Sermon on Love* tally (`223` of `266` statements defining what love is, yielding `266` extracted definitional sentences: `171` negative `"Love is not…"` sentences and `95` affirmative `"Love is…"` sentences, with `43` statements containing both) is archived verbatim in [`tables/love_sermon_concordance.json`](tables/love_sermon_concordance.json).
  - **Chapter II (*Death*)**: `270` canonical calls → `269` counted statements and rendered paintings (`1` English bare-prompt GLM response hit the 64k token cap; five earlier `--fill` `run1_duplicate` calls are excluded from all statistics under frozen rules).

### 2.2 Cohort B: `longitudinal_archaeology` (`825` Public *Death* & *Love* Calls Across `19` Queried Endpoints [`18` Verified + `1` Unverified Alias])
- Executed on **`2026-11-19` UTC** ahead of closed-source API retirement dates (`claude-sonnet-4-5-20250929` retiring Nov 30, 2026; `gpt-4o-2024-08-06` and `gpt-4.1` retiring Jan 14, 2027) using the identical frozen prompts and `p5.js 1.11.13` renderer:
  - **`12` verified 60-call historical models** (`30` *Death* + `30` *Love* = `720` calls): `openai/gpt-4o-2024-08-06`, `openai/gpt-4.1`, `openai/o3`, `openai/gpt-5`, `claude-sonnet-4-5-20250929`, `claude-opus-4-5-20251101`, `claude-opus-4-7`, `claude-opus-4-8`, `google/gemini-2.5-pro`, `x-ai/grok-4.20`, `mistralai/mistral-large-2512`, `qwen/qwen3.7-max`.
  - **`6` verified 15-call bare-*Death* models** (`90` calls): `openai/gpt-5.2`, `openai/gpt-5.5`, `openai/gpt-5.6-sol`, `claude-opus-4-6`, `claude-opus-5`, `google/gemini-3.1-pro-preview`.
  - **`1` unverified retired alias (`mistralai/mistral-large-2407`, `15` calls — `identity_verified = false`, excluded from all statistics)**: Mistral officially retired `mistral-large-2407` on `2025-03-30` (documented to return HTTP 404 after retirement), yet OpenRouter returned `200 OK` on `2026-11-19` with `201,465 / 255,568` (`79.0%`) reasoning tokens incompatible with July 2024 weights. Retained in `tables/archaeology_death_love.jsonl` with `identity_verified = false` for audit completeness and excluded from `reference_cohort.json`.
- **Embargo rule for unreleased chapters**: The `12` full historical archives also pre-registered `900` runs on forthcoming chapters (`freedom`, `justice`, `fairness`). Only their call counts, failure counts, and SHA-256 digests (`tables/archaeology_proofs/*_hashes.txt.ots`) are public; **zero visual, motif, or text statistics from unreleased chapters appear in `reference_cohort.json` or any public table**.

### 2.3 Cohort C: `thinking_ablation_2026-11-20` (`30` Controlled Thinking-Switch Ablation Calls on `Claude Opus 4.8` & `Opus 5`)
- Stored in [`tables/thinking_ablation_death_bare.jsonl`](tables/thinking_ablation_death_bare.jsonl) (`30/30` rendered canvases, anchored via two OpenTimestamps manifests in `tables/archaeology_proofs/2026-11-20_*`).
- Because Nov-19 `Opus 4.5–4.8` batches ran without extended thinking (`thinking_tokens = 0`) whereas `Opus 5` (`159,050` thinking tokens across `15` calls, `~10.6k`/call) and `Opus 5.5` ran with thinking active by default, we ran the missing `2 × 2` crossover cells on frozen trilingual `death/bare` (`n = 15` each) via direct Anthropic Messages API:
  1. `claude-opus-4-8` with `thinking={"type": "adaptive"}, output_config={"effort": "high"}` (`avg 370.8` thinking tokens/call): Simpson title collision dropped from **`36.7%` → `10.0%`**, validated boat/ferryman compositions dropped from **`14/15` → `5/15`**, and opening negations dropped from `15/15` → `11/15`.
  2. `claude-opus-5` with `thinking={"type": "disabled"}` (`0` thinking tokens): Simpson title collision jumped **`16×` from `3.3%` → `53.3%`** (`5/5` identical Mandarin titles `"退潮"`, `4/5` identical French titles `"La chambre qui respire encore"`) and opening negations rose from `11/15` → `14/15`, while boats remained low (`2/15`).

---

## 3. Methodological Controls & Known Endpoint Differences

1. **Upstream API routing**: Contemporary `9` models were called via OpenRouter locked to first-party / full-precision providers; Nov-19 Anthropic historical runs used official Anthropic Message Batches (`anthropic-batch`), other Nov-19 runs used OpenRouter/OpenAI (`3` `mistral-large-2512` retry rows whose local `record.json` logged `"openrouter"` are normalized to `"Mistral"` from `raw_response.json`), and Nov-20 thinking-ablation runs used direct Anthropic Messages API (`anthropic-direct`).
2. **Model identifier echo vs. weight proof**: Across all APIs, `model_served` records the model string echoed by the server, which proves endpoint routing echo rather than cryptographic weight identity (as demonstrated by `mistral-large-2407` above).
3. **API output token caps (`api_output_cap`)**: `64,000` tokens on all models except `openai/gpt-4o-2024-08-06` (`16,384` API output cap) and `openai/gpt-4.1` (`32,768` API output cap — an API parameter ceiling, not a hardware limit).
4. **Reasoning token exposure (`reasoning_reported`)**: `google/gemini-4-argon` (OpenRouter) and three older Anthropic Batch endpoints (`claude-opus-4-5-20251101`, `claude-opus-4-6`, `claude-sonnet-4-5-20250929`, whose `usage` payload omitted `output_tokens_details`) do not expose thinking-token counts and are stored as `null` (`NA`, `reasoning_reported = false`), never `0`. `claude-opus-4-7` (`0`), `claude-opus-4-8` (`0`), and `claude-opus-5` (`159,050` total) include explicit `usage.output_tokens_details.thinking_tokens` in `raw_response.json`.
5. **Request parameter logging**: `still-ours` CLI (`>= v1.1.0`) writes full `request_params` into `record.json` (present in `thinking_ablation_death_bare.jsonl`); the `2026-11-19` harvest scripts left per-run `max_tokens` unset in `record.json` (batch-level `batch_input.json` is preserved for Anthropic batches).
6. **Release month vs. execution wall-clock**: All `825` longitudinal runs were executed on `2026-11-19` UTC; `era` indicates each snapshot's **release month** (`2024-08` to `2026-08`). Also note that the `15`-run bare-*Death* sieve rule (`> 15%` shift) was formulated exploratorily on the same day as data collection rather than pre-registered prior to collection.
7. **Language compliance (`response_language`, `language_compliant`)**: `openai/gpt-4o-2024-08-06` frequently answered Chinese and French prompts in English (`death/zh`: `8/10` English replies + `1/10` English safety refusal; `death/fr`: `8/10` English replies; `love/zh`: `3/10` English; `love/fr`: `5/10` English). Cross-linguistic comparisons should therefore exclude or flag `gpt-4o-2024-08-06`.

---

## 4. Automated Diagnostic Metrics & Validation (`still-ours report v1.1.2`)

Full validation statistics against the `269` human/protocol-coded contemporary *Death* runs are embedded in [`still_ours/data/reference_cohort.json`](still_ours/data/reference_cohort.json):

- **Metric 1 — Title Collision Probability (Simpson's $C$)**: Within each homogeneous cell $g = (\text{model}, \text{chapter}, \text{language}, \text{ask\_type})$, $C_g = \sum_t c_t(c_t - 1) / [n_g(n_g - 1)]$, averaged across cells with 1,000-resample cell bootstrap 95% CIs (invariant to sample size $n_g$).
- **Metric 2 — Excess Code Identifier Jaccard ($J_{\text{obs}} - J_{\text{null}}$)**: Within-cell pairwise Jaccard over non-builtin JS identifiers (`>= 4` chars, `P5_BUILTINS` stripped) minus empirical cross-model random pairing baseline $J_{\text{null}}$ matched by identifier-count quartile (`overall J_null = 0.0205`). Unvalidated visual regexes (`Corpse/Skull/Bed` combined recall `= 0.500 < 0.80` on frozen *Death* `body` `40/269`) are excluded from the automated scorecard; camelCase-split `Boat / Crossing` (`Precision = 1.000`, `Recall = 1.000` on OpenAI bare *Death* `14/15`) is reported separately as a validated auxiliary Death indicator.
- **Metric 3 — Opening Negation Rate**: Validated against Protocol v1.0 frozen `neg` (`162/269`) at **`95.9%` agreement, Cohen's $\kappa = 0.9134$** (`not X, but Y` auxiliary regex: `80.7%` agreement, $\kappa = 0.5792$).
- **Metric 4 — Reasoning Token Share (excl. truncations)**: Ranked separately within the reasoning-model sub-cohort; unexposed endpoints return `NA`; token-cap truncations are counted separately and excluded from the ratio.

---

## 5. Cryptographic Verification (`23` Bitcoin Mainnet / OpenTimestamps Proofs)

- **Contemporary Death (`1,856` files)**: `tables/death_hashes.txt` (`sha256: e737871130ce5916…`), anchored in **Bitcoin Blocks `#974,473`, `#974,486`, `#974,488`**.
- **Contemporary Love (`1,924` files)**: `tables/love_hashes.txt` (`sha256: 001af88b9256de70…`), anchored in **Bitcoin Blocks `#975,705`, `#975,712`, `#975,715`**.
- **Longitudinal Archaeology (`19` archives, `2026-11-19`)**: `tables/archaeology_proofs/2026-11-19_*_hashes.txt.ots`, anchored in **Bitcoin Blocks `#976,612`, `#976,629`, `#976,634`**.
- **Controlled Thinking-Switch Ablation (`2` archives, `2026-11-20`)**: `tables/archaeology_proofs/2026-11-20_*_hashes.txt.ots` (`94` files each).

---

## 6. Licensing

- **Code (`still_ours/`, `protocols/`)**: MIT License.
- **Data, model statements, sketches & rendered paintings**: Creative Commons Attribution 4.0 International (**CC BY 4.0**).
- **Curated interactive exhibition (`stillours.art`)**: **CC BY-NC-ND 4.0**.
