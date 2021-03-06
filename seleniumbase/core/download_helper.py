import os
import shutil
import sys
import time
from seleniumbase.config import settings
from seleniumbase.fixtures import constants

# Folder for saving downloaded files.
# If initiated by WebDriver clicks, works ONLY for Chrome and Firefox.
# Browser used doesn't matter if done with self.download_file(file_url)
# or self.save_file_as(file_url, new_file_name)
DOWNLOADS_DIR = constants.Files.DOWNLOADS_FOLDER
ARCHIVE_DIR = constants.Files.ARCHIVED_DOWNLOADS_FOLDER

abs_path = os.path.abspath('.')
downloads_path = os.path.join(abs_path, DOWNLOADS_DIR)


def get_downloads_folder():
    return downloads_path


def reset_downloads_folder():
    ''' Clears the downloads folder.
        If settings.ARCHIVE_EXISTING_DOWNLOADS is set to True, archives it. '''
    if os.path.exists(downloads_path) and not os.listdir(downloads_path) == []:
        archived_downloads_folder = os.path.join(downloads_path, '..',
                                                 ARCHIVE_DIR)
        if not "".join(sys.argv) == "-c":
            # Only move files if the test run is not multi-threaded.
            # (Running tests with "-n NUM" will create threads that only
            # have "-c" in the sys.argv list. Easy to catch.)
            reset_downloads_folder_assistant(archived_downloads_folder)


def reset_downloads_folder_assistant(archived_downloads_folder):
    if not os.path.exists(archived_downloads_folder):
        os.makedirs(archived_downloads_folder)
    new_archived_downloads_sub_folder = "%s/downloads_%s" % (
        archived_downloads_folder, int(time.time()))
    if os.path.exists(downloads_path):
        if not os.listdir(downloads_path) == []:
            shutil.move(downloads_path, new_archived_downloads_sub_folder)
            os.makedirs(downloads_path)
    if not settings.ARCHIVE_EXISTING_DOWNLOADS:
        try:
            shutil.rmtree(new_archived_downloads_sub_folder)
        except OSError:
            pass
