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
    


import requests
import logging
from django.conf import settings
from requests.exceptions import RequestException

# Initialize logger for audit trails
logger = logging.getLogger(__name__)

class T24Client:
    def __init__(self):
        self.base_url = settings.T24_API_URL
        self.headers = {
            "Authorization": f"Bearer {settings.T24_API_TOKEN}",
            "Content-Type": "application/json"
        }

    def get_accounts(self, t24_customer_id):
        url = f"{self.base_url}/api/accounts/{t24_customer_id}/"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            # ADD THIS:
            if response.status_code != 200:
                print(f"DEBUG: T24 API returned status {response.status_code}: {response.text}")
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"DEBUG: Connection error: {e}")
            return None
        # Temporary hard-coded mock to verify your Portal dashboard display
    # def get_accounts(self, t24_customer_id):
    #     # Skip the actual API call
    #     return [
    #         {"id": "10121284-001", "balance": 5000.00, "account_type": "Savings"},
    #         {"id": "10121284-002", "balance": 150.00, "account_type": "Current"}
    #     ]