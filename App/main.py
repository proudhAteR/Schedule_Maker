from typer import Typer, Option, Argument, echo
from asyncio import run as async_call
from App.Schedule_Maker import Scheduler
from Infrastructure.Utils.Logger import Logger
from Infrastructure.Utils.help_texts import *

app = Typer()
scheduler = Scheduler()


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
        scheduler.event(description, priority)
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
        echo(events_block)
    elif events:
        events_block = events.split(";")
    else:
        raise Logger.error("You must provide either --file or a block of events.")

    async_call(
        scheduler.schedule(events_block, start)
    )


if __name__ == "__main__":
    app()
