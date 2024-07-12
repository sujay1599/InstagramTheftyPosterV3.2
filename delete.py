import os

def delete_uploaded_files():
    log_filename = 'upload_log.txt'
    downloads_dir = 'downloads'

    if os.path.exists(log_filename):
        with open(log_filename, 'r') as log_file:
            uploaded_reels = set(line.strip() for line in log_file)
    else:
        print("No upload log found.")
        return

    for filename in os.listdir(downloads_dir):
        base_filename = '_'.join(filename.split('_')[:2])  # Extract username and reel_id part
        if base_filename in uploaded_reels:
            file_path = os.path.join(downloads_dir, filename)
            try:
                os.remove(file_path)
                print(f"Deleted file: {filename}")
            except Exception as e:
                print(f"Failed to delete {filename}: {e}")

if __name__ == "__main__":
    delete_uploaded_files()
