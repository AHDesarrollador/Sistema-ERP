#!/usr/bin/env python3
"""
Test the dashboard functionality
"""
import subprocess
import time
import requests

def test_dashboard():
    print("🧪 Testing ERP Dashboard Functionality")
    print("="*50)
    
    # Test server response
    try:
        response = requests.get('http://localhost:8000/dashboard/')
        if response.status_code == 200:
            print("✅ Dashboard page loads correctly")
            print(f"   Content length: {len(response.content)} bytes")
        else:
            print(f"❌ Dashboard page error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard connection error: {e}")
        return False
    
    # Test API endpoints that dashboard uses
    token = "b5b2f64f0fd8a0c6736bfe7b5b688d0f1083555b"
    headers = {'Authorization': f'Token {token}'}
    
    endpoints = {
        'Inventory Stats': '/api/inventory/stats/',
        'Sales Stats': '/api/sales/stats/',
        'Products': '/api/inventory/products/',
    }
    
    print("\n📊 Testing API endpoints used by dashboard:")
    
    all_working = True
    for name, endpoint in endpoints.items():
        try:
            response = requests.get(f'http://localhost:8000{endpoint}', headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {name}: OK ({len(str(data))} bytes)")
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
                all_working = False
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            all_working = False
    
    return all_working

def show_dashboard_info():
    print("\n" + "="*60)
    print("📊 ERP DASHBOARD - READY TO USE!")
    print("="*60)
    
    print("\n🌐 Access Information:")
    print("• Dashboard URL: http://localhost:8000/dashboard/")
    print("• Login not required for dashboard")
    print("• Data loads automatically with API token")
    
    print("\n🔑 API Token (pre-configured):")
    print("b5b2f64f0fd8a0c6736bfe7b5b688d0f1083555b")
    
    print("\n📈 Dashboard Features:")
    print("• ✅ Real-time stats cards")
    print("• ✅ Sales performance chart")
    print("• ✅ Inventory status pie chart") 
    print("• ✅ Top products by value chart")
    print("• ✅ Auto-refresh every 30 seconds")
    print("• ✅ Manual refresh button")
    
    print("\n💡 What you'll see:")
    print("• Total Products: Live count from database")
    print("• Stock Value: Total inventory value")
    print("• Low Stock Items: Products below minimum")
    print("• Monthly Sales: This month's revenue")
    print("• Interactive charts with real data")
    
    print("\n🎯 Next Steps:")
    print("1. Open: http://localhost:8000/dashboard/")
    print("2. Wait for charts to load (2-3 seconds)")
    print("3. Explore the interactive visualizations")
    print("4. Use 'Refresh Data' button to update")
    print("5. Check browser console (F12) for debug info")

def main():
    # Test dashboard
    if test_dashboard():
        print("\n🎉 All tests passed!")
        show_dashboard_info()
    else:
        print("\n⚠️  Some tests failed. Check the server and try again.")
        print("\nTo restart server:")
        print("cd 'Python Project'")
        print("python3 run.py")

if __name__ == "__main__":
    main()