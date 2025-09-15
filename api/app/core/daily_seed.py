import hashlib

def target_index_for(date_str: str, salt: str, corpus_size: int) -> int:
    h = hashlib.sha256((salt + date_str).encode('utf-8')).hexdigest()
    n = int(h, 16)
    return n % corpus_size
