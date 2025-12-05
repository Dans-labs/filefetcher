import filefetcher as ff

PIDS = ["http://hdl.handle.net/21.T15999/01BYJvzYl"]

def main():
    try:
        for pid in PIDS:
            file_list = ff.file_raw_records(pid)
            print(f"Fetched raw file list for PID {pid}:")
            print(file_list)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

