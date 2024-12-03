import json, os
from pathlib import Path
from types import SimpleNamespace
from datetime import date

PROJECT_ROOT = Path('../')
CONFIG_FILE = PROJECT_ROOT / 'config.json'
EXAMPLE_CONFIG_FILE = PROJECT_ROOT / 'config.example.json'


class NestedNamespace(SimpleNamespace):
  def __init__(self, dictionary, **kwargs):
    super().__init__(**kwargs)
    for key, value in dictionary.items():
      self.__setattr__(key, self.__get_entry__(value))

  def __getattr__(self, key):
    return None

  def __get_entry__(self, value):
    if isinstance(value, dict):
      return NestedNamespace(value)
    elif isinstance(value, list):
      return [self.__get_entry__(item) for item in value]
    else:
      return value

  def to_dict(self):
    return self.__dict__


def override_with_environment(e_d, d, prefix=[]):
  for key, value in e_d.items():
    if key not in d:
      d[key] = None
    full_key = '_'.join(prefix + [key]) if prefix else key
    if isinstance(value, dict):
      override_with_environment(value, d[key], prefix + [key])
    else:
      env = get_env(full_key)
      if env is not None:
        d[key] = env


def get_env(key):
  if key in os.environ:
    return os.environ[key]
  elif key.upper() in os.environ:
    return os.environ[key.upper()]
  return None


def load_config():
  with EXAMPLE_CONFIG_FILE.open('r') as config_file:
    example_config = json.load(config_file)
  with CONFIG_FILE.open('r') as config_file:
    config = json.load(config_file)
    override_with_environment(example_config, config)
  if config['aoc']['year'] == None:
    config['aoc']['year'] = date.today().year
  return NestedNamespace(config)
