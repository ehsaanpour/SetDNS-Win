# DNS Toggler for Windows

A beautiful and user-friendly DNS Toggler application for Windows that allows you to easily switch between different DNS servers with just one click.

## Features

### 🎨 Beautiful and User-Friendly UI
- Modern dark theme with blue accent colors
- Clean and intuitive interface
- Real-time status updates
- Activity log for tracking changes

### ⚡ One-Click Toggle
- Easily switch your IPv4 DNS settings on or off
- Automatic detection of current DNS status
- Quick enable/disable functionality

### 🌐 Pre-configured DNS Servers
The application comes with the following DNS servers pre-configured:

| Name | Primary DNS | Secondary DNS |
|------|-------------|---------------|
| **Electro** | 78.157.42.100 | 78.157.42.101 |
| **Shecan** | 178.22.122.100 | 185.51.200.2 |
| **Begzar** | 185.55.226.26 | 185.55.225.25 |
| **Server.ir** | 65.109.177.244 | 65.109.209.224 |
| **Shatel** | 85.15.1.14 | 85.15.1.15 |
| **Radar** | 10.202.10.10 | 10.202.10.11 |
| **hostiran.net** | 172.29.2.100 | 172.29.0.100 |

### ➕ Custom DNS Support
- Add your own custom DNS servers
- Persistent storage of custom DNS configurations
- Easy management of custom DNS entries

## Installation

### Prerequisites
- Windows 10/11
- Python 3.7 or higher
- Administrator privileges (required for DNS changes)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd SetDNS-Win
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python dns_toggler.py
   ```

## Usage

### Basic Usage
1. **Launch the application** - Run `python dns_toggler.py`
2. **Select a DNS server** - Choose from the dropdown menu
3. **Toggle DNS** - Click the "Enable DNS" button to activate the selected DNS server
4. **Disable DNS** - Click "Disable DNS" to switch back to DHCP mode

### Adding Custom DNS Servers
1. Click the **"Add Custom DNS"** button
2. Enter a name for your DNS server
3. Enter the primary and secondary DNS IP addresses
4. Click **"Save"** to add the custom DNS server

### Monitoring
- The application shows real-time DNS status
- Activity log tracks all DNS changes
- Current DNS configuration is displayed at the top

## Features in Detail

### Status Display
- Shows whether DNS is currently enabled or disabled
- Displays current DNS server addresses
- Real-time updates when changes are made

### DNS Selection
- Dropdown menu with all available DNS servers
- Shows primary and secondary DNS addresses for selected server
- Easy switching between different DNS providers

### Activity Log
- Tracks all DNS changes with timestamps
- Helps troubleshoot any issues
- Provides history of DNS modifications

### Custom DNS Management
- Add unlimited custom DNS servers
- Persistent storage in `custom_dns.json`
- Automatic loading of custom DNS on startup

## Technical Details

### Network Interface Detection
- Automatically detects active network adapters (Ethernet/Wi-Fi)
- Supports both wired and wireless connections
- Handles multiple network interfaces

### DNS Configuration
- Uses Windows `netsh` commands for DNS configuration
- Supports both static DNS and DHCP modes
- Handles primary and secondary DNS servers

### Error Handling
- Comprehensive error checking and reporting
- User-friendly error messages
- Graceful handling of network issues

## Troubleshooting

### Common Issues

**"Access Denied" Error**
- Run the application as Administrator
- Right-click on the Python executable and select "Run as Administrator"

**DNS Not Changing**
- Check if you have administrator privileges
- Ensure your network adapter is active
- Try refreshing the status

**Application Won't Start**
- Verify Python is installed correctly
- Check all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're using Python 3.7 or higher

### Network Adapter Issues
- The application automatically detects the active network adapter
- If issues occur, try refreshing the status
- Ensure your network connection is stable

## File Structure

```
SetDNS-Win/
├── dns_toggler.py          # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── custom_dns.json        # Custom DNS storage (created automatically)
└── .git/                  # Git repository
```

## Dependencies

- **customtkinter**: Modern UI framework for tkinter
- **pillow**: Image processing library (required by customtkinter)
- **psutil**: System and process utilities
- **tkinter**: Built-in Python GUI framework

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Review the activity log for error messages
3. Ensure you're running the application as Administrator
4. Verify your network connection is stable

---

**Note**: This application requires Administrator privileges to modify DNS settings on Windows. Always run as Administrator for full functionality. 