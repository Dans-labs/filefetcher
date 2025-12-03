# examples/example_usage.py
import asyncio
from filefetcher import core

PIDS = ["10.17026/DANS-XGB-TW5U", "http://hdl.handle.net/21.T15999/01BYJvzYl"]

async def main():
    try:
        for pid in PIDS:
            file_list = await core.fetch_raw_file_info(pid)
            print(f"Fetched file list for PID {pid}:")
            print(file_list)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

