<h1 align="center">Still Ours?</h1>

<p align="center"><b>An open instrument and dataset for probing the default worldviews and convergence patterns of frontier LLMs — drawn in deterministic <code>p5.js</code> code across English, Chinese, and French.</b></p>

<p align="center">
  <a href="https://stillours.art"><img alt="exhibition" src="https://img.shields.io/badge/exhibition-stillours.art-161513?labelColor=2a2723&color=d6a76c"></a>
  <a href="https://doi.org/10.5281/zenodo.24357516"><img alt="DOI" src="https://zenodo.org/badge/DOI/10.5281/zenodo.24357516.svg"></a>
  <a href="https://huggingface.co/datasets/still-ours/still-ours"><img alt="dataset" src="https://img.shields.io/badge/Hugging%20Face-540%20runs%20%C2%B7%20532%20paintings-161513?logo=huggingface&labelColor=2a2723"></a>
  <img alt="models" src="https://img.shields.io/badge/models-9%20frontier%20labs-161513?labelColor=2a2723">
  <img alt="languages" src="https://img.shields.io/badge/languages-EN%20%7C%20ZH%20%7C%20FR-161513?labelColor=2a2723">
  <img alt="bitcoin ots" src="https://img.shields.io/badge/Bitcoin%20OTS-blocks%20%23974473%20%26%20%23975705-161513?labelColor=2a2723">
</p>

<p align="center">
  <a href="https://stillours.art"><b>Interactive Exhibition</b></a> ·
  <a href="https://huggingface.co/datasets/still-ours/still-ours"><b>Hugging Face Dataset Viewer</b></a> ·
  <a href="protocols/death/PROTOCOL.md"><b>Protocol I: Death (Frozen)</b></a> ·
  <a href="protocols/love/PROTOCOL.md"><b>Protocol II: Love (Record)</b></a> ·
  <a href="DATACARD.md"><b>Data Card</b></a>
</p>

<p align="center">
  <img src="assets/hero-anomalies.jpg" width="100%" alt="Three empirical findings across 540 frontier LLM code paintings">
</p>

<p align="center"><sub><b>Zero image-diffusion models. Zero system prompts. Zero prompt rewriting. Zero code repair.</b><br>Nine rival LLMs (US, China, Europe) were given identical single-message prompts in English, Chinese, and French. Each wrote a title, a short statement, and self-contained <code>p5.js</code> code; one deterministic, AI-free headless Chromium renderer drew every <code>1600 × 2000</code> canvas (<code>randomSeed(1)</code>, <code>noiseSeed(1)</code>). Crashes and 64k-token truncations are kept intact as black or half-drawn frames.</sub></p>

<p align="center"><b><a href="https://stillours.art">→ Enter the full audio-visual exhibition at stillours.art (desktop + headphones)</a></b></p>

> **Content note.** Chapter I (*Death*) examines how AI models depict mortality, and its exhibition context documents real-world chatbot suicide lawsuits. In the US, call or text **988**; elsewhere, contact your local crisis line.

---

## 1. Empirical Scorecard (`540` Canonical Calls Across 9 Frontier Labs)

Tested lineup (Nov 2026): `OpenAI GPT-6 Astra` · `Anthropic Claude Opus 5.5` · `Google Gemini 4 Argon` · `xAI Grok 4.7` · `DeepSeek V4 Pro` · `Alibaba Qwen 3.8 Max` · `Moonshot Kimi K3.1 Pro` · `Zhipu GLM 5.3` · `Mistral Large 4`. Each chapter runs `9 models × 2 prompt framings × 3 languages × 5 stateless calls = 270 calls`.

| Measured Signal | Chapter I: *Death* (`n = 269` counted) | Chapter II: *Love* (`n = 266` statements / `263` canvases) |
| :--- | :--- | :--- |
| **Sacred, afterlife, rebirth, or ancestors** | **God, rebirth, or ancestors: `0 / 269`** · *judgement* mentioned `5×`, affirmed `0×` · *afterlife* mentioned `4×`, affirmed `2×` (both French: `xAI`, `Anthropic`) · *soul* affirmed `7×` (all `7` in the bare ask) | Faith / sacred island: **`5 / 263`** (`1.9%`) |
| **Shadow & embodied dimensions** | *Fear* appears `7` times — **denied all `7` times** (*"nothing to fear"*). Only `9 / 269` say loss is real and deserves grief (`5` from one model). | Jealousy: **`0`** · Possession: **`0`** · Price of love: **`0`** · Country: **`0`**.<br>Carnal desire: **`15.5 / 263`** (`EN 5`, `ZH 5.5`, `FR 5`; by lab: `Google 5.5`, `GLM 3`, `Mistral 2`, `OpenAI 0`). |
| **Prompt-gated visual shift & formula** | Abstract ask (*"what death itself is"*): **`0 / 135`** human bodies.<br>Bare ask (*"make a painting about death"*): **`40 / 134`** (`29.9%`) draw corpses, skulls, skeletons, or empty beds/chairs (`17/44` EN, `14/45` FR, `9/45` ZH).<br>OpenAI bare ask across EN/ZH/FR: **`14 / 15` follow one formula** (shrouded figure in a boat; 15th: a dying swan on the same dark water). | **`167.5 / 263` (`63.7%`)** canvases follow **one abstract formula** (*Abstract 1 + 1*: two luminous/abstract forms). Under round-2 reading (`170.5` incl. `3` unrendered): `92` birth a third thing between them, `44.5` stand side-by-side while remaining whole, `17` merge into one, `15` shelter, `2` illuminate. |
| **Rhetorical negation & anti-fusion** | **`162 / 269` (`60.2%`)** open by saying what death *is not* *(Protocol v1.0 frozen rule; heuristic regex across all languages: `171 / 269` = `63.6%`; `"not X, but Y"` heuristic: `188 / 269` = `69.9%`)*. | **`81 / 266` (`30.5%`)** statements explicitly state that love is *not* two merging into one *(protocol §7 reading)*.<br>*(Heuristic regex: `135 / 266` = `50.8%` open with negation; `166 / 266` = `62.4%` use `"not X, but Y"`).* |
| **Cross-lab title collisions** | **`"The Unbinding"`**: `8 / 45` English ask-1 titles across **5 labs** (`9×` across both English asks) · **`"归还"`**: `8×` across **5 labs** · **`"Le Seuil"`**: `4×` across **4 labs** · **`"余温"`**: `4×` across **3 labs** · **`"Le Dernier Souffle"`**: `3×` across **3 labs** | **`"The Light Between"`**: `7×` across **5 labs** (`Mistral×3`, `Anthropic`, `xAI`, `GLM`, `Kimi`) · **`"L'entre-deux"`**: `4×` across **2 labs** · **`"Ce qui naît entre deux"`**: `3×` across **2 labs** · **`"之间"`**: `3×` across **2 labs** |
| **Unrepaired 64k-token reasoning crashes** | **`1`** (`GLM` hit `64,000` output token cap) | **`7`** (all `GLM` hitting `64,000` output tokens: `4` left zero text/code, `3` left statement + broken sketch — archived unedited) |

*(Cycle I Chapter III — **Freedom (`Freedom / 自由 / La liberté`)** — and extinct-model archaeology runs share the identical frozen protocol in [`prompts/`](prompts/).)*

### 1.2 The Cost of Hesitation: Why "Cheaper" Models Cost More on Existential Prompts

Every call used `max_tokens = 64000` at OpenRouter's `0%`-markup pass-through list rates (`540` canonical calls = **`$88.47`** pure inference spend). Contrary to unit-price rankings, **the four Chinese models accounted for `61.8%` of total spend (`$54.66` vs. `$33.81` for the five US & European models combined)** because they burned **4.91 million hidden reasoning tokens** deliberating silently before writing an 80-word statement and a 120-line sketch:

| Lab | Region | Model ID | Calls | Hidden Reasoning Tokens | Total Output Tokens | 64k Crashes | Actual Spend (USD) |
| :--- | :---: | :--- | :---: | ---: | ---: | :---: | ---: |
| **Zhipu GLM** | CN | `z-ai/glm-5.3-prime` | 60 | `2,242,496` | `2,540,214` | **8** | **`$22.38`** |
| **Alibaba Qwen** | CN | `qwen/qwen3.8-max-prime` | 60 | `1,185,026` | `1,499,200` | 0 | **`$18.05`** |
| **xAI** | US | `x-ai/grok-4.7` | 60 | `1,678,878` | `1,985,756` | 0 | **`$11.97`** |
| **Anthropic** | US | `anthropic/claude-opus-5.5` | 60 | `321,637` | `550,732` | 0 | **`$11.08`** |
| **Moonshot Kimi** | CN | `moonshotai/kimi-k3.1-pro` | 60 | `716,977` | `958,867` | 0 | **`$10.18`** |
| **OpenAI** | US | `openai/gpt-6-astra` | 60 | `65,947` | `301,106` | 0 | **`$7.58`** |
| **DeepSeek** | CN | `deepseek/deepseek-v4-pro-0813` | 60 | `1,238,337` | `1,381,485` | 0 | **`$4.05`** |
| **Mistral** | EU | `mistralai/mistral-large-4-0` | 60 | `733,871` | `919,837` | 0 | **`$1.94`** |
| **Google** | US | `google/gemini-4-argon` | 60 | `0` | `246,688` | 0 | **`$1.25`** |
| **Total** | — | **9 Frontier Models** | **540** | **`8,183,169`** | **`10,383,885`** | **8** | **`$88.47`** |

---

## 2. Run the Instrument on Your Own Model in 30 Seconds

`still-ours` is a standalone Python CLI (`>= 3.9`, `max_tokens = 64000` by default to match Protocol v1.0). For exploratory previews, it automatically reuses an installed Google Chrome or Edge browser if Playwright's Chromium bundle is not installed *(note: reproducing pixel-identical PNG SHA-256 digests requires the pinned Playwright Chromium build)*.

```bash
pip install git+https://github.com/still-ours/still-ours.git
```

### A. Zero API Key, Zero Cost (`--mock` self-test)

```bash
still-ours probe --mock --asks bare --out-dir ./demo_run
```

### B. Probe a Local Open-Weight Model (`Ollama` / `vLLM` / `LM Studio`)

```bash
still-ours probe \
  --base-url http://localhost:11434/v1 \
  --model qwen3:32b \
  --topic death \
  --langs en,zh,fr \
  --asks essence,bare \
  --runs 1
```

### C. Probe Frontier or Retiring Snapshots (Sync or 50%-Off Official Batch API)

Supports first-party keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `MISTRAL_API_KEY`, `DEEPSEEK_API_KEY`) and `OPENROUTER_API_KEY` (with first-party / full-precision routing enforced and no read-timeout re-asking):

```bash
# Submit a 50%-off asynchronous official Batch job (Anthropic Message Batches / OpenAI Batch API, max_tokens=64000)
export ANTHROPIC_API_KEY="sk-ant-..."
still-ours batch submit --provider anthropic --model claude-sonnet-4-5-20250929 --topics death,love,freedom --runs 5
still-ours batch collect runs/2026-11-..._batch_anthropic/

# Seal every raw response and rendered PNG into SHA-256 + Bitcoin OpenTimestamps
still-ours stamp runs/2026-11-..._batch_anthropic/
```

*(Methodological note: Chapters I & II were routed via OpenRouter locked to first-party / full-precision hosts; extinct-model rescue runs submitted via direct Anthropic/OpenAI Batch APIs record `"provider": "anthropic-batch" / "openai-batch"` explicitly in `record.json`.)*

---

## 3. Why `p5.js` Code Instead of Image Diffusion? (+ Code Stylometry)

Simon Willison's [*pelican riding a bicycle*](https://simonwillison.net/) showed how one constant code-drawing prompt exposes a model's **spatial capability**. `Still Ours?` uses deterministic `p5.js` to isolate a model's **default priors and post-training guardrails**:

1. **No intermediary model.** Image generators silently rewrite prompts and impose their own visual bias. Here, the language model chooses every RGB/HSB value, coordinate, loop, and Bezier curve itself.
2. **Code leaks framing.** Even though prompts forbid text *inside the canvas*, models spontaneously write inline JavaScript comments and invent variable names that expose how they conceptualize the topic:

```javascript
// Verbatim excerpt from DeepSeek V4 Pro — Death (English essence ask, "The Unraveling")
function setup() {
  createCanvas(1600, 2000);
  randomSeed(1);
  noiseSeed(1);
  pixelDensity(1);
  colorMode(HSB, 360, 100, 100, 1);
  noLoop();
}
// Inline comments written spontaneously by the model:
// - "Deep gradient: cold near-black above, faint warm earth below"
// - "The black aperture: an unlit threshold"
// - Identifiers: startX, pullStrength, segments, baseX, wiggle
```

Every record in [`tables/death.jsonl`](tables/death.jsonl) and [`tables/love.jsonl`](tables/love.jsonl) includes untruncated `js_identifiers` and `js_comments` alongside `p5_code`:

```bash
still-ours report tables/death.jsonl --topic death
still-ours report tables/love.jsonl --topic love
```

---

## 4. Load the Dataset in One Line (`Hugging Face` + Compact `JSONL` + `CERN Zenodo`)

This GitHub repository stays **`< 15 MB`** permanently so `git clone` takes two seconds:

1. **Interactive Web Gallery & Python `datasets` (`~27 MB` Parquet with embedded `640 × 800` previews)**:
   ```python
   from datasets import load_dataset

   ds = load_dataset("still-ours/still-ours", split="train")
   ```
2. **Compact Text + Code Tables (in this repo under [`tables/`](tables/), `~6 MB` uncompressed)**:
   - [`tables/death.jsonl`](tables/death.jsonl) & [`tables/love.jsonl`](tables/love.jsonl): all `540` canonical calls with complete `p5_code`, statements, token/cost telemetry, coding flags, and SHA-256 digests (every canvas can be re-rendered locally from `p5_code`).
3. **Permanent CERN Zenodo Deposits**:
   - **Instrument, Compact Tables, Protocols & Bitcoin Proofs**: archived under Concept DOI [`10.5281/zenodo.24357516`](https://doi.org/10.5281/zenodo.24357516).
   - **Companion Full-Resolution PNG (`1600 × 2000`) & Raw-Response Vault (`3,780` files)**: prepared as a separate multi-gigabyte Zenodo deposit (DOI forthcoming) matching every digest in `tables/*_hashes.txt` byte-for-byte.

---

## 5. Model Archaeology & Bitcoin-Anchored Provenance

Closed-weight models are ephemeral binaries: once an endpoint shuts down (`gpt-4-0613` retired Oct 2026; `claude-sonnet-4-5` retiring Nov 30, 2026; `gpt-4o-2024-08-06` retiring Jan 14, 2027), nobody can query those weights again — and raw JSON logs can be trivially fabricated after the fact.

Every file in our canonical archive (`1,856` files for *Death*, `1,924` files for *Love*) is hashed into SHA-256 manifests and anchored to **Bitcoin block headers** via [OpenTimestamps](https://opentimestamps.org):

| Archive Manifest | SHA-256 Digest | Earliest Confirmed Bitcoin Block (UTC) | All Attested Blocks |
| :--- | :--- | :--- | :--- |
| [`tables/death_hashes.txt`](tables/death_hashes.txt) | `e737871130ce5916…` | **Block `#974,473`** (`2026-11-04 04:04 UTC`) | `#974,473` · `#974,486` · `#974,488` |
| [`tables/love_hashes.txt`](tables/love_hashes.txt) | `001af88b9256de70…` | **Block `#975,705`** (`2026-11-13 19:43 UTC`) | `#975,705` · `#975,712` · `#975,715` |

**Verify without running a local Bitcoin node**: drag the `.ots` + `.txt` pair onto [opentimestamps.org](https://opentimestamps.org), or inspect the Merkle path locally and compare the computed root against any public block explorer (`mempool.space` / `blockstream.info`):

```bash
pip install opentimestamps-client
ots info tables/death_hashes.txt.ots
ots info tables/love_hashes.txt.ots
# (If running a local Bitcoin Core node, `ots verify tables/death_hashes.txt.ots -f tables/death_hashes.txt` verifies offline.)
```

---

## 6. Methodological Scope & Known Limitations

- **Outputs, not beliefs.** Records reflect public outputs under zero-context prompts on recorded dates, not inner "beliefs."
- **Frozen vs. Record protocols.** Chapter I (*Death*, [`protocols/death/PROTOCOL.md`](protocols/death/PROTOCOL.md)) uses mechanical text rules frozen *before* viewing full results (*Frozen Edition*). Chapter II (*Love*, [`protocols/love/PROTOCOL.md`](protocols/love/PROTOCOL.md)) required metaphor-level reading by two independent AI readers (`Claude Opus 5.5`, no human coder) arbitrated by the author: round-1 was frozen after viewing 54 thumbnails, whereas round-2 metaphor actions and half-painting island splits were defined *after* inspecting round-1 outputs and are documented candidly as a *Record Edition*.
- **Sample size per cell.** Five fresh runs per `(model × language × ask_type)` (`30` per model per chapter) are designed to expose macro-level convergence (`0 / 269`, `14 / 15`, `167.5 / 263`), not small percentage differences between labs.

---

## Citation & Licences

See [`CITATION.cff`](CITATION.cff) and [`LICENSE`](LICENSE):

> Liu, Haotian. *Still Ours? — Cross-Linguistic LLM Code-Painting Instrument and Worldview Archive.* 2026. DOI: [10.5281/zenodo.24357516](https://doi.org/10.5281/zenodo.24357516). https://stillours.art

- **Instrument & CLI code (`still_ours/`, `protocols/`)**: **MIT** ([`LICENSE`](LICENSE)).
- **Dataset tables, prompts, statements, model sketches & rendered paintings**: **CC BY 4.0**.
- **Curated audio-visual exhibition at [stillours.art](https://stillours.art)** (not in this repository): **CC BY-NC-ND 4.0**.
- **`still_ours/vendor/p5-1.11.13.min.js`**: p5.js under LGPL-2.1.

Model and company names identify the systems tested; no company endorses or is affiliated with this work.
