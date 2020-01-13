# -*- coding: utf-8 -*-

import json
from configirl import read_text, strip_comments
from config import Config

config = Config()

if config.is_ci_runtime():
    pass
else:
    config_data = dict()
    config_shared_data = json.loads(strip_comments(read_text("01-config-shared.json")))
    config_raw_data = json.loads(strip_comments(read_text("config-raw.json")))
    config_data.update(config_shared_data)
    config_data.update(config_raw_data)
    config.update(config_data)
