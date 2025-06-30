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
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        
        # Language settings
        self.current_language = "en"  # Default language
        self.languages = {
            "en": {
                "title": "DNS Toggler",
                "checking_status": "Checking DNS status...",
                "current_dns_dhcp": "Current DNS: Auto (DHCP)",
                "enable_dns": "Enable DNS",
                "disable_dns": "Disable DNS",
                "select_dns": "Select DNS Server:",
                "add_custom_dns": "Add Custom DNS",
                "about": "About",
                "refresh_status": "Refresh Status",
                "activity_log": "Activity Log:",
                "dns_enabled": "DNS: Enabled",
                "dns_disabled": "DNS: Disabled (Using DHCP)",
                "dns_enabled_with_server": "DNS: Enabled ({})",
                "primary": "Primary: {}",
                "secondary": "Secondary: {}",
                "dns_name": "DNS Name:",
                "primary_dns": "Primary DNS:",
                "secondary_dns": "Secondary DNS:",
                "save": "Save",
                "cancel": "Cancel",
                "close": "Close",
                "open_github": "Open GitHub Repository",
                "about_title": "About DNS Toggler",
                "version": "Version 1.1.0",
                "about_text": "This software is developed by Ehsan Ehsanpour.\nThis software is open source and free. If you encounter any bugs or issues, you can open a new issue on the GitHub project at https://github.com/ehsaanpour/SetDNS-Win",
                "language": "Language",
                "english": "English",
                "persian": "Persian",
                "success": "Success",
                "error": "Error",
                "dns_enabled_success": "DNS enabled successfully!\nServer: {}\nAddresses: {}",
                "dns_disabled_success": "DNS disabled successfully!\nSwitched to DHCP mode.",
                "all_fields_required": "All fields are required!",
                "enter_valid_ip": "Please enter valid IP addresses!",
                "dns_name_exists": "DNS name already exists!",
                "custom_dns_added": "Custom DNS '{}' added successfully!",
                "failed_enable_dns": "Failed to enable DNS: {}",
                "failed_disable_dns": "Failed to disable DNS: {}",
                "invalid_dns_selection": "Invalid DNS selection",
                "enabling_dns": "Enabling DNS: {} ({})",
                "disabling_dns": "Disabling DNS (switching to DHCP)",
                "successfully_enabled": "Successfully enabled {} DNS",
                "successfully_disabled": "Successfully disabled DNS (DHCP enabled)",
                "refreshing_status": "Refreshing DNS status...",
                "error_checking_dns": "Error checking DNS: {}",
                "dns_toggler_started": "DNS Toggler started",
                "added_custom_dns": "Added custom DNS: {} ({}, {})",
                "admin_required": "Administrator privileges are required to disable DNS."
            },
            "fa": {
                "title": "تغییر دهنده DNS",
                "checking_status": "در حال بررسی وضعیت DNS...",
                "current_dns_dhcp": "DNS فعلی: خودکار (DHCP)",
                "enable_dns": "فعال کردن DNS",
                "disable_dns": "غیرفعال کردن DNS",
                "select_dns": "انتخاب سرور DNS:",
                "add_custom_dns": "افزودن DNS سفارشی",
                "about": "درباره",
                "refresh_status": "بروزرسانی وضعیت",
                "activity_log": "گزارش فعالیت:",
                "dns_enabled": "DNS: فعال",
                "dns_disabled": "DNS: غیرفعال (استفاده از DHCP)",
                "dns_enabled_with_server": "DNS: فعال ({})",
                "primary": "اصلی: {}",
                "secondary": "ثانویه: {}",
                "dns_name": "نام DNS:",
                "primary_dns": "DNS اصلی:",
                "secondary_dns": "DNS ثانویه:",
                "save": "ذخیره",
                "cancel": "انصراف",
                "close": "بستن",
                "open_github": "باز کردن مخزن GitHub",
                "about_title": "درباره تغییر دهنده DNS",
                "version": "نسخه ۱.۱.۰",
                "about_text": "این نرم افزار توسط احسان احسانپور توسعه پیدا کرده است.\nاین نرم افزار متن باز و رایگان می باشد، درصورت مشاهده هرگونه باگ یا مشکل می توانید در گیت هاب این پروژه به آدرس https://github.com/ehsaanpour/SetDNS-Win یک issue جدید باز کنید.",
                "language": "زبان",
                "english": "انگلیسی",
                "persian": "فارسی",
                "success": "موفقیت",
                "error": "خطا",
                "dns_enabled_success": "DNS با موفقیت فعال شد!\nسرور: {}\nآدرس‌ها: {}",
                "dns_disabled_success": "DNS با موفقیت غیرفعال شد!\nبه حالت DHCP تغییر یافت.",
                "all_fields_required": "تمام فیلدها الزامی هستند!",
                "enter_valid_ip": "لطفاً آدرس‌های IP معتبر وارد کنید!",
                "dns_name_exists": "نام DNS قبلاً وجود دارد!",
                "custom_dns_added": "DNS سفارشی '{}' با موفقیت اضافه شد!",
                "failed_enable_dns": "فعال کردن DNS ناموفق بود: {}",
                "failed_disable_dns": "غیرفعال کردن DNS ناموفق بود: {}",
                "invalid_dns_selection": "انتخاب DNS نامعتبر",
                "enabling_dns": "در حال فعال کردن DNS: {} ({})",
                "disabling_dns": "در حال غیرفعال کردن DNS (تغییر به DHCP)",
                "successfully_enabled": "DNS {} با موفقیت فعال شد",
                "successfully_disabled": "DNS با موفقیت غیرفعال شد (DHCP فعال شد)",
                "refreshing_status": "در حال بروزرسانی وضعیت DNS...",
                "error_checking_dns": "خطا در بررسی DNS: {}",
                "dns_toggler_started": "تغییر دهنده DNS شروع شد",
                "added_custom_dns": "DNS سفارشی اضافه شد: {} ({}, {})",
                "admin_required": "دسترسی مدیر سیستم برای غیرفعال کردن DNS اجباری است."
            }
        }
        
        # DNS servers data
        self.default_dns_servers = {
            "Electro": ["78.157.42.100", "78.157.42.101"],
            "Shecan": ["178.22.122.100", "185.51.200.2"],
            "Begzar": ["185.55.226.26", "185.55.225.25"],
            "Server.ir": ["65.109.177.244", "65.109.209.224"],
            "Shatel": ["85.15.1.14", "85.15.1.15"],
            "Radar": ["10.202.10.10", "10.202.10.11"],
            "hostiran.net": ["172.29.2.100", "172.29.0.100"]
        }
        self.dns_servers = self.default_dns_servers.copy()
        
        self.current_dns = None
        self.is_dns_enabled = False
        self.load_custom_dns()
        
        self.setup_ui()
        self.check_current_dns()
    
    def get_text(self, key):
        """Get text in current language"""
        return self.languages[self.current_language].get(key, key)
    
    def switch_language(self, language):
        """Switch application language"""
        self.current_language = language
        self.update_ui_text()
    
    def update_ui_text(self):
        """Update all UI text elements to current language"""
        # Update window title
        self.root.title(f"{self.get_text('title')} - Windows")
        
        # Update main title
        self.title_label.configure(text=self.get_text('title'))
        
        # Update status label
        if self.is_dns_enabled:
            if self.current_dns:
                self.status_label.configure(text=self.get_text('dns_enabled_with_server').format(self.dns_var.get()))
            else:
                self.status_label.configure(text=self.get_text('dns_enabled'))
        else:
            self.status_label.configure(text=self.get_text('dns_disabled'))
        
        # Update current DNS label
        if self.current_dns:
            self.current_dns_label.configure(text=f"Current DNS: {', '.join(self.current_dns)}")
        else:
            self.current_dns_label.configure(text=self.get_text('current_dns_dhcp'))
        
        # Update toggle button
        if self.is_dns_enabled:
            self.toggle_button.configure(text=self.get_text('disable_dns'))
        else:
            self.toggle_button.configure(text=self.get_text('enable_dns'))
        
        # Update selection label
        self.selection_label.configure(text=self.get_text('select_dns'))
        
        # Update DNS info
        self.update_dns_info()
        
        # Update button texts
        self.add_dns_button.configure(text=self.get_text('add_custom_dns'))
        self.about_button.configure(text=self.get_text('about'))
        self.refresh_button.configure(text=self.get_text('refresh_status'))
        
        # Update log label
        self.log_label.configure(text=self.get_text('activity_log'))
        
        # Update language button
        if self.current_language == "en":
            self.language_button.configure(text=self.get_text('persian'))
        else:
            self.language_button.configure(text=self.get_text('english'))
        
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
            custom_dns = {}
            for name, servers in self.dns_servers.items():
                if name not in self.default_dns_servers or self.default_dns_servers.get(name) != servers:
                    custom_dns[name] = servers
            
            with open("custom_dns.json", "w") as f:
                json.dump(custom_dns, f, indent=2)
        except Exception as e:
            print(f"Error saving custom DNS: {e}")
    
    def show_about(self):
        """Show about dialog with bilingual description"""
        about_text = self.get_text('about_text')
        
        # Create about dialog
        about_dialog = ctk.CTkToplevel(self.root)
        about_dialog.title(self.get_text('about_title'))
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
            text=f"{self.get_text('title')} - Windows",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Version
        version_label = ctk.CTkLabel(
            about_dialog,
            text=self.get_text('version'),
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
            text=self.get_text('open_github'),
            command=open_github,
            font=ctk.CTkFont(size=14),
            height=35
        )
        github_button.pack(pady=10)
        
        # Close button
        close_button = ctk.CTkButton(
            about_dialog,
            text=self.get_text('close'),
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
        self.title_label = ctk.CTkLabel(
            main_frame, 
            text=self.get_text('title'), 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.pack(pady=(20, 30))
        
        # Status frame
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            status_frame,
            text=self.get_text('checking_status'),
            font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(pady=10)
        
        # Current DNS display
        self.current_dns_label = ctk.CTkLabel(
            status_frame,
            text=self.get_text('current_dns_dhcp'),
            font=ctk.CTkFont(size=14)
        )
        self.current_dns_label.pack(pady=5)
        
        # Toggle button
        self.toggle_button = ctk.CTkButton(
            status_frame,
            text=self.get_text('enable_dns'),
            command=self.toggle_dns,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40
        )
        self.toggle_button.pack(pady=20)
        
        # DNS Selection frame
        selection_frame = ctk.CTkFrame(main_frame)
        selection_frame.pack(fill="x", padx=20, pady=10)
        
        # DNS Selection label
        self.selection_label = ctk.CTkLabel(
            selection_frame,
            text=self.get_text('select_dns'),
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.selection_label.pack(pady=10)
        
        # DNS Selection combobox
        self.dns_var = ctk.StringVar(value="Electro" if "Electro" in self.dns_servers else "")
        
        # DNS Selection scrollable frame
        self.dns_scroll_frame = ctk.CTkScrollableFrame(selection_frame, height=120)
        self.dns_scroll_frame.pack(fill="x", padx=10, pady=5)

        self.populate_dns_list()
        
        # DNS info display
        self.dns_info_label = ctk.CTkLabel(
            selection_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.dns_info_label.pack(pady=5)
        
        # Update DNS info when selection changes
        self.update_dns_info()
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        # Add Custom DNS button
        self.add_dns_button = ctk.CTkButton(
            buttons_frame,
            text=self.get_text('add_custom_dns'),
            command=self.add_custom_dns,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.add_dns_button.pack(side="left", padx=10, pady=10)
        
        # About button
        self.about_button = ctk.CTkButton(
            buttons_frame,
            text=self.get_text('about'),
            command=self.show_about,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.about_button.pack(side="left", padx=10, pady=10)
        
        # Language button
        self.language_button = ctk.CTkButton(
            buttons_frame,
            text=self.get_text('persian'),
            command=lambda: self.switch_language("fa" if self.current_language == "en" else "en"),
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.language_button.pack(side="left", padx=10, pady=10)
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(
            buttons_frame,
            text=self.get_text('refresh_status'),
            command=self.refresh_status,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.refresh_button.pack(side="right", padx=10, pady=10)
        
        # Log frame
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Log label
        self.log_label = ctk.CTkLabel(
            log_frame,
            text=self.get_text('activity_log'),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.log_label.pack(pady=10)
        
        # Log text area
        self.log_text = ctk.CTkTextbox(
            log_frame,
            height=150,
            font=ctk.CTkFont(size=12)
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log(self.get_text('dns_toggler_started'))
    
    def populate_dns_list(self):
        """Populate the DNS server list in the UI"""
        # Clear existing widgets
        for widget in self.dns_scroll_frame.winfo_children():
            widget.destroy()
        
        dns_names = list(self.dns_servers.keys())
        if not dns_names:
            no_server_label = ctk.CTkLabel(self.dns_scroll_frame, text="No DNS servers available.")
            no_server_label.pack(pady=10)
            return

        for dns_name in dns_names:
            entry_frame = ctk.CTkFrame(self.dns_scroll_frame)
            entry_frame.pack(fill="x", padx=5, pady=3, expand=True)
            
            radio_button = ctk.CTkRadioButton(
                entry_frame,
                text=dns_name,
                variable=self.dns_var,
                value=dns_name,
                command=self.update_dns_info
            )
            radio_button.pack(side="left", padx=(5, 0))

            remove_button = ctk.CTkButton(
                entry_frame,
                text="X",
                command=lambda name=dns_name: self.remove_dns(name),
                width=28,
                height=28,
                fg_color="transparent",
                text_color=("#FF0000", "#FF0000"),
                hover_color=("#e0e0e0", "#404040")
            )
            remove_button.pack(side="right", padx=(0, 5))

    def remove_dns(self, dns_name_to_remove):
        """Remove a DNS server from the list"""
        if dns_name_to_remove in self.dns_servers:
            del self.dns_servers[dns_name_to_remove]
            self.save_custom_dns()
            self.log(f"Removed DNS server: {dns_name_to_remove}")
            
            if self.dns_var.get() == dns_name_to_remove:
                if self.dns_servers:
                    self.dns_var.set(list(self.dns_servers.keys())[0])
                else:
                    self.dns_var.set("")
            
            self.populate_dns_list()
            self.update_dns_info()

    def update_dns_info(self, event=None):
        """Update DNS info display"""
        selected_dns = self.dns_var.get()
        if selected_dns and selected_dns in self.dns_servers:
            dns_servers = self.dns_servers[selected_dns]
            info_text = f"{self.get_text('primary').format(dns_servers[0])}\n{self.get_text('secondary').format(dns_servers[1])}"
            self.dns_info_label.configure(text=info_text)
        else:
            self.dns_info_label.configure(text="")
    
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
                timeout=30,  # Increased timeout
                creationflags=subprocess.CREATE_NO_WINDOW  # Hide console window
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out. The DNS server might be slow or unreachable."
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
                    self.current_dns_label.configure(text=self.get_text('current_dns_dhcp'))
                    self.status_label.configure(text=self.get_text('dns_disabled'))
                    self.toggle_button.configure(text=self.get_text('enable_dns'))
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
                        self.status_label.configure(text=self.get_text('dns_enabled'))
                        self.toggle_button.configure(text=self.get_text('disable_dns'))
                    else:
                        self.current_dns = None
                        self.is_dns_enabled = False
                        self.current_dns_label.configure(text=self.get_text('current_dns_dhcp'))
                        self.status_label.configure(text=self.get_text('dns_disabled'))
                        self.toggle_button.configure(text=self.get_text('enable_dns'))
            else:
                self.log(self.get_text('error_checking_dns').format(error))
        
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
                self.log(self.get_text('invalid_dns_selection'))
                return
            
            dns_servers = self.dns_servers[selected_dns]
            adapter = self.get_active_network_adapter()
            
            self.log(self.get_text('enabling_dns').format(selected_dns, ', '.join(dns_servers)))
            
            # Set primary DNS
            success1, output1, error1 = self.run_command(
                f'netsh interface ip set dns "{adapter}" static {dns_servers[0]}'
            )
            
            # Set secondary DNS
            success2, output2, error2 = self.run_command(
                f'netsh interface ip add dns "{adapter}" {dns_servers[1]} index=2'
            )
            
            if success1 and success2:
                self.log(self.get_text('successfully_enabled').format(selected_dns))
                self.is_dns_enabled = True
                self.current_dns = dns_servers
                self.status_label.configure(text=self.get_text('dns_enabled_with_server').format(selected_dns))
                self.toggle_button.configure(text=self.get_text('disable_dns'))
                self.current_dns_label.configure(text=f"Current DNS: {', '.join(dns_servers)}")
                messagebox.showinfo(self.get_text('success'), self.get_text('dns_enabled_success').format(selected_dns, ', '.join(dns_servers)))
            else:
                # Check if it's a permission error
                error_text = error1 or error2
                if "Access is denied" in error_text or "access denied" in error_text.lower():
                    error_msg = f"{self.get_text('failed_enable_dns').format(error_text)}\n\n{self.get_text('admin_required')}"
                else:
                    error_msg = self.get_text('failed_enable_dns').format(error_text)
                
                self.log(error_msg)
                messagebox.showerror(self.get_text('error'), error_msg)
        
        threading.Thread(target=enable, daemon=True).start()
    
    def disable_dns(self):
        """Disable DNS and use DHCP"""
        def disable():
            adapter = self.get_active_network_adapter()
            
            self.log(self.get_text('disabling_dns'))
            
            success, output, error = self.run_command(
                f'netsh interface ip set dns "{adapter}" dhcp'
            )
            
            if success:
                self.log(self.get_text('successfully_disabled'))
                self.is_dns_enabled = False
                self.current_dns = None
                self.status_label.configure(text=self.get_text('dns_disabled'))
                self.toggle_button.configure(text=self.get_text('enable_dns'))
                self.current_dns_label.configure(text=self.get_text('current_dns_dhcp'))
                messagebox.showinfo(self.get_text('success'), self.get_text('dns_disabled_success'))
            else:
                # Check if it's a permission error
                if "Access is denied" in error or "access denied" in error.lower():
                    error_msg = f"{self.get_text('failed_disable_dns').format(error)}\n\n{self.get_text('admin_required')}"
                else:
                    error_msg = self.get_text('failed_disable_dns').format(error)
                
                self.log(error_msg)
                messagebox.showerror(self.get_text('error'), error_msg)
        
        threading.Thread(target=disable, daemon=True).start()
    
    def add_custom_dns(self):
        """Add custom DNS server"""
        # Create custom dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(self.get_text('add_custom_dns'))
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Name entry
        name_label = ctk.CTkLabel(dialog, text=self.get_text('dns_name'), font=ctk.CTkFont(size=14))
        name_label.pack(pady=(20, 5))
        
        name_entry = ctk.CTkEntry(dialog, width=300, font=ctk.CTkFont(size=14))
        name_entry.pack(pady=5)
        
        # Primary DNS entry
        primary_label = ctk.CTkLabel(dialog, text=self.get_text('primary_dns'), font=ctk.CTkFont(size=14))
        primary_label.pack(pady=(10, 5))
        
        primary_entry = ctk.CTkEntry(dialog, width=300, font=ctk.CTkFont(size=14))
        primary_entry.pack(pady=5)
        
        # Secondary DNS entry
        secondary_label = ctk.CTkLabel(dialog, text=self.get_text('secondary_dns'), font=ctk.CTkFont(size=14))
        secondary_label.pack(pady=(10, 5))
        
        secondary_entry = ctk.CTkEntry(dialog, width=300, font=ctk.CTkFont(size=14))
        secondary_entry.pack(pady=5)
        
        def save_custom_dns():
            name = name_entry.get().strip()
            primary = primary_entry.get().strip()
            secondary = secondary_entry.get().strip()
            
            if not name or not primary or not secondary:
                messagebox.showerror(self.get_text('error'), self.get_text('all_fields_required'))
                return
            
            if not self.is_valid_ip(primary) or not self.is_valid_ip(secondary):
                messagebox.showerror(self.get_text('error'), self.get_text('enter_valid_ip'))
                return
            
            if name in self.dns_servers:
                messagebox.showerror(self.get_text('error'), self.get_text('dns_name_exists'))
                return
            
            # Add to dictionary
            self.dns_servers[name] = [primary, secondary]
            
            # Update combobox
            self.populate_dns_list()
            self.dns_var.set(name)
            
            # Save to file
            self.save_custom_dns()
            
            self.log(self.get_text('added_custom_dns').format(name, primary, secondary))
            messagebox.showinfo(self.get_text('success'), self.get_text('custom_dns_added').format(name))
            dialog.destroy()
        
        # Save button
        save_button = ctk.CTkButton(
            dialog,
            text=self.get_text('save'),
            command=save_custom_dns,
            font=ctk.CTkFont(size=14),
            height=35
        )
        save_button.pack(pady=20)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            dialog,
            text=self.get_text('cancel'),
            command=dialog.destroy,
            font=ctk.CTkFont(size=14),
            height=35
        )
        cancel_button.pack(pady=5)
    
    def refresh_status(self):
        """Refresh DNS status"""
        self.log(self.get_text('refreshing_status'))
        self.check_current_dns()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = DNSToggler()
    app.run()