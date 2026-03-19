import os
import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find st.markdown(...)
    # We want to find ones that don't have unsafe_allow_html=True
    # and add it.

    # Find: st.markdown("""<html code>""")
    # Replace: st.markdown("""<html code>""", unsafe_allow_html=True)
    
    # We can do this roughly:
    # Match st.markdown( then any content until closing )
    # If the content doesn't contain unsafe_allow_html, and contains <div or <span or <style or <h1 or <h2 or <h3 or <p, add it.

    new_content = ""
    idx = 0
    pattern = re.compile(r'st\.markdown\s*\(')

    while True:
        match = pattern.search(content, idx)
        if not match:
            new_content += content[idx:]
            break
        
        start = match.end()
        # Find matching parenthesis
        paren_count = 1
        end = start
        in_string = False
        string_char = None
        in_triple_string = False

        while end < len(content) and paren_count > 0:
            char = content[end]
            if char == '\\':
                end += 2
                continue

            if not in_string:
                if char in ("'", '"'):
                    in_string = True
                    string_char = char
                    if content[end:end+3] == char*3:
                        in_triple_string = True
                        end += 3
                        continue
                elif char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
            else:
                if in_triple_string and content[end:end+3] == string_char*3:
                    in_string = False
                    in_triple_string = False
                    end += 2
                elif not in_triple_string and char == string_char:
                    in_string = False

            end += 1

        if paren_count == 0:
            arg_content = content[start:end-1]
            if ('unsafe_allow_html' not in arg_content) and ('<' in arg_content and '>' in arg_content):
                # We should add it
                modified_arg = arg_content + ", unsafe_allow_html=True"
                new_content += content[idx:match.start()] + "st.markdown(" + modified_arg + ")"
            else:
                new_content += content[idx:end]
            idx = end
        else:
            new_content += content[idx:end]
            idx = end

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Patched {filepath}")

if __name__ == "__main__":
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and file != 'test_st.py' and file != 'patch_st.py':
                patch_file(os.path.join(root, file))
