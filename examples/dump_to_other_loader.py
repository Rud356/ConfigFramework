from pathlib import Path
from config_framework.loaders import Yaml, JsonString

with open("out.yaml", mode="w") as f:
    f.write("")

yaml = Yaml.load(Path("../out.yaml"))
json_loader = JsonString.load('{"key": 111}')
json_loader.dump_to(yaml)
