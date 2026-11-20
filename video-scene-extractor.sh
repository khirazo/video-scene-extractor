#!/usr/bin/env bash

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
IS_WSL=false
if grep -qi microsoft /proc/sys/kernel/osrelease 2>/dev/null; then
    IS_WSL=true
fi

if command -v uv >/dev/null 2>&1; then
    if [[ "$IS_WSL" == true && -z "${UV_PROJECT_ENVIRONMENT:-}" ]]; then
        export UV_PROJECT_ENVIRONMENT="$SCRIPT_DIR/.venv-wsl"
    fi
    exec uv run --project "$SCRIPT_DIR" video-scene-extractor "$@"
fi

PYTHON=""
if [[ "$IS_WSL" == true && -x "$SCRIPT_DIR/.venv-wsl/bin/python" ]]; then
    PYTHON="$SCRIPT_DIR/.venv-wsl/bin/python"
else
    for ENV_NAME in .venv venv; do
        if [[ -x "$SCRIPT_DIR/$ENV_NAME/bin/python" ]]; then
            PYTHON="$SCRIPT_DIR/$ENV_NAME/bin/python"
            break
        fi
    done
fi

if [[ -z "$PYTHON" ]]; then
    if command -v python3 >/dev/null 2>&1; then
        PYTHON="$(command -v python3)"
    elif command -v python >/dev/null 2>&1; then
        PYTHON="$(command -v python)"
    fi
fi

if [[ -z "$PYTHON" ]]; then
    echo "Error: uv or Python 3.10+ was not found." >&2
    exit 127
fi

if ! "$PYTHON" -c 'import sys; raise SystemExit(sys.version_info < (3, 10))'; then
    echo "Error: Python 3.10 or higher is required." >&2
    exit 1
fi

export PYTHONPATH="$SCRIPT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
exec "$PYTHON" -m video_scene_extractor "$@"