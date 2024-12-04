from datetime import datetime

from helpers import load_config
from aoc import get_leaderboard, get_url
from formatting import build_leaderboard_table, build_solve_table
from rich.console import Console
from slack_sdk.webhook import WebhookClient


def main():
  leaderboard = get_leaderboard(config.aoc)
  ts = datetime.now()
  console.print(f'Leaderboard fetched at {ts} for {config.aoc.year} day {ts.day}')

  post_leaderboard(leaderboard, ts)
  post_solves(leaderboard, ts)


def post_leaderboard(leaderboard, ts):
  max_players = 25
  leaderboard_table, player_count = build_leaderboard_table(leaderboard, max_players=max_players)
  max_players = min(max_players, player_count)
  response = post_message(
    f'Leaderboard {config.aoc.year}: Top {max_players} as of {ts.strftime('%H:%M:%S')} - {get_url(config.aoc, json=False)}',
    [leaderboard_table]
  )
  console.print(f'Posted leaderboard to Slack at {datetime.now()}')


def post_solves(leaderboard, ts):
  solve_table, solve_count = build_solve_table(leaderboard, ts.day, only_new=config.aoc.only_new_solves)
  if solve_count == 0:
    console.print(f'No solves to post')
  else:
    response = post_message(
      f'Day {ts.day} solve times as of {ts.strftime('%H:%M:%S')}',
      [solve_table]
    )
    console.print(f'Posted {solve_count} solves to Slack at {datetime.now()}')


def post_message(text = None, attachments = None):
  body = {
    'username': 'Advent of Code',
    'icon_url': config.slack.icon_url
  }

  if text is not None:
    body['text'] = text
  if attachments is not None:
    for a in attachments:
      console.print(a)
    body['attachments'] = [{ 'text': f'```{a}```' } for a in attachments]
  if config.slack.disable:
    return
  return slack_client.send_dict(body)


if __name__ == '__main__':
  config = load_config()
  console = Console()
  slack_client = WebhookClient(config.slack.webhook_url)
  main()
