#!/usr/bin/env python
"""
Quick Start Script for ERP Dashboard
"""
import os
import subprocess
import socket
import time

def check_port(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
        return True
    except OSError:
        return False

def find_available_port(start_port=8000):
    """Find an available port"""
    for port in range(start_port, start_port + 20):
        if check_port(port):
            return port
    return None

def main():
    print("🚀 ERP Dashboard Quick Start")
    print("="*40)
    
    # Kill existing servers
    try:
        subprocess.run(['pkill', '-f', 'manage.py runserver'], 
                      capture_output=True, text=True)
        print("🧹 Cleared existing servers")
        time.sleep(2)
    except:
        pass
    
    # Find available port
    port = find_available_port(8000)
    if not port:
        print("❌ No available ports found")
        return
    
    print(f"✅ Using port: {port}")
    
    # Change to project directory
    os.chdir("/home/ariel/Python Project")
    
    # Start server in background
    try:
        subprocess.Popen([
            'bash', '-c', 
            f'source venv/bin/activate && python manage.py runserver {port} > server.log 2>&1'
        ])
        
        # Wait and test
        time.sleep(4)
        
        # Test if server is running
        try:
            import urllib.request
            urllib.request.urlopen(f'http://localhost:{port}/admin/', timeout=5)
            print("✅ Server started successfully!")
        except:
            print("⚠️  Server starting... (may take a moment)")
        
        # Show URLs
        print(f"\n🌐 Access URLs:")
        print(f"• Admin: http://localhost:{port}/admin/")
        print(f"• API: http://localhost:{port}/api/")
        print(f"• Dashboard: http://localhost:{port}/dashboard/")
        
        print(f"\n🔑 Credentials:")
        print(f"• User: admin")
        print(f"• Pass: admin123")
        
        print(f"\n🛑 To stop: pkill -f 'manage.py runserver'")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()