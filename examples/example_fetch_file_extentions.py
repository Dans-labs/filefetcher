# examples/example_usage.py
from filefetcher import api as ff

PIDS = ["10.17026/DANS-XGB-TW5U", "http://hdl.handle.net/21.T15999/01BYJvzYl"]

def main():
    try:
        for pid in PIDS:
            file_list = ff.file_extensions(pid)
            file_mime_types = ff.file_mime_types(pid)
            print(f"Fetched file extension and mime-types for PID {pid}:")
            print(file_list)
            print(file_mime_types)
            print("-" * 40)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

