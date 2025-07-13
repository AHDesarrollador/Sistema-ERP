#!/usr/bin/env python
"""
Fix login issue - The USERNAME_FIELD is set to 'email' not 'username'
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_dashboard_project.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

def fix_admin_user():
    """Fix admin user with correct email authentication"""
    print("🔧 Setting up admin user for EMAIL authentication...")
    
    # Delete existing admin users
    User.objects.filter(username='admin').delete()
    User.objects.filter(email='admin@erp.com').delete()
    
    # Create admin user with proper email
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@erp.com',  # This will be the login field!
        password='admin123'
    )
    
    # Set admin privileges
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.is_active = True
    admin_user.save()
    
    print("✅ Admin user created:")
    print(f"   Username: {admin_user.username}")
    print(f"   Email: {admin_user.email}")
    print(f"   LOGIN WITH EMAIL: admin@erp.com")
    print(f"   Password: admin123")
    
    return admin_user

def test_authentication():
    """Test both username and email authentication"""
    print("\n🧪 Testing authentication methods...")
    
    # Test 1: Username authentication (should fail)
    user1 = authenticate(username='admin', password='admin123')
    print(f"Username auth (admin): {'✅ SUCCESS' if user1 else '❌ FAILED (expected)'}")
    
    # Test 2: Email authentication (should work)
    user2 = authenticate(username='admin@erp.com', password='admin123')  # Note: still uses 'username' parameter
    print(f"Email auth (admin@erp.com): {'✅ SUCCESS' if user2 else '❌ FAILED'}")
    
    # Test 3: Direct email authentication
    try:
        user3 = authenticate(email='admin@erp.com', password='admin123')
        print(f"Direct email auth: {'✅ SUCCESS' if user3 else '❌ FAILED'}")
    except:
        print("Direct email auth: ❌ NOT SUPPORTED")
    
    return user2 or user1

def create_api_token(user):
    """Create API token"""
    if not user:
        print("❌ Cannot create token - no user provided")
        return None
    
    # Delete existing token
    Token.objects.filter(user=user).delete()
    
    # Create new token
    token = Token.objects.create(user=user)
    print(f"✅ API token created: {token.key}")
    
    return token.key

def show_correct_login_info():
    """Show the correct login information"""
    print("\n" + "="*70)
    print("🎯 CORRECT LOGIN CREDENTIALS")
    print("="*70)
    
    print("\n🌐 ADMIN PANEL LOGIN:")
    print("URL: http://localhost:8000/admin/")
    print("👤 Username/Email: admin@erp.com")  # Use EMAIL not username!
    print("🔒 Password: admin123")
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("• LOGIN WITH EMAIL: admin@erp.com (NOT 'admin')")
    print("• The Username field in Django admin expects EMAIL")
    print("• This is because USERNAME_FIELD = 'email' in the User model")
    
    print("\n🔧 TROUBLESHOOTING:")
    print("• Make sure to use admin@erp.com as username")
    print("• Clear browser cache/cookies")
    print("• Try incognito mode")
    print("• Ensure server is running")

def create_alternative_admin():
    """Create alternative admin with simple username"""
    print("\n👤 Creating alternative admin user...")
    
    # Delete if exists
    User.objects.filter(email='simple@admin.com').delete()
    
    # Create simple admin
    simple_admin = User.objects.create_user(
        username='simple',
        email='simple@admin.com',
        password='simple123'
    )
    
    simple_admin.is_staff = True
    simple_admin.is_superuser = True
    simple_admin.is_active = True
    simple_admin.save()
    
    print("✅ Alternative admin created:")
    print("   Email (login): simple@admin.com")
    print("   Password: simple123")
    
    return simple_admin

def main():
    print("🔐 FINAL LOGIN FIX")
    print("="*50)
    
    # Fix admin user
    admin_user = fix_admin_user()
    
    # Test authentication
    authenticated_user = test_authentication()
    
    # Create token if authentication worked
    token = None
    if authenticated_user:
        token = create_api_token(authenticated_user)
    
    # Create alternative admin
    alt_admin = create_alternative_admin()
    
    # Test alternative admin
    print("\n🧪 Testing alternative admin...")
    alt_user = authenticate(username='simple@admin.com', password='simple123')
    print(f"Alternative admin: {'✅ SUCCESS' if alt_user else '❌ FAILED'}")
    
    if alt_user and not token:
        token = create_api_token(alt_user)
    
    # Show final instructions
    show_correct_login_info()
    
    print(f"\n🔑 FINAL SUMMARY:")
    print(f"Main Admin Email: admin@erp.com")
    print(f"Main Admin Password: admin123")
    print(f"Alternative Admin Email: simple@admin.com") 
    print(f"Alternative Password: simple123")
    if token:
        print(f"API Token: {token}")
    
    print(f"\n✅ LOGIN NOW WITH EMAIL ADDRESS!")

if __name__ == '__main__':
    main()