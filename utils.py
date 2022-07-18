
import os
import re


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



def format_path(path):
    path = path.strip(" '\"").replace("'\\''", "'").replace("\\", "/") + "/"
    path = re.sub("/+$", "/", path)
    return path


def setup(origin_path):
    """Do basic checks and return the usable path
    and list of files of the entered folder.
    """

    # TODO: it's not so efficient, maybe os.getcwd() was good enough.
    realpath = os.path.realpath(__file__).replace("\\", "/")
    realpath = realpath[:realpath.rindex("/")]

    # If the input path is invalid,
    # create a folder called 'songs' in the current path
    # and use it as the 'origin_path'.
    origin_path = format_path(origin_path)
    if origin_path in ["/", "./", "//"] or not os.path.isdir(origin_path):
        origin_path = realpath + "/songs/"
        if not os.path.isdir(origin_path):
            os.mkdir(origin_path)

    # Get the list of all files in the 'origin_path'.
    origin_files = sorted(os.listdir(origin_path))
    if not origin_files:
        print("\n This folder is empty!\n")
        raise SystemExit

    return origin_path, origin_files
