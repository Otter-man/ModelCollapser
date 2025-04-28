# ModelCollapser

This script uses OpenAI’s `gpt-image-1` model to perform iterative image edits: it takes a base image and a text prompt, generates a new image, then uses that output as the next input, repeating for _N_ iterations.  
Usually it leads to model collapse.

---

## 🚀 Features

- **Iterative edits**: produce a chain of variants by feeding each output back as input.
- **Auto-retry**: optional `--retries` flag to automatically retry failed API calls. Useful for when image or prompt is not passing consistently OpenAI filters - this sometimes happen, and image is generated only after some retries.
- **Verbose output**: prints progress and file paths as it runs.
- **Unique output folders**: each run creates a new UUID-named directory to avoid collisions.

---

## 📋 Prerequisites

- Python 3.7+
- OpenAI Python package

Install dependencies:

```bash
pip install openai
```

---

## 🔧 Setup

1. **Clone or download** this repository, and ensure `main.py` is in your working dir.
2. **Set your API key**:

   ```bash
   export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
   ```


---

## ⚙️ Usage

```bash
python main.py \
  --image <base_image_path> \
  --prompt "Your descriptive prompt here" \
  --n <iterations> \
  [--retries <X>]
```

- `--image` (`-i`): path to your starting image file (PNG/JPG/WebP).
- `--prompt` (`-p`): text prompt guiding the edits.
- `--n` (`-n`): number of iterations (chain length).
- `--retries` (`-r`, optional): automatic retry count on failure. If omitted, script will prompt you interactively.

### Example

```bash
python main.py --image photo.jpg --prompt "Add a subtle watercolor effect" --n 5 --retries 3
```

Outputs will appear in a newly created folder named like `f47ac10b-58cc-4372-a567-0e02b2c3d479/` with files `1.png`, `2.png`, ..., `5.png`.

---

## 🔄 Customization Points

In `main.py`, you can tweak these parameters directly:

| Parameter         | Default         | Description                                                                                      |
|-------------------|-----------------|--------------------------------------------------------------------------------------------------|
| **QUALITY**       | `medium`        | Image quality level (`low`, `medium`, `high` or `auto`).                                         |
| **SIZE**          | `1024x1024`     | Output resolution. Options: `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), `auto` |
| **RETRIES**       | `None`          | Set default retry count; passing `--retries` overrides this.                                     |

To change, locate the `client.images.edit(...)` call and modify the parameters accordingly.

---

## ⚠️ Notes

- The script expects your `OPENAI_API_KEY` in the environment. No hard-coded keys.
- If an iteration fails and retries are exhausted (or you choose not to retry), the chain stops early and returns whatever was generated up to that point.

---

## 📄 License

MIT
