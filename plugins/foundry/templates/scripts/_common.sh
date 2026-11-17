# Sourced by the other scripts. CODE = this code's folder (foundry/<code>), ROOT = project root.
CODE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="$(cd "$CODE/../.." && pwd)"
# Main-code root: the original project, or a copy given by FOUNDRY_SRC (used by mutate).
SRC_ROOT="${FOUNDRY_SRC:-$ROOT}"
# Main-code paths from foundry.json, relative to the project root.
SOURCES=$(python3 -c 'import json,sys; c=json.load(open(sys.argv[1])); s=c.get("source") or []; print(" ".join([s] if isinstance(s,str) else s))' "$CODE/foundry.json")
