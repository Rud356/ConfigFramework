import json

from config_framework import utils, loaders, Variable

loader_json = loaders.JsonString.load(
    '{"hello": "rud", "version": "42"}'
)

specific_deserializer = utils.LoaderSpecificDeserializer(
    {
        # * goes for any loader that didn't matched listed ones
        "*": lambda var, value: int(value),
        # And like this we specify transformation method for some loader
        loaders.JsonString: lambda var, value: int(value),
        # This can be helpful when you need some transformations to be done
        # if settings are stored in different ways for different loaders
    }
)
# The same thing goes for LoaderSpecificSerializer
specific_serializer = utils.LoaderSpecificSerializer(
    {
        "*": lambda var, value: json.dumps(value),
        loaders.JsonString: lambda var, value: json.dumps(value)
    }
)
# However this one is used when dumping data from loader

version_variable = Variable(loader_json, "version")
version_variable.register_deserializer(specific_deserializer)
version_variable.register_serializer(specific_serializer)
