from ConfigFramework import ConfigVariable, JSONStringConfigLoader, CompositeConfigLoader, BaseConfig


config_loader_1 = JSONStringConfigLoader('{"a": "world"}')
config_loader_2 = JSONStringConfigLoader('{"pretty simple": true}')
combined_loader = CompositeConfigLoader.load(config_loader_1, config_loader_2)


class Config(BaseConfig):
    hello = ConfigVariable.variable("a", combined_loader)
    is_it_simple = ConfigVariable.variable("pretty simple", combined_loader)

    def __post_init__(self, *args, **kwargs):
        print("Hello", self.hello)
        print("Is it simple? ", self.is_it_simple)

    def change_values(self):
        self.hello.value = "WORLD"
        # We won't see any output because of not having return
        # And this data isn't dumped to file, but you may try it yourself!

        self.hello.loader.dump()


conf = Config()
