from asyncio import run as async_call
from pathlib import Path
from typing import Optional

import typer

import Infrastructure.Utils.Helpers.Imports as Imp
from Infrastructure.Utils.Helpers.Help_texts import EVENT_HELP
from Infrastructure.Utils.Logs.Logger import Logger

app = typer.Typer()


@app.command(help="Create an event from natural language input.")
def event(
        description: str = typer.Argument(..., help=EVENT_HELP["description"]),
        priority: Optional[str] = typer.Option(
            None,
            "--priority",
            "-pr",
            help="\n".join(f"{k}: {v}" for k, v in EVENT_HELP["priority"].items()),
            show_choices=True,
            case_sensitive=False
        )
):
    try:
        if priority:
            p = priority.lower()
            if p not in EVENT_HELP["priority"]:
                raise typer.BadParameter(f"Priority must be one of: {', '.join(EVENT_HELP['priority'].keys())}")
        else:
            p = None

        from App.SM import SM

        async_call(
            SM().event(description, p)
        )
    except Exception as e:
        Logger.error(f"Failed to create event: {e}")
        raise typer.Exit(code=1)


@app.command(help="Create a schedule using a block of events.")
def schedule(
        events: Optional[str] = typer.Argument(None, help="Block of events, ';' separated."),
        file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to file with one event per line."),
        start: Optional[str] = typer.Option(None, "-s", "--start", help="Starting date (yy-mm-dd).")
):
    try:
        if not events and not file:
            raise typer.BadParameter("Provide either a block of events or a file path.")

        if file:
            path = Path(file)
            if not path.exists():
                raise typer.BadParameter(f"File not found: {file}")
            with open(path, "r", encoding="utf-8") as f:
                events_list = [line.strip() for line in f if line.strip()]
        else:
            events_list = [e.strip() for e in events.split(";") if e.strip()]

        if not events_list:
            raise typer.BadParameter("No valid events provided.")

        from App.SM import SM
        async_call(
            SM().schedule(events_list, start)
        )
    except Exception as e:
        Logger.error(f"Failed to create schedule: {e}")
        raise typer.Exit(code=2)


@app.command(help="Get schedule overview for a given date.")
def overview(
        date: Optional[str] = typer.Option(None, "-o", "--on", help="Date or expression like 'today', 'next monday'.")
):
    try:
        from App.SM import SM
        events, date_time = async_call(
            SM().overview(date)
        )

        Logger.success(f"{len(events)} event(s) found on {date_time.date()}")
        for start_str, summary in events:
            Logger.info(f"{start_str}: {summary}")

    except Exception as e:
        Logger.error(f"Failed to give overview: {e}")
        raise typer.Exit(code=3)


@app.command(help="Connect to your google account.")
def auth():
    try:
        from App.SM import SM

        SM().connect()
    except Exception as e:
        Logger.error(f"Failed to connect: {e}")
        raise typer.Exit(code=4)


def run():
    Imp.run()
    app()


if __name__ == "__main__":
    run()
