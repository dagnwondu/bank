from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = "admin", "Admin"
        FINANCE = "finance", "Finance"
        BUSINESS = "business", "Business"
        CUSTOMER = "customer", "Customer"

    # Core banking identity
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CUSTOMER
    )
    
    # Integration field for T24 IRIS API
    t24_customer_id = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        unique=True,
        help_text="The unique ID of the customer in the T24 Core Banking System."
    )
    t24_customer_accounts = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        unique=True,
        help_text="Account numbers associated with the customer in the T24 Core Banking System."
    )

    # Profile & Security
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Meta
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"

    def get_full_name(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()

    class Meta:
        verbose_name = "System User"
        permissions = [
            ("can_register_customers", "Can register customers"),
            ("can_view_customers", "Can view customer records"),
            ("can_edit_customers", "Can edit customer records"),
            ("can_delete_customers", "Can delete customer records"),
            ("can_view_reports", "Can view reports"),
            ("can_generate_reports", "Can generate reports"),
            ("can_manage_users", "Can manage user accounts"),
        ]