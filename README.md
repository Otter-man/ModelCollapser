# ModelCollapser

Iteratively edits an image with OpenAI’s `gpt-image-1`, feeding each result back as the next input. Optionally applies a yellow‑tint color correction between steps. Each run writes outputs into a fresh UUID directory.

## Quick Start

- Python 3.10+ recommended
- Install: `pip install openai` (add `opencv-python numpy` if using `--correct`)
- Set key: `export OPENAI_API_KEY=...`
- Run:

```bash
python main.py -i example.jpg -p "Your prompt" -n 3 [-r 2] [--correct]
```

## CLI

```bash
python main.py -i IMAGE -p PROMPT -n N [-r RETRIES] [--correct]
```
- `-i, --image`  base image path
- `-p, --prompt` text prompt
- `-n, --n`      iteration count
- `-r, --retries` auto‑retry on failure (otherwise prompts)
- `--correct`    save and use color‑corrected frames between steps

## Output

- Creates `<uuid>/generated/01.png, 02.png, ...`
- With `--correct` also writes `<uuid>/corrected/01.png, ...` and uses corrected frames for the next iteration

## Utilities

- `make_movies_from_stills.py`: turns PNG sequences (`01.png`, `02.png`, ...) into MP4s via ffmpeg in all subdirectories of the current workdir.
  Example: `python make_movies_from_stills.py`

## License

MIT
