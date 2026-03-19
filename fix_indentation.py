"""
fix_indentation.py
------------------
Fixes the Streamlit HTML-as-code-block rendering bug.

Root cause: Streamlit's Markdown parser treats lines with 4+ leading spaces
as code blocks, even inside st.markdown(..., unsafe_allow_html=True).
Since our HTML strings are indented inside Python functions, the tags get
rendered as raw code rather than actual HTML.

Fix: For every st.markdown("""...""") call that contains HTML, we
re-write the string so each line starts at column 0 (dedented).
"""

import os
import re
import textwrap

TARGET_DIRS = [
    r"d:\proof_of_reality\pages",
    r"d:\proof_of_reality\auth",
    r"d:\proof_of_reality\utils",
    r"d:\proof_of_reality",   # includes app.py
]

SKIP_FILES = {"fix_indentation.py", "patch_st.py", "test_st.py",
              "test_patch.py", "test_patch_2.py"}


def needs_dedent(s: str) -> bool:
    """Return True if any line is indented >= 4 spaces (Markdown code-block threshold)."""
    for line in s.splitlines():
        if line and line[0] in (' ', '\t'):
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            if indent >= 4:
                return True
    return False


def fix_file(path: str) -> bool:
    with open(path, 'r', encoding='utf-8') as fh:
        original = fh.read()

    result = []
    pos = 0
    changed = False

    # Match:  st.markdown("""  or  st.markdown('''
    # We deliberately look for triple-quoted strings only — they're the ones
    # containing multi-line HTML.
    call_re = re.compile(r'st\.markdown\s*\(')

    while pos < len(original):
        m = call_re.search(original, pos)
        if not m:
            result.append(original[pos:])
            break

        # Emit everything before the call
        result.append(original[pos:m.start()])

        # Now walk the argument list manually to find the opening quote
        arg_start = m.end()           # just after the '('
        i = arg_start

        # Skip optional whitespace/newline before the string
        while i < len(original) and original[i] in ' \t\r\n':
            i += 1

        # Detect triple-quoted string
        if original[i:i+3] in ('"""', "'''"):
            quote = original[i:i+3]
            str_start = i + 3          # content starts here
            str_end = original.find(quote, str_start)
            if str_end == -1:
                # Malformed — just emit as-is
                result.append(original[m.start():])
                pos = len(original)
                break

            raw_content = original[str_start:str_end]

            # Only touch it if it has HTML-looking content
            has_html = '<' in raw_content and '>' in raw_content

            if has_html and needs_dedent(raw_content):
                fixed = textwrap.dedent(raw_content)
                # Rebuild the call so the string starts at column 0
                # (no leading spaces before the opening quote either)
                result.append(
                    'm.group()'.replace('m.group()', original[m.start():m.end()])   # "st.markdown("
                )
                result.append(quote + fixed + quote)
                # Now emit the rest of the argument list as-is (unsafe_allow_html etc)
                pos = str_end + 3
                changed = True
            else:
                # Nothing to fix — emit up to and including rest of string
                result.append(original[m.start(): str_end + 3])
                pos = str_end + 3

        else:
            # Single-quoted or f-string or variable — not our concern, emit as-is
            result.append(original[m.start():m.end()])
            pos = m.end()

    new_src = ''.join(result)
    if changed and new_src != original:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new_src)
        print(f"  ✔ Fixed: {path}")
        return True
    return False


def main():
    total = 0
    for d in TARGET_DIRS:
        if not os.path.isdir(d):
            continue
        for fname in os.listdir(d):
            if not fname.endswith('.py'):
                continue
            if fname in SKIP_FILES:
                continue
            fpath = os.path.join(d, fname)
            if os.path.isfile(fpath):
                if fix_file(fpath):
                    total += 1

    print(f"\nDone. {total} file(s) patched.")


if __name__ == "__main__":
    main()
