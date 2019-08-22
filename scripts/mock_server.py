import hashlib
import os
import pickle
from flask import Flask, request
from urllib.parse import urlsplit, quote, unquote
import requests


MOCK_SERVER_PORT = 8001
MOCK_SERVER = 'http://localhost:{port}'.format(port=MOCK_SERVER_PORT)

app = Flask(__name__)

this_path = os.path.split(os.path.abspath(__file__))[0]
cache_path = os.path.abspath(os.path.join(this_path, '..', 'cache'))
os.makedirs(cache_path, exist_ok=True)


def pack_url(url):
    scheme, rest = url.split('//')
    return os.path.join(quote(scheme), rest)


def unpack_url(url):
    scheme, *rest = url.split('/')
    return '{}//{}'.format(unquote(scheme), '/'.join(rest))


def get_cache_filename(cache_key):
    m = hashlib.md5()
    for k in cache_key:
        k = str(k).encode('utf-8')
        m.update(k)
    cache_hash = m.hexdigest()
    return os.path.join(cache_path, cache_hash)


def get_post_content(cache_filename, post_data):
    if not os.path.exists(cache_filename):
        split = urlsplit(request.url)
        orig_url = unpack_url(split.path[1:])
        resp = requests.post(orig_url, data=post_data)
        content = resp.content

        with open(cache_filename, 'wb') as f:
            pickle.dump(content, f)

    else:
        with open(cache_filename, 'rb') as f:
            content = pickle.load(f)

    return content


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def get_cached_remote(path):

    if request.data:  # POST
        cache_key = (path, request.data)
        cache_filename = get_cache_filename(cache_key)
        content = get_post_content(cache_filename, request.data)

    elif request.json:  # POST
        cache_key = (path, request.json)
        cache_filename = get_cache_filename(cache_key)
        content = get_post_content(cache_filename, request.json)

    elif request.form:  # POST
        cache_key = (path, request.form)
        cache_filename = get_cache_filename(cache_key)
        content = get_post_content(cache_filename, request.values)

    else:  # assume GET
        cache_key = (path, request.args)
        cache_filename = get_cache_filename(cache_key)

        print('here', cache_filename)
        if not os.path.exists(cache_filename):
            split = urlsplit(request.url)
            orig_url = unpack_url('{}?{}'.format(split.path[1:], split.query))
            resp = requests.get(orig_url)
            content = resp.content

            with open(cache_filename, 'wb') as f:
                pickle.dump(content, f)

        else:
            with open(cache_filename, 'rb') as f:
                content = pickle.load(f)

    return content


if __name__ == '__main__':
    app.run(port=MOCK_SERVER_PORT)
