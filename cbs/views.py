from django.http import JsonResponse
from .models import Account

# cbs/views.py
def mock_t24_api_account_balance(request, customer_id):
    # Now the variable name matches the data being passed
    # Filter directly by the customer_id field on your Account model
    accounts = Account.objects.filter(t24_customer_id=customer_id)
    
    if not accounts.exists():
        return JsonResponse({"error": "No accounts found"}, status=404)

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