import subprocess
import sys
from asyncio import run as async_call
from pathlib import Path
from typing import Optional, List

import typer
from typer import Typer, Option, Argument, Exit

import Infrastructure.Utils.Helpers.Imports as Imp
from App.Schedule_Maker import Schedule_Maker
from Infrastructure.Services.Google.GoogleCalendar import GoogleCalendar
from Infrastructure.Utils.FileHandler import FileHandler
from Infrastructure.Utils.Helpers.Help_texts import EVENT_HELP
from Infrastructure.Utils.Logs.Logger import Logger


class App:
    def __init__(self):
        Imp.run()
        self.app = Typer()
        self.maker = Schedule_Maker(GoogleCalendar())
        self._setup_commands()
        self._setup_callbacks()

    def _setup_commands(self):
        self.app.command(help="Create an event from natural language input.")(self.event)
        self.app.command(help="Create a schedule using a block of events.")(self.schedule)
        self.app.command(help="Gives the schedule for a given date.")(self.overview)

    def _setup_callbacks(self):
        @self.app.callback(invoke_without_command=True)
        def main(
                ctx: typer.Context,
                upgrade: bool = Option(
                    False,
                    "--upgrade",
                    "-u",
                    help="Upgrade Schedule Maker to the latest version",
                    is_flag=True,
                    show_default=True,
                )
        ):
            if upgrade:
                self.run_update()
                raise Exit()

            # Optional: show help if no command is provided
            if ctx.invoked_subcommand is None:
                typer.echo(ctx.get_help())
                raise Exit()

    @staticmethod
    def is_pipx():
        return "pipx" in sys.executable.lower()

    @staticmethod
    def update_pipx():
        try:
            typer.echo("Updating Schedule Maker via pipx...")
            subprocess.run([sys.executable, "-m", "pipx", "upgrade", "sm"], check=True)
            typer.echo("Update completed successfully.")
        except subprocess.CalledProcessError:
            typer.echo("pipx upgrade failed, trying uninstall + install...")
            subprocess.run([sys.executable, "-m", "pipx", "uninstall", "sm"], check=True)
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pipx",
                    "install",
                    "git+https://github.com/proudhAteR/Schedule_Maker.git",
                    "--pip-args=--only-binary :all:",
                ],
                check=True,
            )
            typer.echo("Update completed successfully.")

    @staticmethod
    def update_pip():
        repo_path = FileHandler.root()
        typer.echo(f"Updating from git in {repo_path} ...")
        subprocess.run(["git", "-C", str(repo_path), "pull"], check=True)
        typer.echo("Reinstalling package...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "-e", str(repo_path)], check=True)
        typer.echo("Update completed successfully.")

    def run_update(self):
        if self.is_pipx():
            self.update_pipx()
        else:
            self.update_pip()

    @staticmethod
    def _validate_priority(priority: str) -> str:
        if not priority:
            return priority

        priority = priority.lower()
        valid_priorities = list(EVENT_HELP["priority"].keys())

        if priority not in valid_priorities:
            Logger.error(f"Priority must be one of: {', '.join(valid_priorities)}")
            raise

        return priority

    @staticmethod
    def _load_events_from_file(file_path: str) -> List[str]:
        try:
            path = Path(file_path)
            if not path.exists():
                Logger.error(f"File not found: {file_path}")
                raise

            with open(path, "r", encoding="utf-8") as f:
                events = [line.strip() for line in f.readlines() if line.strip()]

            if not events:
                Logger.error(f"No events found in file: {file_path}")

            return events

        except IOError as e:
            Logger.error(f"Error reading file {file_path}: {e}")
            raise

    @staticmethod
    def _parse_events_string(events_str: str) -> List[str]:
        events = [event.strip() for event in events_str.split(";") if event.strip()]

        if not events:
            Logger.error("No valid events found in the provided string")
            raise

        return events

    def _get_events_list(self, file_path: Optional[str], events_str: Optional[str]) -> List[str]:
        if file_path:
            return self._load_events_from_file(file_path)
        elif events_str:
            return self._parse_events_string(events_str)
        else:
            Logger.error("You must provide either --file or a block of events as argument")
            raise

    def event(
            self,
            description: str = Argument(..., help=EVENT_HELP["description"]),
            priority: Optional[str] = Option(
                None,
                "--priority",
                "-pr",
                help="\n".join(f"{k}: {v}" for k, v in EVENT_HELP["priority"].items()),
                show_choices=True,
                case_sensitive=False
            )
    ):
        try:
            validated_priority = self._validate_priority(priority)
            async_call(self.maker.event(description, validated_priority))

        except Exception as e:
            Logger.error(f"Failed to create event: {e}")
            raise Exit(1)

    def schedule(
            self,
            events: Optional[str] = Argument(None, help="Block of events, ';' separated."),
            file: Optional[str] = Option(
                None,
                "--file",
                "-f",
                help="Path to a file containing events (one per line)."
            ),
            start: Optional[str] = Option(
                None,
                "-s",
                "--start",
                help="The session starting date using yy-mm-dd format."
            )
    ):
        try:
            events_list = self._get_events_list(file, events)
            async_call(self.maker.schedule(events_list, start))
        except Exception as e:
            Logger.error(f"Failed to create schedule: {e}")
            raise Exit(2)

    def overview(
            self, date: Optional[str] = Option(
                None,
                "-o",
                "--on",
                help="The day or moment you want to see the schedule for (e.g., 'today', 'next Monday', '2025-07-22')."
            )
    ):

        try:
            async_call(self.maker.overview(date))
        except Exception as e:
            Logger.error(f"Failed to give overview: {e}")
            raise Exit(3)

    def run(self):
        self.app()


__instance = App()
app = __instance.app

if __name__ == "__main__":
    __instance.run()
