import re

def normalize_word(s: str) -> str:
    s = s.strip().lower()
    if not re.fullmatch(r'[a-z]+', s):
        return ''
    return s
