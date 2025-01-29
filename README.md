# Telegram Video Downloader with Resume Support

This Python script downloads videos from a specified Telegram channel, supports resuming incomplete downloads, and includes a progress bar to track the download status.

## Features

- Downloads videos from a specified Telegram channel.
- Resumes partially downloaded videos without starting over.
- Displays a progress bar for each download.
- Logs events and errors to a log file (stored in the `logs` folder).

---

## Before Run

### Prerequisites

1. **Python Installation**  
   Ensure you have Python 3.7 or later installed on your system. You can download it from [python.org](https://www.python.org/).


### Configuration File
Create a `config.ini` file in the same directory as the script with the following content:

```ini
[telegram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
channel_id = YOUR_CHANNEL_ID
MESSAGE_TEXT = YOUR_HASHTAG_OR_TEXT_FILTER
```

Replace `YOUR_API_ID`, `YOUR_API_HASH`, `YOUR_CHANNEL_ID`, and `YOUR_HASHTAG_OR_TEXT_FILTER` with the appropriate values:
#### **How to Obtain These Values:**

- **api_id** and **api_hash:**
  - Go to [the Telegram API site](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id) 
  - Log in to the Telegram API Development Tools.
  - Create a new application to obtain the `api_id` and `api_hash`.

- **channel_id:**
  - Use the `get_channel_id.py` script (explained below) to fetch the ID of the target channel.

- **MESSAGE_TEXT:**
  - Specify the hashtag or keyword to filter messages containing videos. For example, `#MyVideos`.


---

### How to Install
#### Clone or Download the Repository
Clone the repository or download the script to your local machine:

```bash
git clone https://github.com/AlexeyPlatkovsky/TelegramVideoDownloader.git
cd TelegramVideoDownloader
```

#### Install Dependencies
Make sure the required libraries are installed:

```bash
pip install -r requirements.txt
```

#### Create the Logs and Download Folder
The script automatically creates a `logs` and `download` folder in the script directory if it doesn't exist. No manual steps are needed.

---

### How to Use

#### Purpose of `get_channel_id.py`

The `get_channel_id.py` script helps fetch the IDs of all accessible Telegram channels and chats for your account. These IDs are necessary for configuring the `channel_id` field in the `config.ini` file.

#### How to Use:
1. **Run the script:**
   ```bash
   python get_channel_id.py
   ```
2. **Authenticate with Your Telegram Account:**
 - Enter your Telegram phone number. 
 - Verify the login by entering the code sent to your Telegram app.  

3. **Note the channel_id:**
 - Look for the desired channel in the script output.  
 - Copy its ID and update the `channel_id` field in your `config.ini` file.

#### Main Script Command-Line Execution
Run the script from the command line as follows:

```bash
python download_videos.py --download-folder "path_to_download_folder"
```

Replace `"path_to_download_folder"` with the directory where you want the downloaded videos to be saved.
If no `--download-folder` is specified, videos are saved in the default `downloads` folder.

##### Example:
```bash
python download_videos.py --download-folder "C:/Users/YourName/Videos"
```

#### First time run:  
When you run script first time, Telegram can ask you to enter your phone number and security code
```angelscript
Please enter your phone (or bot token):
Please enter the code you received: 
```

---

### Logs
- Logs are stored in the `logs` folder.
- Each run creates a new log file with a timestamp in the name, e.g., `download_videos_2025-01-29_12-30-00.log`.
- If the folder contains more than 10 log files, the script automatically deletes the oldest log files.

---

### Troubleshooting
#### `ModuleNotFoundError: No module named 'telethon'`
Ensure you have installed the `telethon` library:

```bash
pip install telethon
```

#### Telegram API Errors
- Ensure your `api_id` and `api_hash` in `config.ini` are correct.
- Make sure your Telegram account has access to the specified channel.

#### Permission Issues
- Run the script as an administrator if you encounter file permission errors on Windows.

---

### License
This project is licensed under the MIT License. See the LICENSE file for details.