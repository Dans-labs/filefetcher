import asyncio
import filefetcher.core as core


def file_records(pid: str):
    """Fetch file information by its pid.

    Args:
        pid (str): The pid of the file.

    Returns:
        dict: A dictionary containing file information.
    """
    return asyncio.run(core.fetch_file_info(pid))

def file_extensions(pid: str):
    """Fetch file extensions by its pid.

    Args:
        pid (str): The pid of the file.

    Returns:
        set: A set of unique file extensions.
    """
    return asyncio.run(core.fetch_file_extensions(pid))

def file_mime_types(pid: str):
    """Fetch file mime types by its pid.

    Args:
        pid (str): The pid of the file.

    Returns:
        set: A set of unique file mime types.
    """
    return asyncio.run(core.fetch_file_mime_types(pid))

def file_name_and_types(pid: str):
    """Fetch file names and mime types by its pid.

    Args:
        pid (str): The pid of the file.

    Returns:
        list: A list of tuples containing file names and mime types.
    """
    return asyncio.run(core.fetch_file_name_and_type(pid))

def validate_file_record(file_record: dict):
    """Validate a file record against the JSON schema.

    Args:
        file_record (dict): The file record to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return core.validate_file_record(file_record)
