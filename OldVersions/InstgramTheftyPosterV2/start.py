import yaml
from cryptography.fernet import Fernet
import getpass
import os

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
        'enabled': input('Enable scraping? (true/false): ').lower() == 'true',
        'profiles': input('Enter profiles to scrape (space separated): '),
        'num_reels': int(input('Number of reels to scrape per profile: ')),
        'scrape_interval_minutes': int(input('Interval between scrapes (minutes): '))
    },
    'uploading': {
        'enabled': input('Enable uploading? (true/false): ').lower() == 'true',
        'upload_interval_minutes': int(input('Interval between uploads (minutes): ')),
        'add_to_story': input('Add to story? (true/false): ').lower() == 'true'
    }
}

# Ask about using the original description
use_original_description = input('Use original description? (true/false): ').lower() == 'true'
config['description'] = {
    'use_original': use_original_description
}

if use_original_description:
    # Ask about hashtags and credit if using original description
    use_hashtags = input('Add hashtags? (true/false): ').lower() == 'true'
    config['hashtags'] = {
        'use_hashtags': use_hashtags
    }
    if use_hashtags:
        config['hashtags']['hashtags_list'] = input('Enter hashtags (space separated): ')

    give_credit = input('Give credit? (true/false): ').lower() == 'true'
    config['credit'] = {
        'give_credit': give_credit
    }
else:
    # Ask for custom description, hashtags, and credit if not using original description
    custom_description = input('Enter custom description: ')
    config['description']['custom_description'] = custom_description

    use_hashtags = input('Add hashtags? (true/false): ').lower() == 'true'
    config['hashtags'] = {
        'use_hashtags': use_hashtags
    }
    if use_hashtags:
        config['hashtags']['hashtags_list'] = input('Enter hashtags (space separated): ')

    give_credit = input('Give credit? (true/false): ').lower() == 'true'
    config['credit'] = {
        'give_credit': give_credit
    }

# Deleting logic - capture the interval for running delete.py
config['deleting'] = {
    'delete_interval_minutes': int(input('Interval between deletions (minutes): '))
}

# Save the config to a file
with open('config.yaml', 'w') as file:
    yaml.dump(config, file)

print('Configuration saved to config.yaml')

# Delete status.json and last_scraped_timestamp.txt if they exist
status_file = 'status.json'
last_scraped_file = 'last_scraped_timestamp.txt'

if os.path.exists(status_file):
    os.remove(status_file)
    print('Deleted status.json')

if os.path.exists(last_scraped_file):
    os.remove(last_scraped_file)
    print('Deleted last_scraped_timestamp.txt')
