# Instagram Thefty Poster V3

Instagram Thefty Poster V3 builds upon the features of V2, introducing several enhancements and new functionalities to improve the automation process of scraping, uploading, and managing Instagram reels.

## Features

- **All Features from V2**: Includes all functionalities from V2, such as scraping reels, uploading with customizable descriptions, adding to stories, interval-based tasks, and encrypted credentials.
- **Enhanced Randomized Actions**: More sophisticated random liking, commenting, and forwarding to simulate human behavior better.
- **Improved Dashboard**: Enhanced dashboard using the `rich` library for a more detailed and visually appealing display of activities.
- **Automated Scheduling**: More robust scheduling for scraping, uploading, and deletion tasks.
- **Detailed Logging**: Improved logging for better traceability and debugging.
- **Additional Configuration Options**: More settings for customization in `config.yaml`.

## Requirements

- Python 3.6+
- Required Python packages (specified in `requirements.txt`)

### Install Required Packages

You can install all the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sujay1599/InstagramTheftyPosterV3.git
   cd InstagramTheftyPosterV3
   ```

2. Install the required packages using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Run `start.py` to create the `config.yaml` file:
   ```bash
   python start.py
   ```
   Follow the prompts to enter your configuration details. This will generate a `config.yaml` file with the necessary settings, including encrypted Instagram credentials.

## Usage

Run the script:
```bash
python main.py
```

### Configuration

The `config.yaml` file will be generated by running `start.py`. It includes the following settings:

- **Instagram Credentials**: Provide your Instagram username and password. These will be encrypted and stored securely.
- **Scraping Settings**:
  - `enabled`: Set to `true` to enable scraping.
  - `profiles`: Space-separated list of Instagram profiles to scrape reels from.
  - `num_reels`: Number of reels to scrape per profile.
  - `scrape_interval_minutes`: Interval in minutes between scraping sessions.
- **Uploading Settings**:
  - `enabled`: Set to `true` to enable uploading.
  - `upload_interval_minutes`: Interval in minutes between uploads.
  - `add_to_story`: Set to `true` to add reels to your Instagram story.
- **Description Settings**:
  - `use_original`: Set to `true` to use the original reel description. If `false`, you will be prompted to enter a custom description.
  - `custom_description`: The custom description to use if `use_original` is `false`.
- **Hashtags Settings**:
  - `use_hashtags`: Set to `true` to use hashtags in the reel descriptions.
  - `hashtags_list`: List of hashtags to include in the reel descriptions (if `use_hashtags` is `true`).
- **Credit Settings**:
  - `give_credit`: Set to `true` to give credit to the original poster in the reel descriptions.
- **Deleting Settings**:
  - `delete_interval_minutes`: Interval in minutes between deletions.
- **Comments and Forwarding**:
  - `leave_comment`: Set to `true` to leave comments on scraped videos.
  - `comments`: List of comments to leave if `leave_comment` is `true`.
  - `forward_videos`: Set to `true` to forward videos to groups.
  - `groups`: List of group names to forward videos to if `forward_videos` is `true`.

### Logging

The script maintains a log file (`upload_log.txt`) to keep track of uploaded reels, a status file (`status.json`) to track the last action times, and a random upload times file (`random-upload-times.json`) to log the random sleep times between uploads.

### Dashboard

Run the dashboard script to view detailed information about scraping and uploading activities:

```bash
python dashboard.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Disclaimer

This script is intended for educational and personal use only. Use it responsibly and ensure you comply with Instagram's terms of service and guidelines.

---

## Differences Between V2 and V3

### New Features in V3

1. **Enhanced Randomized Actions**:
   - Improved algorithms for randomized liking, commenting, and forwarding to better mimic human behavior.

2. **Improved Dashboard**:
   - A more detailed and visually appealing dashboard using the `rich` library to display scraping and uploading activities.

3. **Automated Scheduling**:
   - More robust scheduling mechanisms for tasks, ensuring smoother and more efficient operations.

4. **Detailed Logging**:
   - Enhanced logging capabilities for better traceability and easier debugging of issues.

5. **Additional Configuration Options**:
   - More settings available in the `config.yaml` file for greater customization of the tool’s behavior.

6. **Comments and Forwarding**:
   - Additional options for leaving comments on scraped videos and forwarding them to specified groups.

### Improvements from V2 to V3

- **Randomized Action Logic**: Improved logic to make actions such as liking, commenting, and forwarding more random and human-like.
- **User Interface**: A more comprehensive and user-friendly dashboard.
- **Scheduling and Automation**: Enhanced scheduling for more reliable automation of tasks.
- **Logging and Debugging**: More detailed logging for easier issue identification and resolution.
- **Configurable Options**: Greater flexibility with additional configurable options.

By incorporating these improvements and new features, V3 aims to provide a more efficient, reliable, and user-friendly experience for automating Instagram reel management tasks.
