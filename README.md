# Fake Git History Generator

A simple utility to generate fake git history for a Github and Gitlab profile to make your profile look more active than it actually is.

***Author: [Md. Almas Ali](https://almasali.net)***

[![PyPI version](https://badge.fury.io/py/fake-git-history.svg)](https://badge.fury.io/py/fake-git-history)
[![Downloads](https://pepy.tech/badge/fake-git-history)](https://pepy.tech/project/fake-git-history)
[![wakatime](https://wakatime.com/badge/user/168edf9f-71dc-49cc-bf77-592d9c9d4eed/project/60aed9e5-281b-4468-8819-5a1cef8d90d8.svg)](https://wakatime.com/badge/user/168edf9f-71dc-49cc-bf77-592d9c9d4eed/project/60aed9e5-281b-4468-8819-5a1cef8d90d8)
![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FAlmas-Ali%2Ffake-git-history&count_bg=%2379C83D&title_bg=%23555555&icon=github.svg&icon_color=%23E7E7E7&title=Hits&edge_flat=false)

![How it works](https://github.com/Almas-Ali/fake-git-history/blob/master/contribution-graph.gif "How it works")

## Table of Contents

- [Introduction](#introduction)
- [Support This Project](#support-this-project)
- [Installation](#installation)
- [Options and Usage](#options-and-usage)
  - [`--commit-per-day` and `-c`](#--commit-per-day-and--c)
  - [`--work-days-only` and `-wd`](#--work-days-only-and--wd)
  - [`--weekends-only` and `-we`](#--weekends-only-and--we)
  - [`--start-date` and `--end-date` or `-sd` and `-ed`](#--start-date-and--end-date-or--sd-and--ed)
  - [`--start-time` and `--end-time` or `-st` and `-et`](#--start-time-and--end-time-or--st-and--et)
  - [`--time-zone` and `-tz`](#--time-zone-and--tz)
  - [`--remote-origin` and `-r`](#--remote-origin-and---r)
  - [`--auto-git-push` and `-a`](#--auto-git-push-and--a)
  - [`--verbose` and `-vv`](#--verbose-and--vv)
  - [`--version` and `-v`](#--version-and--v)
  - [`--help` and `-h`](#--help-and--h)
- [Demo and Examples](#demo-and-examples)
  - [Example 1](#example-1)
  - [Example 2](#example-2)
  - [Example 3](#example-3)
  - [Example 4](#example-4)
  - [Example 5](#example-5)
- [Caution](#caution)
- [License](#license)

## Introduction

Fake Git History Generator is a simple utility to generate fake git history for a Github and Gitlab profile to make your profile look more active than it actually is. It generates fake commits for the last 90 days (by default config) with random commit counts per day (0-3). You can also specify the number of commits per day, start date, end date, start time, end time, time zone, work days only, weekends only, remote origin, auto git push, and verbose output.

It uses the `git` command to create commits and push them to the remote repository.

**Give this project a star, if you like it. (Highly Recommended) 🌟**

This project is inspired by [fake-git-history](https://github.com/artiebits/fake-git-history) JS project.

**Note:** Read the [Caution](#caution) section before using this tool.

## Support This Project

If you find this project useful and want to support my work, you can buy me a coffee. My work is open source and free. Your support will allow me to continue my work and build more projects. Thank you for your support!

<a href="https://www.buymeacoffee.com/almaspr3" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" title="Support Md. Almas Ali"></a>

## Installation

You need to have [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [Python3](https://www.python.org/downloads/) installed on your machine. Then you can install it with `pip`.

```bash
pip install fake-git-history
```

You can also install it from source. If you want then follow this.

```bash
# Clone the git repository
git clone https://github.com/Almas-Ali/fake-git-history.git fake-git-history

# Change your directory to fake-git-history
cd fake-git-history

# Install it with pip
pip install .
```

## Options and Usage

### `--commit-per-day` and `-c`

Specify the number of commits to be created for each day.
The default value is `0-3`, which means it will randomly generate from 0 to 3 commits per day. For example, to generate commits randomly between 6 and 12 per day, you can do:

```bash
fake-git-history --commit-per-day "6-12"
# or
fake-git-history -c "6-12"
```

You can also give a strict number. For example, you need 16 contributions every single day. Then use this command. Not recommended, this will make views to easily detect your bot.

```bash
fake-git-history --commit-per-day "16"
# or
fake-git-history -c "16"
```

### `--work-days-only` and `-wd`

Use this option if you don't want to commit on weekends. Example:

```bash
fake-git-history --work-days-only
# or
fake-git-history -d
```

### `--weekends-only` and `-we`

Use this option if you only want to contribute on weekends. Example:

```bash
fake-git-history --weekends-only
# or
fake-git-history -w
```

### `--start-date` and `--end-date` or `-sd` and `-ed`

The starting data is by default set to previous 90 days from the current date and end date is by default present date. If you don't change, it will create commits for the last 90 days. You can change the start date and end date. Example:

```bash
# User defined start and end date
fake-git-history --start-date "01/03/2016" --end-date "12/02/2023"
# or
fake-git-history -s "01/03/2016" -e "12/02/2023"

# Flexible end date
fake-git-history --start-date "01/03/2016"
# or
fake-git-history -s "01/03/2016"
```

The date formating is `DD/MM/YYYY`. You have to write this way.

### `--start-time` and `--end-time` or `-st` and `-et`

The starting time is by default set to `00:00:00` and end time is by default `23:59:59`. You can change the start time and end time. Example:

```bash
# User defined start and end time
fake-git-history --start-time "09:00:00" --end-time "17:00:00"
# or
fake-git-history -st "09:00:00" -et "17:00:00"
```

The time formating is `HH:MM:SS`. You have to write this way.

### `--time-zone` and `-tz`

The time zone is by default set to your local time zone. You can change the time zone. Example:

```bash
# User defined time zone
fake-git-history --time-zone "+0600"
# or
fake-git-history -tz "+0600"
```

The time zone formating is `+HHMM` or `-HHMM`. You have to write this way.

### `--remote-origin` and `-r`

Use this option to set the remote origin. Example:

```bash
fake-git-history --remote-origin "git@github.com:<YOUR-USERNAME>/<YOUR-REPO>.git"
# or
fake-git-history -r "git@github.com:<YOUR-USERNAME>/<YOUR-REPO>.git"
```

### `--auto-git-push` and `-a`

Use this option to automatically push the commits to the remote repository. Example:

```bash
fake-git-history --auto-git-push
# or
fake-git-history -a
```

### `--verbose` and `-vv`

Use this option to see the verbose output. Without this option you won't be able to see much information about the process. Example:

```bash
fake-git-history --verbose
# or
fake-git-history -vv
```

### `--version` and `-v`

Use this option to check the version of this script.

```bash
fake-git-history --version
# or
fake-git-history -v
```

### `--help` and `-h`

You can always refer to this help menu to see the options available. Example:

```bash
fake-git-history --help
```

**Output**

```bash
usage: fake-git-history [-h] [--start-date START_DATE] [--end-date END_DATE] [--start-time START_TIME] [--end-time END_TIME] [--time-zone TIME_ZONE] [--work-days-only] [--weekends-only] [--commit-per-day COMMIT_PER_DAY] [--auto-git-push] [--remote-origin REMOTE_ORIGIN] [--verbose] [--version]

Fake Git History - A simple utility to generate fake git history for a Github and Gitlab profile.

options:
  -h, --help            show this help message and exit
  --start-date START_DATE, -sd START_DATE
                        Set the start date (dd/mm/yyyy)
  --end-date END_DATE, -ed END_DATE
                        Set the end date (dd/mm/yyyy)
  --start-time START_TIME, -st START_TIME
                        Set the start time (hh:mm:ss)
  --end-time END_TIME, -et END_TIME
                        Set the end time (hh:mm:ss)
  --time-zone TIME_ZONE, -tz TIME_ZONE
                        Set the time zone in the format +0600
  --work-days-only, -wd
                        Create commits to workdays only
  --weekends-only, -we  Create commits to weekends only
  --commit-per-day COMMIT_PER_DAY, -c COMMIT_PER_DAY
                        Set the number of commits per day
  --auto-git-push, -a   Enable auto git push
  --remote-origin REMOTE_ORIGIN, -r REMOTE_ORIGIN
                        Set the remote origin
  --verbose, -vv        Enable verbose mode
  --version, -v         Show the version
```

After running the script, you will see a `my-history` folder in your current directory. This folder contains the git repository with the fake commits. You can check the commits by going to the `my-history` folder and running the `git log` command.

```bash
cd my-history
git log
```

If you have enabled the auto git push and set the remote origin, then the commits will be pushed to the remote repository. You can check the commits on your Github or Gitlab profile.

## Demo and Examples

### Example 1

Generate fake git history for the last 90 days with 0-3 commits per day.

```bash
fake-git-history
```

### Example 2

Generate fake git history for the last 90 days with 6-12 commits per day.

```bash
fake-git-history --commit-per-day "6-12"
# or
fake-git-history -c "6-12"
```

### Example 3

Generate fake git history from 01/03/2016 to 12/02/2023 with 6-12 commits per day with verbose output.

```bash
fake-git-history --start-date "01/03/2016" --end-date "12/02/2023" --commit-per-day "6-12" --verbose
# or
fake-git-history -sd "01/03/2016" -ed "12/02/2023" -c "6-12" -vv
```

### Example 4

Generate fake git history from 03/02/2000 to present date with 60-100 commits per day with verbose output. Add remote origin and auto git push.

```bash
fake-git-history --start-date "03/02/2000" --commit-per-day "60-100" --remote-origin "git@github.com:<YOUR-USERNAME>/<YOUR-REPO>.git" --auto-git-push --verbose
# or
fake-git-history -sd "03/02/2000" -c "60-100" -r "git@github.com:<YOUR-USERNAME>/<YOUR-REPO>.git" -a -vv
```

### Example 5

Generate fake git history from "07/03/2021" to "07/03/2022" and start time "09:00:00" and end time "17:00:00" with 4-6 commits per day in "-0300" timezone with verbose output. Add remote origin and auto git push.

```bash
fake-git-history --start-date "07/03/2021" --end-date "07/03/2022" --start-time "09:00:00" --end-time "17:00:00" -tz "-0300" --commit-per-day "4-6" --remote-origin "git@github.com:<YOUR-USERNAME>/<YOUR-REPO>.git" --auto-git-push --verbose
# or
fake-git-history -sd "07/03/2021" -ed "07/03/2022" -st "09:00:00" -et "17:00:00" -tz "-0300" -c "4-6" -r "git@github.com:<YOUR-USERNAME>/<YOUR-REPO>.git" -a -vv
```

**Note 1:** You need to have SSH keys setup for the auto git push to work. If you don't have SSH keys setup, you can follow this [guide](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh).

**Note 2:** Don't forget to change your repository in private mode if you don't want others to see your fake commits. You can do this by going to your repository settings and changing the visibility to private.

## Caution

This tool was created as a joke, so please don't take it seriously. While cheating is never encouraged, if someone is judging your professional skills based on your GitHub activity graph, they deserve to see a rich activity graph. 🤓

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify this project. If you liked this project, give it a star ⭐.
