import pyotp
import tkinter as tk

# Create a GUI window and set it to be always on top
root = tk.Tk()
root.title("OTP Generator")
root.attributes("-topmost", True)

# Create a dictionary to hold the service keys and their corresponding tab names
service_keys = {}

# Define functions to add and delete service keys, and change the tab name
def add_service_key():
    service_key = service_key_entry.get()
    if service_key not in service_keys:
        tab_name = tab_name_entry.get() or service_key
        service_keys[service_key] = tab_name
        add_service_key_label(service_key, tab_name)
        update_otp_labels()

def delete_service_key(service_key):
    if service_key in service_keys:
        del service_keys[service_key]
        for child in service_key_labels.winfo_children():
            if child.service_key == service_key:
                child.destroy()
        update_otp_labels()

def change_tab_name(service_key):
    tab_name = tab_name_entry.get() or service_key
    service_keys[service_key] = tab_name
    for child in service_key_labels.winfo_children():
        if child.service_key == service_key:
            child.configure(text=tab_name)

# Create a frame to hold the service key and tab name entry fields, and button
entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=10)

service_key_entry = tk.Entry(entry_frame, width=30)
service_key_entry.pack(side=tk.LEFT, padx=5, pady=5)

tab_name_entry = tk.Entry(entry_frame, width=20)
tab_name_entry.pack(side=tk.LEFT, padx=5, pady=5)

add_button = tk.Button(entry_frame, text="Add", command=add_service_key)
add_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame to hold the service key labels
service_key_labels = tk.Frame(root)
service_key_labels.pack(padx=10, pady=10)

# Define a function to add a service key label to the GUI
def add_service_key_label(service_key, tab_name):
    label_frame = tk.LabelFrame(service_key_labels, text=tab_name)
    label_frame.pack(padx=5, pady=5)

    otp_label = tk.Label(label_frame, font=("Helvetica", 24), padx=20, pady=20)
    otp_label.pack()

    change_tab_name_button = tk.Button(label_frame, text="Change Tab Name", command=lambda: change_tab_name(service_key))
    change_tab_name_button.pack()

    delete_button = tk.Button(label_frame, text="Delete", command=lambda: delete_service_key(service_key))
    delete_button.pack()

    # Store the service key in the label frame for easy access later
    label_frame.service_key = service_key

# Define a function to update the OTP labels
def update_otp_labels():
    # Update the OTP labels for each service key
    for child in service_key_labels.winfo_children():
        service_key = child.service_key
        totp = pyotp.TOTP(service_key)
        otp = totp.now()
        otp_label = child.winfo_children()[0]
        otp_label.config(text=otp)

    # Schedule the function to be called again after 1 second
    root.after(1000, update_otp_labels)

# Call the function to start updating the OTP labels
update_otp_labels()

# Start the GUI main loop
root.mainloop()