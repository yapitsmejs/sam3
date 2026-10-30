# sam3Toolkit

Utilities for running Segment Anything 3 (SAM3) segmentation.

> **Status:** experimentation phase. `notebooks/sam3Playground.ipynb` is the scratchpad
> for exploring SAM3; the `sam3Toolkit` package itself is still an empty skeleton.

## Install

This project is managed with [`uv`](https://docs.astral.sh/uv/) on Python 3.12.

```bash
uv sync --extra dev          # package + dev tools only (what CI uses; no torch)
uv sync --all-extras         # + SAM3 stack (CUDA 12.8 PyTorch) + Jupyter
```

Extras:

| Extra      | Contents                                                                 |
| ---------- | ------------------------------------------------------------------------ |
| `sam3`     | `sam3` (pinned upstream commit), `torch` 2.10 / `torchvision` 0.25 from the cu128 index, `triton-windows` on Windows |
| `notebook` | JupyterLab, ipykernel, and the libraries `sam3.visualization_utils` needs |
| `dev`      | pytest, ruff, mypy                                                       |

### SAM3 checkpoint access

The weights on Hugging Face are gated:

1. Request access at <https://huggingface.co/facebook/sam3> (manual approval).
2. `uv run hf auth login` with a *read* token.

The first model load downloads the checkpoint (~3.5 GB) into the Hugging Face cache.

### Environment notes

- **CUDA 12.8 wheels** are required for Blackwell GPUs (sm_120); `pyproject.toml`
  routes `torch`/`torchvision` to the PyTorch cu128 index (except on macOS).
- **`sam3` is installed from a pinned upstream commit**, not PyPI: the PyPI 0.1.4 wheel
  is missing the tokenizer's BPE vocab file. Bump the commit in `[tool.uv.sources]`.
- **Windows:** `sam3` imports `triton` unconditionally, so the `triton-windows` wheel is
  used instead of upstream triton.
- **Corporate TLS inspection:** `huggingface_hub` uses certifi, which doesn't trust the
  corporate CA. Call `truststore.inject_into_ssl()` before downloading (the notebook does).

## Usage

Open `notebooks/sam3Playground.ipynb` with the `.venv` kernel (VS Code), or
`uv run jupyter lab`. Put your own images in `data/` (git-ignored).

```python
from PIL import Image
from sam3 import build_sam3_image_model
from sam3.model.sam3_image_processor import Sam3Processor

processor = Sam3Processor(build_sam3_image_model())
state = processor.set_image(Image.open("data/myImage.jpg").convert("RGB"))
state = processor.set_text_prompt(state=state, prompt="car")
masks, boxes, scores = state["masks"], state["boxes"], state["scores"]
```

## Development

```bash
uv run pytest                 # run tests (dev loop, no coverage gate)
uv run ruff check .           # lint
uv run ruff format .          # format
uv run mypy src/sam3Toolkit     # type check
uv run python scripts/check.py   # GATE: lint + format + types + tests + branch coverage ≥ 90%
```

Run `scripts/check.py` before pushing or opening a PR — it fails if ruff is
unhappy, formatting would change, **mypy** finds a type error, or branch coverage
on the package drops below 90%. See [`CONVENTIONS.md`](CONVENTIONS.md) for the
full naming, code-style, and test-driven conventions.

### Automation

These run the same gate as you do locally, so a red PR cannot merge:

- **CI** (`.github/workflows/ci.yml`) runs `scripts/check.py` on every push and PR.
- **Git hooks** (`.githooks/`) are opt-in per clone — fast `ruff` checks on
  commit, the full gate on push. One-time setup:
  ```bash
  git config core.hooksPath .githooks
  git update-index --chmod=+x .githooks/pre-commit .githooks/pre-push
  ```
  Use `git commit --no-verify` during active red-phase work; the pre-push hook
  and CI still enforce before anything lands.
- **Dependabot** (`.github/dependabot.yml`) opens weekly dependency PRs (uv +
  GitHub Actions) that must pass the gate like any other.
- **PR template** (`.github/PULL_REQUEST_TEMPLATE.md`) prompts contributors for
  the red-green workflow and the gate checklist.

## Finishing project setup

This repo was created from a template whose setup was done partially: the package is
renamed to `sam3Toolkit` and the SAM3 dependencies are in place, but the project intake,
full README, and `plans/developmentPlan.md` were deferred until after experimenting.
When you're ready to design the package, ask your agent to:

```
Finish setting up this project. Read `agenticProjectSetup.md`: skip the rename and
dependency steps (already done), run the intake questions with me, then write the
README and plans/developmentPlan.md, delete the example files and
`agenticProjectSetup.md`, run the placeholder sweep, and run the gate.
```
