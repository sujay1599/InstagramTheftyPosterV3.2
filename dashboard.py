import os
import json
from rich.console import Console
from rich.table import Table
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

def read_upload_log():
    if not os.path.exists(log_file):
        console.print("[bold red]Upload log file not found.[/bold red]")
        return []
    with open(log_file, 'r') as f:
        uploads = f.readlines()
    return [upload.strip() for upload in uploads]

def get_file_counts():
    if not os.path.exists(downloads_dir):
        console.print("[bold red]Downloads directory not found.[/bold red]")
        return 0, 0, 0, 0
    total_files = [f for f in os.listdir(downloads_dir) if f.endswith('.mp4')]
    upload_log = read_upload_log()
    uploaded_files = [f for f in total_files if f.rsplit('.', 1)[0] in upload_log]
    unuploaded_files = [f for f in total_files if f not in uploaded_files]
    folder_size = sum(os.path.getsize(os.path.join(downloads_dir, f)) for f in os.listdir(downloads_dir)) / (1024 * 1024)  # size in MB
    return len(total_files), len(uploaded_files), len(unuploaded_files), folder_size

def format_time(timestamp):
    if not timestamp or timestamp == 'None':
        return "N/A"
    try:
        return datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "Invalid timestamp"

def main():
    status = read_status()
    if not status:
        return

    uploads = read_upload_log()
    total_files, uploaded_files, unuploaded_files, folder_size = get_file_counts()

    console.print("=" * 80, justify="left")
    console.print("[bold yellow]Instagram Thefty Poster Dashboard[/bold yellow]", justify="left")
    console.print("=" * 80, justify="left")

    # Scrape and Upload Status Table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Scrape Status", justify="center")
    table.add_column("Upload Status", justify="center")

    table.add_row(
        f"Last Scrape Time: {format_time(status.get('last_scrape_time'))}\nNext Scrape Time: {format_time(status.get('next_scrape_time'))}",
        f"Last Upload Time: {format_time(status.get('last_upload_time'))}\nNext Upload Time: {format_time(status.get('next_upload_time'))}"
    )

    console.print(table)

    # File Counts Table
    file_table = Table(show_header=True, header_style="bold magenta")
    file_table.add_column("Metric", justify="center")
    file_table.add_column("Value", justify="center")

    file_table.add_row("Total .mp4 Files", str(total_files))
    file_table.add_row("Uploaded .mp4 Files", str(uploaded_files))
    file_table.add_row("Unuploaded .mp4 Files", str(unuploaded_files))
    file_table.add_row("Downloads Folder Size (MB)", f"{folder_size:.2f}")

    console.print(file_table)

    # Last 10 Uploads
    console.print("[bold]Last 10 Uploads[/bold]")
    for upload in uploads[-10:]:
        console.print(f"- {upload}")

    # Reels Scraped
    console.print("[bold]Reels Scraped[/bold]")
    for reel in status.get('reels_scraped', []):
        console.print(f"- {reel}")

    # Story Upload and Deletion Status Table
    table2 = Table(show_header=True, header_style="bold magenta")
    table2.add_column("Story Upload Status", justify="center")
    table2.add_column("Deletion Status", justify="center")

    table2.add_row(
        f"Last Story Upload Time: {format_time(status.get('last_story_upload_time'))}\nNext Story Upload Time: {format_time(status.get('next_story_upload_time'))}",
        f"Last Deletion Time: {format_time(status.get('last_deletion_time'))}\nNext Deletion Time: {format_time(status.get('next_deletion_time'))}"
    )

    console.print(table2)

if __name__ == "__main__":
    main()
