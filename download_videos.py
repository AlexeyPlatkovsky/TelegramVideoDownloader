import os
import logging
from telethon import TelegramClient
from tqdm import tqdm
import argparse
from configparser import ConfigParser
from datetime import datetime

MEGABYTE = 1024 * 1024

# Define log folder and create it if it doesn't exist
LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)
# Log file retention limit
LOG_FILE_LIMIT = 10

# Generate the logfile name with the current date and time, stored in the log folder
LOG_FILE = os.path.join(LOG_FOLDER, f"download_videos_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

def cleanup_old_logs(log_folder, limit):
    """
    Ensure the log folder contains no more than the specified number of log files.
    Deletes the oldest log files if the limit is exceeded.

    :param log_folder: Path to the folder containing log files
    :param limit: Maximum number of log files to retain
    """
    # Get all log files in the folder
    log_files = [os.path.join(log_folder, f) for f in os.listdir(log_folder) if f.endswith(".log")]

    # Sort log files by creation time (oldest first)
    log_files.sort(key=os.path.getctime)

    # Delete the oldest files if the limit is exceeded
    while len(log_files) >= limit:
        oldest_file = log_files.pop(0)  # Get the oldest file
        os.remove(oldest_file)  # Delete the file
        logging.info(f"Deleted old log file: {oldest_file}")


# Clean up old log files before starting logging
cleanup_old_logs(LOG_FOLDER, LOG_FILE_LIMIT)

# Configure logging to log both to a file and the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),  # Log to file with UTF-8 encoding
        logging.StreamHandler()                          # Log to console
    ]
)

logger = logging.getLogger(__name__)

# Load configuration settings from 'config.ini'
config = ConfigParser()
config.read("config.ini")

# Read Telegram API credentials and channel details from the configuration file
api_id = int(config["telegram"]["api_id"])
api_hash = config["telegram"]["api_hash"]
channel_id = int(config["telegram"]["channel_id"])
MESSAGE_TEXT = config["telegram"]["MESSAGE_TEXT"]

# Initialize the Telegram client session with the provided API credentials
client = TelegramClient("user_session", api_id, api_hash)


async def download_with_resume(message, file_path):
    """
    Resume a partially downloaded file using the Telegram get_file method and display a progress bar.

    Parameters:
        message (Message): The Telegram message containing the file to download.
        file_path (str): The local file path where the file should be saved.
    """
    current_size = 0
    # Check if the file already exists and get its current size
    if os.path.exists(file_path):
        current_size = os.path.getsize(file_path)
        logger.info(f"Partial file found: {file_path}, size: {current_size / MEGABYTE} Mbs")

    # If the file size matches the expected size, skip the download
    if current_size == message.file.size:
        logger.info(f"File already fully downloaded: {file_path}")
        return

    logger.info(f"Resuming download for: {file_path}")

    # Initialize a progress bar with the file size and resume from the current size
    with tqdm(
            desc=f"Downloading {os.path.basename(file_path)}",
            total=message.file.size,
            initial=current_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024
    ) as bar:
        try:
            # Resume downloading using the get_file method
            async for chunk in client.iter_download(
                    message.media.document,
                    offset=current_size,
                    request_size=MEGABYTE  # Download in 1MB chunks
            ):
                with open(file_path, "ab") as f:
                    f.write(chunk)
                    bar.update(len(chunk))
        except Exception as exception:
            logger.error(f"Error during download: {exception}")
            bar.close()
    logger.info(f"Download completed: {file_path}")


async def main(download_folder):
    """
    Main logic to download videos from a Telegram channel.

    Parameters:
        download_folder (str): Directory where the downloaded videos will be stored.
    """
    # Ensure the download directory exists
    os.makedirs(download_folder, exist_ok=True)

    # Connect to Telegram
    await client.start()
    logger.info("Client connected to Telegram.")

    logger.info("Start looking through messages.")
    # Iterate through messages in the specified Telegram channel
    # Process only messages that contain a video and the target text
    async for message in client.iter_messages(channel_id):
        # Check if the message has a video and the text
        if message.video and (message.text and MESSAGE_TEXT in message.text):
            # Get the file name or assign a default name
            file_name = message.file.name if message.file and message.file.name else f"video_{message.id}.mp4"
            file_path = os.path.join(download_folder, file_name)
            logger.info(f"Found video with: {file_name}")

            try:
                await download_with_resume(message, file_path)
            except Exception as exception:
                logger.error(f"Error downloading video {file_name}: {exception}")


if __name__ == "__main__":
    import asyncio

    # Parse command-line arguments to specify the download folder
    parser = argparse.ArgumentParser(description="Telegram Video Downloader with Resume Support")
    parser.add_argument(
        "--download-folder",
        type=str,
        help="Folder to save downloaded videos",
        default="downloads"
    )
    args = parser.parse_args()

    # Run the main script
    try:
        asyncio.run(main(args.download_folder))
    except Exception as e:
        logger.critical(f"Script terminated with an error: {e}")
