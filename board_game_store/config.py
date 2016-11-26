import json
import os

_config = None


def load(app):
    global _config
    with open(os.path.join(app.root_path, 'config.json')) as f:
        _config = json.load(f)


def get(key):
    return _config[key]
