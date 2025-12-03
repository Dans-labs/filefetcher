# filefetcher

Fetches file information for a given PID, DOI, or URL.

## Installation

```
uv add https://github.com/Dans-labs/filefetcher.git
```

## Usage

```python
from filefetcher import api as ff
DOI = "10.5072/FK2/ABCDE"
files = ff.file_records(DOI)
file_extensions = ff.file_extensions(DOI)
file_mimetypes = ff.file_mime_types(DOI)
```

## File record schema

`file_records` return a list of files following this schema:

```json
[
  {
    "name": "example.txt",
    "link": "https://example.com/example.txt",
    "size": 1024,
    "mime_type": "text/plain",
    "checksum_value": "abc123",
    "checksum_type": "md5",
    "access_request": False,
    "publication_date": "Some non standard date string",
    "embargo": "Some non standard date string or None",
    "file_pid": "unique-file-identifier, which is null most of the time",
    "dataset_pid": "parent dataset identifier"
  }
]
```
