from sphinx.ext import apidoc


def init_doc():
    config_framework_dir = '../ConfigFramework'
    apidoc.main([
        '-f', '-T', '-E', '-M',
        '-o', './source/',
        config_framework_dir,
    ])

init_doc()
