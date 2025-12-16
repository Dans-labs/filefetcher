import asyncio
import logging
import importlib
import pkgutil
import mimetypes
import json
import jsonschema
from jsonschema import FormatChecker

from pathlib import Path

logger = logging.getLogger(__name__)


ADAPTOR_FOLDER = Path(__file__).parent / "adaptors"
SCHEMA_FILE = Path(__file__).parent / "file_record.schema.json"

class RepositoryNotSupported(Exception):
    pass

def load_adaptors():
    """Dynamically load all adaptors in the adaptors folder."""
    adaptors = {}
    adaptor_priority_list = []
    package_name = "filefetcher.adaptors"

    for finder, name, ispkg in pkgutil.iter_modules([str(ADAPTOR_FOLDER)]):
        module_name = f"{package_name}.{name}"
        module = importlib.import_module(module_name)
        if hasattr(module, "info") and callable(module.info):
            adaptors[name] = module
            adaptor_priority_list.append((name, getattr(module, "PRIORITY", 100)))
    # Sort adaptors by priority
    adaptor_priority_list.sort(key=lambda x: x[1])
    adaptor_priority_list = [name for name, _ in adaptor_priority_list]
    return (adaptors, adaptor_priority_list)

# Automatically load adaptors on import
(adaptors, adaptor_priority_list) = load_adaptors()
file_record_schema = None

# Load JSON Schema
with open(SCHEMA_FILE, "r") as f:
    file_record_schema = json.load(f)

def validate_file_record(file_record: dict) -> bool:
    try:
        jsonschema.validate(instance=file_record, schema=file_record_schema, format_checker=FormatChecker())
        return True
    except jsonschema.ValidationError as e:
        logger.error(f"File record validation error: {e.message}")
        return False

async def fetch_file_info(pid: str) -> list:
    metadata = []
    errors = []
    for adaptor_name in adaptor_priority_list:
        m = adaptors[adaptor_name]
        try:
            metadata = await asyncio.to_thread(m.files, pid)
            if metadata:
                break
        except RepositoryNotSupported as e:
            errors.append((adaptor_name, str(e)))
            continue

    if len(errors) == len(adaptor_priority_list):
        error_messages = "; ".join([f"{name}: {msg}" for name, msg in errors])
        raise RepositoryNotSupported(f"All adaptors failed for PID {pid}. Errors: {error_messages}")
    return metadata

async def fetch_raw_file_info(pid: str) -> dict:
    raw_metadata = None
    errors = []
    for adaptor_name in adaptor_priority_list:
        m = adaptors[adaptor_name]
        try:
            metadata = await asyncio.to_thread(m.info, pid)
            if metadata:
                raw_metadata = metadata.files
                break
        except RepositoryNotSupported as e:
            errors.append((adaptor_name, str(e)))
            continue

    if len(errors) == len(adaptor_priority_list):
        error_messages = "; ".join([f"{name}: {msg}" for name, msg in errors])
        raise RepositoryNotSupported(f"All adaptors failed for PID {pid}. Errors: {error_messages}")
    return {
            "files": raw_metadata
    }

async def fetch_file_name_and_type(pid:str) -> list:
    files = await fetch_file_info(pid)
    name_and_type = [(r['name'], r['mime_type']) for r in files]
    return name_and_type

async def fetch_file_mime_types(pid:str) -> list:
    files = await fetch_file_info(pid)
    unique_types = list({r['mime_type'] for r in files})
    return unique_types

async def fetch_file_extensions(pid:str) -> list:
    files = await fetch_file_info(pid)
    extensions = {Path(r['name']).suffix.lower() for r in files}
    # Handle files without extensions
    # by guessing from mime type
    records_without_extension = [r for r in files if not Path(r['name']).suffix]
    for r in records_without_extension:
        mime_type = r.get('mime_type')
        if mime_type and (ext := mimetypes.guess_extension(mime_type)):
                extensions.add(ext.lower())
    # Remove empty string if present
    extensions.discard('')  
    return list(extensions)
