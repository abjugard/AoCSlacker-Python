from io import StringIO
from rich import box
from rich.console import Console
from rich.table import Table
from helpers import NestedNamespace

TABLE_WIDTH = 28


def build_leaderboard_table(leaderboard, max_players=25):
  players = leaderboard.players[:max_players]

  w = calculate_leaderboard_widths(players)
  use_global = w.g_score > 0
  use_change = w.change > 0
  spaces = 2 + int(use_global) + int(use_change)
  fixed = sum(w.to_dict().values()) + spaces
  name_width = TABLE_WIDTH - fixed

  table = Table(padding=(0, 0), collapse_padding=True, box=box.SIMPLE)
  table.add_column(justify='right', width=w.pos)
  if use_change:
    table.add_column(width=w.change)
  table.add_column('Name', width=name_width, no_wrap=True)
  table.add_column('📋', justify='right', width=w.score)
  if use_global:
    table.add_column(title='🌐', justify='right', width=w.g_score)

  for p in players:
    data = [str(p.position)]
    if use_change:
      data.append(p.change_icon)
    data.extend([p.name, str(p.score)])
    if use_global:
      data.append(str(p.global_score) or '-')
    table.add_row(*data)

  console = Console(file=StringIO(), record=True)
  console.print(table)
  return remove_border(console.export_text()), len(players)


def calculate_leaderboard_widths(players):
  max_pos = max_score = max_global = 0
  for p in players:
    max_pos = max(max_pos, p.position)
    max_score = max(max_score, p.score)
    max_global = max(max_global, p.global_score)

  return NestedNamespace({
    'pos': len(str(max_pos)),
    'change': int(any(p.change != 0 for p in players)),
    'score': len(str(max_score)),
    'g_score': len(str(max_global)) if max_global > 0 else 0
  })


def build_solve_table(leaderboard, day, only_new=False):
  solves = leaderboard.get_solves(day, only_new)
  if len(solves) == 0:
    return None, 0

  w = calculate_solve_widths(solves)
  fixed = sum(w.to_dict().values()) + 2 # spaces between columns
  name_width = TABLE_WIDTH - fixed

  table = Table(padding=(0, 0), box=box.SIMPLE)
  table.add_column('Time', width=w.time)
  table.add_column('Name', width=name_width, no_wrap=True)
  table.add_column('🏆', justify='right', width=w.score)

  for s in solves:
    table.add_row(s.solve_time_str, s.player, str(s.position))

  console = Console(file=StringIO(), record=True)
  console.print(table)
  return remove_border(console.export_text()), len(solves)


def remove_border(block):
  result = []

  for line in block.split('\n')[1:-2]:
    result.append(line[1:])

  return '\n'.join(result)


def calculate_solve_widths(solves):
  max_time = ''
  max_pos = 0
  for s in solves:
    max_time = max(max_time, s.solve_time_str)
    max_pos = max(max_pos, s.position)

  return NestedNamespace({
    'time': len(str(max_time)),
    'pos': max(len(str(max_pos)), 2)
  })

