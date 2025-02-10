import os
import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from getmac import get_mac_address
import socket
import platform


class NetworkScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Scanner")
        self.root.geometry("600x400")
        
        self.scanning = False
        
        # UI Components
        self.label = tk.Label(root, text="Enter Network IP Prefix (Default: 192.168.1.)")
        self.label.pack(pady=5)
        
        self.ip_entry = tk.Entry(root, width=20)
        self.ip_entry.insert(0, "192.168.1.")
        self.ip_entry.pack(pady=5)
        
        self.scan_button = tk.Button(root, text="Start Scan", command=self.start_scan)
        self.scan_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop Scan", command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        self.progress = ttk.Progressbar(root, length=300, mode='indeterminate')
        self.progress.pack(pady=5)
        
        self.tree = ttk.Treeview(root, columns=("IP", "MAC", "Hostname"), show='headings')
        self.tree.heading("IP", text="IP Address")
        self.tree.heading("MAC", text="MAC Address")
        self.tree.heading("Hostname", text="Hostname")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.active_devices = []
    
    def ping_device(self, ip):
        if platform.system().lower() == "windows":
            response = os.system(f"ping -n 1 -w 500 {ip} > nul 2>&1")
        else:
            response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")

        if response == 0 and self.scanning:
            mac = get_mac_address(ip=ip) or "UNKNOWN_MAC"
            hostname = socket.getfqdn(ip)
            self.active_devices.append((ip, mac, hostname))
            self.tree.insert("", tk.END, values=(ip, mac, hostname))
    
    def scan_network(self):
        self.active_devices.clear()
        self.tree.delete(*self.tree.get_children())
        self.scanning = True
        self.progress.start()
        
        network_prefix = self.ip_entry.get().strip()
        threads = []
        for i in range(1, 255):
            ip = f"{network_prefix}{i}"
            thread = threading.Thread(target=self.ping_device, args=(ip,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        self.progress.stop()
        self.scanning = False
        messagebox.showinfo("Scan Complete", "Network scanning completed!")
    
    def start_scan(self):
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.scan_network, daemon=True).start()
    
    def stop_scan(self):
        self.scanning = False
        self.progress.stop()
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showinfo("Scan Stopped", "Network scanning has been stopped.")


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkScannerGUI(root)
    root.mainloop()
