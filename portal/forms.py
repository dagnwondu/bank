# portal/forms.py
from django import forms
from cbs.models import Account


class TransferForm(forms.Form):
# portal/forms.py

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            # Assuming you store the T24 ID in the User profile or a custom setting
            # If your user object has access to their T24 ID:
            t24_id = getattr(self.user, 't24_customer_id', None)
            
            if t24_id:
                self.fields['source_account'].queryset = Account.objects.filter(
                    t24_customer_id=t24_id, 
                    is_active=True # Only allow transfers from active accounts
                )
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
    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source_account')
        amount = cleaned_data.get('amount')

        if source:
            # Business Rule: Ensure account is active
            if not source.is_active:
                raise forms.ValidationError("This account is currently restricted.")
            
            # Business Rule: Check balance
            if amount and source.balance < amount:
                raise forms.ValidationError("Insufficient funds.")
                
        return cleaned_data



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
    # portal/forms.py

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            # Assuming you store the T24 ID in the User profile or a custom setting
            # If your user object has access to their T24 ID:
            t24_id = getattr(self.user, 't24_customer_id', None)
            
            if t24_id:
                self.fields['source_account'].queryset = Account.objects.filter(
                    t24_customer_id=t24_id, 
                    is_active=True # Only allow transfers from active accounts
                )
            else:
                self.fields['source_account'].queryset = Account.objects.none()

        def clean(self):
            cleaned_data = super().clean()
            source = cleaned_data.get('source_account')
            amount = cleaned_data.get('amount')

            if source:
                # Business Rule: Ensure account is active
                if not source.is_active:
                    raise forms.ValidationError("This account is currently restricted.")
                
                # Business Rule: Check balance
                if amount and source.balance < amount:
                    raise forms.ValidationError("Insufficient funds.")
                    
            return cleaned_data