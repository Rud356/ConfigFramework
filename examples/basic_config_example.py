from ConfigFramework import BaseConfig, loaders, variables

first_loader = loaders.JsonStringLoader.load('{"Is it simple?": true}', defaults={"useful?": "maybe", "pi": 2.74})
second_loader = loaders.JsonStringLoader.load('{"Is it simple?": false, "Var": "value"}')
composite_loader = loaders.CompositeLoader.load(first_loader, second_loader)


class Config(BaseConfig):
    is_simple = variables.BoolVar("Is it simple?", first_loader)
    is_useful = variables.ConfigVar("useful?", first_loader, validator=lambda v: v == "maybe")
    # You can set default values if they're not passing test in function
    # Write a function that returns True/False value or raises ValueError with explanation what's wrong
    # If default value fails check - it will also throw an error
    # but if it passes - it will be set
    pi = variables.FloatVar("pi", first_loader, default=3.14, constant=True, validator=lambda v: v == 3.14)

    class NestedConfig(BaseConfig):
        are_composite_loaders_simple = variables.BoolVar("Is it simple?", composite_loader)

        def __post_init__(self, *args, **kwargs):
            # As you may see here - the order of passed loaders matters when we have same keys in loaders
            # The order variables being looked up is going from left to right and it takes first value

            # Also __post_init__ of nested config takes same args as ones, that been passed to Config

            # Since nested configs will be initialized while main config inits - main config will be the last one to run
            # __post_init__. Keep that in mind
            print(
                "Is it simple to use composite loaders? "
                f"{'Yes' if self.are_composite_loaders_simple.value else 'No'}"
            )
            print("Nested config:", kwargs['phrase'])

    def __post_init__(self, *args, **kwargs):
        # Here you can write some code that will be ran after initialization of config class
        is_simple_to_str = 'simple' if self.is_simple.value else 'hard'
        print(f"ConfigFramework is {is_simple_to_str} and {self.is_useful.value} useful")
        print(f"Here's pi = {self.pi.value}")
        print("Main config:", kwargs['phrase'])


config = Config(phrase="Here's a way to pass variables")

# And here's example of constants
try:
    print("pi is constant:", config.pi.is_constant)
    config.pi.value = 2.22

except NotImplementedError:
    print("You can not set value to constants on runtime")
