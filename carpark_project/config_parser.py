import tomli


def parse_config():
    with open("config.toml", "r") as file:
        config_string = file.read()
    config = tomli.loads(config_string)
    return config
