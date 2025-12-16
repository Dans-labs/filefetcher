import filefetcher as ff

pid = "https://zenodo.org/records/15222400"

def main():
    file_records = ff.file_records(pid)
    file_list = ff.file_extensions(pid)
    file_mime_types = ff.file_mime_types(pid)
    print("Fetched file records:")
    print(file_records)
    print(f"Fetched file extension and mime-types for PID {pid}:")
    print(file_list)
    print(file_mime_types)

if __name__ == "__main__":
    main()

