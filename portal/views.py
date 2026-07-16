from django.shortcuts import render , redirect
from django.contrib import messages
from authentication.views import role_required
from core.services import T24Client, Account
from .forms import TransferForm, ExternalTransferForm
from cbs.models import Transaction
 

@role_required(['customer'])
def customer_dashboard(request):
    client = T24Client()
    raw_accounts = client.get_accounts(request.user.t24_customer_id)
    context = {
        "user": request.user,
        "accounts": raw_accounts,
        "greeting": "Welcome back, Financial Wizard!"
    }
    return render(request, 'portal/customer_dashboard.html', context)
@role_required(['customer'])
def get_customer_data(user):
    # This lookup is only possible because of that unique T24 ID
    if not user.t24_customer_id:
        return "No T24 mapping found."
    
    # Use the ID to call the T24 IRIS API
    client = T24Client()
    return client.get_accounts(customer_id=user.t24_customer_id)
@role_required(['customer'])
def fund_transfer_page(request):
    # Initialize both forms
    internal_form = TransferForm(request.POST or None, user=request.user, prefix='internal')
    external_form = ExternalTransferForm(request.POST or None, user=request.user, prefix='external')

    if request.method == 'POST':
        transfer_type = request.POST.get('transfer_type')
        
        # Determine which form to validate based on the hidden input
        if transfer_type == 'external' and external_form.is_valid():
            # Process External Transfer logic here
            # e.g., external_form.save() or call T24 service
            messages.success(request, "External transfer initiated successfully.")
            return redirect('dashboard')
            
        elif transfer_type == 'internal' and internal_form.is_valid():
            # Process Internal Transfer logic here
            messages.success(request, "Internal transfer completed successfully.")
            return redirect('dashboard')
        
        else:
            messages.error(request, "Please correct the errors in the form.")

    return render(request, 'portal/fund_transfer_page.html', {
        'internal_form': internal_form,
        'external_form': external_form
    })


def transaction_list_partial(request):
    transactions = Transaction.objects.filter(
        account__t24_customer_id=request.user.t24_customer_id
    ).order_by('-created_at')[:5]
    
    return render(request, 'portal/partials/transaction_rows.html', {
        'transactions': transactions
    })