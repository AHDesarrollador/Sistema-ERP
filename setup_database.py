#!/usr/bin/env python
"""
Script to setup and verify database connection
"""
import os
import sys
import subprocess
import psycopg2

def test_postgresql_connection():
    """Test PostgreSQL connection with different common passwords"""
    
    common_passwords = [
        'postgres',  # Most common default
        'password',  # Current .env setting
        '123456',
        'admin',
        '',  # No password
    ]
    
    print("🔍 Testing PostgreSQL connection...")
    
    for password in common_passwords:
        try:
            conn = psycopg2.connect(
                host='localhost',
                port='5432',
                user='postgres',
                password=password,
                database='postgres'  # Connect to default database first
            )
            conn.close()
            print(f"✅ Connection successful with password: '{password}'")
            return password
        except psycopg2.OperationalError as e:
            if "password authentication failed" in str(e):
                continue
            else:
                print(f"❌ Connection failed: {e}")
                return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    print("❌ Could not connect with any common password")
    return None

def create_database(password):
    """Create the ERP database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            user='postgres',
            password=password,
            database='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'erp_dashboard_db'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE erp_dashboard_db")
            print("✅ Created database: erp_dashboard_db")
        else:
            print("ℹ️  Database erp_dashboard_db already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def update_env_file(password):
    """Update .env file with correct password"""
    env_path = "/home/ariel/Python Project/.env"
    
    try:
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        with open(env_path, 'w') as f:
            for line in lines:
                if line.startswith('DATABASE_PASSWORD='):
                    f.write(f'DATABASE_PASSWORD={password}\n')
                else:
                    f.write(line)
        
        print(f"✅ Updated .env file with password: '{password}'")
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def setup_django():
    """Setup Django with correct database"""
    project_dir = "/home/ariel/Python Project"
    
    try:
        os.chdir(project_dir)
        
        # Activate virtual environment and run Django commands
        commands = [
            "source venv/bin/activate && python manage.py migrate",
            "source venv/bin/activate && python create_sample_data.py"
        ]
        
        for cmd in commands:
            print(f"🔄 Running: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Command successful")
                if result.stdout:
                    print(result.stdout)
            else:
                print(f"❌ Command failed: {result.stderr}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up Django: {e}")
        return False

def main():
    print("🚀 ERP Database Setup Script")
    print("=" * 40)
    
    # Test PostgreSQL connection
    password = test_postgresql_connection()
    
    if password is None:
        print("\n❌ Could not connect to PostgreSQL.")
        print("Please check that:")
        print("1. PostgreSQL is running (sudo systemctl start postgresql)")
        print("2. You know the postgres user password")
        print("\nTo reset postgres password:")
        print("sudo -u postgres psql")
        print("ALTER USER postgres PASSWORD 'newpassword';")
        return
    
    # Update .env file
    if not update_env_file(password):
        return
    
    # Create database
    if not create_database(password):
        return
    
    # Setup Django
    if not setup_django():
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Database Information:")
    print(f"• Database: erp_dashboard_db")
    print(f"• User: postgres") 
    print(f"• Password: {password}")
    print(f"• Host: localhost")
    print(f"• Port: 5432")
    
    print("\n🔑 Django Admin:")
    print("• Username: admin")
    print("• Password: admin123")
    
    print("\n🌐 URLs:")
    print("• Admin: http://localhost:8001/admin/")
    print("• API: http://localhost:8001/api/")
    print("• Dashboard: http://localhost:8001/dashboard/")

if __name__ == "__main__":
    main()