import os, hashlib, tempfile, requests
from typing import List, Tuple

def download_file(url: str) -> str:
    """Download remote file to a temp path and return path."""
    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    suffix = os.path.splitext(url.split('?')[0])[-1] or '.pdf'
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, 'wb') as f:
        for chunk in r.iter_content(1024*1024):
            if chunk:
                f.write(chunk)
    return path

def compute_doc_hash(url: str) -> str:
    return hashlib.md5(url.encode('utf-8')).hexdigest()

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    """Yield text chunks roughly chunk_size words with overlap."""
    words = text.split()
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i+chunk_size])
        yield chunk
        i += chunk_size - overlap
