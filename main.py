import customtkinter as ctk
from tkinter import messagebox, filedialog
import csv
from jobspy import scrape_jobs
import threading
import os

ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def scrape_and_save():
    search_term = search_entry.get()
    site_names_input = sites_entry.get()
    location = location_entry.get()
    results_wanted = int(results_entry.get())

    if not search_term or not site_names_input or not location:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    site_names = [site.strip().lower() for site in site_names_input.split(',')]

    progress_bar.set(0)
    status_label.configure(text="Scraping jobs...")
    scrape_button.configure(state='disabled')

    def scrape_thread():
        try:
            jobs = scrape_jobs(
                site_name=site_names,
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                hours_old=72,
                country_indeed='USA'
            )

            status_label.configure(text=f"Found {len(jobs)} jobs")
            progress_bar.set(0.5)

            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                jobs.to_csv(file_path, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
                progress_bar.set(1)
                status_label.configure(text=f"Jobs saved to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Found {len(jobs)} jobs. Saved to {os.path.basename(file_path)}")
            else:
                status_label.configure(text="Save operation cancelled")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_label.configure(text="An error occurred")
        finally:
            scrape_button.configure(state='normal')

    threading.Thread(target=scrape_thread).start()

# Create the main window
root = ctk.CTk()
root.title("Job Scraper")
root.geometry("600x500")

# Create a main frame
main_frame = ctk.CTkFrame(root, corner_radius=20)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Create and place widgets
search_entry = ctk.CTkEntry(main_frame, placeholder_text="Job Title")
search_entry.pack(pady=(20, 10), padx=20, fill="x")

sites_entry = ctk.CTkEntry(main_frame, placeholder_text="Sites (comma-separated)")
sites_entry.pack(pady=10, padx=20, fill="x")

location_entry = ctk.CTkEntry(main_frame, placeholder_text="Location")
location_entry.insert(0, "Dallas, TX")  # Default value
location_entry.pack(pady=10, padx=20, fill="x")

results_entry = ctk.CTkEntry(main_frame, placeholder_text="Number of Results")
results_entry.insert(0, "20")  # Default value
results_entry.pack(pady=10, padx=20, fill="x")

scrape_button = ctk.CTkButton(main_frame, text="Scrape Jobs", command=scrape_and_save)
scrape_button.pack(pady=20)

status_label = ctk.CTkLabel(main_frame, text="")
status_label.pack(pady=10)

progress_bar = ctk.CTkProgressBar(main_frame)
progress_bar.pack(pady=10, padx=20, fill="x")
progress_bar.set(0)

# Function to center the window
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'+{x}+{y}')

center_window(root)

# Start the GUI event loop
root.mainloop()