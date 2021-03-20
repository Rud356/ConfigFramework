from ConfigFramework import variables, loaders, DumpCaster

# This is example of how you can get to some value underneath of other dictionaries, that been loaded from config
variable = variables.ConfigVar("some/path/to/nested/value", ...)


def caster(value):
    # Here you can do whatever you wish with your variable and return required type that will be used in code
    return str(value)


def dump_caster(config_var: variables.ConfigVar):
    # Here you can do whatever you need to save this variable in a way it will be easier to load for you
    return int(config_var.value)


# This will help you with choosing correct way to cast variable, depending on where it was loaded from
advanced_dump_caster = DumpCaster({
    loaders.JsonLoader: dump_caster,  # Setting dump function for specific loader
    '*': str  # Default dump_caster function for loaders that aren't listed here
})

casted_variable = variables.ConfigVar("variable", ..., caster=caster, dump_caster=advanced_dump_caster)
