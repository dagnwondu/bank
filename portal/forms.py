# portal/forms.py
from django import forms
from cbs.models import Account

class TransferForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            # Explicitly access the customer record linked to the user
            # Assuming your model relationship is defined as 'customer'
            customer = getattr(self.user, 'customer', None)
            
            if customer:
                self.fields['source_account'].queryset = Account.objects.filter(customer=customer)
            else:
                self.fields['source_account'].queryset = Account.objects.none()
    source_account = forms.ModelChoiceField(
        queryset=Account.objects.none(), # Will set in __init__
        widget=forms.Select(attrs={'class': 'w-full mt-1 p-3 border rounded-lg'})
    )
    beneficiary = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'class': 'w-full mt-1 p-3 border rounded-lg', 'placeholder': 'Account Number'})
    )
    amount = forms.DecimalField(
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'w-full mt-1 p-3 border rounded-lg', 'placeholder': '0.00'})
    )



# portal/forms.py
from django import forms
from cbs.models import Account

class ExternalTransferForm(forms.Form):
    # Standard Fields
    source_account = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        widget=forms.Select(attrs={'class': 'w-full mt-1 p-3 border rounded-lg'})
    )
    beneficiary_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'w-full mt-1 p-3 border rounded-lg'}))
    beneficiary_iban = forms.CharField(max_length=34, widget=forms.TextInput(attrs={'class': 'w-full mt-1 p-3 border rounded-lg'}))
    bank_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'w-full mt-1 p-3 border rounded-lg'}))
    swift_code = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'w-full mt-1 p-3 border rounded-lg'}))
    amount = forms.DecimalField(min_value=0.01, widget=forms.NumberInput(attrs={'class': 'w-full mt-1 p-3 border rounded-lg'}))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            # Fix: Retrieve the actual Customer instance linked to the user
            # If the user is a staff/admin, 'customer' might not exist, so use getattr
            customer = getattr(self.user, 'customer', None)
            
            if customer:
                # Query using the instance, not the related user object
                self.fields['source_account'].queryset = Account.objects.filter(customer=customer)
            else:
                self.fields['source_account'].queryset = Account.objects.none()
