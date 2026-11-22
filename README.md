# Video Scene Extractor

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Extract screenshots from training videos using scene detection and merge them into PDF.

[日本語版 README はこちら](README_ja.md)

## Features

- 🎬 **Automatic Scene Detection**: Detects scene changes in videos using PySceneDetect
- 📸 **Smart Screenshot Extraction**: Extracts frames only when significant changes occur
- 📄 **PDF Generation**: Merges extracted images into a single PDF document
- ⚙️ **Highly Configurable**: Flexible threshold and quality settings
- 🖥️ **Cross-Platform**: Works on Windows (native and WSL), macOS, and Linux
- 🚀 **CLI Interface**: Easy-to-use command-line interface

## Use Cases

- Extract slides from presentation videos
- Capture screen transitions from demo videos
- Create summaries of training videos
- Document video content as PDF

## Installation

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (recommended), or Python 3.10+ for a non-uv environment
- FFmpeg available on `PATH`

Install FFmpeg using the package manager for your platform. On Windows, install a native Windows build and make sure `ffmpeg.exe` is available in the Windows `PATH`; the WSL installation is separate.

### Install the project

Clone the repository, change into its directory, and sync the project environment:

```sh
git clone https://github.com/yourusername/video-scene-extractor.git
cd video-scene-extractor
uv sync
```

This creates `.venv`, installs the project and its dependencies, and installs the development tools in the `dev` group. Keep separate environments for WSL and native Windows; do not share virtual environments between them.

When both systems use the same Windows-backed checkout, use the WSL wrapper (it selects `.venv-wsl`) or, before direct uv commands, run:

```bash
export UV_PROJECT_ENVIRONMENT="$PWD/.venv-wsl"
```

### Using the same checkout from Windows and WSL

Python virtual environments are operating-system-specific. Do not use one `.venv` from both native Windows and WSL, even when both access the same checkout on the Windows filesystem. Use `.venv` for native Windows and `.venv-wsl` for WSL instead.

If both systems use `.venv`, `uv` can detect that the environment was created for a different platform. Depending on the command, uv version, and host platform, uv may recreate the environment or stop with an error rather than replacing it. This can make the next launch from the other system fail.

To avoid this issue, use the supplied wrappers: `video-scene-extractor.ps1` uses `.venv` on Windows, and `video-scene-extractor.sh` uses `.venv-wsl` when run in WSL. For direct WSL `uv` commands, set `UV_PROJECT_ENVIRONMENT` as shown above. Keep that variable in your WSL shell configuration if you use direct `uv` commands regularly.

To recover from an incompatible environment, remove only the environment for the system you are currently using, then let uv create it again:

**Windows PowerShell:**

```powershell
Remove-Item -Recurse -Force .venv
uv sync
```

**WSL:**

```bash
rm -rf .venv-wsl
UV_PROJECT_ENVIRONMENT=.venv-wsl uv sync
```

Do not remove the other system's environment unless you intend to rebuild it there as well.

When using an environment without `uv`, install the project and its dependencies into that interpreter first:

**Windows PowerShell:**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

**Linux and macOS:**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

**WSL using the same Windows-backed checkout:**

```bash
python3 -m venv .venv-wsl
.venv-wsl/bin/python -m pip install -e .
```

## Quick Start

Use the wrapper for your platform; it selects the runtime automatically.

**Windows PowerShell:**

```powershell
.\video-scene-extractor.ps1 input_video.mp4
```

**Linux, macOS, and WSL:**

```bash
bash video-scene-extractor.sh input_video.mp4
```

The wrapper prefers `uv`, then a project `.venv` or `venv`, and finally a local Python 3.10+ interpreter. Without `uv`, dependencies must already be installed in the selected environment. In WSL, the wrapper uses `.venv-wsl` by default so it does not reuse a Windows `.venv` when both systems access the same checkout.

You can also invoke the CLI directly with `uv run video-scene-extractor ...`.

This will:
1. Detect scene changes in `input_video.mp4`
2. Extract screenshots at each scene change
3. Create `output.pdf` with all screenshots

### Specify Output File

```sh
uv run video-scene-extractor input_video.mp4 -o slides.pdf
```

### Adjust Detection Sensitivity

```sh
# Higher threshold = detect only major changes (recommended for slides)
uv run video-scene-extractor input_video.mp4 -t 25.0

# Lower threshold = detect more subtle changes (for demos)
uv run video-scene-extractor input_video.mp4 -t 10.0
```

### Keep Extracted Images

```sh
uv run video-scene-extractor input_video.mp4 --keep-images --output-dir ./frames
```

### Portrait PDF for Documents

```sh
uv run video-scene-extractor document.mp4 --orientation portrait --title "Documentation"
```

### Run Ruff

```sh
uv run ruff check .
```
## Command-Line Options

```
Usage: video-scene-extractor [OPTIONS] INPUT_VIDEO

Arguments:
  INPUT_VIDEO              Input video file path

Output Options:
  -o, --output PATH        Output PDF file path [default: output.pdf]
  --output-dir PATH        Image output directory [default: ./frames]
  --keep-images            Keep images after PDF generation

Scene Detection Options:
  -t, --threshold FLOAT    Scene detection threshold (0-100) [default: 17.0]
  --min-scene-len INT      Minimum scene length in frames [default: 15]
  --position TEXT          Frame extraction position (start/middle/end) [default: start]

Image Options:
  --format TEXT            Image format (jpg/png) [default: jpg]
  --quality INT            JPEG quality (1-100) [default: 95]
  --max-width INT          Maximum width in pixels
  --max-height INT         Maximum height in pixels

PDF Options:
  --page-size TEXT         Page size (A4/Letter) [default: A4]
  --orientation TEXT       Page orientation (portrait/landscape) [default: portrait]
  --no-timestamp           Hide timestamp on images
  --title TEXT             PDF title

Other Options:
  --config PATH            Configuration file path
  --verbose, -v            Verbose output
  --version                Show version
  --help                   Show help message
```

## Configuration File

You can use a YAML configuration file for persistent settings. This is useful for maintaining consistent settings across multiple runs.

### Creating a Configuration File

1. Copy the template file:
```bash
cp config.yaml.template config.yaml
```

2. Edit `config.yaml` with your preferred settings:
```yaml
# config.yaml
detection:
  threshold: 17.0        # Scene detection sensitivity
  min_scene_len: 15      # Minimum scene length in frames
  position: start        # Frame extraction position (start/middle/end)

image:
  format: jpg            # Image format (jpg/png)
  quality: 95            # JPEG quality (1-100)
  max_width: 1920        # Maximum width (null = keep original)
  max_height: 1080       # Maximum height (null = keep original)

pdf:
  page_size: A4          # Page size (A4/Letter/A3/Legal)
  orientation: landscape # Page orientation (portrait/landscape)
  add_timestamp: true    # Add timestamp to images
  title: null            # PDF title (null = use video filename)

output:
  output_dir: ./frames   # Directory for extracted images
  keep_images: false     # Keep images after PDF generation
  verbose: false         # Enable verbose logging
```

3. Use the configuration file:
```bash
video-scene-extractor input_video.mp4 --config config.yaml
```

**Note:** `config.yaml` is git-ignored to keep your settings private. Only the template file is tracked in the repository.

### Configuration Examples

The `examples/` directory contains pre-configured settings for common use cases:

**For Presentation Slides** (`examples/config_slides.yaml`):
- Higher threshold (20.0) for slide transitions
- PNG format for better quality
- Landscape orientation

**For Demo Videos** (`examples/config_demo.yaml`):
- Lower threshold (12.0) for subtle changes
- JPEG format for smaller file size
- Landscape orientation for wide screen demos

Use example configurations:
```bash
video-scene-extractor input_video.mp4 --config examples/config_slides.yaml
```

### CLI Arguments Override Config File

Command-line arguments always take precedence over configuration file settings:
```bash
# Uses config.yaml but overrides threshold
video-scene-extractor input_video.mp4 --config config.yaml -t 25.0
```

## Threshold Tuning Guide

The `threshold` parameter controls scene detection sensitivity:

| Video Type | Recommended Threshold | Description |
|------------|----------------------|-------------|
| Presentation Slides | 15-25 | Detects slide transitions |
| Demo Videos | 10-15 | Detects screen changes |
| Mixed Content | 17 (default) | Balanced detection |
| Subtle Changes | 5-10 | More sensitive |

**Tips:**
- Start with the default (17.0) and adjust based on results
- Higher values = fewer, more significant scenes
- Lower values = more scenes, including subtle changes
- Test with a short video clip first

## Examples

### Extract Slides from Training Video

```bash
video-scene-extractor training.mp4 \
  -o training_slides.pdf \
  -t 20.0 \
  --orientation landscape \
  --title "Training Materials"
```

### Capture Demo Screenshots

```bash
video-scene-extractor demo.mp4 \
  -o demo_screenshots.pdf \
  -t 12.0 \
  --keep-images \
  --output-dir ./demo_frames
```

### High-Quality PNG Export

```bash
video-scene-extractor presentation.mp4 \
  --format png \
  --quality 100 \
  --max-width 1920 \
  --max-height 1080
```

## Acknowledgments

- [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) - Scene detection engine
- [FFmpeg](https://ffmpeg.org/) - Video processing
- [Pillow](https://python-pillow.org/) - Image processing
- [img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf) - PDF generation

## Troubleshooting

### FFmpeg Not Found

```bash
# Check if FFmpeg is installed
ffmpeg -version

# If not installed, refer to the installation instructions above
```

### Out of Memory Errors

When processing large videos, try these options:

```bash
# Limit image size
video-scene-extractor large_video.mp4 --max-width 1280 --max-height 720

# Increase threshold to reduce number of extracted frames
video-scene-extractor large_video.mp4 -t 25.0
```

### Too Many/Too Few Extracted Frames

Adjust the threshold:

```bash
# Too many frames - increase threshold
video-scene-extractor video.mp4 -t 25.0

# Too few frames - decrease threshold
video-scene-extractor video.mp4 -t 10.0
```

## FAQ

**Q: What video formats are supported?**

A: All formats supported by FFmpeg (MP4, AVI, MOV, MKV, etc.).

**Q: How long does processing take?**

A: Depends on video length and resolution. Typically 5-10 minutes for a 1-hour video.


---
