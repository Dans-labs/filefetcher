import datahugger
import logging
from filefetcher.core import RepositoryNotSupported
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)

PRIORITY = 0

def test():
    logger.debug("Loaded Datahugger adaptor.")
    return True

@lru_cache(maxsize=128)
def info(identifier: str):
    try:
        metadata = datahugger.info(identifier, {"type": "file"})
        return metadata
    except datahugger.RepositoryNotSupportedError as e:
        raise RepositoryNotSupported(e)

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
    file_records = []
    metadata = info(identifier)
    if not metadata:
        return []
    files = metadata.files
    for file in files:
        logger.debug(f"Processing file: {file.get('name')}")
        if 'raw_metadata' not in file:
            logger.warning(f"File {file.get('name')} is missing raw_metadata.")
        record = {}
        record['name'] = file.get('name')
        record['link'] = file.get('link')
        record['size'] = file.get('size')
        record['mime_type'] = file.get('raw_metadata', {}).get('contentType')
        record['ext'] = Path(record['name']).suffix.lower()
        checksum_value, checksum_type = _get_checksum(file)
        record['checksum_value'] = checksum_value
        record['checksum_type'] = checksum_type
        record['access_request'] = file.get('raw_metadata', {}).get('fileAccessRequest')
        record['publication_date'] = file.get('raw_metadata', {}).get('publicationDate')
        embargo = file.get('raw_metadata', {}).get('embargo', {})
        if isinstance(embargo, dict):
            record['embargo'] = file.get('raw_metadata', {}).get('embargo', {}).get('dateAvailable')
        else:
            record['embargo'] = embargo
        record['file_pid'] = None
        record['dataset_pid'] = identifier
        file_records.append(record)
        
    return file_records



