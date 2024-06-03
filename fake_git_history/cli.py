from typing import NamedTuple, List, Dict, Tuple
import argparse
from datetime import datetime, timedelta, timezone
import random
import string
import os
import subprocess
import re

import rong  # type: ignore

__version__ = "1.0.2"


class Commit(NamedTuple):
    message: str
    date: str


class FakeGitHistory:
    def __init__(self) -> None:
        self._current_commit: int = 0
        self._commits: List[Commit] = []
        self._start_date: datetime = (
            datetime.now() - timedelta(days=90)
        )
        self._end_date: datetime = datetime.now()
        self._start_time: str = "00:00:00"
        self._end_time: str = "23:59:59"
        self._time_zone: str = (
            datetime.now(timezone.utc)
            .astimezone()
            .strftime("%z")
        )
        self._commit_per_day: str = "0-3"
        self.is_work_days_only: bool = False
        self.is_weekends_only: bool = False
        self._verbose: bool = False
        self._auto_git_push: bool = False
        self._remote_origin: str = ""

        # rong config
        self._log: rong.Log = rong.Log(debug=False)

    def work_days_only(self) -> None:
        """Set the commits to workdays only."""
        self.is_work_days_only = True
        self._log.primary("Set to workdays only.")

    def weekends_only(self) -> None:
        """Set the commits to weekends only."""
        self.is_weekends_only = True
        self._log.primary("Set to weekends only.")

    def set_start_date(self, date: str) -> None:
        """Set the start date (dd/mm/yyyy)."""
        self._start_date = datetime.strptime(
            date, "%d/%m/%Y"
        )
        self._log.primary(
            f"Start date set to: {self._start_date}"
        )

    def set_end_date(self, date: str) -> None:
        """Set the end date (dd/mm/yyyy)."""
        self._end_date = datetime.strptime(date, "%d/%m/%Y")
        self._log.primary(
            f"End date set to: {self._end_date}"
        )

    def set_start_time(self, time: str) -> None:
        """Set the start time (hh:mm:ss)."""
        self._start_time = time
        self._log.primary(
            f"Start time set to: {self._start_time}"
        )

    def set_end_time(self, time: str) -> None:
        """Set the end time (hh:mm:ss)."""
        self._end_time = time
        self._log.primary(
            f"End time set to: {self._end_time}"
        )

    def get_random_time(self) -> str:
        """Generate a random time between start and end time."""
        # Define the time format
        time_format = "%H:%M:%S"

        # Convert start and end times to datetime objects
        start_time = datetime.strptime(
            self._start_time, time_format
        )
        end_time = datetime.strptime(
            self._end_time, time_format
        )

        # Calculate the time difference in seconds
        delta = end_time - start_time
        total_seconds = delta.total_seconds()

        # Generate a random number of seconds within the time range
        random_seconds = random.randint(
            0, int(total_seconds)
        )

        # Get the random time by adding the random seconds to the start time
        random_time = start_time + timedelta(
            seconds=random_seconds
        )

        # Return the random time as a string
        return random_time.strftime(time_format)

    def set_time_zone(self, time_zone: str) -> None:
        """Set the time zone in the format +0600"""
        if re.match(r"[\+\-]\d{4}", time_zone):
            self._time_zone = time_zone
        else:
            self._log.errormsg(
                "Invalid time zone. Please provide a time zone in the format +0600."
            )
        self._log.primary(
            f"Time zone set to: {self._time_zone}"
        )

    def set_commit_per_day(self, count_range: str) -> None:
        """Set the number of commits per day."""
        self._commit_per_day = count_range
        self._log.primary(
            f"Commits per day set to: {self._commit_per_day}"
        )

    def get_commit_per_day(self, count_range: str) -> int:
        """Set the number of commits per day."""
        _internal_commit_per_day: int = 0

        if re.match(r"\d+-\d+", count_range):
            _range_list: List[str] = (
                count_range.strip().split("-")
            )
            _internal_commit_per_day = random.randint(
                int(_range_list[0]), int(_range_list[1])
            )
        elif re.match(r"\d+", count_range):
            _internal_commit_per_day = int(count_range)
        else:
            self._log.errormsg(
                "Invalid range. Please provide a range like 0-99999 or a single number."
            )

        self._log.primary(
            f"Commits per day set to: {_internal_commit_per_day}"
        )

        return _internal_commit_per_day

    def set_remote_origin(self, remote_origin: str) -> None:
        """Set the remote origin."""
        self._remote_origin = remote_origin
        self._log.primary(
            f"Remote origin set to: {remote_origin}"
        )

    def enable_verbose(self) -> None:
        """Enable verbose mode."""
        self._verbose = True
        self._log.debug = True
        self._log.okmsg("Verbose mode enabled.")

    def disable_verbose(self) -> None:
        """Disable verbose mode."""
        self._log.okmsg("Verbose mode disabled.")
        self._verbose = False
        self._log.debug = False

    def version(self) -> None:
        """Show the version."""
        rong.Text(
            text=f"Fake Git History version v{__version__}",
            fg=rong.ForegroundColor.GREEN,
            styles=[rong.Style.BOLD],
        ).print()

    def set_auto_git_push(self) -> None:
        """Set auto git push."""
        self._auto_git_push = True
        self._log.primary("Auto git push enabled.")

    def worker(
        self,
        filename: str,
        filecontent: str,
        adderstring: str,
        removerstring: str,
        state: int = 0,
    ) -> None:
        """Worker function to create commits."""

        # Create a file with the filename
        with open(filename, "a") as file:
            file.write(filecontent)

        # Setting a default time
        _time: str = self.get_random_time()

        # dates "Sat Jun 26 20:38:25 2021 +0600"
        dates: Dict[str, str] = {
            "date": self._start_date.strftime("%d"),
            "dateName": self._start_date.strftime("%a"),
            "month": self._start_date.strftime("%b"),
            "year": self._start_date.strftime("%Y"),
        }

        _commit_date: str = f"{dates.get('dateName')} {dates.get('month')} {dates.get('date')} {_time} {dates.get('year')} {self._time_zone}"

        # log the commit date
        self._log.primary(f"Commit date: {_commit_date}")

        def add_file_commit() -> None:
            _ = subprocess.Popen(
                ["git", "add", filename],
                stdout=subprocess.PIPE,
            ).communicate()

            _ = subprocess.Popen(
                ["git", "commit", "-m", adderstring],
                stdout=subprocess.PIPE,
            ).communicate()

            _ = subprocess.Popen(
                [
                    "git",
                    "commit",
                    "--amend",
                    "--no-edit",
                    f'--date="{_commit_date}"',
                ],
                stdout=subprocess.PIPE,
            ).communicate()

        def remove_file_commit() -> None:
            os.remove(filename)

            _ = subprocess.Popen(
                ["git", "add", filename],
                stdout=subprocess.PIPE,
            ).communicate()

            _ = subprocess.Popen(
                ["git", "commit", "-m", removerstring],
                stdout=subprocess.PIPE,
            ).communicate()

            _ = subprocess.Popen(
                [
                    "git",
                    "commit",
                    "--amend",
                    "--no-edit",
                    f'--date="{_commit_date}"',
                ],
                stdout=subprocess.PIPE,
            ).communicate()

        if state == 0:
            add_file_commit()
        elif state == 1:
            remove_file_commit()
        else:
            self._log.errormsg("Invalid state.")

    def name_maker(self) -> Dict[str, str]:
        alpha: str = string.ascii_letters * 3
        name = "".join(random.sample(alpha, 20))
        description = "".join(random.sample(alpha, 50))

        return {"name": name, "description": description}

    def run(self) -> None:
        """Run the script."""
        self._log.waitmsg("Running script.")
        self._log.primary(f"Start date: {self._start_date}")
        self._log.primary(f"End date: {self._end_date}")
        self._log.green(
            f"Commits per day: {self._commit_per_day}"
        )
        # self._log.warning(f"Commits: {self._commits}")

        _state: int = 0

        def update_state(
            state: int = 0,
        ) -> Tuple[int, Dict[str, str]]:
            name_description: Dict[str, str] = {}
            if state == 0:
                state = 1
                name_description = self.name_maker()
            elif state == 1:
                state = 0
            else:
                self._log.errormsg("Invalid state.")
            return state, name_description

        # Create a my-history folder if it doesn't exist
        if not os.path.exists("my-history"):
            os.makedirs("my-history")

        # Change the directory to my-history
        os.chdir("my-history")

        # Initialize a git repository if it doesn't exist
        if not os.path.exists(".git"):
            _ = subprocess.Popen(
                ["git", "init"], stdout=subprocess.PIPE
            ).communicate()

        try:
            # loop through start date to end date and create commits
            while self._start_date <= self._end_date:
                # Check if the date is a weekend or workday
                # weekend is 5 (Saturday) and 6 (Sunday)
                # workday is 0 (Monday) to 4 (Friday)
                # else work 7 days
                if (
                    self.is_work_days_only
                    and self._start_date.weekday() >= 5
                ):
                    self._log.waitmsg(
                        f"Skipping weekend date: {self._start_date} ({self._start_date.strftime('%a')})"
                    )
                    # increment the date
                    self._start_date += timedelta(days=1)
                    continue
                elif (
                    self.is_weekends_only
                    and self._start_date.weekday() < 5
                ):
                    self._log.waitmsg(
                        f"Skipping weekday date: {self._start_date} ({self._start_date.strftime('%a')})"
                    )
                    # increment the date
                    self._start_date += timedelta(days=1)
                    continue

                self._log.waitmsg(
                    f"Processing date: {self._start_date} ({self._start_date.strftime('%a')})"
                )

                _internal_commit_per_day: int = (
                    self.get_commit_per_day(
                        self._commit_per_day
                    )
                )
                name_description: Dict[str, str] = (
                    self.name_maker()
                )

                for i in range(_internal_commit_per_day):
                    # per date commit count
                    self._log.primary(
                        f"Processing commit: {i + 1} of {_internal_commit_per_day}"
                    )
                    self.worker(
                        filename=f"{name_description.get('name')}.txt",
                        filecontent=f"This is the content of {name_description.get('description')}",
                        adderstring=f"Add {name_description.get('name')}.txt",
                        removerstring=f"Remove {name_description.get('name')}.txt",
                        state=_state,
                    )
                    _, name_description = update_state(
                        state=_state
                    )

                _, name_description = update_state(
                    state=_state
                )

                self._start_date += timedelta(days=1)

        except Exception as e:
            self._log.errormsg(f"An error occurred: {e}")
            self._log.errormsg("Script failed.")
            return

        if self._remote_origin != "":
            stdout, stderr = subprocess.Popen(
                [
                    "git",
                    "remote",
                    "add",
                    "origin",
                    self._remote_origin,
                ],
                stdout=subprocess.PIPE,
            ).communicate()
            if stderr:
                self._log.errormsg(f"Error: {str(stderr)}")
            if stdout:
                self._log.okmsg(
                    f"Remote origin set to {self._remote_origin}"
                )

        if self._auto_git_push:
            if self._remote_origin == "":
                self._log.errormsg(
                    "Remote origin not set. Please set the remote origin."
                )
                return
            stdout, stderr = subprocess.Popen(
                ["git", "push", "-u", "origin", "master"],
                stdout=subprocess.PIPE,
            ).communicate()
            if stderr:
                self._log.errormsg(f"Error: {str(stderr)}")
            if stdout:
                self._log.okmsg(
                    f"Pushed to {self._remote_origin}"
                )

        self._log.okmsg("Script completed.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fake Git History - A simple utility to generate fake git history for a Github and Gitlab profile."
    )
    parser.add_argument(
        "--start-date",
        "-sd",
        type=str,
        help="Set the start date (dd/mm/yyyy)",
    )
    parser.add_argument(
        "--end-date",
        "-ed",
        type=str,
        help="Set the end date (dd/mm/yyyy)",
    )
    parser.add_argument(
        "--start-time",
        "-st",
        type=str,
        help="Set the start time (hh:mm:ss)",
    )
    parser.add_argument(
        "--end-time",
        "-et",
        type=str,
        help="Set the end time (hh:mm:ss)",
    )
    parser.add_argument(
        "--time-zone",
        "-tz",
        type=str,
        help="Set the time zone in the format +0600",
    )
    parser.add_argument(
        "--work-days-only",
        "-wd",
        action="store_true",
        help="Create commits to workdays only",
    )
    parser.add_argument(
        "--weekends-only",
        "-we",
        action="store_true",
        help="Create commits to weekends only",
    )
    parser.add_argument(
        "--commit-per-day",
        "-c",
        type=str,
        help="Set the number of commits per day",
    )
    parser.add_argument(
        "--auto-git-push",
        "-a",
        action="store_true",
        help="Enable auto git push",
    )
    parser.add_argument(
        "--remote-origin",
        "-r",
        type=str,
        help="Set the remote origin",
    )
    parser.add_argument(
        "--verbose",
        "-vv",
        action="store_true",
        help="Enable verbose mode",
    )
    parser.add_argument(
        "--version",
        "-v",
        action="store_true",
        help="Show the version",
    )

    args = parser.parse_args()

    fgh = FakeGitHistory()

    if args.verbose:
        fgh.enable_verbose()
    if args.start_date:
        fgh.set_start_date(date=args.start_date)
    if args.end_date:
        fgh.set_end_date(date=args.end_date)
    if args.start_time:
        fgh.set_start_time(time=args.start_time)
    if args.end_time:
        fgh.set_end_time(time=args.end_time)
    if args.time_zone:
        fgh.set_time_zone(time_zone=args.time_zone)
    if args.work_days_only:
        fgh.work_days_only()
    if args.weekends_only:
        fgh.weekends_only()
    if args.commit_per_day:
        fgh.set_commit_per_day(
            count_range=str(args.commit_per_day)
        )
    if args.remote_origin:
        fgh.set_remote_origin(
            remote_origin=args.remote_origin
        )
    if args.auto_git_push:
        fgh.set_auto_git_push()
    if args.version:
        fgh.version()
        exit()

    fgh.run()
