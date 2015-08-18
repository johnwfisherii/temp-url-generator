import hashlib, zlib, pickle, urllib

my_secret = "####"

def encode_data(data):
    text = zlib.compress(pickle.dumps(data, 0)).encode('base64').replace('\n', '')
    m = hashlib.md5(my_secret + text).hexdigest()[:12]
    return m, text

def decode_data(hash, enc):
    text = urllib.unquote(enc)
    m = hashlib.md5(my_secret + text).hexdigest()[:12]
    if m != hash:
        raise Exception("Bad Hash")
    data = pickle.loads(zlib.decompress(text.decode('base64')))
    return data