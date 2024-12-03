import urllib.request, json
from helpers import PROJECT_ROOT
from leaderboard import Leaderboard

LEADERBOARD_URL = 'https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard_id}'
HISTORY_BASEDIR = PROJECT_ROOT / 'data'


def get_data_path(aoc_config):
  if not HISTORY_BASEDIR.exists():
    HISTORY_BASEDIR.mkdir()
  leaderbaord_history_dir = HISTORY_BASEDIR / str(aoc_config.year)
  if not leaderbaord_history_dir.exists():
    leaderbaord_history_dir.mkdir()
  return leaderbaord_history_dir / f'{aoc_config.leaderboard_id}.json'


def load_last(aoc_config):
  leaderboard_file = get_data_path(aoc_config)
  if leaderboard_file.exists():
    with leaderboard_file.open('r') as f:
      leaderboard_data = json.load(f)
      return Leaderboard(aoc_config, leaderboard_data)
  return None


def get_url(aoc_config, json=True):
  url = LEADERBOARD_URL.format(**aoc_config.to_dict())
  if json:
    url += '.json'
  return url


def get_leaderboard(aoc_config):
  last_leaderboard = load_last(aoc_config)

  request = urllib.request.Request(
    url=get_url(aoc_config), 
    headers={
      "Cookie": f'session={aoc_config.session}'
    }
  )

  with urllib.request.urlopen(request) as response:
    response_data = response.read().decode("utf-8")
    leaderboard = json.loads(response_data)

  leaderboard_file = get_data_path(aoc_config)
  with leaderboard_file.open('w',encoding='utf-8') as f:
    json.dump(leaderboard, f, indent=2, ensure_ascii=False)

  return Leaderboard(aoc_config, leaderboard, last_leaderboard)
