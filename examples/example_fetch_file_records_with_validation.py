import filefetcher as ff

PIDS = ["10.17026/DANS-XGB-TW5U", "http://hdl.handle.net/21.T15999/01BYJvzYl"]

def main():
    try:
        for pid in PIDS:
            file_list = ff.file_records(pid)
            print(f"Fetched file list for PID {pid}:")
            for file in file_list:
                valid = ff.validate_file_record(file)               
                print(f"  File: {file['name']}, Valid: {valid}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

