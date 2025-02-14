import socket
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox

# --- Network Functions ---

def ping_host(host):
    """Ping a host to check connectivity."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "4", host]
    try:
        output = subprocess.run(command, capture_output=True, text=True, check=True)
        return output.stdout
    except subprocess.CalledProcessError:
        return f"Failed to reach {host}"

def dns_lookup(domain):
    """Resolve a domain to an IP address."""
    try:
        ip = socket.gethostbyname(domain)
        return f"{domain} resolves to {ip}"
    except socket.gaierror:
        return f"Failed to resolve {domain}"

def check_open_port(host, port):
    """Check if a port is open on a host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex((host, port))
        if result == 0:
            return f"Port {port} on {host} is open"
        else:
            return f"Port {port} on {host} is closed"

# --- GUI Functions ---

def run_ping():
    host = entry.get()
    if not host:
        messagebox.showwarning("Input Error", "Please enter a host or IP address.")
        return
    result = ping_host(host)
    messagebox.showinfo("Ping Result", result)

def run_dns_lookup():
    domain = entry.get()
    if not domain:
        messagebox.showwarning("Input Error", "Please enter a domain.")
        return
    result = dns_lookup(domain)
    messagebox.showinfo("DNS Lookup Result", result)

def run_port_check():
    host = entry.get()
    port = port_entry.get()
    if not host or not port:
        messagebox.showwarning("Input Error", "Please enter a host and port.")
        return
    try:
        port = int(port)
        result = check_open_port(host, port)
        messagebox.showinfo("Port Check Result", result)
    except ValueError:
        messagebox.showwarning("Input Error", "Port must be a number.")

# --- GUI Setup ---

root = tk.Tk()
root.title("Python Network Troubleshooter")

tk.Label(root, text="Enter Host/Domain:").pack()
entry = tk.Entry(root)
entry.pack()

tk.Label(root, text="Enter Port (Optional):").pack()
port_entry = tk.Entry(root)
port_entry.pack()

tk.Button(root, text="Ping", command=run_ping).pack()
tk.Button(root, text="DNS Lookup", command=run_dns_lookup).pack()
tk.Button(root, text="Check Open Port", command=run_port_check).pack()

root.mainloop()