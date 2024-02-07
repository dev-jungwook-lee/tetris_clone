import yaml
from munch import DefaultMunch


def get_cfg(cfg_path):
    with open(cfg_path, 'r') as file:
        configs = yaml.safe_load(file)
    return DefaultMunch.fromDict(configs)
