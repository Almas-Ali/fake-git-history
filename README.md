# Fake Git History Generator

A command-line tool that generates GitHub or GitLab activity graph to make it look like you have been coding regularly.

<img src="https://github.com/Almas-Ali/fake-git-history/blob/master/contribution-graph.png" alt="How it works" />

## Features

Python project details:

- [x] PEP-8 Complaint.
- [x] Strictly type annotated.
- [x] Well tested.

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

## Support This Project

If you rely on this tool and find it useful, please consider supporting it. Maintaining an open source project takes time and a cup of coffee would be greatly appreciated!

<a href="https://www.buymeacoffee.com/almaspr3" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" title="Support Md. Almas Ali"></a>

## Options and Usage

### `--commit-per-day`

Specify the number of commits to be created for each day.
The default value is `0-3`, which means it will randomly generate from 0 to 3 commits per day. For example, to generate commits randomly between 6 and 12 per day, you can do:

```bash
fake-git-history --commit-per-day "6-12"
```

You can also give a strict number. For example, you need 16 contributions every single day. Then use this command. Not recommended, this will make views to easily detect your bot.

```bash
fake-git-history --commit-per-day "16"
```

### `--work-days-only`

Use this option if you don't want to commit on weekends. Example:

```bash
fake-git-history --work-days-only
```

### `--weekends-only`

Use this option if you only want to contribute on weekends. Example:

```bash
fake-git-history --weekends-only
```

### `--start-date` and `--end-date`

You have to give this script a starting date to start from. But end date is by default present date. If you don't change it, it will make contribution history for you till present date. Example:

```bash
# Strict end date
fake-git-history --start-date "01/03/2016" --endDate "12/02/2023"

# Flexible end date
fake-git-history --start-date "01/03/2016"
```

The date formating is `DD/MM/YYYY`. You have to write this way.

### `--verbose`

Use this option to see the verbose output. Without this option you won't be able to see much information about the process. Example:

```bash
fake-git-history --verbose
```

### `--version`

Use this option to check the version of this script.

```bash
fake-git-history --version
```

### `--help` and `-h`

You can always refer to this help menu to see the options available. Example:

```bash
fake-git-history --help
```

**Output**

```bash
usage: fake-git-history [-h] [--start-date START_DATE] [--end-date END_DATE] [--work-days-only] [--weekends-only] [--commit-per-day COMMIT_PER_DAY] [--verbose] [--version]

Fake Git History - A python script to create fake git history.

options:
  -h, --help            show this help message and exit
  --start-date START_DATE
                        Set the start date (dd/mm/yyyy)
  --end-date END_DATE   Set the end date (dd/mm/yyyy)
  --work-days-only      Filter commits to workdays only
  --weekends-only       Filter commits to weekends only
  --commit-per-day COMMIT_PER_DAY
                        Set the number of commits per day
  --verbose             Enable verbose mode
  --version             Show the version
```

## PS

This tool was created as a joke, so please don't take it seriously. While cheating is never encouraged, if someone is judging your professional skills based on your GitHub activity graph, they deserve to see a rich activity graph 🤓

## License

[MIT License](LICENSE)
