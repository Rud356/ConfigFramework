from ConfigFramework import BaseConfig
from ConfigFramework.loaders import DictLoader
from ConfigFramework.variables import ConfigVar, IntVar
from ConfigFramework.custom_types import VariableType

loader = DictLoader.load({"a": 1, "b": 2.22})


class Config(BaseConfig):
    # Following method of type hinting is deprecated and will be deleted in 2.5.0
    a: VariableType[int] = IntVar("a", loader)
    # Since 2.2.0 it's recommended to use ConfigVar to type hint things
    b: ConfigVar[float] = ConfigVar("b", loader)


conf = Config()
# You will get float functions suggestions from IDE if you use it like that!
conf.b.value.as_integer_ratio()
