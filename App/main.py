from typer import *

from App.Schedule_Maker import Scheduler

app = Typer(help="Schedule Maker CLI: Create and manage your events quickly from the terminal.")
scheduler = Scheduler()


@app.command(help="Create an event from natural language input.")
def event(description: str = Argument(..., help="Natural language event description")):
    scheduler.event(description)


@app.command(help="Create a schedule using a block of events.")
def schedule(events: str = Argument(..., help="Block of events")):
    scheduler.schedule(events)


if __name__ == "__main__":
    app()
