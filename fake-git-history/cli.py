from typing import NamedTuple, List, Dict, Optional, Tuple
import argparse
from datetime import datetime, timedelta
import random
import string
import os
import subprocess
import re

import rong  # type: ignore


class Commit(NamedTuple):
    message: str
    date: str


class FakeGitHistory:
    def __init__(self) -> None:
        self._current_commit: int = 0
        self._commits: List[Commit] = []
        self._start_date: datetime = datetime.now()
        self._end_date: datetime = datetime.now()
        self._commit_per_day: str = "3"
        self._verbose: bool = False

        # rong config
        self._log: rong.Log = rong.Log(debug=False)

    def work_days_only(self):
        """Filter commits to workdays only."""
        self._commits = [
            commit
            for commit in self._commits
            if datetime.strptime(
                commit.date, "%Y-%m-%d %H:%M:%S"
            ).weekday()
            < 5
        ]
        self._log.primary("Filtered to workdays only.")

    def weekends_only(self):
        """Filter commits to weekends only."""
        self._commits = [
            commit
            for commit in self._commits
            if datetime.strptime(
                commit.date, "%Y-%m-%d %H:%M:%S"
            ).weekday()
            >= 5
        ]
        self._log.primary("Filtered to weekends only.")

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
        self._log.primary(f"End date set to: {self._end_date}")

    def set_commit_per_day(self, count_range: str) -> None:
        """Set the number of commits per day."""
        self._commit_per_day = count_range
        self._log.primary(
            f"Commits per day set to: {self._commit_per_day}"
        )

    def get_commit_per_day(
        self,
        count_range: str,
        calculate_and_return: bool = False,
    ) -> Optional[int]:
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

        if calculate_and_return:
            return _internal_commit_per_day

    def enable_verbose(self):
        """Enable verbose mode."""
        self._verbose = True
        self._log.debug = True
        self._log.okmsg("Verbose mode enabled.")

    def disable_verbose(self):
        """Disable verbose mode."""
        self._log.okmsg("Verbose mode disabled.")
        self._verbose = False
        self._log.debug = False

    def version(self):
        """Show the version."""
        print("Fake Git History version 1.0.0")

    def worker(
        self,
        filename: str,
        filecontent: str,
        adderstring: str,
        removerstring: str,
        state: int = 0,
    ) -> None:
        """Worker function to create commits."""

        with open(filename, "a") as file:
            file.write(filecontent)

        # Setting a default time
        _time: str = datetime.now().strftime("%H:%M:%S")

        # dates "Sat Jun 26 20:38:25 2021 +0600"
        dates: Dict[str, str] = {
            "date": self._start_date.strftime("%d"),
            "dateName": self._start_date.strftime("%a"),
            "month": self._start_date.strftime("%b"),
            "year": self._start_date.strftime("%Y"),
        }

        _commit_date: str = f"{dates.get('dateName')} {dates.get('month')} {
            dates.get('date')} {_time} {dates.get('year')} +0600"

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

    def run(self):
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

        try:
            # loop through start date to end date and create commits
            while self._start_date <= self._end_date:
                self._log.waitmsg(
                    f"Processing date: {self._start_date}"
                )

                _internal_commit_per_day: int = (
                    self.get_commit_per_day(
                        self._commit_per_day,
                        calculate_and_return=True,
                    )
                    or 1
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
                    _, name_description = update_state(state=_state)

                _, name_description = update_state(state=_state)

                self._start_date += timedelta(days=1)

        except Exception as e:
            self._log.errormsg(f"An error occurred: {e}")
            self._log.errormsg("Script failed.")
            return

        self._log.okmsg("Script completed.")


def main():
    parser = argparse.ArgumentParser(
        description="Fake Git History - A python script to create fake git history."
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="Set the start date (dd/mm/yyyy)",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        help="Set the end date (dd/mm/yyyy)",
    )
    parser.add_argument(
        "--work-days-only",
        action="store_true",
        help="Filter commits to workdays only",
    )
    parser.add_argument(
        "--weekends-only",
        action="store_true",
        help="Filter commits to weekends only",
    )
    parser.add_argument(
        "--commit-per-day",
        type=str,
        help="Set the number of commits per day",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose mode",
    )
    parser.add_argument(
        "--version",
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
    if args.work_days_only:
        fgh.work_days_only()
    if args.weekends_only:
        fgh.weekends_only()
    if args.commit_per_day:
        fgh.set_commit_per_day(
            count_range=str(args.commit_per_day)
        )
    if args.version:
        fgh.version()

    fgh.run()
