#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$script_dir/check-no-local-paths.sh"
node "$script_dir/check-aeon-sources.mjs"
python3 "$script_dir/check-aeon-abnf.py" --metadata-only
