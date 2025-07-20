from asyncio import run as async_call
from pathlib import Path
from typing import Optional, List

from typer import Typer, Option, Argument, Exit

import Infrastructure.Utils.Helpers.Imports as Imp
from App.Schedule_Maker import Schedule_Maker
from Infrastructure.Services.Google.GoogleCalendar import GoogleCalendar
from Infrastructure.Utils.Helpers.Help_texts import EVENT_HELP
from Infrastructure.Utils.Logs.Logger import Logger


class App:
    def __init__(self):
        Imp.run()
        self.app = Typer()
        self.maker = Schedule_Maker(
            GoogleCalendar()
        )
        self._setup_commands()

    def _setup_commands(self):
        self.app.command(help="Create an event from natural language input.")(self.event)
        self.app.command(help="Create a schedule using a block of events.")(self.schedule)

    @staticmethod
    def _validate_priority(priority: str) -> str:
        if not priority:
            return priority

        priority = priority.lower()
        valid_priorities = list(EVENT_HELP["priority"].keys())

        if priority not in valid_priorities:
            Logger.error(f"Priority must be one of: {', '.join(valid_priorities)}")
            raise Exit(1)

        return priority

    @staticmethod
    def _load_events_from_file(file_path: str) -> List[str]:
        try:
            path = Path(file_path)
            if not path.exists():
                Logger.error(f"File not found: {file_path}")
                raise Exit(1)

            with open(path, "r", encoding="utf-8") as f:
                events = [line.strip() for line in f.readlines() if line.strip()]

            if not events:
                Logger.error(f"No events found in file: {file_path}")

            return events

        except IOError as e:
            Logger.error(f"Error reading file {file_path}: {e}")
            raise Exit(1)

    @staticmethod
    def _parse_events_string(events_str: str) -> List[str]:
        events = [event.strip() for event in events_str.split(";") if event.strip()]

        if not events:
            Logger.error("No valid events found in the provided string")
            raise Exit(1)

        return events

    def _get_events_list(self, file_path: Optional[str], events_str: Optional[str]) -> List[str]:
        if file_path:
            return self._load_events_from_file(file_path)
        elif events_str:
            return self._parse_events_string(events_str)
        else:
            Logger.error("You must provide either --file or a block of events as argument")
            raise Exit(1)

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
            raise Exit(1)

    def run(self):
        self.app()


__instance = App()
app = __instance.app

if __name__ == "__main__":
    __instance.run()
