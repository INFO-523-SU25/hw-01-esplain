# check_allowed_files.py
#!/usr/bin/env python3
import sys
import glob
import os
from pathlib import Path

ALLOWED_PATTERNS = sys.argv[1:]
TODO_PHRASE = "# TODO: Implement your solution here"
CONTEXT_LINES = 2              # lines shown before/after the match

# ---------------------------------------------------------------------
# 1. Verify allowed files exist (original behavior, but globbing recursive)
# ---------------------------------------------------------------------
found_files = []
for pattern in ALLOWED_PATTERNS:
    found_files.extend(glob.glob(pattern, recursive=True))

if not found_files:
    print("❌  Error: No allowed files found in the repository.")
    sys.exit(1)

print(f"✅  Allowed files found ({len(found_files)}):")
for f in sorted(found_files):
    print(f"   • {f}")

# ---------------------------------------------------------------------
# 2. Ensure at least one hw-*.ipynb notebook exists
# ---------------------------------------------------------------------
notebooks = glob.glob("hw-*.ipynb")
if not notebooks:
    print("❌  Error: No hw-*.ipynb file found.")
    sys.exit(1)

# ---------------------------------------------------------------------
# 3. Scan notebooks for TODOs and print context with line numbers
# ---------------------------------------------------------------------
def report_todo(nb_path: str) -> bool:
    """Return True if a TODO was found."""
    with open(nb_path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    hit = False
    for idx, line in enumerate(lines, start=1):
        if TODO_PHRASE in line:
            hit = True
            print(f"\n❌  TODO placeholder found in {nb_path} @ line {idx}:")
            # Show context lines before
            for i in range(max(0, idx - CONTEXT_LINES - 1), idx - 1):
                print(f"      {i+1:4d} | {lines[i].rstrip()}")
            # Highlight offending line
            print(f"   -->{idx:4d} | {line.rstrip()}")
            # Show context lines after
            for i in range(idx, min(len(lines), idx + CONTEXT_LINES)):
                print(f"      {i+1:4d} | {lines[i].rstrip()}")
    return hit

todo_found = False
for nb in notebooks:
    if report_todo(nb):
        todo_found = True

if todo_found:
    print("\n❌  One or more TODO placeholders detected — failing check.")
    sys.exit(1)

print("\n🎉  All notebook checks passed.")
