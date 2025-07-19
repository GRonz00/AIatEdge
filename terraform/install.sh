#!/usr/bin/env bash

set -eou pipefail

curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME"/.local/bin/env
mkdir project
pushd project
uv venv --seed
source .venv/bin/activate
uv pip install vllm --torch-backend=auto