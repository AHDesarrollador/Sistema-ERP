#!/usr/bin/env python
"""
Fix admin login issues - Reset credentials completely
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_dashboard_project.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

def reset_admin_user():
    """Reset admin user completely"""
    print("🔧 Resetting admin user...")
    
    # Delete existing admin user if exists
    try:
        existing_admin = User.objects.filter(username='admin').first()
        if existing_admin:
            existing_admin.delete()
            print("🗑️  Deleted existing admin user")
    except:
        pass
    
    # Create fresh admin user
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@erp.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    
    # Set admin privileges
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.is_active = True
    admin_user.save()
    
    print("✅ Created new admin user:")
    print(f"   Username: admin")
    print(f"   Password: admin123")
    print(f"   Email: admin@erp.com")
    print(f"   Staff: {admin_user.is_staff}")
    print(f"   Superuser: {admin_user.is_superuser}")
    print(f"   Active: {admin_user.is_active}")
    
    return admin_user

def test_authentication():
    """Test authentication methods"""
    print("\n🧪 Testing authentication...")
    
    # Test 1: Django authenticate
    user = authenticate(username='admin', password='admin123')
    if user:
        print("✅ Django authentication: SUCCESS")
        print(f"   User: {user.username}")
        print(f"   Active: {user.is_active}")
        print(f"   Staff: {user.is_staff}")
    else:
        print("❌ Django authentication: FAILED")
    
    # Test 2: Manual password check
    try:
        admin_user = User.objects.get(username='admin')
        if admin_user.check_password('admin123'):
            print("✅ Password check: SUCCESS")
        else:
            print("❌ Password check: FAILED")
    except User.DoesNotExist:
        print("❌ User does not exist")
    
    return user

def create_api_token(user):
    """Create API token"""
    print("\n🔑 Creating API token...")
    
    # Delete existing token
    Token.objects.filter(user=user).delete()
    
    # Create new token
    token = Token.objects.create(user=user)
    print(f"✅ New API token: {token.key}")
    
    return token.key

def verify_database():
    """Verify database state"""
    print("\n📊 Database verification...")
    
    total_users = User.objects.count()
    admin_users = User.objects.filter(is_superuser=True).count()
    active_users = User.objects.filter(is_active=True).count()
    
    print(f"Total users: {total_users}")
    print(f"Admin users: {admin_users}")
    print(f"Active users: {active_users}")
    
    # List all users
    print("\nAll users:")
    for user in User.objects.all():
        print(f"  • {user.username} - Active: {user.is_active} - Admin: {user.is_superuser}")

def create_test_user():
    """Create additional test user"""
    print("\n👤 Creating test user...")
    
    # Delete if exists
    User.objects.filter(username='testuser').delete()
    
    test_user = User.objects.create_user(
        username='testuser',
        email='test@erp.com',
        password='test123',
        is_active=True
    )
    
    print(f"✅ Test user created: testuser/test123")
    return test_user

def show_login_instructions():
    """Show detailed login instructions"""
    print("\n" + "="*60)
    print("🎯 LOGIN INSTRUCTIONS")
    print("="*60)
    
    print("\n🌐 ADMIN PANEL LOGIN:")
    print("1. Go to: http://localhost:8000/admin/")
    print("2. Username: admin")
    print("3. Password: admin123")
    print("4. Click 'Log in'")
    
    print("\n🔧 TROUBLESHOOTING:")
    print("• Clear browser cache and cookies")
    print("• Try incognito/private browsing mode")
    print("• Check if server is running on correct port")
    print("• Verify no typos in username/password")
    
    print("\n🔗 API ACCESS:")
    print("• Token: [Will be shown below]")
    print("• Header: Authorization: Token [your-token]")
    
    print("\n📱 ALTERNATIVE LOGIN:")
    print("• Test user: testuser/test123")
    print("• (Regular user, not admin)")

def main():
    print("🔐 ADMIN LOGIN FIX SCRIPT")
    print("="*50)
    
    # Step 1: Reset admin user
    admin_user = reset_admin_user()
    
    # Step 2: Test authentication
    auth_user = test_authentication()
    
    if not auth_user:
        print("❌ Authentication failed even after reset!")
        print("There might be a deeper issue with the Django setup.")
        return
    
    # Step 3: Create API token
    token = create_api_token(admin_user)
    
    # Step 4: Verify database
    verify_database()
    
    # Step 5: Create test user
    create_test_user()
    
    # Step 6: Show instructions
    show_login_instructions()
    
    print(f"\n🔑 FINAL CREDENTIALS:")
    print(f"Admin User: admin")
    print(f"Admin Pass: admin123")
    print(f"API Token: {token}")
    
    print(f"\n✅ LOGIN SHOULD NOW WORK!")
    print(f"Try: http://localhost:8000/admin/")

if __name__ == '__main__':
    main()