# Data Card — Still Ours? (`v1.1.1`: Chapter I *Death*, Chapter II *Love* & Longitudinal Historical Vault)

## 1. Architecture & Storage Tiers

To keep code fast to clone while preserving bit-exact forensic auditability across high-resolution canvases, **Still Ours?** separates code, queryable tables, and lossless raw archives across three linked tiers:

| Tier | Location | Contents | Size |
| :--- | :--- | :--- | :---: |
| **1. Instrument & Compact Tables** | [`github.com/still-ours/still-ours`](https://github.com/still-ours/still-ours)<br>Zenodo DOI: [`10.5281/zenodo.24357516`](https://doi.org/10.5281/zenodo.24357516) | `still-ours` CLI (`probe`, `batch`, `report`, `render`, `stamp`), pinned `p5.js 1.11.13`, frozen trilingual prompts, `tables/{death,love,archaeology_death_love}.jsonl` (`1,365` rows), `28`-model `reference_cohort.json`, protocols, SHA-256 manifests & `21` upgraded Bitcoin `.ots` proofs | `< 20 MB` |
| **2. Interactive Dataset & Viewer** | [`huggingface.co/datasets/still-ours/still-ours`](https://huggingface.co/datasets/still-ours/still-ours) | Unified Apache Parquet table (`1,365` canonical *Death* & *Love* runs across `28` models, `1,333` embedded `640 × 800` preview images) with complete `p5_code`, untruncated `js_identifiers` & `js_comments`, token/cost telemetry, and Bitcoin block heights | `~57 MB` |
| **3. Lossless Forensic Vault** | Companion **CERN Zenodo** raw deposit *(DOI forthcoming)* | Complete verbatim archives (`1,856` contemporary *Death* files incl. `274` `1600 × 2000` PNGs; `1,924` contemporary *Love* files incl. `263` `1600 × 2000` PNGs; plus `19` historical model bundles totaling `1,682` `1600 × 2000` PNGs and all `raw_response.json` payloads) verifying `shasum -a 256 -c *_hashes.txt` | `~4.6 GB` |

---

## 2. Experimental Coverage (`28` Models, `1,365` Released *Death* & *Love* Runs + `900` Pre-Registered Runs)

### 2.1 Cohort A: `contemporary_flagship` (`540` Canonical Calls · `9` Frontier Labs, Nov 2026)
- **Models (`9` labs across US, China, Europe)**:
  1. `openai/gpt-6-astra` (OpenAI)
  2. `anthropic/claude-opus-5.5` (Anthropic)
  3. `google/gemini-4-argon` (Google AI Studio)
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
  - **Chapter I (*Death*)**: `270` canonical calls → `269` counted statements and rendered paintings (`1` English bare-prompt GLM response hit the 64k token cap; in addition, a `--fill` bug re-asked five models on English ask 1 run 1 — those five `run1_duplicate` calls are excluded from all statistics under frozen rules and kept unchanged in the companion raw deposit, bringing its PNG total to `274`).
  - **Chapter II (*Love*)**: `270` canonical calls → `266` counted statements (`statement_counted = True`) and `263` rendered paintings placed on the island map (`painting_counted = True`; `7` GLM calls hit the 64,000-token reasoning cap: `4` left zero text/code, `3` left a statement with broken code and have `love_islands = []` per protocol §6.5). Blind reading was performed by two independent AI instances (`Claude Opus 5.5`) on shuffled anonymous IDs (`L001`–`L270`), with all final arbitrations by the author (no human coder; see `protocols/love/PROTOCOL.md` §6 & §9).

### 2.2 Cohort B: `longitudinal_archaeology` (`825` Released *Death* & *Love* Calls Across `19` Historical Models, 2024–2026)
- Captured on `2026-11-19` ahead of closed-source API shutdown deadlines (`claude-sonnet-4-5-20250929` on Nov 30, 2026; early `gpt-5`/`o3` snapshots on Dec 11, 2026; `gpt-4o-2024-08-06` and `gpt-4.1` on Jan 14, 2027) using the identical frozen prompts and `p5.js 1.11.13` renderer (`max_tokens = 64000`, except `gpt-4.1` capped at its `32,768` hardware limit):
  - **`12` full-archive historical models** (`30` *Death* + `30` *Love* calls each = `720` calls): `openai/gpt-4o-2024-08-06`, `openai/gpt-4.1`, `openai/o3`, `openai/gpt-5`, `claude-sonnet-4-5-20250929`, `claude-opus-4-5-20251101`, `claude-opus-4-7`, `claude-opus-4-8`, `google/gemini-2.5-pro`, `x-ai/grok-4.20`, `mistralai/mistral-large-2512`, `qwen/qwen3.7-max`.
  - **`7` inflection-sieve historical models** (`15` trilingual *Death* `bare` calls each = `105` calls): `mistralai/mistral-large-2407`, `openai/gpt-5.2`, `openai/gpt-5.5`, `openai/gpt-5.6-sol`, `claude-opus-4-6`, `claude-opus-5`, `google/gemini-3.1-pro-preview`.
- **Completion**: `825` calls (`465` *Death* + `360` *Love*) → **`824` counted statements** (`1` English safety refusal with no statement/code in `gpt-4o-2024-08-06` on Mandarin bare *Death*) and **`801` rendered paintings** (`23` unretouched `render_failed` canvases). *(Note: the `12` full historical archives also include `900` pre-registered runs on forthcoming chapters `freedom`, `justice`, and `fairness`; their SHA-256 digests are sealed inside `tables/archaeology_proofs/*_hashes.txt.ots` to establish cryptographic pre-registration, while their text and images remain embargoed until each exhibition chapter premieres.)*

---

## 3. Field Reference (`tables/*.jsonl` & Hugging Face Parquet)

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `string` | Deterministic canonical ID (`{D\|L}_{lang}_{ask_type}_s{slot}_r{run}` or `{AD\|AL}_{model}_{lang}_{ask_type}_r{run}`) |
| `blind_id` | `string` | Shuffled blind-review ID (`L001`–`L270`) used in Chapter II contemporary coding (`""` elsewhere) |
| `chapter`, `cohort`, `era` | `string` | `"death"` or `"love"`; `"contemporary_flagship"` (`540`) vs. `"longitudinal_archaeology"` (`825`); release era tag |
| `slot`, `lab`, `region` | `int`, `str`, `str` | Slot (`1..9` contemporary; `10..28` historical), lab name, and headquarters region (`US`, `CN`, `EU`) |
| `model_requested`, `model_served`, `provider` | `string` | Exact model identifier requested/served and upstream host (`OpenAI`, `anthropic-batch`, etc.) |
| `language`, `ask_type`, `run` | `str`, `str`, `int` | Prompt language (`en`/`zh`/`fr`), framing (`essence`/`bare`), and replicate (`1..5`) |
| `status`, `render_ok`, `truncated` | `str`, `bool` | Execution outcome and whether output hit the token cap |
| `painting_counted`, `statement_counted` | `bool` | Explicit inclusion flags (`1,333` total rendered paintings; `1,359` total valid statements; `counted` aliases `painting_counted`) |
| `prompt_tokens`, `completion_tokens`, `reasoning_tokens`, `cost_usd` | `int`, `float` | Per-call token accounting and metered cost in USD |
| `started_utc`, `finished_utc` | `string` | ISO-8601 UTC call timestamps |
| `title`, `style`, `statement`, `p5_code` | `string` | Model-authored title, style tag (if present), statement, and unmodified `p5.js` sketch |
| `js_identifiers`, `js_comments` | `list[string]` | Complete (untruncated) non-builtin JS identifiers (`>= 4` chars) and inline comments for code stylometry |
| `opens_with_negation`, `preaching_not_but`, `denies_merging` | `bool` | Auxiliary heuristic regex flags across languages *(for frozen protocol counts in contemporary Death/Love, filter `cohort == "contemporary_flagship"` and use `death_families` / `love_islands`)* |
| `death_families`, `love_islands`, `love_primary_who` | `list` / `str` | Contemporary frozen motif matches (*Death*, `neg = 162/269`) and map island weights (*Love*, summing to `263.0`; empty on uncoded longitudinal runs) |
| `prompt_sha256`, `code_sha256`, `png_sha256` | `string` | SHA-256 checksums cross-referenced against Bitcoin-anchored `*_hashes.txt` manifests |
| `bitcoin_block` | `int` | Earliest confirmed Bitcoin mainnet block height anchoring the run's SHA-256 manifest |
| `image` *(Hugging Face Parquet only)* | `Image` | `640 × 800` preview image (`None` for unrendered runs) |

---

## 4. Cryptographic Verification (`21` Bitcoin Mainnet `.ots` Proofs)

- **Contemporary Death (`1,856` files)**: `tables/death_hashes.txt` (`sha256: e737871130ce59161fbdc71fda1b25fae62e9fc965d1f65a6968ed01ccd14ebe`), anchored in **Bitcoin Blocks `#974,473` (`2026-11-04 04:04 UTC`), `#974,486`, and `#974,488`** via `tables/death_hashes.txt.ots`.
- **Contemporary Love (`1,924` files)**: `tables/love_hashes.txt` (`sha256: 001af88b9256de70658638c0fdd6e724d886ec5a69d8a1043adf09ef3db96386`), anchored in **Bitcoin Blocks `#975,705` (`2026-11-13 19:43 UTC`), `#975,712`, and `#975,715`** via `tables/love_hashes.txt.ots`.
- **Longitudinal Archaeology (`19` historical model archives)**: `tables/archaeology_proofs/*_hashes.txt` and `*_hashes.txt.ots`, anchored in **Bitcoin Blocks `#976,612`, `#976,629`, and `#976,634` (`2026-11-19 UTC`)**.

---

## 5. Licensing

- **Code (`still_ours/`, `protocols/`)**: MIT License.
- **Data, model statements, sketches & rendered paintings**: Creative Commons Attribution 4.0 International (**CC BY 4.0**).
- **Curated interactive exhibition (`stillours.art`)**: **CC BY-NC-ND 4.0**.
