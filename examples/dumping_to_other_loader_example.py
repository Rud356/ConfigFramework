from ConfigFramework.loaders import JsonLoader, YAMLLoader

# Init loaders
yaml_loader = YAMLLoader.load(..., defaults={"Another example": "here"})
json_loader = JsonLoader.load(..., defaults={"key": "value"})

# That is how you can dump some data from one loader to another, if they're compatible.
# That means that json and yaml are pretty similar and types from python can be easily converted from one to another,
#  but EnvLoader won't be able to dump data because it requires too many effort to cast all variables to proper types
#  and yet won't be able to dump lists. Read docs for specific loaders dumper before using.

# Also you should keep in mind that include defaults parameter also specifies if default values defined and you want
#  them to appear in dumped config
yaml_loader.dump_to(json_loader, include_defaults=True)
