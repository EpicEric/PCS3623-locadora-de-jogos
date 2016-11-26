import json
import os

_config = None


def load(app):
    global _config
    path = os.path.join(app.root_path, 'config.json')
    if os.path.isfile(path):
        with open(path) as f:
            _config = json.load(f)


def get(key):
    if _config and key in _config:
        return _config[key]
    value = os.environ.get('BOARD_STORE_CONFIG_{}'.format(key))
    if value is not None:
        return value
    raise RuntimeError('Config key not found: {}'.format(key))
