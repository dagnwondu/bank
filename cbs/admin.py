from django.contrib import admin
from .models import Account, Transaction
from .models import Customer

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'account_type', 'balance')
    search_fields = ('account_number',)
    list_filter = ( 'account_type',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'account', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'created_at',)
    readonly_fields = ('created_at',) # Keeps it audit-friendly

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Display the most important banking fields in the list view
    list_display = ('full_name', 't24_customer_id', 'id_number', 'phone_number')
    
    # Enable search for quick lookups by staff
    search_fields = ('full_name', 't24_customer_id', 'id_number')
    
    # Organize fields if you have a lot of them
    fieldsets = (
        ('Account Details', {
            'fields': ('t24_customer_id',)
        }),
        ('Personal Information', {
            'fields': ('full_name', 'date_of_birth', 'id_number', 'phone_number', 'address')
        }),
    )