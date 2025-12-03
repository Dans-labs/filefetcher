import filefetcher.core as core


def file_records(pid: str):
    """Fetch file information by its pid.

    Args:
        pid (str): The pid of the file.

    Returns:
        dict: A dictionary containing file information.
    """
    return core.fetch_file_info(pid)
