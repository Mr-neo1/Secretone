import datetime as dt
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import pygame


# Set up logging configuration
logging.basicConfig(filename='announcement_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


# Function to create a new SQLite database table to store scheduled announcements
def create_table():
    try:
        conn = sqlite3.connect("announcements.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY,
                announcement TEXT NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                repeat TEXT NOT NULL,
                selected_files TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("Table 'announcements' created successfully.")
    except Exception as e:
        print("Error during table creation:", e)



def insert_announcement(announcement, date, time, repeat, selected_files):
    print("Inserting announcement:", announcement)
    print("Date:", date)
    print("Time:", time)
    print("Repeat:", repeat)
    print("Selected files:", selected_files)

    conn = sqlite3.connect("announcements.db")
    c = conn.cursor()
    files_string = "|".join(selected_files)
    c.execute("""
        INSERT INTO announcements (announcement, date, time, repeat, selected_files)
        VALUES (?, ?, ?, ?, ?)
    """, (announcement, date, time, repeat, files_string))
    conn.commit()
    conn.close()

# Function to schedule an announcement
def schedule_announcement(announcement, date, time, repeat, selected_files):
    # Convert the date and time strings to datetime objects
    alarm_datetime = dt.datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")

    scheduler = BackgroundScheduler()

    if repeat == "Everyday":
        scheduler.add_job(play_announcement, 'cron', day_of_week='mon-sun', hour=alarm_datetime.hour,
                          minute=alarm_datetime.minute, second=alarm_datetime.second,
                          args=(announcement, selected_files))
    else:  # Repeat Once
        scheduler.add_job(play_announcement, 'date', run_date=alarm_datetime,
                          args=(announcement, selected_files))

    scheduler.start()
def play_announcement(announcement, selected_files):
    # Perform the action to play the alarm with the announcement and selected file
    logging.info("Playing announcement: %s", announcement)

    # Ensure that at least one file is selected
    if not selected_files:
        logging.warning("No file selected to play.")
        return

    # Play the selected file using the play_sound function
    selected_file = selected_files[0]  # Get the first selected file from the list
    try:
        play_sound(selected_file)
        logging.info("Announcement '%s' played successfully.", announcement)
    except Exception as e:
        logging.error("Error while playing announcement '%s': %s", announcement, str(e))




# Function to play a sound
def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# Fetch the scheduled announcements from the database
def get_scheduled_announcements():
    conn = sqlite3.connect("announcements.db")
    c = conn.cursor()
    c.execute("SELECT * FROM announcements")
    rows = c.fetchall()
    conn.close()
    return rows

#button working logics------------------------------------------------------------------------------------------------------------
def refresh_application(self):

        # Refresh the scheduled announcements table in the right bottom frame
        self.create_right_bottom_frame()

        # Refresh the current day announcements table in the right top frame
        self.create_right_top_frame()

        # Refresh the log file display
        self.display_log_file()

#-----------------------------------------------------------------------------------------------------------------------------------
# Run this part of the code when calling backend.py directly
if __name__ == "__main__":
    # Create the database table if it doesn't exist
    create_table()

    # Fetch the values from the UI and call the schedule_announcement function
    # Replace these variables with the values fetched from your UI
    announcement = "Announcement"
    date = "2023-07-12"
    time = "10:00:00"
    repeat = "Everyday"
    selected_files = ["file1.mp3", "file2.wav"]

    # Insert the fetched values into the database
    insert_announcement(announcement, date, time, repeat, selected_files)

    # Call the function to schedule the announcement
    schedule_announcement(announcement, date, time, repeat, selected_files)
