import os
import yaml
import json
from cryptography.fernet import Fernet
from instagrapi import Client
from time import sleep, time
from datetime import datetime, timedelta
import moviepy.editor as mp
import subprocess

# Delete status.json and last_scraped_timestamp.txt if they exist
status_file = 'status.json'
last_scraped_file = 'last_scraped_timestamp.txt'

if os.path.exists(status_file):
    os.remove(status_file)
    print('Deleted status.json')

if os.path.exists(last_scraped_file):
    os.remove(last_scraped_file)
    print('Deleted last_scraped_timestamp.txt')

# Load configuration
def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# Decrypt credentials
def decrypt_credentials(config):
    key = config['key'].encode()
    cipher_suite = Fernet(key)
    username = cipher_suite.decrypt(config['instagram']['username'].encode()).decode()
    password = cipher_suite.decrypt(config['instagram']['password'].encode()).decode()
    return username, password

INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD = decrypt_credentials(config)

# Initialize variables from config
SCRAPING_ENABLED = config['scraping']['enabled']
UPLOAD_ENABLED = config['uploading']['enabled']
NUM_REELS = config['scraping']['num_reels']
USE_HASHTAGS = config['hashtags']['use_hashtags']
HASHTAGS_LIST = config['hashtags'].get('hashtags_list', '')
UPLOAD_INTERVAL_MINUTES = config['uploading']['upload_interval_minutes']
ADD_TO_STORY = config['uploading']['add_to_story']
SCRAPE_INTERVAL_MINUTES = config['scraping']['scrape_interval_minutes']
DELETE_INTERVAL_MINUTES = config['deleting']['delete_interval_minutes']
USE_ORIGINAL_DESCRIPTION = config['description']['use_original']
CUSTOM_DESCRIPTION = config['description'].get('custom_description', '')
GIVE_CREDIT = config['credit']['give_credit']

# Initialize Instagram client
cl = Client()
session_file = 'session.json'
log_filename = 'upload_log.txt'

default_status = {
    "last_scrape_time": None,
    "next_scrape_time": None,
    "reels_scraped": [],
    "last_upload_time": None,
    "next_upload_time": None,
    "last_story_upload_time": None,
    "next_story_upload_time": None,
    "last_delete_time": None
}

def initialize_status_file():
    if not os.path.exists(status_file):
        with open(status_file, 'w') as f:
            json.dump(default_status, f, indent=4, default=str)

initialize_status_file()

def update_status(**kwargs):
    status = default_status.copy()  # Start with default status
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            status.update(json.load(f))  # Update with current status
    
    status.update(kwargs)  # Update with new values
    
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=4, default=str)

def read_status():
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            status = json.load(f)
            # Convert times to float
            for key in ["last_scrape_time", "next_scrape_time", "last_upload_time", "next_upload_time", "last_story_upload_time", "next_story_upload_time", "last_delete_time"]:
                if status[key] is not None and isinstance(status[key], str):
                    status[key] = datetime.strptime(status[key], "%Y-%m-%d %H:%M:%S.%f").timestamp()
            return status
    return default_status

status = read_status()

# Initialize last_scraped_timestamp
last_scraped_timestamp = 0

def login():
    if os.path.exists(session_file):
        try:
            cl.load_settings(session_file)
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            print("Logged in using session file")
        except Exception as e:
            print(f"Failed to login using session file: {e}")
            try:
                cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
                cl.dump_settings(session_file)
                print("Logged in using username and password, session file updated")
            except Exception as e:
                print(f"Username/password login failed: {e}")
                exit(1)
    else:
        try:
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            cl.dump_settings(session_file)
            print("Logged in using username and password, session file created")
        except Exception as e:
            print(f"Username/password login failed: {e}")
            exit(1)

# Perform login
login()

if os.path.exists(log_filename):
    with open(log_filename, 'r') as log_file:
        uploaded_reels = set(line.strip() for line in log_file)
else:
    uploaded_reels = set()

def get_unuploaded_reels():
    downloads_dir = 'downloads'
    unuploaded_reels = []
    for filename in os.listdir(downloads_dir):
        if filename.endswith('.mp4'):
            reel_id = filename.split('_')[1].split('.')[0]
            if reel_id not in uploaded_reels:
                unuploaded_reels.append(filename)
    return unuploaded_reels

def scrape_reels(username, num_reels):
    global last_scraped_timestamp
    user_id = cl.user_id_from_username(username)
    all_downloaded_reels = []
    downloaded_reels = []
    while len(downloaded_reels) < num_reels:
        try:
            reels = cl.user_clips(user_id, amount=50)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e} - Retrying in 5 seconds")
            sleep(5)
            continue
        except Exception as e:
            print(f"Error fetching reels: {e}")
            break

        if not reels:
            break

        for reel in reels:
            reel_timestamp = reel.taken_at.timestamp()
            reel_filename = f"{username}_{reel.pk}.mp4"
            expected_media_path = os.path.join('downloads', reel_filename)

            if reel.pk in uploaded_reels or os.path.exists(expected_media_path):
                continue

            if reel_timestamp <= last_scraped_timestamp:
                continue

            try:
                media_path = cl.clip_download(reel.pk, folder='downloads')
            except Exception as e:
                print(f"Failed to download reel {reel.pk}: {e}")
                continue

            if os.path.exists(media_path):
                description_path = os.path.join('downloads', f'{reel.pk}.txt')
                with open(description_path, 'w', encoding='utf-8') as f:
                    f.write(reel.caption_text)
                print(f"Scraped and saved reel: {reel.pk}")
                downloaded_reels.append(reel)
                all_downloaded_reels.append(f"{username}_{reel.pk}")
                if len(downloaded_reels) >= num_reels:
                    break

    if downloaded_reels:
        last_scraped_timestamp = max(reel.taken_at.timestamp() for reel in downloaded_reels)
        with open(last_scraped_file, 'w') as file:
            file.write(str(int(last_scraped_timestamp)))

        update_status(
            last_scrape_time=datetime.now().timestamp(),
            next_scrape_time=(datetime.now() + timedelta(minutes=SCRAPE_INTERVAL_MINUTES)).timestamp(),
            reels_scraped=all_downloaded_reels
        )

    return downloaded_reels

def build_description(original_description, profile_username):
    if USE_ORIGINAL_DESCRIPTION:
        description = original_description
    else:
        description = CUSTOM_DESCRIPTION

    if USE_HASHTAGS:
        description += f"\n{HASHTAGS_LIST}"

    if GIVE_CREDIT:
        description += f"\nTaken from: @{profile_username}"

    return description

def upload_reels_with_new_descriptions(unuploaded_reels):
    if not unuploaded_reels:
        print("No new reels to upload.")
        return
    for reel_file in unuploaded_reels:
        reel_id = reel_file.split('_')[1].split('.')[0]
        profile_username = reel_file.split('_')[0]
        media_path = os.path.join('downloads', reel_file)
        description_path = os.path.join('downloads', f'{reel_id}.txt')
        if not os.path.exists(media_path) or f"{profile_username}_{reel_id}" in uploaded_reels:
            print(f"Media file {media_path} not found or already uploaded. Skipping upload for reel: {reel_id}")
            continue

        # Read original description
        with open(description_path, 'r', encoding='utf-8') as f:
            original_description = f.read()

        # Build the final description
        new_description = build_description(original_description, profile_username)
        
        # Upload to Instagram feed
        cl.clip_upload(media_path, new_description)
        print(f"Uploaded reel: {reel_id} with description: {new_description}")
        
        # Upload to Instagram story
        if ADD_TO_STORY:
            cl.video_upload_to_story(media_path, new_description)
            print(f"Added reel: {reel_id} to story")
        
        # Release video file resources using moviepy
        video = mp.VideoFileClip(media_path)
        video.reader.close()
        if video.audio:
            video.audio.reader.close_proc()
        
        # Log the upload
        with open(log_filename, 'a') as log_file:
            log_file.write(f"{profile_username}_{reel_id}\n")
        
        # Update the set of uploaded reels
        uploaded_reels.add(f"{profile_username}_{reel_id}")
        
        update_status(
            last_upload_time=datetime.now().timestamp(),
            next_upload_time=(datetime.now() + timedelta(minutes=UPLOAD_INTERVAL_MINUTES)).timestamp()
        )
        
        if ADD_TO_STORY:
            update_status(
                last_story_upload_time=datetime.now().timestamp(),
                next_story_upload_time=(datetime.now() + timedelta(minutes=UPLOAD_INTERVAL_MINUTES)).timestamp()
            )

        # Show the dashboard after each upload
        show_dashboard()

        next_upload_time = datetime.now() + timedelta(minutes=UPLOAD_INTERVAL_MINUTES)
        print(f"Next upload at: {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Waiting for {UPLOAD_INTERVAL_MINUTES} minutes before next upload.")
        sleep(UPLOAD_INTERVAL_MINUTES * 60)

def show_dashboard():
    subprocess.run(["python", "dashboard.py"])  # Call dashboard.py

def main():
    global last_scraped_timestamp
    
    status = read_status()
    
    # Initialize times if they are None
    last_scrape_time = status.get("last_scrape_time")
    if last_scrape_time is None:
        last_scrape_time = time() - (SCRAPE_INTERVAL_MINUTES * 60)

    last_upload_time = status.get("last_upload_time")
    if last_upload_time is None:
        last_upload_time = time() - (UPLOAD_INTERVAL_MINUTES * 60)

    last_delete_time = status.get("last_delete_time")
    if last_delete_time is None:
        last_delete_time = 0

    # Initialize last_scraped_timestamp from file if it exists
    if os.path.exists(last_scraped_file):
        with open(last_scraped_file, 'r') as file:
            try:
                last_scraped_timestamp = int(file.read().strip())
            except ValueError:
                last_scraped_timestamp = 0

    while True:
        current_time = time()

        if (current_time - last_scrape_time) >= SCRAPE_INTERVAL_MINUTES * 60:
            if SCRAPING_ENABLED:
                for profile in config['scraping']['profiles'].split():
                    print(f"Scraping profile: {profile}")
                    scrape_reels(profile, num_reels=NUM_REELS)
                last_scrape_time = current_time
                update_status(last_scrape_time=last_scrape_time, next_scrape_time=current_time + SCRAPE_INTERVAL_MINUTES * 60)

        if (current_time - last_upload_time) >= UPLOAD_INTERVAL_MINUTES * 60:
            if UPLOAD_ENABLED:
                upload_reels_with_new_descriptions(get_unuploaded_reels())
                last_upload_time = current_time
                update_status(last_upload_time=last_upload_time, next_upload_time=current_time + UPLOAD_INTERVAL_MINUTES * 60)

        # Check if it's time to run delete.py
        if (current_time - last_delete_time) >= DELETE_INTERVAL_MINUTES * 60:
            print("Running delete.py")
            subprocess.run(["python", "delete.py"])
            last_delete_time = current_time
            update_status(last_delete_time=last_delete_time)

        sleep(60)

if __name__ == "__main__":
    main()
