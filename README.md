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
