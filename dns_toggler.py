import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import customtkinter as ctk
import subprocess
import json
import os
from typing import Dict, List, Tuple
import threading
import time
import webbrowser

# Set appearance mode
ctk.set_appearance_mode("dark")

class DNSToggler:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("DNS Toggler - Windows")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # DNS servers data
        self.dns_servers = {
            "Electro": ["78.157.42.100", "78.157.42.101"],
            "Shecan": ["178.22.122.100", "185.51.200.2"],
            "Begzar": ["185.55.226.26", "185.55.225.25"],
            "Server.ir": ["65.109.177.244", "65.109.209.224"],
            "Shatel": ["85.15.1.14", "85.15.1.15"],
            "Radar": ["10.202.10.10", "10.202.10.11"],
            "hostiran.net": ["172.29.2.100", "172.29.0.100"]
        }
        
        self.current_dns = None
        self.is_dns_enabled = False
        self.load_custom_dns()
        
        self.setup_ui()
        self.check_current_dns()
        
    def load_custom_dns(self):
        """Load custom DNS servers from file"""
        try:
            if os.path.exists("custom_dns.json"):
                with open("custom_dns.json", "r") as f:
                    custom_dns = json.load(f)
                    self.dns_servers.update(custom_dns)
        except Exception as e:
            print(f"Error loading custom DNS: {e}")
    
    def save_custom_dns(self):
        """Save custom DNS servers to file"""
        try:
            with open("custom_dns.json", "w") as f:
                json.dump(self.dns_servers, f, indent=2)
        except Exception as e:
            print(f"Error saving custom DNS: {e}")
    
    def show_about(self):
        """Show about dialog with English description"""
        about_text = """This software is developed by Ehsan Ehsanpour.
This software is open source and free. If you encounter any bugs or issues, you can open a new issue on the GitHub project at https://github.com/ehsaanpour/SetDNS-Win"""
        
        # Create about dialog
        about_dialog = ctk.CTkToplevel(self.root)
        about_dialog.title("About DNS Toggler")
        about_dialog.geometry("600x400")
        about_dialog.transient(self.root)
        about_dialog.grab_set()
        
        # Center the dialog
        about_dialog.update_idletasks()
        x = (about_dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (about_dialog.winfo_screenheight() // 2) - (400 // 2)
        about_dialog.geometry(f"600x400+{x}+{y}")
        
        # Title
        title_label = ctk.CTkLabel(
            about_dialog,
            text="DNS Toggler - Windows",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Version
        version_label = ctk.CTkLabel(
            about_dialog,
            text="Version 1.0.0",
            font=ctk.CTkFont(size=14)
        )
        version_label.pack(pady=(0, 20))
        
        # About text
        about_textbox = ctk.CTkTextbox(
            about_dialog,
            width=550,
            height=200,
            font=ctk.CTkFont(size=12)
        )
        about_textbox.pack(pady=10, padx=20)
        about_textbox.insert("1.0", about_text)
        about_textbox.configure(state="disabled")
        
        # GitHub link button
        def open_github():
            webbrowser.open("https://github.com/ehsaanpour/SetDNS-Win")
        
        github_button = ctk.CTkButton(
            about_dialog,
            text="Open GitHub Repository",
            command=open_github,
            font=ctk.CTkFont(size=14),
            height=35
        )
        github_button.pack(pady=10)
        
        # Close button
        close_button = ctk.CTkButton(
            about_dialog,
            text="Close",
            command=about_dialog.destroy,
            font=ctk.CTkFont(size=14),
            height=35
        )
        close_button.pack(pady=10)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="DNS Toggler", 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Status frame
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Checking DNS status...",
            font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(pady=10)
        
        # Current DNS display
        self.current_dns_label = ctk.CTkLabel(
            status_frame,
            text="Current DNS: Auto (DHCP)",
            font=ctk.CTkFont(size=14)
        )
        self.current_dns_label.pack(pady=5)
        
        # Toggle button
        self.toggle_button = ctk.CTkButton(
            status_frame,
            text="Enable DNS",
            command=self.toggle_dns,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40
        )
        self.toggle_button.pack(pady=20)
        
        # DNS Selection frame
        selection_frame = ctk.CTkFrame(main_frame)
        selection_frame.pack(fill="x", padx=20, pady=10)
        
        # DNS Selection label
        selection_label = ctk.CTkLabel(
            selection_frame,
            text="Select DNS Server:",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        selection_label.pack(pady=10)
        
        # DNS Selection combobox
        self.dns_var = ctk.StringVar(value="Electro")
        self.dns_combo = ctk.CTkComboBox(
            selection_frame,
            values=list(self.dns_servers.keys()),
            variable=self.dns_var,
            font=ctk.CTkFont(size=14),
            width=200
        )
        self.dns_combo.pack(pady=10)
        
        # DNS info display
        self.dns_info_label = ctk.CTkLabel(
            selection_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.dns_info_label.pack(pady=5)
        
        # Update DNS info when selection changes
        self.dns_combo.bind("<<ComboboxSelected>>", self.update_dns_info)
        self.update_dns_info()
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        # Add Custom DNS button
        add_dns_button = ctk.CTkButton(
            buttons_frame,
            text="Add Custom DNS",
            command=self.add_custom_dns,
            font=ctk.CTkFont(size=14),
            height=35
        )
        add_dns_button.pack(side="left", padx=10, pady=10)
        
        # About button
        about_button = ctk.CTkButton(
            buttons_frame,
            text="About",
            command=self.show_about,
            font=ctk.CTkFont(size=14),
            height=35
        )
        about_button.pack(side="left", padx=10, pady=10)
        
        # Refresh button
        refresh_button = ctk.CTkButton(
            buttons_frame,
            text="Refresh Status",
            command=self.refresh_status,
            font=ctk.CTkFont(size=14),
            height=35
        )
        refresh_button.pack(side="right", padx=10, pady=10)
        
        # Log frame
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Log label
        log_label = ctk.CTkLabel(
            log_frame,
            text="Activity Log:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        log_label.pack(pady=10)
        
        # Log text area
        self.log_text = ctk.CTkTextbox(
            log_frame,
            height=150,
            font=ctk.CTkFont(size=12)
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log("DNS Toggler started")
    
    def update_dns_info(self, event=None):
        """Update DNS info display"""
        selected_dns = self.dns_var.get()
        if selected_dns in self.dns_servers:
            dns_servers = self.dns_servers[selected_dns]
            info_text = f"Primary: {dns_servers[0]}\nSecondary: {dns_servers[1]}"
            self.dns_info_label.configure(text=info_text)
    
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert("end", log_message)
        self.log_text.see("end")
        print(log_message.strip())
    
    def run_command(self, command):
        """Run a command and return the result"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def get_active_network_adapter(self):
        """Get the active network adapter name"""
        success, output, error = self.run_command("netsh interface show interface")
        if success:
            lines = output.strip().split('\n')
            for line in lines:
                if "Connected" in line and ("Ethernet" in line or "Wi-Fi" in line):
                    parts = line.split()
                    if len(parts) >= 4:
                        return " ".join(parts[3:])
        return "Ethernet"  # Default fallback
    
    def check_current_dns(self):
        """Check current DNS settings"""
        def check():
            adapter = self.get_active_network_adapter()
            success, output, error = self.run_command(f'netsh interface ip show dns "{adapter}"')
            
            if success:
                if "DHCP" in output:
                    self.current_dns = None
                    self.is_dns_enabled = False
                    self.current_dns_label.configure(text="Current DNS: Auto (DHCP)")
                    self.status_label.configure(text="DNS: Disabled (Using DHCP)")
                    self.toggle_button.configure(text="Enable DNS")
                else:
                    # Parse DNS servers from output
                    lines = output.strip().split('\n')
                    dns_servers = []
                    for line in lines:
                        if line.strip().startswith(('0.0.0.0', '1.1.1.1', '8.8.8.8')):
                            continue
                        if any(char.isdigit() for char in line):
                            parts = line.strip().split()
                            for part in parts:
                                if self.is_valid_ip(part):
                                    dns_servers.append(part)
                    
                    if dns_servers:
                        self.current_dns = dns_servers
                        self.is_dns_enabled = True
                        self.current_dns_label.configure(text=f"Current DNS: {', '.join(dns_servers)}")
                        self.status_label.configure(text="DNS: Enabled")
                        self.toggle_button.configure(text="Disable DNS")
                    else:
                        self.current_dns = None
                        self.is_dns_enabled = False
                        self.current_dns_label.configure(text="Current DNS: Auto (DHCP)")
                        self.status_label.configure(text="DNS: Disabled (Using DHCP)")
                        self.toggle_button.configure(text="Enable DNS")
            else:
                self.log(f"Error checking DNS: {error}")
        
        threading.Thread(target=check, daemon=True).start()
    
    def is_valid_ip(self, ip):
        """Check if string is a valid IP address"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            for part in parts:
                if not part.isdigit() or not 0 <= int(part) <= 255:
                    return False
            return True
        except:
            return False
    
    def toggle_dns(self):
        """Toggle DNS settings"""
        if self.is_dns_enabled:
            self.disable_dns()
        else:
            self.enable_dns()
    
    def enable_dns(self):
        """Enable DNS with selected server"""
        def enable():
            selected_dns = self.dns_var.get()
            if selected_dns not in self.dns_servers:
                self.log("Invalid DNS selection")
                return
            
            dns_servers = self.dns_servers[selected_dns]
            adapter = self.get_active_network_adapter()
            
            self.log(f"Enabling DNS: {selected_dns} ({', '.join(dns_servers)})")
            
            # Set primary DNS
            success1, output1, error1 = self.run_command(
                f'netsh interface ip set dns "{adapter}" static {dns_servers[0]}'
            )
            
            # Set secondary DNS
            success2, output2, error2 = self.run_command(
                f'netsh interface ip add dns "{adapter}" {dns_servers[1]} index=2'
            )
            
            if success1 and success2:
                self.log(f"Successfully enabled {selected_dns} DNS")
                self.is_dns_enabled = True
                self.current_dns = dns_servers
                self.status_label.configure(text=f"DNS: Enabled ({selected_dns})")
                self.toggle_button.configure(text="Disable DNS")
                self.current_dns_label.configure(text=f"Current DNS: {', '.join(dns_servers)}")
                messagebox.showinfo("Success", f"DNS enabled successfully!\nServer: {selected_dns}\nAddresses: {', '.join(dns_servers)}")
            else:
                error_msg = f"Failed to enable DNS: {error1 or error2}"
                self.log(error_msg)
                messagebox.showerror("Error", error_msg)
        
        threading.Thread(target=enable, daemon=True).start()
    
    def disable_dns(self):
        """Disable DNS and use DHCP"""
        def disable():
            adapter = self.get_active_network_adapter()
            
            self.log("Disabling DNS (switching to DHCP)")
            
            success, output, error = self.run_command(
                f'netsh interface ip set dns "{adapter}" dhcp'
            )
            
            if success:
                self.log("Successfully disabled DNS (DHCP enabled)")
                self.is_dns_enabled = False
                self.current_dns = None
                self.status_label.configure(text="DNS: Disabled (Using DHCP)")
                self.toggle_button.configure(text="Enable DNS")
                self.current_dns_label.configure(text="Current DNS: Auto (DHCP)")
                messagebox.showinfo("Success", "DNS disabled successfully!\nSwitched to DHCP mode.")
            else:
                error_msg = f"Failed to disable DNS: {error}"
                self.log(error_msg)
                messagebox.showerror("Error", error_msg)
        
        threading.Thread(target=disable, daemon=True).start()
    
    def add_custom_dns(self):
        """Add custom DNS server"""
        # Create custom dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Custom DNS")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Name entry
        name_label = ctk.CTkLabel(dialog, text="DNS Name:", font=ctk.CTkFont(size=14))
        name_label.pack(pady=(20, 5))
        
        name_entry = ctk.CTkEntry(dialog, width=300, font=ctk.CTkFont(size=14))
        name_entry.pack(pady=5)
        
        # Primary DNS entry
        primary_label = ctk.CTkLabel(dialog, text="Primary DNS:", font=ctk.CTkFont(size=14))
        primary_label.pack(pady=(10, 5))
        
        primary_entry = ctk.CTkEntry(dialog, width=300, font=ctk.CTkFont(size=14))
        primary_entry.pack(pady=5)
        
        # Secondary DNS entry
        secondary_label = ctk.CTkLabel(dialog, text="Secondary DNS:", font=ctk.CTkFont(size=14))
        secondary_label.pack(pady=(10, 5))
        
        secondary_entry = ctk.CTkEntry(dialog, width=300, font=ctk.CTkFont(size=14))
        secondary_entry.pack(pady=5)
        
        def save_custom_dns():
            name = name_entry.get().strip()
            primary = primary_entry.get().strip()
            secondary = secondary_entry.get().strip()
            
            if not name or not primary or not secondary:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            if not self.is_valid_ip(primary) or not self.is_valid_ip(secondary):
                messagebox.showerror("Error", "Please enter valid IP addresses!")
                return
            
            if name in self.dns_servers:
                messagebox.showerror("Error", "DNS name already exists!")
                return
            
            # Add to dictionary
            self.dns_servers[name] = [primary, secondary]
            
            # Update combobox
            current_values = list(self.dns_combo.cget("values"))
            current_values.append(name)
            self.dns_combo.configure(values=current_values)
            
            # Save to file
            self.save_custom_dns()
            
            self.log(f"Added custom DNS: {name} ({primary}, {secondary})")
            messagebox.showinfo("Success", f"Custom DNS '{name}' added successfully!")
            dialog.destroy()
        
        # Save button
        save_button = ctk.CTkButton(
            dialog,
            text="Save",
            command=save_custom_dns,
            font=ctk.CTkFont(size=14),
            height=35
        )
        save_button.pack(pady=20)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            dialog,
            text="Cancel",
            command=dialog.destroy,
            font=ctk.CTkFont(size=14),
            height=35
        )
        cancel_button.pack(pady=5)
    
    def refresh_status(self):
        """Refresh DNS status"""
        self.log("Refreshing DNS status...")
        self.check_current_dns()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = DNSToggler()
    app.run() 