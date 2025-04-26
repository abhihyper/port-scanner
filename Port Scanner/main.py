import socket
import threading

# Function to scan a single port
def scan_port(ip, port, open_ports):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout after 1 second if no response
        
        # Attempt to connect to the port
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            open_ports.append(port)  # Add port to list if it's open
            print(f"Port {port}: OPEN")
        sock.close()
    
    except socket.error:
        pass  # Ignore errors for individual ports

# Function to validate the input and resolve domain names
def get_input():
    try:
        ip_or_domain = input("Enter target IP address or domain name: ")

        # Check if input is an IP address or a domain name
        try:
            # Try to resolve the domain name to an IP address
            ip = socket.gethostbyname(ip_or_domain)
            print(f"Resolved IP address: {ip}")
        except socket.error:
            # If it's not a domain name, check if it's an IP address
            try:
                socket.inet_aton(ip_or_domain)  # Raises error for invalid IP format
                ip = ip_or_domain
                print(f"Using provided IP address: {ip}")
            except socket.error:
                print("Error: Invalid IP address or domain name format")
                exit(1)
        
        port_range = input("Enter port range (start_port-end_port): ")
        
        # Split the port range into start and end port
        start_port, end_port = map(int, port_range.split('-'))
        
        if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
            raise ValueError("Ports must be between 1 and 65535")
        if start_port > end_port:
            raise ValueError("Start port cannot be greater than end port")
        
        return ip, start_port, end_port
    
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

# Function to start the port scanning process
def port_scanner(ip, start_port, end_port):
    open_ports = []
    threads = []
    
    print(f"\nScanning {ip} from port {start_port} to {end_port}...\n")
    
    # Create and start threads for each port
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return open_ports

# Main execution
if __name__ == "__main__":
    print("=== Port Scanner with Multi-threading ===")
    ip, start_port, end_port = get_input()
    open_ports = port_scanner(ip, start_port, end_port)
    
    if open_ports:
        print("\nScan complete. Open ports found:")
        for port in open_ports:
            print(f"- Port {port}")
    else:
        print("\nScan complete. No open ports found in the specified range.")
