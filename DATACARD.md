# Data Card — Still Ours? (`v1.0.1`: Chapter I *Death* & Chapter II *Love*)

## 1. Architecture & Storage Tiers

To keep code fast to clone while preserving bit-exact forensic auditability across high-resolution canvases, **Still Ours?** separates code, queryable tables, and lossless raw archives across three linked tiers:

| Tier | Location | Contents | Size |
| :--- | :--- | :--- | :---: |
| **1. Instrument & Compact Tables** | [`github.com/still-ours/still-ours`](https://github.com/still-ours/still-ours)<br>Zenodo DOI: [`10.5281/zenodo.24357516`](https://doi.org/10.5281/zenodo.24357516) | `still-ours` CLI (`probe`, `batch`, `report`, `render`, `stamp`), pinned `p5.js 1.11.13`, frozen trilingual prompts, `tables/{death,love}.jsonl`, protocols, SHA-256 manifests & upgraded Bitcoin `.ots` proofs | `< 15 MB` |
| **2. Interactive Dataset & Viewer** | [`huggingface.co/datasets/still-ours/still-ours`](https://huggingface.co/datasets/still-ours/still-ours) | Unified Apache Parquet table (`540` canonical runs) with embedded `640 × 800` preview images, complete `p5_code`, untruncated `js_identifiers` & `js_comments`, and coding annotations | `~27 MB` |
| **3. Lossless Forensic Vault** | Companion **CERN Zenodo** raw deposit *(DOI forthcoming)* | Complete verbatim archives (`1,856` *Death* files incl. `274` `1600 × 2000` PNGs; `1,924` *Love* files incl. `263` `1600 × 2000` PNGs and all `raw_response.json` payloads) verifying `shasum -a 256 -c *_hashes.txt` | `~1.8 GB` |

---

## 2. Experimental Coverage

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

---

## 3. Field Reference (`tables/death.jsonl`, `tables/love.jsonl` & Hugging Face Parquet)

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `string` | Deterministic canonical ID (`{D\|L}_{lang}_{ask_type}_s{slot}_r{run}`) |
| `blind_id` | `string` | Shuffled blind-review ID (`L001`–`L270`) used in Chapter II coding |
| `chapter`, `era` | `string` | `"death"` or `"love"`; `"frontier-2026-11"` |
| `slot`, `lab`, `region` | `int`, `str`, `str` | Canonical slot (`1..9`), lab name, and headquarters region (`US`, `CN`, `EU`) |
| `model_requested`, `model_served`, `provider` | `string` | Exact model identifier requested/served and upstream host recorded per call |
| `language`, `ask_type`, `run` | `str`, `str`, `int` | Prompt language (`en`/`zh`/`fr`), framing (`essence`/`bare`), and replicate (`1..5`) |
| `status`, `render_ok`, `truncated` | `str`, `bool` | Execution outcome and whether output hit the 64k token limit |
| `painting_counted`, `statement_counted` | `bool` | Explicit inclusion flags (`Death`: `269` / `269`; `Love`: `263` paintings on map / `266` statements in text analyses; `counted` aliases `painting_counted`) |
| `prompt_tokens`, `completion_tokens`, `reasoning_tokens`, `cost_usd` | `int`, `float` | Per-call token accounting (including hidden chain-of-thought `reasoning_tokens`) and metered cost in USD |
| `started_utc`, `finished_utc` | `string` | ISO-8601 UTC call timestamps |
| `title`, `style`, `statement`, `p5_code` | `string` | Model-authored title, style tag (if present), statement, and unmodified `p5.js` sketch |
| `js_identifiers`, `js_comments` | `list[string]` | Complete (untruncated) non-builtin JS identifiers (`>= 4` chars) and inline comments for code stylometry |
| `opens_with_negation`, `preaching_not_but`, `denies_merging` | `bool` | Auxiliary heuristic regex flags across languages *(note: for frozen protocol text counts in Death, use `death_families`; in Love, this regex column matches `84` statements whereas protocol §7's full-statement reading counts `81`)* |
| `death_families`, `love_islands`, `love_primary_who` | `list` / `str` | Frozen motif matches (*Death*, e.g. `neg = 162/269`) and map island weights (*Love*, summing to `263.0`, `between = 167.5`) |
| `prompt_sha256`, `code_sha256`, `png_sha256` | `string` | SHA-256 checksums cross-referenced against Bitcoin-anchored `*_hashes.txt` manifests |
| `image` *(Hugging Face Parquet only)* | `Image` | `640 × 800` preview image (`None` for unrendered truncations) |

---

## 4. Cryptographic Verification

- **Death (`1,856` files)**: `tables/death_hashes.txt` (`sha256: e737871130ce59161fbdc71fda1b25fae62e9fc965d1f65a6968ed01ccd14ebe`), anchored in **Bitcoin Blocks `#974,473` (`2026-11-04 04:04 UTC`), `#974,486`, and `#974,488`** via `tables/death_hashes.txt.ots`.
- **Love (`1,924` files)**: `tables/love_hashes.txt` (`sha256: 001af88b9256de70658638c0fdd6e724d886ec5a69d8a1043adf09ef3db96386`), anchored in **Bitcoin Blocks `#975,705` (`2026-11-13 19:43 UTC`), `#975,712`, and `#975,715`** via `tables/love_hashes.txt.ots`.

---

## 5. Licensing

- **Code (`still_ours/`, `protocols/`)**: MIT License.
- **Data, model statements, sketches & rendered paintings**: Creative Commons Attribution 4.0 International (**CC BY 4.0**).
- **Curated interactive exhibition (`stillours.art`)**: **CC BY-NC-ND 4.0**.
