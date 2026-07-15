from django.shortcuts import render
from django.contrib import messages
from authentication.views import role_required
from core.services import T24Client

@role_required(['customer'])
def customer_dashboard(request):
    client = T24Client()
    
    # Fetch accounts - returns list or None
    accounts = client.get_accounts(request.user.t24_customer_id)
    
    if accounts is None:
        messages.error(request, "Unable to connect to the banking core. Please try again.")
        accounts = []

    context = {
        "user": request.user,
        "accounts": accounts,
        "greeting": "Welcome back, Financial Wizard!"
    }
    return render(request, 'portal/customer_dashboard.html', context)
def get_customer_data(user):
    # This lookup is only possible because of that unique T24 ID
    if not user.t24_customer_id:
        return "No T24 mapping found."
    
    # Use the ID to call the T24 IRIS API
    client = T24Client()
    return client.get_accounts(customer_id=user.t24_customer_id)