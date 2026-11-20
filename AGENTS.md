# Development Guide

## Local Supplement

At the start of work, read `AGENTS.local.md` in the repository root when it exists.
It supplements these instructions with machine-specific information and must not be committed.
Add shared procedures, design decisions, and dependency information to this `AGENTS.md` or another tracked document.

## Project Overview

- This is a Python CLI that extracts scene images from videos and generates a PDF.
- Package source is in `src/video_scene_extractor/`; the CLI entry point is `video-scene-extractor`.
- FFmpeg is required as an external command and must be available on the execution environment's `PATH`.
- The source uses Python 3.10 syntax. Keep the Python requirement in `pyproject.toml` aligned when changing compatibility.

## Dependencies and Execution

- `pyproject.toml` is the source of truth for Python dependencies. Commit `uv.lock` and keep it in sync with `pyproject.toml`.
- The standard commands are `uv sync`, `uv run video-scene-extractor --help`, `uv run ruff check .`, and the platform wrapper scripts.
- Support both WSL and native Windows. Do not share virtual environments between operating systems; create one per environment.
- The wrappers are `video-scene-extractor.ps1` for Windows PowerShell and `video-scene-extractor.sh` for Linux, macOS, and WSL. They prefer uv, then use an existing `.venv` or `venv`, then a local Python 3.10+ interpreter. On WSL, the shell wrapper defaults uv to `.venv-wsl` to avoid sharing the Windows `.venv`.

## Quality Checks

- Run `ruff check .` after changing Python code.
- Ruff configuration and its development dependency are defined in `pyproject.toml`. Assess the impact on existing code before changing its rules.
- There are currently no automated tests. For behavioral changes, at minimum verify `video-scene-extractor --help` and, when possible, generate a PDF from a short video.
- Do not commit generated PDFs, images, videos, or local configuration files.

## Change Guidelines

- Keep changes small and scoped to the requested task. Update the lockfile when adding or updating dependencies.
- Keep English and Japanese README setup instructions synchronized whenever either one changes.
- Put machine-specific paths, installation state, credentials, and personal settings only in `AGENTS.local.md`.
