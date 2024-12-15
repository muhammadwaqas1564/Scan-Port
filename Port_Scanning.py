import socket
import tkinter as tk
from tkinter import messagebox, ttk

def scan_ports():
    """
    Function to scan ports and update progress bar and results in the UI.
    """
    # Get user inputs
    target = target_entry.get()
    start_port = start_port_entry.get()
    end_port = end_port_entry.get()

    # Validate inputs
    if not target or not start_port or not end_port:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        start_port = int(start_port)
        end_port = int(end_port)

        if start_port > end_port:
            messagebox.showerror("Input Error", "Start port must be less than or equal to end port.")
            return

        # Resolve hostname to IP
        resolved_ip = socket.gethostbyname(target)

    except ValueError:
        messagebox.showerror("Input Error", "Ports must be numeric.")
        return
    except socket.gaierror:
        messagebox.showerror("Input Error", f"Could not resolve '{target}' to an IP address.")
        return

    # Prepare for scanning
    results = []
    total_ports = end_port - start_port + 1
    progress_bar["maximum"] = total_ports
    progress_label.config(text="Scanning...")
    progress_bar.pack(pady=10)  # Show progress bar when scan starts

    for count, port in enumerate(range(start_port, end_port + 1), start=1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((resolved_ip, port)) == 0:
                    results.append(f"Port {port}: OPEN")
        except Exception as e:
            results.append(f"Error on port {port}: {e}")

        # Update progress bar
        progress_bar["value"] = count
        progress_percentage = int((count / total_ports) * 100)
        progress_label.config(text=f"Progress: {progress_percentage}%")
        app.update_idletasks()  # Update UI

    # Display results
    if results:
        result_label.config(text="\n".join(results), justify="left")
    else:
        result_label.config(text="No open ports found.")
    
    progress_label.config(text="Scanning Complete.")

# Create main application window
app = tk.Tk()
app.title("Port Scanner")
app.geometry("500x600")

# Set background color for the window
app.config(bg="#f0f0f0")  # Light gray background for the main window

# Create and place input fields and labels with background color
tk.Label(app, text="Target IP/Hostname:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
target_entry = tk.Entry(app, font=("Arial", 12), bg="#ffffff")  # White background for entry fields
target_entry.pack(pady=5)

tk.Label(app, text="Start Port:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
start_port_entry = tk.Entry(app, font=("Arial", 12), bg="#ffffff")
start_port_entry.pack(pady=5)

tk.Label(app, text="End Port:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
end_port_entry = tk.Entry(app, font=("Arial", 12), bg="#ffffff")
end_port_entry.pack(pady=5)

# Create and place submit button with background color
submit_button = tk.Button(app, text="Scan Ports", font=("Arial", 12), command=scan_ports, bg="#4CAF50", fg="white")
submit_button.pack(pady=20)

# Create and place progress bar (hidden initially)
progress_bar = ttk.Progressbar(app, orient="horizontal", length=400, mode="determinate")

# Create and place progress label with background color
progress_label = tk.Label(app, text="Progress: 0%", font=("Arial", 12), bg="#f0f0f0")
progress_label.pack(pady=5)

# Create and place results label with background color
result_label = tk.Label(app, text="", font=("Arial", 12), anchor="w", justify="left", wraplength=450, bg="#f0f0f0")
result_label.pack(pady=10, fill="both", expand=True)

# Run the Tkinter event loop
app.mainloop()
