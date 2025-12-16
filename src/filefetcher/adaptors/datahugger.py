import datahugger
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

PRIORITY = 0

def test():
    logger.debug("Loaded Datahugger adaptor.")
    return True

@lru_cache(maxsize=128)
def info(identifier: str):
    metadata = datahugger.info(identifier, {"type": "file"})
    return metadata

def _get_checksum(obj: dict):
    checksum_info = obj.get('raw_metadata', {}).get('checksum', {})
    if isinstance(checksum_info, str):
        parts = checksum_info.split(':', 1)
        if len(parts) == 2:
            return parts[1], parts[0]
        else:
            return checksum_info, None
    if (isinstance(checksum_info, dict) 
        and checksum_info.get("value") is not None
        and checksum_info.get("type") is not None
    ):
        return checksum_info.get('value'), checksum_info.get('type')

    return checksum_info, None

def files(identifier: str):
    print("here")
    file_records = []
    metadata = info(identifier)
    if not metadata:
        return []
    files = metadata.files
    for file in files:
        print("there", file)
        logger.info(f"Processing file: {file.get('name')}")
        record = {}
        record['name'] = file.get('name')
        record['link'] = file.get('link')
        record['size'] = file.get('size')
        record['mime_type'] = file.get('raw_metadata', {}).get('contentType')
        checksum_value, checksum_type = _get_checksum(file)
        record['checksum_value'] = checksum_value
        record['checksum_type'] = checksum_type
        record['access_request'] = file.get('raw_metadata', {}).get('fileAccessRequest')
        record['publication_date'] = file.get('raw_metadata', {}).get('publicationDate')
        record['embargo'] = file.get('raw_metadata', {}).get('embargo', {}).get('dateAvailable')
        record['file_pid'] = None
        record['dataset_pid'] = identifier
        file_records.append(record)
        
    return file_records



