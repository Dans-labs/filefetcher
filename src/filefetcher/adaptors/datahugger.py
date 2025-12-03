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
    try:
        metadata = datahugger.info(identifier, {"type": "file"})
        return metadata
    except Exception as e:
        logger.debug(f"Datahugger adaptor failed for identifier {identifier}: {e}.")
        return None

def files(identifier: str):
    file_records = []
    metadata = info(identifier)
    if not metadata:
        return []
    files = metadata.files
    for file in files:
        record = {}
        record['name'] = file.get('name')
        record['link'] = file.get('link')
        record['size'] = file.get('size')
        record['mime_type'] = file.get('raw_metadata', {}).get('contentType')
        record['checksum_value'] = file.get('raw_metadata', {}).get('checksum', {}).get('value')
        record['checksum_type'] = file.get('raw_metadata', {}).get('checksum', {}).get('type')
        record['access_request'] = file.get('raw_metadata', {}).get('fileAccessRequest')
        record['publication_date'] = file.get('raw_metadata', {}).get('publicationDate')
        record['embargo'] = file.get('raw_metadata', {}).get('embargo', {}).get('dateAvailable')
        record['file_pid'] = None
        record['dataset_pid'] = identifier
        file_records.append(record)
        
    return file_records



