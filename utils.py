
from pathlib import Path


# Number of
successful = 0
unsuccessful = 0


def report(is_successful, message=""):
    """Count the number of successful and
    unsuccessful lyrics attachments.
    """

    global successful, unsuccessful
    if is_successful:
        successful += 1
    else:
        unsuccessful += 1

    if message:
        print(message)


def print_report(suc_title, unsuc_title):
    print(
        f"\n\n\n {suc_title}: {successful}",
        f"\n {unsuc_title}: {unsuccessful}"
    )


def print_header(path, files):
    print("\n" + "─"*len(path) + "──┐")
    print(" " + path + " │", len(files))
    print("─"*len(path) + "──┘")


def format_path(path):
    path = path.strip(" '\"").replace("'\\''", "'")
    path = Path(path).expanduser().resolve()
    return path
