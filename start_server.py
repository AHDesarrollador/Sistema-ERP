#!/usr/bin/env python
"""
Script to start the ERP Dashboard server
"""
import os
import subprocess
import sys

def main():
    print("🚀 Starting ERP Dashboard System...")
    print("=" * 50)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Activate virtual environment and start server
    if os.name == 'nt':  # Windows
        activate_cmd = r"venv\Scripts\activate"
        python_cmd = r"venv\Scripts\python"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
        python_cmd = "venv/bin/python"
    
    print("Starting Django server on http://localhost:8001")
    print("\n📋 Available URLs:")
    print("• Admin Panel: http://localhost:8001/admin/")
    print("• API Root: http://localhost:8001/api/")
    print("• Dashboard: http://localhost:8001/dashboard/")
    print("\n🔑 Login Credentials:")
    print("• Username: admin")
    print("• Password: admin123")
    print("• API Token: 86f3295ac254f35c44b75715d789799066c6848c")
    print("\n💡 Use Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the Django development server
        subprocess.run([python_cmd, "manage.py", "runserver", "8001"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except FileNotFoundError:
        print("❌ Error: Python virtual environment not found.")
        print("Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()