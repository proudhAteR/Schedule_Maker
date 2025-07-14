from typer import *

from App.Schedule_Maker import Scheduler
from Utils.Logger import Logger

app = Typer(help="Schedule Maker CLI: Create and manage your events quickly from the terminal.")
scheduler = Scheduler()
e_help = """
Natural language event description\n
[Course Name] in [Location] from [Start Time] to [End Time] every [Day] by [Teacher]
\nExample: Math in Room 101 from 10:00 to 11:00 every Monday by Mr. Smith
"""


@app.command(help="Create an event from natural language input.")
def event(description: str = Argument(..., help=e_help)):
    scheduler.event(description)


@app.command(help="Create a schedule using a block of events.")
def schedule(
        file: str = Option(None, "--file", "-f", help="Path to a file containing events (one per line)."),
        events: str = Argument(None, help="Block of events, ';' separated."),
        start: str = Option(..., "-s", "--start", help="The session starting date using yy-mm-dd format.")
):
    if file:
        with open(file, "r") as f:
            events_block = f.read()
    elif events:
        events_block = events
    else:
        raise Logger.error("You must provide either --file or a block of events.")

    scheduler.schedule(events_block, start)


if __name__ == "__main__":
    app()
