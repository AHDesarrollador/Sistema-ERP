from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_manager = models.BooleanField(default=False)
    can_view_dashboard = models.BooleanField(default=False, help_text="Can access dashboard")
    can_manage_inventory = models.BooleanField(default=False, help_text="Can manage inventory")
    can_manage_sales = models.BooleanField(default=False, help_text="Can manage sales")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        permissions = [
            ("view_dashboard", "Can view dashboard"),
            ("manage_inventory", "Can manage inventory"),
            ("manage_sales", "Can manage sales"),
        ]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
