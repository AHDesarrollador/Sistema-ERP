#!/usr/bin/env python
"""
ERP Dashboard Startup Script - Version 2.0
Handles port conflicts and provides multiple options
"""
import os
import subprocess
import sys
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
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + 100):
        if check_port(port):
            return port
    return None

def kill_django_servers():
    """Kill any running Django servers"""
    try:
        result = subprocess.run(['pkill', '-f', 'manage.py runserver'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("🧹 Stopped existing Django servers")
            time.sleep(2)
        return True
    except:
        return False

def start_server(port):
    """Start Django server on specified port"""
    project_dir = "/home/ariel/Python Project"
    os.chdir(project_dir)
    
    print(f"🚀 Starting Django server on port {port}...")
    
    try:
        # Use subprocess.Popen for non-blocking start
        process = subprocess.Popen([
            'bash', '-c', 
            f'source venv/bin/activate && python manage.py runserver {port}'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment and check if process started successfully
        time.sleep(3)
        
        if process.poll() is None:  # Process is still running
            print(f"✅ Server started successfully on port {port}")
            return port, process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start: {stderr.decode()}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return None, None

def show_system_info(port):
    """Show system information and URLs"""
    print("\n" + "="*60)
    print("🎉 ERP DASHBOARD SYSTEM STARTED SUCCESSFULLY!")
    print("="*60)
    
    print(f"\n🌐 ACCESS URLS:")
    print(f"• Admin Panel: http://localhost:{port}/admin/")
    print(f"• API Root: http://localhost:{port}/api/")
    print(f"• Dashboard: http://localhost:{port}/dashboard/")
    
    print(f"\n🔑 LOGIN CREDENTIALS:")
    print(f"• Username: admin")
    print(f"• Password: admin123")
    print(f"• API Token: 86f3295ac254f35c44b75715d789799066c6848c")
    
    print(f"\n🔗 API EXAMPLES:")
    print(f"curl -H \"Authorization: Token 86f3295ac254f35c44b75715d789799066c6848c\" \\")
    print(f"     http://localhost:{port}/api/inventory/stats/")
    
    print(f"\n💡 FEATURES AVAILABLE:")
    print(f"• ✅ Complete inventory management")
    print(f"• ✅ Sales processing and reporting") 
    print(f"• ✅ User authentication and management")
    print(f"• ✅ Interactive dashboard with charts")
    print(f"• ✅ RESTful API with token authentication")
    print(f"• ✅ Admin interface for data management")
    
    print(f"\n🛑 TO STOP THE SERVER:")
    print(f"Press Ctrl+C or run: pkill -f 'manage.py runserver'")

def test_server(port):
    """Test if server is responding"""
    try:
        import urllib.request
        urllib.request.urlopen(f'http://localhost:{port}/admin/', timeout=5)
        return True
    except:
        return False

def main():
    print("🚀 ERP DASHBOARD SYSTEM STARTUP")
    print("="*50)
    
    # Step 1: Clean up any existing servers
    print("🧹 Cleaning up existing servers...")
    kill_django_servers()
    
    # Step 2: Find available port
    print("🔍 Finding available port...")
    port = find_available_port(8000)
    
    if not port:
        print("❌ No available ports found. Please free up some ports.")
        return
    
    print(f"✅ Found available port: {port}")
    
    # Step 3: Start server
    server_port, process = start_server(port)
    
    if not server_port:
        print("❌ Failed to start server. Check for errors above.")
        return
    
    # Step 4: Test server
    print("🧪 Testing server response...")
    if test_server(server_port):
        print("✅ Server is responding correctly")
    else:
        print("⚠️  Server started but may need a moment to be ready")
    
    # Step 5: Show information
    show_system_info(server_port)
    
    # Step 6: Keep script running
    try:
        print(f"\n📱 Server running on http://localhost:{server_port}")
        print("Press Ctrl+C to stop...")
        process.wait()  # Wait for the server process
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        process.terminate()
        print("✅ Server stopped successfully")

if __name__ == "__main__":
    main()