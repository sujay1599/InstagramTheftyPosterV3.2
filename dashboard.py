import os
import json

status_file = 'status.json'

def read_status():
    if not os.path.exists(status_file):
        print("Status file not found.")
        return {}
    with open(status_file, 'r') as f:
        status = json.load(f)
    return status

def print_status(status):
    print("Scrape Status:")
    print(f"  Last Scrape Time: {status.get('last_scrape_time')}")
    print(f"  Next Scrape Time: {status.get('next_scrape_time')}")
    print(f"  Reels Scraped: {status.get('reels_scraped', [])}")
    
    print("\nUpload Status:")
    print(f"  Last Upload Time: {status.get('last_upload_time')}")
    print(f"  Next Upload Time: {status.get('next_upload_time')}")
    
    if 'last_story_upload_time' in status:
        print("\nStory Upload Status:")
        print(f"  Last Story Upload Time: {status.get('last_story_upload_time')}")
        print(f"  Next Story Upload Time: {status.get('next_story_upload_time')}")
    
    if 'last_deletion_time' in status:
        print("\nDeletion Status:")
        print(f"  Last Deletion Time: {status.get('last_deletion_time')}")
        print(f"  Next Deletion Time: {status.get('next_deletion_time')}")

def main():
    status = read_status()
    if status:
        print_status(status)

if __name__ == "__main__":
    main()
