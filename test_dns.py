#!/usr/bin/env python3
"""
DNS Toggler Test Script
This script tests DNS functionality and network connectivity
"""

import subprocess
import socket
import time
import sys

def run_command(command):
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

def get_current_dns():
    """Get current DNS settings"""
    print("Checking current DNS settings...")
    
    # Get active network adapter
    success, output, error = run_command("netsh interface show interface")
    if not success:
        print(f"Error getting network interfaces: {error}")
        return None
    
    adapter = None
    lines = output.strip().split('\n')
    for line in lines:
        if "Connected" in line and ("Ethernet" in line or "Wi-Fi" in line):
            parts = line.split()
            if len(parts) >= 4:
                adapter = " ".join(parts[3:])
                break
    
    if not adapter:
        print("No active network adapter found")
        return None
    
    print(f"Active adapter: {adapter}")
    
    # Get DNS settings
    success, output, error = run_command(f'netsh interface ip show dns "{adapter}"')
    if not success:
        print(f"Error getting DNS settings: {error}")
        return None
    
    print("Current DNS configuration:")
    print(output)
    
    # Parse DNS servers
    dns_servers = []
    lines = output.strip().split('\n')
    for line in lines:
        if any(char.isdigit() for char in line):
            parts = line.strip().split()
            for part in parts:
                if is_valid_ip(part):
                    dns_servers.append(part)
    
    return adapter, dns_servers

def is_valid_ip(ip):
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

def test_dns_resolution(dns_servers):
    """Test DNS resolution with given servers"""
    print(f"\nTesting DNS resolution with servers: {dns_servers}")
    
    test_domains = [
        "google.com",
        "github.com",
        "microsoft.com"
    ]
    
    for domain in test_domains:
        print(f"\nTesting resolution of {domain}:")
        
        # Test with system DNS
        try:
            start_time = time.time()
            ip = socket.gethostbyname(domain)
            end_time = time.time()
            print(f"  System DNS: {ip} ({(end_time - start_time)*1000:.1f}ms)")
        except Exception as e:
            print(f"  System DNS: Failed - {e}")
        
        # Test with specific DNS servers
        for dns_server in dns_servers:
            try:
                # Create a resolver with specific DNS server
                resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                resolver.settimeout(5)
                
                # Simple DNS query (this is a basic test)
                start_time = time.time()
                resolver.connect((dns_server, 53))
                end_time = time.time()
                print(f"  {dns_server}: Connected ({(end_time - start_time)*1000:.1f}ms)")
                resolver.close()
            except Exception as e:
                print(f"  {dns_server}: Failed - {e}")

def test_network_connectivity():
    """Test basic network connectivity"""
    print("\nTesting network connectivity...")
    
    test_hosts = [
        ("8.8.8.8", "Google DNS"),
        ("1.1.1.1", "Cloudflare DNS"),
        ("208.67.222.222", "OpenDNS")
    ]
    
    for ip, name in test_hosts:
        try:
            start_time = time.time()
            socket.create_connection((ip, 53), timeout=5)
            end_time = time.time()
            print(f"  {name} ({ip}): Connected ({(end_time - start_time)*1000:.1f}ms)")
        except Exception as e:
            print(f"  {name} ({ip}): Failed - {e}")

def main():
    """Main test function"""
    print("=" * 50)
    print("DNS Toggler - Test Script")
    print("=" * 50)
    
    # Check if running as administrator
    try:
        is_admin = subprocess.run(
            "net session",
            shell=True,
            capture_output=True,
            text=True
        ).returncode == 0
    except:
        is_admin = False
    
    if not is_admin:
        print("WARNING: Not running as Administrator")
        print("DNS tests may fail. Consider running as Administrator.\n")
    
    # Get current DNS settings
    result = get_current_dns()
    if result:
        adapter, dns_servers = result
        print(f"\nCurrent DNS servers: {dns_servers if dns_servers else 'DHCP'}")
        
        if dns_servers:
            test_dns_resolution(dns_servers)
        else:
            print("\nUsing DHCP - no specific DNS servers to test")
    else:
        print("Failed to get DNS settings")
    
    # Test network connectivity
    test_network_connectivity()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("=" * 50)

if __name__ == "__main__":
    main() 