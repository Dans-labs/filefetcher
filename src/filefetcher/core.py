import asyncio
import logging
import importlib
import pkgutil
import json
import jsonschema
from jsonschema import FormatChecker

from pathlib import Path

logger = logging.getLogger(__name__)


ADAPTOR_FOLDER = Path(__file__).parent / "adaptors"
SCHEMA_FILE = Path(__file__).parent / "file_record.schema.json"

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

async def fetch_file_info(pid: str) -> dict:
    metadata = []
    for adaptor_name in adaptor_priority_list:
        m = adaptors[adaptor_name]
        metadata = await asyncio.to_thread(m.files, pid)
        if metadata:
            break
    return metadata

async def fetch_raw_file_info(pid: str) -> dict:
    raw_metadata = None
    for adaptor_name in adaptor_priority_list:
        m = adaptors[adaptor_name]
        metadata = await asyncio.to_thread(m.info, pid)
        if metadata:
            raw_metadata = metadata.files
            break
    return {
            "adaptor": adaptor_name,
            "files": raw_metadata
    }

async def fetch_file_mime_types(pid:str) -> list:
    files = await fetch_file_info(pid)
    unique_types = list({r['mime_type'] for r in files})
    return unique_types

async def fetch_file_extensions(pid:str) -> list:
    files = await fetch_file_info(pid)
    extensions = list({Path(r['name']).suffix for r in files})
    return extensions
