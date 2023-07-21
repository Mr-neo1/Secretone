import datetime
import os
import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
from PIL import ImageTk, Image
import datetime as dt
import backend
from backend import schedule_announcement, play_announcement, insert_announcement, create_table

# Define colors for the new design
PRIMARY_COLOR = "#0D0320"  # Dark background color
SECONDARY_COLOR = "#14E882"  # Accent color
TEXT_COLOR = "white"  # Text color

class AnnouncementScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("CT UNIVERSITY Announcement Scheduler")
        self.root.geometry("1540x800+0+0")
        self.root.config(bg=PRIMARY_COLOR)

        self.create_title_label()
        self.create_data_frame()
        self.create_left_frame()
        self.create_middle_frame()
        self.create_right_top_frame()
        self.create_right_bottom_frame()
        self.create_button_frame()
        self.create_details_frame()
        pygame.mixer.init()



    def create_title_label(self):

        title_frame = tk.Frame(self.root, bg=PRIMARY_COLOR)
        title_frame.pack(side=tk.TOP, fill=tk.X, pady=20)

        # Load the logo image
        logo_image = Image.open("Ct_logo.png")
        logo_image = logo_image.resize((50, 50))  # Adjust the size of the logo as needed
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Create a label for the logo
        logo_label = tk.Label(title_frame, image=logo_photo, bg=PRIMARY_COLOR)
        logo_label.image = logo_photo
        logo_label.grid(row=0, column=0, padx=(280,20))

        lbl_title = tk.Label(
            title_frame,
            bd=0,
            relief=tk.RIDGE,
            text="CT UNIVERSITY ANNOUNCEMENT SCHEDULER",
            fg=SECONDARY_COLOR,
            bg=PRIMARY_COLOR,
            font=("roadies", 30, "bold")
        )

        lbl_title.grid(row=0, column=1)

    def create_data_frame(self):
        self.data_frame = tk.Frame(self.root, bd=3, padx=20, relief=tk.GROOVE, bg=PRIMARY_COLOR)
        self.data_frame.place(x=0, y=90, width=1530, height=480)

    def create_left_frame(self):
        left_frame = tk.LabelFrame(
            self.root,
            bd=0,
            highlightthickness=0,
            padx=20,
            pady=30,
            relief=tk.RIDGE,
            font=("arial", 12, "bold"),
            text="Announcement Scheduler",
            bg="white",
            fg="black"
        )
        left_frame.place(x=5, y=96, width=330, height=450)

        # Use resized icons
        icon_size = (24, 24)
        label_icon = Image.open("icons/icons8-create-24.png").resize(icon_size)
        label_icon = ImageTk.PhotoImage(label_icon)

        icon_label = tk.Label(left_frame, image=label_icon, padx=0, pady=15, bg="white")
        icon_label.image = label_icon
        icon_label.grid(row=0, column=0, pady=(20, 0))

        announcement_entry = tk.Entry(left_frame, font=("times new roman", 12), bd=0, relief=tk.SOLID, width=20)
        announcement_entry.insert(0, "Announcement")
        separator = ttk.Separator(left_frame, orient="horizontal")
        separator.grid(row=0, column=1, padx=(10, 20), pady=(45, 0), sticky="ew")
        announcement_entry.grid(row=0, column=1, padx=(10, 20), pady=(20, 0), sticky=tk.W)
        announcement_entry.config(bd=0, highlightthickness=0)

        # Update the icons with resized versions
        label_icon = Image.open("icons/icons8-calendar-24.png").resize(icon_size)
        label_icon = ImageTk.PhotoImage(label_icon)

        icon_label = tk.Label(left_frame, image=label_icon, padx=0, pady=10, bg="white")
        icon_label.image = label_icon
        icon_label.grid(row=1, column=0, pady=(20, 0))

        # Set current date and time in the respective entry fields
        current_date = dt.datetime.now().strftime("%Y-%m-%d")
        date_entry = tk.Entry(left_frame, font=("times new roman", 12), bd=0, relief=tk.FLAT, width=20)
        date_entry.grid(row=1, column=1, padx=(10, 20), pady=(20, 0), sticky=tk.W)
        separator = ttk.Separator(left_frame, orient="horizontal")
        separator.grid(row=1, column=1, padx=(10, 20), pady=(45, 0), sticky="ew")
        date_entry.insert(0, current_date)

        # Update the icons with resized versions
        label_icon = Image.open("icons/icons8-time-24.png").resize(icon_size)
        label_icon = ImageTk.PhotoImage(label_icon)

        icon_label = tk.Label(left_frame, image=label_icon, padx=0, pady=10, bg="white")
        icon_label.image = label_icon
        icon_label.grid(row=2, column=0, pady=(20, 0))

        current_time = dt.datetime.now().strftime("%H:%M:%S")
        time_entry = tk.Entry(left_frame, font=("times new roman", 12), relief=tk.FLAT, width=20)
        time_entry.grid(row=2, column=1, padx=(10, 20), pady=(20, 0), sticky=tk.W)

        separator = ttk.Separator(left_frame, orient="horizontal")
        separator.grid(row=2, column=1, padx=(10, 20), pady=(45, 0), sticky="ew")
        time_entry.insert(0, current_time)

        # Update the icons with resized versions
        label_icon = Image.open("icons/icons8-repeat-24.png").resize(icon_size)
        label_icon = ImageTk.PhotoImage(label_icon)

        repeat_var = tk.StringVar()
        repeat_dropdown = ttk.Combobox(
            left_frame,
            textvariable=repeat_var,
            font=("times new roman", 12),
            state="readonly",
            width=20
        )
        repeat_dropdown["values"] = ("Everyday", "Once")
        repeat_dropdown.current(1)  # Set default selection to index 1, which is "Once"
        repeat_dropdown.grid(row=3, column=1, padx=(10, 20), pady=20, sticky=tk.W)

        icon_label = tk.Label(left_frame, image=label_icon, padx=0, pady=10, bg="white")
        icon_label.image = label_icon
        icon_label.grid(row=3, column=0, pady=(20, 0))

        # Update the icons with resized versions
        label_icon = Image.open("icons/icons8-upload-file-24.png").resize(icon_size)
        label_icon = ImageTk.PhotoImage(label_icon)

        icon_label = tk.Label(left_frame, image=label_icon, padx=0, pady=8, bg="white")
        icon_label.image = label_icon
        icon_label.grid(row=4, column=0, pady=(20, 0))

        self.file_paths = []  # Store the selected file paths
        self.file_label = tk.Label(
            left_frame,
            text="",
            font=("times new roman", 10),
            padx=10,
            pady=5,
            wraplength=200,
            bg="white"
        )
        self.file_label.grid(row=5, column=1, padx=(10, 20), pady=(0, 20), sticky=tk.W)

        def browse_files():
            filetypes = (("Audio files", "*.mp3;*.wav"), ("All files", "*.*"))
            selected_files = filedialog.askopenfilenames(filetypes=filetypes)

            if selected_files:
                # Clear the current file listbox selection
                self.file_listbox.selection_clear(0, tk.END)

                # Clear the file name label
                self.file_label.config(text="")

                self.file_paths = list(selected_files)  # Update the file paths

                for file_path in selected_files:
                    # Insert the selected file path into the file listbox
                    self.file_listbox.insert(tk.END, file_path)

                # Select the first file in the listbox by default
                self.file_listbox.selection_set(0)

        browse_button = tk.Button(
            left_frame,
            text="Browse",
            command=browse_files,
            font=("times new roman", 12, "bold"),
            bg="#0067c0",
            fg=TEXT_COLOR,
            width=12
        )
        browse_button.grid(row=4, column=1, padx=(10, 20), pady=15, sticky=tk.W)

        def add_schedule():
            announcement = announcement_entry.get()  # Get the announcement value from UI
            date = date_entry.get()  # Get the date value from UI
            time = time_entry.get()  # Get the time value from UI
            repeat = repeat_var.get()  # Get the repeat value from UI
            selected_files = ob.file_listbox.curselection()  # Get the indices of selected files from the listbox

            if not selected_files:
                # No file selected from the listbox
                messagebox.showinfo("Error", "Please select a sound file from the listbox.")
                return

            # Get the selected file from the listbox based on the first selected index
            selected_file = ob.file_listbox.get(selected_files[0])

            # Call the insert_announcement function from backend.py to save the data in the database
            insert_announcement(announcement, date, time, repeat, [selected_file])  # Pass the selected file as a list

            # Call the schedule_announcement function from backend.py
            schedule_announcement(announcement, date, time, repeat, [selected_file])  # Pass the selected file as a list

            # Display a success message
            messagebox.showinfo("Success", "Alarm scheduled successfully.")

        # Create the schedule button
        schedule_button = tk.Button(
            left_frame,
            text="Add Schedule",
            command=add_schedule,
            font=("times new roman", 14, "bold"),
            bg="#0067c0",
            fg=TEXT_COLOR,
            width=20
        )
        schedule_button.grid(row=7, column=0, columnspan=2, padx=40, pady=20)

    def create_middle_frame(self):
        middle_frame = tk.LabelFrame(
            self.data_frame,
            bd=0,
            highlightthickness=0,
            padx=20,
            relief=tk.RIDGE,
            font=("arial", 12, "bold"),
            text="Controls",
            bg="white",
            fg="black"
        )
        middle_frame.place(x=315, y=4, width=332, height=450)

        def play_sound():
            selected_files = self.file_listbox.curselection()
            if selected_files:
                selected_file = self.file_listbox.get(selected_files[0])
                pygame.mixer.music.load(selected_file)  # Load the selected audio file
                pygame.mixer.music.play()  # Play the loaded audio file
            else:
                messagebox.showinfo("No File Selected", "Please select a sound file to play.")

        def pause_sound():
            pygame.mixer.music.pause()  # Pause the currently playing audio

        play_button = tk.Button(
            middle_frame,
            text="Play",
            command=play_sound,
            font=("times new roman", 12, "bold"),
            bg="#0067c0",
            fg=TEXT_COLOR,
            width=10
        )
        play_button.place(x=20, y=330)

        pause_button = tk.Button(
            middle_frame,
            text="Pause",
            command=pause_sound,
            font=("times new roman", 12, "bold"),
            bg="#0067c0",
            fg=TEXT_COLOR,
            width=10
        )
        pause_button.place(x=140, y=330)

        # Create a custom style for the heading label
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Heading.TLabel", background="#0067c0", foreground=TEXT_COLOR, font=("Arial", 14, "bold"))

        # Create a label to display the blue strip background
        blue_strip_label = ttk.Label(middle_frame, background="#0067c0")
        blue_strip_label.pack(fill=tk.X, pady=5)

        # Create the heading label with centered text
        heading_label = ttk.Label(blue_strip_label, text="Audio List", style="Heading.TLabel")
        heading_label.pack(padx=10, pady=5)

        self.file_listbox = tk.Listbox(
            middle_frame,
            selectmode=tk.SINGLE,
            font=("callibary", 10),
            bd=0,
            relief=tk.SOLID,
            width=40,
            height=17
        )
        self.file_listbox.place(x=5, y=35)  # Adjust the y-coordinate to leave space for the heading label

        def update_file_label(event):
            selected_files = self.file_listbox.curselection()
            if selected_files:
                selected_file = self.file_listbox.get(selected_files[0])
                file_name = os.path.basename(selected_file)
                self.file_label.config(text="Selected file: " + file_name)
            else:
                self.file_label.config(text="")

        self.file_listbox.bind("<<ListboxSelect>>", update_file_label)

    def create_right_top_frame(self):
        right_top_frame = tk.LabelFrame(
            self.data_frame,
            bd=2,
            padx=20,
            relief=tk.RIDGE,
            font=("arial", 12, "bold"),
            text="Current Day Announcements",
            bg="white"
        )
        right_top_frame.place(x=650, y=5, width=850, height=225)

        # Create a custom style for the headings
        style = ttk.Style()
        style.theme_use("default")

        # Configure the heading style with the desired background color (blue strip)
        style.configure(
            "Custom.Treeview.Heading",
            background="#0067c0",
            foreground=TEXT_COLOR,
            font=("Arial", 10, "bold")
        )

        # Set the same background and foreground colors for the active heading state (no hover effect)
        style.map(
            "Custom.Treeview.Heading",
            background=[("active", "#0067c0"), ("!active", "#0067c0")],
            foreground=[("active", TEXT_COLOR), ("!active", TEXT_COLOR)]
        )

        scroll_x = ttk.Scrollbar(right_top_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(right_top_frame, orient=tk.VERTICAL)
        current_day_table = ttk.Treeview(
            right_top_frame,
            columns=("lblNo", "lblName", "lblDate", "lblTime", "lblRepeat", "lblFile"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            style="Custom.Treeview"  # Use the custom style for the Treeview
        )

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x.config(command=current_day_table.xview)
        scroll_y.config(command=current_day_table.yview)

        current_day_table.heading("lblNo", text="Serial No", anchor="w")
        current_day_table.heading("lblName", text="Label", anchor="w")
        current_day_table.heading("lblDate", text="Date", anchor="w")
        current_day_table.heading("lblTime", text="Time", anchor="w")
        current_day_table.heading("lblRepeat", text="Repeat", anchor="w")
        current_day_table.heading("lblFile", text="File", anchor="w")

        current_day_table.column("lblNo", width=100)
        current_day_table.column("lblName", width=100)
        current_day_table.column("lblDate", width=100)
        current_day_table.column("lblTime", width=100)
        current_day_table.column("lblRepeat", width=100)
        current_day_table.column("lblFile", width=1000)

        scroll_x.config(command=current_day_table.xview)
        scroll_y.config(command=current_day_table.yview)

        current_day_table["show"] = "headings"
        current_day_table.pack(fill=tk.BOTH, expand=1)

        # Fetch current day announcements from the database
        data = self.get_current_day_announcements()

        # Populate the scheduled_table with the data and add serial numbers
        for item in data:
            current_day_table.insert("", tk.END, values=item)

    def get_current_day_announcements(self):
        conn = sqlite3.connect("announcements.db")
        c = conn.cursor()

        # Get the current date
        current_date = datetime.datetime.now().date()

        # Fetch scheduled announcements for the current day
        c.execute("SELECT * FROM announcements WHERE date = ?", (current_date,))

        rows = c.fetchall()
        conn.close()
        return rows

    def create_right_bottom_frame(self):
        right_bottom_frame = tk.LabelFrame(
            self.data_frame,
            bd=2,
            padx=20,
            relief=tk.RIDGE,
            font=("arial", 12, "bold"),
            text="Scheduled Announcements",
            bg="white"
        )
        right_bottom_frame.place(x=650, y=230, width=850, height=225)

        # Create a custom style for the headings
        style = ttk.Style()
        style.theme_use("default")

        # Configure the heading style with the desired background color (blue strip)
        style.configure(
            "Custom.Treeview.Heading",
            background="#0067c0",
            foreground=TEXT_COLOR,
            font=("Arial", 10, "bold")
        )

        # Set the same background and foreground colors for the active heading state (no hover effect)
        style.map(
            "Custom.Treeview.Heading",
            background=[("active", "#0067c0"), ("!active", "#0067c0")],
            foreground=[("active", TEXT_COLOR), ("!active", TEXT_COLOR)]
        )

        scroll_x = ttk.Scrollbar(right_bottom_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(right_bottom_frame, orient=tk.VERTICAL)
        scheduled_table = ttk.Treeview(
            right_bottom_frame,
            columns=("lblNo", "lblName", "lblDate", "lblTime", "lblRepeat", "lblFile"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            style="Custom.Treeview"  # Use the custom style for the Treeview
        )

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x.config(command=scheduled_table.xview)
        scroll_y.config(command=scheduled_table.yview)

        scheduled_table.heading("lblNo", text="Serial No", anchor="w")
        scheduled_table.heading("lblName", text="Label", anchor="w")
        scheduled_table.heading("lblDate", text="Date", anchor="w")
        scheduled_table.heading("lblTime", text="Time", anchor="w")
        scheduled_table.heading("lblRepeat", text="Repeat", anchor="w")
        scheduled_table.heading("lblFile", text="File", anchor="w")

        scheduled_table.column("lblNo", width=100)
        scheduled_table.column("lblName", width=100)
        scheduled_table.column("lblDate", width=100)
        scheduled_table.column("lblTime", width=100)
        scheduled_table.column("lblRepeat", width=100)
        scheduled_table.column("lblFile", width=1000)

        scroll_x.config(command=scheduled_table.xview)
        scroll_y.config(command=scheduled_table.yview)

        scheduled_table["show"] = "headings"
        scheduled_table.pack(fill=tk.BOTH, expand=1)

        # Fetch scheduled announcements from the database
        data = self.get_scheduled_announcements()

        # Populate the scheduled_table with the data and add serial numbers
        for item in data:
            scheduled_table.insert("", tk.END, values=item)

    def get_scheduled_announcements(self):
        conn = sqlite3.connect("announcements.db")
        c = conn.cursor()

        # Get the current date
        current_date = datetime.datetime.now().date()

        # Fetch scheduled announcements for the current day and future dates
        c.execute("SELECT * FROM announcements WHERE date >= ?", (current_date,))

        rows = c.fetchall()
        conn.close()
        return rows

    def create_button_frame(self):
        button_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE, bg="white")
        button_frame.place(x=0, y=550, width=1530, height=50)



        # Add the Refresh button
        refresh_button = tk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh_application_ui,
            font=("times new roman", 14, "bold"),
            bg="#0067c0",
            fg=TEXT_COLOR,
            width=12
        )
        refresh_button.pack(side=tk.LEFT, padx=10)

        

        # Add the Exit button
        exit_button = tk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit,  # Quit the Tkinter application
            font=("times new roman", 14, "bold"),
            bg="#d32f2f",  # Red color for the exit button
            fg="white",
            width=12
        )
        exit_button.pack(side=tk.LEFT, padx=10)

    def refresh_application_ui(self):
        # Call the backend's refresh_application function
        backend.refresh_application(self)  # Call the function from the backend

#----------------------------------------------------------------------------------------
    def create_details_frame(self):
        details_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="white")
        details_frame.place(x=0, y=600, width=1530, height=190)

        # Add a Text widget to display the log file content
        self.log_text = tk.Text(details_frame, wrap=tk.WORD, font=("Arial", 10))
        self.log_text.pack(fill=tk.BOTH, expand=1)

        # Function to read the log file and display its content in the Text widget
        self.display_log_file()


    def display_log_file(self):
        try:
            with open('announcement_log.txt', 'r') as log_file:
                log_content = log_file.readlines()

            self.log_text.delete(1.0, tk.END)  # Clear the Text widget

            # Apply color-coded tags to different log messages
            for line in log_content[::-1]:  # Reverse the order to display the latest log at the top
                if "played successfully." in line:
                    self.log_text.insert(tk.END, line, "success")
                elif "WARNING" in line:
                    self.log_text.insert(tk.END, line, "warning")
                elif "ERROR" in line:
                    self.log_text.insert(tk.END, line, "error")
                else:
                    self.log_text.insert(tk.END, line)

            # Configure the tags to set the colors
            self.log_text.tag_configure("success", foreground="green", font=('bold', 12))
            self.log_text.tag_configure("warning", foreground="red", font=('bold', 12))
            self.log_text.tag_configure("error", foreground="red", font=('bold', 12))

        except FileNotFoundError:
            self.log_text.insert(tk.END, "Log file not found.")  # If log file doesn't exist


if __name__ == "__main__":
    create_table()
    root = tk.Tk()
    ob = AnnouncementScheduler(root)
    root.mainloop()
