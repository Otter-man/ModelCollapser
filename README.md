# ModelCollapser

This script uses OpenAI's `gpt-image-1` model to perform iterative image edits: it takes a base image and a text prompt, generates a new image, then uses that output as the next input, repeating for _N_ iterations.  
Usually it leads to model collapse.

---

## 🚀 Features

- **Iterative edits**: produce a chain of variants by feeding each output back as input.
- **Auto-retry**: optional `--retries` flag to automatically retry failed API calls. Useful for when image or prompt is not passing consistently OpenAI filters - this sometimes happen, and image is generated only after some retries.
- **Verbose output**: prints progress and file paths as it runs.
- **Unique output folders**: each run creates a new UUID-named directory to avoid collisions.
- **Gradio Web UI**: run as a web app for easy image uploads and prompt entry.
- **Docker Support**: run the app in a containerized environment.

---

## 📋 Prerequisites

- Python 3.7+
- OpenAI Python package
- [Optional] Docker (for containerized usage)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔧 Setup

1. **Clone or download** this repository, and ensure `main.py` and `app.py` are in your working dir.
2. **Set your API key**:

   ```bash
   export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
   ```

---

## ⚙️ Usage

### Command Line

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

### Gradio Web App

You can use a web interface for uploading images and entering prompts:

```bash
python app.py
```

- The app will be available at [http://localhost:7860](http://localhost:7860) by default.
- To make it accessible on your network, it binds to `0.0.0.0:7860`.
- Make sure your `OPENAI_API_KEY` is set in your environment.

### Docker

Build and run the app in a container:

```bash
docker build --build-arg OPENAI_API_KEY=your-api-key-here -t modelcollapse .
docker run -p 7860:7860 modelcollapse
```

- The app will be available at [http://localhost:7860](http://localhost:7860)
- The API key is passed securely as a build argument and set as an environment variable in the container.

---

## 🔄 Customization Points

In `main.py`, you can tweak these parameters directly:

| Parameter         | Default         | Description                                                                                      |
|-------------------|-----------------|--------------------------------------------------------------------------------------------------|
| **QUALITY**       | `high`          | Image quality level (`low`, `medium`, `high` or `auto`).                                         |
| **SIZE**          | `1024x1024`     | Output resolution. Options: `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), `auto` |
| **RETRIES**       | `None`          | Set default retry count; passing `--retries` overrides this.                                     |

To change, locate the `client.images.edit(...)` call and modify the parameters accordingly.

---

## ⚠️ Notes

- The script expects your `OPENAI_API_KEY` in the environment. No hard-coded keys.
- If an iteration fails and retries are exhausted (or you choose not to retry), the chain stops early and returns whatever was generated up to that point.
- The Gradio app allows for easy testing and demoing in a browser.
- For Docker, always pass your API key securely as shown above.

---

## 📄 License

MIT
