from filefetcher import api as ff

PIDS = ["10.17026/DANS-XGB-TW5U", "http://hdl.handle.net/21.T15999/01BYJvzYl"]

def main():
    try:
        for pid in PIDS:
            file_list = ff.file_records(pid)
            print(f"Fetched file list for PID {pid}:")
            print(file_list)
            print("-" * 40)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

