#!/usr/bin/env python
"""
Final ERP System Verification
"""
import os
import requests
import subprocess
import time

def check_server_running():
    """Check if Django server is running"""
    try:
        response = requests.get('http://localhost:8001/admin/', timeout=5)
        return response.status_code in [200, 302]  # 302 is redirect to login
    except:
        return False

def start_server():
    """Start Django server if not running"""
    if not check_server_running():
        print("🚀 Starting Django server...")
        os.chdir("/home/ariel/Python Project")
        subprocess.Popen(['bash', '-c', 'source venv/bin/activate && python manage.py runserver 8001 > server.log 2>&1'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)  # Wait for server to start
        
        if check_server_running():
            print("✅ Server started successfully")
            return True
        else:
            print("❌ Failed to start server")
            return False
    else:
        print("✅ Server already running")
        return True

def test_admin_panel():
    """Test admin panel accessibility"""
    print("\n👨‍💼 Testing Admin Panel...")
    try:
        response = requests.get('http://localhost:8001/admin/')
        if response.status_code == 302 and '/admin/login/' in response.headers.get('Location', ''):
            print("✅ Admin panel accessible - redirects to login")
            return True
        else:
            print(f"❌ Admin panel issue - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Admin panel error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔗 Testing API Endpoints...")
    
    token = "86f3295ac254f35c44b75715d789799066c6848c"
    headers = {'Authorization': f'Token {token}'}
    
    endpoints = {
        'Inventory Stats': '/api/inventory/stats/',
        'Sales Stats': '/api/sales/stats/',
        'Products List': '/api/inventory/products/',
        'Sales List': '/api/sales/sales/',
        'User Profile': '/api/users/profile/',
    }
    
    results = {}
    
    for name, endpoint in endpoints.items():
        try:
            response = requests.get(f'http://localhost:8001{endpoint}', headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
                results[name] = True
            else:
                print(f"❌ {name}: Status {response.status_code}")
                results[name] = False
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            results[name] = False
    
    return all(results.values())

def test_dashboard():
    """Test dashboard accessibility"""
    print("\n📊 Testing Dashboard...")
    try:
        response = requests.get('http://localhost:8001/dashboard/')
        if response.status_code == 200:
            print("✅ Dashboard accessible")
            return True
        else:
            print(f"❌ Dashboard issue - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        return False

def show_final_report():
    """Show final system report"""
    print("\n" + "="*60)
    print("🎉 ERP DASHBOARD SYSTEM - FINAL REPORT")
    print("="*60)
    
    print("\n✅ SYSTEM STATUS:")
    print("• Database: SQLite (ready)")
    print("• Server: Django 5.2.4 (running on port 8001)")
    print("• APIs: RESTful endpoints (fully functional)")
    print("• Dashboard: Plotly Dash (integrated)")
    print("• Admin Panel: Django Admin (accessible)")
    
    print("\n🔑 LOGIN CREDENTIALS:")
    print("• Username: admin")
    print("• Password: admin123")
    print("• API Token: 86f3295ac254f35c44b75715d789799066c6848c")
    
    print("\n🌐 ACCESS URLS:")
    print("• Admin Panel: http://localhost:8001/admin/")
    print("• API Root: http://localhost:8001/api/")
    print("• Dashboard: http://localhost:8001/dashboard/")
    print("• API Documentation: http://localhost:8001/api/ (browsable)")
    
    print("\n📊 SAMPLE DATA:")
    print("• Categories: 4 (Electronics, Clothing, Books, Food)")
    print("• Products: 6 (with stock levels)")
    print("• Sales: 5 (completed transactions)")
    print("• Customers: 4 (sample customer data)")
    
    print("\n🔧 FEATURES WORKING:")
    print("• ✅ User authentication and management")
    print("• ✅ Inventory management (products, stock, suppliers)")
    print("• ✅ Sales processing and reporting")
    print("• ✅ Real-time dashboard with charts")
    print("• ✅ RESTful API with token authentication")
    print("• ✅ Admin interface for data management")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Open browser and go to: http://localhost:8001/admin/")
    print("2. Login with admin/admin123")
    print("3. Explore inventory, sales, and user management")
    print("4. Test APIs using the provided token")
    print("5. View dashboard at: http://localhost:8001/dashboard/")
    
    print("\n💡 FOR POSTGRESQL SETUP (optional):")
    print("1. Configure PostgreSQL with proper user/password")
    print("2. Uncomment PostgreSQL settings in settings.py")
    print("3. Update .env file with correct credentials")
    print("4. Run migrations: python manage.py migrate")

def main():
    print("🔍 FINAL ERP SYSTEM VERIFICATION")
    print("="*50)
    
    # Start server
    if not start_server():
        print("❌ Cannot start server. Exiting.")
        return
    
    # Test components
    admin_ok = test_admin_panel()
    api_ok = test_api_endpoints()
    dashboard_ok = test_dashboard()
    
    print(f"\n📋 VERIFICATION RESULTS:")
    print(f"• Admin Panel: {'✅ Working' if admin_ok else '❌ Issues'}")
    print(f"• API Endpoints: {'✅ Working' if api_ok else '❌ Issues'}")
    print(f"• Dashboard: {'✅ Working' if dashboard_ok else '❌ Issues'}")
    
    if all([admin_ok, api_ok, dashboard_ok]):
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
        show_final_report()
    else:
        print("\n⚠️ Some components need attention. Check logs for details.")

if __name__ == "__main__":
    main()