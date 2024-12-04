from helpers import NestedNamespace
from datetime import datetime

CHANGE_ICONS = ' ↑⇈⇊↓'


class Leaderboard(object):
  def __init__(self, aoc_config, leaderboard_dict, last=None):
    super(Leaderboard, self).__init__()
    self.base_data = l = NestedNamespace(leaderboard_dict)
    self.last = last

    self.year = int(l.event)
    self.owner = l.owner_id

    members = l.members.to_dict().values()
    members = sorted(members, key=lambda m: (-m.local_score, m.id))
    self.players = [Player(m, idx+1, last) for idx, m in enumerate(members) \
      if m.id not in aoc_config.excluded_members]

  def get_player(self, user_id):
    return next((m for m in self.players if m.user_id == user_id), None)

  def get_solves(self, day, only_new=False):
    all_solves = []
    for p in self.players:
      all_solves.extend(p.get_solves(day))

    for level in [1, 2]:
      solves = sorted(
        [s for s in all_solves if s.level == level],
        key=lambda s: s.solve_time
      )
      for idx, solve in enumerate(solves):
        solve.set_pos(idx + 1)

    if self.last is not None and only_new:
      last_solves = self.last.get_solves(day)
      all_solves = [s for s in all_solves if not s in last_solves]

    return sorted(all_solves, key=lambda s: s.solve_time)


class Player(object):
  def __init__(self, member, position, last):
    super(Player, self).__init__()
    self.user_id = member.id
    self.name = member.name
    self.position = position
    self.is_new = last is None
    if last is not None and (last_player := last.get_player(self.user_id)) is not None:
      self.change = last_player.position - position
    else:
      self.change = 0
    self.change_icon = CHANGE_ICONS[min(2, max(-2, self.change))].strip()
    self.score = member.local_score
    self.global_score = member.global_score
    self.raw_solves = member.completion_day_level.to_dict()

  def __str__(self):
    s = f'{self.name} in position {self.position} has {self.score} points '
    if self.global_score > 0:
      s += f'(and {self.global_score} global!)'
    return s
    
  def get_solves(self, day):
    chal_key = str(day)
    solves = []
    if chal_key in self.raw_solves:
      raw = self.raw_solves[chal_key].to_dict()
      for idx in "12":
        if idx in raw:
          solve = Solve(self.name, day, int(idx), raw[idx])
          solves.append(solve)
    return solves


class Solve(object):
  def __init__(self, player, day, level, raw_star):
    super(Solve, self).__init__()
    self.player = player
    self.day = day
    self.level = level
    self.solve_time = raw_star.get_star_ts
    dt = datetime.fromtimestamp(raw_star.get_star_ts)
    plus_days = dt.day - day
    self.solve_time_str = dt.strftime('%H:%M:%S')
    if plus_days > 0:
      self.solve_time_str += f'+{plus_days}'
    self.position = None

  def __eq__(self, other):
    return self.player == other.player \
      and self.level == other.level \
      and self.solve_time == other.solve_time

  def __str__(self):
    s = f'{self.player} solved day {self.day} level {self.level} at {self.solve_time_str}'
    if self.position is not None:
      s += f' in position {self.position}'
    return s
    
  def set_pos(self, pos):
    self.position = pos
