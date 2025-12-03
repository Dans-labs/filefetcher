import filefetcher.core as core


def file_records(pid: str):
    """Fetch file information by its pid.

    Args:
        pid (str): The pid of the file.

    Returns:
        dict: A dictionary containing file information.
    """
    return core.fetch_file_info(pid)

def file_extensions(pid: str):
    """Fetch file extensions by its pid.

    Args:
        pid (str): The pid of the file.

    Returns:
        set: A set of unique file extensions.
    """
    return core.fetch_file_extensions(pid)

def file_mime_types(pid: str):
    """Fetch file mime types by its pid.

    Args:
        pid (str): The pid of the file.

    Returns:
        set: A set of unique file mime types.
    """
    return core.fetch_file_mime_types(pid)
