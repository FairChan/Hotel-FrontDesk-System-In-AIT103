import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import os

CSV_FILE = 'guest_info.csv'

def save_data():
    name = name_entry.get().strip()
    room = room_entry.get().strip()
    checkin = checkin_entry.get_date().strftime('%Y-%m-%d')
    checkout = checkout_entry.get_date().strftime('%Y-%m-%d')

    if not name or not room:
        messagebox.showerror("Input Error“, ”All fields must be completed.")
        return




    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, room, checkin, checkout])
        
    messagebox.showinfo("Saved successfully“, ”The guest information has been saved.")
    name_entry.delete(0, tk.END)
    room_entry.delete(0, tk.END)
    load_guest_data()

def load_guest_data(filter_name=None, filter_room=None):
    for row in guest_table.get_children():
        guest_table.delete(row)

    if not os.path.exists(CSV_FILE):
        return

    with open(CSV_FILE, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            name, room, checkin, checkout = row
            if filter_name and filter_name.lower() not in name.lower():
                continue
            if filter_room and filter_room != room:
                continue
            guest_table.insert('', tk.END, values=row)

def search_guest():
    name = search_name_entry.get().strip()
    room = search_room_entry.get().strip()
    load_guest_data(name if name else None, room if room else None)

def load_selected_guest():
    selected = guest_table.selection()
    if not selected:
        messagebox.showwarning("unselected", "Please select the customer record you want to modify first.")
        return

    item = guest_table.item(selected[0])
    global original_data
    original_data = item['values']  #Record the original value for modifying the match
    name_entry.delete(0, tk.END)
    room_entry.delete(0, tk.END)
    name_entry.insert(0, original_data[0])
    room_entry.insert(0, original_data[1])
    checkin_entry.set_date(original_data[2])
    checkout_entry.set_date(original_data[3])

def modify_guest():
    if not original_data:
        messagebox.showwarning("unselected", "Please select the customer record by clicking ‘Load Information’ first.")
        return

    new_data = [
        name_entry.get().strip(),
        room_entry.get().strip(),
        checkin_entry.get_date().strftime('%Y-%m-%d'),
        checkout_entry.get_date().strftime('%Y-%m-%d')
    ]

    if not new_data[0] or not new_data[1]:
        messagebox.showerror("input error", "All fields are required.")
        return

    # Read the original data and replace the corresponding rows
    rows = []
    found = False
    with open(CSV_FILE, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row == original_data:
                rows.append(new_data)
                found = True
            else:
                rows.append(row)

    if found:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        messagebox.showinfo("Modified successfully", "Customer information has been modified.")
        load_guest_data()
    else:
        messagebox.showerror("Modification Failure", "No original customer records were found.")

# Creating the Main Window
root = tk.Tk()
root.title("🏨Hotel Management System")
root.geometry("900x750")
root.configure(bg="#f0f4f7")

try:
    root.iconbitmap("hotel.ico")
except:
    pass

style = ttk.Style()
style.configure('TLabel', font=('Arial', 14), background="#f0f4f7")
style.configure('TButton', font=('Arial', 13), padding=6)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
style.configure("Treeview", font=("Arial", 11), rowheight=25)

main_frame = ttk.Frame(root)
main_frame.pack(pady=20)

ttk.Label(main_frame, text="Hotel guest information entry", font=("Arial", 20, 'bold')).grid(row=0, column=0, columnspan=3, pady=20)

ttk.Label(main_frame, text="Guest Name.").grid(row=1, column=0, sticky=tk.E, pady=10, padx=10)
name_entry = ttk.Entry(main_frame, width=40)
name_entry.grid(row=1, column=1, pady=10, padx=10)

ttk.Label(main_frame, text="Room Number:").grid(row=2, column=0, sticky=tk.E, pady=10, padx=10)
room_entry = ttk.Entry(main_frame, width=40)
room_entry.grid(row=2, column=1, pady=10, padx=10)

ttk.Label(main_frame, text="入Check-in time:").grid(row=3, column=0, sticky=tk.E, pady=10, padx=10)
checkin_entry = DateEntry(main_frame, width=37, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
checkin_entry.grid(row=3, column=1, pady=10, padx=10)

ttk.Label(main_frame, text="Check-out time:").grid(row=4, column=0, sticky=tk.E, pady=10, padx=10)
checkout_entry = DateEntry(main_frame, width=37, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
checkout_entry.grid(row=4, column=1, pady=10, padx=10)

button_frame = ttk.Frame(main_frame)
button_frame.grid(row=5, column=0, columnspan=3, pady=20)

ttk.Button(button_frame, text="Saving information", command=save_data).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Loading information", command=load_selected_guest).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="Modify Information", command=modify_guest).grid(row=0, column=2, padx=10)

# 查询模块
search_frame = ttk.Frame(root)
search_frame.pack(pady=10)

ttk.Label(search_frame, text="Search Name.").grid(row=0, column=0, padx=5)
search_name_entry = ttk.Entry(search_frame, width=20)
search_name_entry.grid(row=0, column=1, padx=5)

ttk.Label(search_frame, text="Room Number:").grid(row=0, column=2, padx=5)
search_room_entry = ttk.Entry(search_frame, width=20)
search_room_entry.grid(row=0, column=3, padx=5)

ttk.Button(search_frame, text="Search", command=search_guest).grid(row=0, column=4, padx=10)

#Customer Information Form
table_frame = ttk.Frame(root)
table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

guest_table = ttk.Treeview(table_frame, columns=("Name", "Room Number", "Check-in Time", "Check-out Time"), show='headings')
guest_table.heading("Name", text="Name")
guest_table.heading("Room Number", text="Room Number")
guest_table.heading("Check-in Time", text="Check-out Time")
guest_table.heading("Check-out Time", text="Check-out Time")

guest_table.column("Name", width=150)
guest_table.column("Room Number", width=100)
guest_table.column("Check-in Time", width=150)
guest_table.column("Check-out Time", width=150)
guest_table.pack(fill=tk.BOTH, expand=True)

original_data = None  #  For comparison when modifying records

load_guest_data()

root.mainloop()
