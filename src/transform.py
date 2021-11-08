import hashlib
def shorten(full_url: str):
    md5_url_hash = hashlib.md5(full_url.encode('utf-8'))
    md5_url = md5_url_hash.hexdigest()[0:7]
    return md5_url