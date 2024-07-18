import os
import json
from rich.console import Console
from datetime import datetime

status_file = 'status.json'
log_file = 'upload_log.txt'
downloads_dir = 'downloads'
console = Console()

def read_status():
    if not os.path.exists(status_file):
        console.print("[bold red]Status file not found.[/bold red]")
        return {}
    with open(status_file, 'r') as f:
        status = json.load(f)
    return status

def update_status(**kwargs):
    status = read_status()
    status.update(kwargs)
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=4, default=str)

def read_upload_log():
    if not os.path.exists(log_file):
        console.print("[bold red]Upload log file not found.[/bold red]")
        return []
    with open(log_file, 'r') as f:
        uploads = f.readlines()
    return [upload.strip() for upload in uploads]

def delete_uploaded_files():
    upload_log = read_upload_log()
    if not upload_log:
        console.print("[bold yellow]No files to delete.[/bold yellow]")
        return

    deleted_files = []
    for log_entry in upload_log:
        file_prefix = log_entry
        for extension in ['.mp4', '.txt', '.mp4.jpg']:
            file_path = os.path.join(downloads_dir, file_prefix + extension)
            if os.path.exists(file_path):
                os.remove(file_path)
                deleted_files.append(file_path)
                console.print(f"[bold green]Deleted file:[/bold green] {file_path}")

    if deleted_files:
        update_status(
            last_delete_time=datetime.now().timestamp()
        )
    else:
        console.print("[bold yellow]No matching files found to delete.[/bold yellow]")

def main():
    delete_uploaded_files()

if __name__ == "__main__":
    main()
