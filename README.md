# AoCSlacker-Python

Notify Slack channel with Advent of Code leaderboard, now in glorious Python in true AoC spirit!

## Crontab
Crontab syntax to run every Monday at 12:00

```bash
# m h  dom mon dow   command
0 12 * * 1 AOC_SESSION='xyz' AOC_LEADERBOARD_ID='xxxxx' AOC_YEAR='xxxx' SLACK_WEBHOOK_URL='https://hooks.slack.com/services/xxx/xxx/xxx' /usr/bin/python /path/to/aocslacker-python/src/bot.py
```

## systemd
Copy and modify `AoCSlacker-Python.service.example` to `AoCSlacker-Python.service`
and hardlink it to your systemd unit library. Copy and modify
`AoCSlacker-Python.timer.example` to `AoCSlacker-Python.timer` and hardlink it to your
systemd unit library. Run `systemctl edit AoCSlacker-Python.service` and insert:

```
[Service]
Environment="AOC_YEAR=<AoC contest year>"
Environment="AOC_LEADERBOARD_ID=<leaderboard ID>"
Environment="AOC_SESSION=<AoC session cookie>"
Environment="SLACK_WEBHOOK_URL=<Slack webhook URL>"
```

Finally run `systemctl enable --now AoCSlacker-Python.timer`

## Example output

### Total

```md
Leaderboard 2024: Top {count, max 25} as of 10:55:29 - https://adventofcode.com/{aoc_year}/leaderboard/private/view/{aoc_leaderboard_id}

   Name                   📋 
──────────────────────────── 
 1 Person                 62 
 2 Person                 61 
 3 Person                 56 
 4 Person                 45 
 5 Person                 37 
 6 Person                 32 
 7 Person                 29 
 8 Person                 23 
 9 Person                 20 
10 Person                 18 
11 Person                 17 
```
### Daily

```md
Leaderboard 2024: Day {day} solve times as of 10:55:29

Time     Name             🏆 
──────────────────────────── 
06:07:49 Person            1 
06:08:57 Person            2 
06:11:54 Person            1 
06:12:15 Person            3 
06:15:35 Person            2 
06:24:11 Person            4 
06:24:57 Person            5 
06:29:07 Person            3 
06:32:13 Person            4 
06:47:20 Person            5 
07:15:28 Person            6 
07:31:38 Person            6 
07:50:18 Person            7 
07:58:19 Person            8 
08:02:51 Person            9 
08:08:56 Person            7 
08:20:13 Person            8 
```
