#!/usr/bin/env python
"""
Test database connection methods
"""
import subprocess
import os

def test_postgresql_methods():
    """Test different PostgreSQL connection methods"""
    
    print("🔍 Testing PostgreSQL connection methods...")
    
    # Method 1: Try with psql command as current user
    print("\n1. Testing psql with current user...")
    try:
        result = subprocess.run(['psql', '-U', os.getenv('USER'), '-d', 'postgres', '-c', '\\l'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Connected with current user")
            print(result.stdout)
            return "peer_auth"
        else:
            print(f"❌ Failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Method 2: Try with postgres user
    print("\n2. Testing psql with postgres user...")
    try:
        result = subprocess.run(['sudo', '-u', 'postgres', 'psql', '-c', '\\l'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Connected with postgres user")
            return "postgres_user"
        else:
            print(f"❌ Failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Method 3: Check postgres configuration
    print("\n3. Checking PostgreSQL configuration...")
    try:
        result = subprocess.run(['sudo', '-u', 'postgres', 'psql', '-c', 'SHOW config_file;'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Config file location: {result.stdout}")
        else:
            print(f"❌ Failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def get_postgres_info():
    """Get PostgreSQL connection information"""
    
    print("\n📋 PostgreSQL Information:")
    
    # Get PostgreSQL version
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Version: {result.stdout.strip()}")
    except:
        pass
    
    # Check if we can connect to create database
    print("\n🔧 Creating database for ERP system...")
    try:
        # Try to create database as current user
        result = subprocess.run([
            'createdb', '-U', os.getenv('USER'), 'erp_dashboard_db'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database 'erp_dashboard_db' created successfully")
            return True
        elif "already exists" in result.stderr:
            print("ℹ️  Database 'erp_dashboard_db' already exists")
            return True
        else:
            print(f"❌ Failed to create database: {result.stderr}")
    except Exception as e:
        print(f"❌ Error creating database: {e}")
    
    return False

def main():
    print("🧪 PostgreSQL Connection Test")
    print("=" * 40)
    
    # Test connection methods
    method = test_postgresql_methods()
    
    # Try to create database
    db_ready = get_postgres_info()
    
    if db_ready:
        print("\n✅ PostgreSQL is ready for Django!")
        print("\nNext steps:")
        print("1. Update .env file with correct credentials")
        print("2. Run Django migrations")
        print("3. Create sample data")
    else:
        print("\n❌ PostgreSQL setup needs attention")
        print("\nTry these commands:")
        print("sudo -u postgres createdb erp_dashboard_db")
        print("sudo -u postgres psql -c \"ALTER USER postgres PASSWORD 'newpassword';\"")

if __name__ == "__main__":
    main()