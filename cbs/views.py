from django.http import JsonResponse
from .models import Account

# cbs/views.py
def mock_t24_api_account_balance(request, account_number): # 'account_number' parameter name is now actually 't24_customer_id'
    # 1. Filter all accounts belonging to this customer ID
    accounts = Account.objects.filter(customer__t24_customer_id=account_number)
    
    if not accounts.exists():
        return JsonResponse({"error": "No accounts found"}, status=404)

    # 2. Serialize multiple accounts into a list
    data = [
        {
            "account_number": acc.account_number,
            "balance": float(acc.balance),
            "currency": "ETB",
            "status": acc.status
        }
        for acc in accounts
    ]
    
    return JsonResponse(data, safe=False)