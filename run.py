#!/usr/bin/env python3
"""
Simple ERP System Launcher
Usage: python3 run.py
"""
import subprocess
import time
import os

def main():
    print("🚀 Starting ERP Dashboard System...")
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Kill any existing servers
    subprocess.run(['pkill', '-f', 'manage.py runserver'], 
                  capture_output=True, text=True)
    time.sleep(1)
    
    # Start server
    try:
        print("🔄 Starting on http://localhost:8000")
        subprocess.run([
            'bash', '-c', 
            'source venv/bin/activate && python manage.py runserver 8000'
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    main()