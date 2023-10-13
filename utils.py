
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
        f"\n\n\n {suc_title}: {successful}"
        f"\n {unsuc_title}: {unsuccessful}"
    )


def get_header(path, full_path=True):
    files_num = sum(file.is_file() for file in path.iterdir())
    title = path.name
    if full_path:
        title = str(path)
    return (f"\n┌─{'─'*len(title)}─┐" +
            f"\n│ {title} │ {files_num}" +
            f"\n└─{'─'*len(title)}─┘")


def format_path(path):
    path = path.strip(" '\"").replace("'\\''", "'")
    path = Path(path).expanduser().resolve()
    return path


def is_valid_dir(path):
    if (path in ["", "/", "."]
        or not path.is_dir()
        or path.samefile("/")
        or path.samefile(Path())
        or path.samefile(Path.home())):
        return False
    return True
