from cbs.models import Account, Transaction
import requests
from django.conf import settings
# core/services.py

class T24MockEngine:
    @staticmethod
    def process_transaction(account_id, amount, tx_type):
        """Simulates the core banking transaction engine logic."""
        account = Account.objects.get(account_number=account_id)
        
        # Validation Logic (The 'Core' stuff)
        if tx_type == 'DR' and account.balance < amount:
            return {"status": "error", "message": "Insufficient funds"}
            
        # Update State
        if tx_type == 'CR':
            account.balance += amount
        else:
            account.balance -= amount
        account.save()
        
        # Create Audit Log
        Transaction.objects.create(account=account, amount=amount, transaction_type=tx_type)
        
        return {"status": "success", "new_balance": account.balance}
    


class T24Client:
    def __init__(self):
        self.base_url = settings.T24_API_URL
        self.headers = {
            "Authorization": f"Bearer {settings.T24_API_TOKEN}",
            "Content-Type": "application/json"
        }

    # core/services.py
    def get_accounts(self, t24_customer_id):
        url = f"{self.base_url}/accounts/{t24_customer_id}/"        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            return data # Ensure this is a LIST
        
        return None