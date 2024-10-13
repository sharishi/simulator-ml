import yaml


def parse_to_dict(config_text: str) -> dict:
    """Convert yaml to dict"""
    try:
        config_dict = yaml.safe_load(config_text)
    except yaml.YAMLError as e:
        raise ValueError(f"Ошибка парсинга YAML: {e}")
    return config_dict


def parse_config(config_file: dict, prefix="") -> str:
    """Parse dict"""
    result = ""
    for key, val in config_file.items():
        new_prefix = prefix + key
        if isinstance(val, dict):
            result += parse_config(val, new_prefix + '.')
        else:
            result += f"{new_prefix}={val}\n"
    return result


def yaml_to_env(config_file: str) -> str:
    """Main function"""
    config_dict = parse_to_dict(config_file)
    result = parse_config(config_dict)

    return result


def is_integer(value: str) -> bool:
    """Check if value is an integer"""
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value: str) -> bool:
    """Check if value is a float"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def convert_value(value: str):
    """Convert value"""
    if is_integer(value):
        return int(value)
    elif is_float(value):
        return float(value)
    elif value.lower() in ['true', 'false']:
        return value.lower() == 'true'
    return value


def set_nested_dict(config_dict: dict, keys: list, value):
    """Fill thr dict"""
    for key in keys[:-1]:
        config_dict = config_dict.setdefault(key, {})
    config_dict[keys[-1]] = convert_value(value)


def env_to_dict(env_list: str) -> dict:
    """Parse the dict"""
    config_dict = dict()
    lines = env_list.strip().splitlines()

    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            keys = key.split('.')
            set_nested_dict(config_dict, keys, value)

    return config_dict


def dict_to_yaml(config_dict: dict) -> str:
    """Convert dict to yaml"""
    return yaml.dump(config_dict, sort_keys=True, default_flow_style=False)


def env_to_yaml(env_list: str) -> str:
    """Main env_to_yaml function"""
    config_dict = env_to_dict(env_list)
    return dict_to_yaml(config_dict)
