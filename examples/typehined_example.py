from ConfigFramework import BaseConfig
from ConfigFramework.loaders import DictLoader
from ConfigFramework.variables import ConfigVar
from ConfigFramework.custom_types import VariableType

loader = DictLoader.load({"a": 1, "b": 2.22})


class Config(BaseConfig):
    a: VariableType[int] = ConfigVar("a", loader)
    b: VariableType[float] = ConfigVar("b", loader)


conf = Config()
# You will get float functions suggestions from IDE if you use it like that!
conf.b.value.as_integer_ratio()
