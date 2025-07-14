from textwrap import dedent

from Utils.Logger import Logger


def block_instructions():
    print(dedent("""
        If you want to start from a specific date, begin your schedule like this:
        Schedule starts on [Date]
    """))
    print("Paste your events below (one per line). Finish input by pressing Enter twice:\n")


def sentence_instructions():
    print(
        dedent("""
            [Course Name] in [Location] from [Start Time] to [End Time] every [Day] by [Teacher]
            Example: Math in Room 101 from 10:00 to 11:00 every Monday by Mr. Smith
        """)
    )


def read_block() -> list[str]:
    # Read multi-line block from stdin until double Enter (empty line)
    block = []
    while True:
        line = input()
        if not line.strip():
            break
        block.append(line.strip())

    if not block:
        Logger.warning("No input lines were provided for schedule.")

    return block
