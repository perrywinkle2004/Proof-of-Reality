"""
fix_markdown_indent.py
----------------------
Fixes the Streamlit HTML-rendered-as-code-block bug across the entire project.

Root cause:
  Streamlit's Markdown renderer treats any line with 4+ leading spaces as a
  pre/code block, even inside st.markdown(..., unsafe_allow_html=True).
  Because all the HTML strings are inside Python functions (indented 4-8 spaces),
  every tag triggers the code-block rule.

Fix:
  For every st.markdown triple-quoted string that contains HTML we apply
  textwrap.dedent to the string literal in the SOURCE FILE so that
  the HTML starts at column 0, permanently, with no runtime patching needed.
"""

import os
import re
import textwrap

ROOT = r"d:\proof_of_reality"

# Directories to process (non-recursive here — all target .py files are immediate children)
TARGET_DIRS = [
    os.path.join(ROOT, "pages"),
    os.path.join(ROOT, "auth"),
    os.path.join(ROOT, "utils"),
    os.path.join(ROOT, "modules") if os.path.isdir(os.path.join(ROOT, "modules")) else None,
    os.path.join(ROOT, "analytics") if os.path.isdir(os.path.join(ROOT, "analytics")) else None,
    ROOT,   # app.py etc.
]

SKIP_FILES = {
    "fix_markdown_indent.py", "fix_indentation.py", "patch_st.py",
    "test_st.py", "test_patch.py", "test_patch_2.py",
}


# ---------------------------------------------------------------------------
# Tokeniser-style walk: find every st.markdown( call, extract its first
# argument (the string), dedent it, and write back.
# ---------------------------------------------------------------------------

CALL_RE = re.compile(r'\bst\.markdown\s*\(')


def dedent_html_string(raw: str) -> str:
    """Apply textwrap.dedent then strip a single leading newline if present."""
    fixed = textwrap.dedent(raw)
    # Remove a leading newline that Python adds when the triple-quote is
    # immediately followed by a newline in source. Keep trailing whitespace
    # intact so closing """ still sits on its own line.
    if fixed.startswith('\n'):
        fixed = fixed[1:]
    return fixed


def process_source(src: str) -> tuple[str, int]:
    """Return (new_source, number_of_changes)."""
    out = []
    pos = 0
    changes = 0

    while pos < len(src):
        m = CALL_RE.search(src, pos)
        if not m:
            out.append(src[pos:])
            break

        # Emit everything before "st.markdown("
        out.append(src[pos: m.end()])
        pos = m.end()

        # Skip whitespace between '(' and the string
        i = pos
        while i < len(src) and src[i] in ' \t\r\n':
            i += 1

        # Detect triple-quoted string (regular or f-string)
        is_fstring = False
        if i < len(src) and src[i] == 'f':
            is_fstring = True
            i += 1

        if i + 3 > len(src):
            out.append(src[pos:])
            pos = len(src)
            break

        triple = src[i: i + 3]
        if triple not in ('"""', "'''"):
            # Not a triple-quoted string — leave as-is
            out.append(src[pos: i])
            pos = i
            continue

        quote = triple
        str_body_start = i + 3
        str_body_end = src.find(quote, str_body_start)

        if str_body_end == -1:
            # Unclosed string — bail
            out.append(src[pos:])
            pos = len(src)
            break

        raw_body = src[str_body_start: str_body_end]

        # Only touch strings that contain HTML and have indented lines
        has_html = '<' in raw_body and '>' in raw_body
        max_indent = max(
            (len(line) - len(line.lstrip()) for line in raw_body.splitlines() if line.strip()),
            default=0
        )

        if has_html and max_indent >= 4:
            fixed_body = dedent_html_string(raw_body)
            # Re-assemble: emit the whitespace before the quote, then the string
            out.append(src[pos: i])          # whitespace gap (if any)
            if is_fstring:
                out.append('f')
            out.append(quote + fixed_body + quote)
            pos = str_body_end + 3
            changes += 1
        else:
            # Nothing to fix — emit as-is up to end of string
            out.append(src[pos: str_body_end + 3])
            pos = str_body_end + 3

    return ''.join(out), changes


def fix_file(path: str) -> bool:
    with open(path, 'r', encoding='utf-8') as fh:
        original = fh.read()

    new_src, changes = process_source(original)

    if changes > 0 and new_src != original:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new_src)
        print(f"  ✔ {path}  ({changes} string(s) fixed)")
        return True
    return False


def main():
    total_files = 0
    for d in TARGET_DIRS:
        if not d or not os.path.isdir(d):
            continue
        for fname in sorted(os.listdir(d)):
            if not fname.endswith('.py') or fname in SKIP_FILES:
                continue
            fpath = os.path.join(d, fname)
            if os.path.isfile(fpath):
                if fix_file(fpath):
                    total_files += 1

    print(f"\nDone — {total_files} file(s) patched.")


if __name__ == "__main__":
    main()
