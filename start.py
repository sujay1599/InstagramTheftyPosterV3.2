import yaml
from cryptography.fernet import Fernet
import getpass
import os

def get_input(prompt, input_type=str, retries=3):
    while retries > 0:
        try:
            return input_type(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
            retries -= 1
    raise ValueError("Too many invalid attempts.")

def get_boolean_input(prompt):
    return input(prompt).strip().lower() in ['true', 'yes', 'y']

# Generate a key and instantiate a Fernet instance
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Get credentials from the user
username = input('Enter Instagram username: ').encode()
password = getpass.getpass('Enter Instagram password: ').encode()  # Use getpass to hide input

# Encrypt the credentials
encrypted_username = cipher_suite.encrypt(username).decode()
encrypted_password = cipher_suite.encrypt(password).decode()

# Store the encrypted credentials and the encryption key in the config
config = {
    'instagram': {
        'username': encrypted_username,
        'password': encrypted_password
    },
    'key': key.decode(),  # Store the encryption key in the config
    'scraping': {
        'enabled': get_boolean_input('Enable scraping? (true/false): '),
        'profiles': input('Enter profiles to scrape (space separated): '),
        'num_reels': get_input('Number of reels to scrape per profile: ', int),
        'scrape_interval_minutes': get_input('Interval between scrapes (minutes): ', int),
        'like_reels': get_boolean_input('Like scraped videos? (true/false): ')
    },
    'uploading': {
        'enabled': get_boolean_input('Enable uploading? (true/false): '),
        'upload_interval_minutes': get_input('Interval between uploads (minutes): ', int),
        'add_to_story': get_boolean_input('Add to story? (true/false): ')
    }
}

# Ask about using the original description
use_original_description = get_boolean_input('Use original description? (true/false): ')
config['description'] = {
    'use_original': use_original_description
}

if use_original_description:
    # Ask about hashtags and credit if using original description
    use_hashtags = get_boolean_input('Add hashtags? (true/false): ')
    config['hashtags'] = {
        'use_hashtags': use_hashtags
    }
    if use_hashtags:
        config['hashtags']['hashtags_list'] = input('Enter hashtags (space separated): ')

    give_credit = get_boolean_input('Give credit? (true/false): ')
    config['credit'] = {
        'give_credit': give_credit
    }
else:
    # Ask for custom description, hashtags, and credit if not using original description
    custom_description = input('Enter custom description: ')
    config['description']['custom_description'] = custom_description

    use_hashtags = get_boolean_input('Add hashtags? (true/false): ')
    config['hashtags'] = {
        'use_hashtags': use_hashtags
    }
    if use_hashtags:
        config['hashtags']['hashtags_list'] = input('Enter hashtags (space separated): ')

    give_credit = get_boolean_input('Give credit? (true/false): ')
    config['credit'] = {
        'give_credit': give_credit
    }

# Adding user-defined comments for scraped videos
leave_comment = get_boolean_input('Leave comment on scraped videos? (true/false): ')
config['leave_comment'] = leave_comment

if leave_comment:
    config['comments'] = input('Enter comments (comma separated): ').split(',')

# Deleting logic - capture the interval for running delete.py
config['deleting'] = {
    'delete_interval_minutes': get_input('Interval between deletions (minutes): ', int)
}

# Save the config to a file
with open('config.yaml', 'w') as file:
    yaml.dump(config, file)

print('Configuration saved to config.yaml')

# Delete status.json, last_scraped_timestamp.txt, and random-upload-times.json if they exist
status_file = 'status.json'
last_scraped_file = 'last_scraped_timestamp.txt'
random_upload_time_file = 'random-upload-times.json'

for file in [status_file, last_scraped_file, random_upload_time_file]:
    if os.path.exists(file):
        os.remove(file)
        print(f'Deleted {file}')
