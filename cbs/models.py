# cbs/models.py
from django.db import models
from django.conf import settings



class Customer(models.Model):
    t24_customer_id = models.CharField(max_length=20, unique=True)
    # Banking-specific identity
    
    # KYC / Personal Information
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    id_number = models.CharField(max_length=50, unique=True, verbose_name="National ID / Passport")
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    
    # System metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} ({self.t24_customer_id})"

    class Meta:
        verbose_name = "Banking Customer"
        verbose_name_plural = "Banking Customers"



class Account(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    t24_customer_id = models.CharField(max_length=20, null=True, blank=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    account_type = models.CharField(max_length=20, choices=[('SAV', 'Savings'), ('CUR', 'Current')])
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return f"{self.account_number}"



class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('CR', 'Credit'), ('DR', 'Debit')])
    reference = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    contra_account = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        ordering = ['-created_at']
