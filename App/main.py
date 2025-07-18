from asyncio import run as async_call
from typer import Typer, Option, Argument

import Infrastructure.Utils.Helpers.Imports as Imp
from App.Schedule_Maker import Schedule_Maker
from Infrastructure.Services.Google.GoogleCalendar import GoogleCalendar
from Infrastructure.Utils.Helpers.Help_texts import *
from Infrastructure.Utils.Logs.Logger import Logger

Imp.run()
app = Typer()
maker = Schedule_Maker(
    GoogleCalendar()
)


@app.command(help="Create an event from natural language input.")
def event(
        description: str = Argument(..., help=EVENT_HELP["description"]),
        priority: str = Option(
            "medium",
            "--priority",
            "-pr",
            help="\n".join(f"{k}: {v}" for k, v in EVENT_HELP["priority"].items()),
            show_choices=True,
            case_sensitive=False
        )
):
    priority = priority.lower()
    pr_list = EVENT_HELP["priority"].keys()

    if priority not in pr_list:
        raise ValueError(f"Priority must be one of: {', '.join(pr_list)}")

    async_call(
        maker.event(description, priority)
    )


@app.command(help="Create a schedule using a block of events.")
def schedule(
        file: str = Option(None, "--file", "-f", help="Path to a file containing events (one per line)."),
        events: str = Argument(None, help="Block of events, ';' separated."),
        start: str = Option(None, "-s", "--start", help="The session starting date using yy-mm-dd format.")
):
    if file:
        with open(file, "r") as f:
            events_block = f.read().splitlines()
    elif events:
        events_block = events.split(";")
    else:
        raise Logger.error("You must provide either --file or a block of events.")

    async_call(
        maker.schedule(events_block, start)
    )


if __name__ == "__main__":
    app()
